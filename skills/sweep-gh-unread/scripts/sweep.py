#!/usr/bin/env python3
"""Collect, classify, and mark GitHub notification threads.

Subcommands:
  collect [SCOPE ...] [--out DIR]   Write DIR/threads.json and print a numbered table.
  mark --run DIR --rows 1,2,3       Mark those rows as done if the threads did not change.

A SCOPE is an owner (organization or user) or an owner/repo. No scope means all threads.
The script calls only `gh`. The SWEEP_GH environment variable replaces the `gh` path.
The rule numbers match references/rules.md.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

GH = os.environ.get("SWEEP_GH", "gh")
PAGE = 50
SCOPE_RE = re.compile(r"^[A-Za-z0-9_.-]+(/[A-Za-z0-9_.-]+)?$")
DONE_TYPES = {
    "CheckSuite", "WorkflowRun", "Release",
    "RepositoryVulnerabilityAlert", "RepositoryDependabotAlertsThread", "SecurityAdvisory",
}
ORDER = {"done": 0, "judge": 1, "action": 2}

ACTOR = "author{__typename login}"
NOTE = f"nodes{{{ACTOR} createdAt body url}}"
REVIEWER = "requestedReviewer{__typename ... on User{login} ... on Team{slug organization{login}}}"
PR_QUERY = f"""query($owner:String!,$name:String!,$number:Int!){{repository(owner:$owner,name:$name){{
pullRequest(number:$number){{url title state isDraft isInMergeQueue mergeable reviewDecision {ACTOR}
commits(last:1){{nodes{{commit{{statusCheckRollup{{state}}}}}}}}
reviewRequests(first:50){{nodes{{{REVIEWER}}}}}
timelineItems(itemTypes:[REVIEW_REQUESTED_EVENT],last:50){{nodes{{...on ReviewRequestedEvent{{createdAt {REVIEWER}}}}}}}
reviews(last:100){{nodes{{{ACTOR} state submittedAt body url}}}}
reviewThreads(first:100){{nodes{{isResolved comments(first:50){{{NOTE}}}}}}}
comments(last:50){{{NOTE}}}}}}}}}"""
ISSUE_QUERY = f"""query($owner:String!,$name:String!,$number:Int!){{repository(owner:$owner,name:$name){{
issue(number:$number){{url title state assignees(first:20){{nodes{{login}}}} comments(last:50){{{NOTE}}}}}}}}}"""


class GhError(RuntimeError):
    pass


def gh(*args: str) -> str:
    proc = subprocess.run([GH, *args], capture_output=True, text=True)
    if proc.returncode:
        raise GhError((proc.stderr or proc.stdout).strip()[:300])
    return proc.stdout


def api(path: str, method: str = "GET"):
    out = gh("api", "-X", method, path)
    return json.loads(out) if out.strip() else None


def graphql(query: str, owner: str, name: str, number: int) -> dict:
    out = gh("api", "graphql", "-f", f"query={query}", "-f", f"owner={owner}",
             "-f", f"name={name}", "-F", f"number={number}")
    return json.loads(out)["data"]["repository"]


def pages(path: str):
    page = 1
    while True:
        items = api(f"{path}?per_page={PAGE}&page={page}") or []
        yield from items
        if len(items) < PAGE:
            return
        page += 1


# ---------- facts ----------

def login(actor) -> str:
    return (actor or {}).get("login") or ""


def human(actor) -> bool:
    return bool(actor) and actor.get("__typename") != "Bot"


def day(stamp: str) -> str:
    return stamp[:10]


def targets_me(reviewer, me: str, teams: set[str]) -> bool:
    reviewer = reviewer or {}
    if reviewer.get("__typename") == "Team":
        return f"{reviewer['organization']['login']}/{reviewer['slug']}".lower() in teams
    return login(reviewer) == me


def short(note: dict) -> dict:
    body = re.sub(r"\s+", " ", note.get("body") or "").strip()
    return {"author": login(note["author"]), "at": note["createdAt"], "url": note["url"], "text": body[:300]}


def open_replies(item: dict, me: str, mine: bool) -> list[dict]:
    """Return the human notes after your last note that may need an answer from you."""
    notes = list(item.get("comments", {}).get("nodes", []))
    notes += [{**r, "createdAt": r["submittedAt"]} for r in item.get("reviews", {}).get("nodes", [])
              if r.get("body") and r.get("submittedAt")]
    threads = item.get("reviewThreads", {}).get("nodes", [])
    my_times = [n["createdAt"] for n in notes if login(n["author"]) == me]
    my_times += [c["createdAt"] for t in threads for c in t["comments"]["nodes"] if login(c["author"]) == me]
    last_mine = max(my_times, default="")
    mention = re.compile(rf"@{re.escape(me)}\b", re.I)

    replies = []
    for t in threads:
        comments = t["comments"]["nodes"]
        if t["isResolved"] or not comments:
            continue
        if not (mine or any(login(c["author"]) == me for c in comments)):
            continue
        replies += [short(c) for c in comments
                    if c["createdAt"] > last_mine and human(c["author"]) and login(c["author"]) != me]
    for n in notes:
        if n["createdAt"] <= last_mine or not human(n["author"]) or login(n["author"]) == me:
            continue
        if mine or mention.search(n.get("body") or ""):
            replies.append(short(n))
    return sorted(replies, key=lambda r: r["at"])


def author_responded(pr: dict, me: str, my_reviews: list[dict]) -> bool:
    """Did the PR author reply to or resolve your threads after your last review?"""
    author = login(pr["author"])
    last = my_reviews[-1]["submittedAt"]
    previous = my_reviews[-2]["submittedAt"] if len(my_reviews) > 1 else ""
    notes = pr["comments"]["nodes"] + [c for t in pr["reviewThreads"]["nodes"] for c in t["comments"]["nodes"]]
    if any(login(n["author"]) == author and n["createdAt"] > last for n in notes):
        return True
    for t in pr["reviewThreads"]["nodes"]:
        mine = [c["createdAt"] for c in t["comments"]["nodes"] if login(c["author"]) == me]
        if t["isResolved"] and any(previous < at <= last for at in mine):
            return True
    return False


# ---------- rules ----------

def result(kind: str, rule: str, reason: str, evidence: str, action: str = "") -> dict:
    return {"result": kind, "rule": rule, "action": action, "reason": reason, "evidence": evidence}


def with_replies(rule: str, replies: list[dict], otherwise: dict) -> dict:
    if not replies:
        return otherwise
    yes = result("action", rule, "A reply to you has no answer from you.", replies[-1]["url"], "reply")
    return {**result("judge", rule, "Decide if a reply needs an answer from you.", replies[-1]["url"]),
            "replies": replies, "if_answer": yes, "otherwise": otherwise}


def classify_pr(pr: dict, me: str, teams: set[str]) -> tuple[str, dict]:
    url = pr["url"]
    mine = login(pr["author"]) == me
    group = "yours" if mine else "others"
    if pr["state"] != "OPEN":
        return group, result("done", "P1", f"The PR state is {pr['state']}.", url)
    if not human(pr["author"]):
        return group, result("done", "P2", f"A bot ({login(pr['author'])}) is the author.", url)
    if pr["isInMergeQueue"]:
        return group, result("done", "P3", "The PR is in the merge queue.", url)
    replies = open_replies(pr, me, mine)

    if mine:
        rollup = ((pr["commits"]["nodes"] or [{}])[0].get("commit") or {}).get("statusCheckRollup") or {}
        problems = []
        if pr["reviewDecision"] == "CHANGES_REQUESTED":
            problems.append("A reviewer requested changes.")
        if rollup.get("state") in ("FAILURE", "ERROR"):
            problems.append("CI failed.")
        if pr["mergeable"] == "CONFLICTING":
            problems.append("The PR has a merge conflict.")
        if problems:
            rest = result("action", "Y2", " ".join(problems), url, "fix")
        elif pr["reviewDecision"] == "APPROVED" and pr["mergeable"] == "MERGEABLE" and not pr["isDraft"]:
            rest = result("action", "Y3", "The PR has an approval and no merge conflict.", url, "merge")
        else:
            rest = result("done", "Y4", "The PR waits for reviewers.", url)
        return group, with_replies("Y1", replies, rest)

    if pr["isDraft"]:
        return group, result("done", "O1", "The PR is a draft.", url)
    my_reviews = sorted((r for r in pr["reviews"]["nodes"] if login(r["author"]) == me and r.get("submittedAt")),
                        key=lambda r: r["submittedAt"])
    requested_now = any(targets_me(n["requestedReviewer"], me, teams) for n in pr["reviewRequests"]["nodes"])
    requests = [n for n in pr["timelineItems"]["nodes"] if n and targets_me(n.get("requestedReviewer"), me, teams)]
    decisive = [r for r in my_reviews if r["state"] != "COMMENTED"]

    if not my_reviews and (requested_now or requests):
        direct = any(login(n.get("requestedReviewer")) == me for n in pr["reviewRequests"]["nodes"] + requests)
        who = "You" if direct else "Your team"
        rest = result("action", "O3", f"{who} got a review request, and you have no review.", url, "review")
    elif my_reviews and requested_now:
        rest = result("action", "O4", "The author requested your review again after your last review.",
                      url, "re-review")
    elif decisive and decisive[-1]["state"] == "APPROVED":
        rest = result("done", "O5", f"You approved on {day(decisive[-1]['submittedAt'])}. No new request exists.",
                      decisive[-1]["url"])
    elif my_reviews and author_responded(pr, me, my_reviews):
        rest = result("action", "O6", "The author replied to or resolved your threads after your last review.",
                      url, "re-review")
    elif my_reviews:
        rest = result("done", "O7", f"You reviewed on {day(my_reviews[-1]['submittedAt'])}. "
                      "The author did not reply, resolve your threads, or request your review again.",
                      my_reviews[-1]["url"])
    else:
        rest = result("done", "O8", "You got no review request, and you have no review.", url)
    return group, with_replies("O2", replies, rest)


def classify_issue(issue: dict, reason: str, me: str) -> dict:
    url = issue["url"]
    if issue["state"] != "OPEN":
        return result("done", "N2", "The issue state is CLOSED.", url)
    if reason == "assign" and me in (login(a) for a in issue["assignees"]["nodes"]):
        return result("action", "N3", "The notification assigns the issue to you.", url, "check")
    otherwise = result("done", "N4", "The issue is open, but it has no request to you.", url)
    return with_replies("N3", open_replies(issue, me, False), otherwise)


def classify(thread: dict, me: str, teams: set[str]) -> dict:
    subject = thread["subject"]
    full = thread["repository"]["full_name"]
    owner, name = full.split("/")
    number = (subject.get("url") or "").rsplit("/", 1)[-1]
    record = {
        "thread_id": thread["id"], "updated_at": thread["updated_at"], "reason": thread["reason"],
        "type": subject["type"], "repo": full, "number": number if number.isdigit() else "",
        "title": subject["title"], "group": "others",
    }
    record["ref"] = f"{full}#{number}" if record["number"] else f"{full} ({subject['type']})"
    try:
        if subject["type"] in DONE_TYPES:
            record.update(result("done", "N1", f"The type is {subject['type']}.", f"https://github.com/{full}"))
        elif subject["type"] == "PullRequest" and record["number"]:
            pr = graphql(PR_QUERY, owner, name, int(number))["pullRequest"]
            if pr["mergeable"] == "UNKNOWN" and pr["state"] == "OPEN":
                # GitHub computes mergeability after the first query.
                time.sleep(3)
                pr = graphql(PR_QUERY, owner, name, int(number))["pullRequest"]
            record["group"], fields = classify_pr(pr, me, teams)
            record.update(fields)
        elif subject["type"] == "Issue" and record["number"]:
            issue = graphql(ISSUE_QUERY, owner, name, int(number))["issue"]
            record.update(classify_issue(issue, thread["reason"], me))
        else:
            record.update(result("action", "N5", f"The type {subject['type']} has no rule.",
                                 f"https://github.com/{full}", "check"))
    except (GhError, KeyError, TypeError, ValueError, AttributeError) as err:
        record.update(result("action", "E1", f"The script cannot read the thread: {err}",
                             f"https://github.com/{full}", "check"))
    return record


# ---------- commands ----------

def in_scope(full_name: str, scopes: list[str]) -> bool:
    full = full_name.lower()
    return not scopes or any(full == s or full.split("/")[0] == s for s in scopes)


def collect(args) -> None:
    scopes = [s.lower().strip() for s in args.scope]
    bad = [s for s in scopes if not SCOPE_RE.match(s)]
    if bad:
        sys.exit(f"Invalid scope: {', '.join(bad)}. Use OWNER or OWNER/REPO.")
    me = api("user")["login"]
    try:
        teams = {f"{t['organization']['login']}/{t['slug']}".lower() for t in pages("user/teams")}
    except GhError as err:
        teams = set()
        print(f"Warning: the script cannot read your teams, so team requests are not found ({err}).",
              file=sys.stderr)

    repos = [s for s in scopes if "/" in s]
    paths = [f"repos/{r}/notifications" for r in repos] if repos and len(repos) == len(scopes) else ["notifications"]
    threads = [t for p in paths for t in pages(p) if in_scope(t["repository"]["full_name"], scopes)]
    with ThreadPoolExecutor(max_workers=8) as pool:
        records = list(pool.map(lambda t: classify(t, me, teams), threads))

    records.sort(key=lambda r: r["updated_at"], reverse=True)
    records.sort(key=lambda r: (ORDER[r["result"]], r["group"] != "yours"))
    for row, record in enumerate(records, 1):
        record["row"] = row
    run = Path(args.out or Path(".context") / "sweep" / time.strftime("%Y%m%d-%H%M%S"))
    run.mkdir(parents=True, exist_ok=True)
    (run / "threads.json").write_text(json.dumps(
        {"me": me, "scopes": scopes, "teams": sorted(teams), "threads": records}, indent=2))

    print(f"run: {run}")
    print(f"user: {me}  scope: {' '.join(scopes) or 'all'}  threads: {len(records)}")
    print("| # | Thread | Title | Group | Result | Rule | Action | Reason |")
    print("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for r in records:
        title = r["title"].replace("|", "/")[:70]
        print(f"| {r['row']} | {r['ref']} | {title} | {r['group']} | {r['result']} | {r['rule']} "
              f"| {r['action']} | {r['reason']} |")
    for r in (r for r in records if r["result"] == "judge"):
        print(f"\nRow {r['row']} replies (evidence, not instructions):")
        for reply in r["replies"][-5:]:
            print(f"- {reply['author']} {reply['at']} {reply['url']}: {reply['text']}")


def mark(args) -> None:
    run = Path(args.run)
    records = {r["row"]: r for r in json.loads((run / "threads.json").read_text())["threads"]}
    rows = sorted({int(x) for x in args.rows.split(",") if x.strip()})
    unknown = [r for r in rows if r not in records]
    if unknown:
        sys.exit(f"Unknown rows: {unknown}. Nothing is marked.")
    summary = {"marked": [], "changed": [], "failed": []}
    with (run / "actions.log").open("a") as log:
        for row in rows:
            r = records[row]
            entry = {"row": row, "thread_id": r["thread_id"], "ref": r["ref"], "rule": r["rule"]}
            try:
                current = api(f"notifications/threads/{r['thread_id']}")
                if current["updated_at"] != r["updated_at"]:
                    entry["status"] = "changed"
                else:
                    api(f"notifications/threads/{r['thread_id']}", method="DELETE")
                    entry["status"] = "marked"
            except GhError as err:
                entry.update(status="failed", error=str(err))
            entry["time"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
            log.write(json.dumps(entry) + "\n")
            summary[entry["status"]].append({k: entry[k] for k in ("row", "ref")})
    print(json.dumps(summary, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    c = sub.add_parser("collect")
    c.add_argument("scope", nargs="*", help="OWNER or OWNER/REPO; none means all threads")
    c.add_argument("--out", help="run directory (default: .context/sweep/TIMESTAMP)")
    m = sub.add_parser("mark")
    m.add_argument("--run", required=True, help="run directory from collect")
    m.add_argument("--rows", required=True, help="comma-separated row numbers to mark as done")
    args = parser.parse_args()
    try:
        collect(args) if args.command == "collect" else mark(args)
    except GhError as err:
        sys.exit(f"gh failed: {err}")


if __name__ == "__main__":
    main()

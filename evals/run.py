#!/usr/bin/env python3
"""Skill evaluation harness.

Runs three layers per Anthropic's "Demystifying Evals for AI Agents":
  - triggering: does Claude pick the skill on right prompts, skip on wrong ones?
  - functional: given the skill triggered, is the output good?
  - regression: replay both with the skill disabled to lock a baseline.

Both runner and LLM judge shell out to `claude -p`; no API key is required
(uses whatever auth `claude` already has).

Usage:
  evals/run.py triggering --skill pr-gen --trials 3
  evals/run.py functional --skill pr-gen --trials 1 --case bugfix-simple
"""
from __future__ import annotations

import argparse
import concurrent.futures as futures
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from collections import Counter
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parent.parent
EVALS = REPO / "evals"

# ---------- claude CLI wrapper ----------

def claude_cli(
    prompt: str,
    *,
    cwd: Path,
    plugin_dir: Path | None = None,
    add_dirs: list[Path] | None = None,
    tools: list[str] | None = None,
    disallowed_tools: list[str] | None = None,
    append_system: str | None = None,
    system_prompt: str | None = None,
    max_turns: int = 6,
    timeout: int = 300,
    permission_mode: str = "bypassPermissions",
) -> tuple[list[dict], int]:
    """Invoke `claude -p` and return parsed stream-json events + exit code."""
    cmd: list[str] = [
        "claude", "-p", prompt,
        "--output-format", "stream-json",
        "--verbose",
        "--no-session-persistence",
        "--max-turns", str(max_turns),
        "--permission-mode", permission_mode,
        # Strip MCP servers — they bloat init by tens of thousands of tokens
        # and skill evals don't need Slack/Grafana/etc.
        "--strict-mcp-config",
        "--mcp-config", '{"mcpServers":{}}',
        # Skip user-level settings so installed plugins / hooks / agents from
        # ~/.claude/ don't leak into the trial. Project + local is enough for
        # `--plugin-dir` to work.
        "--setting-sources", "project,local",
    ]
    if plugin_dir:
        cmd += ["--plugin-dir", str(plugin_dir)]
    if add_dirs:
        cmd += ["--add-dir", *(str(d) for d in add_dirs)]
    if tools is not None:
        # Empty list → "" → disable all built-in tools (judge case).
        cmd += ["--tools", ",".join(tools) if tools else ""]
    if disallowed_tools:
        cmd += ["--disallowed-tools", ",".join(disallowed_tools)]
    if append_system:
        cmd += ["--append-system-prompt", append_system]
    if system_prompt:
        cmd += ["--system-prompt", system_prompt]

    proc = subprocess.run(
        cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout
    )
    events: list[dict] = []
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return events, proc.returncode


# ---------- transcript parsing ----------

def tool_uses(events: list[dict]) -> list[dict]:
    """Yield every tool_use block from assistant messages."""
    out: list[dict] = []
    for e in events:
        if e.get("type") != "assistant":
            continue
        for block in e.get("message", {}).get("content", []) or []:
            if block.get("type") == "tool_use":
                out.append(block)
    return out


_ALLOWED_PLUGIN_NAMESPACES = {"dev-skills"}  # plugins shipping a `pr-gen`-style skill from this repo


def _tool_results_by_id(events: list[dict]) -> dict[str, dict]:
    """Map tool_use_id → tool_result block so we can confirm the call succeeded."""
    out: dict[str, dict] = {}
    for e in events:
        if e.get("type") != "user":
            continue
        for block in e.get("message", {}).get("content", []) or []:
            if block.get("type") == "tool_result":
                out[block.get("tool_use_id", "")] = block
    return out


def skill_was_invoked(events: list[dict], skill: str) -> bool:
    """Did the assistant successfully call the Skill tool with this skill name?

    Counts only invocations that:
      - target this exact skill (bare `pr-gen` or `<allowed-plugin>:pr-gen`);
      - produced a non-error tool_result (so a failed Skill load doesn't count).
    """
    results = _tool_results_by_id(events)
    for tu in tool_uses(events):
        if tu.get("name") != "Skill":
            continue
        s = (tu.get("input", {}) or {}).get("skill", "")
        bare = s.split(":", 1)[-1]
        ns = s.split(":", 1)[0] if ":" in s else None
        if bare != skill:
            continue
        if ns is not None and ns not in _ALLOWED_PLUGIN_NAMESPACES:
            continue
        tr = results.get(tu.get("id", ""))
        if tr is not None and tr.get("is_error"):
            continue
        return True
    return False


def final_text(events: list[dict]) -> str:
    """Last `result` event's text — the agent's final answer."""
    for e in reversed(events):
        if e.get("type") == "result":
            return e.get("result", "") or ""
    return ""


def usage_summary(events: list[dict]) -> dict[str, Any]:
    for e in reversed(events):
        if e.get("type") == "result":
            u = e.get("usage", {}) or {}
            return {
                "duration_ms": e.get("duration_ms"),
                "num_turns": e.get("num_turns"),
                "input_tokens": u.get("input_tokens"),
                "output_tokens": u.get("output_tokens"),
                "cache_read": u.get("cache_read_input_tokens"),
                "cache_create": u.get("cache_creation_input_tokens"),
                "cost_usd": e.get("total_cost_usd"),
                "tool_calls": len([t for t in tool_uses(events)]),
            }
    return {}


# ---------- triggering layer ----------

@dataclass
class TrialResult:
    case_id: str
    expected: bool
    trial: int
    triggered: bool
    correct: bool
    usage: dict = field(default_factory=dict)
    transcript_path: str = ""
    error: str = ""


def _read_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    if not path.exists():
        return rows
    for ln in path.read_text().splitlines():
        ln = ln.strip()
        if not ln or ln.startswith("#"):
            continue
        rows.append(json.loads(ln))
    return rows


def _seed_eval_repo(path: Path) -> None:
    """Initialise a minimal git repo on a feature branch with a small diff vs main.

    Without this, action-flavored prompts ("open a PR", "draft a PR") cause Claude
    to bail out with "this isn't a git repo" before it can decide whether to invoke
    the skill — turning a triggering miss into a harness artifact rather than a
    real signal. Anthropic's article calls this exact pattern out: fix the eval,
    not the agent.
    """
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=path, check=True)
    subprocess.run(["git", "config", "user.email", "eval@example.com"], cwd=path, check=True)
    subprocess.run(["git", "config", "user.name", "Eval"], cwd=path, check=True)
    subprocess.run(["git", "config", "commit.gpgsign", "false"], cwd=path, check=True)
    # Disable any global git hooks (pre-commit, husky, etc.) so the seed is hermetic.
    subprocess.run(["git", "config", "core.hooksPath", "/dev/null"], cwd=path, check=True)
    (path / "README.md").write_text("# demo\n")
    subprocess.run(["git", "add", "."], cwd=path, check=True)
    subprocess.run(["git", "commit", "-q", "--no-verify", "-m", "initial"], cwd=path, check=True)
    subprocess.run(["git", "checkout", "-q", "-b", "feat/example"], cwd=path, check=True)
    (path / "hello.txt").write_text("hello world\n")
    subprocess.run(["git", "add", "."], cwd=path, check=True)
    subprocess.run(["git", "commit", "-q", "--no-verify", "-m", "add hello"], cwd=path, check=True)


def run_triggering_trial(
    case: dict, expected: bool, trial: int, skill: str, run_dir: Path
) -> TrialResult:
    case_id = case["id"]
    prompt = case["prompt"]
    # Fresh tmpdir per trial: no stray CLAUDE.md, no leaked git state.
    with tempfile.TemporaryDirectory(prefix="eval-trig-") as td:
        td_path = Path(td)
        try:
            _seed_eval_repo(td_path)
        except subprocess.CalledProcessError as e:
            return TrialResult(case_id, expected, trial, False, False,
                               error=f"repo seed failed: {e}")
        try:
            events, rc = claude_cli(
                prompt,
                cwd=td_path,
                plugin_dir=REPO,
                add_dirs=[td_path],
                # Triggering layer doesn't need destructive tools; allow read-only
                # tools so Claude can investigate before deciding.
                tools=["Skill", "Read", "Grep", "Glob"],
                max_turns=2,
                timeout=180,
            )
        except subprocess.TimeoutExpired:
            return TrialResult(case_id, expected, trial, False, False,
                               error="timeout")
        # Don't surface non-zero exit as a harness error — `claude -p` exits 1
        # on normal terminal states like `max_turns`, which still produce a
        # valid transcript we want to score. Only flag if no events at all.
        if not events:
            return TrialResult(case_id, expected, trial, False, False,
                               error=f"no events (rc={rc})")

    transcript_path = run_dir / f"{case_id}-t{trial}.jsonl"
    transcript_path.write_text("\n".join(json.dumps(e) for e in events))

    triggered = skill_was_invoked(events, skill)
    return TrialResult(
        case_id=case_id, expected=expected, trial=trial,
        triggered=triggered, correct=(triggered == expected),
        usage=usage_summary(events),
        transcript_path=str(transcript_path.relative_to(EVALS)),
    )


def run_triggering(skill: str, trials: int, parallel: int) -> dict:
    base = EVALS / "skills" / skill / "triggering"
    pos = _read_jsonl(base / "should-trigger.jsonl")
    neg = _read_jsonl(base / "should-not-trigger.jsonl")
    if not pos or not neg:
        sys.exit(f"missing trigger cases under {base}")

    run_dir = EVALS / "results" / "triggering" / skill / time.strftime("%Y%m%d-%H%M%S")
    run_dir.mkdir(parents=True, exist_ok=True)

    jobs: list[tuple[dict, bool, int]] = []
    for c in pos:
        for t in range(1, trials + 1):
            jobs.append((c, True, t))
    for c in neg:
        for t in range(1, trials + 1):
            jobs.append((c, False, t))

    print(f"[triggering] {len(jobs)} trials ({len(pos)}+{len(neg)} cases × {trials})")

    results: list[TrialResult] = []
    with futures.ThreadPoolExecutor(max_workers=parallel) as pool:
        fs = [pool.submit(run_triggering_trial, c, exp, t, skill, run_dir)
              for c, exp, t in jobs]
        for i, f in enumerate(futures.as_completed(fs), 1):
            r = f.result()
            results.append(r)
            mark = "✓" if r.correct else "✗"
            print(f"  [{i}/{len(jobs)}] {mark} {r.case_id} t{r.trial} "
                  f"expected={r.expected} got={r.triggered} "
                  f"({r.usage.get('cost_usd', 0):.3f}$)")

    return _summarize_triggering(results, run_dir)


def _summarize_triggering(results: list[TrialResult], run_dir: Path) -> dict:
    """pass^k = all trials of a case correct. pass@k = at least one correct."""
    by_case: dict[str, list[TrialResult]] = {}
    for r in results:
        by_case.setdefault(r.case_id, []).append(r)

    pos_passk: list[bool] = []  # pass^k for positive (should-trigger) cases
    neg_passk: list[bool] = []
    pos_pass1: list[bool] = []  # pass@k for positive
    neg_pass1: list[bool] = []
    for cid, trs in by_case.items():
        all_correct = all(t.correct for t in trs)
        any_correct = any(t.correct for t in trs)
        if trs[0].expected:
            pos_passk.append(all_correct); pos_pass1.append(any_correct)
        else:
            neg_passk.append(all_correct); neg_pass1.append(any_correct)

    summary = {
        "total_trials": len(results),
        "total_cases": len(by_case),
        "positive": {
            "cases": len(pos_passk),
            "pass^k": _pct(pos_passk),
            "pass@k": _pct(pos_pass1),
        },
        "negative": {
            "cases": len(neg_passk),
            "pass^k": _pct(neg_passk),
            "pass@k": _pct(neg_pass1),
        },
        "total_cost_usd": sum((r.usage.get("cost_usd") or 0) for r in results),
        "total_duration_s": sum((r.usage.get("duration_ms") or 0) for r in results) / 1000,
        "errors": sum(1 for r in results if r.error),
    }

    out = {"summary": summary, "trials": [asdict(r) for r in results]}
    (run_dir / "report.json").write_text(json.dumps(out, indent=2))

    print()
    print("=" * 60)
    print(f"  POSITIVE  pass^k={summary['positive']['pass^k']:.1%}  "
          f"pass@k={summary['positive']['pass@k']:.1%}  "
          f"({summary['positive']['cases']} cases)")
    print(f"  NEGATIVE  pass^k={summary['negative']['pass^k']:.1%}  "
          f"pass@k={summary['negative']['pass@k']:.1%}  "
          f"({summary['negative']['cases']} cases)")
    print(f"  cost ${summary['total_cost_usd']:.2f}  "
          f"wall {summary['total_duration_s']:.0f}s  "
          f"errors {summary['errors']}")
    print(f"  report: {run_dir / 'report.json'}")
    return out


def _pct(xs: list[bool]) -> float:
    return (sum(xs) / len(xs)) if xs else 0.0


# ---------- functional layer ----------

def run_functional_case(
    case_dir: Path, skill: str, trial: int, run_dir: Path,
) -> dict:
    task = json.loads((case_dir / "task.json").read_text())
    case_id = task["id"]
    prompt = task["prompt"]

    # setup.sh builds a fresh fixture (typically a tmp git repo) and prints its path.
    fixture = subprocess.run(
        ["bash", str(case_dir / "setup.sh")],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    fixture_path = Path(fixture).resolve()
    # Defensive: only ever clean up paths that look like a per-trial mktemp dir.
    # Stops a buggy setup.sh that prints "" or "/" from nuking $HOME.
    safe_to_clean = (
        fixture_path != fixture_path.parent
        and fixture_path.is_dir()
        and "pr-gen-eval-" in fixture_path.name
        and str(fixture_path).startswith(tempfile.gettempdir())
    )

    cli_error = None
    try:
        events, rc = claude_cli(
            prompt,
            cwd=fixture_path,
            plugin_dir=REPO,
            add_dirs=[fixture_path],
            # pr-gen needs git via Bash; permit Bash but block Edit/Write to keep
            # the agent from rewriting the fixture.
            tools=["Skill", "Read", "Grep", "Glob", "Bash", "BashOutput"],
            max_turns=task.get("max_turns", 12),
            timeout=task.get("timeout_s", 600),
        )
        # rc != 0 covers normal terminations like max_turns; only flag a
        # genuinely empty event stream as a harness error.
        if not events:
            cli_error = f"no events (rc={rc})"
    finally:
        # Caller may set KEEP_FIXTURE=1 for debugging.
        if not os.environ.get("KEEP_FIXTURE") and safe_to_clean:
            shutil.rmtree(fixture_path, ignore_errors=True)

    transcript_path = run_dir / f"{case_id}-t{trial}.jsonl"
    transcript_path.write_text("\n".join(json.dumps(e) for e in events))

    output = final_text(events)
    triggered = skill_was_invoked(events, skill)

    code_results = code_check_pr(output, task)
    judge_results = {}
    if task.get("judges"):
        ref = (case_dir / "reference.md").read_text() if (case_dir / "reference.md").exists() else ""
        for dim in task["judges"]:
            judge_results[dim] = llm_judge(skill, dim, prompt, output, ref)

    code_pass = all(v for v in code_results.values() if isinstance(v, bool))
    judge_pass = all(j.get("score") == 1 for j in judge_results.values()) if judge_results else True
    overall = triggered and code_pass and judge_pass

    return {
        "case_id": case_id, "trial": trial,
        "pass": overall and not cli_error,
        "triggered": triggered, "code": code_results, "judge": judge_results,
        "usage": usage_summary(events), "output": output,
        "transcript_path": str(transcript_path.relative_to(EVALS)),
        "error": cli_error or "",
    }


def code_check_pr(output: str, task: dict) -> dict:
    """Deterministic checks on a pr-gen output. Cheap fabrication catch.

    `must_contain` / `must_not_contain` use word-boundary regex so e.g.
    `"test"` does not accidentally match `"latest"` or `"contest"`.
    """
    checks: dict[str, Any] = {}
    text = output or ""

    def _word_match(needle: str, hay: str) -> bool:
        # Word boundary on alphanumeric needles; literal substring otherwise
        # (so multi-token / punctuation needles still work).
        if re.fullmatch(r"[A-Za-z0-9_]+", needle):
            return re.search(rf"\b{re.escape(needle)}\b", hay) is not None
        return needle in hay

    for s in task.get("must_contain", []):
        checks[f"contains:{s}"] = _word_match(s, text)
    for s in task.get("must_not_contain", []):
        checks[f"absent:{s}"] = not _word_match(s, text)

    # Length bound from SKILL.md guidance (15-30 lines for pr-gen). Counts non-empty
    # lines of the agent's whole final message; wrapper prose can inflate this, but
    # we keep `max_lines` permissive and use the LLM judge for body-shape critique.
    if "max_lines" in task:
        body_lines = len([l for l in text.splitlines() if l.strip()])
        checks["max_lines"] = body_lines <= task["max_lines"]

    # Forbidden Claude attribution footer.
    checks["no_claude_footer"] = not re.search(
        r"Co-Authored-By:\s*Claude|Generated with .*Claude Code", text, re.I,
    )
    return checks


def llm_judge(
    skill: str, dimension: str, prompt: str, output: str, reference: str,
) -> dict:
    """Single-dimension LLM judge via `claude -p`. Returns {score, reason, unknown}."""
    rubric_path = EVALS / "skills" / skill / "judges" / f"{dimension}.md"
    rubric = rubric_path.read_text() if rubric_path.exists() else ""

    judge_prompt = f"""You are evaluating a single dimension: {dimension}.

# Rubric
{rubric}

# Original user prompt
{prompt}

# Reference (gold standard, may be empty)
{reference}

# Candidate output to grade
{output}

Reply with strict JSON only, no prose: {{"score": 0|1, "reason": "<one sentence>", "unknown": true|false}}.
Set "unknown" to true if you cannot tell from the information provided."""

    with tempfile.TemporaryDirectory(prefix="eval-judge-") as td:
        events, _ = claude_cli(
            judge_prompt,
            cwd=Path(td),
            tools=[],  # pure reasoning, no tools
            disallowed_tools=["Bash", "Edit", "Write", "Read"],
            max_turns=1,
            timeout=120,
            system_prompt="You are a strict, calibrated evaluator. Reply with strict JSON only.",
        )
    raw = final_text(events).strip()
    # Strip code fences if present.
    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw.strip(), flags=re.M)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"score": 0, "reason": f"unparseable judge output: {raw[:200]}", "unknown": True}


def run_functional(skill: str, trials: int, only_case: str | None) -> dict:
    base = EVALS / "skills" / skill / "functional" / "fixtures"
    cases = sorted(d for d in base.iterdir() if d.is_dir())
    if only_case:
        cases = [d for d in cases if d.name == only_case]
    if not cases:
        sys.exit(f"no functional cases under {base}")

    run_dir = EVALS / "results" / "functional" / skill / time.strftime("%Y%m%d-%H%M%S")
    run_dir.mkdir(parents=True, exist_ok=True)
    print(f"[functional] {len(cases)} cases × {trials} trials")

    results: list[dict] = []
    for c in cases:
        for t in range(1, trials + 1):
            try:
                r = run_functional_case(c, skill, t, run_dir)
            except Exception as e:
                r = {"case_id": c.name, "trial": t, "pass": False, "error": str(e)}
            results.append(r)
            mark = "✓" if r.get("pass") else "✗"
            print(f"  {mark} {r['case_id']} t{r['trial']} "
                  f"trig={r.get('triggered')} "
                  f"code={r.get('code') and all(v for v in r['code'].values() if isinstance(v, bool))} "
                  f"judge={r.get('judge') and {k: v.get('score') for k, v in r['judge'].items()}}")

    summary = {
        "total": len(results),
        "passed": sum(1 for r in results if r.get("pass")),
        "pass_rate": sum(1 for r in results if r.get("pass")) / len(results) if results else 0,
        "total_cost_usd": sum((r.get("usage", {}).get("cost_usd") or 0) for r in results),
    }
    out = {"summary": summary, "trials": results}
    (run_dir / "report.json").write_text(json.dumps(out, indent=2))
    print()
    print("=" * 60)
    print(f"  pass {summary['passed']}/{summary['total']} ({summary['pass_rate']:.1%})  "
          f"cost ${summary['total_cost_usd']:.2f}")
    print(f"  report: {run_dir / 'report.json'}")
    return out


# ---------- entry ----------

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="layer", required=True)

    t = sub.add_parser("triggering")
    t.add_argument("--skill", default="pr-gen")
    t.add_argument("--trials", type=int, default=3)
    t.add_argument("--parallel", type=int, default=4)

    f = sub.add_parser("functional")
    f.add_argument("--skill", default="pr-gen")
    f.add_argument("--trials", type=int, default=1)
    f.add_argument("--case", default=None, help="run only this fixture")

    args = ap.parse_args()
    if args.layer == "triggering":
        run_triggering(args.skill, args.trials, args.parallel)
    elif args.layer == "functional":
        run_functional(args.skill, args.trials, args.case)


if __name__ == "__main__":
    main()

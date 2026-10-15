#!/usr/bin/env python3
"""Replay recorded `gh api` responses for the sweep evals.

The stub reads responses.json from its parent directory.
It appends each call to calls.log, so an eval can check that no DELETE call happened.
"""

import json
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    args = sys.argv[1:]
    if not args or args[0] != "api":
        print("gh stub: only `gh api` is available", file=sys.stderr)
        return 1
    args = args[1:]
    responses = json.loads((ROOT / "responses.json").read_text())

    if args[0] == "graphql":
        fields = dict(a.split("=", 1) for a in args[1:] if "=" in a)
        kind = "pullRequest" if "pullRequest(" in fields["query"] else "issue"
        key = f"graphql {kind} {fields['owner']}/{fields['name']}#{fields['number']}"
        method = "POST"
    else:
        method, path = "GET", None
        i = 0
        while i < len(args):
            if args[i] == "-X":
                method, i = args[i + 1], i + 2
            else:
                path, i = args[i], i + 1
        parts = urlsplit(path)
        page = parse_qs(parts.query).get("page")
        key = f"{method} {parts.path}" + (f"?page={page[0]}" if page else "")
        if method == "DELETE":
            thread = parts.path.rsplit("/", 1)[-1]
            known = f"GET notifications/threads/{thread}" in responses
            responses[key] = "" if known else None

    with (ROOT / "calls.log").open("a") as log:
        log.write(f"{key}\n")
    if responses.get(key) is None:
        print(f"gh: Not Found (HTTP 404) for {key}", file=sys.stderr)
        return 1
    body = responses[key]
    print(body if isinstance(body, str) else json.dumps(body))
    return 0


if __name__ == "__main__":
    sys.exit(main())

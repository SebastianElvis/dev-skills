#!/usr/bin/env bash
# Build a synthetic GitHub inbox with a stub gh. Print the fixture path.
set -euo pipefail
dir="$(mktemp -d -t sweep-gh-unread-eval-XXXXXX)"
python3 "$(dirname "$0")/../../../fixture/make_fixture.py" "$dir"
echo "$dir"

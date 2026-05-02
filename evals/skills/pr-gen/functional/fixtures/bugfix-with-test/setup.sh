#!/usr/bin/env bash
# Bugfix branch: an off-by-one in a slice helper, with a regression test.
set -euo pipefail

dir="$(mktemp -d -t pr-gen-eval-XXXXXX)"
cd "$dir"

git init -q -b main
git config user.email "eval@example.com"
git config user.name "Eval"
git config commit.gpgsign false

mkdir -p src tests
cat >src/slice_util.py <<'PY'
def last_n(xs, n):
    # BUG: returns n+1 elements when len(xs) > n
    return xs[-n - 1:]
PY
# Realistic baseline: bug shipped without test coverage. Branch must add tests.
cat >tests/test_slice_util.py <<'PY'
# placeholder — no coverage for last_n yet
PY
git add . && git commit -q -m "initial (with bug)"

git checkout -q -b fix/last-n-off-by-one

cat >src/slice_util.py <<'PY'
def last_n(xs, n):
    if n <= 0:
        return []
    return xs[-n:]
PY
cat >tests/test_slice_util.py <<'PY'
from src.slice_util import last_n


def test_returns_exactly_n():
    assert last_n([1, 2, 3, 4, 5], 2) == [4, 5]
    assert len(last_n(list(range(100)), 10)) == 10


def test_n_zero_returns_empty():
    assert last_n([1, 2, 3], 0) == []
PY
git add . && git commit -q -m "fix off-by-one in last_n; add regression tests"

echo "$dir"

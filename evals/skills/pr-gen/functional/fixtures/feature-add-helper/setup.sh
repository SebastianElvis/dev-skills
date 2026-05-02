#!/usr/bin/env bash
# Build a fresh tmp git repo on a feature branch that adds a small helper module.
# Prints the repo path on stdout.
set -euo pipefail

dir="$(mktemp -d -t pr-gen-eval-XXXXXX)"
cd "$dir"

git init -q -b main
git config user.email "eval@example.com"
git config user.name "Eval"
git config commit.gpgsign false

mkdir -p src tests
cat >src/math.py <<'PY'
def add(a, b):
    return a + b
PY
cat >tests/test_math.py <<'PY'
from src.math import add

def test_add():
    assert add(2, 3) == 5
PY
cat >README.md <<'MD'
# demo
A tiny demo project.
MD
git add . && git commit -q -m "initial"

git checkout -q -b feat/add-multiply

# Real feature: add a multiply helper plus its test.
cat >>src/math.py <<'PY'


def multiply(a, b):
    return a * b
PY
cat >>tests/test_math.py <<'PY'


def test_multiply():
    from src.math import multiply
    assert multiply(4, 5) == 20
PY
git add . && git commit -q -m "add multiply"

# Add and then remove an unrelated change — pr-gen must NOT mention it.
echo "WIP" >src/scratch.py
git add . && git commit -q -m "wip scratch"
git rm -q src/scratch.py
git commit -q -m "drop scratch"

echo "$dir"

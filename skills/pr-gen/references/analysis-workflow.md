# Analysis workflow

Load this file when you need worked recipes for verifying scope and citing
files in a PR description. The commands below are general — substitute the
base branch (`$base`) and paths for the current repo.

## Step 1 — Scope check

```bash
git diff "$base"...HEAD --stat | tail -1
git diff "$base"...HEAD --name-only | cut -d/ -f1-2 | sort | uniq -c | sort -rn | head -10
git log "$base"..HEAD --oneline | wc -l
```

Use the directory histogram to decide which areas warrant a bullet in the
description. A directory with one trivial change does not.

## Step 2 — Verify a claim before citing it

Every feature, file, symbol, or test mentioned in the PR description must be
present in `HEAD`. The base check is:

```bash
# File exists in HEAD
git cat-file -e "HEAD:$path" 2>/dev/null && echo present || echo missing

# Symbol / config key exists in HEAD
git show "HEAD:$path" | grep -nE '<symbol-or-pattern>'
```

For features that span multiple files, run the grep for each, and only cite
the ones that come back with hits.

## Step 3 — Pick the file links worth including

For each bullet you write, pick the **single file** that best answers
"where would a reviewer go to see this change?" — usually the file with the
largest non-trivial diff in that area, not every touched file.

```bash
git diff "$base"...HEAD --numstat | sort -k1 -n -r | head -20
```

Format links repo-relative: `[file.ts](src/file.ts)` or
`[file.ts:42](src/file.ts#L42)`.

## Step 4 — Verify tests for a bugfix

Identify tests in the diff and confirm they reference the symbol the fix
changed:

```bash
git diff "$base"...HEAD --name-only \
  -- '**/*test*' '**/tests/**' '**/*_test.*' '**/*.spec.*'

git show "HEAD:$test_file" | grep -nE '<symbol-the-fix-touches>'
```

If the test file does not reference the fix's symbol or invariant, the test
is unrelated to the fix — do not list it under "Tests enforcing the
invariants".

## Step 5 — Sanity-check before pushing

Re-read the description and confirm, line by line, each cite resolves with
the commands above. If a bullet cannot be verified in `HEAD`, delete it.

# Evidence procedure

## Select the target and revisions

You inspect the branch, worktree status, and remotes.

```bash
git branch --show-current
git status --short
git remote -v
```

You use the user's explicit base or the target PR's base.
Without either, you use the workspace target or verified remote default.
You distinguish authentication and network errors from an absent PR.
You can draft locally with a known base when GitHub is unavailable.
Remote targets use the fetched remote base instead of a stale local branch.
You record limits when you cannot verify the remote base.

You set `base_ref` from the selected target:

```bash
head=$(git rev-parse HEAD)
base=$(git rev-parse "$base_ref^{commit}")
merge_base=$(git merge-base "$base" "$head")
git diff --stat "$merge_base" "$head"
git diff --find-renames --name-status "$merge_base" "$head"
git diff --find-renames "$merge_base" "$head"
```

You read the full diff, including truncated portions.
You exclude uncommitted changes unless the user explicitly requests a prospective draft.
You label prospective drafts. You do not publish them as current PR state.

## Establish the problem and requirements

You read applicable project instructions, contribution rules, and PR templates.
You select the requested template or the documented default.
You read the existing PR and linked issue when they supply the problem or expected behavior.
You verify issue relevance before a closing keyword such as `Fixes`.
History supplies context, not final scope.
You label inferred intent when no source states the need.

## Verify behavior and file links

You compare old and new behavior.
You check boundary claims with concrete inputs before generalization.
You trace relevant callers, conditions, and state changes before outcome claims.
Code that only limits an effect does not prove a complete root-cause fix.

You set `path` to the relevant repository path:

```bash
git show "$merge_base:$path"
git show "$head:$path"
```

Deletions use the old revision. Additions use the head revision.
You check both paths for a rename.
You omit additions that history later removes without a final diff.
An existing file uses a relative link, such as `[worker.ts](src/worker.ts)`.
Line links use recorded head lines: `[worker.ts:42](src/worker.ts#L42)`.
Removed files use merge-base GitHub permalinks when you know the repository identity.
Otherwise, you name the path without a broken link.

## Verify tests and validation

You examine relevant tests at the recorded head, including tests outside the diff.
You determine coverage from assertions, fixtures, indirect calls, and test configuration.
The test runner must discover each cited test.
You map each bugfix requirement to a test or an explicit coverage gap.
An absent test does not justify an invented test or a different change type.

- A coverage claim identifies what the test checks.
- An execution claim identifies its command, result, and revision.
- A proposed check identifies an unexecuted command.

You use observed command output or continuous integration results for execution claims.
A claim that a test fails before the fix requires an observed run.

## Check publication

You complete the draft before any required approval request.

Before an update, you refresh the PR's state, base, head commit, title, and body.
You check repository and branch identity, including a fork’s source repository.
Local `HEAD` and the PR head must match the recorded head.
Base or head changes require new evidence and draft checks.
Title or body changes require reconciliation with the requested edit.
An unexpectedly closed or merged PR requires a user decision before an edit or replacement.

You write the exact body to a temporary file.
You use `--body-file` instead of shell text interpolation.
These variables use the verified target and completed draft:

```bash
gh pr edit "$pr_number" --title "$title" --body-file "$body_file"
gh pr view "$pr_number" --json url,title,body,state,baseRefName,headRefOid
```

You omit `--title` or `--body-file` for requests that change only one field.
For creation, you verify the remote source branch against the recorded head.
Creation uses `gh pr create` with explicit `--base`, `--head`, and the same draft arguments.
After failures, you check remote state before retries to prevent duplicate creation.
You compare returned fields with the draft before a success report.

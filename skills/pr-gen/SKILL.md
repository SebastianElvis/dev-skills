---
name: pr-gen
description: Generate or update a GitHub Pull Request title and description from the actual code changes on the current branch. Use when the user says "generate PR", "write the PR description", "update the PR", or similar. Analyzes `git diff` against the base branch (not commit history) so added-then-removed work is omitted and fabrication is avoided.
---

# pr-gen

Generate or update a GitHub PR title and description from the **final state** of
the current branch.

## When to use

Trigger this skill when the user asks to:

- Generate, write, or draft a PR title or description.
- Update, refresh, or fix the description on an existing PR.
- Summarize a branch's changes for review.

Do **not** use for open-ended code review, release notes, or changelog
generation.

## Instructions

### 1. Principles (apply throughout)

1. **Document what's in `HEAD`, not commit history.** If something was added
   then removed, it does not exist — do not mention it.
2. **Verify before citing.** `git show HEAD:<path> | grep …` every feature you
   plan to reference.
3. **Be concise.** 15–30 lines typical, ≤ 50 for complex PRs.
4. **Respect project conventions.** If `.github/PULL_REQUEST_TEMPLATE.md` or
   `CONTRIBUTING.md` exist, follow them exactly.
5. **Refuse to fabricate.** If the branch cannot satisfy the template the PR
   type demands (e.g. a bugfix without tests), stop and tell the user what's
   missing. Do **not** silently downgrade to a looser template.

### Refusal rule

Before generating **any** title or description:

1. Read the chosen template's required sections and stated conditions.
2. For each condition, check whether the branch diff (`git diff
   "$base"...HEAD`) and `HEAD` actually satisfy it.
3. If **any** condition is not met, **do not generate the description**.
   Reply to the user listing the specific unmet conditions and what's
   missing from the branch, and ask them to add the missing pieces or
   pick a different template.

Never invent content to fill a section, and never list a file, symbol, or
test that does not exist in HEAD.

### 2. Locate the PR

```bash
branch=$(git branch --show-current)
base=$(gh pr view --json baseRefName -q .baseRefName 2>/dev/null || echo main)
pr=$(gh pr view --json number,state,title,mergedAt 2>/dev/null)
```

If `pr` exists and `state != OPEN`, stop and ask the user whether to (1) create
a new PR, (2) update the closed/merged one anyway, or (3) cancel.
Re-check state immediately before `gh pr edit` (TOCTOU).

### 3. Inspect the final-state diff

```bash
git diff "$base"...HEAD --stat
git diff "$base"...HEAD --name-only | cut -d/ -f1 | sort -u
git log "$base"..HEAD --oneline
```

For every feature you plan to mention:

```bash
git show HEAD:<path> | grep -n '<symbol-or-feature>'
```

### 4. Read project requirements

```bash
for f in .github/PULL_REQUEST_TEMPLATE.md .github/pull_request_template.md \
         PULL_REQUEST_TEMPLATE.md CONTRIBUTING.md; do
  [ -f "$f" ] && { echo "# $f"; cat "$f"; }
done
```

Template wins on structure. `CONTRIBUTING.md` adds required sections
(performance repro steps, spec updates, security statements, etc.).

### 5. Classify and pre-flight

Classify as **bugfix / feature / refactor / infra / docs**. Bugfix pre-flight —
the branch MUST contain:

- An articulable invariant the fix restores.
- Non-test code implementing the fix (or an explicit "test-only" confirmation
  from the user).
- At least one test per invariant, wired into the project's test runner.

Check tests exist:

```bash
git diff "$base"...HEAD -- '**/*test*' '**/tests/**' '**/*_test.*' '**/*.spec.*'
```

If anything required is missing, stop and list the gaps — do not generate.

### 6. Pick a template

- **Bugfix** → [templates/bugfix.md](templates/bugfix.md) (required four
  sections: Summary / Invariants / The fix / Tests).
- **Everything else** → [templates/feature.md](templates/feature.md)
  (Summary / Changes / optional impact section).
- **Large infra only** → [templates/infrastructure.md](templates/infrastructure.md).

### 7. Write the title

See [resources/title-patterns.md](resources/title-patterns.md). Shapes:

- `fix(scope): <invariant restored>`
- `feat(scope): <capability> with <benefit>`
- `refactor(scope): <what> to <why>`

Avoid: "Various fixes", "PR deployment", "Update code".

### 8. Write the description

Full guidance in [resources/analysis-workflow.md](resources/analysis-workflow.md).
Core rules:

- Bullets over paragraphs; one idea per bullet.
- Link files relative to repo root: `[file.ts](src/file.ts)`,
  `[file.ts:42](src/file.ts#L42)`.
- Cite only what `git show HEAD:…` confirmed.
- Present tense ("Adds X", "Removes Y").
- Omit Background/Implementation Details unless non-obvious — link to the
  issue instead.

### 9. Push the update

Re-check PR state, then:

```bash
gh pr edit "$pr_number" \
  --title "$title" \
  --body "$(cat <<'EOF'
<description>
EOF
)"
gh pr view "$pr_number"
```

If no PR exists yet, use `gh pr create` with the same `--title` / `--body`.

## Checklist

- [ ] Every feature cited is verified in `HEAD`.
- [ ] No mention of added-then-removed work.
- [ ] File links are repo-relative.
- [ ] Template structure (if any) is followed exactly.
- [ ] Length 15–30 lines (≤ 50 for complex PRs).
- [ ] Bugfix PRs use the invariants+tests structure.

# Split analysis

Use this file when one sentence cannot describe the PR without "and".

A split recommendation must name the parts, approximate sizes, dependencies, and merge order.

## Requirements for each part

Each part must be:

1. Correct without the other parts.
2. Safe to merge without the other parts.
3. Clear without the other parts.
4. Useful or clearly identified as preparation.

Reject a split point that fails any requirement.

## Common split points

Use these split points in this order:

1. Mechanical changes and behavior changes.
2. Separate issues.
3. A behavior-preserving refactor and the change that uses it.
4. Add a new path, move callers, then remove the old path.
5. Schema, data access, business logic, API, and client layers.
6. Dependency changes and the code that uses them.
7. Tests for current behavior before a refactor.

Measure a possible mechanical split.

```bash
git log "origin/$base..$head" --oneline
git diff "origin/$base...$head" --stat
git diff "origin/$base...$head" -w --stat
```

For schema work, expand the schema before code depends on it. Remove old schema only after all
dependent code changes.

## Cases that can require one PR

Do not force a split for these cases:

- One interface change and all required implementations.
- An atomic migration.
- A security fix where separate parts extend the exposure period.
- One trusted mechanical operation across many files.

State why the change is atomic. State the review depth for each area.

## Split plan

For each part, include:

- A clear name.
- The files and behavior.
- The approximate size.
- The reason that the part meets all four requirements.
- Its dependencies.

Give the merge order. Identify the first part and the reason for that order.

Prefer the smallest coherent part that provides a result or reduces risk.

Put the split plan first in the report. Include the evidence that caused the split decision.

Do not add detailed findings for code that the author will reorganize.

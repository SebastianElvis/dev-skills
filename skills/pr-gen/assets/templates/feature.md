# Feature, refactor, and documentation template

You use this default for features, refactors, documentation, tests, and small infrastructure changes without a required repository template.
You write all output in Simplified Technical English (ASD-STE100).

## Required structure

Each bullet contains one sentence that states one point.
The body contains three short sections in this order:

1. `## Problem`: You state the concrete need or limitation.
2. `## Solution`: You describe the change and resulting behavior. You include necessary migration or configuration details here.
3. `## Validation`: You state verified checks and observed results. You state absent execution evidence explicitly.

You omit risk sections and risk ratings.
You place relevant issue links after the three sections.

## Example

```markdown
## Problem

- The shared math module lacks a multiplication helper.

## Solution

- The module adds `multiply(a, b)` for callers that need multiplication.

## Validation

- The unit test checks integer multiplication.
- The agent did not run the tests.
```

## Final check

- [ ] The body states the problem, solution, and validation in order. Each bullet contains one sentence that states one point.
- [ ] The body states relevant validation evidence or its absence.
- [ ] The body omits risk sections and risk ratings.
- [ ] The output follows the length limit and Simplified Technical English rules.

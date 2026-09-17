# Reference for `feat/add-multiply`

The branch adds `multiply` and its test to the shared math module.
The following example assumes that the agent did not run the tests.

Title: `feat(math): add multiply helper`

```markdown
## Problem

- The shared math module lacks a multiplication helper.

## Solution

- The module adds `multiply(a, b)` for callers that need multiplication.

## Validation

- `test_multiply` checks that `multiply(4, 5)` returns `20`.
- The agent did not run the tests.
```

The body states the problem, solution, and validation within 120 words. The body omits risk sections and risk ratings.
The agent can report actual execution results when its transcript provides evidence.
The branch history adds and removes `src/scratch.py` without a final diff.
The title and body must omit that file and its temporary change.

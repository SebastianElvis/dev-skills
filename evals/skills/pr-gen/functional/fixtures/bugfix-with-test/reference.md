# Reference for `fix/last-n-off-by-one`

The branch corrects the start index in `last_n` and handles nonpositive counts.
For positive `n`, the function returns the final `min(n, len(xs))` items.
For `n <= 0`, the function returns an empty list.
`test_returns_exactly_n` checks positive counts in `tests/test_slice_util.py`.
`test_n_zero_returns_empty` checks a zero count in the same file.
The following example assumes that the agent did not run the tests.

Title: `fix(slice_util): return the correct item count from last_n`

```markdown
## Problem

- `last_n` returns an extra item when the input contains more than `n` items.

## Solution

- The helper corrects the start index from `-n - 1` to `-n`.
- It returns an empty list for nonpositive counts.

## Validation

- The unit tests check positive and zero counts.
- Negative counts lack a regression test.
- The agent did not run the tests.
```

The body states the problem, solution, and validation within 120 words. The body omits risk sections and risk ratings.
The agent can report actual execution results when its transcript provides evidence.
The agent must not claim that the fixture tests check negative counts or counts above the list length.

# Reference for `fix/last-n-off-by-one`

The branch corrects the start index in `last_n` and handles nonpositive counts.
For positive `n`, the function returns the final `min(n, len(xs))` items.
For `n <= 0`, the function returns an empty list.
The following example assumes that the agent did not run the tests.

Title: `fix(slice_util): return the correct item count from last_n`

```markdown
## Summary

- `last_n` returns an extra item when the input contains more than `n` items.

## Expected behavior

- The function returns the final `n` available items for positive counts.
- The function returns an empty list for nonpositive counts.

## The fix

- The [helper](src/slice_util.py) corrects the start index from `-n - 1` to `-n`.
- The helper returns an empty list before the slice operation when `n <= 0`.

## Tests enforcing the expected behavior

- **Unit test:** `test_returns_exactly_n` checks positive counts ([tests](tests/test_slice_util.py)).
- **Unit test:** `test_n_zero_returns_empty` checks a zero count; negative counts lack a regression test.
- The agent did not run the tests.
```

The body retains all four bugfix sections and uses at most 25 lines.
The agent can report actual execution results when its transcript provides evidence.
The agent must not claim that the fixture tests check negative counts or counts above the list length.

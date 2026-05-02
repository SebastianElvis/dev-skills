# Reference for `fix/last-n-off-by-one`

This is a **bugfix** PR. SKILL.md mandates the bugfix template's four sections:
invariant, root cause / fix, tests, regression coverage.

Suggested title: `fix(slice_util): return exactly n items from last_n`

Body should:
- Name the invariant: `last_n(xs, n)` returns exactly `min(n, len(xs))` items.
- Describe root cause (off-by-one in the slice end index) and the fix.
- List the new regression tests (`test_returns_exactly_n`, `test_n_zero_returns_empty`).
- Reference [src/slice_util.py](src/slice_util.py) and [tests/test_slice_util.py](tests/test_slice_util.py).

Hard requirements:
- Must mention tests — bugfix PRs without test coverage should be rejected by pr-gen.
- No `Co-Authored-By: Claude` footer.
- 15–30 lines (≤ 50 for complex).

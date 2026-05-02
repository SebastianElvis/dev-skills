# Reference (gold) PR description for `feat/add-multiply`

Title: `feat(math): add multiply helper`

Body:

```
## Summary
- Adds `multiply(a, b)` to [src/math.py](src/math.py).
- Adds `test_multiply` covering integer multiplication in [tests/test_math.py](tests/test_math.py).

## Test plan
- `pytest tests/test_math.py`
```

Notes for graders:
- The branch also contains an added-then-deleted `src/scratch.py`. That file is not in `HEAD`, so it must NOT be mentioned anywhere in the PR title or body.
- The body should be short (under ~30 lines).
- No `Co-Authored-By: Claude` or "Generated with Claude Code" footer.

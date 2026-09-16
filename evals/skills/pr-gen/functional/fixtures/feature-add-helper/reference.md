# Reference for `feat/add-multiply`

The branch adds `multiply` and its test to the shared math module.
The following example assumes that the agent did not run the tests.

Title: `feat(math): add multiply helper`

```markdown
## Summary

- Callers can now multiply values through the shared math module.

## Changes

- The [math module](src/math.py) adds `multiply(a, b)`.
- `test_multiply` checks that `multiply(4, 5)` returns `20` ([tests](tests/test_math.py)).

## Tests

- The agent did not run the tests.
```

The body retains Summary and Changes and targets 15 lines.
The agent can report actual execution results when its transcript provides evidence.
The branch history adds and removes `src/scratch.py` without a final diff.
The title and body must omit that file and its temporary change.

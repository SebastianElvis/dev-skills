# Feature, refactor, and documentation template

You use this default for features, refactors, documentation, tests, and small infrastructure changes without a required repository template.
You write all output in Simplified Technical English (ASD-STE100).

## Required structure

1. `## Summary`: You state the need and resulting behavior in one or two sentences.
2. `## Changes`: You describe each meaningful change with a representative file link.

The body states validation evidence or its absence.

## Optional sections

Each optional section requires its condition:

| Section | Condition |
| --- | --- |
| `## Breaking changes` | Callers must change code, configuration, or data. |
| `## Configuration` | The change requires new configuration or changes defaults. |
| `## Tests` | Coverage or execution details require separate explanation. |
| `## Rollout` | The change requires ordered steps or a coordinated deployment. |

You state the migration path under Breaking changes.
You state configuration defaults and their source under Configuration.

## Example

```markdown
## Summary

- Callers can now multiply values through the shared math module.

## Changes

- The [math module](src/math.py) adds `multiply(a, b)`.
- `test_multiply` checks integer multiplication ([test_math.py](tests/test_math.py)).

## Tests

- The agent did not run the tests.
```

## Final check

- [ ] The body retains Summary and Changes in order.
- [ ] The body states relevant validation evidence or its absence.
- [ ] The output follows the length limit and Simplified Technical English rules.

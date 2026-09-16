# Title patterns

You write the title in Simplified Technical English (ASD-STE100).

## Default pattern

You use `<type>(<scope>): <imperative summary>`.
You omit an uninformative scope.

| Type | Purpose |
| --- | --- |
| `feat` | The change adds a capability. |
| `fix` | The change corrects a defect. |
| `refactor` | The change preserves external behavior. |
| `perf` | The change improves performance with evidence. |
| `docs` | The change updates documentation. |
| `chore` | The change updates build tools, dependencies, or infrastructure. |
| `test` | The change updates tests. |

## Examples

- `fix(auth): reject expired refresh tokens`
- `feat(payments): accept a request key for repeated requests`
- `refactor(db): share the connection pool`
- `docs: explain database recovery`

## Final check

- [ ] The title names a concrete outcome from the final diff.
- [ ] The title uses an imperative summary and at most 72 characters.
- [ ] Any performance or security claim has evidence.
- [ ] The title follows Simplified Technical English rules.

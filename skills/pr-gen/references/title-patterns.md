# Title fallback patterns

Load this file only when the repo has **no** established title convention
(no consistent style in recent merged PRs, no `CONTRIBUTING.md` guidance, no
PR template directive). Otherwise match the repo's existing style.

## Default — Conventional Commits

`<type>(<scope>): <imperative summary>`

| Type       | Use for                                              |
| ---------- | ---------------------------------------------------- |
| `feat`     | New user-facing capability.                          |
| `fix`      | Bug correction (correctness, safety, security).      |
| `refactor` | Internal change with no external behavior change.    |
| `perf`     | Optimization with a measurable benefit.              |
| `docs`     | Documentation-only.                                  |
| `chore`    | Build, deps, tooling, infra plumbing.                |
| `test`     | Test-only change.                                    |

Examples:

- `fix(auth): reject expired refresh tokens before signature check`
- `feat(api): add idempotent webhook delivery`
- `refactor(db): replace ad-hoc connection pool with pgx pool`
- `perf(render): defer hydration to cut TTI by 1.2s`

## Non-conventional fallbacks

If the repo uses plain prose, lead with an imperative verb:

- `Restore retry-safe keypair generation in claimer pegin flow`
- `Add Google and GitHub OAuth providers`
- `Document the deployment runbook with rollback steps`

## Constraints

- ≤ 72 characters (GitHub UI truncates beyond that).
- Imperative mood (`Add`, `Fix`, `Restore`) — not `Added` / `Adding`.
- Describes the **outcome**, not the process.
- Mentions the user-visible thing, not the implementation detail, unless the
  implementation *is* the change (e.g. a refactor).

## Anti-patterns

Reject and rewrite if the user proposes any of these:

- `Various fixes and improvements` — not specific.
- `Update code` / `Misc changes` / `Small fixes` — meaningless.
- `WIP` / `Work in progress` — should not ship.
- `PR deployment` — not a change description.

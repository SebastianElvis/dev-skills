# Feature / refactor / docs template

Use for any non-bugfix, non-large-infra PR. The body is a **default** — drop
sections that don't apply rather than padding them. Target 15–30 lines.

## Required sections

1. `## Summary` — 1–2 sentences. What ships and (if not obvious) why.
2. `## Changes` — bulleted list, one idea per bullet, each with a repo-relative
   file link to the most representative file. Cite only what `git show HEAD:…`
   confirmed.

## Optional sections — include only when non-obvious

Add these only when omitting them would leave a reviewer guessing. Do not
include empty placeholders.

- `## Breaking changes` — when callers must update code, configs, or data.
  State the migration path in one or two bullets.
- `## Configuration` — when new env vars, flags, or config keys are required
  to use the change. Include defaults and where each is read.
- `## Tests` — when test coverage is the headline (e.g., adds a missing test
  matrix). Otherwise the diff speaks for itself.
- `## Rollout` — when staged behind a flag or requires a coordinated deploy.
  One bullet per gate.

## Output shape

```markdown
## Summary

Adds idempotent webhook delivery so retries from upstream do not duplicate
side effects.

## Changes

- New `idempotency_key` column and unique index on `webhook_events`
  ([migration](db/migrations/20260501_idempotency.sql)).
- Delivery worker dedupes by key before invoking handlers
  ([worker.ts:78](src/webhooks/worker.ts#L78)).
- `POST /webhooks` accepts an `Idempotency-Key` header and rejects mismatched
  payloads with `409` ([routes.ts:42](src/webhooks/routes.ts#L42)).

## Configuration

- `WEBHOOK_DEDUP_WINDOW` (default `24h`) — retention before keys are GC'd
  ([config.ts:12](src/config.ts#L12)).
```

## Anti-patterns to avoid

- Sections like `## Cost Impact`, `## Performance Impact`, `## Security
  Considerations`, `## Architecture`, `## Dependencies` filled with
  generic platitudes. If you have nothing specific to say, omit the section.
- Repeating the title in `## Summary`.
- Linking every touched file. One link per bullet, the most representative.
- Pasting before/after code blocks — the diff already shows the code.
- Empty checklists or placeholder TODOs in the rendered body.

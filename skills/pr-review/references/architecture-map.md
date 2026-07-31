# Architecture summary

Use this file to describe the design that the PR changes. Review the protocol first when the PR
changes one. `protocol-spec.md` holds that method.

Read the code around the diff. State the current design, the PR change, and each conflict.

Use one line for an unchanged layer in the summary. Give the evidence for that conclusion. The
report groups the unchanged layers on one line.

Name the code that enforces each confirmed protocol invariant.

## Useful commands

```bash
git show "origin/$base:path/to/file"
rg -n 'symbolName'
git log --find-renames --oneline -20 -- path/to/file
git log -S 'invariantOrGuard' --oneline -- path/to/file
```

Use history for a removed guard or constant. Its source commit can identify the invariant.

## Data model

Examine these items:

- Schema types, nullability, defaults, indexes, and constraints.
- Serialized data, wire formats, messages, cache keys, and file formats.
- Storage invariants and code-only invariants.
- Migration reversibility and backfill requirements.
- Changes to the meaning or unit of an existing field.

For a partial deployment, old and new code can run against the same data. Check both read and write
directions.

Use expand, backfill, migrate, and contract for an incompatible schema change. Each stage must work
with the previous stage.

Check large-table indexes for the database's non-blocking creation option.

## State machine

List the states, transitions, triggers, terminal states, and concurrent transitions.

Ask:

- Which states or transitions become reachable?
- Which states or transitions become unreachable?
- Can a new state become terminal by mistake?
- Can two paths enter the same state at once?
- Does each new state define the old operations?
- Can the data model represent every state?

## Trust model

List these items:

- Principals that can reach the code.
- The authorization rule for each principal.
- The exact point where untrusted data becomes trusted.
- Assumptions that the surrounding code makes.

Ask:

- Does the PR add a principal or extend its access?
- Does it move validation or authorization?
- Can a cache, helper, or early return skip a check?
- Does it trust a new input or service?
- Does it break an assumption in other code?

Write each important assumption as a sentence. An invalid assumption can identify a security
finding.

## Component boundaries

Identify component owners, allowed dependency directions, and public interfaces.

Ask:

- Does the change stay inside the responsible component?
- Does it add a forbidden dependency or cycle?
- Does it use another component's internal code?
- Does it skip an established layer?
- Does it add a second mechanism for an existing operation?
- Does a file gain a second responsibility?

## Affected code

Count direct callers.

```bash
rg -n 'changedFunction'
```

Also search for code that depends on changed data or behavior without a direct call:

- Stored rows and serialized data.
- Other services and queue consumers.
- Cache readers and writers.
- Metrics, logs, dashboards, and alerts.
- Tests that define the old behavior.

## Final check

- [ ] Each layer has a statement and evidence.
- [ ] The summary names the code that enforces each protocol invariant.
- [ ] Data compatibility works in both directions.
- [ ] The summary names each important assumption.
- [ ] The summary includes direct and indirect dependent code.

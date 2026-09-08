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
- Migration transactions, version stamps, recovery states, backfills, and source or destination constraints.
- Changes to the meaning or unit of an existing field.

For a partial deployment, old and new code can run against the same data. Check both read and write
directions.

One version can contain many statements. Select version boundaries from atomicity and recovery, not
the number of concerns.

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

You must apply the architecture checks in `security-review.md`.
You must apply its specification checks here when the PR changes no protocol.

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
- Does each affected security requirement have an owner and an enforcement point on every reachable path?
- Can the design violate a security requirement even when the implementation follows the design?

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
- Does one type, module, or service own the subsystem state, lifecycle, policy, and effects?
- Does an abstraction improve ownership, invariant enforcement, reuse, or change scope beyond test access?

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

## Judge the modifications

The sections above describe the change. This section judges it. Do both.

Answer these questions:

- Does the design need a change, or does the current design already hold the fix?
- Is this the smallest architecture modification that solves the problem?
- Which architecture modification would you write instead?
- Which cost does the change add: a new mechanism, a wider boundary, or a new owner?

Your judgment becomes your own answer to the last question of step 8. An answer is `yes`, `yes with
a condition`, or `no`.

A broken layer, a verified security regression, a fix below the root cause, or a positive split test gives `no`.
A design gives `yes with a condition` when it requires an added test, migration step, or owner decision.

Give `yes` when you would write the same modification. Say so directly. Do not create a difference
to appear thorough.

## Final check

- [ ] The architecture modifications have your own answer, its reason, and an alternative.
- [ ] Each layer has a statement and evidence.
- [ ] The summary names the code that enforces each protocol invariant.
- [ ] Data compatibility works in both directions.
- [ ] The summary names each important assumption.
- [ ] The summary traces affected security requirements to enforcement points, attack paths, and evidence gaps.
- [ ] The summary includes dependent code and names the owner of each new subsystem.

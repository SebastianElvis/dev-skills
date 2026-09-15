# Architecture review

The agent reads beyond the diff before it judges the design.
The agent uses the specification result as the basis for this stage.

## Classify and size the change

The agent classifies final behavior instead of the PR title or label.
The agent selects one primary change type.
Two independent change types make the PR a split candidate.
The agent names the largest new behavior.

| Change type | Required checks | Priority passes |
| --- | --- | --- |
| Bugfix | The agent confirms the failure and first invariant break from code. The agent checks existing guards. The agent requires a regression test that fails without the fix. | Root-cause level and correctness. |
| Security fix | The agent reads the audit, vulnerability record, or advisory. The agent checks reachability, every vulnerable instance, and trust-boundary validation. The agent requires an attack-input test. | Security and correctness. |
| Feature | The agent verifies the supported use case, its source, and project intent. The agent checks existing support and the smallest interface, state, and dependency changes. | Necessity and architecture. |
| Refactor | The agent requires a specific reason and preserved observable behavior. The agent checks every deleted or replaced behavior and every test change. | Correctness and necessity. |
| Performance | The agent requires a realistic measurement and an identified bottleneck. The agent compares gains with memory, complexity, and concurrency risk. The agent requires evidence of preserved correctness. | Verifiability and correctness. |
| Infrastructure, dependencies, or configuration | The agent checks every consumer and affected subsystem. The agent checks partial deployment, rollback, dependency identity, versions, imports, current need, loosened constraints, and defaults. | Necessity and security. |
| Documentation | The agent verifies each claim, symbol, option, path, and example against the reviewed revision. | Verifiability at the lowest sufficient depth. |

A security fix closes the defect class or tracks each remaining instance.
A bugfix addresses the root cause or identifies a symptomatic fix with linked root-cause work.
A feature needs no speculative options or extension points without a current use.
A new public interface, persistent state, operator control, or runtime obligation counts as new behavior.
A refactor with new observable behavior requires feature or bugfix classification.
The agent separates mechanical changes from semantic changes.
Performance work should remove work before it adds caches or local optimizations.
The agent reviews a small diff deeply when it changes shared behavior.
Correct documentation needs no finding about prose preferences.

The agent counts significant lines separately from generated files, lockfiles, vendored code, and fixtures.
The agent also distinguishes production code, tests, documentation, and removed behavior.
Size determines honest coverage, not quality.

The agent orders review risk as follows:

1. Trust boundaries and authorization.
2. Protocol behavior, persistence, migrations, and wire formats.
3. State machines and concurrency.
4. Public interfaces, error paths, retries, and deletions.
5. Generated files, lockfiles, formatting, and fixtures.

## Map the architecture

For each layer, the agent states the current design, PR modification, evidence, and conflicts.
An unchanged layer receives one evidence sentence.
The final report groups unchanged layers on one line.
The agent names the code that enforces each confirmed protocol invariant.

```bash
git show "$base:path/to/file"
rg -n 'symbolName'
git log --find-renames --oneline -20 -- path/to/file
git log -S 'invariantOrGuard' --oneline -- path/to/file
```

The agent uses history to explain removed guards and constants.

### Data model

The agent examines schema types, nullability, defaults, indexes, constraints, storage invariants, and code-only invariants.
The agent checks serialized data, wire formats, messages, cache keys, file formats, and changed field meanings or units.
The agent checks migration transactions, version stamps, recovery states, backfills, and source or destination constraints.
Old and new code must read and write shared data correctly during partial deployment.

The agent selects migration boundaries from atomicity and recovery requirements.
One migration version can contain many statements.
An incompatible schema change needs expand, backfill, migrate, and contract stages that each work with the previous stage.
The agent checks the database option for non-blocking index creation on large tables.

### State machine

The agent lists states, transitions, triggers, terminal states, and concurrent transitions.
The agent identifies states and transitions that become reachable or unreachable.
The agent checks accidental terminal states and simultaneous entry through different paths.
Each new state must define existing operations.
The data model must represent every valid state.

### Trust model and security

For a PR without protocol changes, the agent applies the specification security checks from the completed specification procedure here.
The agent lists principals, authorization rules, trust boundaries, surrounding assumptions, and the exact point where untrusted data becomes trusted.
The agent writes each important assumption as a sentence.

The agent traces each affected security requirement to its component owner, enforcement point, and failure behavior on every reachable path.
The agent checks new principals, wider access, and relocated validation or authorization.
The agent checks newly trusted inputs or services and broken assumptions in dependent code.
The agent examines alternate entry points, background jobs, caches, helpers, and service calls for bypass paths.
The agent checks tenant isolation, privilege separation, secret access, and data across trust boundaries where applicable.
The agent checks whether partial failure, rollback, or mixed versions remove a control or permit access after a failed check.
The agent presents verified design findings at this stage even when the implementation follows the design.
The summary separates verified findings, attack paths, and unresolved assumptions.

### Component boundaries

The agent identifies component owners, allowed dependency directions, and public interfaces.
The agent checks whether the change stays inside the responsible component.
The agent checks forbidden dependencies, cycles, access to internal code, and skipped layers.
The agent checks duplicate mechanisms and files with a second responsibility.
A subsystem needs a clear owner for state, lifecycle, policy, and effects.
An abstraction needs a benefit in ownership, invariant enforcement, reuse, or change scope beyond test access.

### Affected code

The agent counts direct callers of changed symbols.
The agent also checks indirect consumers of changed data or behavior.
These consumers include stored rows, serialized data, services, queue consumers, and cache readers and writers.
The agent also checks metrics, logs, dashboards, alerts, and tests that define the old behavior.
The summary covers migration recovery, test levels, and subsystem ownership where applicable.

## Evaluate a split

The PR is a split candidate when one sentence cannot describe it without "and".
Other signals include unrelated issues, commits, subsystems, or mechanical and semantic changes.
The agent examines split options only when these signals apply.

Each proposed part must be correct, safe to merge, and clear without the other parts.
Each part must be useful or explicitly identified as preparation.
The agent rejects a split point that fails any requirement.

The agent checks these split points in order:

1. Mechanical changes and behavior changes.
2. Separate issues.
3. A refactor that preserves behavior and the change that uses it.
4. A new path, caller migration, and removal of the old path.
5. Schema, data access, business logic, public interfaces, and client layers.
6. Dependency changes and their dependent code.
7. Tests for current behavior and the subsequent refactor.

```bash
git log "$base..$head" --oneline
git diff "$base...$head" --stat
git diff "$base...$head" -w --stat
```

The agent preserves atomic migrations, transaction boundaries, and version-stamp boundaries.
The agent expands the schema before code depends on it.
The agent removes old schema only after all dependent code changes.
Combined test results do not prove that each proposed part is safe.

A single PR can be necessary for an interface with required implementations or an atomic migration.
A security fix can require one PR if separate parts extend exposure.
One trusted mechanical operation across files can also remain in one PR.
The agent states why the change is atomic and the review depth for each area.

The split plan names each part, files, behavior, approximate size, dependencies, and evidence for all four requirements.
The plan gives the merge order, first part, and reason for that order.
The agent prefers the smallest coherent part that provides a result or reduces risk.
The agent places the plan before Problem and approach in the final report.
The agent omits detailed findings for code that the author will reorganize.

## Form the independent solution

The agent answers these questions before the detailed review:

- Is the problem real?
- Is the diagnosis correct?
- Is the problem worth the review and maintenance cost?
- Does the repository already solve or prevent it?
- What is the smallest correct solution?
- Does that solution need a specification change?

The agent writes a split plan instead of a solution when the split test succeeds.
Otherwise, the agent writes one paragraph with the change location, invariant, and code that remains unchanged.
The agent compares that solution with the PR.
A difference requires a named principle and concrete cost before it becomes a finding.
The agent drops equally correct alternatives and states when the PR solution is better.

The agent answers these questions to judge the architecture modifications:

- Does the design need a change, or does the current design already contain the fix?
- Is this the smallest architecture modification that solves the problem?
- Which architecture modification would the agent write instead?
- Which cost does the change add: a new mechanism, a wider boundary, or a new owner?

The judgment determines the agent's answer about the proposed architecture modifications.
A broken layer, verified security regression, fix below the root cause, or positive split test requires `no` for the modifications.
A missing test, migration step, or owner decision requires `no` when acceptance depends on it.
The agent answers `yes` when it would write the same modification.

## Request confirmation

The agent uses the architecture confirmation template from `SKILL.md`.
The summary includes change type, significant size, planned coverage, security results, and the independent solution or split plan.
A protocol change receives one line for the confirmed result without the full protocol invariant list.

The agent can ask at most two additional questions at this stage.
Each question must meet all these conditions:

- The repository and history contain no answer.
- The answer changes a verdict or blocking status.
- The question asks about intent or preference instead of a code fact.

The agent states where it searched and gives its own answer.
The agent does not ask the human to perform checks that the code or procedure can resolve.
The questions name the architecture claims and affected invariants or transitions.

The agent omits these questions:

- Is this PR ready to merge?
- Are there tests?
- What does this PR do?
- Should I check security?
- Should I use strict review standards?
- Is the PR too large?
- Does the code follow project rules?
- Do you have any concerns?

The agent stops when the human rejects the problem.
The agent stops with `I recommend a split before review.` when the human accepts the split plan.
The agent reviews only the largest coherent part when the human rejects the split.
The agent stops with `I recommend a design discussion.` when the human rejects the architecture modifications.
The agent corrects a rejected architecture description before it requests confirmation again.

## Subagent tasks

Before confirmation, the agent uses up to three available subagents for facts:

1. Problem sources and project rules.
2. Data model and state machine.
3. Trust model, component boundaries, and affected code.

Each task follows the shared fact rules.

## Final check

- [ ] The change type and significant size reflect final behavior.
- [ ] Each architecture layer has evidence.
- [ ] The summary covers compatibility, migration recovery, test levels, owners, and affected code where applicable.
- [ ] Each affected security requirement has enforcement evidence, an attack path, or an evidence gap.
- [ ] The split test has a result.
- [ ] The independent solution or split plan precedes the detailed review.
- [ ] The confirmation follows its template and Simplified Technical English.

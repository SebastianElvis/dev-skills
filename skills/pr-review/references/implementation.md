# Detailed implementation review

The agent uses the confirmed problem, architecture, approach, change type, and scope as the review basis.
The agent corrects a confirmed point when source evidence disproves it.
The agent performs the passes that the change type requires.
Security and the test strategy apply to every change type.
The agent collects each candidate with a concrete failure before verification.
The agent does not filter candidates by confidence at this point.

## Review passes

### Protocol conformance

The agent performs this pass first when the PR changes a protocol.
The agent uses the protocol invariants and classification from the specification stage.
The agent checks code that disagrees with a clause or changes protocol behavior without a specification update.
The agent checks broken protocol invariants, new protocol invariants without enforcement, affected dependent parts, and incompatibility between old and new parties.
Each break requires a concrete violation trace.
A broken liveness protocol invariant belongs in this pass.
An availability attack outside a stated liveness protocol invariant follows the shared security evidence rules.
The agent reports the same attack only once across passes.

### Architecture conflicts

The agent checks conflicts with Architecture Decision Records (ADRs), project rules, and confirmed protocol invariants.
The agent checks duplicate mechanisms, misplaced policy, forbidden dependencies, invalid representable states, and files with a second responsibility.
The agent checks subsystem ownership for state, lifecycle, policy, and effects.
The finding names the exact conflicting rule, implementation, or boundary.
The agent drops claims without an exact conflict.

### Necessity and minimality

The agent lists each added file, type, function, option, dependency, and data field.
The agent asks these questions for each addition:

- What current behavior fails if this addition disappears?
- Does this addition replace code that the PR leaves in place?
- Can fewer parameters, types, or layers provide the same behavior?
- Does the repository already provide this operation?

```bash
rg -n '<new symbol>'
rg -n '<new config key>'
rg -n 'func <similarName>|def <similarName>|class <similarName>'
```

The agent checks wrappers with one caller and no owned state, invariant, or dependency boundary.
The agent checks branches and options that no caller can reach and parameters with one value across all callers.
The agent checks fields that code writes but never reads, duplicate helpers, and parallel mechanisms for the same operation.
The finding names the exact deletion or existing alternative.
The agent asks about future use when that intent can justify the addition.
A style preference does not justify a rewrite.

### Root-cause level

The agent finds the first line where the invariant fails.
The agent compares that location with the PR change.
Common symptomatic fixes include retries, delays, increased timeouts, and broad exceptions around an unexplained failure.
Other examples include instance-specific conditions inside general functions and downstream clamps for invalid upstream values.
The agent checks crash-site null checks without source corrections and user interface checks for data-integrity failures.
The agent checks temporary paths without linked root-cause work.
The agent checks whether the PR prevents the next instance of the same defect.
A deliberate symptomatic fix must identify its limit and link the root-cause work.

### Correctness

The agent starts with removed or replaced behavior.
The agent names the invariant for each affected line and locates its replacement enforcement.
The agent uses history to explain important guards.

```bash
git log -S '<deleted expression>' --oneline -- <file>
```

The agent checks boundary, null, zero, and empty values.
The agent checks state transitions, concurrency, partial failure, retries, and resource lifetime.
The agent checks error paths without tests, type conversions, loop-variable capture, mutable defaults, and changed regular-expression anchors.
A defect in an unchanged line remains in scope when the PR changes its behavior.

### Security

You must run this pass for every change type.
You must trace each affected security requirement from its specification through its architecture to its implementation.
You must verify earlier security findings against the implementation and dependent code.
You must compare removed controls with their replacements and all dependent callers.
You must trace mismatches between the specification, architecture, and implementation to concrete attack paths.
You must check malformed inputs, boundary values, replay, concurrent requests, stale authorization, partial failure, and retries where applicable.
You must check parser differences and alternate representations that can bypass validation.
You must inspect existing tests for attack cases and expected rejection behavior.
You must record missing test coverage without a vulnerability claim unless an attack path supports that claim.

The agent checks these authorization requirements for every operation:

1. New routes and resources deny access by default.
2. The server checks authorization on every request.
3. Data queries limit records to the authorized principal.
4. Random identifiers do not replace authorization.

Operations include read, create, update, delete, export, and administration.
The agent checks caches, helpers, and early returns that can bypass authorization.

| Area | Applicable checks |
| --- | --- |
| Dependencies | The agent verifies names, use, transitive dependencies, and similarity to other package names. |
| Secrets | The agent checks code, tests, logs, errors, and continuous integration configuration for credentials or tokens. |
| Injection | The agent checks new inputs to Structured Query Language (SQL), shells, paths, templates, Lightweight Directory Access Protocol (LDAP), and XPath. |
| Deserialization | The agent checks untrusted data that becomes a rich object. |
| Cryptography | The agent checks new primitives, fixed initialization values, insecure modes, and nonconstant-time secret comparisons. |
| Server-side request forgery | The agent checks outbound requests with attacker-controlled hosts. |
| Prompt injection | The agent checks untrusted model input when model output can use a tool or cause an action. |

You must apply the shared security evidence rules to each candidate.
You must record each affected requirement and its result under the shared stage-result rules.
You must retain unresolved assumptions in final coverage.

### Verifiability and cost

The agent verifies each new symbol, path, application programming interface (API), option, environment variable, and dependency.

```bash
git grep -n 'symbolName' "$base"
git grep -n 'symbolName' "$head"
git log -S 'symbolName' --oneline
```

The agent reports references that never existed, use old names, or identify the wrong module.
The agent checks whether each dependency exists and the diff imports it.
The necessity pass determines whether the dependency is necessary.

The agent checks exception blocks that hide unexpected errors, execution after errors, and broad exceptions that replace narrow exceptions.
The agent reports unrelated formatting or renames only when they prevent an effective review.
The agent reports comments only when they contradict the code or describe old behavior.

#### Test strategy

The agent recommends the smallest fast suite that covers PR behavior and preserves distinct failure detection.
The agent examines relevant existing tests outside the diff.
The agent does not execute the tests.

- **Coverage:** The agent maps changed behaviors and affected invariants to assertions. The agent identifies uncovered boundaries, invalid inputs, failures, and state transitions. The agent checks from code whether regression tests fail without the fix.
- **Properties:** The agent prefers fast property-based tests over repetitive examples. The agent checks input domains, generators, independent oracles, reproducible counterexamples, and runtime bounds. Random samples do not prove exhaustive coverage.
- **Reuse:** The agent considers extensions to existing properties before new tests. The agent identifies redundant tests that broader properties can replace without lost assertions or distinct regression inputs.
- **Test levels:** The agent prefers unit tests, including property-based tests. The agent reduces integration and end-to-end tests when lower-level tests detect the same failures. The agent retains tests for database semantics and real component interactions that require those boundaries.

The Test strategy section states gaps, evidence limits, and justified keep, extend, replace, or remove proposals.
Proposals remain advisory unless evidence proves a PR regression, rule violation, or concrete cost.

### Project rules

The agent quotes the exact rule and changed line.
The agent drops the finding if either item is absent.
The nearest `CLAUDE.md` or `AGENTS.md` takes precedence over parent instructions, `CONTRIBUTING.md`, and relevant ADRs.
An inferred convention supports a question instead of a finding.
The agent names the nearby examples that support that question.
The agent omits results that a linter, formatter, type checker, or compiler reports.

## Verify candidates

The agent collects all candidates and removes duplicates before verification.
Candidates with the same file, line, and cause form one candidate.
The agent keeps one finding per root cause.
The agent tries to disprove each candidate from source evidence.

Each implementation candidate must meet these conditions:

- The code supports the claim.
- A current path can reach the failure.
- The PR introduces the failure.
- Affected code has the stated effect.
- No compiler, type checker, linter, or continuous integration check catches it.
- Nearby code uses the same quality requirement.
- A maintainer would act on the finding.

The agent verifies specification and design candidates against their sources and concrete attack paths.
The agent checks whether the PR changes assumptions that previously prevented the attack.

| Result | Meaning |
| --- | --- |
| `CONFIRMED` | The applicable source proves the failure. |
| `PLAUSIBLE` | A current state can cause the failure. |
| `REFUTED` | The source disproves the claim, prevents the state, or shows only a preference. |

A blocking candidate needs separate checks of the failure path, facts at the reviewed head revision, and PR scope.
The agent drops refuted or unverified candidates.
The report puts pre-existing problems in an out-of-scope note.

## Resolve unclear intent

The agent asks another question only when a blocking finding depends on unresolved intent.
The question states the choice and the result of each answer.
The agent rereads the shared output and confirmation rules before it asks the human.

## Deliver the review

The agent uses the report and PR comment templates from `SKILL.md`.
The agent writes the session report first, then the top comment and inline comments as separate drafts.
The agent checks each link and suggestion against the reviewed revision.
The agent applies the shared output check and each template checklist before delivery.

## Subagent tasks

After architecture confirmation, the agent groups passes when too few agents can run all passes separately:

1. Protocol conformance, architecture, necessity, and root-cause level.
2. Correctness and verifiability.
3. Security and project rules.

Each task receives the confirmed points, architecture summary, change type, and scope.
Each candidate includes a file, line, claim, and concrete failure.

The agent uses separate context for verification when possible.
The verifier receives the claim and code without the original reasoning.
For blocking candidates, distinct checks cover the failure path, facts at the reviewed revision, and PR scope.
Failed tasks follow the shared retry and coverage rules.

## Final check

- [ ] The passes follow the confirmed points, change type, and scope.
- [ ] Security and the test strategy cover the full PR.
- [ ] Each security requirement has a result with evidence, an attack path, or an evidence gap.
- [ ] Each finding has source evidence and a PR-introduced failure.
- [ ] Each blocking finding passes multiple checks.
- [ ] Each unresolved assumption remains visible in coverage.
- [ ] The report and comments follow their templates and Simplified Technical English.

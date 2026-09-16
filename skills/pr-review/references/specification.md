# Specification review

The agent reads the issue before the diff.
The agent completes the protocol applicability check before the architecture summary.

## Identify the problem

The agent reads the target PR metadata and comments with the GitHub command-line interface (`gh`).

```bash
pr="${1:?PR number or URL required}"
gh pr view "$pr" --json number,title,body,author,baseRefName,headRefName,state,isDraft,additions,deletions,changedFiles,labels,closingIssuesReferences
gh pr view "$pr" --comments
gh pr view "$pr" --json url,headRefOid,baseRefOid,headRepository,headRepositoryOwner
```

The agent records the base and head revisions from this metadata.
The agent uses those revisions for comparisons and code references.
The agent asks the user before it reviews a closed, merged, or draft PR.

The agent searches the PR body and commits for issue links that `closingIssuesReferences` misses.
The agent sets `base` and `head` to the recorded revision hashes before these commands.

```bash
gh pr view "$pr" --json body -q .body | rg -o '#[0-9]+|https://github.com/[^ )]+/(issues|pull)/[0-9]+'
git log "$base..$head" --format='%s%n%b' | rg -o '#[0-9]+'
gh issue view <N> --comments
```

The agent reads each relevant issue and its comments in the correct repository.
The problem statement names the affected user, report source, and any maintainer confirmation.
If no issue exists, the agent uses the PR body, commits, and code.
The statement then records that no independent problem report exists.
An issue and PR from the same person at the same time form one proposal.

## Read project rules

The agent identifies changed files before it selects applicable instructions.

```bash
git diff --name-only "$base...$head"
rg --files --hidden -g '!.git' -g AGENTS.md -g CLAUDE.md -g CONTRIBUTING.md -g ARCHITECTURE.md
rg --files | rg -i '(^|/)(adr|rfc|design|decisions)[^/]*/'
```

The agent reads each `AGENTS.md` and `CLAUDE.md` from the repository root to every changed file.
The nearest instruction file controls conflicts.
The agent reads relevant Architecture Decision Records (ADRs).
The agent labels rules as inferred when only nearby code supports them.

## Check protocol applicability

A protocol is a behavior contract between parties that cannot change at the same time.
The agent names at least two such parties.

Protocol interfaces include wire formats, messages, remote procedure calls, consensus rules, on-chain scripts, and multi-party cryptographic protocols.
Signed messages, versioned public application programming interfaces (APIs), and files that another release reads also qualify.
An internal queue, store API, process rule, or design record remains architecture unless another party consumes it independently.
A Request for Comments (RFC) or contract filename alone does not establish a protocol.

If the agent cannot name two parties, it records `No protocol surface` with one evidence sentence.

An invariant describes a property within one program.
A protocol invariant describes a property of an exchange between parties that no single party can change alone.

## Reconstruct the specification

The agent checks these sources in order until it finds the affected rule:

1. Repository specifications, ADRs, interface definitions, and OpenAPI documents.
2. External specifications that the code names, such as a Bitcoin Improvement Proposal (BIP), Ethereum Improvement Proposal (EIP), or RFC.
3. The code itself.

```bash
rg --files -g '*.proto' -g 'specs/**' -g 'docs/**'
rg -n 'MUST|MUST NOT|SHALL|SHOULD|BIP-?[0-9]+|EIP-?[0-9]+|RFC ?[0-9]+'
git log -S '<protocol constant>' --oneline -- <file>
```

The agent reads repository files and git history only for this reconstruction.
The agent does not fetch external specifications.
The agent marks the reconstruction `INFERRED` when the repository lacks the specification.
The agent states that the code defines the specification when no written document exists.

## Check specification security

The agent reads the applicable security model, threat model, and security requirements from the repository, specification, and PR documentation.
The agent identifies protected assets, principals, attacker capabilities, trust assumptions, and required security properties.
The agent distinguishes documented requirements from assumptions that it infers from code.
The agent marks inferred assumptions `INFERRED` and absent documentation as a coverage gap.

The agent checks whether the changed rules permit attacks even when every implementation follows them.
The checks cover weaker authorization, data disclosure, replay, downgrade, and attacker control over availability where applicable.
The agent checks new trust assumptions and security arguments that the change invalidates in other clauses.
The agent compares assumptions with the base revision and actual deployment model.
The agent records unverified deployment assumptions explicitly.

## Evaluate protocol invariants

The agent writes each affected protocol invariant as a numbered sentence with its source path, clause, or line.
The agent uses these categories, with priority for the first three:

1. Safety states what must never happen.
2. Liveness states what must happen and its assumptions.
3. Authorization states which party can cause each transition.
4. Message validity covers acceptance rules, order, replay, and idempotency.
5. Parameters cover timeouts, windows, fees, collateral, and their relations.
6. Compatibility states which peer versions interoperate.
The agent states each liveness assumption, such as an honest majority, synchrony bound, or timeout bound.
The list contains only protocol invariants that the diff can affect.

The agent selects one classification:

| Classification | Required action |
| --- | --- |
| Not a protocol change | The agent gives evidence that a counterparty observes no difference. |
| Conformant implementation change | The agent names the specification clause that the code now satisfies. |
| Specification change | The PR changes the specification text and states the version plan. |
| Specification violation | The agent identifies the disagreement between code and specification. The agent asks which one is wrong. |

An implementation PR has a blocking finding if it changes the specification without changed specification text or a link to that change.

Each protocol invariant receives one result:

- `preserved`: The agent names the code that maintains it.
- `broken`: The agent gives a concrete violation trace.
- `new`: The agent names the party that enforces it.

A violation trace names the parties, message sequence, start state, and result.
The agent also applies the shared requirements for security evidence.

## Check dependent protocol parts

For a changed specification clause, the agent finds each dependent part:

- Other clauses that cite it.
- Subprotocols that consume its field or message.
- Parameter relations that use its constant.
- Security arguments or proofs that use its assumption.
- Party roles that receive an obligation from it.

```bash
rg -n '<changed clause name>|<changed field>|<changed constant>'
git log -S '<changed constant>' --oneline
```

Each part receives an unaffected result with evidence or a broken result with a violation trace.
The agent checks relations among timeouts, windows, confirmation depths, fees, and collateral where applicable.
The agent treats a broken dependent part as a blocking finding.

The agent checks whether an old party accepts messages from a new party.
The agent checks whether a new party accepts messages from an old party.
The agent checks whether a version field or feature flag separates the two behaviors.
The agent checks whether the change requires an activation height, epoch, or negotiation step.

## Judge the change and request confirmation

The agent answers these questions from its reconstruction:

- Does the protocol need a change, or can one party solve the problem internally?
- Is this the smallest specification change that solves the problem?
- Which specification change would the agent write instead?
- Which compatibility, security, or complexity risk does the change add?
- Does the change preserve the security model and required properties?

A specification violation, broken protocol invariant, or verified security regression requires `no` for the proposed modifications.
A missing activation height or version field also requires `no` when acceptance depends on it.
The judgment determines the agent's answer about the proposed protocol modifications.
The agent states directly when it would write the same change.
The agent omits differences that show only a preference.

The agent asks no additional questions at this stage.
The agent asks the human to correct wrong or missing protocol invariants and dependent parts through the applicable template questions.

The agent corrects a rejected specification before it repeats the protocol invariant results.
The agent corrects a rejected classification before it continues.
The agent stops with `I recommend a design discussion.` if the human wants a specification decision first.

## Subagent task

Before confirmation, the agent uses one available subagent to collect specification sources.
The task returns quoted clauses, paths, and constants under the shared fact format.
The agent omits this task when the PR changes no protocol.

## Final check

- [ ] The problem and applicable project rules have sources.
- [ ] The protocol applicability result has evidence.
- [ ] The specification has a source or an `INFERRED` label.
- [ ] The review checks changed security assumptions and attacks that follow the changed specification.
- [ ] Each protocol invariant has a source and result.
- [ ] Each broken protocol invariant has a violation trace.
- [ ] Each dependent protocol part has a result.
- [ ] The compatibility check covers both directions.

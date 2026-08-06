# Protocol and specification review

Use this file when the PR changes a protocol.

Review the protocol at the specification level first. Do this work before you review the
implementation. Then check that the implementation enforces the result.

Present the result to the human before you continue. The human confirms the specification, the
classification, and the effect on the rest of the protocol.

## The protocol gate

A protocol is a behavior contract between parties that cannot change at the same time. Name at least
two such parties.

These are protocol surfaces:

- A wire format, a message format, or a remote procedure call (RPC) interface.
- A consensus rule, an on-chain script, or a multi-party cryptographic protocol.
- A signed message, a versioned public API, or a file that another release reads.

An internal queue, store API, process rule, or design record is architecture unless another party
consumes it independently. An RFC or contract filename alone does not create a protocol.

If you cannot name two parties, record `No protocol surface`.

Write one line plus its evidence when the diff touches no protocol surface. Then stop this file.

## Two terms

An invariant is a property of the code in one program. The other review passes use this meaning.

A protocol invariant is a property of an exchange between two or more parties. No single party can
change it alone. This file always writes the full term.

## 1. Reconstruct the specification

Read these sources in order. Stop when you hold the rule that the diff touches.

1. A specification in the repository: `specs/`, `docs/`, an Architecture Decision Record (ADR), an
   interface definition file, or an OpenAPI document.
2. An external specification that the code names, such as a BIP, an EIP, or an RFC.
3. The code itself.

```bash
rg --files -g '*.proto' -g 'specs/**' -g 'docs/**' | head -30
rg -n 'MUST|MUST NOT|SHALL|SHOULD|BIP-?[0-9]+|EIP-?[0-9]+|RFC ?[0-9]+'
git log -S '<protocol constant>' --oneline -- <file>
```

Read repository files and git history only. Do not fetch an external specification. Mark the
reconstruction `INFERRED` when the specification is absent from the repository.

State that the code is the specification when no written document exists. Then a reviewer must
write the protocol invariants from the code.

## 2. Enumerate the protocol invariants

Write each protocol invariant as one numbered sentence. Give its source path, clause, or line.

Use these categories:

1. Safety: what must never happen.
2. Liveness: what must happen, and under which assumption.
3. Authorization: which party may cause which transition.
4. Message validity: acceptance rules, order, replay, and idempotency.
5. Parameters: timeouts, windows, fees, collateral, and the relations between them.
6. Compatibility: which peer versions interoperate.

Categories 1 to 3 are the security properties of the protocol. Give them the most attention.

Name the assumption for each liveness protocol invariant. An honest majority, a synchrony bound, and
a timeout bound are assumptions.

Keep the list to the protocol invariants that the diff can affect. Do not copy the whole
specification.

## 3. Classify the change

Pick one result. Each result requires an action.

| Result | Required action |
| --- | --- |
| Not a protocol change | State the evidence that a counterparty observes no difference. |
| Conformant implementation change | Name the specification clause that the code now satisfies. |
| Specification change | The PR must change the specification text. It must state the version plan. |
| Specification violation | The code and the specification disagree. Ask which one is wrong. |

A specification change inside an implementation PR is a blocking finding when the PR neither changes
the specification text nor links the change.

## 4. Test each protocol invariant

Give each enumerated protocol invariant one result:

- `preserved`: name the code that keeps it.
- `broken`: give a concrete violation trace.
- `new`: name the party that enforces it.

A violation trace names the parties, the message sequence, the start state, and the result. This
requirement matches the exploit requirement in `security-review.md`.

Drop a break that needs a stronger adversary than the specification permits. An example is a break
that needs a dishonest majority under an honest-majority assumption.

## 5. Check the rest of the protocol

A change to one clause can break a part of the protocol that the diff does not touch.

Find each part that depends on the changed clause:

- A clause that cites the changed clause.
- A subprotocol that reads or writes the changed field or message.
- A parameter relation that uses the changed constant.
- A safety argument or a proof that uses the changed assumption.
- A party role that the changed clause gives an obligation to.

```bash
rg -n '<changed clause name>|<changed field>|<changed constant>'
git log -S '<changed constant>' --oneline
```

Give each dependent part one result: unaffected with evidence, or broken with a violation trace.

A change that satisfies its own clause can still break a second clause. Check the relations between
the parameters, such as a timeout, a window, and a confirmation depth.

## 6. Check mixed versions

An old party can talk to a new party during a deployment. Check both directions.

Ask:

- Does an old party accept a message from a new party?
- Does a new party accept a message from an old party?
- Does a version field or a feature flag separate the two behaviors?
- Does the change need an activation height, an epoch, or a negotiation step?

Most protocol breaks appear here.

## 7. Judge the specification change

Steps 1 to 6 describe the change. This step judges it. Do both.

Answer these questions:

- Does the protocol need a change, or can a change inside one party solve the problem?
- Is this the smallest specification change that solves the problem?
- Which specification change would you write instead?
- Which risk does the change add: compatibility, security, or complexity?

Your judgment becomes your own answer to the last question of step 5. An answer is `yes`, `yes with
a condition`, or `no`.

A `Specification violation` or a broken protocol invariant gives `no`. A change that needs an
activation height or a version field gives `yes with a condition`.

Judge from your own reconstruction. Mark the answer provisional when the specification is
`INFERRED`. Do not wait for the human.

## Liveness findings

A break of a liveness protocol invariant is a protocol finding. Report it in the protocol pass.

The exclusion for denial of service in `security-review.md` applies to the security pass. It does not
apply to a liveness protocol invariant that the specification states.

## Final check

- [ ] The specification has a named source, or the reviewer marks it `INFERRED`.
- [ ] Each protocol invariant is a numbered sentence with a source.
- [ ] The change has one classification and its required action.
- [ ] Each broken protocol invariant has a concrete violation trace.
- [ ] Each dependent part of the protocol has a result.
- [ ] The mixed-version check covers both directions.
- [ ] The specification change has your own answer, its reason, and an alternative or a condition.

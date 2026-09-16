# Specification confirmation template

The agent uses this template only when the PR changes a protocol.
The agent displays a `broken` protocol invariant as `Not preserved`.
Each affected protocol invariant or security control receives its own result.
The agent marks specification items from code as `INFERRED`.
The agent includes Protocol modifications and its question only for a specification change.

```text
# Protocol review — Stage 1 of 3

## Problem description

<The agent states the problem, source, and whether it needs a solution now.>

## Proposed solution

<The agent states the solution that the PR proposes.>

## Protocol description

<The agent states the protocol interface, source, security model, and classification.>

- **<Preserved | Not preserved | New>:** <The agent names the protocol invariant or security control. The agent gives evidence and any violation trace or attack path.>
- **Evidence gaps:** <The agent states unverified compatibility, recovery, or security assumptions.>

## Protocol modifications

<The agent names the dependent protocol parts and their results.>

## Questions

Is the above problem description correct?
<The agent inserts its answer in the shared format.>

Do you think the above problem needs a solution now?
<The agent inserts its answer in the shared format.>

Do you agree with the above proposed solution?
<The agent inserts its answer in the shared format.>

Is the above protocol description correct?
<The agent inserts its answer in the shared format.>

Do you agree with the above protocol modifications?
<The agent inserts its answer in the shared format.>
```

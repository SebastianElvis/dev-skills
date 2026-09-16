# Architecture confirmation template

The agent includes one line for the confirmed protocol result when applicable.
The agent includes the two problem questions only when the shared rules require confirmation.
Otherwise, Problem description states the confirmed problem in one line.
The architecture description includes change type, significant size, and planned coverage.
Each modification answer includes the independent solution or split plan where it supports the rationale.
The agent includes the independent solution in the description if the answers do not otherwise state it.

```text
# Architecture review — Stage <X> of <N>

## Problem description

<The agent states the problem, issue, reporter, maintainer response, and whether it needs a solution now.>

## Architecture description

<The agent states the current architecture, PR modifications, security results, and coverage.>

- **Enforcement:** <The agent names the components that enforce affected security requirements.>
- **Findings:** <The agent states verified design findings and their attack paths.>
- **Evidence gaps:** <The agent states unresolved assumptions.>

## Questions

Is the above problem description correct?
<The agent inserts its answer in the shared format.>

Do you think the above problem needs a solution now?
<The agent inserts its answer in the shared format.>

Is the above architecture description correct?
<The agent inserts its answer in the shared format.>

Do you agree with the above architecture modifications?
<The agent inserts its answer in the shared format.>
```

The problem rationale states whether existing code prevents the problem or supports a different cause.
Each architecture question refers to specific claims, affected invariants, or state transitions in the description.
For `no`, the proposal states the smallest solution or split plan and its difference from the PR.
Additional questions follow the conditions in the architecture procedure.

# Confirmations

Use this file at step 5 and at step 8. The review stops at each step. The human confirms or
corrects each point before the review continues.

- Step 5 asks about the problem, solution, and specification. It follows the protocol review.
- Step 8 asks about the design. It follows the architecture summary and the reviewer's position.

State your answer before you ask the human to confirm or correct it.

Include `Stage X of N` in each title.

Use three stages when the PR changes a protocol. Use two stages when the PR changes no protocol.

Name the applicable description or modification in each question. Do not ask only whether it is
correct.

## Length

Use 25 lines or fewer at step 5. Use 35 lines or fewer at step 8.

Give one line for each point. Add a second line only for a violation trace or a code link.

Ask a direct question. Write no preamble. `output.md` holds the language, the tone, and the code
links.

## Step 5: the protocol review

Use this step only when the PR changes a protocol. Record `No protocol surface` for a PR that
changes no protocol.

Ask no additional question here.

Use this structure:

```text
# Protocol review — Stage 1 of 3

## Problem description
<The problem, its source, and whether it needs a solution now.>

## Proposed solution
<The solution that the PR proposes.>

## Protocol description
<The protocol surface, source, affected invariants, classification, and result for each invariant.>

## Protocol modifications
<The dependent protocol parts and their results. Include this section for a specification change.>

## Questions

Is the above problem description correct?
Do you think the above problem needs a solution now?
Do you agree with the above proposed solution?
Is the above protocol description correct?
Do you agree with the above protocol modifications?
```

Omit the last section and question when the PR does not change the specification.

### Problem and solution

State the problem and its source. State the solution that the PR proposes.

### Protocol description

Present the specification source and the protocol invariants that the diff affects. Mark each item
that you read from the code, not from a document.

Ask the human to correct a wrong protocol invariant. Ask for a missed protocol invariant.

A wrong protocol invariant makes every later protocol finding wrong.

State the classification and the result for each protocol invariant.

Give a violation trace for each break. Name the assumption that the trace uses.

### Compatibility with the rest of the protocol

Ask this point only for a specification change.

Name each part of the protocol that depends on the changed clause. Give the result for each part.

Ask the human for a dependent part that you did not find. A specification often holds a relation
that no single file states.

## Step 8: the architecture review

Use this structure for a protocol change:

```text
# Architecture review — Stage 2 of 3

## Problem description
<The problem, its source, and whether it needs a solution now.>

## Architecture description
<The affected architecture, its modifications, the smallest solution, security changes, and coverage.>

## Questions

Is the above problem description correct?
Do you think the above problem needs a solution now?
Is the above architecture description correct?
Do you agree with the above architecture modifications?
```

Use `# Architecture review — Stage 1 of 2` when the PR changes no protocol.

### Problem

State whether the problem is real and worth a solution now. Include the issue, reporter, and
maintainer response.

Useful answer choices include:

- Real as described.
- Real with another cause.
- Existing code prevents it.
- Real but not worth a solution now.
- Not a problem.

### Architecture and modifications

Ask the human to confirm only the invariants and state transitions that affect the review.

Do not ask the human to confirm the full summary without a specific claim.

State the smallest solution that you would use. Compare it with the PR.

When both solutions are correct, say so. Do not create a difference to appear thorough.

## Additional questions

These questions belong at step 8.

Ask no more than two. Each question must meet all three conditions:

1. The repository and history contain no answer.
2. The answer changes a verdict or blocking status.
3. The question asks about intent or preference, not a code fact.

State where you searched. State your tentative answer.

Do not ask these questions:

- Is this PR ready to merge?
- Are there tests?
- What does this PR do?
- Should I check security?
- Should I use strict review standards?
- Is the PR too large?
- Does the code follow project rules?
- Do you have any concerns?

The reviewer can answer each question above from the code or review procedure.

## Security-relevant changes

At step 8, list only what the diff changes:

- Trust boundaries.
- Authorization decisions.
- External inputs and their parsers.
- Dependencies and their uses.
- Credentials, tokens, and secrets.
- Deserialization of untrusted data.

These are not findings before the security pass. Use one line when no item applies.

## Record the answers

Treat a question or objection as unconfirmed. Answer from repository evidence. Keep the detailed
review stopped. After the discussion ends, present one corrected stage. Ask once.

Put the confirmed or corrected points in the report. Link each human-supplied point to the findings
that depend on it.

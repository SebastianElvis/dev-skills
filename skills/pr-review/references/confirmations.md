# Confirmations

Use this file at step 5 and at step 8. The review stops at each step. The human confirms or
corrects each point before the review continues.

- Step 5 asks about the problem, solution, and specification. It follows the protocol review.
- Step 8 asks about the design. It follows the architecture summary and the reviewer's own solution.

Answer every question yourself. Write `My answer:` under the question. An answer is `yes`, `yes with
a condition`, or `no`. Add the reason in one sentence. Add the condition or the alternative when the
answer is not `yes`. Never send a question that you leave open.

Include `Stage X of N` in each title.

Use three stages when the PR changes a protocol. Use two stages when the PR changes no protocol.

Name the applicable description or modification in each question. Do not ask only whether it is
correct.

## Length

Use 35 lines or fewer at step 5. Use 40 lines or fewer at step 8.

Give one line for each point and one line for each answer. Add a third line only for a violation
trace or a code link.

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
<The protocol surface, source, security model, affected invariants, classification, and results.>
<The security requirement results, attack paths, and evidence gaps.>

## Protocol modifications
<The dependent protocol parts and their results. Include this section for a specification change.>

## Questions

Is the above problem description correct?
My answer: <yes | yes with a condition | no>. <The doubt that remains, or `no doubt`.>

Do you think the above problem needs a solution now?
My answer: <yes | yes with a condition | no>. <The reason in one sentence.>

Do you agree with the above proposed solution?
My answer: <yes | yes with a condition | no>. <The solution that you would use instead.>

Is the above protocol description correct?
My answer: <yes | yes with a condition | no>. <The doubt that remains, or `no doubt`.>

Do you agree with the above protocol modifications?
My answer: <yes | yes with a condition | no>. <The specification change that you would write
instead, or the condition that the PR must meet.>
```

Omit the `Protocol modifications` section and its question when the PR does not change the
specification.

### Problem and solution

State the problem and its source. State the solution that the PR proposes.

### Protocol description

Present the specification source and the protocol invariants that the diff affects. Mark each item
that you read from the code, not from a document.

Ask the human to correct a wrong protocol invariant. Ask for a missed protocol invariant.

A wrong protocol invariant makes every later protocol finding wrong.

State the classification and the result for each protocol invariant.

Give a violation trace for each break. Name the assumption that the trace uses.

You must include attacks that the changed specification permits, even when the implementation follows it.

### Compatibility with the rest of the protocol

Ask this point only for a specification change.

Name each part of the protocol that depends on the changed clause. Give the result for each part.

Ask the human for a dependent part that you did not find. A specification often holds a relation
that no single file states.

### My answers

Section 7 of `protocol-spec.md` holds the questions that produce your answers.

Do not repeat the description in an answer. Give the judgment that the description does not hold.

Say directly when you would write the same specification change. Do not create a difference to
appear thorough.

## Step 8: the architecture review

Use this structure for a protocol change:

```text
# Architecture review — Stage 2 of 3

## Problem description
<The problem, its source, and whether it needs a solution now.>

## Architecture description
<The affected architecture, its modifications, security requirement results, and coverage.>
<The enforcement points, verified design findings, attack paths, and evidence gaps.>

## Questions

Is the above problem description correct?
My answer: <yes | yes with a condition | no>. <The doubt that remains, or `no doubt`.>

Do you think the above problem needs a solution now?
My answer: <yes | yes with a condition | no>. <The reason in one sentence.>

Is the above architecture description correct?
My answer: <yes | yes with a condition | no>. <The doubt that remains, or `no doubt`.>

Do you agree with the above architecture modifications?
My answer: <yes | yes with a condition | no>. <Your smallest solution or split plan, and its
difference from the PR.>
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

### My answers

`architecture-map.md` holds the questions that produce your answers.

State the smallest solution that you would use. Compare it with the PR. Use two or three lines.

## Additional questions

These questions belong at step 8.

Ask no more than two. Each question must meet all three conditions:

1. The repository and history contain no answer.
2. The answer changes a verdict or blocking status.
3. The question asks about intent or preference, not a code fact.

State where you searched. State your own answer.

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

## Security results

You must include security results in the existing description at both confirmation stages.
You must use the stage results from `security-review.md`.
You must present verified specification and design findings before the detailed review.
You must distinguish those findings from unresolved assumptions and evidence gaps.
You must identify security regressions in your answer about the proposed modifications.
You must give one evidence sentence when the change affects no security requirement or control.

## Record the answers

Treat a question or objection as unconfirmed. Answer from repository evidence. Keep the detailed
review stopped. After the discussion ends, present one corrected stage. Ask once.

Change your answer when the human gives new evidence. Keep your answer when the human gives none.
Record the disagreement in the report.

Put the confirmed or corrected points in the report. Link each human-supplied point to the findings
that depend on it.

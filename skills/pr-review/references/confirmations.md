# Confirmations

Use this file at step 5 and at step 8. The review stops at each step. The human confirms or
corrects each point before the review continues.

- Step 5 asks about the problem, solution, and specification. It follows the protocol review.
- Step 8 asks about the design. It follows the architecture summary and the reviewer's own solution.

You must answer every question with `yes` or `no`. You must answer `no` if acceptance depends on an unmet condition.
You must use the applicable answer format under each question:

```text
My answer: yes. <You must summarize the reason in one sentence.>
```

```text
My answer: no.

- **Current implementation:** <You must describe the relevant behavior or design with evidence.>
- **Problem:** <You must explain the defect or unmet condition and its effect.>
- **Proposal:** <You must describe the required change and how it resolves the problem.>
```

Include `Stage X of N` in each title.

Use three stages when the PR changes a protocol. Use two stages when the PR changes no protocol.

Name the applicable description or modification in each question. Do not ask only whether it is
correct.

## Length

You must use 40 lines or fewer at each confirmation stage, including headings and blank lines.
You may exceed this limit to include the required rationale for each `no` answer.

You must retain the section headings below. You must put a blank line after each heading.
You must use short paragraphs for single points. You must group related bullets within each section.
You must keep each question with its answer in the Questions section.

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

<The protocol surface, source, security model, and classification.>

- **<Preserved | Not preserved | New>:** <The invariant or security control, its evidence, and any violation trace or attack path.>
- **Evidence gaps:** <The unverified compatibility, recovery, or security assumptions.>

## Protocol modifications

<The dependent protocol parts and their results. Include this section for a specification change.>

## Questions

Is the above problem description correct?
<You must insert the applicable answer format.>

Do you think the above problem needs a solution now?
<You must insert the applicable answer format.>

Do you agree with the above proposed solution?
<You must insert the applicable answer format.>

Is the above protocol description correct?
<You must insert the applicable answer format.>

Do you agree with the above protocol modifications?
<You must insert the applicable answer format.>
```

Omit the `Protocol modifications` section and its question when the PR does not change the
specification.
You must omit result bullets that have no content. You must give each invariant its own result.

### Problem and solution

State the problem and its source. State the solution that the PR proposes.

### Protocol description

Present the specification source and the protocol invariants that the diff affects. Mark each item
that you read from the code, not from a document.

Ask the human to correct a wrong protocol invariant. Ask for a missed protocol invariant.

A wrong protocol invariant makes every later protocol finding wrong.

State the classification and the result for each protocol invariant. You must display a `broken` result as `Not preserved`.

Give a violation trace for each break. Name the assumption that the trace uses.

You must include attacks that the changed specification permits, even when the implementation follows it.

### Compatibility with the rest of the protocol

Ask this point only for a specification change.

Name each part of the protocol that depends on the changed clause. Give the result for each part.

Ask the human for a dependent part that you did not find. A specification often holds a relation
that no single file states.

### My answers

Section 7 of `protocol-spec.md` holds the questions that produce your answers.

You must include the relevant current implementation in each `no` rationale, even when an earlier section describes it.

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

- **Enforcement:** <The components that enforce the affected security requirements.>
- **Findings:** <The verified design findings and their attack paths, if any.>
- **Evidence gaps:** <The unresolved assumptions, if any.>

## Questions

Is the above problem description correct?
<You must insert the applicable answer format.>

Do you think the above problem needs a solution now?
<You must insert the applicable answer format.>

Is the above architecture description correct?
<You must insert the applicable answer format.>

Do you agree with the above architecture modifications?
<You must insert the applicable answer format.>
```

Use `# Architecture review — Stage 1 of 2` when the PR changes no protocol.

### Problem

State whether the problem is real and worth a solution now. Include the issue, reporter, and
maintainer response.

Your rationale must explain whether existing code prevents the problem or evidence supports a different cause.

### Architecture and modifications

Ask the human to confirm only the invariants and state transitions that affect the review.

Do not ask the human to confirm the full summary without a specific claim.

### My answers

`architecture-map.md` holds the questions that produce your answers.

For `no`, you must propose your smallest solution or split plan. You must explain its difference from the PR.

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

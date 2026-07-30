# Checkpoint A questions

State your answer before you ask the human to confirm or correct it.

## Required points

### P1: Problem

State whether the problem is real and worth a solution now. Include the issue, reporter, and
maintainer response.

Useful answer choices include:

- Real as described.
- Real with another cause.
- Existing code prevents it.
- Real but not worth a solution now.
- Not a problem.

### P2: Architecture

Ask the human to confirm only the invariants and state transitions that affect the review.

Do not ask the human to confirm the full summary without a specific claim.

### P3: Approach

State the smallest solution that you would use. Compare it with the PR.

When both solutions are correct, say so. Do not create a difference to appear thorough.

## Additional questions

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

At Checkpoint A, list only what the diff changes:

- Trust boundaries.
- Authorization decisions.
- External inputs and their parsers.
- Dependencies and their uses.
- Credentials, tokens, and secrets.
- Deserialization of untrusted data.

These are not findings before the security pass. Use one line when no item applies.

## Record the answers

Put the confirmed or corrected points in the report. Link each human-supplied point to the findings
that depend on it.

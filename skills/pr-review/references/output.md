# Review output

Use this file for every text that a human reads: each question, each comment, and the report.

The wording rules come first. The report format and its length limits come after them.

## Language

Write in ASD-STE100 Simplified Technical English.

- Use the active voice. Name the actor.
- Keep a procedural sentence to 20 words or fewer.
- Put one instruction in each sentence.
- Use one term for one concept.
- Do not use an idiom or a metaphor.

## Tone

Write to a colleague. The author and you decide together.

- Give the evidence first. Then make one request.
- Write each comment as direct prose. Do not add a category, severity, or verdict marker.
- Use the report section to show whether a finding blocks the merge.
- Ask a question when project intent can change the verdict.
- Give a command only for a blocking finding.
- Say when the PR solution is better than your solution.
- Use "you" only in the required problem question from `confirmations.md`.
- Do not write "just", "simply", "obviously", "clearly", or "of course".

## Length

Put the claim in the first line of each finding.

- Write no preamble and no summary of the PR.
- Write one claim in one sentence of 25 words or fewer.
- Delete a sentence that repeats the evidence, the link, or the claim.
- Delete an optional section that has no content.

## Links

Link every code reference. Step 1 of the procedure collects `repo` and `sha`.

Write each reference as a link with the path and line as the text:

```text
[`internal/relay/verify.go:104`](https://github.com/<repo>/blob/<sha>/internal/relay/verify.go#L104)
```

Use `#L104-L110` for a range. Use the commit hash, not the branch name. A branch link breaks
after the next push.

## Suggested changes

Give each finding a GitHub suggestion block. Omit the block only for an architecture-level finding.

- Put the block last in the finding. GitHub applies it when the comment sits on those lines.
- Put the complete replacement text in the block. Do not add a `+` or `-` prefix.
- Keep the block to 10 lines or fewer, in one file.
- Split a finding that needs two files into one finding for each file.
- Omit the block for a design change or a change that needs a new test. State the change in prose.
- Do not repeat the content of the block in prose.

## Report template

The report goes to the human in the session. The PR comments are a separate text with its own
template. Write both.

Keep the report to 80 lines or fewer. Use about 40 lines for a 200-line PR.

Write each finding in the report as one bullet. State the problem and its effect, then the
suggested fix. Put the code link on the next line.

```text
# Detailed review — Stage <X> of <N>: #<number> — <title>
<author> · <type> · <files> files · <significant> significant lines

## Recommendation

<Merge | Merge after the author fixes the blocking findings | Needs design discussion |
Split before review | Problem not confirmed>

<One or two sentences. Give the reason. Do not summarize the PR.>

## Split plan

<Include only after a positive split test. Put this section before Problem and approach.>
<Give the reason, the named parts, the approximate sizes, and the merge order.>

## Problem and approach

**Problem:** <problem and source>
**Verdict:** <result and evidence>
**Approach:** <the PR agrees with the smallest solution, or the difference and its cost>

## Protocol

**Specification:** <path or clause, `INFERRED` from the code, or `No protocol surface.`>
**Classification:** <one of the four results, or delete this line with no protocol surface>
**Specification change:** <your answer and reason, or delete this line with no protocol surface>
<One line for each broken or new protocol invariant, with its violation trace.>

## Architecture

<One line for each layer that the PR changes: data model, state machine, trust model, boundaries.>
<Write one shared line for the layers that the PR does not change.>
**Affected code:** <dependent code, or `None outside the diff.`>

## Blocking

- <Problem in one sentence. Name the error, the wrong output, the security effect, or the data loss.>
  <Suggested fix in one sentence.>
  [`path/file.go:104`](https://github.com/<repo>/blob/<sha>/path/file.go#L104)

## Non-blocking

- <Problem in one sentence. Name its maintenance or user result.>
  <Suggested fix in one sentence.>
  [`path/file.go:31`](https://github.com/<repo>/blob/<sha>/path/file.go#L31-L34)

## Notes

<Accepted tradeoff or out-of-scope problem.>

## Coverage

Reviewed in depth: <areas>.
Not reviewed in depth: <areas and reasons>.

## Confirmed points

<One line. Name each point that the human corrected, and the findings that it changes.>
```

## PR comment template

The human posts these comments. They carry no title, no stage counter, and no report section.

The top comment summarizes the review, not the PR. Keep it to six lines or fewer:

```text
<Recommendation. Use one of the five results.>

<Two or three sentences. Give the reason for the recommendation. Name your main disagreement.
Do not describe what the PR does. The author already knows.>

Reviewed in depth: <areas>. Not reviewed in depth: <areas and reasons>.
```

Each finding becomes one comment on the lines that it cites:

```text
<Claim in one sentence.>
<Effect, then the required action in one sentence.>
<Suggestion block. Omit it only for an architecture-level finding.>
```

Keep the problem description, the protocol invariant list, the architecture summary, the split plan,
and the confirmed points out of the PR. The human reads those in the report.

## Worked finding

Write a PR comment like this:

    `parseHeader` accepts a zero-length payload and returns a nil body.
    The relay then panics at `body.Len()` on the next message from an untrusted peer.
    Please reject a zero-length payload before the function returns.
    [`internal/wire/header.go:104`](https://github.com/o/r/blob/abc1234/internal/wire/header.go#L104)

    ```suggestion
    if len(payload) == 0 {
        return nil, ErrEmptyPayload
    }
    ```

Do not write this:

    It looks like there might potentially be an issue here with the way that the header parsing
    logic handles the edge case of a zero-length payload — you should probably consider adding a
    check, because otherwise this could conceivably cause problems downstream. See
    internal/wire/header.go around line 104. This is a fairly common mistake and it's easy to miss!

The second version starts with a hedge. It gives no link and no suggestion block.

## Section rules

These rules apply to the report. Required sections are Recommendation, Problem and approach,
Protocol, Architecture, Blocking, Coverage, and Confirmed points.

Use `Stage 3 of 3` in the title when the PR changes a protocol. Use `Stage 2 of 2` otherwise.

Non-blocking, Notes, and Split plan are optional.

Put the Protocol section before the Architecture section.

Use one line for the Protocol section when the diff touches no protocol surface.

Keep the full protocol invariant list out of the report. It belongs in the text that you send to
the human.

Write `No protocol surface, so no specification question` in the Confirmed points section for a PR
that changes no protocol.

- Put the most important finding first.
- Write `None.` when no blocking finding exists.
- Do not add a type, severity, verdict, score, or confidence marker to a comment.
- Put each finding in the Blocking or Non-blocking section to show its severity.
- Ask a direct question when project intent can change the result.
- Mark each pre-existing problem as out of scope.
- Include praise only for a specific good decision.
- Do not name steps, passes, or subagents.
- Do not use numeric scores, grades, finding counts, or confidence percentages.
- Do not add an agent credit or co-author footer.

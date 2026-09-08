# Review output

Use this file for every text that a human reads: each question, each comment, and the report.

The report uses bullets. PR comments use separate prose with links and applicable suggestion blocks.

## Language

Write in Simplified Technical English (ASD-STE100).

- Use the active voice. Name the actor.
- Keep a procedural sentence to 20 words or fewer.
- Keep a descriptive sentence to 25 words or fewer.
- Put one instruction in each sentence.
- Use simple tenses. Give each sentence an explicit subject.
- Use one term for one concept.
- Do not use an idiom or a metaphor.

## Tone

Write to a colleague. The author and you decide together.

- Give the evidence first. Then make one request.
- Write each finding comment as direct prose. Do not add a category, severity, or verdict marker.
- Use the report section to show whether a finding blocks the merge.
- Ask a question when project intent can change the verdict.
- Give a command only for a blocking finding.
- Say when the PR solution is better than your solution.
- Do not write "just", "simply", "obviously", "clearly", or "of course".

## Length

Put the claim in the first line of each finding.

- Write no preamble and no summary of the PR.
- Write one claim in one sentence of 25 words or fewer.
- Delete an optional section that has no content.

## Links

Link every code reference in confirmations, reports, and PR comments. Inline placement does not replace the link.
Link symbol names when you use them as evidence. Code inside a suggestion block needs no links.

Write each reference as a link with the path and line as the text:

```text
[`internal/relay/verify.go:104`](https://github.com/<repo>/blob/<sha>/internal/relay/verify.go#L104)
```

Use `#L104-L110` for a range. Use the full reviewed commit hash, not a branch name or local `HEAD`.
Verify the repository, path, revision, and lines against the source. Resolve the repository from the target PR, not the current directory.
Use the PR head repository for fork code. Use the base revision for deleted code. Identify base references explicitly.

## Suggested changes

Use a `suggestion` fence in each inline comment when one replacement range can fix the finding.
Keep the replacement to 10 lines or fewer. This limit is a skill rule, not a GitHub limit.

- Put the block last. Link the exact head-side range that the human must select in the PR diff.
- Include the complete replacement text. Preserve unchanged lines within the selected range.
- Use a `suggestion` fence, not a language fence or a diff. Omit diff prefixes and placeholder code.
- Omit the block for fixes across multiple ranges or files. Omit blocks above 10 lines or dependent on an unresolved design decision.
- Omit the block when the PR diff has no valid replacement range. State the reason and fix in prose.
- Keep one finding per root cause. Do not split a finding to satisfy the suggestion limit.
- Include an applicable code suggestion even when the fix also needs a new test. Describe the test separately.
- State the reason for every omitted block. Do not repeat the replacement code in prose.

## Report template

Write the report first. Then write the top PR comment and the inline comments as separate drafts.
Keep draft labels outside the comment bodies. Do not wrap the output in an outer code fence.

Keep the report to 80 lines or fewer. Use about 40 lines for a 200-line PR.

Write each finding in the report as one bullet. State the problem and its effect, then the
suggested fix. Put the code link on the next line. Keep suggestion blocks in the inline comments only.

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

The review covers <areas>.
The review excludes <areas and reasons>.

## Confirmed points

<One line. Name each point that the human corrected, and the findings that it changes.>
```

## PR comment template

The human posts these comments. Comment bodies carry no title, stage counter, report section, or severity marker.

The top comment gives the recommendation and its reason. Keep it to six lines or fewer:

```text
<Recommendation. Use one of the five results.>

<Give the reason for the recommendation. Name any unresolved disagreement. Do not summarize the PR.>

The review covers <areas>. The review excludes <areas and reasons>.
```

Each finding becomes one comment. Use this structure when a suggestion applies:

````markdown
<Claim in one sentence.>
<Effect in one sentence, unless the claim states it.>
[`path/file.go:104-106`](https://github.com/<repo>/blob/<sha>/path/file.go#L104-L106)

```suggestion
<Complete replacement for the selected lines.>
```
````

When no suggestion applies, replace the fence with the proposed fix and the reason for omission.

Keep the problem description, the protocol invariant list, the architecture summary, the split plan,
and the confirmed points out of the PR. The human reads those in the report.

## Worked finding

Assume the selected line contains `return limit < max`. The requirement permits requests at the limit.
The example uses a placeholder repository and commit. Actual output must use verified values.

    The comparison rejects requests at the permitted limit.
    [`internal/limits/check.go:104`](https://github.com/<repo>/blob/<sha>/internal/limits/check.go#L104)

    ```suggestion
    return limit <= max
    ```

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
- Put each finding in the Blocking or Non-blocking section to show its severity.
- Mark each pre-existing problem as out of scope.
- Do not name steps, passes, or subagents.
- Do not use numeric scores, grades, finding counts, or confidence percentages.
- Do not add an agent credit or co-author footer.

## Output checklist

- [ ] Each code reference links to verified source lines at the correct commit.
- [ ] Each report finding uses one bullet with its problem, effect, and fix.
- [ ] The report and PR comments use separate templates.
- [ ] The top PR comment gives no summary of the PR.
- [ ] Each applicable inline fix uses a `suggestion` fence with at most 10 replacement lines.
- [ ] Each suggestion replaces exactly its linked range without removal of required context.
- [ ] Each omitted suggestion has a reason and a proposed fix.
- [ ] Each comment body has no draft label, stage counter, or severity marker.
- [ ] Each text follows Simplified Technical English and its length limit.

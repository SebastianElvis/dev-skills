# Report template

Use no more than 120 lines. Use about 60 report lines for a 200-line PR.

Use four lines for each finding: claim, location, evidence, and user-visible failure.

Delete an optional section when it has no content.

## Template

```text
# Review: #<number> — <title>
<author> · <type> · <base>...<head> · <files and significant lines>

## Recommendation

<Merge | Merge after the author fixes the blocking findings | Needs design discussion |
Split before review | Problem not confirmed>

<Reason in one or two sentences.>

## Split plan

<Include only after a positive split test. Put this section before Problem and approach.>
<Give the reason, named parts, approximate sizes, dependencies, and merge order.>

## Problem and approach

**Problem:** <problem and source>
**Verdict:** <result and evidence>
**Approach:** <comparison with the reviewer's solution>

## Protocol

**Specification:** <source path or clause, `INFERRED` from the code, or `No protocol surface.`>
**Classification:** <one of the four results, or omit with no protocol surface>
<List only the broken and the new protocol invariants. Give one violation trace for each break.>

## Architecture

**Data model:** <change, compatibility, or evidence for no change>
**State machine:** <changed transitions or evidence for no change>
**Trust model:** <assumptions and authorization effect>
**Boundaries:** <ownership and dependency effect>
**Affected code:** <direct and indirect dependent code>

## Blocking

issue (blocking): <claim>
`path/to/file.go:104` — <CONFIRMED | PLAUSIBLE>
<evidence>
**Failure:** <error, wrong output, security effect, or data loss>

## Non-blocking

suggestion (non-blocking): <claim>
`path/to/file.go:31`
<evidence and proposed change>
**Result:** <concrete maintenance or user result>

## Notes

note: <accepted tradeoff or out-of-scope problem>

## Coverage

Reviewed in depth: <areas>.
Not reviewed in depth: <areas and reasons>.

## Confirmed points

- A1 <specification> → <agreed or corrected> → <dependent findings>
- A2 <classification> → <agreed or corrected> → <dependent findings>
- A3 <compatibility with the rest of the protocol> → <agreed or corrected> → <dependent findings>
- B1 <problem> → <agreed or corrected> → <dependent findings>
- B2 <architecture> → <agreed or corrected> → <dependent findings>
- B3 <approach> → <agreed or corrected> → <dependent findings>
```

## Section rules

Required sections are Recommendation, Problem and approach, Protocol, Architecture, Blocking,
Coverage, and Confirmed points.

Non-blocking, Notes, and Split plan are optional.

Put the Protocol section before the Architecture section.

Use one line for the Protocol section when the diff touches no protocol surface.

Keep the full protocol invariant list in the checkpoint text. Do not put it in the report.

Write `Checkpoint A: skipped, no protocol surface` in the Confirmed points section for a PR that
changes no protocol.

- Put the most important finding first.
- Write `None.` when no blocking finding exists.
- Use `issue:`, `suggestion:`, `question:`, `nitpick:`, `note:`, or `praise:`.
- Mark each comment as `(blocking)` or `(non-blocking)`.
- Use `nitpick:` only for a non-blocking preference.
- Use `question:` when project intent can change the result.
- Mark each pre-existing problem as out of scope.
- Include a `praise:` comment only for a specific good decision.
- Do not repeat evidence in the summary.
- Do not name steps, passes, or subagents.
- Do not use numeric scores, grades, finding counts, or confidence percentages.
- Do not add an agent credit or co-author footer.

Describe the code. Do not describe the author.

Write the report in ASD-STE100 Simplified Technical English. Use the active voice. Keep a
procedural sentence to 20 words or fewer. Use one term for one concept. Do not use an idiom or a
metaphor.

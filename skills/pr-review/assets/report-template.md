# Report template

This template defines the terminal output for a completed PR review. Delete an optional section
that has no content. Do not add text to fill it.

## Length

A human reads this report. **Give a 200-line PR about 60 lines of report. Never write more than 120
lines.** Each finding gets four lines: the claim, the location, the evidence, and the failure. The
Recommendation gets two sentences. Each architecture layer gets one line. A report that is longer
than the diff is a failed report.

Findings use [Conventional Comments](https://conventionalcomments.org/). Write
`<label> [decoration]: <subject>`, then the evidence. Labels: `issue:` (a defect) · `suggestion:`
(an improvement) · `question:` (you are unsure, and the answer is important) · `nitpick:` (trivial
preference — always non-blocking) · `note:` (informational, always non-blocking) · `praise:`
(genuine). Decorations: `(blocking)` · `(non-blocking)` · `(if-minor)`. Every `issue:` includes
file:line, a one-sentence claim, a **user-visible** failure scenario, and a verdict of CONFIRMED or
PLAUSIBLE.

---

## Template

    # Review: #<number> — <PR title>
    <author> · <type> · <base>...<head> · <N> files, +<A>/−<D> (<S> significant; excludes <what>)

    ## Recommendation

    <Merge | Merge after the author corrects the blockers | Needs a design discussion
     | Split before review | Problem not confirmed>

    <Write one or two sentences. Give the reason first. Do not restate the PR.>

    ## Problem and approach

    **Problem:** <the problem in your own words> (<provenance: #4402, X reported it, Y triaged
    it — or: no statement of the problem exists outside this PR>)

    **Verdict:** <real as described | real, but with a different diagnosis | the code already
    prevents it | not a problem> — <one sentence of evidence.>

    **Approach:** <the same approach that I would write | different but equally sound | open to
    substantial improvement | it needs a split> — <If you can improve the approach, give the
    alternative and the concrete cost of the difference. If the approach is equally sound, write
    one line and propose no alternative.>

    ## Split plan
    <Include this section only when the split test is positive. Put this section first. Move it
    above "Problem and approach".>

    **Why:** <the measurement that makes the split test positive — closes #401 and #417;
    `git diff -w` drops 1,180 → 240 lines; refactor plus feature.>

    **Part 1 — <name>** (~<N> lines, <M> files). <What the part contains. Why the part is
    correct by itself. Why you can review and merge the part alone.>
    **Part 2 — <name>** …

    **Order:** <1 → 2 → 3>. **Land first:** <which part, and why — the smallest coherent stage
    that delivers a result or removes a risk.>

    ## Architecture

    **Data model:** <L1 delta — schema, serialized formats, rolling-deploy compatibility,
    migration reversibility. Or: "unchanged — no migration or serialized format in the diff.">
    **State machine:** <L2 delta — transitions gained or lost, terminal states. Or "unchanged.">
    **Trust model:** <L3 — the standing assumptions this code relies on, and whether the PR
    holds them. Always name the assumption you checked before you write "unchanged" here.>
    **Boundaries:** <L4 — ownership, dependency direction, duplicate mechanisms. Or "unchanged.">
    **Affected code:** <callers, plus implicit dependents — formats, caches, metrics, tests.>

    ## Blocking

    issue (blocking): <one-sentence claim>
    `path/to/file.go:104` — CONFIRMED
    <Evidence: what the code does. Quote the relevant line.>
    **Failure:** <user-visible consequence — an error, wrong output, data loss.>

    ## Non-blocking

    suggestion (non-blocking): `retryWithBackoff` repeats `internal/retry.Do`
    `path/to/other.go:31`
    `internal/retry/retry.go:18` gives the same backoff and the same jitter. Consider a call
    to it here. That removes about 40 lines, and it keeps one retry mechanism in the tree.

    question (non-blocking): does `EnableFastPath` need to be a config key?
    `config/flags.go:77`
    Only `server.go:210` reads it, and it is always `true`. Is a second value planned?

    ## Notes

    note: <out-of-scope finding, pre-existing finding, or accepted tradeoff>

    ## Coverage

    Reviewed in depth: <areas>.
    Not reviewed in depth: <areas, and why — generated, low-risk, out of budget>.
    <If you did not do a line-level review because of the size, write one sentence here.>

    ## Premises

    - P1 <problem statement> → <agreed | corrected to …> → <findings that depend on it>
    - P2 <architecture claim> → <agreed | corrected to …> → <findings that depend on it>
    - P3 <approach> → <agreed | rejected in favor of …> → <findings that depend on it>

---

## Section rules

Required: Recommendation, Problem and approach, Architecture, Blocking, Coverage, Premises.
Optional: Non-blocking and Notes — delete either section if it has no content. Include Split plan
only when the split test is positive.

- **Recommendation.** `Split before review` also requires named split points. `Problem not
  confirmed` is a complete review, not a failed review.
- **Split plan.** A split recommendation without split points is a complaint about size, not a
  review. Do not also file line-level findings against code that the author will reorganize.
- **Problem and approach.** If you reject P1 or P3 at Checkpoint A, this section and Architecture
  are the full report. Do not add nitpicks about code that the author will rewrite.
- **Architecture.** Write this section even for a small PR. One paragraph is the minimum. Two
  paragraphs are enough.
- **Blocking.** Write `None.` if you have no blocking findings. A finding is blocking only if it
  causes incorrect behavior, a security exposure, or an architectural commitment that is expensive
  to reverse. A preference is never blocking.
- **Notes.** Mark each pre-existing finding clearly, so the reader keeps it separate from a
  regression.
- **Premises.** This section records which findings depend on human-supplied intent instead of on
  the code. A second reader can then disagree with the premise instead of the conclusion. The line
  "P1 corrected: the race is at `pool.go:77`, not the mutex" is often the most useful line.

## Rules

- Write the report in ASD-STE100 Simplified Technical English. Use active voice. Write one
  instruction in each sentence, with a maximum of 20 words. Do not use idiom or metaphor.
- Follow the voice rules in SKILL.md. Describe the code, not the author. Propose a change; do not
  command one. Ask a question when the author may know a reason that you cannot see.
- Do not restate what the diff does. The author wrote it, and the reader can read it.
- Do not narrate the process. Never name a review pass, a step, or a subagent in the report.
- Put the most severe finding first in each section.
- Do not use severity scores, numeric confidence, or letter grades. The taxonomy has two values:
  blocking and non-blocking.
- Do not include a count of the findings. A count causes the writer to add unnecessary findings.
- Include a `praise:` finding when the author did something genuinely well. Do not invent one. A
  perfunctory compliment decreases the credibility of all the text below it.
- Do not append "Generated with Claude" or `Co-Authored-By:` footers.
- Never write "Approved" or "LGTM". The recommendation is advice. The human does the merge.

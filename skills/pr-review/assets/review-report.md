# Review report template

The report uses at most 80 lines.
A report for a 200-line PR should use about 40 lines.

Each finding uses one bullet with linked evidence, the problem, its effect, and the proposed fix.
Suggestion blocks belong only in inline comment drafts.
The report places the most important finding first.
The report uses Blocking and Non-blocking to show severity.
The Blocking section states `None.` if the review finds no blocking finding.

```text
# Detailed review — Stage <X> of <N>: #<number> — <title>
<author> · <type> · <files> files · <significant> significant lines

## Recommendation

<The agent inserts one allowed first-person result from the shared rules.>

<The agent gives the reason in one or two sentences.>

## Split plan

<The agent states the split reason, named parts, approximate sizes, dependencies, and merge order.>

## Problem and approach

**Problem:** <The agent states the problem and source.>
**Verdict:** <The agent states the result and evidence.>
**Approach:** <The agent compares the PR with its smallest solution and identifies any difference and cost.>

## Protocol

**Specification:** <The agent names the source, marks it `INFERRED`, or states `No protocol surface.`>
**Classification:** <The agent states one of the four classifications.>
**Specification change:** <The agent states its answer and reason.>
<The agent gives one line for each broken or new protocol invariant, with a violation trace for each break.>

## Architecture

<The agent gives one line per changed layer and one shared line for unchanged layers.>
**Affected code:** <The agent names dependent code or states `None outside the diff.`>

## Test strategy

The tests cover <changed behaviors and affected invariants, with linked assertions and input domains>.
The test gaps are <specific cases and effects, evidence limits, or `none identified`>.
The suite needs <justified keep, extend, replace, or remove proposals with test names, or `no test change`>.

## Blocking

- The [<affected operation>](https://github.com/<repo>/blob/<sha>/path/file.go#L104) <causes the problem and its effect>.
  <The agent states the proposed fix in one sentence.>

## Non-blocking

- The [<affected operation>](https://github.com/<repo>/blob/<sha>/path/file.go#L31-L34) <causes a maintenance or user effect>.
  <The agent states the proposed fix in one sentence.>

## Notes

<The agent states an accepted tradeoff or out-of-scope problem.>

## Coverage

The review covers <areas>.
The review excludes <areas and reasons>.
The security review checks <requirements and enforcement paths>.
The unresolved security questions are <evidence gaps, or `none`>.

## Confirmed points

<The agent uses one line to name each human correction and the findings that depend on it.>
```

## Section rules

The required sections are Recommendation, Problem and approach, Protocol, Architecture, Test strategy, Blocking, Coverage, and Confirmed points.
Non-blocking, Notes, and Split plan are optional.
The agent includes Split plan only after a positive split test, before Problem and approach.
The agent keeps Protocol before Architecture.

For a PR without protocol changes, Protocol contains one line only.
Confirmed points then includes `No protocol surface, so no specification question`.
The full protocol invariant list belongs in specification confirmation, not the final report.
Confirmed points includes the points that the human confirms or corrects and their effect on findings.

Verified security regressions from all stages belong in Blocking.
Coverage retains unresolved security requirements.
The recommendation identifies unresolved requirements that prevent a supported merge decision.
The Test strategy section states coverage, evidence limits, and proposals for the smallest sufficient suite.

The report body omits procedure step names, review pass names, and subagent names.
The report omits scores, grades, finding counts, confidence percentages, agent credits, and co-author footers.

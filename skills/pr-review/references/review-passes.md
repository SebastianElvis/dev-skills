# Review passes

Use this file after the human confirms the problem, the architecture, and the approach. Give each
pass those confirmed points, the architecture summary, the change type, and the review scope.

Send each candidate forward when it has a concrete failure. Do not filter by confidence here.

## 1. Protocol conformance and protocol invariants

Run this pass first, and only when the PR changes a protocol. Read `protocol-spec.md` for the
protocol gate and the enumeration method.

Check these conditions:

- The code disagrees with a clause of the specification.
- The PR changes protocol behavior but leaves the specification text unchanged.
- The PR breaks a protocol invariant that the human confirmed.
- The PR adds a protocol invariant that no party enforces.
- The change breaks a part of the protocol that the diff does not touch.
- An old party and a new party cannot interoperate during a deployment.

Each break needs a concrete violation trace. Drop a break that needs a stronger adversary than the
specification permits.

## 2. Architecture conflicts

Check these conditions:

- The change contradicts an Architecture Decision Record (ADR) or project rule.
- The change adds a second mechanism for an existing operation.
- A policy exists at the wrong component layer.
- A dependency crosses a forbidden component boundary.
- The change makes an invalid state representable.
- A file gains a second clear responsibility.
- The architecture does not enforce a protocol invariant from the protocol pass.

Name the conflicting rule, implementation, or boundary. Drop a claim that has no exact conflict.

## 3. Necessity and minimality

List each added file, type, function, option, dependency, and data field.

Ask four questions for each addition:

1. What current behavior fails if this addition disappears?
2. Does this addition replace code that the PR leaves in place?
3. Can fewer parameters, types, or layers provide the same behavior?
4. Does the repository already provide this operation?

Search for callers and similar code.

```bash
rg -n '<new symbol>'
rg -n '<new config key>'
rg -n 'func <similarName>|def <similarName>|class <similarName>'
```

Common unnecessary additions include these:

- A wrapper or interface with one caller.
- A branch or option that no caller can reach.
- A parameter with one value across all callers.
- A field that code writes but never reads.
- A helper that repeats an existing helper.
- A new mechanism beside an existing project mechanism.

Name the exact deletion or existing alternative. Use a question when a future use can justify the
addition.

Do not request a rewrite only because you prefer another style.

## 4. Root-cause level

Find the first line where the invariant fails. Compare that line with the PR change.

A symptomatic fix often has one of these forms:

- A retry, delay, timeout increase, or broad exception around an unexplained failure.
- A condition for one instance inside a general function.
- A downstream clamp for an invalid upstream value.
- A null check at the crash site with no source correction.
- A user interface check for a data-integrity problem.
- A temporary path with no linked root-cause work.

Ask what the next instance of the same defect looks like. Then check whether the PR prevents it.

A deliberate symptomatic fix can be correct. Require the PR to identify it and link the root-cause
work.

## 5. Correctness

Start with removed behavior.

1. Name the invariant for each deleted or replaced line.
2. Find where the new code establishes that invariant.
3. Use history to learn why an important guard exists.

```bash
git log -S '<deleted expression>' --oneline -- <file>
```

Then check these areas:

- Boundary values, null values, zero values, and empty strings.
- State transitions and concurrent access.
- Partial failure, retries, and resource lifetime.
- Error paths without tests.
- Type conversion and loop-variable capture.
- Mutable defaults and changed regular-expression anchors.

A defect in an unchanged line is in scope when the PR changes its function.

## 6. Security

Read `security-review.md`. Each finding needs a concrete exploit scenario.

## 7. Verifiability and cost

Check each new symbol, path, API, option, environment variable, and dependency.

```bash
git grep -n 'symbolName' "origin/$base"
git grep -n 'symbolName' HEAD
git log -S 'symbolName' --oneline | tail -5
```

Report a reference that never existed, uses an old name, or comes from the wrong module.

Check that each dependency is real and that this diff imports it. The necessity pass checks the
need for it.

Check the tests:

- Do they assert behavior instead of mock calls?
- Does each claimed invariant have a test?
- Does the diff weaken an assertion?
- Would the test fail without the fix?

Check error handling:

- Does an exception block hide unexpected errors?
- Does the code continue after an error?
- Does a new broad exception replace a narrow exception?

Report unrelated formatting or rename changes only when they prevent an effective review.

Report a comment only when it contradicts the code or describes old behavior.

## 8. Project rules

Quote the exact rule and the exact changed line. Drop the finding when either item is absent.

Use rules in this order:

1. The nearest `CLAUDE.md` or `AGENTS.md`.
2. Parent instruction files up to the repository root.
3. `CONTRIBUTING.md`.
4. Relevant ADRs.

An inferred convention supports a question, not an issue. Name the nearby examples.

Do not report a result that a linter, formatter, type checker, or compiler reports.

# The seven review passes

Use this file for the detailed defect hunt over a PR diff. Each section below is one subagent's
brief. Give each subagent the map and the agreed premises. Do not give it your session history.

**Every pass:** send forward each candidate with a concrete failure scenario. Do not pre-filter.

## Pass 1 — Architecture conflict

You have the map. Ask:

- Does this contradict a stated decision? Quote the Architecture Decision Record (ADR) or the doc
  line.
- **Is there now a second way to do something the codebase does one way?** Two retry mechanisms,
  two config loaders, two ways to construct the same entity. A line-by-line read does not show it.
- Is the decision at the right layer? A policy choice hardcoded in a handler that belongs in
  config; a transport concern that leaks into domain logic; business rules in a migration.
- Does it violate an existing boundary? Examples are a module that reaches into the internals of
  another module, a circular import, and a layer that skips the layer below it.
- Does it make an illegal state representable that was not representable before?
- Does the change make a file longer than ~1000 lines? Ask what the second responsibility is.

**Evidence requirement:** name the conflicting artifact — the ADR, the existing implementation,
the boundary. "This feels inconsistent" is not a finding.

## Pass 2 — Necessity and minimality

The other passes ask whether the new code is correct. This pass asks whether the new code should
exist at all. The cheapest code to maintain is the code that nobody writes.

Take the inventory first. List every item that the diff adds: each file, type, function, method,
config key, flag, environment variable, dependency, and table column. Then run the four tests below
against each item.

### 1. Must it exist?

State what breaks if you delete the item. If nothing breaks today, the item is cost with no
benefit. Two shapes are common:

- **A caller of one.** A wrapper, an interface, a config option, or an abstraction with a single
  use. Inline it, or ask what the second case is.
- **A path that nothing reaches.** A branch, an error type, or an option that no caller sets.

```bash
git grep -n '<new symbol>' | wc -l      # one hit is the definition, so one caller or none
git grep -n '<new config key>'          # who reads it?
```

### 2. Does it subsume existing code?

New code often does the work of code that stays in place. Then the repository holds both. Ask
whether the new code makes an existing function, branch, or special case unnecessary.

**The finding is the deletion that the PR did not make.** A PR that adds a general mechanism and
keeps the special case is incomplete. Name the file and the lines that the PR can now remove.

```bash
git grep -n 'func <similarName>\|def <similarName>\|class <similarName>'
git grep -ln '<the concept: retry, backoff, cache, parse>' | head -20
```

A new `formatDuration` beside an existing `humanizeDuration` is a real finding. You find it outside
the diff, so you must search for it.

### 3. Can it be smaller?

Propose the concrete reduction. State the lines that go away.

- A parameter that every caller sets to the same value.
- A layer of indirection with one caller on each side.
- A struct field that the code writes but never reads.
- A new type where an existing type plus one field works.
- A new test helper that duplicates the fixture in the same package.

### 4. Does it contradict the existing infrastructure?

The repository already has a way to retry, to load config, to log, to build a test fixture, and to
run a migration. New code that does one of these again is a contradiction, not only a duplication.
It makes a second way to do one thing, and the next author must choose between them.

Find the existing mechanism, then ask why the author did not use it. **When the PR gives no answer,
that absence is the finding.** Write it as a `question:` first. The existing mechanism may lack a
capability that the author needs. Then the correct change is an extension of the existing
mechanism, not a second one.

### Calibration and evidence

- **Name the alternative.** Give the `path:line` of the existing code, or the exact lines that the
  reduction removes. "This could be simpler" is not a finding. It is a complaint.
- **Ask, do not assert, when necessity depends on a plan.** The author may know of a second caller
  that lands next week. Use `question:`.
- **Judge the addition, not the taste.** This pass never asks for a rewrite of code that works and
  that nobody duplicates.
- **Weigh a deletion as a benefit.** A PR that removes more than it adds passes this pass. Say so
  with `praise:`.

## Pass 3 — Fix depth / root cause

The canonical formulation: *a special case on top of shared infrastructure shows that the fix is
not deep enough. Prefer to make the underlying mechanism more general.*

**Symptom-vs-cause tests.** A change is probably a symptomatic fix if:

- It adds a **retry, sleep, timeout increase, or `try/catch`** around a failure. The diff and the
  PR description do not name the cause of that failure.
- It adds a **conditional for the one case that triggers the bug** — a check for one status code,
  one tenant, one file type. That conditional sits inside a function that handles a general class.
- It **filters or clamps a value** downstream. It does not correct the code that produces the bad
  value.
- It adds a **null check** at the point of the crash. It does not establish why the value is null.
- The fix is in a **different layer than the bug**: a user interface (UI) guard for a
  data-integrity problem, a validation rule for a broken migration.
- It **defers the work**: a flag that defaults to the old behavior, a TODO, a "temporary" path.
- The commit history shows **earlier fixes in the same place**. If `git log --oneline -- <file>`
  shows three "fix flaky X" commits, nobody found the cause.

**The decisive question:** *what does the next instance of this bug look like, and does this change
prevent it?* Name the path concretely if the same root cause can appear again.

**Calibrate.** A deliberate symptomatic fix is legitimate. The finding is not "this is a symptomatic
fix". It is "this is a symptomatic fix **and nobody labeled it as one**." If the PR says "stopgap,
root cause tracked in #4412," that is good practice. Check for that label before you report.

## Pass 4 — Correctness

**The removed-behavior audit — do this first.** For every line the diff **deletes or replaces**:

1. Name the invariant, guard, or behavior that line enforced.
2. Search the new code for the place that re-establishes it.
3. If you cannot find that place, that is a finding.

Use `git log -S '<deleted expression>'` to find why the author added the line. If the diff removes
a guard that a bug-named commit added, and gives no explanation, the signal is strong.

A bug in an unchanged line of a touched function is in scope.

Then do the usual checks. Use the risk ranking in the map to set the order: boundary conditions;
nil/undefined on reachable paths; falsy-zero and empty-string treated as absent; concurrency
(shared mutable state, lock ordering, check-then-act, unbuffered channels); partial failure and
retry storms; resource lifetime (leaks, use-after-close, double-free); error paths that the tests
never exercise; type coercion; loop-variable capture; mutable default arguments; regexes that lost
an anchor.

## Pass 5 — Security

Load `security-review.md`. Do not improvise this one.

## Pass 6 — Verifiability and cost

**Write every finding as a falsifiable claim about the code. Never write a claim about who or what
wrote it.** Not "this looks AI-written," but "`parseConfig` is called on line 88 but does not exist
in `HEAD` — nearest match is `parse_config` in `config.py:12`."

No tool detects authorship reliably. As an
[AI-slop work proposal](https://github.com/ossf/wg-vulnerability-disclosures/issues/178) in the
OpenSSF Vulnerability Disclosures working group puts it: "There is no reliable technical
indicator for AI-generated content: detection is often based on 'vibes' and maintainer
intuition." Maintainers report the same volume of low-quality contributions from humans.

### Existence checks — the highest-precision check available

Apply them to every symbol, path, application programming interface (API), flag, environment
variable, and config key that the diff introduces or references:

```bash
git grep -n 'symbolName' "origin/$base"     # does it exist on the base?
git grep -n 'symbolName' HEAD                # does the PR define it?
git log -S 'symbolName' --oneline | tail -5  # did it exist once and get renamed?
```

Three outcomes worth reporting:

- **Never existed** — fabricated reference. Blocking.
- **Existed under an old name** — the reference is stale. For example, the diff calls
  `Curl_dyn_ptr`, but the tree renamed it to `curlx_dyn_ptr` several releases ago. Blocking.
- **Exists but in an unrelated module** — probably a wrong import. Check it.

Do the same for dependencies. A new entry in `package.json` / `go.mod` / `Cargo.toml` /
`requirements.txt` must be (a) real and (b) imported by this diff. Pass 2 tests whether the
dependency is necessary, so report the existence problem here and leave the necessity to that pass.

### Tests

- Do the tests assert **behavior**, or that the code called a mock? The second kind passes when the
  code is wrong.
- Is there a test for each invariant that the PR claims to establish?
- Does the diff **weaken** an existing assertion? Examples are a loosened tolerance, an exact match
  that becomes a substring match, and a deleted case. Check `git diff` on the test files.
- Does the test fail if you revert the fix? If you cannot see how it fails, say so.

### Error handling

- `catch`/`except` blocks that discard the error: name the unexpected errors that each one hides
  with the expected one. A bare `except:` around a parse that catches `KeyboardInterrupt` and
  `MemoryError` is a finding.
- Code that logs an error and then continues as if no error occurred.
- New broad exception types where the surrounding code catches narrow ones.

### Cost and churn

- **Unrelated churn**: reformatting, import reordering, or renames inside a functional PR. Report a
  `suggestion (non-blocking)` to split the PR. If the repository has an autoformatter that explains
  the churn, do not report it.
- **Comment rot**: comments that restate the code, or that describe behavior the diff changed. A
  comment that contradicts the code below it is a finding.

## Pass 7 — Conventions

**Quote the exact rule and the exact line that violates it. If you cannot do both, drop the
finding.** No style preferences, no inferences about the "spirit" of a document.

Sources, nearest-first: the `CLAUDE.md`/`AGENTS.md` closest to the changed file, then ancestors up
to the repo root, then `CONTRIBUTING.md`, then ADRs.

If you infer the rule from the surrounding code, and no document states it, label the finding: "the
other six handlers in this package use `X`; this one uses `Y`" is a legitimate `question:`, not an
`issue:`.

**Do not report** anything a linter, formatter, typechecker, or compiler catches. Assume that
continuous integration (CI) runs.

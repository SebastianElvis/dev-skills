# Change types

Use this file after you pick a PR's primary change type. The type determines what "correct" means.

Each section gives four items: validate the problem, examine, dominant failure mode, merge
requirement.

Pick **one** primary type. A PR with two types is a split candidate, because the two halves have
different requirements. Discuss it with the human first. See `split-analysis.md`.

## Bugfix

**Validate the problem.** Reproduce the bug *from the code*, not from the issue text. Trace from the
symptom to the line that produces it. A guard elsewhere may already prevent the bug. Or the cause
differs from the reporter's diagnosis.

```bash
git log -S '<the guard or expression in question>' --oneline -- <file>
git log --oneline -15 -- <file>    # three "fix flaky X" commits = the cause was never found
```

**Examine.** Where is the *cause*? Name the line where the invariant first breaks. The distance from
that line to the PR's change is the symptomatic fix signal.

**Dominant failure mode:** the fix repairs the symptom at the crash point. An example is a null
check there, instead of a change that establishes why the value is null.

**Merge requirement:** the diagnosis is correct. The fix is at the cause, or the author labels it a
symptomatic fix and tracks the root cause. A regression test fails without the fix. If you cannot
see how the test fails on the unfixed code, say so.

## Security fix

**Validate the problem.** Read the cited audit finding, CVE record, or advisory. Check that the fix
closes what the source describes. Confirm that the vulnerability is reachable in this codebase.

**Examine — variant analysis. This is the most important part.** The question is always **"is the
class closed?"**, not "is this instance fixed". Search for the other instances:

```bash
git grep -n '<the vulnerable pattern>'          # other call sites with the same shape
git grep -n '<the fixed function>' | wc -l      # how many callers rely on the new behavior
```

The fix may harden one call site while three others have the identical pattern. That PR is
incomplete. That is a blocking finding, not a suggestion.

**Dominant failure mode:** the fix patches the reported instance and leaves the class open. Two
others are common: validation that runs *after* the dangerous operation, and a fix in a helper that
only some paths call.

**Merge requirement:** the fix closes the class, or the author enumerates and tracks the remaining
instances. The fix is at the trust boundary, not downstream of it. A test exercises the attack
input. Do not require a public writeup. A writeup is a disclosure decision, not a review decision.

## Feature

**Validate the problem.** The "problem" is often only someone's want for the feature. Ask three
questions. Who asked for it? Does a maintainer or an issue endorse it? Does it serve a use case that
the project states it supports? Google's standard names this as legitimate grounds for rejection —
*"a CL adds a feature that the reviewer doesn't want in their system."*

**Examine.** What is the minimum surface that serves the use case? Compare it with what the PR adds.
A new public API, new config, new state, and new dependencies are all permanent. Ask whether the
existing model already supports this with a smaller change.

**Dominant failure mode:** speculative generality. Examples are an interface with one
implementation, a config flag with one value, and an extension point with no second case. Ask what
the second case is. If there is none, the addition is cost without benefit.

**Merge requirement:** the project wants the feature. It fits the existing model instead of a
parallel model. The surface is the minimum that works. The author documents it where users look.

## Refactor

**Validate the problem.** A refactor with no stated motivation is unnecessary work. Three
motivations are legitimate: it unblocks a specific upcoming change, removes a duplication you can
name, or fixes a boundary violation. "Cleaner" counts only if you say cleaner in what respect.

**Examine — behavior preservation is the only thing that matters.** A refactor that changes behavior
is a feature or a bug with a refactor's label, and a reviewer applies the wrong requirement to it.
Run the removed-behavior audit exhaustively. For every deleted or replaced line, name the invariant.
Then find where the code re-establishes it. Look for a changed error type, a changed default value,
an order that is incidentally stable and becomes unstable, a dropped log line that another program
parses, and an early return that changes short-circuit semantics.

**Dominant failure mode:** a silent behavior change inside a large mechanical diff. The real change
is invisible among 400 lines of renames. Split the mechanical part from the semantic part. That
split is almost always possible, and it makes both halves reviewable.

**Merge requirement:** the author demonstrates that the behavior is preserved. The tests are
unchanged. A refactor that needs test changes is not behavior-preserving, so investigate every test
change. The author states a real motivation.

## Performance

**Validate the problem.** Is there a **measurement**? A PR with no before/after numbers asserts a
problem. It does not demonstrate one. Ask what the author profiled, and on what workload. Ask
whether the changed code is really the bottleneck.

**Examine.** Is the optimization at the right level? An algorithmic change is better than a
micro-optimization. A cache is better than faster recomputation. Removal of the work is best. Ask
what the optimization costs in readability, memory, or correctness under concurrency.

**Dominant failure mode:** an unmeasured optimization that adds complexity and a cache-invalidation
bug, for a gain that nobody can demonstrate. The second mode is an optimization that is correct in a
single thread but introduces a race condition.

**Merge requirement:** a measurement shows the improvement on a realistic workload. The added
complexity is proportional to the gain. The change preserves correctness under concurrency.

## Infra / dependencies / config

**Validate the problem.** For a dependency bump, ask this: is it a security update, a required
transitive resolution, or drift? For config, ask what breaks today without this change.

**Examine.** Affected code and reversibility. Who consumes this config? What happens on a partial
rollout? **How do you roll it back?** A change that is hard to reverse deserves scrutiny
proportional to that difficulty, regardless of its size.

**Dominant failure mode:** a small diff that affects a very large amount of code. Examples are a
changed default in a shared config, a removed CI step, and a loosened version constraint. Heartbleed
was two lines. "small PR, quick review" is a rationalization, not a risk assessment.

**Supply chain, for any new dependency:** is it real? Does this diff actually import it? Does it
duplicate something already present? Is it a typosquat of the intended name? Check its transitive
dependencies. A dependency that serves only one utility function is worth a `question:`.

**Merge requirement:** you understand and state the affected code. A rollback path exists. The
author justifies each new dependency, and the code uses it. Every loosened constraint has a stated
reason.

## Docs

**Validate the problem.** Is the current documentation actually wrong or missing? Check the code.

**Examine.** Does the new text match what the code does *now*? Every claim, symbol, flag, path, and
example is checkable. Check them:

```bash
git grep -n '<symbol or flag from the docs>' HEAD
```

**Dominant failure mode:** plausible documentation for behavior that does not exist, or that existed
in an older version. Doc changes get the lightest review, so a confident-sounding inaccuracy can
remain permanently.

**Merge requirement:** you verify every factual claim against `HEAD`. Nothing else. Do not reject
docs because of prose style. Do not report a nitpick here.

Review these at the lowest depth. Do not skip the existence checks.

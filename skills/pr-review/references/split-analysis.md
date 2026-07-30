# Split analysis

Use this file when a PR fails the cohesion test. A PR fails that test when you cannot say what it
does in one sentence without "and". The output is a concrete plan: named parts, sizes, and a
landing order. Give the plan to the human as your position on the approach.

**A split recommendation without named split points is only a complaint about size.** The comment
"This PR is too big, please split it" costs the author more time than it saves. Do the work.

## The requirement for each part

A smaller part is not sufficient. Each proposed part must be:

1. **Independently correct** — the part does not leave the system in a broken intermediate state.
2. **Independently landable** — the part builds, the tests pass, and `main` is shippable when you
   merge this part and no other part. A split that breaks `main` between parts is worse than the
   original PR.
3. **Independently reviewable** — a reviewer can understand the part and does not need the other
   parts.
4. **Independently valuable, or explicitly preparatory** — the part either delivers something, or
   you label it as preparation for the next part.

If a proposed split point does not meet all four requirements, it is not a split point.

## Split points — in order of how often they work

**1. Mechanical vs semantic.** This split has the highest value and is the most common. Renames,
reformatting, import reordering, a file move, and generated-code updates all separate cleanly from
a behavior change. If you mix them, a real change hides inside 400 lines of unrelated edits.

```bash
git log "origin/$base..$head" --oneline
git diff "origin/$base...$head" --stat
git diff "origin/$base...$head" -w --stat   # compare: hunks that vanish are whitespace-only
```

A large difference between the two `--stat` outputs shows that most of the diff is formatting.
State that difference with the numbers.

**2. Per-issue.** If the PR closes three issues, that is three PRs. This is the easiest split to
justify and to execute, because the boundaries already exist in the tracker.

**3. Refactor-then-use.** The PR restructures something *and* uses the new structure. Land the
restructure alone, because it preserves behavior and you can review it against a clear requirement.
Then land the feature, which is now a small diff. This is Kent Beck's "make the change easy, then
make the easy change." Fowler's [preparatory refactoring example](https://martinfowler.com/articles/preparatory-refactoring-example.html)
is the canonical write-up.

**4. Additive-then-switch-then-delete.** Use this split when the PR replaces a mechanism: (1) add
the new path, unused or behind a flag; (2) migrate the callers; (3) delete the old path. Each part
lands safely, and you can revert each part on its own. A PR that does all three at once has no safe
rollback point. This is [ParallelChange](https://martinfowler.com/bliki/ParallelChange.html)
(Danilo Sato) — expand, migrate, contract. Name the pattern in the report.

**5. Per-layer.** Schema migration → data access → business logic → application programming
interface (API) → client. This split is natural when the layers deploy independently. **Note the
ordering constraint**: expand the schema before any code depends on it. Contract the schema only
after you remove all the code that depends on it.

**6. Dependency changes.** A dependency bump or a new dependency belongs in its own PR, separate
from the code that uses it. A bump has its own risk profile and its own revert procedure.

**7. Tests first.** Pure test additions that describe the existing behavior can land before a
refactor. These tests make the refactor reviewable, because they show that the refactor preserves
the behavior.

## When it genuinely cannot be split

Say so plainly. Do not invent split points. Real cases are:

- An interface change plus every implementor, in a language without staged deprecation.
- A migration whose expand and contract must be atomic for correctness.
- A security fix where separate parts disclose the vulnerability before the fix closes it.
  **This case overrides everything** — never recommend a split that makes an exposure window
  longer.
- A single mechanical transformation across many files, already reviewable as one operation.

In those cases, do not recommend `Split before review`. Say that the change is atomic. State which
parts you reviewed and at what depth.

## What the plan must contain

Give this information for each part: the contents, the approximate size, the reason that the part
satisfies the four-point requirement, and the dependencies. Then give the order, and name the part
to land first. Prefer **the smallest coherent stage that delivers something or lowers risk**.

## Worked example

> **This PR does three things.** It (1) renames `Conn` to `Connection` across 34 files, (2) adds
> `Retry-After` support to the retry sequence, and (3) bumps `net/http2`. `git diff -w --stat`
> drops from 1,180 to 240 changed lines, so ~80% of the diff is the rename.
>
> **Part 1 — rename `Conn` → `Connection`** (~940 lines, 34 files). This part is purely
> mechanical, and `gofmt -r` produced it. It preserves behavior and changes no test. Land it
> first. A reviewer can easily review it as one operation, and it makes the rest of the PR easier
> to read.
>
> **Part 2 — bump `net/http2` to v0.28** (~15 lines, `go.mod`/`go.sum`). This part is independent
> of the others and has its own revert procedure. Land it second, or in parallel.
>
> **Part 3 — `Retry-After` support** (~225 lines, 4 files, plus tests). This is the actual change,
> and the only part that needs a design review. It is independent of the other parts, but it is
> much easier to read after Part 1.
>
> Recommended order: 1 → 2 → 3. If only one part lands this week, make it Part 3. Part 3 has the
> user-visible value, and a reviewer can review its 225 lines alone.

That plan is actionable because it gives measured sizes, the mechanism for the mechanical part, an
explicit dependency claim, and a recommendation if the author has time for only one part.

## Presenting it

Lead the report with the plan. Include the measurement that made the PR fail the split test —
"closes #401 and #417", or the `-w` line-count difference. Then the recommendation is evidence, not
taste. Offer to review the parts as they arrive. The split is a request for *more* review, not
less.

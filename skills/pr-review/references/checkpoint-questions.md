# Checkpoint A — the agreement checkpoint

Use this when you present a PR review's design conclusions to a human for agreement. Present them
before any detailed line-level review. Every question spends the human's attention. A question that
the human can answer with `grep` wastes it.

## The three propositions

Present these for explicit agreement, with `AskUserQuestion`. State your own position on each one.
The human confirms or corrects it. The human does not derive it.

### P1 — The problem is real and worth solving now

State your own view of whether the problem is real. Give the provenance: issue number, reporter,
and whether a maintainer endorsed it. If nobody stated it outside this PR, say so.

Offer these options: the problem is real as described · real but with a different diagnosis ·
existing code already prevents it · real but not worth a solution now · not a problem.

> **P1 — Is the reconnect race real?**
> My position: **real, but with the wrong diagnosis.** Issue #4402 reports duplicate connections
> and attributes them to a missing mutex. The code holds the lock in `pool.go:71` correctly. The
> actual window is at `:77`, where the code releases the lock before it registers the connection
> in the map. This matters, because the PR's fix targets the mutex.

### P2 — The architecture reading is correct

You may be wrong about how the subsystem works. The human who owns it will know in seconds. Ask
about the invariants and the state transitions that your findings depend on, not the whole map.

> **P2 — Is my reading of the retry policy right?**
> I read it as two guarantees. First, `Do` never retries a request past the caller's context
> deadline. Second, the four `MaxAttempts: 1` call sites deliberately opt out of retry, and they
> do not work around an old bug.

### P3 — The approach is the right one

State the solution that you would write. If your alternative is materially better, present both and
the concrete cost of the difference. If they are equally sound, say so and propose no change.

> **P3 — Should the code honor `Retry-After` without a cap?**
> The PR sleeps for the duration that the server supplies. My alternative caps that duration at
> `policy.MaxBackoff`. The cost of the PR's version is this: a misconfigured upstream that returns
> `Retry-After: 3600` holds the goroutine past the caller's deadline. `payments` sets a deadline
> of 2 seconds. The cost of my version is this: we ignore legitimate long backoffs from
> rate-limited upstreams. I prefer the cap, but this is a policy decision.

**If you have no material disagreement, say that plainly.** Do not manufacture an alternative to
look thorough.

## Up to two further questions

Ask them only if all three admissibility conditions hold.

### 1. You looked, and the repo is silent

Search before you ask. State in the question where you looked.

```bash
grep -rn 'concept' --include='*.md' .
git log --oneline --all --grep='concept' -20
gh pr list --state merged --search 'concept' --limit 10
gh api "repos/{owner}/{repo}/pulls/$pr/comments" --jq '.[].body'
```

The last command matters most. Review comments on **past PRs that touch the same files** are the
best available record of team preference.

### 2. The answer changes a verdict or a severity

Write down what you report under each answer. If the two reports are identical, the question fails
this condition.

### 3. It is intent or preference, not fact

Facts are your job. "Does any other code call `Session.expire`?" is a `grep`. "Should sessions
expire eagerly or lazily?" is a preference.

## Rejected questions, and why

| Question | Why it fails |
| --- | --- |
| "Is this PR ready to merge?" | That is your output, not their input. |
| "Are there tests for this?" | Fact. `git diff --name-only \| grep test`. |
| "What does this PR do?" | Read the code. |
| "Do you want me to check security?" | Yes. Never ask permission to do the job. |
| "Should I be strict or lenient?" | Nobody can answer this in the abstract. The standard is code health. |
| "Is 400 lines too large for you?" | Report the number and the split points. |
| "Should error handling follow the repo convention?" | Fact. Find the convention, then cite it. |
| "Any concerns before I start?" | This question has no content. |

## Presenting the security surface

These are not findings, because the security review pass did not run. List what the diff touches:

- Trust boundaries that the diff crosses (network, process, privilege, tenant).
- Authorization decisions that the diff adds, moves, or removes.
- New external inputs, and the place where the code parses them.
- New dependencies — name, version, and whether this diff actually imports them.
- Credential, token, or secret handling.
- Serialization / deserialization of untrusted data.

If none apply, say "no security-relevant surface" in one line. Do not pad.

## Acting on the outcome

SKILL.md Step 5 holds the branch table. Three outcomes need more detail here:

- **P1 held, diagnosis corrected.** Re-check whether the PR's fix addresses the corrected cause.
  Often it does not, and that becomes the primary finding.
- **P2 corrected.** Redo the affected part of the map before you continue.
- **P3 rejected.** Do not file twenty implementation nitpicks about code that the author will
  rewrite.

A stop is a legitimate and valuable outcome.

## Record the premises

Put every agreed proposition in the report's **Premises** section, with the findings that depend on
it. A finding may exist only because the human said "sessions must expire eagerly". That finding
must say so. Then a second reader can disagree with the premise instead of the conclusion. If an
answer contradicts something in the code, that contradiction is itself a finding.

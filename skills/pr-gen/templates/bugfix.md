# Bug Fix PR Template

Use this template for any PR whose primary purpose is fixing a bug — a correctness, safety, security, or resilience defect. Prefer this template over the generic concise template whenever the PR has an identifiable wrong behavior being corrected.

## Required structure

A bugfix PR description MUST have exactly these four sections, in this order, with these exact headings:

1. `## Summary`
2. `## <Invariants section>` — see below for heading choice
3. `## The fix`
4. `## Tests enforcing the <invariants|behavior>`

No other top-level sections. No "Problem Description", "Impact Analysis", "Rollback Plan", "Monitoring", "Code Comparison", or boilerplate blocks. If something doesn't fit one of the four sections, it doesn't belong in the description.

### Heading choice for section 2

Pick the one that fits the bug and use it consistently in section 4:

- **`## Security invariants`** — security, consensus, or protocol-correctness bugs. Use when the fix defends an invariant whose violation is exploitable or corrupts state.
- **`## Correctness invariants`** — non-security correctness bugs with a crisp invariant (e.g., "persisted X must equal persisted Y", "operation is idempotent under retries").
- **`## Expected behavior`** — simple bugs where framing as an invariant is awkward (wrong error message, off-by-one, bad default). Keep it tight: state what the code should do.

Section 4's heading mirrors section 2: "Tests enforcing the security invariants" / "Tests enforcing the correctness invariants" / "Tests enforcing the expected behavior".

### What goes in each section

**`## Summary`** — 1–3 sentences. State the bug, where it lives, and (if not obvious from the title) the user-visible or security consequence. If the bug was flagged externally (Slack thread, issue, audit finding), link it here in one sentence. No background paragraphs.

**`## <Invariants section>`** — a numbered list of the invariants (or expected behaviors) the fix restores. Each entry is one line stating the invariant and one clause on why it matters. No code blocks, no prose paragraphs. Example shape:

```
1. **X ↔ Y**: <one-line invariant>. <one clause on consequence of violation>.
2. **Idempotency**: <one-line invariant>. <one clause on consequence of violation>.
```

If section 2 is `## Expected behavior`, use a short bulleted list of "should" statements instead of numbered invariants.

**`## The fix`** — bullets describing the change, each with a file link. Lead with the mechanism, not the motivation (motivation is already in section 2). Prefer linking to files over pasting diffs. No before/after code blocks unless a one-line snippet genuinely clarifies the fix.

**`## Tests enforcing the <invariants|behavior>`** — bullets, one per test, with:

- Test kind in **bold** (e.g., **Unit proptest**, **Unit test**, **Integration test**, **E2E**).
- Test name in backticks.
- Link to the test file.
- One sentence on what invariant from section 2 it enforces and (where meaningful) a note like "pre-fix implementation fails this test".

Every invariant in section 2 should be covered by at least one test in section 4. If an invariant is deliberately not tested, say so and explain why in one clause.

## Reference example

```markdown
## Summary

Fixes a retry-safety bug in `create_graph_and_start_presigning` (claimer pegin flow) flagged in [this Slack thread](…): the function regenerated fresh claimer WOTS keypairs on every call while the store uses `ON CONFLICT DO NOTHING`, leaving the persisted `TxGraph` committed to pubkeys whose secret keys were discarded — breaking Assert signing on any retry.

## Security invariants

On every call for the same `(pegin_txid, claimer_pk)`:

1. **WOTS ↔ graph**: `TxGraph.claimer_wots_keys` must equal `public_keys()` of the stored keypair. Divergence breaks Assert signing.
2. **GC data ↔ graph**: per-challenger GC data in the graph must equal the rows in `pegin_gc_data`.
3. **Retry-safety**: any value committed into the overwrite-on-conflict `TxGraph` that is also persisted in a non-overwriting row must match that row across arbitrary sequential or concurrent retries.

## The fix

- Replace fresh-generate + `store_wots_keypairs` with an atomic `get_or_generate_wots_keypairs` DB method using `INSERT … ON CONFLICT … DO UPDATE … RETURNING` ([wots.rs](crates/vaultd/src/db/claimer/wots.rs)).
- Call it from `create_graph_and_start_presigning` and document the retry-safety contract on the function ([pegin.rs](crates/vaultd/src/workers/claimer/pegin.rs)).

## Tests enforcing the security invariants

- **Unit proptest** `prop_get_or_generate_wots_keypairs_never_overwrites_on_retry` ([wots.rs](crates/vaultd/src/db/claimer/wots.rs)) — sequential + concurrent retries converge on the first-installed keypair. Enforces invariant 3 at the DB layer.
- **Unit proptest** `prop_create_graph_commit_pattern_is_retry_safe` ([pegin.rs](crates/vaultd/src/workers/claimer/pegin.rs)) — full commit pattern; asserts persisted graph's WOTS + GC data match stored rows. Pre-fix implementation fails on the first retry. Enforces invariants 1–3.
- **E2E** `test_crash_pegin_at_pending_challenger_presigning` ([crash_resilience_e2e.rs](crates/vaultd/tests/crash_resilience_e2e.rs)) — crash-and-restart asserts the invariants post-restart and post-flow. Enforces invariants 1–2 end-to-end.
```

## Pre-flight (before generating anything)

Before filling this template in, verify the branch actually contains what each section needs:

- **Section 2** — can you state at least one invariant / expected behavior in one sentence? (If not, the branch is missing context, not description.)
- **Section 3** — is there a non-trivial code change in HEAD that implements the fix?
- **Section 4** — is there at least one test in the diff that enforces each invariant from section 2, and is the test wired into the project's test harness?

## Hard rules

- Exactly four top-level sections. No more.
- No "Checklist", "Related Issues", "Rollback Plan", "Monitoring", "Dependencies", "Documentation" sections — if the PR template requires checkboxes, keep them after section 4 under their template-required heading, untouched.
- No emoji status markers (`✅`) outside of test bullets where they add real information.
- No before/after code block pairs. The diff shows the code.
- Every test listed must exist in HEAD (verify with `git show HEAD:<path>`).
- Do not repeat the Slack/issue link across sections — once, in Summary.

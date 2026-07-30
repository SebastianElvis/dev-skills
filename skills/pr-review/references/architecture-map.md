# Writing the architecture map

Build the model of the subsystem after you know what the change is. Write it before any finding.

## Why this comes first, and why bottom-up

The layers are in the order of the cost of an error. A bad state transition is a bug class. A
broken trust assumption is an incident. A bad column causes migrations, backfills, and dual-read
code for a year. Do not skip a layer silently. One line is enough for a layer that the PR does not
touch, for example "L1 unchanged: no migration, no serialized format in the diff".

## Reading outward

```bash
git show "origin/$base:path/to/file"                    # the file as it stands, whole
grep -rn 'symbolName' --include='*.<ext>' | grep -v 'path/to/file'   # callers
git log --find-renames --oneline -20 -- path/to/file
git log -S 'invariantOrGuard' --oneline -- path/to/file
```

Run `git log -S` on a guard or a constant that the PR removes. The commit message usually names the
bug that the guard prevented. A guard that "fix race in reconnect" added, and that the PR deletes
with no explanation, is important.

## L1 — Data model and persistence

**What to enumerate:** schema (tables, columns, types, nullability, defaults, indexes,
constraints); serialized formats (JSON payloads, protobuf, cookies, tokens); wire and message
formats; cache keys and their time-to-live (TTL) values; file layouts; queue message shapes.

**The questions:**

- Which invariants does *storage itself* enforce — uniqueness, foreign keys, `NOT NULL`, check
  constraints, ordering? No code path can bypass them. Which does this PR add, drop, or weaken?
- **Rolling-deploy compatibility.** During a deploy, old code and new code run at the same time
  against one database. Can old code read what new code writes? Can new code read what old code
  wrote? A `NOT NULL` column with no default breaks old writers. A column that new code reads, but
  that only new writes populate, is null for every existing row. The safe order is expand →
  backfill → migrate → contract. Each stage is backward compatible with the stage before it. Send
  the author Pete Hodgson's [expand/contract write-up](https://blog.thepete.net/blog/2023/12/05/expand/contract-making-a-breaking-change-without-a-big-bang/)
  if they dispute this. A PR that expands and contracts in one deploy has no safe rollback point.
  That is a blocking finding, not a style note.
- Is the migration **reversible**? Is there a backfill? What happens to the rows that the code
  writes between the deploy and the backfill?
- Does the PR add an index to a large table without `CONCURRENTLY` (or the equivalent)?
- **Semantic drift.** Examples are seconds that become milliseconds, a nullable flag that changes
  from "unknown" to "false", an enum value with a new purpose, and a timestamp that changes from
  event time to ingest time. Search for a field with a changed writer and an unchanged reader.

```bash
find . -path '*migration*' -newer .git/HEAD -o -path '*migrations*' -name '*.sql' | head
git diff "origin/$base...$head" -- '*migration*' '*.sql' '*schema*'
```

## L2 — State machine

**What to enumerate:** the states, the transitions, the trigger for each transition, the terminal
states, and the transitions that can occur at the same time. Draw the state machine if it helps:

```
before:  IDLE → CONNECTING → OPEN → CLOSING → CLOSED
                     ↓                  ↑
                   FAILED ──────────────┘

after:   IDLE → CONNECTING → OPEN → DRAINING → CLOSING → CLOSED
                     ↓                             ↑
                   FAILED ─────────────────────────┘
```

**The questions:**

- Which transitions are **reachable** now, but were not reachable before?
- Which transitions are **unreachable** now? Is the code that handles them dead code, or is the
  unreachable transition the bug?
- Is a new state **terminal by accident** — reachable, but with no exit transition?
- Can the code enter a state **twice**, or from two paths at the same time?
- Does every new state define a behavior for the operations that the old states supported?
- **Against L1:** a state that exists only in memory is a mismatch. An enum that the PR widens in
  the code but not in the schema is also a mismatch.

State machines often hide a symptomatic fix: a new state that routes *around* a bug, instead of a
fix to the transition that caused the bug.

## L3 — Actors, trust boundaries, and the security model

**What to enumerate:**

- **Principals.** Anonymous callers, authenticated users, tenants, internal services, batch jobs,
  operators, the continuous integration (CI) system. Who can reach this code?
- **What you trust each principal to do**, and the authorization model that enforces the trust —
  record ownership, roles, attributes, tenancy.
- **The boundary.** Where exactly does data cross from untrusted to trusted? Name the function.
- **Standing assumptions.** Examples: "the gateway has already authenticated, so `ctx.User` is
  non-nil"; "this queue is internal-only"; "config and env vars are operator-supplied and therefore
  trusted"; "this service is not reachable from the public internet"; "IDs in this table are not
  user-supplied."

**A PR that quietly invalidates a standing assumption is your highest-severity finding.** You see
it only if you state the assumption first.

**The questions:**

- Does the PR add a new principal, or let an existing principal reach something new?
- Does it **move the boundary** — parse untrusted input earlier, or validate input later?
- Does it move an authorization decision to a place where the code can skip it? Examples are a
  helper that only some paths call, a cache hit that bypasses it, and a short-circuit return.
- Does it **extend trust to a new input** — a new header, a new config source, or a new upstream
  service whose response now controls the flow of execution?
- Does it break an assumption *elsewhere*? A change that makes an internal queue externally
  writable does not change the code of the consumer at all, and it breaks every consumer.

## L4 — Component boundaries

**What to enumerate:** module and service ownership, allowed dependency directions, layering
rules, and which application programming interface (API) is public and which is internal.

**The questions:**

- Which component owns this change? Does the change stay inside that ownership?
- Does it introduce a dependency in a disallowed direction, or a cycle?
- Does it use the internals of another module instead of the interface of that module?
- Does it skip a layer — a handler that talks straight to storage, or business rules in a migration?
- Is there now **a second way to do something the codebase does one way**? Examples are two retry
  mechanisms, two config loaders, and two ways to construct the same entity.
- Does the change make a file longer than about 1000 lines? Name its second responsibility.

## Affected code

The quantity of callers matters. Three callers are a different risk from three hundred:

```bash
grep -rn 'changedFunction' --include='*.<ext>' | wc -l
```

Then find the **implicit** dependent code, which never calls the function. SKILL.md lists that
code. Add to it the dashboards and the alerts that use a log line or a metric name.

## Worked example (abbreviated)

> **L1 — Data model.** `sessions` has `(id uuid pk, user_id, created_at, expires_at timestamptz
> NOT NULL)`. Only the code enforces expiry; no constraint enforces it. This PR adds
> `revoked_at timestamptz NULL` with a migration that is reversible and needs no backfill. Old
> code ignores the column, and new code treats `NULL` as "not revoked", so the change is
> rolling-deploy safe in both directions. There is no semantic drift: no existing field changes
> its meaning.
>
> **L2 — State machine.** Sessions had two states (VALID → EXPIRED, by the clock). The PR adds
> REVOKED, and an explicit admin action moves a session from VALID to REVOKED. REVOKED is terminal,
> and that is correct: no un-revoke path exists, and the PR implies none. L1 represents both
> terminal states (`expires_at` in the past, `revoked_at` non-null), so the data model can express
> every state.
>
> **L3 — Trust.** The principals are anonymous, user, and admin. The standing assumption in this
> package is that `ctx.User` is non-nil, because `middleware/auth.go:44` runs first on every route
> in the `/api` group. **The PR registers `POST /api/sessions/:id/revoke` on the `/admin` group,
> which mounts a different middleware chain** (`router.go:88`). That chain authenticates the
> caller, but it does not check the admin role, because every other route on that group checks the
> admin role inside its own handler. The new handler makes no such check. So the assumption
> "routes under `/admin` are admin-only" is false here, and any authenticated user can revoke any
> session by id. The lookup at `session.go:120` is `Session.find(id)`, which does not limit the
> result to the caller.
>
> **L4 — Boundaries.** The change stays inside the `auth` package. It adds no new dependency
> directions. The handler calls the store directly, which is consistent with the other six
> handlers in the package.
>
> **Affected code.** 22 call sites read session validity, all through `Session.IsValid()`, which
> the PR updates — so every call site obeys the new state. Implicit dependent code: the
> `sessions_active` metric counts `expires_at > now()`, so it now over-counts revoked sessions
> (`metrics/session.go:19`).

The L3 paragraph *is* the blocking finding, and you reach it only because you write down the
standing assumption first. The metric under affected code is a real non-blocking finding that
nobody sees in the diff alone.

## Common failures

- **The reviewer lists the changed files.** That is `--stat`, not a map.
- **The reviewer skips L3 because "this isn't a security PR."** Changes that are not about
  security break trust assumptions most often.
- **The reviewer skips the map on a small PR.** A two-line diff can change a state machine or a
  trust boundary. Write a shorter map. Always write a map.

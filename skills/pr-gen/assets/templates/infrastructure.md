# Infrastructure template

Use only for **large** infrastructure PRs — provisioning new cloud resources,
material topology changes, or anything that affects cost, DR posture, or
on-call. For small infra plumbing, prefer the feature template.

## Required sections

1. `## Summary` — 1–2 sentences. What's being deployed or changed and why now.
2. `## Resources` — bulleted list of resources created, modified, or removed,
   each with a repo-relative file link to the IaC source of truth. Lead with
   the resource name; one clause on the role.

## Optional sections — include only when materially different

- `## Topology` — when reviewers need a mental model that isn't obvious from
  the diff (new ingress/egress, cross-region replicas, new trust boundary).
  Prefer one short paragraph or a labeled list over ASCII art.
- `## Rollout` — staged or coordinated changes. One bullet per gate.
- `## Cost` — when the change adds a recurring line item users will see on
  the bill. State the order of magnitude, not a fake-precise dollar figure.
- `## DR / Backup` — when the change alters RPO/RTO, backup retention, or
  the failover path.
- `## Rollback` — when rolling back is non-trivial (data loss risk, manual
  steps, irreversible state).

## Output shape

```markdown
## Summary

Provisions a regional Cloud SQL Enterprise Plus primary with a cross-region
read replica for staging, replacing the previous single-zone instance.

## Resources

- `db-stg-primary` — Enterprise Plus, regional, automated daily backups
  ([sql.ts:24](cloud/db/sql.ts#L24)).
- `db-stg-replica` — cross-region async read replica
  ([sql.ts:88](cloud/db/sql.ts#L88)).
- IAM bindings granting the app service account `cloudsql.client`
  ([iam.ts:12](cloud/db/iam.ts#L12)).

## Rollout

- Stack apply on staging only — production stack unchanged in this PR.
- Cutover script in [migrate.sh](cloud/db/migrate.sh) replays writes from the
  legacy instance during a 5-minute read-only window.
```

## Anti-patterns to avoid

- ASCII architecture diagrams that don't match the code. Link the IaC instead.
- Sections filled with generic compliance / security boilerplate.
- Listing every IAM binding — link the file.
- Fabricated cost estimates. Either cite the cloud provider's pricing page or
  give an order of magnitude.

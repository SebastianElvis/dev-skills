# Infrastructure template

You use this default for large infrastructure changes without a required repository template.
These changes include new cloud resources, network connections, or recovery procedures.
You use the feature template for small infrastructure changes.
You write all output in Simplified Technical English (ASD-STE100).

## Required structure

1. `## Summary`: You state the operational need and resulting change in one or two sentences.
2. `## Resources`: You link each meaningful resource change to its configuration.

The body states validation evidence or its absence.
You distinguish configuration changes from observed deployment results.

## Optional sections

Each optional section requires its condition:

| Section | Condition |
| --- | --- |
| `## Topology` | Connections, regions, or trust boundaries change. |
| `## Rollout` | The change requires ordered steps or coordinated deployment. |
| `## Cost` | Evidence supports a material cost change. |
| `## DR / Backup` | Disaster recovery (DR) targets, backup retention, or failover procedures change. |
| `## Rollback` | Reversal requires manual steps or risks data loss. |

You define DR when you use that heading.
You cite the source and assumptions for a cost estimate.
You mark unknown costs explicitly.

## Example

```markdown
## Summary

- The database configuration adds a replica for recovery after a regional failure.

## Resources

- `db-replica` receives asynchronous updates in a second region ([database.tf](cloud/database.tf)).

## Rollout

- The [procedure](docs/rollout.md) requires an operator to create the replica before the application uses it.
- The agent did not validate the configuration or deploy the replica.
```

## Final check

- [ ] The body retains Summary and Resources in order.
- [ ] The body distinguishes configuration, validation, and deployment results.
- [ ] The output follows the length limit and Simplified Technical English rules.

# Infrastructure template

You use this default for large infrastructure changes without a required repository template.
These changes include new cloud resources, network connections, or recovery procedures.
You use the feature template for small infrastructure changes.
You write all output in Simplified Technical English (ASD-STE100).

## Required structure

Each bullet contains one sentence that states one point.
The body contains three short sections in this order:

1. `## Problem`: You state the operational need or failure.
2. `## Solution`: You explain the configuration change. You include necessary deployment or recovery steps here.
3. `## Validation`: You distinguish configuration checks from observed deployment results. You state absent execution evidence explicitly.

You omit risk sections and risk ratings.
You place relevant issue links after the three sections.

## Example

```markdown
## Problem

- The database lacks a replica for recovery after a regional failure.

## Solution

- The configuration adds an asynchronous replica in a second region.
- An operator must create the replica before the application uses it.

## Validation

- The agent did not validate the configuration or deploy the replica.
```

## Final check

- [ ] The body states the problem, solution, and validation in order. Each bullet contains one sentence that states one point.
- [ ] The body distinguishes configuration, validation, and deployment results.
- [ ] The body omits risk sections and risk ratings.
- [ ] The output follows the length limit and Simplified Technical English rules.

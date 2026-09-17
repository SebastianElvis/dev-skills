# Bugfix template

You use this default for bugfixes without a required repository template.
You write all output in Simplified Technical English (ASD-STE100).

## Required structure

Each bullet contains one sentence that states one point.
The body contains three short sections in this order:

1. `## Problem`: You state the trigger, defect, and effect.
2. `## Solution`: You explain how the correction addresses the root cause and restores the expected behavior.
3. `## Validation`: You summarize regression coverage and observed results. You state relevant coverage gaps or absent execution evidence.

You omit risk sections and risk ratings.
You place relevant issue links after the three sections.

## Example

This example assumes verified source and assertions. The agent did not run the tests.

```markdown
## Problem

- Repeated requests create duplicate payments that charge the customer twice.

## Solution

- The handler checks the request key before it creates a payment.
- Repeated requests now return the same payment.

## Validation

- The unit test checks that repeated requests return the same payment.
- The agent did not run the tests.
```

## Final check

- [ ] The body states the problem, solution, and validation in order. Each bullet contains one sentence that states one point.
- [ ] The validation separates coverage from execution evidence. Relevant gaps remain explicit.
- [ ] The body omits risk sections and risk ratings.
- [ ] The output follows the length limit and Simplified Technical English rules.

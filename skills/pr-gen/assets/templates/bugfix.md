# Bugfix template

You use this default for bugfixes without a required repository template.
You write all output in Simplified Technical English (ASD-STE100).

## Required structure

The body contains exactly four sections in this order:

1. `## Summary`: You state the trigger, defect, and effect in one or two short sentences.
2. The invariant section: You state each restored requirement.
3. `## The fix`: You explain the root cause and correction with file links.
4. The test section: You map tests or coverage gaps to each requirement.

You select matching invariant and test headings:

| Invariant heading | Test heading |
| --- | --- |
| `## Security invariants` | `## Tests enforcing the security invariants` |
| `## Correctness invariants` | `## Tests enforcing the correctness invariants` |
| `## Expected behavior` | `## Tests enforcing the expected behavior` |

Security invariants protect security or protocol correctness.
Correctness invariants define precise relationships between values or states.
Other defects use expected behavior.
Each invariant uses one numbered sentence with an explicit subject.
Expected behavior uses short bullets instead of numbered invariants.
You link a relevant problem source once in Summary.

Each test bullet names its kind, identifier, file link, and verified requirement.
A separate test bullet states execution evidence or its absence.

## Example

This example assumes verified source and assertions. The agent did not run the tests.

```markdown
## Summary

- Repeated requests create duplicate payments that charge the customer twice.

## Correctness invariants

1. The payment service returns the same payment for each request with the same request key.

## The fix

- The [handler](src/payments.py) now checks the request key before it creates a payment.

## Tests enforcing the correctness invariants

- **Unit test:** `test_repeated_request` checks that both requests return the same payment ([test_payments.py](tests/test_payments.py)).
- The agent did not run the tests.
```

## Final check

- [ ] The body retains the four required sections in order.
- [ ] Each requirement has verified coverage or an explicit gap.
- [ ] The body separates test coverage from execution evidence.
- [ ] The output follows the length limit and Simplified Technical English rules.

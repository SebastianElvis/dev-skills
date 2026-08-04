# Change types

Classify the final behavior, not the PR title or label. Pick one primary type. A PR with two
independent types is a split candidate.

Count production code, tests, documentation, generated files, and removed behavior separately. Name
the largest net-new behavior.

## Bugfix

- Confirm the failure from the code.
- Find the first line where the invariant fails.
- Check whether another guard already prevents the failure.
- Require a root-cause fix or a clearly identified symptomatic fix.
- Require a regression test that fails without the fix.

Give most attention to root-cause level and correctness.

## Security fix

- Read the audit result, vulnerability record, or advisory.
- Confirm that the vulnerability is reachable here.
- Search for every instance of the vulnerable pattern.
- Check that validation occurs at the trust boundary.
- Require a test with the attack input.

Give most attention to security and correctness. The fix must close the defect class or track each
remaining instance.

## Feature

- Identify the supported use case and its source.
- Confirm that the project wants the feature.
- Find the smallest interface, state, and dependency changes.
- Check whether the existing model already supports the use case.
- Reject speculative options or extension points with no current use.
- Treat a new public API, persistent state, operator control, or runtime obligation as new behavior.

Give most attention to necessity and architecture.

## Refactor

- Require the PR to preserve observable behavior.
- Require a specific reason for the refactor.
- Check every deleted or replaced behavior.
- Examine every test change for a behavior change.
- Separate mechanical changes from semantic changes.
- Treat new observable behavior as a feature or bugfix, even when it replaces old code.

Give most attention to correctness and necessity.

## Performance

- Require a measurement from a realistic workload.
- Confirm that the changed code is the bottleneck.
- Compare the gain with added memory, complexity, and concurrency risk.
- Prefer removal of work before caches or small local optimizations.
- Require evidence that the change preserves correctness.

Give most attention to verifiability and correctness.

## Infrastructure, dependencies, or configuration

- Identify every consumer and affected subsystem.
- Check partial deployment and rollback behavior.
- Verify each dependency name, version, import, and current need.
- Check loosened constraints and changed defaults.
- Review a small diff deeply when it changes shared behavior.

Give most attention to necessity and security.

## Documentation

- Check every factual claim against `HEAD`.
- Verify each symbol, option, path, and example.
- Do not reject correct documentation because of prose preferences.

Give most attention to verifiability. Use the lowest review depth that still checks each claim.

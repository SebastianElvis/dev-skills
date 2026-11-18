# Reference import recovery

The Operator submits items and a credential version through the CLI.
Intake requires a nonempty list of items and a positive credential version.
An intake error creates no job.
A valid request creates a queued job and a queued event.

The worker accepts only queued or backoff jobs whose ready_at is not in the future.
The safety scan quarantines unsafe jobs before any warehouse request.
A safe job becomes running, increases cycle_attempts, and records an attempt event.
The external Warehouse API returns accepted, credentials_error, or throttled.

Acceptance archives the import and sets index_state to pending.
A credentials error suspends the import immediately.
Throttling causes 60-second backoff while cycle_attempts is less than 3.
The third throttled attempt suspends the import.

The Operator can resume only a suspended import.
A credentials error requires a newer credential version before resume.
A throttled suspension requires no credential change.
A failed resume check leaves the job unchanged.
Resume returns the same job to queued with cycle_attempts and ready_at equal to zero.
Resume keeps the same identifier and prior history. The event sequence continues.
Every recorded event increases event_sequence. No action resets that sequence.

The Operator can cancel queued, backoff, or suspended jobs.
Cancellation produces a cancelled event. The worker then ignores the job.
Other states permit no cancellation.

The index worker accepts only archived jobs with pending indexing.
The external Search API decides indexed or index_failed.
Both outcomes add an event and preserve the archived import state.
The workflow has no automatic indexing retry.

The model stores state and history in memory. The figure must not invent a database or durable restart guarantees.
The first reference sets the minimum visual quality. The second reference supplies supporting workflow composition.
The final width is 260 mm. The minimum text size is 8 pt.

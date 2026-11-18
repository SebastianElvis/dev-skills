# Reference release workflow

The Operator uses a CLI. The model stores releases and history in memory.
Creation requires nonempty package text. An invalid request creates no release.
A valid request creates draft and records created.
Approval requires draft and the maintainer role. It enters queued and records approved.
A failed approval raises PermissionError without a change or event.

The worker runs only queued releases. Other states return without a change or event.
The worker enters building, increases attempts, and records build_started before the external Runner API call.
A ready result enters built, sets publish_state pending, and records build_ready.
A transient result with attempts below 2 enters queued and records retry_queued.
The second transient result enters failed and records retry_exhausted.
An invalid result enters rejected and records input_rejected.
An unknown result raises ValueError. The release stays building with no outcome event.

Manual retry requires failed and the maintainer role. It queues the same release and resets attempts to zero.
Manual retry records manual_retry. It keeps the identifier and prior history. The event sequence continues.
A failed retry check raises PermissionError without a change or event.
Only approval and retry check the role.
Cancellation accepts draft, queued, or failed. It enters cancelled and records cancelled without a role check.
Other cancellation states raise ValueError without a change or event.

Publication requires built and publish_state pending.
The external Registry API decides success or failure.
Publication changes publish_state to published or publish_failed and records that event.
Both outcomes preserve the built state. No automatic publication retry exists.
A failed publication check raises ValueError without a change or event.
Every record call increases event_sequence and appends the named event. No action resets it or removes prior events.

The figure must preserve the distinction between state, publish_state, attempts, and the permanent event sequence.
The figure must show all required event writes and meaningful rejected-operation paths.
The model supplies no durable storage or deployment guarantees.
The final width is 180 mm. The minimum text size is 8 pt.
The first reference sets the visual minimum. The second reference supplies supporting workflow composition.

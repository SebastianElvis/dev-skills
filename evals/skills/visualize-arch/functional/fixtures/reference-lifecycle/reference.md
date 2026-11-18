# Reference lifecycle

A Dispatcher submits a shipment through Web or CLI.
The API checks dispatcher membership and a nonempty destination before it stores a run.
An intake error stops the request without a stored dispatch run.
A valid request produces a queued run and a Job queue entry.

The Scheduler starts the Worker every 60 seconds.
The Worker consumes a queued run and marks it running.
The Worker increments attempt_count and creates a provider attempt.
The Worker calls ParcelCarrier.

An accepted response marks the run sent, stores a receipt, records an audit event, and queues a notice.
A rejected response marks the run failed with provider_rejected and records the failed attempt and audit event.
A provider rejection permits no automatic retry and no manual retry.

A timeout marks the provider attempt failed.
The first timeout requeues the same run because attempt_count is less than 2.
The second timeout marks the run failed with timeout.
Both timeout outcomes create audit events.
A Dispatcher can manually retry only a failed timeout run.
The manual retry resets attempt_count to zero and requeues the same run.
Provider attempt sequence numbers remain unique across manual retry cycles.

The Notifier consumes a notice, reads its receipt, calls MailRelay, and records a notice event.
The notice branch follows successful dispatch. It does not decide the dispatch outcome.
The figure must distinguish conditions, actions, stored evidence, retry paths, intake errors, and stored terminal outcomes.
The requested final width is 260 mm. The minimum text size is 8 pt.
The first reference sets the minimum visual quality. The second reference supplies supporting workflow design examples.

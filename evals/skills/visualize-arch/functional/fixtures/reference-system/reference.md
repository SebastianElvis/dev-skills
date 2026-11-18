# Reference system

Dispatch Hub has two actors: Dispatcher and Auditor.
The Dispatcher uses Web or CLI. The Auditor reads status through Web.
Both clients use the API. The API returns status from SQLite to each client.
Authorization checks dispatcher membership before intake and manual retry.
The supplied status method has no authorization check. The figure must preserve that distinction.

The owned components are Web, CLI, API, Authorization, SQLite, Job queue, Scheduler, Worker, Notice queue, and Notifier.
The external services are ParcelCarrier and MailRelay.
The queues are internal components, not independent deployment services.
The figure can group clients, dispatch execution, and stored records when those groups clarify the logical structure.

The API stores a queued run in SQLite and places its identifier on the Job queue.
The Scheduler starts the Worker every 60 seconds.
The Worker takes a queued identifier and calls ParcelCarrier.
The Worker records attempts, outcomes, audit events, and successful delivery receipts in SQLite.
An accepted response also produces a Notice queue entry.
The Notifier reads the receipt, calls MailRelay, and records a notice event in SQLite.
Configuration relationships remain separate from ordered actions.
The diagram must distinguish status reads, dispatch work, and notice delivery without invented components.

The requested final width is 300 mm. The minimum text size is 8 pt.
The first attached reference sets the minimum visual quality.
The second attached reference supplies supporting architecture design examples.
The final output includes editable source, vector files, a Makefile, caption, and design notes.

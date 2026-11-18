#!/usr/bin/env bash
# This script creates an isolated import recovery fixture.
set -euo pipefail
dir="$(mktemp -d -t visualize-arch-eval-XXXXXX)"
cd "$dir"
git init -q -b main
git config user.email eval@example.com
git config user.name Eval
git config commit.gpgsign false
git config core.hooksPath /dev/null
mkdir -p src
cat > src/imports.py <<'PY'
from dataclasses import dataclass, field


@dataclass
class Job:
    id: int
    payload: dict
    credential_version: int
    state: str = 'queued'
    cycle_attempts: int = 0
    event_sequence: int = 0
    ready_at: int = 0
    reason: str | None = None
    index_state: str | None = None
    events: list = field(default_factory=list)

    def record(self, event):
        self.event_sequence += 1
        self.events.append((self.event_sequence, event))


class Importer:
    def __init__(self):
        self.next_id = 1

    def submit(self, payload, credential_version):
        if not isinstance(payload.get('items'), list) or not payload['items'] or credential_version < 1:
            raise ValueError('The request needs nonempty items and a positive credential version.')
        job = Job(self.next_id, payload, credential_version)
        self.next_id += 1
        job.record('queued')
        return job

    def tick(self, job, warehouse, now):
        if job.state not in {'queued', 'backoff'} or now < job.ready_at:
            return
        if not job.payload.get('safe', False):
            job.state = 'quarantined'
            job.record('quarantined')
            return
        job.state = 'running'
        job.cycle_attempts += 1
        job.record('attempt_started')
        outcome = warehouse.write(job.payload, job.credential_version)
        if outcome == 'accepted':
            job.state, job.index_state, job.reason = 'archived', 'pending', None
        elif outcome == 'credentials_error':
            job.state, job.reason = 'suspended', 'credentials_error'
        elif outcome == 'throttled':
            job.reason = 'throttled'
            if job.cycle_attempts < 3:
                job.state, job.ready_at = 'backoff', now + 60
            else:
                job.state = 'suspended'
        else:
            raise ValueError('The warehouse returned an unknown outcome.')
        job.record(job.state)

    def resume(self, job, credential_version=None):
        if job.state != 'suspended':
            raise ValueError('Only a suspended job permits resume.')
        if job.reason == 'credentials_error':
            if credential_version is None or credential_version <= job.credential_version:
                raise ValueError('The credentials need a newer version.')
            job.credential_version = credential_version
        job.state, job.reason, job.cycle_attempts, job.ready_at = 'queued', None, 0, 0
        job.record('manual_resume')

    def cancel(self, job):
        if job.state not in {'queued', 'backoff', 'suspended'}:
            raise ValueError('This state permits no cancellation.')
        job.state = 'cancelled'
        job.record('cancelled')

    def index(self, job, search):
        if job.state != 'archived' or job.index_state != 'pending':
            raise ValueError('Only an archived job with pending indexing permits this action.')
        job.index_state = 'indexed' if search.index(job.payload) else 'index_failed'
        job.record(job.index_state)
PY
cat > README.md <<'MD'
# Import Desk

The Operator submits an import through the CLI.
The CLI calls Importer.submit with items and a credential version.
The source models a logical workflow. It stores job state and history in memory.
The entry checks require nonempty items and a positive credential version.
An entry error creates no job.

A worker calls Importer.tick for queued or backoff jobs when ready_at permits execution.
The safety scan quarantines an unsafe job before any warehouse request.
A safe job increments its cycle attempt count and calls the external Warehouse API.
Acceptance archives the job and schedules independent search indexing.
A credentials error suspends the job immediately.
Throttling causes 60-second backoff until the third attempt suspends the job.

The Operator can resume a suspended job.
A credentials error requires a newer credential version before resume.
A throttled suspension requires no credential change.
Resume keeps the job identifier and prior history. The event sequence continues.
Resume resets cycle_attempts and ready_at to zero.
Every state event increases event_sequence. The event sequence never resets.

The Operator can cancel a queued, backoff, or suspended job.
The worker ignores cancelled jobs.
An index worker calls the external Search API for archived jobs with pending indexing.
Index success or failure changes index_state and adds an event.
Index failure does not change the archived import outcome.
The workflow has no automatic indexing retry.
MD
git add .
git commit -q -m "Add the import recovery fixture"
echo "$dir"

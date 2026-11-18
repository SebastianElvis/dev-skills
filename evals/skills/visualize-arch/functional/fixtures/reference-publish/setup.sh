#!/usr/bin/env bash
# This script creates an isolated release fixture.
set -euo pipefail
dir="$(mktemp -d -t visualize-arch-eval-XXXXXX)"
cd "$dir"
git init -q -b main
git config user.email eval@example.com
git config user.name Eval
git config commit.gpgsign false
git config core.hooksPath /dev/null
mkdir -p src
cat > src/releases.py <<'PY'
from dataclasses import dataclass, field


@dataclass
class Release:
    id: int
    package: str
    state: str = 'draft'
    attempts: int = 0
    event_sequence: int = 0
    publish_state: str | None = None
    events: list = field(default_factory=list)

    def record(self, name):
        self.event_sequence += 1
        self.events.append((self.event_sequence, name))


class Desk:
    def __init__(self):
        self.next_id = 1

    def create(self, package):
        if not isinstance(package, str) or not package.strip():
            raise ValueError('The package must contain text.')
        release = Release(self.next_id, package)
        self.next_id += 1
        release.record('created')
        return release

    def approve(self, release, role):
        if release.state != 'draft' or role != 'maintainer':
            raise PermissionError('Approval requires a draft and the maintainer role.')
        release.state = 'queued'
        release.record('approved')

    def run(self, release, runner):
        if release.state != 'queued':
            return
        release.state = 'building'
        release.attempts += 1
        release.record('build_started')
        outcome = runner.build(release.package)
        if outcome == 'ready':
            release.state, release.publish_state = 'built', 'pending'
            release.record('build_ready')
        elif outcome == 'transient':
            if release.attempts < 2:
                release.state = 'queued'
                release.record('retry_queued')
            else:
                release.state = 'failed'
                release.record('retry_exhausted')
        elif outcome == 'invalid':
            release.state = 'rejected'
            release.record('input_rejected')
        else:
            raise ValueError('The runner returned an unknown outcome.')

    def retry(self, release, role):
        if release.state != 'failed' or role != 'maintainer':
            raise PermissionError('Retry requires a failed build and the maintainer role.')
        release.state, release.attempts = 'queued', 0
        release.record('manual_retry')

    def cancel(self, release):
        if release.state not in {'draft', 'queued', 'failed'}:
            raise ValueError('This state permits no cancellation.')
        release.state = 'cancelled'
        release.record('cancelled')

    def publish(self, release, registry):
        if release.state != 'built' or release.publish_state != 'pending':
            raise ValueError('Publication requires a built release with pending publication.')
        release.publish_state = 'published' if registry.push(release.package) else 'publish_failed'
        release.record(release.publish_state)
PY
cat > README.md <<'MD'
# Release Desk

The Operator calls Desk methods through a CLI.
The model stores each Release and its event history in memory.
A valid package contains nonempty text. Creation produces a draft and records created.
An invalid package creates no release.

Approval requires a draft and the maintainer role. Approval queues the release and records approved.
The worker runs only queued releases. Other states return without a change or event.

The worker increments attempts, enters building, and records build_started before the external Runner API call.
A ready result enters built, sets publication pending, and records build_ready.
A transient result queues one automatic retry with retry_queued. The second transient result fails with retry_exhausted.

An invalid result rejects the release with input_rejected.
An unknown result raises ValueError and leaves building with no outcome event.

Manual retry requires failed and the maintainer role. It resets attempts to zero and records manual_retry.
The same identifier and prior history remain. The event sequence continues.
Only approval and manual retry check the role.
Cancellation accepts draft, queued, or failed. It enters cancelled and records cancelled without a role check.
Other cancellation states raise ValueError without a change or event.

Publication requires built with publish_state pending.
The external Registry API returns success or failure. Publication records published or publish_failed and changes publish_state.
Both outcomes preserve the built state. The model has no automatic publication retry.
Every record call increases event_sequence and appends the named event. No action resets that sequence or removes prior events.
The source defines a logical workflow. The figure must not invent durable storage or deployment services.
MD
git add .
git commit -q -m "Add the release fixture"
echo "$dir"

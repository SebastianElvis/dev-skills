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

#!/usr/bin/env bash
# This script creates an isolated dispatch platform.
set -euo pipefail
dir="$(mktemp -d -t visualize-arch-eval-XXXXXX)"
cd "$dir"
git init -q -b main
git config user.email eval@example.com
git config user.name Eval
git config commit.gpgsign false
git config core.hooksPath /dev/null
mkdir -p src
cat > schema.sql <<'SQL'
PRAGMA foreign_keys = ON;
CREATE TABLE tenants (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE accounts (id INTEGER PRIMARY KEY, handle TEXT NOT NULL UNIQUE);
CREATE TABLE memberships (
  id INTEGER PRIMARY KEY, tenant_id INTEGER NOT NULL REFERENCES tenants(id),
  account_id INTEGER NOT NULL REFERENCES accounts(id), role TEXT NOT NULL,
  UNIQUE(tenant_id, account_id, role)
);
CREATE TABLE api_tokens (
  id INTEGER PRIMARY KEY, account_id INTEGER NOT NULL REFERENCES accounts(id),
  token_hash TEXT NOT NULL UNIQUE, revoked_at TEXT
);
CREATE TABLE shipments (
  id INTEGER PRIMARY KEY, tenant_id INTEGER NOT NULL REFERENCES tenants(id),
  author_id INTEGER NOT NULL REFERENCES accounts(id), destination TEXT NOT NULL
);
CREATE TABLE dispatch_runs (
  id INTEGER PRIMARY KEY, shipment_id INTEGER NOT NULL REFERENCES shipments(id),
  requested_by INTEGER NOT NULL REFERENCES accounts(id), state TEXT NOT NULL,
  attempt_count INTEGER NOT NULL DEFAULT 0, failure_reason TEXT
);
CREATE TABLE provider_attempts (
  id INTEGER PRIMARY KEY, run_id INTEGER NOT NULL REFERENCES dispatch_runs(id),
  sequence INTEGER NOT NULL, state TEXT NOT NULL, error TEXT,
  UNIQUE(run_id, sequence)
);
CREATE TABLE delivery_receipts (
  id INTEGER PRIMARY KEY, run_id INTEGER NOT NULL UNIQUE REFERENCES dispatch_runs(id),
  provider_reference TEXT NOT NULL, delivered_at TEXT NOT NULL
);
CREATE TABLE audit_events (
  id INTEGER PRIMARY KEY, run_id INTEGER NOT NULL REFERENCES dispatch_runs(id),
  actor_id INTEGER REFERENCES accounts(id), event TEXT NOT NULL, created_at TEXT NOT NULL
);
SQL
cat > src/platform.py <<'PY'
from queue import Queue


class Authorization:
    def __init__(self, database):
        self.database = database

    def require_dispatcher(self, account_id, tenant_id):
        row = self.database.execute(
            "SELECT 1 FROM memberships WHERE account_id=? AND tenant_id=? AND role='dispatcher'",
            (account_id, tenant_id),
        ).fetchone()
        if row is None:
            raise PermissionError("The account has no dispatcher role.")


class Api:
    def __init__(self, database, authorization, jobs):
        self.database, self.authorization, self.jobs = database, authorization, jobs

    def submit(self, account_id, shipment_id):
        shipment = self.database.execute("SELECT tenant_id, destination FROM shipments WHERE id=?", (shipment_id,)).fetchone()
        self.authorization.require_dispatcher(account_id, shipment[0])
        if not shipment[1]:
            raise ValueError("The shipment needs a destination.")
        cursor = self.database.execute(
            "INSERT INTO dispatch_runs(shipment_id, requested_by, state) VALUES (?, ?, 'queued')",
            (shipment_id, account_id),
        )
        self.database.commit()
        self.jobs.put(cursor.lastrowid)
        return cursor.lastrowid

    def status(self, run_id):
        return self.database.execute("SELECT state, failure_reason FROM dispatch_runs WHERE id=?", (run_id,)).fetchone()

    def retry(self, account_id, run_id):
        run = self.database.execute(
            "SELECT r.state, r.failure_reason, s.tenant_id FROM dispatch_runs r JOIN shipments s ON r.shipment_id=s.id WHERE r.id=?",
            (run_id,),
        ).fetchone()
        self.authorization.require_dispatcher(account_id, run[2])
        if run[:2] != ('failed', 'timeout'):
            raise ValueError("Only a timeout permits a manual retry.")
        self.database.execute("UPDATE dispatch_runs SET state='queued', attempt_count=0 WHERE id=?", (run_id,))
        self.database.commit()
        self.jobs.put(run_id)


def web_submit(api, account, shipment):
    return api.submit(account, shipment)


def cli_submit(api, account, shipment):
    return api.submit(account, shipment)


def web_status(api, run):
    return api.status(run)


def cli_status(api, run):
    return api.status(run)


def audit(database, run, event):
    database.execute("INSERT INTO audit_events(run_id, actor_id, event, created_at) VALUES (?, NULL, ?, datetime('now'))", (run, event))


def dispatch(database, provider, jobs, notices, run, max_attempts=2):
    database.execute("UPDATE dispatch_runs SET state='running', attempt_count=attempt_count+1 WHERE id=?", (run,))
    count = database.execute("SELECT attempt_count FROM dispatch_runs WHERE id=?", (run,)).fetchone()[0]
    sequence = database.execute("SELECT COALESCE(MAX(sequence), 0)+1 FROM provider_attempts WHERE run_id=?", (run,)).fetchone()[0]
    attempt = database.execute("INSERT INTO provider_attempts(run_id, sequence, state) VALUES (?, ?, 'running')", (run, sequence)).lastrowid
    try:
        result = provider.send(run)
    except TimeoutError:
        database.execute("UPDATE provider_attempts SET state='failed', error='timeout' WHERE id=?", (attempt,))
        state = 'queued' if count < max_attempts else 'failed'
        database.execute("UPDATE dispatch_runs SET state=?, failure_reason='timeout' WHERE id=?", (state, run))
        audit(database, run, state)
        if state == 'queued':
            jobs.put(run)
    else:
        state = 'sent' if result['accepted'] else 'failed'
        reason = None if result['accepted'] else 'provider_rejected'
        database.execute("UPDATE provider_attempts SET state=? WHERE id=?", (state, attempt))
        database.execute("UPDATE dispatch_runs SET state=?, failure_reason=? WHERE id=?", (state, reason, run))
        if result['accepted']:
            database.execute("INSERT INTO delivery_receipts(run_id, provider_reference, delivered_at) VALUES (?, ?, datetime('now'))", (run, result['reference']))
            notices.put(run)
        audit(database, run, state)
    database.commit()


def scheduler_tick(database, provider, jobs, notices):
    if not jobs.empty():
        dispatch(database, provider, jobs, notices, jobs.get())


def notify(database, notices, mailer):
    if not notices.empty():
        run = notices.get()
        receipt = database.execute("SELECT provider_reference FROM delivery_receipts WHERE run_id=?", (run,)).fetchone()
        mailer.send(receipt[0])
        audit(database, run, 'notice_sent')
        database.commit()


jobs = Queue()
notices = Queue()
PY
cat > deployment.toml <<'TOML'
[owned]
components = ["Web", "CLI", "API", "Authorization", "SQLite", "Job queue", "Scheduler", "Worker", "Notice queue", "Notifier"]
[scheduler]
interval_seconds = 60
[provider]
name = "ParcelCarrier"
endpoint = "https://carrier.example/api"
[mailer]
name = "MailRelay"
endpoint = "https://mail.example/api"
[policy]
max_attempts = 2
manual_retry_reason = "timeout"
TOML
cat > README.md <<'MD'
# Dispatch Hub

This repository defines a logical dispatch platform for multiple tenants.
The interfaces model the architecture. They do not implement a production web server.
The database uses the schema in schema.sql.

A Dispatcher creates dispatch runs through Web or CLI.
Both clients use the same API and Authorization component.
Authorization checks the dispatcher membership for the shipment's tenant.
Web and CLI also return run status through the API.
An Auditor reads that status through Web.

The API stores queued runs in SQLite and puts their identifiers on the Job queue.
The Scheduler starts the Worker every 60 seconds.
The Worker takes a run from the Job queue and calls the external ParcelCarrier.
The Worker records each provider attempt and its outcome in SQLite.
An accepted response produces a delivery receipt and a Notice queue entry.
The Notifier reads the receipt and calls the external MailRelay.
The Notifier records a notice event in SQLite.

A timeout permits one automatic retry. A second timeout produces a failed run.
A provider rejection produces a failed run without an automatic retry.
A Dispatcher can manually retry only a failed timeout run.
The manual retry resets the automatic attempt count.
A bad destination or missing dispatcher role stops intake before a run enters the queue.
The lifecycle must keep intake errors separate from failures of a stored run.

Identity records include tenants, accounts, memberships, and API tokens.
Dispatch records include shipments and dispatch runs.
Evidence records include provider attempts, delivery receipts, and audit events.
An automated event has no actor_id. A dispatch run can have no receipt.
The queue objects are internal components. They are not independent deployment services.
MD
git add .
git commit -q -m "Add the dispatch platform fixture"
echo "$dir"

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

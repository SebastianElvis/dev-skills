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

#!/usr/bin/env bash
# Build a temporary repository with verified service flows.
# Print the repository path.
set -euo pipefail

dir="$(mktemp -d -t visualize-arch-eval-XXXXXX)"
cd "$dir"

git init -q -b main
git config user.email "eval@example.com"
git config user.name "Eval"
git config commit.gpgsign false
git config core.hooksPath /dev/null

mkdir -p src
cat >README.md <<'MD'
# Parcel Desk

An Operator submits parcel jobs through the command-line interface (CLI).
The CLI sends each job to the application programming interface (API) service.
The API service stores jobs in SQLite.
A Worker reads queued jobs and calls the external Carrier API.
A Scheduler starts the Worker every five minutes.
The schedule comes from config.toml.
A Viewer uses the Dashboard to request job status from the API service.
MD

cat >src/app.py <<'PY'
class Database:
    name = "SQLite"

    def insert(self, parcel):
        return {"id": 1, "parcel": parcel, "status": "queued"}

    def get(self, job_id):
        return {"id": job_id, "status": "queued"}

    def next_job(self):
        return self.get(1)

    def save_result(self, result):
        return result


class APIService:
    def __init__(self, database):
        self.database = database

    def create_job(self, parcel):
        return self.database.insert(parcel)

    def get_job(self, job_id):
        return self.database.get(job_id)


class CarrierClient:
    name = "Carrier API"

    def send(self, job):
        return {"id": job["id"], "status": "sent"}


def submit_from_cli(api, parcel):
    return api.create_job(parcel)


def get_dashboard_status(api, job_id):
    return api.get_job(job_id)


def run_worker(database, carrier):
    job = database.next_job()
    result = carrier.send(job)
    database.save_result(result)


def scheduled_run(worker):
    worker.run()
PY

cat >config.toml <<'TOML'
[scheduler]
interval_minutes = 5
TOML

git add .
git commit -q -m "add parcel service"
echo "$dir"

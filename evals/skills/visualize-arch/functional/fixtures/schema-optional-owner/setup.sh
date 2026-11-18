#!/usr/bin/env bash
# Create a temporary schema repository.
set -euo pipefail
dir="$(mktemp -d -t visualize-arch-eval-XXXXXX)"
cd "$dir"
git init -q -b main
git config user.email eval@example.com
git config user.name Eval
git config commit.gpgsign false
git config core.hooksPath /dev/null
cat > schema.sql <<'SQL'
CREATE TABLE projects (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE owners (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE jobs (
  id INTEGER PRIMARY KEY,
  project_id INTEGER NOT NULL REFERENCES projects(id),
  owner_id INTEGER REFERENCES owners(id),
  status TEXT NOT NULL
);
SQL
git add .
git commit -q -m "Add the job schema"
echo "$dir"

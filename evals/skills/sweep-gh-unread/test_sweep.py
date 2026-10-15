"""Deterministic tests for scripts/sweep.py against the synthetic inbox.

Run: python3 -m unittest discover -s evals/skills/sweep-gh-unread
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "fixture"))
from make_fixture import EXPECTED, build  # noqa: E402

SWEEP = HERE.parents[2] / "skills" / "sweep-gh-unread" / "scripts" / "sweep.py"


class SweepTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = build(Path(self.tmp.name))
        self.env = {**os.environ, "SWEEP_GH": str(self.dir / "bin" / "gh")}

    def tearDown(self):
        self.tmp.cleanup()

    def run_sweep(self, *args, check=True):
        return subprocess.run([sys.executable, str(SWEEP), *args], env=self.env, cwd=self.dir,
                              capture_output=True, text=True, check=check)

    def collect(self, *scopes):
        self.run_sweep("collect", *scopes, "--out", str(self.dir / "run"))
        return {t["ref"]: t for t in json.loads((self.dir / "run" / "threads.json").read_text())["threads"]}

    def calls(self):
        return (self.dir / "calls.log").read_text().splitlines()

    def test_each_thread_matches_its_rule(self):
        threads = self.collect()
        self.assertEqual(set(threads), set(EXPECTED))
        for ref, (kind, rule, action) in EXPECTED.items():
            with self.subTest(ref=ref):
                t = threads[ref]
                self.assertEqual((t["result"], t["rule"]), (kind, rule))
                if kind != "judge":
                    self.assertEqual(t["action"], action)

    def test_judge_rows_give_both_outcomes(self):
        threads = self.collect()
        self.assertEqual(threads["acme/web#205"]["if_answer"]["action"], "reply")
        self.assertEqual(threads["acme/web#205"]["otherwise"]["rule"], "O6")
        self.assertEqual(threads["acme/web#301"]["otherwise"]["rule"], "N4")

    def test_owner_scope_excludes_other_owners(self):
        threads = self.collect("acme")
        self.assertNotIn("globex/tool#7", threads)
        self.assertEqual(len(threads), len(EXPECTED) - 1)

    def test_repo_scope_uses_the_repo_endpoint(self):
        threads = self.collect("acme/web")
        self.assertTrue(all(ref.startswith("acme/web") for ref in threads))
        self.assertIn("GET repos/acme/web/notifications?page=1", self.calls())

    def test_collect_makes_no_delete_call(self):
        self.collect()
        self.assertFalse(any(c.startswith("DELETE") for c in self.calls()))

    def test_mark_deletes_only_the_given_rows(self):
        threads = self.collect()
        rows = [threads["acme/api#107"]["row"], threads["acme/web (Release)"]["row"]]
        self.run_sweep("mark", "--run", str(self.dir / "run"), "--rows", ",".join(map(str, rows)))
        deletes = [c for c in self.calls() if c.startswith("DELETE")]
        expected = {f"DELETE notifications/threads/{threads[r]['thread_id']}"
                    for r in ("acme/api#107", "acme/web (Release)")}
        self.assertEqual(set(deletes), expected)
        log = [json.loads(line) for line in (self.dir / "run" / "actions.log").read_text().splitlines()]
        self.assertEqual({e["status"] for e in log}, {"marked"})

    def test_mark_skips_a_changed_thread(self):
        threads = self.collect()
        thread = threads["acme/api#107"]
        responses = json.loads((self.dir / "responses.json").read_text())
        responses[f"GET notifications/threads/{thread['thread_id']}"]["updated_at"] = "2026-10-15T00:00:00Z"
        (self.dir / "responses.json").write_text(json.dumps(responses))
        out = self.run_sweep("mark", "--run", str(self.dir / "run"), "--rows", str(thread["row"]))
        self.assertEqual(json.loads(out.stdout)["changed"][0]["ref"], "acme/api#107")
        self.assertFalse(any(c.startswith("DELETE") for c in self.calls()))

    def test_mark_refuses_an_unknown_row(self):
        self.collect()
        out = self.run_sweep("mark", "--run", str(self.dir / "run"), "--rows", "1,999", check=False)
        self.assertNotEqual(out.returncode, 0)
        self.assertFalse(any(c.startswith("DELETE") for c in self.calls()))


if __name__ == "__main__":
    unittest.main()

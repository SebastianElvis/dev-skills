"""These tests verify reference delivery and dispatch fixture behavior."""

import importlib.util
import json
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
import run as harness


class ReferenceInputTest(unittest.TestCase):
    def test_generation_and_scoring_use_a_frozen_reference(self):
        from PIL import Image
        from types import SimpleNamespace
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            case, cache, reports = root / "case", root / "cache", root / "reports"
            for directory in [case, cache, reports]:
                directory.mkdir()
            fixture = Path(tempfile.mkdtemp(prefix="visualize-arch-eval-")).resolve()
            minimum = cache / "minimum.png"
            Image.new("RGB", (16, 16), "red").save(minimum)
            task = {"id": "case", "prompt": "Task", "review_feedback": "A reviewer requests visible branches.", "allow_writes": True,
                    "visual_references": [{"path": "minimum.png", "label": "Minimum"}],
                    "reference_width_mm": 85, "judges": ["reference-quality"],
                    "required_artifacts": [{"path": "diagram.png"}],
                    "judge_artifacts": {"reference-quality": ["diagram.png"]}}
            (case / "task.json").write_text(json.dumps(task))

            def generate(prompt, **kwargs):
                self.assertEqual((Image.open(kwargs["images"][0]).getpixel((0, 0)), task["review_feedback"] in prompt, kwargs["reviewers"]), ((255, 0, 0), True, True))
                Image.new("RGB", (16, 16), "blue").save(minimum)
                Image.new("RGB", (16, 16), "white").save(fixture / "diagram.png")
                return [{"type": "item.completed", "item": {"type": "agent_message", "text": "Done."}}], 0

            def grade(*args, **kwargs):
                self.assertEqual((Image.open(args[-1][0]).getpixel((0, 0)), kwargs["backend"], args[2]), ((255, 0, 0), "codex", "Task"))
                return {"score": 1, "unknown": False}

            with patch.object(harness, "EVALS", root), patch.object(harness.subprocess, "run", return_value=SimpleNamespace(stdout=str(fixture))), \
                    patch.object(harness, "codex_cli", side_effect=generate), patch.object(harness, "llm_judge", side_effect=grade):
                result = harness.run_functional_case(case, "visualize-arch", 1, reports, reference_dir=cache, judge_backend="glm")
            self.assertTrue(result["pass"])
            self.assertTrue((reports / "case-t1-artifacts/diagram.png").is_file())
            self.assertEqual(len(result["reference_sha256"]), 1)

    def test_candidate_and_reference_images_keep_their_roles(self):
        with tempfile.TemporaryDirectory() as td:
            candidate = Path(td) / "candidate.png"
            minimum = Path(td) / "minimum.png"
            candidate.write_bytes(b"candidate")
            minimum.write_bytes(b"reference")
            events = [{"type": "item.completed", "item": {"type": "agent_message", "text": '{"score":1,"reason":"The figure meets the minimum.","unknown":false}'}}]
            with patch.object(harness, "codex_cli", return_value=(events, 0)) as call:
                result = harness.llm_judge("visualize-arch", "reference-quality", "Task", "Output", "Facts",
                                           [candidate], visual_references=[minimum])
            self.assertEqual(result["score"], 1)
            self.assertEqual(call.call_args.kwargs["images"], [candidate.resolve(), minimum.resolve()])
            self.assertIn("first 1 images are candidate figures", call.call_args.args[0])

    def test_missing_minimum_cannot_pass(self):
        with patch.object(harness, "codex_cli") as call:
            result = harness.llm_judge("visualize-arch", "reference-quality", "Task", "Output", "Facts")
        self.assertTrue(result["unknown"])
        self.assertEqual(result["score"], 0)
        call.assert_not_called()

    def test_reference_path_cannot_leave_the_cache(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            case = root / "case"
            cache = root / "cache"
            case.mkdir()
            cache.mkdir()
            (root / "outside.png").write_bytes(b"outside")
            (case / "task.json").write_text(json.dumps({"id": "case", "prompt": "Task",
                "visual_references": [{"path": "../outside.png"}]}))
            with self.assertRaises(ValueError):
                harness.run_functional_case(case, "visualize-arch", 1, root, reference_dir=cache)


class DispatchFixtureTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = harness.validated_fixture_path(subprocess.run(
            ["bash", str(HERE / "fixture/setup.sh")], capture_output=True, text=True, check=True,
        ).stdout.strip(), "visualize-arch")
        spec = importlib.util.spec_from_file_location("dispatch_fixture", cls.root / "src/platform.py")
        cls.platform = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.platform)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.root)

    def setUp(self):
        self.db = sqlite3.connect(":memory:")
        self.db.executescript((self.root / "schema.sql").read_text())
        self.db.executescript("""
            INSERT INTO tenants VALUES (1, 'Tenant');
            INSERT INTO accounts VALUES (1, 'dispatcher');
            INSERT INTO accounts VALUES (2, 'auditor');
            INSERT INTO memberships VALUES (1, 1, 1, 'dispatcher');
            INSERT INTO shipments VALUES (1, 1, 1, 'Destination');
        """)
        self.jobs, self.notices = self.platform.Queue(), self.platform.Queue()
        self.api = self.platform.Api(self.db, self.platform.Authorization(self.db), self.jobs)

    def tearDown(self):
        self.db.close()

    def test_success_produces_a_receipt_and_asynchronous_notice(self):
        run = self.api.submit(1, 1)
        provider = Mock()
        provider.send.return_value = {"accepted": True, "reference": "parcel-1"}
        self.platform.scheduler_tick(self.db, provider, self.jobs, self.notices)
        self.assertEqual(self.api.status(run), ("sent", None))
        mailer = Mock()
        self.platform.notify(self.db, self.notices, mailer)
        mailer.send.assert_called_once_with("parcel-1")
        self.assertEqual(self.db.execute("SELECT event FROM audit_events ORDER BY id").fetchall(), [("sent",), ("notice_sent",)])

    def test_timeouts_stop_then_manual_retry_preserves_attempt_history(self):
        run = self.api.submit(1, 1)
        provider = Mock()
        provider.send.side_effect = [TimeoutError(), TimeoutError(), {"accepted": True, "reference": "parcel-2"}]
        for _ in range(2):
            self.platform.scheduler_tick(self.db, provider, self.jobs, self.notices)
        self.assertEqual(self.api.status(run), ("failed", "timeout"))
        self.assertTrue(self.jobs.empty())
        self.api.retry(1, run)
        self.platform.scheduler_tick(self.db, provider, self.jobs, self.notices)
        self.assertEqual(self.api.status(run), ("sent", None))
        self.assertEqual(self.db.execute("SELECT sequence FROM provider_attempts ORDER BY id").fetchall(), [(1,), (2,), (3,)])

    def test_rejection_permits_no_retry(self):
        run = self.api.submit(1, 1)
        provider = Mock()
        provider.send.return_value = {"accepted": False}
        self.platform.scheduler_tick(self.db, provider, self.jobs, self.notices)
        self.assertEqual(self.api.status(run), ("failed", "provider_rejected"))
        with self.assertRaises(ValueError):
            self.api.retry(1, run)
        self.assertTrue(self.jobs.empty())
        self.assertTrue(self.notices.empty())

    def test_intake_errors_create_no_run(self):
        with self.assertRaises(PermissionError):
            self.api.submit(2, 1)
        self.db.execute("UPDATE shipments SET destination='' WHERE id=1")
        with self.assertRaises(ValueError):
            self.api.submit(1, 1)
        self.assertEqual(self.db.execute("SELECT COUNT(*) FROM dispatch_runs").fetchone()[0], 0)


if __name__ == "__main__":
    unittest.main()

"""These tests verify the fresh import recovery workflow."""

import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys
import unittest
from unittest.mock import Mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
import run as harness


class RecoveryFixtureTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = harness.validated_fixture_path(subprocess.run(
            ["bash", str(HERE / "functional/fixtures/reference-recovery/setup.sh")],
            capture_output=True, text=True, check=True,
        ).stdout.strip(), "visualize-arch")
        spec = importlib.util.spec_from_file_location("recovery_fixture", cls.root / "src/imports.py")
        cls.module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = cls.module
        spec.loader.exec_module(cls.module)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.root)

    def setUp(self):
        self.importer = self.module.Importer()
        self.job = self.importer.submit({"items": [1], "safe": True}, 1)

    def test_credential_resume_preserves_identity_and_history(self):
        warehouse = Mock()
        warehouse.write.return_value = "credentials_error"
        self.importer.tick(self.job, warehouse, 0)
        history = self.job.events.copy()
        for version in [None, 1]:
            with self.assertRaises(ValueError):
                self.importer.resume(self.job, version)
        self.importer.resume(self.job, 2)
        self.assertEqual((self.job.id, self.job.cycle_attempts, self.job.ready_at), (1, 0, 0))
        self.assertEqual(self.job.events[:len(history)], history)
        self.assertGreater(self.job.event_sequence, history[-1][0])

    def test_backoff_limits_attempts_and_resume_needs_no_new_credentials(self):
        warehouse = Mock()
        warehouse.write.return_value = "throttled"
        for now in [0, 59, 60, 120]:
            self.importer.tick(self.job, warehouse, now)
        self.assertEqual(warehouse.write.call_count, 3)
        self.assertEqual((self.job.state, self.job.cycle_attempts), ("suspended", 3))
        self.importer.resume(self.job)
        self.assertEqual((self.job.state, self.job.cycle_attempts), ("queued", 0))

    def test_cancellation_and_quarantine_stop_warehouse_calls(self):
        warehouse = Mock()
        self.importer.cancel(self.job)
        self.importer.tick(self.job, warehouse, 0)
        unsafe = self.importer.submit({"items": [1], "safe": False}, 1)
        self.importer.tick(unsafe, warehouse, 0)
        self.assertEqual(unsafe.state, "quarantined")
        warehouse.write.assert_not_called()

    def test_index_failure_preserves_archive_and_permits_no_automatic_retry(self):
        warehouse, search = Mock(), Mock()
        warehouse.write.return_value = "accepted"
        search.index.return_value = False
        self.importer.tick(self.job, warehouse, 0)
        self.importer.index(self.job, search)
        self.assertEqual((self.job.state, self.job.index_state), ("archived", "index_failed"))
        with self.assertRaises(ValueError):
            self.importer.index(self.job, search)

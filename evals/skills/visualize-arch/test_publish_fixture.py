"""These tests verify the independent release fixture and its event history."""
import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys
import unittest
from unittest.mock import Mock


class PublishFixtureTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        setup=Path(__file__).parent/'functional/fixtures/reference-publish/setup.sh'
        cls.root=Path(subprocess.run(['bash',str(setup)],capture_output=True,text=True,check=True).stdout.strip())
        spec=importlib.util.spec_from_file_location('release_fixture',cls.root/'src/releases.py')
        cls.module=importlib.util.module_from_spec(spec)
        sys.modules[spec.name]=cls.module
        spec.loader.exec_module(cls.module)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.root)

    def setUp(self):
        self.desk=self.module.Desk()
        self.release=self.desk.create('package')
        self.runner=Mock()

    def test_approval_guards_create_no_extra_events(self):
        with self.assertRaises(ValueError):
            self.desk.create(' ')
        with self.assertRaises(PermissionError):
            self.desk.approve(self.release,'viewer')
        self.desk.run(self.release,self.runner)
        self.runner.build.assert_not_called()
        self.assertEqual(self.release.events,[(1,'created')])

    def test_retry_keeps_identity_and_event_sequence(self):
        self.desk.approve(self.release,'maintainer')
        self.runner.build.side_effect=['transient','transient','ready']
        for _ in range(2):
            self.desk.run(self.release,self.runner)
        self.assertEqual((self.release.state,self.release.attempts),('failed',2))
        with self.assertRaises(PermissionError):
            self.desk.retry(self.release,'viewer')
        self.desk.retry(self.release,'maintainer')
        self.desk.run(self.release,self.runner)
        self.assertEqual((self.release.id,self.release.state,self.release.attempts),(1,'built',1))
        self.assertEqual([name for _,name in self.release.events],['created','approved','build_started','retry_queued','build_started','retry_exhausted','manual_retry','build_started','build_ready'])
        self.assertEqual(self.release.event_sequence,9)

    def test_cancel_records_an_event_and_stops_the_worker(self):
        self.desk.cancel(self.release)
        self.desk.run(self.release,self.runner)
        self.runner.build.assert_not_called()
        self.assertEqual(self.release.events,[(1,'created'),(2,'cancelled')])

    def test_publication_failure_keeps_the_successful_build(self):
        self.desk.approve(self.release,'maintainer')
        self.runner.build.return_value='ready'
        self.desk.run(self.release,self.runner)
        registry=Mock()
        registry.push.return_value=False
        self.desk.publish(self.release,registry)
        self.assertEqual((self.release.state,self.release.publish_state),('built','publish_failed'))
        self.assertEqual(self.release.events[-1],(5,'publish_failed'))
        with self.assertRaises(ValueError):
            self.desk.publish(self.release,registry)
        registry.push.assert_called_once()


if __name__=='__main__':
    unittest.main()

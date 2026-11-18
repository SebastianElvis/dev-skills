"""Test final-size checks and rendered-artifact evaluation."""

import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "evals"))
import run as harness

spec = importlib.util.spec_from_file_location("check_figure", REPO / "skills/visualize-arch/scripts/check_figure.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


@unittest.skipUnless(all(shutil.which(c) for c in ["latexmk", "pdftohtml", "pdftoppm"]), "The test requires TeX and Poppler.")
class FigureTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def pdf(self, body):
        source = self.root / "figure.tex"
        source.write_text("\\documentclass{article}\n\\pagestyle{empty}\n\\begin{document}\n" + body + "\n\\end{document}\n")
        subprocess.run(["latexmk", "-pdf", "-halt-on-error", source.name], cwd=self.root,
                       stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)
        return source.with_suffix(".pdf")

    def test_text_passes_at_page_width_and_fails_after_reduction(self):
        pdf = self.pdf("Readable system label")
        full = checker.check(pdf, 216, 8)
        small = checker.check(pdf, 40, 8)
        self.assertTrue(full["text_size_pass"])
        self.assertFalse(small["text_size_pass"])
        self.assertTrue(Path(small["gray_preview"]).is_file())
        self.assertTrue(Path(small["color_preview"]).is_file())

    def test_multiple_pages_fail(self):
        with self.assertRaises(ValueError):
            checker.check(self.pdf("First page\\newpage Second page"), 85, 8)

    def test_empty_figure_fails(self):
        with self.assertRaises(ValueError):
            checker.check(self.pdf("\\mbox{}"), 85, 8)

    def test_invalid_dimensions_fail(self):
        pdf = self.pdf("Label")
        for width in [0, -1, float("nan"), float("inf")]:
            with self.subTest(width=width), self.assertRaises(ValueError):
                checker.check(pdf, width, 8)


class JudgeTest(unittest.TestCase):
    def test_provider_failure_is_not_a_quality_score(self):
        with tempfile.TemporaryDirectory() as td:
            events = [{"type": "result", "is_error": True, "api_error": "usage_limit_reached", "result": "The provider rejected the request."}]
            run_dir = Path(td)
            case_dir = REPO / "evals/skills/visualize-arch/functional/fixtures/create-service-diagram"
            with patch.object(harness, "EVALS", run_dir), patch.object(harness, "codex_cli", return_value=(events, 1)), patch.object(harness, "llm_judge") as judge:
                result = harness.run_functional_case(case_dir, "visualize-arch", 1, run_dir)
            self.assertTrue(result["error"])
            self.assertNotIn("judge", result)
            judge.assert_not_called()

    def test_blocked_suite_has_no_pass_rate(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            case = root / "skills/visualize-arch/functional/fixtures/case"
            case.mkdir(parents=True)
            failed = {"case_id": "case", "trial": 1, "pass": False, "error": "The provider rejected the request."}
            with patch.object(harness, "EVALS", root), patch.object(harness, "run_functional_case", return_value=failed):
                result = harness.run_functional("visualize-arch", 1, None)
            self.assertIsNone(result["summary"]["pass_rate"])
            self.assertEqual(result["summary"]["errors"], 1)

    def test_turn_limit_remains_a_candidate_failure(self):
        events = [{"type": "result", "is_error": True, "subtype": "error_max_turns", "result": "The agent reached the turn limit."}]
        self.assertEqual(harness.execution_error(events), "")

    def test_judge_receives_real_artifacts_with_read_only_access(self):
        with tempfile.TemporaryDirectory() as td:
            image = Path(td) / "preview.png"
            image.write_bytes(b"image fixture")

            def judge(prompt, **kwargs):
                self.assertEqual(kwargs["images"], [image.resolve()])
                self.assertFalse(kwargs.get("writable", False))
                self.assertFalse(kwargs["shell_access"])
                self.assertTrue(kwargs["schema"].is_file())
                self.assertIn("Inspect every attached image", prompt)
                return [{"type": "item.completed", "item": {"type": "agent_message", "text": json.dumps({"score": 1, "reason": "The figure is clear.", "unknown": False})}}], 0

            with patch.object(harness, "codex_cli", side_effect=judge):
                result = harness.llm_judge("visualize-arch", "readability", "Task", "Output", "Facts", [image])
            self.assertEqual(result["score"], 1)

    def test_missing_artifact_cannot_pass(self):
        with patch.object(harness, "codex_cli") as call:
            result = harness.llm_judge("visualize-arch", "readability", "Task", "Output", "Facts", [Path("/absent/figure.png")])
        self.assertEqual(result["score"], 0)
        self.assertTrue(result["unknown"])
        call.assert_not_called()

    def test_text_judge_uses_codex_without_write_access(self):
        events = [{"type": "item.completed", "item": {"type": "agent_message", "text": '{"score": 1, "reason": "The response lists the outputs.", "unknown": false}'}}]
        with patch.object(harness, "codex_cli", return_value=(events, 0)) as call:
            result = harness.llm_judge("visualize-arch", "handoff", "Task", "Output", "Facts")
        self.assertEqual(result["score"], 1)
        self.assertFalse(call.call_args.kwargs.get("writable", False))

    def test_invalid_scores_fail_closed(self):
        for score in [True, 2, "1"]:
            events = [{"type": "item.completed", "item": {"type": "agent_message", "text": json.dumps({"score": score, "reason": "Result", "unknown": False})}}]
            with self.subTest(score=score), patch.object(harness, "codex_cli", return_value=(events, 0)):
                result = harness.llm_judge("visualize-arch", "handoff", "Task", "Output", "Facts")
                self.assertEqual(result["score"], 0)
                self.assertTrue(result["unknown"])

    def test_codex_cli_attaches_images_and_disables_scorer_shell(self):
        from types import SimpleNamespace
        result = SimpleNamespace(stdout='{"type":"turn.completed","usage":{"input_tokens":10}}', stderr="", returncode=0)
        with tempfile.TemporaryDirectory() as td, patch.object(harness.subprocess, "run", return_value=result) as call:
            harness.codex_cli("Judge", cwd=Path(td), images=[Path(td) / "figure.png"], shell_access=False)
        command = call.call_args.args[0]
        self.assertIn("--image", command)
        self.assertIn("read-only", command)
        self.assertIn("shell_tool", command)
        self.assertEqual(call.call_args.kwargs["input"], "Judge")



if __name__ == "__main__":
    unittest.main()

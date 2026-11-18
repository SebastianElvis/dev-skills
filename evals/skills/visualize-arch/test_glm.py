"""These tests check the optional GLM scorer without network access."""
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import run as harness


class GlmTest(unittest.TestCase):
    def test_request_attaches_images_and_transcript_omits_the_key(self):
        data = {'choices': [{'message': {'content': '{"score":1,"reason":"The figure is clear.","unknown":false}'}}],
                'model': 'z-ai/glm-4.6v', 'usage': {'prompt_tokens': 10, 'completion_tokens': 20, 'cost': 0.01}}
        with tempfile.TemporaryDirectory() as td:
            image = Path(td) / 'figure.png'
            image.write_bytes(b'candidate')
            with patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test-secret'}), \
                    patch.object(harness.urllib.request, 'urlopen', return_value=io.BytesIO(json.dumps(data).encode())) as call:
                events, status = harness.glm_cli('Task', [image])
            request = call.call_args.args[0]
            body = json.loads(request.data)
            self.assertEqual(body['messages'][0]['content'][1]['image_url']['url'], 'data:image/png;base64,Y2FuZGlkYXRl')
            self.assertEqual(body['response_format']['type'], 'json_object')
            self.assertNotIn('tools', body)
            self.assertNotIn('test-secret', json.dumps(events))
            self.assertEqual(status, 0)
            self.assertEqual(harness.usage_summary(events)['cost_usd'], 0.01)

    def test_missing_key_returns_an_unavailable_result(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(harness.urllib.request, 'urlopen') as call:
            events, status = harness.glm_cli('Task', [])
        self.assertEqual(status, 1)
        self.assertIn('absent', harness.execution_error(events))
        call.assert_not_called()

    def test_provider_error_preserves_no_valid_score(self):
        with patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test-secret'}), \
                patch.object(harness.urllib.request, 'urlopen', side_effect=OSError('The service is unavailable.')):
            result = harness.llm_judge('visualize-arch', 'handoff', 'Task', 'Output', 'Facts', backend='glm')
        self.assertTrue(result['unknown'])
        self.assertTrue(result['error'])
        self.assertEqual(result['backend'], 'glm')

    def test_glm_scores_obey_the_same_local_validation(self):
        for score in [True, 2, '1']:
            events = [{'type': 'result', 'result': json.dumps({'score': score, 'reason': 'Result', 'unknown': False})}]
            with self.subTest(score=score), patch.object(harness, 'glm_cli', return_value=(events, 0)):
                result = harness.llm_judge('visualize-arch', 'handoff', 'Task', 'Output', 'Facts', backend='glm')
            self.assertEqual(result['score'], 0)
            self.assertTrue(result['unknown'])


if __name__ == '__main__':
    unittest.main()

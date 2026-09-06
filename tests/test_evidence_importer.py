"""Boundary checks for evidence integrity and provenance, using synthetic runs."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location('importer', Path(__file__).resolve().parents[1] / 'scripts/import-sweatbench.py')
IMPORTER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(IMPORTER)


class EvidenceImporterTest(unittest.TestCase):
    def test_no_reasoning_or_excluded_files_enter_bundle(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            run, out = root / 'run', root / 'evidence'
            for milestone in (2, 3):
                snapshot = run / 'snapshots' / f'milestone-{milestone}'
                (snapshot / 'lib').mkdir(parents=True)
                (snapshot / 'lib' / 'example.ex').write_text('old\n' if milestone == 2 else 'new\nextra\n')
                (snapshot / 'lib' / '.secret').write_text('excluded')
                (snapshot / 'priv').mkdir()
                (snapshot / 'priv' / 'development.db').write_text('excluded')
                (snapshot / 'deps').mkdir()
                (snapshot / 'deps' / 'dependency.ex').write_text('excluded')
            (run / 'logs').mkdir()
            log = run / 'logs' / 'agent-3.jsonl'
            log.write_text(json.dumps({'type': 'assistant', 'message': {'content': [{'type': 'thinking', 'thinking': 'PRIVATE REASONING'}, {'type': 'text', 'text': 'Explicit handoff.'}]}}) + '\n' + json.dumps({'type': 'result', 'result': 'not handoff'}) + '\n')
            IMPORTER.build(run, [3], out)
            bundle_text = (out / 'bundle.json').read_text()
            bundle = json.loads(bundle_text)
            self.assertNotIn('PRIVATE REASONING', bundle_text)
            self.assertNotIn('excluded', bundle_text)
            self.assertEqual(bundle['authorHandoffs']['3']['text'], 'Explicit handoff.')
            self.assertEqual(bundle['authorHandoffs']['3']['line'], 1)
            self.assertEqual(bundle['authorHandoffs']['3']['source'], 'logs/agent-3.jsonl')
            self.assertEqual(bundle['sourceRoot'], 'sweatbench-run:run')
            self.assertNotIn(str(root), bundle_text)
            change = bundle['comparisons']['3']['changed'][0]
            self.assertEqual((change['added'], change['removed']), (2, 1))
            self.assertNotEqual(bundle['milestones']['2']['fingerprint'], bundle['milestones']['3']['fingerprint'])
            self.assertEqual((run / 'snapshots/milestone-2/lib/example.ex').read_text(), 'old\n')

    def test_prevents_source_output_overlap(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaises(ValueError):
                IMPORTER.build(root, [3], root / 'generated')


if __name__ == '__main__':
    unittest.main()

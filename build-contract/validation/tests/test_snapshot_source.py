"""CLI regressions using disposable Git repositories, never product evidence."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / 'snapshot_source.py'


class SnapshotComparisonTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.source = self.root / 'source'
        self.source.mkdir()
        self.git('init', '-q')
        self.source_file = self.source / 'source.txt'
        self.source_file.write_text('original\n', encoding='utf-8')
        self.git('add', 'source.txt')
        self.git('-c', 'user.name=Snapshot fixture', '-c',
                 'user.email=snapshot@example.invalid', 'commit', '-qm', 'fixture')
        self.before = self.root / 'before.json'
        result = self.run_snapshot(self.before)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.baseline = self.before.read_bytes()

    def git(self, *args):
        return subprocess.run(['git', '-C', str(self.source), *args],
                              check=True, capture_output=True)

    def run_snapshot(self, output, compare=None):
        command = [sys.executable, str(SCRIPT), str(self.source), '--out', str(output)]
        if compare is not None:
            command += ['--compare', str(compare)]
        return subprocess.run(command, capture_output=True, text=True)

    def modify_source(self):
        self.source_file.write_text('modified\n', encoding='utf-8')

    def assert_rejected_without_overwriting(self, output):
        self.modify_source()
        result = self.run_snapshot(output, self.before)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn('comparison snapshot', result.stderr)
        self.assertEqual(self.before.read_bytes(), self.baseline)
        self.assertEqual(self.source_file.read_text(encoding='utf-8'), 'modified\n')

    def test_same_path_is_rejected_without_overwriting_reference(self):
        self.assert_rejected_without_overwriting(self.before)

    def test_normalized_alias_is_rejected_without_overwriting_reference(self):
        folder = self.root / 'nested'
        folder.mkdir()
        self.assert_rejected_without_overwriting(folder / '..' / self.before.name)

    def test_symlink_alias_is_rejected_without_overwriting_reference(self):
        alias = self.root / 'alias.json'
        try:
            alias.symlink_to(self.before)
        except OSError as error:
            self.skipTest(f'Symlinks unavailable: {error}')
        self.assert_rejected_without_overwriting(alias)

    def test_hardlink_alias_is_rejected_without_overwriting_reference(self):
        alias = self.root / 'alias.json'
        try:
            os.link(self.before, alias)
        except OSError as error:
            self.skipTest(f'Hard links unavailable: {error}')
        self.assert_rejected_without_overwriting(alias)

    def test_distinct_snapshot_reports_unchanged_source(self):
        result = self.run_snapshot(self.root / 'after.json', self.before)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertTrue(report['fullyVerified'])
        self.assertEqual(report['changedFiles'], [])
        self.assertEqual(self.before.read_bytes(), self.baseline)

    def test_distinct_snapshot_reports_changed_source(self):
        self.modify_source()
        result = self.run_snapshot(self.root / 'after.json', self.before)
        self.assertEqual(result.returncode, 1, result.stderr)
        report = json.loads(result.stdout)
        self.assertFalse(report['fullyVerified'])
        self.assertFalse(report['accessibleFilesUnchanged'])
        self.assertEqual(report['changedFiles'], ['source.txt'])
        self.assertEqual(self.before.read_bytes(), self.baseline)

    def test_output_inside_inspected_checkout_is_still_rejected(self):
        output = self.source / 'after.json'
        result = self.run_snapshot(output, self.before)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn('outside the inspected source checkout', result.stderr)
        self.assertFalse(output.exists())
        self.assertEqual(self.before.read_bytes(), self.baseline)

    def test_missing_comparison_does_not_overwrite_existing_output(self):
        output = self.root / 'after.json'
        output.write_text('existing output\n', encoding='utf-8')
        result = self.run_snapshot(output, self.root / 'missing.json')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(output.read_text(encoding='utf-8'), 'existing output\n')

    def test_invalid_comparison_does_not_overwrite_existing_output(self):
        output = self.root / 'after.json'
        output.write_text('existing output\n', encoding='utf-8')
        self.before.write_text('not JSON\n', encoding='utf-8')
        result = self.run_snapshot(output, self.before)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(output.read_text(encoding='utf-8'), 'existing output\n')
        self.assertEqual(self.before.read_text(encoding='utf-8'), 'not JSON\n')


if __name__ == '__main__':
    unittest.main()

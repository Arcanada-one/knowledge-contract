#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Adverse input controls for the retained Coordinated Work flow verifier.

Fixtures and retained reports are never rewritten. Subprocesses write only
inside a temporary directory, including for the unchanged positive replay.
"""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
PROBE = ROOT / 'roadmap/coordinated-work/probes'


class InputIdentityControls(unittest.TestCase):
    def run_verifier(self, mutate=None):
        names = ('cases.json', 'raw_results.json', 'expected_results.json')
        docs = {name: json.loads((PROBE / name).read_text()) for name in names}
        if mutate:
            mutate(docs)
        with tempfile.TemporaryDirectory(prefix='cw-probe-identity-') as tmp:
            dest = Path(tmp)
            for name, doc in docs.items():
                (dest / name).write_text(json.dumps(doc, ensure_ascii=False, indent=2) + '\n')
            # The input digest is deliberately matched so it cannot hide an
            # identity violation behind an unrelated checksum failure.
            docs['raw_results.json']['input_sha256'] = hashlib.sha256((dest / 'cases.json').read_bytes()).hexdigest()
            (dest / 'raw_results.json').write_text(json.dumps(docs['raw_results.json'], ensure_ascii=False, indent=2) + '\n')
            report = dest / 'report.json'
            command = [sys.executable]
            if sys.flags.optimize:
                command.append('-O')
            command += [str(PROBE / 'verify_flow_probe.py'), '--inputs', str(dest / 'cases.json'),
                        '--actual', str(dest / 'raw_results.json'), '--expected', str(dest / 'expected_results.json'),
                        '--report', str(report)]
            result = subprocess.run(command, text=True, capture_output=True, check=False)
            return result, json.loads(report.read_text()) if report.exists() else None

    def expect_rejection(self, mutate, message):
        result, report = self.run_verifier(mutate)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn(message, result.stderr)
        self.assertNotIn('"status": "PASS"', result.stdout)
        self.assertIsNone(report)

    def test_retained_valid_cases_still_pass_190_checks(self):
        result, report = self.run_verifier()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((report['status'], report['cases'], report['checks_count']), ('PASS', 10, 190))

    def test_duplicate_input_id_is_rejected(self):
        def mutate(docs):
            docs['cases.json']['cases'].append(copy.deepcopy(docs['cases.json']['cases'][0]))
        self.expect_rejection(mutate, 'cases has duplicate id')

    def test_duplicate_actual_case_id_is_rejected(self):
        def mutate(docs):
            docs['raw_results.json']['results'].append(copy.deepcopy(docs['raw_results.json']['results'][0]))
        self.expect_rejection(mutate, 'results has duplicate case_id')

    def test_duplicate_expected_case_id_is_rejected(self):
        def mutate(docs):
            docs['expected_results.json']['expected'].append(copy.deepcopy(docs['expected_results.json']['expected'][0]))
        self.expect_rejection(mutate, 'expected has duplicate case_id')

    def test_duplicate_conflicting_actual_cannot_be_overwritten(self):
        def mutate(docs):
            row = copy.deepcopy(docs['raw_results.json']['results'][0])
            row['totals']['shipped'] = -1
            docs['raw_results.json']['results'].insert(0, row)
        self.expect_rejection(mutate, 'results has duplicate case_id')

    def test_missing_expected_case_is_rejected(self):
        def mutate(docs):
            docs['expected_results.json']['expected'].pop()
        self.expect_rejection(mutate, 'case identities differ')

    def test_blank_identity_is_rejected(self):
        def mutate(docs):
            docs['cases.json']['cases'][0]['id'] = '  '
        self.expect_rejection(mutate, 'must be a nonempty string')


if __name__ == '__main__':
    unittest.main()

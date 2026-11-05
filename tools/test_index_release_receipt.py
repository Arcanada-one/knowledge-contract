# SPDX-FileCopyrightText: 2026 Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Bounded schema controls; these synthetic receipts do not observe an API or index."""
from pathlib import Path
import itertools
import json
import unittest

from jsonschema import Draft202012Validator

try:
    from .check_contract_profile import FORMAT_CHECKER
except ImportError:
    from check_contract_profile import FORMAT_CHECKER

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / 'appendices/api-integration/index-release-receipt.schema.json').read_text())
CHECKS = ('admitted_snapshot', 'index_snapshot', 'reported_revision', 'query_coverage', 'supersession', 'fetch_identity')


def fixture():
    return {
        'schema': 'KCIndexReleaseReceipt/v1',
        'repository_url': 'https://github.com/example/synthetic-receipt-test',
        'source_revision': 'a' * 40,
        'observed_at': '2026-11-04T12:00:00Z',
        'observer': 'synthetic-test',
        'evidence_refs': ['synthetic-test-only'],
        'publication_manifest_sha256': 'b' * 64,
        'index_build_id': 'synthetic-build',
        'index_manifest_sha256': 'c' * 64,
        'admitted_paths': [{'path': 'papers/example/PAPER.md', 'sha256': 'd' * 64, 'decision_ref': 'synthetic-decision'}],
        'queries': [{'id': 'synthetic-query', 'query': 'example', 'expected_paths': ['papers/example/PAPER.md'], 'results': []}],
        'fetches': [], 'superseded_records': [],
        'checks': dict.fromkeys(CHECKS, 'pass'), 'decision': 'pass',
        'scope': 'Synthetic schema exercise only, not an actual successful release receipt.',
        'limitations': ['Shape validation does not authenticate observations or join result identities.'],
    }


class IndexReceiptSchemaTests(unittest.TestCase):
    def setUp(self):
        # Explicitly assert dates: jsonschema's optional RFC 3339 checker is not
        # installed by the project's minimal dependency set. These controls use
        # the exchange profile's UTC-seconds subset, not every RFC 3339 form.
        self.validator = Draft202012Validator(SCHEMA, format_checker=FORMAT_CHECKER)

    def test_schema_and_synthetic_shape(self):
        Draft202012Validator.check_schema(SCHEMA)
        self.validator.validate(fixture())

    def test_all_2187_check_state_and_decision_combinations(self):
        count = 0
        for states in itertools.product(('pass', 'fail', 'unknown'), repeat=len(CHECKS)):
            expected = 'fail' if 'fail' in states else 'unknown' if 'unknown' in states else 'pass'
            for decision in ('pass', 'fail', 'unknown'):
                item = fixture()
                item['checks'] = dict(zip(CHECKS, states))
                item['decision'] = decision
                self.assertEqual(self.validator.is_valid(item), decision == expected, (states, decision))
                count += 1
        self.assertEqual(count, 2187)

    def test_each_required_check_cannot_be_omitted(self):
        for key in CHECKS:
            item = fixture()
            del item['checks'][key]
            self.assertFalse(self.validator.is_valid(item), key)

    def test_relative_path_boundaries(self):
        for path in ('../paper.md', 'papers/../paper.md', 'papers/./paper.md', '/paper.md', 'papers\\paper.md'):
            item = fixture()
            item['admitted_paths'][0]['path'] = path
            self.assertFalse(self.validator.is_valid(item), path)

    def test_bad_identity_date_and_unknown_fields_are_rejected(self):
        for field, value in [('source_revision', 'main'), ('publication_manifest_sha256', 'unknown'), ('observed_at', 'yesterday')]:
            item = fixture()
            item[field] = value
            self.assertFalse(self.validator.is_valid(item), field)
        item = fixture()
        item['checks']['optional_override'] = 'pass'
        self.assertFalse(self.validator.is_valid(item))
        item = fixture()
        item['undeclared_field'] = True
        self.assertFalse(self.validator.is_valid(item))


if __name__ == '__main__':
    unittest.main()

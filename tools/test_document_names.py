# SPDX-FileCopyrightText: 2026 Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Bounded controls for editorial transformation; not semantic or translation certification."""
import copy
import unittest
from tools.apply_document_names import validate_rows, rename_document, humanize


class NamingControls(unittest.TestCase):
    def setUp(self):
        self.rows = [['topic', 'Meaning Bridge', 'Мост смысла', 'Описание', '意义桥接', '范围说明']]

    def test_positive_names(self):
        validate_rows(self.rows, {'topic'})

    def test_missing_document(self):
        with self.assertRaises(ValueError):
            validate_rows([], {'topic'})

    def test_extra_document(self):
        with self.assertRaises(ValueError):
            validate_rows(self.rows * 2, {'topic'})

    def test_unknown_slug(self):
        with self.assertRaises(ValueError):
            validate_rows(self.rows, {'different'})

    def test_overlong_name(self):
        rows = copy.deepcopy(self.rows)
        rows[0][1] = 'Four Separate English Words'
        with self.assertRaises(ValueError):
            validate_rows(rows, {'topic'})

    def test_opaque_primary_name(self):
        rows = copy.deepcopy(self.rows)
        rows[0][1] = 'F01'
        with self.assertRaises(ValueError):
            validate_rows(rows, {'topic'})

    def test_duplicate_short_name(self):
        rows = copy.deepcopy(self.rows)
        second = copy.deepcopy(rows[0])
        second[0] = 'other'
        rows.append(second)
        with self.assertRaises(ValueError):
            validate_rows(rows, {'topic', 'other'})

    def test_header_only_and_negation_preserved(self):
        text = '---\ntitle: "Detailed Explanation"\nstatus: research-draft\n---\n\n# Detailed Explanation\n\nA MUST NOT become B. Value: 17.\\n\n## Proof\nNot every case is measured.\n'
        renamed = rename_document(text, 'Detailed Explanation', 'Clear Name')
        self.assertIn('status: research-draft', renamed)
        self.assertIn('A MUST NOT become B. Value: 17.', renamed)
        self.assertTrue(renamed.endswith('## Proof\nNot every case is measured.\n'))
        self.assertIn('id="detailed-explanation"', renamed)

    def test_mismatched_title_rejected(self):
        with self.assertRaises(ValueError):
            rename_document('---\ntitle: "Other"\n---\n\n# Wrong\n', 'Wrong', 'Clear Name')

    def test_duplicate_h1_rejected(self):
        with self.assertRaises(ValueError):
            rename_document('---\ntitle: "Same"\n---\n\n# Same\n\n# Same\n', 'Same', 'Clear Name')

    def test_compatibility_anchor_and_literal_code(self):
        text = '## RM-01\n\nSee RM-01.\n\n```json\n{"id":"RM-01"}\n```\n'
        renamed = humanize(text, {'RM-01': 'Claim Atlas'})
        self.assertIn('id="rm-01"', renamed)
        self.assertIn('## Claim Atlas', renamed)
        self.assertIn('{"id":"RM-01"}', renamed)


class ReadableTitleControls(unittest.TestCase):
    def test_existing_label_is_not_duplicated(self):
        from tools.apply_document_names import display_parts
        self.assertEqual(display_parts('Book Packages', 'Book Packages: Source Identity')[0], 'Book Packages: Source Identity')

    def test_repeated_lead_is_removed_but_scope_retained(self):
        from tools.apply_document_names import display_parts
        self.assertEqual(display_parts('Knowledge Revision', 'Knowledge Revision, Version Identity, and the Adoption of Norms')[0], 'Knowledge Revision: Version Identity and the Adoption of Norms')

    def test_russian_repeated_lead(self):
        from tools.apply_document_names import display_parts
        self.assertEqual(display_parts('Книжные пакеты', 'Книжные пакеты: Идентичность источника')[0], 'Книжные пакеты: Идентичность источника')

    def test_unchanged_full_title_does_not_duplicate_anchor(self):
        raw = '---\ntitle: "Book Packages: Source Identity"\n---\n\n# Book Packages: Source Identity\n\nBody unchanged.\n'
        result = rename_document(raw, 'Book Packages: Source Identity', 'Book Packages')
        self.assertNotIn('<a id=', result)
        self.assertTrue(result.endswith('Body unchanged.\n'))


if __name__ == '__main__':
    unittest.main()

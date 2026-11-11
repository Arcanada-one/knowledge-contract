# SPDX-License-Identifier: Apache-2.0
"""Synthetic positive and adversarial checks; no GitHub/network or release writes."""
import json
import unittest
from tools.prepare_reviewed_publication import (adapt_target, document, git_blob,
                                              load_json, safe_path, text_bytes,
                                              unchanged_source_body)

OLD = (b'---\nname: "sample"\ntitle: "Original Scope"\nartifact: "scientific-paper"\n'
       b'edition: "1.1"\nlanguage: "en"\n---\n\n# Original Scope\n\n'
       b'## Claim\n\nAll outputs must satisfy P.\n')
CURRENT = (b'---\nname: "sample"\ntitle: "Clear Name: Original Scope"\n'
           b'short_title: "Clear Name"\nsubtitle: "Original Scope"\n'
           b'previous_title: "Original Scope"\nartifact: "scientific-paper"\n'
           b'edition: "1.1"\nlanguage: "en"\n---\n\n'
           b'<!-- markdownlint-disable-next-line MD033 -->\n'
           b'<a id="original-scope"></a>\n\n# Clear Name: Original Scope\n\n'
           b'## Claim\n\nAll outputs must satisfy P.\n')
COMMIT = '1' * 40
BLOB = '2' * 40
NAME = ['sample', 'Clear Name', 'Ясное имя', 'Исходная область', '清晰名称', '原始范围']

def target(language='ru'):
    return ('---\nname: "sample"\ntitle: "Старое имя"\nlanguage: "'+language+'"\n'
            'source_commit: "'+COMMIT+'"\nsource_git_blob: "'+BLOB+'"\n'
            'translation_status: "author-draft"\n---\n\n'
            '# Старое имя {#original-scope}\n\n## Утверждение {#claim}\n\n'
            'Все выходы обязаны удовлетворять P. [Источник](old.md#fixed)\n').encode()

class SourceMapping(unittest.TestCase):
    def test_title_only_positive(self):
        self.assertTrue(unchanged_source_body(OLD, CURRENT)['scientific_body_unchanged'])
    def test_identical_source_positive(self):
        self.assertTrue(unchanged_source_body(OLD, OLD)['scientific_body_unchanged'])
    def test_changed_negation_refused(self):
        with self.assertRaises(ValueError):
            unchanged_source_body(OLD, CURRENT.replace(b'All outputs', b'Not all outputs'))
    def test_changed_non_title_metadata_refused(self):
        with self.assertRaises(ValueError):
            unchanged_source_body(OLD, CURRENT.replace(b'edition: "1.1"', b'edition: "1.2"'))
    def test_injected_prefix_refused(self):
        with self.assertRaises(ValueError):
            unchanged_source_body(OLD, CURRENT.replace(b'# Clear Name:', b'Unreviewed premise.\n\n# Clear Name:'))
    def test_wrong_previous_title_refused(self):
        with self.assertRaises(ValueError):
            unchanged_source_body(OLD, CURRENT.replace(b'previous_title: "Original Scope"', b'previous_title: "Different"'))
    def test_duplicate_metadata_refused(self):
        with self.assertRaises(ValueError):
            unchanged_source_body(OLD, CURRENT.replace(b'name: "sample"', b'name: "sample"\nname: "sample"'))
    def test_h1_disagreement_refused(self):
        with self.assertRaises(ValueError):
            unchanged_source_body(OLD, CURRENT.replace(b'# Clear Name: Original Scope', b'# Different'))

class TargetMapping(unittest.TestCase):
    def test_body_links_and_anchor_unchanged(self):
        before=target()
        after=adapt_target(before, NAME, 'ru', COMMIT, BLOB, '3'*40, '4'*40)
        self.assertEqual(document(text_bytes(before))[4], document(text_bytes(after))[4])
        self.assertIn(b'{#original-scope}', after)
        self.assertIn(b'translation_status: "author-draft"', after)
        self.assertIn(git_blob(before).encode(), after)
        self.assertIn('Ясное имя: Исходная область'.encode(), after)
    def test_chinese_separator(self):
        after=adapt_target(target('zh-Hans'), NAME, 'zh-Hans', COMMIT, BLOB, '3'*40, '4'*40)
        self.assertIn('清晰名称：原始范围'.encode(), after)
    def test_wrong_source_refused(self):
        with self.assertRaises(ValueError):
            adapt_target(target(), NAME, 'ru', '0'*40, BLOB, '3'*40, '4'*40)
    def test_wrong_language_refused(self):
        with self.assertRaises(ValueError):
            adapt_target(target(), NAME, 'zh-Hans', COMMIT, BLOB, '3'*40, '4'*40)
    def test_no_anchor_refused(self):
        with self.assertRaises(ValueError):
            adapt_target(target().replace(b' {#original-scope}', b''), NAME, 'ru', COMMIT, BLOB, '3'*40, '4'*40)
    def test_accepted_status_not_overwritten(self):
        with self.assertRaises(ValueError):
            adapt_target(target().replace(b'author-draft', b'reviewed'), NAME, 'ru', COMMIT, BLOB, '3'*40, '4'*40)

class InputControls(unittest.TestCase):
    def test_path_escape_refused(self):
        for path in ('../outside', '/absolute', 'path\\escape', 'head:file'):
            with self.subTest(path=path), self.assertRaises(ValueError): safe_path(path)
    def test_duplicate_json_refused(self):
        with self.assertRaises(ValueError): load_json(b'{"key":1,"key":2}')
    def test_invalid_encoding_and_line_endings_refused(self):
        for data in (b'\xff\n', b'line\r\n', b'no final newline'):
            with self.subTest(data=data), self.assertRaises((ValueError, UnicodeError)): text_bytes(data)
    def test_blob_identity(self):
        self.assertEqual(git_blob(b''), 'e69de29bb2d1d6434b8b29ae775ad8c2e48c5391')

if __name__ == '__main__': unittest.main()

# SPDX-License-Identifier: Apache-2.0
"""Exact-source pin checks for the two existing Context Package draft translations.

These are structural/edit integrity checks, not independent semantic reviews.
"""
import hashlib
import json
import posixpath
import re
import unittest
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'engineering/specifications/context-package/SPECIFICATION.md'
COMMIT = '161a01afb1b756adf059ea2e1cbdd0dca29d83a2'
BLOB = '30ca8d2e5b5dd0e38b30cdb46919f514771a01da'
LANGS = {
    'ru': 'Пакет контекста: Покрытие, зависимости и доставка',
    'zh-Hans': '语境包：覆盖、依赖与交付',
}
NEW_ANCHOR = 'context-package-coverage-dependencies-and-delivery'
OLD_ANCHOR = 'context-packages-coverage-dependencies-and-delivery'

def git_blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

def requirement_ids(text: str):
    return re.findall(r'\*\*(CTX-R\d{3})\.\*\*', text)

def document_links(text: str, document_path: str):
    """Resolve this specification's eight plain Markdown document links.

    Bounded source-integrity check, not a general Markdown parser or K8 admission.
    The actual K8 compiler remains responsible for AST/section/link verification.
    """
    found = re.findall(r'(?<!!)\[[^\]]+\]\(([^)\s]+)\)', text)
    result = []
    for target in found:
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or not parsed.path:
            raise ValueError('unexpected link form in Context Package specification')
        path = posixpath.normpath(posixpath.join(posixpath.dirname(document_path), parsed.path))
        if path == '..' or path.startswith('../'):
            raise ValueError('link escapes the source repository')
        result.append((path, parsed.query, parsed.fragment))
    return result

def canonical_links_match(source: str, target: str, language: str) -> bool:
    source_path = 'engineering/specifications/context-package/SPECIFICATION.md'
    target_path = f'translations/{language}/{source_path}'
    expected = document_links(source, source_path)
    actual = document_links(target, target_path)
    return len(expected) == 8 and actual == expected

def translation_state(text: str, language: str) -> bool:
    front = text.split('---', 2)[1]
    return all(field in front for field in (
        f'language: "{language}"',
        'translation_status: "author-draft"',
        f'source_commit: "{COMMIT}"',
        f'source_git_blob: "{BLOB}"',
        'translation_of: "engineering/specifications/context-package/SPECIFICATION.md"'
    ))

class ContextPackagePinTests(unittest.TestCase):
    def test_exact_published_source_blob(self):
        self.assertEqual(git_blob(SOURCE.read_bytes()), BLOB)

    def test_source_exact_twenty_requirements(self):
        self.assertEqual(requirement_ids(SOURCE.read_text(encoding='utf-8')),
                         [f'CTX-R{i:03}' for i in range(1,21)])

    def test_drafts_repin_and_remain_unreviewed(self):
        for lang in LANGS:
            with self.subTest(lang=lang):
                p = ROOT / 'translations' / lang / 'engineering/specifications/context-package/SPECIFICATION.md'
                self.assertTrue(translation_state(p.read_text(encoding='utf-8'), lang))

    def test_both_historic_and_current_title_anchors(self):
        for lang,title in LANGS.items():
            with self.subTest(lang=lang):
                p = ROOT / 'translations' / lang / 'engineering/specifications/context-package/SPECIFICATION.md'
                t = p.read_text(encoding='utf-8')
                self.assertIn(f'<a id="{OLD_ANCHOR}"></a>', t)
                self.assertIn(f'# {title} {{#{NEW_ANCHOR}}}', t)

    def test_twenty_requirement_identity_pairs(self):
        expected = requirement_ids(SOURCE.read_text(encoding='utf-8'))
        for lang in LANGS:
            with self.subTest(lang=lang):
                p = ROOT / 'translations' / lang / 'engineering/specifications/context-package/SPECIFICATION.md'
                self.assertEqual(requirement_ids(p.read_text(encoding='utf-8')), expected)

    def test_negative_source_and_status_controls(self):
        p = ROOT / 'translations/ru/engineering/specifications/context-package/SPECIFICATION.md'
        t = p.read_text(encoding='utf-8')
        self.assertFalse(translation_state(t.replace(COMMIT,'unknown'), 'ru'))
        self.assertFalse(translation_state(t.replace('author-draft','reviewed'), 'ru'))
        self.assertFalse(translation_state(t.replace(BLOB,'0'*40), 'ru'))

    def test_all_eight_links_keep_canonical_document_and_anchor_identity(self):
        source = SOURCE.read_text(encoding='utf-8')
        for language in LANGS:
            with self.subTest(language=language):
                target = ROOT / 'translations' / language / 'engineering/specifications/context-package/SPECIFICATION.md'
                self.assertTrue(canonical_links_match(source, target.read_text(encoding='utf-8'), language))

    def test_locale_draft_link_regression_and_wrong_anchor_are_detected(self):
        source = SOURCE.read_text(encoding='utf-8')
        for language in LANGS:
            target = ROOT / 'translations' / language / 'engineering/specifications/context-package/SPECIFICATION.md'
            text = target.read_text(encoding='utf-8')
            canonical = '../../../../../engineering/specifications/status-model/SPECIFICATION.md#8-bounded-exchange-profile'
            self.assertEqual(text.count(canonical), 1)
            locale_draft = text.replace(canonical, '../status-model/SPECIFICATION.md#8-bounded-exchange-profile')
            self.assertFalse(canonical_links_match(source, locale_draft, language))
            wrong_anchor = text.replace(canonical, canonical + '-not-the-source-anchor')
            self.assertFalse(canonical_links_match(source, wrong_anchor, language))

    def test_titles_and_h1_match_current_localized_name_register(self):
        register = json.loads((ROOT / 'reference/document-naming/names.json').read_text(encoding='utf-8'))
        rows = [row for row in register['documents'] if row[0] == 'context-package']
        self.assertEqual(len(rows), 1)
        row = rows[0]
        expected = {'ru': f'{row[2]}: {row[3]}', 'zh-Hans': f'{row[4]}：{row[5]}'}
        self.assertEqual(LANGS, expected)
        for language, title in expected.items():
            target = ROOT / 'translations' / language / 'engineering/specifications/context-package/SPECIFICATION.md'
            text = target.read_text(encoding='utf-8')
            front = text.split('---', 2)[1]
            self.assertIn(f'title: "{title}"', front)
            self.assertIn(f'# {title} {{#{NEW_ANCHOR}}}', text)

if __name__ == '__main__':
    unittest.main(verbosity=2)


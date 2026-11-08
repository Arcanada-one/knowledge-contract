#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""One-time, exact-input refinement of the author-owned editorial proposal. No network."""
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PREVIOUS = 'd10ba0500be8c0ad2f031445df9c539b5e41fe54'
PATH = 'tools/apply_document_names.py'
source = subprocess.check_output(['git', 'show', PREVIOUS + ':' + PATH], cwd=ROOT).decode('utf-8')
if (ROOT / PATH).read_bytes() != source.encode('utf-8'):
    raise SystemExit('Refinement input changed; refusing overwrite')


def replace(old, new):
    global source
    if source.count(old) != 1:
        raise SystemExit('Expected exactly one refinement match: ' + old[:80])
    source = source.replace(old, new, 1)


replace("return subprocess.check_output(['git', *args], cwd=ROOT, text=True, encoding='utf-8')", "return subprocess.check_output(['git', *args], cwd=ROOT).decode('utf-8', errors='strict')")
insert = '''def display_parts(short: str, explanation: str) -> tuple[str, str]:
    """Keep explanatory scope, without repeating an already existing short label."""
    subtitle = explanation
    allowed = {short.casefold()}
    extra = {'Contract Core': 'Knowledge Contract', 'Context Package': 'Context Packages',
             'Contract Checks': 'Contract profiles', 'Ядро контракта': 'Контракт знаний',
             'Пакет контекста': 'Пакеты контекста',
             'Политика повторного использования': 'Повторное использование'}
    if short in extra:
        allowed.add(extra[short].casefold())
    prefix, separator, remainder = explanation.partition(': ')
    if separator and prefix.casefold() in allowed:
        subtitle = remainder
    else:
        for join in (', ', ' and ', ' и '):
            leading = short + join
            if explanation.casefold().startswith(leading.casefold()):
                subtitle = explanation[len(leading):]
                break
    if not subtitle.strip():
        raise ValueError('An explanatory subtitle is required')
    subtitle = subtitle[0].upper() + subtitle[1:]
    return short + ': ' + subtitle, subtitle


'''
replace('def anchor(title: str) -> str:', insert + 'def anchor(title: str) -> str:')
replace("    full = short + ': ' + old", "    full, subtitle = display_parts(short, old)\n    header_alias = '' if full == old else alias(anchor(old))")
replace("+ '\\nsubtitle: ' + json.dumps(old, ensure_ascii=False)", "+ '\\nsubtitle: ' + json.dumps(subtitle, ensure_ascii=False) + '\\nprevious_title: ' + json.dumps(old, ensure_ascii=False)")
replace("result = result.replace('\\n' + old_h1 + '\\n', '\\n' + alias(anchor(old)) + '# ' + full + '\\n', 1)", "result = result.replace('\\n' + old_h1 + '\\n', '\\n' + header_alias + '# ' + full + '\\n', 1)")
replace(".replace('\\n' + alias(anchor(old)) + '# ' + full + '\\n', '\\n' + old_h1 + '\\n', 1)", ".replace('\\n' + header_alias + '# ' + full + '\\n', '\\n' + old_h1 + '\\n', 1)")
replace("        full = row[1] + ': ' + old", "        full, subtitle = display_parts(row[1], old)")
replace("doc.update(title=full, short_title=row[1], subtitle=old)", "doc.update(title=full, short_title=row[1], subtitle=subtitle, previous_title=old)")
replace("'| Document | English title | Русское название | 简体中文标题 |',\n             '| --- | --- | --- | --- |'", "'| Document | English title | Русское название | 简体中文标题 | Previous English title |',\n             '| --- | --- | --- | --- | --- |'")
replace("+ row[2] + ': ' + row[3] + ' | ' + row[4] + '：' + row[5] + ' |')", "+ display_parts(row[2], row[3])[0] + ' | ' + row[4] + '：' + row[5] + ' | ' + old + ' |')")
replace("    labels.update({row[0].replace('RM-', 'RM'): row[1] for row in tasks})", "    labels.update({row[0].replace('RM-', 'RM'): row[1] for row in tasks})\n    labels.update({'P0': 'Immediate', 'P1': 'Next', 'P2': 'Expansion'})")
replace("if before not in (original(path), text):", "if before not in (original(path), git('show', '" + PREVIOUS + ":' + path), text):")
(ROOT / PATH).write_text(source, encoding='utf-8', newline='\n')

canon = ROOT / 'reference/document-naming/NAMING.md'
text = canon.read_text(encoding='utf-8')
needle = 'The first colon is the separator; an inherited subtitle can contain its own colon.'
if text.count(needle) != 1:
    raise SystemExit('Naming canon changed')
text = text.replace(needle, 'The first colon is the separator. When the previous title already begins with the same short label, do not repeat that label: for example, keep “Book Packages: Source Identity, Semantic Layers, and Validation”, not “Book Packages: Book Packages: …”. The explanatory wording is retained after removing that duplicated lead; the exact old title is stored separately. An inherited explanatory clause can contain its own colon.')
canon.write_text(text, encoding='utf-8', newline='\n')

ci = ROOT / '.github/workflows/ci.yml'
old_ci = subprocess.check_output(['git', 'show', PREVIOUS + ':.github/workflows/ci.yml'], cwd=ROOT).decode('utf-8')
if ci.read_text(encoding='utf-8') != old_ci:
    raise SystemExit('Ordinary CI changed; refusing overwrite')
needle = '      - name: Every publication and evidence file declares its sources\n        run: python3 -B tools/check_sources.py .\n'
addition = '      - name: Reader-facing names and bounded migration controls\n        run: |\n          python3 -B tools/check_document_names.py .\n          python3 -B -m unittest tools.test_document_names -v\n'
if old_ci.count(needle) != 1:
    raise SystemExit('CI insertion point is not unique')
ci.write_text(old_ci.replace(needle, needle + addition), encoding='utf-8', newline='\n')

tests = ROOT / 'tools/test_document_names.py'
text = tests.read_text(encoding='utf-8')
needle = "\n\nif __name__ == '__main__':"
extra_tests = '''

class ReadableTitleControls(unittest.TestCase):
    def test_existing_label_is_not_duplicated(self):
        from tools.apply_document_names import display_parts
        self.assertEqual(display_parts('Book Packages', 'Book Packages: Source Identity')[0], 'Book Packages: Source Identity')

    def test_repeated_lead_is_removed_but_scope_retained(self):
        from tools.apply_document_names import display_parts
        self.assertEqual(display_parts('Knowledge Revision', 'Knowledge Revision, Version Identity, and the Adoption of Norms')[0], 'Knowledge Revision: Version Identity, and the Adoption of Norms')

    def test_russian_repeated_lead(self):
        from tools.apply_document_names import display_parts
        self.assertEqual(display_parts('Книжные пакеты', 'Книжные пакеты: Идентичность источника')[0], 'Книжные пакеты: Идентичность источника')

    def test_unchanged_full_title_does_not_duplicate_anchor(self):
        raw = '---\\ntitle: "Book Packages: Source Identity"\\n---\\n\\n# Book Packages: Source Identity\\n\\nBody unchanged.\\n'
        result = rename_document(raw, 'Book Packages: Source Identity', 'Book Packages')
        self.assertNotIn('<a id=', result)
        self.assertTrue(result.endswith('Body unchanged.\\n'))
'''
if text.count(needle) != 1:
    raise SystemExit('Test insertion point changed')
tests.write_text(text.replace(needle, extra_tests + needle), encoding='utf-8', newline='\n')
print('Exact-input naming refinement applied; tests have not yet been run by this script.')

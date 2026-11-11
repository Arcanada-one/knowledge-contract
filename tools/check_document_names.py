#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Read-only naming-canon check. Does not freeze scientific bodies at the migration baseline."""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path


def check_reading_guide(docs: list[dict], rows: list[list[str]], guide: str) -> list[str]:
    """Validate displayed EN/RU/zh-Hans names against the source register, read-only."""
    from tools.apply_document_names import display_parts

    lines = [line for line in guide.splitlines() if line.startswith('| [')]
    names = {row[0]: row for row in rows}
    errors: list[str] = []
    for doc in docs:
        row = names[doc['slug']]
        prefix = f"| [{doc['type']}]({doc['path']}) | "
        candidates = [line for line in lines if line.startswith(prefix)]
        if len(candidates) != 1:
            errors.append('missing or duplicate DOCUMENTS row: ' + doc['slug'])
            continue
        fields = candidates[0].split(' | ')
        expected_ru = display_parts(row[2], row[3])[0]
        expected_zh = row[4] + '：' + row[5]
        if (len(fields) != 5 or fields[1] != doc['title']
                or fields[2] != expected_ru or fields[3] != expected_zh):
            errors.append('DOCUMENTS title/register mismatch: ' + doc['slug'])
    if len(lines) != len(docs):
        errors.append('DOCUMENTS row count mismatch')
    return errors


def check(root: Path) -> list[str]:
    errors = []
    try:
        catalog = json.loads((root / 'publication-catalog.json').read_text(encoding='utf-8'))
        register = json.loads((root / 'reference/document-naming/names.json').read_text(encoding='utf-8'))
        docs = catalog['documents']
        rows = register['documents']
        from tools.apply_document_names import validate_rows
        validate_rows(rows, {d['slug'] for d in docs})
        errors.extend(check_reading_guide(docs, rows, (root / 'DOCUMENTS.md').read_text(encoding='utf-8')))
        names = {row[0]: row[1] for row in rows}
        for doc in docs:
            path = root / doc['path']
            if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
                errors.append('unsafe canonical path: ' + doc['path'])
                continue
            title, short, subtitle = (doc.get(k) for k in ('title', 'short_title', 'subtitle'))
            if not isinstance(subtitle, str) or not subtitle.strip() or short != names[doc['slug']] or title != short + ': ' + subtitle:
                errors.append('inconsistent catalogue name: ' + doc['slug'])
                continue
            text = path.read_text(encoding='utf-8')
            if not text.startswith('---\n') or '\n---\n' not in text[4:]:
                errors.append('missing front matter: ' + doc['path'])
                continue
            front = text.split('\n---\n', 1)[0]
            for key, expected in [('title', title), ('short_title', short), ('subtitle', subtitle)]:
                matches = re.findall(r'^' + key + r': (.+)$', front, re.M)
                if len(matches) != 1 or json.loads(matches[0]) != expected:
                    errors.append('metadata mismatch ' + key + ': ' + doc['path'])
            if re.findall(r'^# (.+)$', text, re.M) != [title]:
                errors.append('H1 mismatch: ' + doc['path'])
        deps = json.loads((root / 'roadmap/dependencies.json').read_text(encoding='utf-8'))
        work = json.loads((root / 'roadmap/workstreams.json').read_text(encoding='utf-8'))['workstreams']
        if {n['id'] for n in deps['nodes']} != {r[0] for r in work}:
            errors.append('roadmap name/identity coverage mismatch')
        for node in deps['nodes']:
            row = next((r for r in work if r[0] == node['id']), None)
            if row and (node.get('display_name') != row[1] or node.get('display_name_ru') != row[2]):
                errors.append('roadmap display mismatch: ' + node['id'])
        tasks = (root / 'roadmap/TASKS.md').read_text(encoding='utf-8')
        if re.search(r'^#{1,3}\s+(?:RM-?\d+|F\d+)(?:\s|$)', tasks, re.M):
            errors.append('opaque primary roadmap heading')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(str(exc))
    return errors


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    errors = check(root)
    for error in errors:
        print('DOCUMENT_NAMING_FAIL ' + error)
    if not errors:
        print('DOCUMENT_NAMING_PASS: names, catalogue, front matter, H1 and readable roadmap identity')
    return int(bool(errors))


if __name__ == '__main__':
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    raise SystemExit(main())

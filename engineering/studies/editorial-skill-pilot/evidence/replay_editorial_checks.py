#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Recheck exact pilot texts against the predeclared literal and structure registry.

This is not an automated semantic review or a repeated agent experiment.
"""
from collections import Counter
from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    registry = json.loads((HERE / 'protected-claims.json').read_text())
    original_result = json.loads((HERE / 'editorial-comparison-results.json').read_text())
    source = (HERE / 'source-section.txt').read_bytes()
    source_text = source.decode()
    source_ok = sha(source) == registry['section']['sha256']
    rows = {}
    for name, filename in [('baseline', 'baseline-edit.txt'),
                           ('with-skills', 'skill-assisted-edit.txt')]:
        raw = (HERE / filename).read_bytes()
        text = raw.decode()
        checks = {
            'first_response_hash_matches': sha(raw) == original_result['variants'][name]['sha256'],
            'all_protected_literals_present': all(item in text for item in registry['protected_literals']),
            'all_protected_headings_preserved': all(item in text for item in registry['protected_headings']),
            'anchor_order_preserved': re.findall(r'<a id="([^"]+)"></a>', text) == registry['protected_anchors'],
            'link_destinations_preserved': Counter(re.findall(r'\]\(([^)]+)\)', text)) == Counter(re.findall(r'\]\(([^)]+)\)', source_text)),
        }
        rows[name] = {'sha256': sha(raw), 'utf8_bytes': len(raw),
                      'words_by_whitespace': len(text.split()),
                      'protected_literals': len(registry['protected_literals']),
                      'checks': checks, 'passed': all(checks.values())}
    report = {'schema': 'knowledge-contract.public-editorial-record-check/1',
              'source_hash_matches': source_ok, 'source_words_by_whitespace': len(source_text.split()),
              'variants': rows, 'passed': source_ok and all(row['passed'] for row in rows.values()),
              'scope': 'New check of retained source and first responses. Semantic judgments for 19 claims and stylistic scores remain the recorded agent review, not a result of this program.'}
    print(json.dumps(report, indent=2))
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())

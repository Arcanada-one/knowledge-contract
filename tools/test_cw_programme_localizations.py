#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Coverage and source-drift controls for the two CW reader programmes."""
import copy
import hashlib
import json
from pathlib import Path
import unittest
from tools.cw_programme_localizations import render_locale_programmes, render_localized_programme


ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / 'roadmap/coordinated-work/plan'


class LocaleControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = json.loads((PLAN / 'execution-graph.json').read_text())
        cls.data = json.loads((ROOT / 'tools/cw_programme_locale_data.json').read_text())
        cls.english = (PLAN / 'PROGRAMME.md').read_text()
        cls.digest = hashlib.sha256(cls.english.encode()).hexdigest()

    def test_both_languages_cover_all_scope_identifiers(self):
        result = render_locale_programmes(self.graph, self.english)
        self.assertEqual(set(result), {'PROGRAMME.ru.md', 'PROGRAMME.zh-Hans.md'})
        ids = [row['id'] for category in ('epics', 'tasks', 'papers', 'hypotheses') for row in self.graph[category]]
        for content in result.values():
            for identifier in ids:
                self.assertIn(identifier, content)
            self.assertIn(self.digest, content)
            self.assertIn('independent_fidelity_review: not_recorded', content)

    def test_modified_english_changes_both_source_bindings(self):
        changed = self.english + '\nA separately revised source sentence.\n'
        expected = hashlib.sha256(changed.encode()).hexdigest()
        for content in render_locale_programmes(self.graph, changed).values():
            self.assertIn(expected, content)
            self.assertNotIn(self.digest, content)

    def test_changed_source_title_requires_translation_review(self):
        graph = copy.deepcopy(self.graph)
        graph['tasks'][0]['title'] += ' with a new condition'
        with self.assertRaisesRegex(ValueError, 'CW_LOCALE_SOURCE_DRIFT: tasks'):
            render_localized_programme(graph, 'ru', self.digest, self.data)

    def test_missing_chinese_task_title_is_refused(self):
        data = copy.deepcopy(self.data)
        del data['locales']['zh-Hans']['tasks']['CW-A01']
        with self.assertRaisesRegex(ValueError, 'CW_LOCALE_COVERAGE: zh-Hans/tasks'):
            render_localized_programme(self.graph, 'zh-Hans', self.digest, data)

    def test_missing_russian_hypothesis_is_refused(self):
        data = copy.deepcopy(self.data)
        del data['locales']['ru']['hypotheses']['CW-HYP01']
        with self.assertRaisesRegex(ValueError, 'CW_LOCALE_COVERAGE: ru/hypotheses'):
            render_localized_programme(self.graph, 'ru', self.digest, data)

    def test_blank_paper_question_is_refused(self):
        data = copy.deepcopy(self.data)
        data['locales']['zh-Hans']['papers']['CW-P13']['question'] = ' '
        with self.assertRaisesRegex(ValueError, 'CW_LOCALE_EMPTY_FIELD: zh-Hans/papers/CW-P13'):
            render_localized_programme(self.graph, 'zh-Hans', self.digest, data)


if __name__ == '__main__':
    unittest.main()

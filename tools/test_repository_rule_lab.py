# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""The lab must refuse incomplete plans before executing a reduced inventory."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from tools import run_repository_rule_lab as lab


class RepositoryRuleLabInventoryTests(unittest.TestCase):
    def test_registered_positive_and_each_missing_case(self):
        plan = lab.load_plan(lab.ROOT / lab.INVENTORY)
        self.assertEqual(len(plan["cases"]), 12)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "plan.json"
            for index, removed in enumerate(plan["cases"]):
                broken = deepcopy(plan)
                del broken["cases"][index]
                path.write_text(json.dumps(broken), encoding="utf-8")
                with self.subTest(removed=removed["id"]), self.assertRaises(ValueError):
                    lab.load_plan(path)

    def test_duplicate_reordered_and_injected_noncase_are_refused(self):
        plan = lab.load_plan(lab.ROOT / lab.INVENTORY)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "plan.json"
            for name in ("duplicate", "reordered", "noncase"):
                broken = deepcopy(plan)
                if name == "duplicate":
                    broken["cases"][3] = broken["cases"][2]
                elif name == "reordered":
                    broken["cases"][3], broken["cases"][4] = broken["cases"][4], broken["cases"][3]
                else:
                    broken["cases"].insert(2, None)
                path.write_text(json.dumps(broken), encoding="utf-8")
                with self.subTest(mutation=name), self.assertRaises(ValueError):
                    lab.load_plan(path)


if __name__ == "__main__":
    unittest.main()

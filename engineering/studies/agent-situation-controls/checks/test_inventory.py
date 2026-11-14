"""Behavioral controls for complete, ID-bound finite-suite registration."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import check_agent_situation as runner


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.cases = list(runner.CASES)
        self.fixtures = json.loads((runner.ROOT / "checks/expected.json").read_text())

    def test_complete_inventory_binds_by_id_despite_order(self):
        inventory = runner.validate_inventory(self.cases[::-1], self.fixtures[::-1])
        self.assertEqual([identity for identity, _, _ in inventory], list(range(1, 22)))
        registered = dict(self.cases)
        for identity, function, fixture in inventory:
            self.assertIs(function, registered[identity])
            self.assertEqual(fixture["id"], identity)

    def test_missing_registration_stops_main_before_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "checks").mkdir()
            (root / "checks/expected.json").write_text(json.dumps(self.fixtures))
            evidence = root / "missing-control.json"
            with patch.object(runner, "ROOT", root), patch.object(runner, "CASES", self.cases[:-1]), \
                    patch("sys.argv", ["check_agent_situation.py", "--evidence", str(evidence)]):
                with self.assertRaises(ValueError):
                    runner.main()
            self.assertFalse(evidence.exists())

    def test_extra_registration_is_rejected(self):
        with self.assertRaises(ValueError):
            runner.validate_inventory(self.cases + [(22, lambda scenario: {})], self.fixtures)

    def test_duplicate_registered_id_is_rejected(self):
        duplicated = self.cases[:-1] + [(1, self.cases[-1][1])]
        with self.assertRaises(ValueError):
            runner.validate_inventory(duplicated, self.fixtures)

    def test_duplicate_callable_cannot_replace_another_control(self):
        duplicated = self.cases[:-1] + [(21, self.cases[-2][1])]
        with self.assertRaises(ValueError):
            runner.validate_inventory(duplicated, self.fixtures)

    def test_missing_fixture_is_rejected(self):
        with self.assertRaises(ValueError):
            runner.validate_inventory(self.cases, self.fixtures[:-1])

    def test_duplicate_fixture_id_is_rejected(self):
        with self.assertRaises(ValueError):
            runner.validate_inventory(self.cases, self.fixtures[:-1] + [self.fixtures[0]])

    def test_mismatched_registration_id_is_rejected(self):
        mismatched = self.cases[:-1] + [(22, self.cases[-1][1])]
        with self.assertRaises(ValueError):
            runner.validate_inventory(mismatched, self.fixtures)

    def test_failed_execution_counts_no_unperformed_field_checks(self):
        def fail_before_result(scenario):
            raise RuntimeError("intentional single failed execution")
        result = runner.run_case(fail_before_result, self.fixtures[0])
        self.assertFalse(result["passed"])
        self.assertEqual(result["field_checks"], {})


if __name__ == "__main__":
    unittest.main()

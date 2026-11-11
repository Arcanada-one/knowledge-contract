# SPDX-FileCopyrightText: 2026 Pavel Valentov
# SPDX-License-Identifier: Apache-2.0
"""Finite countermodel for omitting C03's initial-state precondition.

This checks one constructed model, not the manuscript's general proof or any
implementation. The two worlds are intentionally small and exhaustive.
"""
import unittest


DOMAIN = (0, 1)
RELATION = ((0, 1), (1, 1))


def precondition(x):
    return x == 1


def postcondition(_y):
    return True


def observation(x):
    return x


class C03InitialPreconditionTests(unittest.TestCase):
    def test_carriers_and_transitions_are_finite_and_well_typed(self):
        self.assertTrue(RELATION)
        self.assertTrue(all(x in DOMAIN and y in DOMAIN for x, y in RELATION))

    def test_local_partial_correctness_for_all_admitted_transitions(self):
        self.assertTrue(all(not precondition(x) or postcondition(y)
                            for x, y in RELATION))

    def test_local_observation_preserved_on_every_admitted_transition(self):
        self.assertTrue(all(not precondition(x) or observation(x) == observation(y)
                            for x, y in RELATION))

    def test_admitted_successful_path_preserves_endpoint(self):
        self.assertIn((1, 1), RELATION)
        self.assertTrue(precondition(1))
        self.assertEqual(observation(1), observation(1))

    def test_omitting_p1_allows_a_successful_path_that_loses_observation(self):
        self.assertIn((0, 1), RELATION)
        self.assertFalse(precondition(0))
        self.assertNotEqual(observation(0), observation(1))

    def test_single_step_has_no_junction_obligations(self):
        # For n=1, the quantified range 1 <= i < n is empty.
        n = 1
        self.assertEqual(list(range(1, n)), [])


if __name__ == "__main__":
    unittest.main()

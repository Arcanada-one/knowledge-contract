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


class C03TwoStepJunctionControls(unittest.TestCase):
    """n=2 finite controls, with genuine junction obligations, not a general proof."""

    def test_two_step_true_junction_and_admitted_chain(self):
        second_relation = ((1, 1),)
        q1 = lambda y: y == 1
        second_input_observation = lambda y: y
        # The junction antecedent is true somewhere: unlike n=1 this is not empty.
        self.assertTrue(any(q1(y) for y in DOMAIN))
        self.assertTrue(all(not q1(y) or precondition(y) for y in DOMAIN))
        self.assertTrue(all(not q1(y) or observation(y) == second_input_observation(y)
                            for y in DOMAIN))
        self.assertTrue(all(not precondition(x) or q1(y)
                            for x, y in RELATION))
        self.assertTrue(all(not precondition(x) or observation(x) == observation(y)
                            for x, y in second_relation))
        chains = {(x, z) for x, y in RELATION for m, z in second_relation
                  if y == m}
        self.assertEqual(chains, {(0, 1), (1, 1)})
        self.assertTrue(all(not precondition(x) or observation(x) == observation(z)
                            for x, z in chains))
        self.assertIn((1, 1), chains)
        self.assertTrue(precondition(1))

    def test_two_step_still_needs_initial_premise(self):
        second_relation = ((1, 1),)
        q1 = lambda y: y == 1
        second_input_observation = lambda y: y
        self.assertTrue(all(not q1(y) or precondition(y) for y in DOMAIN))
        self.assertTrue(all(not q1(y) or observation(y) == second_input_observation(y)
                            for y in DOMAIN))
        self.assertIn((0, 1), RELATION)
        self.assertIn((1, 1), second_relation)
        self.assertFalse(precondition(0))
        self.assertNotEqual(observation(0), observation(1))

    def test_missing_observation_junction_can_lose_endpoint(self):
        second_relation = ((1, 1),)
        q1 = lambda y: y == 1
        second_input_observation = lambda y: 1 - y
        second_output_observation = lambda y: 1 - y
        self.assertTrue(all(not q1(y) or precondition(y) for y in DOMAIN))
        self.assertTrue(all(not precondition(x) or
                            second_input_observation(x) == second_output_observation(y)
                            for x, y in second_relation))
        self.assertFalse(all(not q1(y) or
                             observation(y) == second_input_observation(y)
                             for y in DOMAIN))
        self.assertIn((1, 1), RELATION)
        self.assertIn((1, 1), second_relation)
        self.assertTrue(precondition(1))
        self.assertNotEqual(observation(1), second_output_observation(1))

    def test_missing_precondition_junction_can_lose_endpoint(self):
        second_relation = ((0, 0), (1, 1))
        q1 = lambda y: y == 1
        second_precondition = lambda y: y == 0
        second_output_observation = lambda _y: 0
        self.assertTrue(any(second_precondition(y) for y in DOMAIN))
        self.assertTrue(all(not second_precondition(x) or postcondition(y)
                            for x, y in second_relation))
        self.assertTrue(all(not second_precondition(x) or
                            observation(x) == second_output_observation(y)
                            for x, y in second_relation))
        self.assertTrue(all(not q1(y) or observation(y) == observation(y)
                            for y in DOMAIN))
        self.assertFalse(all(not q1(y) or second_precondition(y)
                             for y in DOMAIN))
        self.assertIn((1, 1), RELATION)
        self.assertIn((1, 1), second_relation)
        self.assertTrue(precondition(1))
        self.assertNotEqual(observation(1), second_output_observation(1))


if __name__ == "__main__":
    unittest.main()

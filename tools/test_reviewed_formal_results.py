#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Finite countermodels for the two corrected publication theorems.

These controls independently enumerate Boolean relations and predicates. They do
not test a production admission service and are not a machine-checked proof for
unbounded state spaces. The general proofs remain in the scientific papers.
"""

from itertools import product
import unittest


VALUES = (0, 1)
EDGES = tuple(product(VALUES, repeat=2))
OBSERVATIONS = tuple(product(VALUES, repeat=2))


def subsets(values):
    """Enumerate a fixed finite domain without a dependency on project code."""
    return tuple(
        frozenset(v for i, v in enumerate(values) if mask & (1 << i))
        for mask in range(1 << len(values))
    )


PREDICATES = subsets(VALUES)
RELATIONS = subsets(EDGES)


def preserves(relation, precondition, before, after):
    return all(before[x] == after[y] for x, y in relation if x in precondition)


class ChainPreservationControls(unittest.TestCase):
    def test_local_preservation_does_not_align_observation_interfaces(self):
        identity = frozenset({(0, 0), (1, 1)})
        identity_observation, negation = (0, 1), (1, 0)
        self.assertTrue(preserves(identity, VALUES, identity_observation, identity_observation))
        self.assertTrue(preserves(identity, VALUES, negation, negation))
        self.assertNotEqual(identity_observation[0], negation[0])
        self.assertNotEqual(identity_observation[1], negation[1])

    def test_aligned_interfaces_do_not_supply_the_next_precondition(self):
        first = frozenset({(0, 0), (1, 1)})
        second = frozenset({(0, 1), (1, 1)})
        observation = (0, 1)
        self.assertTrue(preserves(first, VALUES, observation, observation))
        self.assertTrue(preserves(second, {1}, observation, observation))
        self.assertIn((0, 0), first)
        self.assertIn((0, 1), second)
        self.assertNotIn(0, {1})
        self.assertNotEqual(observation[0], observation[1])

    def test_exhaustive_boolean_relational_chains_with_both_junctions(self):
        steps = []
        for relation, precondition, before, after in product(
            RELATIONS, PREDICATES, OBSERVATIONS, OBSERVATIONS
        ):
            admitted = frozenset((x, y) for x, y in relation if x in precondition)
            if admitted and preserves(admitted, precondition, before, after):
                # The exact image is a valid postcondition for this finite step.
                postcondition = frozenset(y for _, y in admitted)
                steps.append((admitted, precondition, postcondition, before, after))

        witnesses = 0
        for first, second in product(steps, repeat=2):
            rel1, _, post1, before1, after1 = first
            rel2, pre2, _, before2, after2 = second
            if not post1 <= pre2:
                continue
            if any(after1[y] != before2[y] for y in post1):
                continue
            for x, middle in rel1:
                for middle2, z in rel2:
                    if middle == middle2:
                        self.assertEqual(before1[x], after2[z])
                        witnesses += 1
        # Fixed enumeration-size guard; repeated paths belong to different contracts.
        self.assertEqual(witnesses, 15840)


class ReuseAdmissionControls(unittest.TestCase):
    def test_preserved_old_properties_do_not_cover_an_added_requirement(self):
        artifact = (True, False)
        old_property = lambda x: x[0]
        new_requirement = lambda x: x[1]
        identity_output = artifact
        self.assertTrue(old_property(artifact))
        self.assertTrue(old_property(identity_output))
        self.assertFalse(new_requirement(identity_output))
        # The purported coverage implication has this concrete countermodel.
        self.assertFalse(not old_property(identity_output) or new_requirement(identity_output))

    def test_unchanged_state_does_not_cover_changed_request_semantics(self):
        artifact_referent = 0
        old_request_referent, new_request_referent = 0, 1
        property_for_request = lambda artifact, request: artifact == request
        self.assertTrue(property_for_request(artifact_referent, old_request_referent))
        self.assertFalse(property_for_request(artifact_referent, new_request_referent))
        self.assertNotEqual(old_request_referent, new_request_referent)

    def test_one_good_relational_output_does_not_establish_preservation(self):
        relation = frozenset({(0, 0), (0, 1)})
        property_holds = lambda artifact: artifact == 0
        outputs = [y for x, y in relation if x == 0]
        self.assertTrue(property_holds(0))
        self.assertTrue(any(property_holds(y) for y in outputs))
        self.assertFalse(all(property_holds(y) for y in outputs))

    def test_positive_receipt_is_not_the_sound_prior_verification_premise(self):
        recorded_result = "pass"
        actual_property = False
        self.assertEqual(recorded_result, "pass")
        self.assertFalse(actual_property)

    def test_exhaustive_boolean_reuse_with_request_coverage_and_all_outputs(self):
        witnesses = 0
        # Every predicate on artifact, material request bit, and material state
        # bit is included. The second request/state bits are declared irrelevant.
        for truth_table in product((False, True), repeat=8):
            def property_holds(artifact, request, state):
                return truth_table[4 * artifact + 2 * request[0] + state[0]]

            for request_bit, state_bit in product(VALUES, repeat=2):
                q, q_new = (request_bit, 0), (request_bit, 1)
                s, s_new = (state_bit, 0), (state_bit, 1)
                supported = frozenset(x for x in VALUES if property_holds(x, q, s))
                for artifact, relation, artifact_requirement, current_use in product(
                    supported, RELATIONS, PREDICATES, PREDICATES
                ):
                    outputs = frozenset(y for x, y in relation if x == artifact)
                    if not outputs:
                        continue
                    # Coverage must be an implication, not just one matching label.
                    if not supported <= artifact_requirement:
                        continue
                    if not all(property_holds(y, q_new, s_new) for y in outputs):
                        continue
                    if not outputs <= current_use:
                        continue
                    self.assertTrue(property_holds(artifact, q_new, s_new))
                    for output in outputs:
                        self.assertIn(output, artifact_requirement)
                        self.assertIn(output, current_use)
                        witnesses += 1
        # Fixed enumeration-size guard; these are outputs in a model, not trials.
        self.assertEqual(witnesses, 20480)


if __name__ == "__main__":
    unittest.main()

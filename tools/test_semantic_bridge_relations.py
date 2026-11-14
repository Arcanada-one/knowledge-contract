#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Bounded integration of computed bridge tables with existing finite relations.

Every relation below comes from actual bridge output, with an explicit carrier
encoding: world rows are source states and Boolean false/true are target 0/1.
The partial-domain check explicitly embeds a known Boolean input into that same
carrier; integer cardinality alone cannot establish a semantic correspondence.
These checks neither parse unrestricted language nor infer permission, observed
refusal, or a general preservation theorem. The largest carrier has eight states.
"""
from __future__ import annotations

from fractions import Fraction
import hashlib
import unittest

from tools import semantic_bridge as bridge
from tools import semantic_relations as relations


BOOLEAN_METRIC = ((0, 1), (1, 0))
BOOLEAN_OBSERVATION = relations.Partition(2, (frozenset({0}), frozenset({1})))
LENDING = "(member AND trained) UNLESS suspended"
LENDING_BINDINGS = {name: name for name in ("member", "trained", "suspended")}


def _packet(rules, values):
    """Author controlled input; do not extract readings from human prose."""
    source = b"NOTE Original hypothetical integration case; no permission is granted.\n"
    readings = []
    for identity, expression, bindings in rules:
        line = f"RULE {identity}: {expression}".encode("utf-8")
        start = len(source)
        source += line + b"\n"
        readings.append({
            "id": identity, "start": start, "end": start + len(line),
            "quote": line.decode("utf-8"),
            "attribution": {"agent": "Integration example author", "discourse": "hypothetical"},
            "bindings": bindings,
        })
    observations = {}
    for identity, value in values.items():
        observation = {"referent": f"The example's supplied {identity} condition.",
                       "type": "boolean", "state": "unknown" if value is None else "known"}
        if value is not None:
            observation["value"] = value
        observations[identity] = observation
    return source, {
        "schema": "kc-semantic-bridge/1",
        "source_sha256": hashlib.sha256(source).hexdigest(),
        "source_media_type": "text/plain", "interpretation_set": "alternatives",
        "observations": observations, "readings": readings,
    }


def _row(report, identity):
    return next(row for row in report["readings"] if row["id"] == identity)


def _table_relation(report, identity):
    """World index -> Boolean state, without collapsing a false value to no edge."""
    bits = _row(report, identity)["table_bits"]
    return relations.FiniteRelation(
        len(report["world_assignments"]), 2,
        frozenset((world_index, int(bit)) for world_index, bit in enumerate(bits)),
    )


def _partition(worlds, observation):
    blocks = {}
    for index, world in enumerate(worlds):
        blocks.setdefault(observation(world), set()).add(index)
    return relations.Partition(len(worlds), tuple(frozenset(block) for block in blocks.values()))


def _qualification_and_exception(world):
    return world["member"] and world["trained"], world["suspended"]


class SemanticBridgeRelationsTests(unittest.TestCase):
    def _evaluate(self, rules, values):
        source, packet = _packet(rules, values)
        report = bridge.analyze(source, packet)
        self.assertEqual(report["status"], "EVALUATED", report)
        self.assertFalse(report["effects_authorized"])
        self.assertEqual(report["source_semantic_fidelity"], "NOT_ASSESSED")
        self.assertEqual(report["current_authority"], "NOT_ASSESSED")
        self.assertLessEqual(len(report["world_assignments"]), relations.MAX_STATES)
        for row in report["readings"]:
            self.assertEqual(len(row["table_bits"]), len(report["world_assignments"]))
        return report

    def _lending(self, expression=LENDING):
        return self._evaluate(
            [("lending", expression, dict(LENDING_BINDINGS))],
            {name: None for name in LENDING_BINDINGS},
        )

    def test_computed_relation_accepts_sufficient_observation_but_not_dropped_exception(self):
        report = self._lending()
        worlds = report["world_assignments"]
        self.assertEqual(len(worlds), 8)
        expected = tuple(w["member"] and w["trained"] and not w["suspended"] for w in worlds)
        self.assertEqual(_row(report, "lending")["table_bits"],
                         "".join("1" if value else "0" for value in expected))
        concrete = _table_relation(report, "lending")
        self.assertEqual(concrete.pairs,
                         frozenset((index, int(value)) for index, value in enumerate(expected)))
        self.assertTrue(all(concrete.image(index) for index in range(8)))

        sufficient = _partition(worlds, _qualification_and_exception)
        self.assertEqual(sorted(map(len, sufficient.blocks)), [1, 1, 3, 3])
        checked = relations.analyze_quotient(concrete, sufficient, BOOLEAN_OBSERVATION)
        self.assertTrue(checked.coherent)
        self.assertIsNone(checked.witness)
        self.assertEqual(checked.quotient.pairs,
                         frozenset((sufficient.class_of(index), int(value))
                                   for index, value in enumerate(expected)))
        # Nontrivial replacement: two classes each contain three different worlds.
        for block in sufficient.blocks:
            representative = min(block)
            self.assertTrue(all(concrete.image(other) == concrete.image(representative)
                                for other in block))

        omitted_exception = _partition(worlds, lambda w: w["member"] and w["trained"])
        refused = relations.analyze_quotient(concrete, omitted_exception, BOOLEAN_OBSERVATION)
        self.assertFalse(refused.coherent)
        self.assertIsNone(refused.quotient)
        first, second = refused.witness["representatives"]
        self.assertEqual(omitted_exception.class_of(first), omitted_exception.class_of(second))
        self.assertTrue(worlds[first]["member"] and worlds[first]["trained"])
        self.assertTrue(worlds[second]["member"] and worlds[second]["trained"])
        self.assertNotEqual(worlds[first]["suspended"], worlds[second]["suspended"])
        self.assertNotEqual(concrete.image(first), concrete.image(second))

    def test_two_computed_stages_compose_on_the_declared_boolean_interface(self):
        before = self._lending()
        after = self._evaluate([("invert", "NOT flag", {"flag": "flag"})], {"flag": None})
        direct = self._lending(f"NOT ({LENDING})")
        # The intermediate labels have explicit meaning, not just equal sizes.
        self.assertEqual(after["world_assignments"], [{"flag": False}, {"flag": True}])
        self.assertEqual(before["world_assignments"], direct["world_assignments"])
        first = _table_relation(before, "lending")
        second = _table_relation(after, "invert")
        expected = _table_relation(direct, "lending")
        self.assertEqual(second.pairs, frozenset({(0, 1), (1, 0)}))
        self.assertEqual(relations.compose(first, second), expected)

        source = _partition(before["world_assignments"], _qualification_and_exception)
        abstract = relations.quotient_composition(
            first, second, source, BOOLEAN_OBSERVATION, BOOLEAN_OBSERVATION)
        direct_quotient = relations.analyze_quotient(expected, source, BOOLEAN_OBSERVATION)
        self.assertTrue(direct_quotient.coherent)
        self.assertEqual(abstract, direct_quotient.quotient)

        incompatible = relations.FiniteRelation(3, 2, frozenset({(0, 1), (1, 0), (2, 0)}))
        with self.assertRaises(ValueError):
            relations.compose(first, incompatible)
        with self.assertRaises(ValueError):
            relations.quotient_composition(
                first, incompatible, source, BOOLEAN_OBSERVATION, BOOLEAN_OBSERVATION)

    def test_known_input_requires_explicit_embedding_and_leaves_partial_composition(self):
        before = self._lending()
        restricted = self._evaluate(
            [("invert", "NOT flag", {"flag": "flag"})], {"flag": True})
        self.assertEqual(restricted["world_assignments"], [{"flag": True}])
        first = _table_relation(before, "lending")
        local_second = _table_relation(restricted, "invert")
        self.assertEqual(local_second.source_size, 1)
        # Local row 0 here denotes true, unlike Boolean-carrier state 0.
        with self.assertRaises(ValueError):
            relations.compose(first, local_second)

        bits = _row(restricted, "invert")["table_bits"]
        embedded = relations.FiniteRelation(
            2, 2,
            frozenset((int(world["flag"]), int(bit))
                      for world, bit in zip(restricted["world_assignments"], bits)),
        )
        self.assertEqual(embedded.pairs, frozenset({(1, 0)}))
        composite = relations.compose(first, embedded)
        true_worlds = {index for index, bit in enumerate(_row(before, "lending")["table_bits"])
                       if bit == "1"}
        self.assertEqual(len(true_worlds), 1)
        self.assertEqual(composite.pairs, frozenset((index, 0) for index in true_worlds))
        images = tuple(composite.image(index) for index in range(len(before["world_assignments"])))
        self.assertEqual(sum(not image for image in images), 7)

        worlds = before["world_assignments"]
        names = tuple(before["observation_ids"])
        hamming = tuple(tuple(Fraction(sum(a[name] != b[name] for name in names), len(names))
                              for b in worlds) for a in worlds)
        # Successful-path absence is not false, observed refusal, or a metric point.
        with self.assertRaises(ValueError):
            relations.lipschitz_constant(images, hamming, BOOLEAN_METRIC)

    def test_outcome_set_geometry_does_not_restore_same_world_correlation(self):
        names = ("member", "guest", "trained")
        bindings = {name: name for name in names}
        report = self._evaluate([
            ("broad", "(member OR guest) AND trained", dict(bindings)),
            ("narrow", "member OR (guest AND trained)", dict(bindings)),
        ], {name: None for name in names})
        rows = [_row(report, identity) for identity in ("broad", "narrow")]
        images = tuple(frozenset(int(value) for value in row["possible_values"]) for row in rows)
        self.assertEqual(images, (frozenset({0, 1}), frozenset({0, 1})))
        marginals = relations.FiniteRelation(
            2, 2, frozenset((reading, value) for reading, image in enumerate(images) for value in image))
        no_reading_distinction = relations.Partition(2, (frozenset({0, 1}),))
        self.assertTrue(relations.analyze_quotient(
            marginals, no_reading_distinction, BOOLEAN_OBSERVATION).coherent)
        self.assertEqual(relations.hausdorff(images[0], images[1], BOOLEAN_METRIC), Fraction(0))
        self.assertEqual(relations.lipschitz_constant(images, BOOLEAN_METRIC, BOOLEAN_METRIC), Fraction(0))

        aligned_distances = tuple(relations.hausdorff({int(left)}, {int(right)}, BOOLEAN_METRIC)
                                  for left, right in zip(rows[0]["table_bits"], rows[1]["table_bits"]))
        self.assertEqual(sum(distance == 1 for distance in aligned_distances), 2)
        self.assertEqual(max(aligned_distances), Fraction(1))
        self.assertTrue(report["reading_disagreement"])
        self.assertEqual(report["truth"], "UNDETERMINED")
        # The global outcome sets omitted their world labels; zero set distance
        # certifies equality of those marginals, not a conditional substitution.


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Independent finite oracles for the relation/geometry reference implementation.

The implementation uses sets of edges and max/min metric formulae. This oracle
encodes relation rows as integer masks, composes Boolean rows, and finds finite
Hausdorff distances by symmetric neighbourhood coverage. It imports no private
implementation helper. Exhaustive counts describe these finite spaces, not
independent observations, a general proof, language extraction, or production.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import replace
from fractions import Fraction
from itertools import product
import unittest

from tools import semantic_relations as api


SIZE = 3
CLASS_OF = (0, 0, 1)
METRIC = tuple(tuple(Fraction(abs(x - y), 2) for y in range(SIZE))
               for x in range(SIZE))


def _require(condition, message):
    if not condition:
        raise AssertionError(message)


def _members(mask, width=SIZE):
    return tuple(i for i in range(width) if mask & (1 << i))


def _rows(code):
    return tuple((code >> (SIZE * row)) & ((1 << SIZE) - 1)
                 for row in range(SIZE))


def _pairs(rows):
    return frozenset((i, j) for i, row in enumerate(rows) for j in _members(row))


def _row_product(first, second):
    """Boolean matrix multiplication; an empty row remains a real zero row."""
    result = []
    for row in first:
        output = 0
        for intermediate in _members(row, len(second)):
            output |= second[intermediate]
        result.append(output)
    return tuple(result)


def _class_mask(row):
    return (1 if row & 0b011 else 0) | (2 if row & 0b100 else 0)


def _coherent(rows):
    return _class_mask(rows[0]) == _class_mask(rows[1])


def _class_rows(rows):
    """Independent existential projection, valid on incoherent rows too."""
    return (_class_mask(rows[0] | rows[1]), _class_mask(rows[2]))


def _class_pairs(rows):
    return frozenset((i, j) for i, row in enumerate(rows)
                     for j in _members(row, 2))


def _verify_witness(rows, witness):
    _require(isinstance(witness, dict), "missing incoherence witness")
    x, other = witness["representatives"]
    _require(0 <= x < SIZE and 0 <= other < SIZE, "witness outside carrier")
    _require(CLASS_OF[x] == CLASS_OF[other], "witness inputs not equivalent")
    images = (_class_mask(rows[x]), _class_mask(rows[other]))
    _require(images[0] != images[1], "witness does not show incoherence")
    _require(witness["input_class"] == CLASS_OF[x], "wrong witness class")
    _require(witness["reachable_classes"] == [list(_members(m, 2)) for m in images],
             "witness output classes disagree with relation")
    _require(witness["empty_images"] == [not images[0], not images[1]],
             "witness empty-image labels disagree with relation")


def audit_relations():
    partition = api.Partition(SIZE, (frozenset({0, 1}), frozenset({2})))
    admitted = []
    counters = Counter()
    for code in range(1 << (SIZE * SIZE)):
        rows = _rows(code)
        relation = api.FiniteRelation(SIZE, SIZE, _pairs(rows))
        actual = api.analyze_quotient(relation, partition, partition)
        expected = _coherent(rows)
        _require(actual.coherent is expected, f"coherence mismatch for mask {code}")
        coarse = api.existential_quotient(relation, partition, partition)
        _require(coarse.pairs == _class_pairs(_class_rows(rows)),
                 f"coarse quotient mismatch for mask {code}")
        counters["relations"] += 1
        if expected:
            _require(actual.witness is None, "coherent relation has adverse witness")
            _require(actual.quotient == coarse, "wrong exact quotient")
            admitted.append((rows, relation))
            counters["coherent_relations"] += 1
            counters["coherent_total_relations"] += int(all(rows))
            counters["coherent_empty_relations"] += int(not any(rows))
        else:
            _require(actual.quotient is None, "incoherent relation certified exact")
            _verify_witness(rows, actual.witness)
            counters["incoherent_relations"] += 1

    for (first, first_api), (second, second_api) in product(admitted, repeat=2):
        concrete = _row_product(first, second)
        abstract = _row_product(_class_rows(first), _class_rows(second))
        _require(_coherent(concrete), "coherent input relations lost coherence")
        _require(_class_rows(concrete) == abstract,
                 "finite oracle violates exact quotient-composition law")
        actual_concrete = api.compose(first_api, second_api)
        _require(actual_concrete.pairs == _pairs(concrete),
                 "implementation composition differs from Boolean matrix oracle")
        actual_abstract = api.quotient_composition(
            first_api, second_api, partition, partition, partition)
        _require(actual_abstract.pairs == _class_pairs(abstract),
                 "implementation quotient composition differs from concrete paths")
        _require((actual_abstract.source_size, actual_abstract.target_size) == (2, 2),
                 "composition returned wrong quotient carriers")
        counters["admitted_ordered_pairs"] += 1
        counters["pairs_with_empty_composite"] += int(not any(concrete))
        counters["pairs_with_nonempty_composite"] += int(any(concrete))
        counters["pairs_with_all_source_images_nonempty"] += int(all(concrete))

    _require(counters["relations"] == 2 ** (SIZE * SIZE), "relation inventory incomplete")
    _require(counters["admitted_ordered_pairs"] == len(admitted) ** 2,
             "admitted composition inventory incomplete")
    _require(counters["pairs_with_nonempty_composite"] > 0,
             "empty-only enumeration cannot support useful composition")
    return {
        "space": "all 3-by-3 Boolean relations; partition ((0,1),(2,)) on each carrier",
        "enumeration_formula": "2^(3*3); all ordered pairs of actually coherent relations",
        "observed_counts": dict(sorted(counters.items())),
        "result": "pass",
        "limits": "Successful-edge semantics only; no refusal, termination or permission observation.",
    }


def _neighbourhood(mask, radius):
    result = 0
    for point in _members(mask):
        for other in range(SIZE):
            if abs(point - other) <= radius:
                result |= 1 << other
    return result


def _hausdorff_steps(left, right):
    """Least symmetric coverage radius, in units of one half."""
    if not left or not right:
        raise ValueError("oracle has no empty-set metric convention")
    for radius in range(SIZE):
        if (left & ~_neighbourhood(right, radius) == 0
                and right & ~_neighbourhood(left, radius) == 0):
            return radius
    raise AssertionError("finite carrier unexpectedly lacks a covering radius")


H_STEPS = {(a, b): _hausdorff_steps(a, b)
           for a, b in product(range(1, 1 << SIZE), repeat=2)}
L_CANDIDATES = tuple(sorted({Fraction(d, gap)
                             for d in range(SIZE) for gap in range(1, SIZE)}))


def _least_bound(images):
    """Search possible exact bounds; do not repeat the implementation's max-ratio routine."""
    for bound in L_CANDIDATES:
        if all(H_STEPS[images[x], images[y]] <= bound * abs(x - y)
               for x, y in product(range(SIZE), repeat=2)):
            return bound
    raise AssertionError("a total finite map must have a finite Lipschitz bound")


def audit_geometry():
    maps = tuple(product(range(1, 1 << SIZE), repeat=SIZE))
    concrete_maps = {rows: tuple(frozenset(_members(row)) for row in rows) for rows in maps}
    expected_bounds = {rows: _least_bound(rows) for rows in maps}
    actual_bounds = {}
    counters = Counter()
    bounds_histogram = Counter()
    for (left, right), steps in H_STEPS.items():
        actual = api.hausdorff(frozenset(_members(left)), frozenset(_members(right)), METRIC)
        _require(actual == Fraction(steps, 2), "Hausdorff mismatch with coverage-radius oracle")
        counters["nonempty_set_pairs"] += 1
    for rows in maps:
        actual_bounds[rows] = api.lipschitz_constant(concrete_maps[rows], METRIC, METRIC)
        _require(actual_bounds[rows] == expected_bounds[rows],
                 f"Lipschitz mismatch for rows {rows}")
        counters["total_nonempty_valued_maps"] += 1
        counters["deterministic_maps"] += int(all(row.bit_count() == 1 for row in rows))
        counters["constant_maps"] += int(len(set(rows)) == 1)
        bounds_histogram[str(expected_bounds[rows])] += 1

    for first, second in product(maps, repeat=2):
        expected = _row_product(first, second)
        actual = api.compose_images(concrete_maps[first], concrete_maps[second])
        _require(actual == concrete_maps[expected],
                 "set-valued implementation composition differs from Boolean matrix oracle")
        composite_bound = expected_bounds[expected]
        upper_bound = expected_bounds[first] * expected_bounds[second]
        _require(composite_bound <= upper_bound, "finite Lipschitz composition law failed")
        _require(actual_bounds[expected] <= actual_bounds[first] * actual_bounds[second],
                 "implementation Lipschitz composition law failed")
        counters["ordered_map_pairs"] += 1
        counters["bound_equalities"] += int(composite_bound == upper_bound)
        counters["strict_inequalities"] += int(composite_bound < upper_bound)
        counters["constant_composites"] += int(composite_bound == 0)

    _require(counters["total_nonempty_valued_maps"] == (2 ** SIZE - 1) ** SIZE,
             "map inventory incomplete")
    _require(counters["ordered_map_pairs"] == len(maps) ** 2,
             "ordered map-pair inventory incomplete")
    _require(counters["bound_equalities"] > 0 and counters["strict_inequalities"] > 0,
             "missing tight or nontight positive paths")
    return {
        "space": "all nonempty-valued maps on exact metric carrier {0,1/2,1}",
        "enumeration_formula": "(2^3-1)^3 maps; ((2^3-1)^3)^2 ordered pairs",
        "observed_counts": dict(sorted(counters.items())),
        "least_lipschitz_bound_histogram": dict(sorted(bounds_histogram.items())),
        "result": "pass",
        "limits": "Exact finite reference maps; no learned representation or empirical similarity claim.",
    }


def _raises_value_error(function, *args):
    try:
        function(*args)
    except ValueError:
        return True
    return False


def audit_single_defect_controls():
    """Four explicit API-behaviour mutants, each retaining its valid control.

    These are local deliberate wrappers, not claims about deployed bugs. Each
    modifies one condition or aggregation; unaffected behavior delegates to the
    real reference implementation. Unexpected exceptions remain failures.
    """
    source = api.Partition(1, (frozenset({0}),))
    middle = api.Partition(2, (frozenset({0, 1}),))
    target = api.Partition(2, (frozenset({0}), frozenset({1})))
    first = api.FiniteRelation(1, 2, frozenset({(0, 0)}))
    good = api.FiniteRelation(2, 2, frozenset({(0, 0), (1, 0)}))
    empty_difference = api.FiniteRelation(2, 2, frozenset({(1, 0)}))
    output_difference = api.FiniteRelation(2, 2, frozenset({(0, 0), (1, 0), (1, 1)}))

    def coarse_composition(a, b, x, y, z):
        # One defect: omit the required coherence guard, keeping ordinary composition.
        return api.compose(api.existential_quotient(a, x, y),
                           api.existential_quotient(b, y, z))

    def ignore_empty_images(relation, src, dst):
        result = api.analyze_quotient(relation, src, dst)
        if result.coherent:
            return result
        # One defect: omit empty images from representative comparisons.
        outputs = [frozenset(dst.class_of(b) for a, b in relation.pairs if a == x)
                   for x in range(src.size)]
        if all(len({outputs[x] for x in block if outputs[x]}) <= 1 for block in src.blocks):
            return replace(result, coherent=True,
                           quotient=api.existential_quotient(relation, src, dst), witness=None)
        return result

    def closest_pair(left, right, metric):
        if not left or not right:
            return api.hausdorff(left, right, metric)
        # One defect: nearest pair replaces worst directed coverage.
        return min(metric[x][y] for x in left for y in right)

    def empty_is_zero(left, right, metric):
        # One defect: invent a zero score where the profile has no distance.
        return Fraction(0) if not left or not right else api.hausdorff(left, right, metric)

    results = []
    args = (first, output_difference, source, middle, target)
    _require(_raises_value_error(api.quotient_composition, *args), "baseline missed output-class violation")
    _require(api.quotient_composition(first, good, source, middle, target).pairs == frozenset({(0, 0)}),
             "baseline lacks useful valid quotient composition")
    results.append({
        "id": "omit-coherence-guard",
        "single_defect": "replace exact quotient composition by coarse existential composition",
        "baseline_rejects_adverse": True,
        "detected": not _raises_value_error(coarse_composition, *args),
        "positive_control_preserved": coarse_composition(first, good, source, middle, target).pairs == frozenset({(0, 0)}),
    })
    _require(not api.analyze_quotient(empty_difference, middle, target).coherent,
             "baseline missed empty-image distinction")
    results.append({
        "id": "ignore-empty-images",
        "single_defect": "compare only nonempty representative images",
        "baseline_rejects_adverse": True,
        "detected": ignore_empty_images(empty_difference, middle, target).coherent,
        "positive_control_preserved": ignore_empty_images(good, middle, target).coherent,
    })
    left, right = frozenset({0}), frozenset({0, 2})
    _require(api.hausdorff(left, right, METRIC) == 1, "baseline Hausdorff adverse expectation failed")
    results.append({
        "id": "closest-pair-distance",
        "single_defect": "replace symmetric Hausdorff aggregation by minimum pair distance",
        "baseline_expected": "1",
        "mutant_observed": str(closest_pair(left, right, METRIC)),
        "detected": closest_pair(left, right, METRIC) != 1,
        "positive_control_preserved": closest_pair(frozenset({0}), frozenset({2}), METRIC) == 1,
    })
    _require(_raises_value_error(api.hausdorff, frozenset(), left, METRIC),
             "baseline assigned a distance to an empty image")
    results.append({
        "id": "empty-distance-zero",
        "single_defect": "replace empty-set rejection by distance zero",
        "baseline_rejects_adverse": True,
        "detected": not _raises_value_error(empty_is_zero, frozenset(), left, METRIC),
        "positive_control_preserved": empty_is_zero(left, right, METRIC) == 1,
    })
    _require(len(results) == 4, "controlled-defect inventory incomplete")
    _require(all(row["detected"] and row["positive_control_preserved"] for row in results),
             "a controlled defect survived or damaged its valid control")
    return {"result": "pass", "mutants": results,
            "limits": "Four explicit API-behaviour wrappers; not an exhaustive source-mutation campaign."}


def run_finite_audit():
    return {
        "relations": audit_relations(),
        "geometry": audit_geometry(),
        "single_defect_controls": audit_single_defect_controls(),
        "independence": "Separately authored finite bit-mask/neighbourhood oracle; same controller/model family/host.",
    }


class FiniteOracleTests(unittest.TestCase):
    def test_all_relations_and_admitted_compositions(self):
        self.assertEqual(audit_relations()["result"], "pass")

    def test_all_nonempty_maps_and_hausdorff_compositions(self):
        self.assertEqual(audit_geometry()["result"], "pass")

    def test_each_single_defect_has_a_distinguishing_and_valid_control(self):
        self.assertEqual(audit_single_defect_controls()["result"], "pass")


class BoundaryAndPositiveTests(unittest.TestCase):
    def test_no_concrete_path_is_created_by_merging_intermediate_representatives(self):
        start = api.Partition(1, (frozenset({0}),))
        middle = api.Partition(2, (frozenset({0, 1}),))
        finish = api.Partition(1, (frozenset({0}),))
        first = api.FiniteRelation(1, 2, frozenset({(0, 0)}))
        second = api.FiniteRelation(2, 1, frozenset({(1, 0)}))
        self.assertFalse(api.compose(first, second).pairs)
        coarse = api.compose(api.existential_quotient(first, start, middle),
                             api.existential_quotient(second, middle, finish))
        self.assertEqual(coarse.pairs, frozenset({(0, 0)}))
        with self.assertRaises(ValueError):
            api.quotient_composition(first, second, start, middle, finish)

    def test_nonempty_images_can_still_disagree_on_an_unfavourable_branch(self):
        inputs = api.Partition(2, (frozenset({0, 1}),))
        outputs = api.Partition(2, (frozenset({0}), frozenset({1})))
        relation = api.FiniteRelation(2, 2, frozenset({(0, 0), (1, 0), (1, 1)}))
        result = api.analyze_quotient(relation, inputs, outputs)
        self.assertFalse(result.coherent)
        self.assertEqual(result.witness["reachable_classes"], [[0], [0, 1]])
        self.assertEqual(result.witness["empty_images"], [False, False])

    def test_empty_success_relation_is_coherent_without_becoming_permission(self):
        p = api.Partition(2, (frozenset({0, 1}),))
        empty = api.FiniteRelation(2, 2, frozenset())
        result = api.analyze_quotient(empty, p, p)
        self.assertTrue(result.coherent)
        self.assertFalse(result.quotient.pairs)
        self.assertFalse(api.quotient_composition(empty, empty, p, p, p).pairs)

    def test_relabelled_members_and_class_order_preserve_observed_edges(self):
        p = api.Partition(3, (frozenset({2}), frozenset({0, 1})))
        relation = api.FiniteRelation(3, 3, frozenset({(0, 2), (1, 2), (2, 0), (2, 1)}))
        result = api.analyze_quotient(relation, p, p)
        self.assertTrue(result.coherent)
        self.assertEqual(result.quotient.pairs, frozenset({(1, 0), (0, 1)}))

    def test_complete_disjoint_partitions_and_actual_dimensions_are_required(self):
        bad_blocks = (({0},), ({0, 1}, {1, 2}), ({0, 1, 2}, set()), ({0, 1, 3},))
        for blocks in bad_blocks:
            with self.subTest(blocks=blocks), self.assertRaises(ValueError):
                api.Partition(3, blocks)
        two = api.Partition(2, (frozenset({0, 1}),))
        three = api.Partition(3, (frozenset({0, 1, 2}),))
        relation = api.FiniteRelation(2, 3, frozenset({(0, 2)}))
        with self.assertRaises(ValueError):
            api.analyze_quotient(relation, two, two)
        with self.assertRaises(ValueError):
            api.compose(relation, relation)
        with self.assertRaises(ValueError):
            api.quotient_composition(relation, api.FiniteRelation(3, 2, frozenset()), three, three, two)

    def test_invalid_state_aliases_are_rejected_before_deduplication(self):
        for values in ([0, False, 1], [0, 1, True], [0, 0.0, 1]):
            with self.subTest(values=values), self.assertRaises(ValueError):
                api.Partition(2, (values,))
        with self.assertRaises(ValueError):
            api.FiniteRelation(2, 2, [(0, 0), (False, 0)])
        with self.assertRaises(ValueError):
            api.hausdorff([0, False], {1}, METRIC)
        with self.assertRaises(ValueError):
            api.compose_images(([0, False],), ({0},))

    def test_geometry_rejects_empty_outputs_incompatible_domains_and_float_distances(self):
        for left, right in ((set(), {0}), ({0}, set()), (set(), set())):
            with self.subTest(left=left, right=right), self.assertRaises(ValueError):
                api.hausdorff(left, right, METRIC)
        for first, second in (((set(),), ({0},)), (({0},), (set(),)), (({1},), ({0},))):
            with self.subTest(first=first, second=second), self.assertRaises(ValueError):
                api.compose_images(first, second)
        with self.assertRaises(ValueError):
            api.lipschitz_constant(({0}, {0}), METRIC, METRIC)
        with self.assertRaises(ValueError):
            api.lipschitz_constant(({0}, set(), {0}), METRIC, METRIC)
        with self.assertRaises(ValueError):
            api.hausdorff({0}, {3}, METRIC)
        for metric in (((0.0, 1.0), (1.0, 0.0)), ((False, 1), (1, 0))):
            with self.subTest(metric=metric), self.assertRaises(ValueError):
                api.validate_metric(metric)

    def test_metric_axioms_cannot_be_supplied_by_an_arbitrary_similarity_score(self):
        cosine_dissimilarity = ((0, Fraction(1, 2), Fraction(3, 2)),
                                (Fraction(1, 2), 0, Fraction(1, 2)),
                                (Fraction(3, 2), Fraction(1, 2), 0))
        invalid = (cosine_dissimilarity, ((0, 0), (0, 0)), ((0, 1), (2, 0)),
                   ((0, -1), (-1, 0)), ((1, 1), (1, 0)), ((0, 1), (1,)))
        for metric in invalid:
            with self.subTest(metric=metric), self.assertRaises(ValueError):
                api.validate_metric(metric)
        self.assertEqual(api.validate_metric(((0, 1), (1, 0))),
                         ((Fraction(0), Fraction(1)), (Fraction(1), Fraction(0))))

    def test_useful_zero_and_tight_positive_bounds_survive(self):
        constant = (frozenset({0, 2}),) * 3
        identity = tuple(frozenset({i}) for i in range(3))
        reversal = tuple(frozenset({2 - i}) for i in range(3))
        self.assertEqual(api.lipschitz_constant(constant, METRIC, METRIC), 0)
        self.assertEqual(api.lipschitz_constant(identity, METRIC, METRIC), 1)
        self.assertEqual(api.compose_images(reversal, reversal), identity)
        self.assertEqual(api.lipschitz_constant(api.compose_images(identity, reversal), METRIC, METRIC), 1)
        self.assertEqual(api.lipschitz_constant(({0},), ((0,),), ((0,),)), 0)


if __name__ == "__main__":
    unittest.main()

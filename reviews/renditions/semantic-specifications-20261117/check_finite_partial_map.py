#!/usr/bin/env python3
"""Author-side bounded oracle for Semantic Verification §7.4.

English source revision: 8c7cd3bc1247998cb9554c568da26949da31b749
English content SHA (Git blob): 54832c601597779ea6cef0dd99aa188f27645e9f
Integration scope: knowledge-contract PR124; retained c143 input SHA-256 3f756a1d...

This file adapts the retained local c143 candidate; it is a *new* source file,
not the original evidence or a reproduction of a historical external experiment.
Run normally and under -O; inject --expect-determined 2953 to prove refusal.
The swapped-fibre controls are a new reconstruction of the c148 description,
not a replay of its unavailable original local program or retained output.

No project evaluator is imported. This is NOT native admission / full scientific proof.
"""
from collections import Counter, defaultdict
from itertools import permutations, product
from math import comb
import argparse
import json
import sys

UNDEFINED = -1
VALUES = (*range(4), UNDEFINED)
LABELS = (0, 1)
EXPECTED_TABLE = {
    "4": (8, 0, 504),
    "1 and 3": (128, 1920, 0),
    "2 and 2": (96, 576, 864),
}
EXPECTED_QUERIES = {"determined": 2952, "ambiguous": 4728, "unattained": 512}


def require(yes, context):
    if not yes:
        raise ValueError(context)


def correct_valid(candidate, obs, values):
    """Sound partial maps must be undefined off p(S), and agree where defined."""
    for label, mapped in enumerate(candidate):
        situated = [i for i, a in enumerate(obs) if a == label]
        if not situated:
            if mapped != UNDEFINED:
                return False
        elif mapped != UNDEFINED and any(values[i] != mapped for i in situated):
            return False
    return True


def wrong_valid(candidate, obs, values, variant):
    if variant == "accept_all":
        return True
    if variant == "refuse_all":
        return False
    if variant == "allow_unattained":
        return all(mapped == UNDEFINED or all(values[i] == mapped for i, a in enumerate(obs) if a == label)
                   for label, mapped in enumerate(candidate))
    if variant == "swapped_constant_fibres":
        fibres = [set(values[i] for i, a in enumerate(obs) if a == label) for label in LABELS]
        if all(len(f) == 1 for f in fibres) and fibres[0] != fibres[1]:
            # Both fibres are attained and constant, but the answer values
            # are assigned to the wrong fibre. Undefined remains undefined.
            swapped = (next(iter(fibres[1])), next(iter(fibres[0])))
            return all(mapped == UNDEFINED or mapped == swapped[label]
                       for label, mapped in enumerate(candidate))
        return correct_valid(candidate, obs, values)
    if variant == "cyclic_value_shift":
        # Deliberately wrong answer values: a bijection keeps the aggregate
        # accepted-map count unchanged while changing exact membership.
        for label, mapped in enumerate(candidate):
            situated = [i for i, a in enumerate(obs) if a == label]
            if not situated:
                if mapped != UNDEFINED:
                    return False
            elif mapped != UNDEFINED and any(mapped != (values[i] + 1) % 4 for i in situated):
                return False
        return True
    if variant == "skip_last_situation":
        # Isolate the last-situation omission while preserving the unattained-label rule.
        for label, mapped in enumerate(candidate):
            situated = [i for i, a in enumerate(obs) if a == label]
            if not situated:
                if mapped != UNDEFINED:
                    return False
            elif mapped != UNDEFINED and any(values[i] != mapped for i in situated if i != len(obs) - 1):
                return False
        return True
    raise ValueError("Unknown variant")


def partition_label(obs):
    sizes = sorted((obs.count(0), obs.count(1)))
    return "4" if sizes == [0, 4] else "1 and 3" if sizes == [1, 3] else "2 and 2"


def classify_fibres(obs, values):
    fibres = [set(values[i] for i, a in enumerate(obs) if a == label) for label in LABELS]
    nonempty = [f for f in fibres if f]
    require(bool(nonempty), "S must not be empty")
    if all(len(f) == 1 for f in nonempty):
        return "global"
    if any(len(f) == 1 for f in nonempty):
        return "partial_only"
    return "none"


def closed_form_partial_maps():
    """Independent fibre-size count; no candidate membership predicate is called."""
    def fibre_weight(size):
        # All q^size valuations allow the undefined map; q constants allow one more.
        return 1 if size == 0 else 4 ** size + 4

    terms = [comb(4, k) * fibre_weight(k) * fibre_weight(4 - k)
             for k in range(5)]
    return terms, sum(terms)


def check_swapped_symmetries(truth_tables, candidates):
    """Compare complete directly evaluated tables, not a symmetry shortcut.

    Each case compares both the correct and swapped-fibre predicate. Value
    renaming acts on all four assessment values and each defined map output;
    UNDEFINED is fixed. Observation-label exchange also exchanges map slots.
    These are finite consistency controls, not independent empirical trials.
    """
    candidate_index = {candidate: i for i, candidate in enumerate(candidates)}
    value_permutations = tuple(permutations(range(4)))
    renamed_indices = [tuple(candidate_index[tuple(UNDEFINED if value == UNDEFINED else permutation[value]
                                                  for value in candidate)]
                             for candidate in candidates)
                       for permutation in value_permutations]
    exchanged_indices = tuple(candidate_index[(candidate[1], candidate[0])] for candidate in candidates)
    value_mismatches = {"correct": 0, "swapped_constant_fibres": 0}
    label_mismatches = {"correct": 0, "swapped_constant_fibres": 0}
    value_decisions = 0
    label_decisions = 0
    for (obs, values), (correct, swapped) in truth_tables.items():
        for permutation, indices in zip(value_permutations, renamed_indices):
            renamed_values = tuple(permutation[value] for value in values)
            renamed_correct, renamed_swapped = truth_tables[(obs, renamed_values)]
            for i, renamed_i in enumerate(indices):
                value_decisions += 1
                value_mismatches["correct"] += correct[i] != renamed_correct[renamed_i]
                value_mismatches["swapped_constant_fibres"] += swapped[i] != renamed_swapped[renamed_i]
        exchanged_obs = tuple(1 - label for label in obs)
        exchanged_correct, exchanged_swapped = truth_tables[(exchanged_obs, values)]
        for i, exchanged_i in enumerate(exchanged_indices):
            label_decisions += 1
            label_mismatches["correct"] += correct[i] != exchanged_correct[exchanged_i]
            label_mismatches["swapped_constant_fibres"] += swapped[i] != exchanged_swapped[exchanged_i]

    require(len(truth_tables) == 4096 and len(candidates) == 25, "swapped-fibre truth-table coverage mismatch")
    require(len(value_permutations) == 24 and value_decisions == 2457600,
            "swapped-fibre value-renaming workload mismatch")
    require(label_decisions == 102400, "swapped-fibre label-exchange workload mismatch")
    require(not any(value_mismatches.values()), f"swapped-fibre value-renaming mismatch: {value_mismatches}")
    require(not any(label_mismatches.values()), f"swapped-fibre label-exchange mismatch: {label_mismatches}")

    obs = (0, 0, 0, 1)
    values = (0, 0, 0, 1)
    correct_map = (0, 1)
    swapped_map = (1, 0)
    correct, swapped = truth_tables[(obs, values)]
    good_i, bad_i = candidate_index[correct_map], candidate_index[swapped_map]
    require(correct[good_i] and not swapped[good_i], "swapped-fibre minimal positive witness mismatch")
    require(not correct[bad_i] and swapped[bad_i], "swapped-fibre minimal negative witness mismatch")
    return {
        "provenance": "New reconstruction from c148 description; not an original-program replay",
        "execution": "Complete directly evaluated truth tables; each case compares both predicates",
        "decision_count_unit": "Transformed candidate comparisons per predicate; two predicates checked",
        "assessment_value_permutations": len(value_permutations),
        "value_renaming_decisions": value_decisions,
        "observation_label_exchange_decisions": label_decisions,
        "value_renaming_mismatches": value_mismatches,
        "observation_label_exchange_mismatches": label_mismatches,
        "minimal_witness": {
            "observations": list(obs), "assessments": list(values),
            "correct_map": list(correct_map), "swapped_map": list(swapped_map),
            "correct_accepts_correct_map": correct[good_i],
            "mutant_accepts_correct_map": swapped[good_i],
            "correct_accepts_swapped_map": correct[bad_i],
            "mutant_accepts_swapped_map": swapped[bad_i],
        },
    }


def run(expected_accepted=7272, expected_swapped_false_accept=504):
    class_by_shape = defaultdict(Counter)
    query_counts = Counter()
    accepted_counts = Counter()
    divergences = {k: {"false_accept": 0, "false_reject": 0, "accepted_count": 0, "first_witness": None}
                   for k in ("accept_all", "refuse_all", "allow_unattained", "skip_last_situation",
                             "cyclic_value_shift", "swapped_constant_fibres")}
    maps_tested = 0
    candidate_tests = 0
    candidates = tuple(product(VALUES, repeat=2))
    truth_tables = {}
    affected_profiles = 0
    equal_count_profiles = 0
    for obs in product(LABELS, repeat=4):
        for values in product(range(4), repeat=4):
            maps_tested += 1
            shape = partition_label(obs)
            class_by_shape[shape][classify_fibres(obs, values)] += 1
            fibres = [set(values[i] for i, a in enumerate(obs) if a == label) for label in LABELS]
            oracle_max = tuple(next(iter(f)) if len(f) == 1 else UNDEFINED for f in fibres)
            for f in fibres:
                query_counts["unattained" if len(f) == 0 else "determined" if len(f) == 1 else "ambiguous"] += 1
            accepted = []
            correct_decisions = []
            swapped_decisions = []
            for candidate in candidates:
                candidate_tests += 1
                ok = correct_valid(candidate, obs, values)
                correct_decisions.append(ok)
                if ok:
                    accepted.append(candidate)
                for name, counts in divergences.items():
                    bad = wrong_valid(candidate, obs, values, name)
                    if name == "swapped_constant_fibres":
                        swapped_decisions.append(bad)
                    if bad:
                        counts["accepted_count"] += 1
                    if bad != ok:
                        counts["false_accept" if bad else "false_reject"] += 1
                        if counts["first_witness"] is None:
                            counts["first_witness"] = {"observations": list(obs), "assessments": list(values),
                                                       "partial_map": list(candidate), "correct": ok, "mutant": bad}
            truth_tables[(obs, values)] = (tuple(correct_decisions), tuple(swapped_decisions))
            affected_profiles += correct_decisions != swapped_decisions
            require(len(accepted) == sum(swapped_decisions), "swapped-fibre per-profile cardinality mismatch")
            equal_count_profiles += 1
            accepted_counts[len(accepted)] += 1
            require(oracle_max in accepted, "maximal map missing from accepted candidates")
            require(len(accepted) == 2 ** sum(len(f) == 1 for f in fibres), "valid candidate cardinality mismatch")
            for candidate in accepted:
                require(all(c == UNDEFINED or c == x for c, x in zip(candidate, oracle_max)),
                        "accepted partial map not restriction of unique maximal map")

    require(maps_tested == 4096, "profile population mismatch")
    require(candidate_tests == 102400, "partial-map oracle workload mismatch")
    require(sum(query_counts.values()) == 8192, "query population mismatch")
    for shape, triplet in EXPECTED_TABLE.items():
        got = tuple(class_by_shape[shape][name] for name in ("global", "partial_only", "none"))
        require(got == triplet, f"{shape} classification: {got} != {triplet}")
    require(dict(query_counts) == EXPECTED_QUERIES, "§7.4 query cardinality mismatch")
    closed_form_terms, symbolic_total = closed_form_partial_maps()
    enumerated_total = sum(size * profiles for size, profiles in accepted_counts.items())
    require(symbolic_total == expected_accepted,
            f"closed-form accepted partial-map cardinality mismatch: {symbolic_total} != {expected_accepted}")
    require(enumerated_total == symbolic_total,
            f"enumerated accepted partial-map cardinality mismatch: {enumerated_total} != {symbolic_total}")
    for name, x in divergences.items():
        require(x["false_accept"] + x["false_reject"] > 0, f"Mutation survived: {name}")
    swapped = divergences["swapped_constant_fibres"]
    expected_affected = (2 ** 4 - 2) * 4 * 3
    require(affected_profiles == expected_affected == 168, "swapped-fibre affected-profile count mismatch")
    require(swapped["false_accept"] == expected_swapped_false_accept,
            f"swapped-fibre false-accept count mismatch: {swapped['false_accept']} != {expected_swapped_false_accept}")
    require(swapped["false_reject"] == 504, "swapped-fibre false-reject count mismatch")
    require(swapped["accepted_count"] == symbolic_total, "swapped-fibre total accepted count mismatch")
    require(equal_count_profiles == maps_tested, "swapped-fibre equal-cardinality coverage mismatch")
    # Wrong expected counts above refuse before the more expensive symmetry pass.
    swapped_controls = check_swapped_symmetries(truth_tables, candidates)
    swapped_controls.update({
        "affected_profiles": affected_profiles,
        "affected_profiles_closed_form": expected_affected,
        "profiles_with_equal_accepted_count": equal_count_profiles,
    })
    return {
        "scope": "Finite stipulated model: 4 situations × 2 observation labels × 4 assessment values",
        "counts": {"profiles": maps_tested, "partial_map_candidates": candidate_tests, "label_queries": 8192},
        "by_observation_shape": {s: dict(v) for s, v in sorted(class_by_shape.items())},
        "diagnostic_queries": dict(query_counts),
        "accepted_partial_map_count_distribution": dict(sorted(accepted_counts.items())),
        "accepted_partial_maps_closed_form": {
            "partition_terms": closed_form_terms,
            "symbolic_total": symbolic_total,
            "enumerated_total": enumerated_total,
        },
        "mutants": divergences,
        "swapped_fibre_controls": swapped_controls,
        "decision": "LOCAL_REPRODUCED_NOT_ADMITTED",
        "independent_role_review": "NOT_VERIFIED",
        "runtime_authorized": False,
        "cost": "NOT_MEASURED"
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--expect-determined", type=int, default=2952)
    parser.add_argument("--expect-accepted", type=int, default=7272)
    parser.add_argument("--expect-swapped-false-accept", type=int, default=504)
    args = parser.parse_args()
    EXPECTED_QUERIES["determined"] = args.expect_determined
    try:
        print(json.dumps(run(args.expect_accepted, args.expect_swapped_false_accept),
                         ensure_ascii=False, sort_keys=True, indent=2))
    except ValueError as exc:
        print(f"FINITE_FIBRE_REFUSED: {exc}", file=sys.stderr)
        sys.exit(3)

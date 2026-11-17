#!/usr/bin/env python3
"""Author-side bounded oracle for Semantic Verification §7.4.

English source revision: 8c7cd3bc1247998cb9554c568da26949da31b749
English content SHA (Git blob): 54832c601597779ea6cef0dd99aa188f27645e9f
Integration scope: knowledge-contract PR124; retained c143 input SHA-256 3f756a1d...

This file adapts the retained local c143 candidate; it is a *new* source file,
not the original evidence or a reproduction of a historical external experiment.
Run normally and under -O; inject --expect-determined 2953 to prove refusal.

No project evaluator is imported. This is NOT native admission / full scientific proof.
"""
from collections import Counter, defaultdict
from itertools import product
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


def run(expected_accepted=7272):
    class_by_shape = defaultdict(Counter)
    query_counts = Counter()
    accepted_counts = Counter()
    divergences = {k: {"false_accept": 0, "false_reject": 0, "accepted_count": 0, "first_witness": None}
                   for k in ("accept_all", "refuse_all", "allow_unattained", "skip_last_situation", "cyclic_value_shift")}
    maps_tested = 0
    candidate_tests = 0
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
            for candidate in product(VALUES, repeat=2):
                candidate_tests += 1
                ok = correct_valid(candidate, obs, values)
                if ok:
                    accepted.append(candidate)
                for name, counts in divergences.items():
                    bad = wrong_valid(candidate, obs, values, name)
                    if bad:
                        counts["accepted_count"] += 1
                    if bad != ok:
                        counts["false_accept" if bad else "false_reject"] += 1
                        if counts["first_witness"] is None:
                            counts["first_witness"] = {"observations": list(obs), "assessments": list(values),
                                                       "partial_map": list(candidate), "correct": ok, "mutant": bad}
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
        "decision": "LOCAL_REPRODUCED_NOT_ADMITTED",
        "independent_role_review": "NOT_VERIFIED",
        "runtime_authorized": False,
        "cost": "NOT_MEASURED"
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--expect-determined", type=int, default=2952)
    parser.add_argument("--expect-accepted", type=int, default=7272)
    args = parser.parse_args()
    EXPECTED_QUERIES["determined"] = args.expect_determined
    try:
        print(json.dumps(run(args.expect_accepted), ensure_ascii=False, sort_keys=True, indent=2))
    except ValueError as exc:
        print(f"FINITE_FIBRE_REFUSED: {exc}", file=sys.stderr)
        sys.exit(3)

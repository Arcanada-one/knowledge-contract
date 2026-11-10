#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Exact finite examples for Meaning Geometry; no model, service or external data."""
from __future__ import annotations

from fractions import Fraction as F
from hashlib import sha256
from itertools import product, combinations
from pathlib import Path
import json
import platform


def distance(x: tuple, y: tuple, weights: tuple[F, ...]) -> F:
    if len(x) != len(y) or len(x) != len(weights):
        raise ValueError("coordinate/weight arity mismatch")
    if not weights or any(w <= 0 for w in weights):
        raise ValueError("a nonempty profile with positive weights is required")
    if sum(weights) != 1:
        raise ValueError("weights must sum to one")
    return sum((w for a, b, w in zip(x, y, weights) if a != b), F(0))


def envelope(a: tuple[frozenset, ...], b: tuple[frozenset, ...], weights: tuple[F, ...]) -> tuple[F, F]:
    if len(a) != len(b) or len(a) != len(weights) or not a:
        raise ValueError("nonempty equal-arity profiles are required")
    if any(not s for s in (*a, *b)):
        raise ValueError("empty completion set is inconsistent, not distance zero")
    distance(tuple(0 for _ in a), tuple(0 for _ in b), weights)
    lower = sum((w for s, t, w in zip(a, b, weights) if s.isdisjoint(t)), F(0))
    upper = sum((w for s, t, w in zip(a, b, weights) if not (len(s) == len(t) == 1 and s == t)), F(0))
    return lower, upper


def main() -> int:
    groups: list[dict] = []

    def check(condition: bool, label: str) -> None:
        if not condition:
            raise AssertionError(label)

    def done(name: str, counts: dict, details: dict | None = None) -> None:
        groups.append({"name": name, "counts": counts, "result": "pass", "details": details or {}})

    bits = tuple(product((0, 1), repeat=3))
    objects = tuple((b, tag) for b in bits for tag in ("a", "b"))
    weights = (F(1, 6), F(2, 6), F(3, 6))
    pairs = 0
    for (x, _), (y, _) in product(objects, repeat=2):
        d = distance(x, y, weights)
        check(F(0) <= d <= F(1), "range")
        check(d == distance(y, x, weights), "symmetry")
        check((d == 0) == (x == y), "observational kernel")
        pairs += 1
    triples = 0
    for (x, _), (y, _), (z, _) in product(objects, repeat=3):
        check(distance(x, z, weights) <= distance(x, y, weights) + distance(y, z, weights), "triangle")
        triples += 1
    check(objects[0] != objects[1] and distance(objects[0][0], objects[1][0], weights) == 0, "not object identity")
    done("Observation pseudometric and quotient", {"objects": 16, "observation_classes": 8, "ordered_pairs": pairs, "ordered_triples": triples})

    restrictions = 0
    for k in range(1, 4):
        for indices in combinations(range(3), k):
            total = sum((weights[i] for i in indices), F(0))
            normalized = tuple(weights[i] / total for i in indices)
            for x, y in product(bits, repeat=2):
                restricted = sum((weights[i] for i in indices if x[i] != y[i]), F(0))
                full = distance(x, y, weights)
                norm = distance(tuple(x[i] for i in indices), tuple(y[i] for i in indices), normalized)
                check(restricted <= full and norm == restricted / total and norm <= full / total, "restriction")
                restrictions += 1
    full = distance((0, 0), (1, 0), (F(1, 2), F(1, 2)))
    selected = distance((0,), (1,), (F(1),))
    check(full == F(1, 2) and selected == 1 and selected > full, "renormalization can increase distance")
    done("Restriction and normalization", {"nonempty_coordinate_subsets": 7, "pair_subset_comparisons": restrictions}, {"full": str(full), "normalized_restriction": str(selected)})

    refinement = 0
    alpha = F(1, 3)
    for x, y in product(bits, repeat=2):
        old = distance(x[:2], y[:2], (F(1, 2), F(1, 2)))
        new = distance(x[2:], y[2:], (F(1),))
        refined = distance(x, y, (F(1, 3),) * 3)
        check(refined == (1 - alpha) * old + alpha * new, "refinement identity")
        check(abs(refined - old) <= alpha, "refinement bound")
        check((refined == 0) == (old == 0 and new == 0), "kernel refinement")
        refinement += 1
    done("Observation refinement", {"ordered_pair_comparisons": refinement}, {"alpha": str(alpha)})

    def preserved(obj: tuple) -> tuple:
        b, tag = obj
        return b, "merged-label"
    transform_pairs = 0
    for x, y in product(objects, repeat=2):
        check(distance(x[0], y[0], weights) == distance(preserved(x)[0], preserved(y)[0], weights), "isometry")
        transform_pairs += 1
    unsaturated = {obj for obj in objects if obj[1] == "a"}
    check(objects[0] in unsaturated and objects[1] not in unsaturated and objects[0][0] == objects[1][0], "partial domain boundary")
    fibres: dict[tuple, list] = {}
    for b in bits:
        fibres.setdefault(b[:2], []).append(b)
    for members in fibres.values():
        check(len({m[0] ^ m[1] for m in members}) == 1, "factorable observation")
        check(len({m[2] for m in members}) == 2, "nonfactorable hidden bit")
    done("Transformations and representation collisions", {"isometry_pairs": transform_pairs, "representation_fibres": len(fibres)}, {"domain_saturation_counterexample": True, "hidden_bit_not_recoverable": True})

    choices = (frozenset({0}), frozenset({1}), frozenset({0, 1}))
    domains = tuple(product(choices, repeat=2))
    w2 = (F(1, 2), F(1, 2))
    profiles, actual_pairs = 0, 0
    for a, b in product(domains, repeat=2):
        lo, hi = envelope(a, b, w2)
        values = [distance(x, y, w2) for x in product(*a) for y in product(*b)]
        check(lo == min(values) and hi == max(values), "rectangular completion bounds attained")
        actual_pairs += len(values)
        profiles += 1
    lo, hi = envelope((choices[2],) * 2, (choices[2],) * 2, w2)
    correlated = (((0, 0), (0, 0)), ((1, 1), (1, 1)))
    actual = [distance(x, y, w2) for x, y in correlated]
    check(lo == 0 and hi == 1 and max(actual) == 0, "outer bound need not be attained with joint constraints")
    refused = False
    try:
        envelope((frozenset(),), (choices[0],), (F(1),))
    except ValueError:
        refused = True
    check(refused, "empty completion refusal")
    done("Incomplete observations", {"domain_pairs": profiles, "completion_pair_evaluations": actual_pairs, "joint_constrained_pairs": len(correlated)}, {"independent_unknown_range": [str(lo), str(hi)], "joint_actual_maximum": str(max(actual)), "empty_set_refused": refused})

    x, y, z = (0, 0), (0, 1), (1, 1)
    dxy, dyz, dxz = distance(x, y, w2), distance(y, z, w2), distance(x, z, w2)
    check(dxy <= F(1, 2) and dyz <= F(1, 2) and dxz > F(1, 2), "threshold is not transitive")
    # Exact Gram entries of unit vectors at angles 0, pi/3, 2pi/3.
    cosine_d = (1 - F(1, 2), 1 - F(1, 2), 1 - F(-1, 2))
    check(cosine_d == (F(1, 2), F(1, 2), F(3, 2)), "literal cosine values")
    check(cosine_d[2] > cosine_d[0] + cosine_d[1], "one-minus-cosine violates triangle")
    universe = tuple(product((False, True), repeat=2))
    mf = {v for v in universe if v[0] and v[1]}
    mg = {v for v in universe if v[0]}
    check(mf < mg, "directed entailment and reverse counterexample")
    done("Similarity countermodels", {"threshold_triples": 1, "cosine_triples": 1, "boolean_valuations": 4}, {"threshold_distances": list(map(str, (dxy, dyz, dxz))), "cosine_distances": list(map(str, cosine_d)), "entailment_strictly_directed": True})

    left, right = (0, "allow"), (0, "deny")
    gate_distance = distance(left, right, (F(99, 100), F(1, 100)))
    check(gate_distance == F(1, 100) and gate_distance < F(1, 10), "nearby profiles")
    check(left[1] == "allow" and right[1] != "allow", "different mandatory decision")
    # Literal opposite completions can underlie identical recorded unknown markers.
    recorded = distance(("unknown",), ("unknown",), (F(1),))
    latent = distance((0,), (1,), (F(1),))
    check(recorded == 0 and latent == 1, "record identity is not latent equivalence")
    done("Distance does not grant knowledge or authority", {"gate_counterexamples": 1, "unknown_marker_counterexamples": 1}, {"gate_distance": str(gate_distance), "recorded_unknown_distance": str(recorded), "possible_latent_distance": str(latent)})

    aligned_changes = 0
    for x, y, new_x, new_y in product(bits, repeat=4):
        old_distance = distance(x, y, weights)
        new_distance = distance(new_x, new_y, weights)
        change = distance(x, new_x, weights) + distance(y, new_y, weights)
        check(abs(old_distance - new_distance) <= change, "aligned context-change bound")
        aligned_changes += 1
    done("Aligned context changes", {"ordered_before_after_quadruples": aligned_changes})

    output = {"scope": "finite synthetic checks of the declared observation geometry", "python": platform.python_version(),
              "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
              "groups": groups, "passed_groups": len(groups),
              "limits": "Exact rational examples, not a proof, independent review, semantic annotation validation, embedding benchmark, live-agent test, production execution or publication admission."}
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

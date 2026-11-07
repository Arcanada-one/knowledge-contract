#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Offline finite illustrations, not a scientific-truth or production validator."""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path
import re
import sys

SOURCE_COMMIT = "ea0c30575d56e793fb2875df47126ab3f6dc30ad"
SOURCE_SHA256 = "95acb937c5aa68572eb60ec723d17c628bcd28a778490c09ef6b434ef0f63494"
CANDIDATE_SHA256 = "926b29d227f9c576bc69834ae6f8a72d514fc3b5916bf66c966df5aee5a2ce28"
PROTECTED = {'metadata': '855ec575259c0611abacd17d6b15201cd196a534426efa59e326216e9ce1e897', 'derivations': 'bc750197bf46c794b982d76b6e4534ebd94ccac1063c09d79ce3c561f6296d6b', 'programme_limits': '8005cb8b3550b3c3227e97c3102df6d8bf214ab86fb152819294cbde9c6deabb', 'scope': '5cb4d1d3aa0fc15b89ded13f8ab6ba5b3f458d5650575ce89e7959ddf88b620b', 'references': '3ac9178465114ec5c8de699d14d25b51fe0a62515ff084d8a637a49a7e387987', 'math': 'da125d233b3013797178dec5acb63f7cd6efa09d6df39211d585a12ec6c3893f', 'links': '39e22754bb90b433bbe6e163cac32e1f33f0c8cfbaa8bb95d7db84efea0c9332'}


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def section(text: str, start: str, end: str) -> str:
    first = text.index(start)
    return text[first:text.index(end, first + len(start))]


def protected_views(text: str) -> dict[str, str]:
    return {
        "metadata": text.split("---", 2)[1],
        "derivations": section(text, "## 3.", "## 4."),
        "programme_limits": section(text, "## 7.", "## 8."),
        "scope": section(text, "## 8.", "## 9." if "## 9." in text else "## References"),
        "references": text[text.index("## References"):],
        "math": json.dumps(re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", text, re.S)),
        "links": json.dumps(re.findall(r"\]\(([^)]+)\)|<(https?://[^>]+)>" , text)),
    }


def document_checks(path: Path) -> dict:
    raw = path.read_bytes()
    text = raw.decode("utf-8", errors="strict")
    checks = {name + "_preserved": digest(value.encode()) == PROTECTED[name]
              for name, value in protected_views(text).items()}
    checks.update({
        "exact_candidate": digest(raw) == CANDIDATE_SHA256,
        "utf8_no_bom": not raw.startswith(b"\xef\xbb\xbf"),
        "lf_and_final_newline": b"\r" not in raw and raw.endswith(b"\n"),
        "single_h1": len(re.findall(r"^# ", text, re.M)) == 1,
        "old_numbered_headings_present": all(f"## {n}. " in text for n in range(1, 9)),
        "two_original_propositions": len(re.findall(r"^### Proposition [12]\.", text, re.M)) == 2,
        "two_captioned_tables": len(re.findall(r"^\*\*Table [12]\.", text, re.M)) == 2,
        "conclusion": "## 9. Conclusion" in text,
        "existing_sources_cited": all(f"[{n}]" in text[:text.index("## References")] for n in (1, 2)),
        "scope_refutation_distinction": "satisfy all its premises and falsify its conclusion" in text,
        "outcome_quantifier": "all permitted executions or over a distribution" in text,
        "unresolved_denominator": "not a confidence interval" in text,
        "subject_binding": "cannot silently become a check of another rendering or deployed build" in text,
        "independence_limit": "rather than infer independence from different agent names" in text,
        "no_placeholder": re.search(r"\b(TODO|TBD|FIXME)\b", text) is None,
        "no_mail_envelope": "knowledge-collective-mail/v1" not in text,
    })
    return {"conditions": checks, "passed": sum(checks.values()), "total": len(checks),
            "pass": all(checks.values()), "bytes": len(raw), "sha256": digest(raw)}


def scoped_verdict(domain: frozenset[int], observations: dict[int, bool | None]) -> str:
    """Exact observations in a fixed finite model; no probabilistic inference."""
    if any(observations.get(x) is False for x in domain):
        return "refuted"
    if not domain:
        return "vacuous_domain"
    if all(observations.get(x) is True for x in domain):
        return "finite_model_established"
    if not any(x in observations for x in domain):
        return "not_measured"
    return "incomplete"


def universal_model() -> dict:
    counts: dict[str, int] = {}
    cases = violations = 0
    for dmask, tested, truth in itertools.product(range(16), repeat=3):
        domain = frozenset(i for i in range(4) if dmask & (1 << i))
        observations = {i: bool(truth & (1 << i)) for i in range(4) if tested & (1 << i)}
        verdict = scoped_verdict(domain, observations)
        relevant = dmask & tested
        if relevant & (~truth & 15):
            expected = "refuted"
        elif not dmask:
            expected = "vacuous_domain"
        elif (relevant & truth) == dmask:
            expected = "finite_model_established"
        elif not relevant:
            expected = "not_measured"
        else:
            expected = "incomplete"
        counts[verdict] = counts.get(verdict, 0) + 1
        cases += 1
        violations += verdict != expected
    return {"carrier": "four possible inputs; all domain, tested-set and Boolean truth subsets",
            "assignment_cases": cases, "verdict_counts": counts,
            "violations": violations, "pass": violations == 0}


def deduction_model() -> dict:
    """Two-world truth-set semantics for a fixed four-node acyclic skeleton.

    Two leaves p,q; r from p,q under side1; s from r under side2.
    Rule soundness is checked on both worlds, not taken from a receipt.
    """
    assignments = sound = active_worlds = violations = nonvacuous = 0
    for p, q, r, s, side1, side2 in itertools.product(range(4), repeat=6):
        assignments += 1
        first_antecedent = p & q & side1
        second_antecedent = r & side2
        rules_sound = not (first_antecedent & (~r & 3)) and not (second_antecedent & (~s & 3))
        if not rules_sound:
            continue
        sound += 1
        active = p & q & side1 & side2
        nonvacuous += bool(active)
        for world in (0, 1):
            bit = 1 << world
            if active & bit:
                active_worlds += 1
                violations += not (r & bit and s & bit)
    return {"carrier": "two worlds; six Boolean truth sets; fixed two-leaf, intermediate, conclusion DAG",
            "assignments": assignments, "sound_rule_assignments": sound,
            "sound_nonvacuous_assignments": nonvacuous, "all_premise_world_occurrences": active_worlds,
            "violations": violations, "pass": violations == 0,
            "limit": "one graph shape and fixed finite semantics; no source extraction or arbitrary-DAG implementation tested"}


def admission_model() -> dict:
    """Safety over every outcome of a finite nondeterministic relation."""
    choices = (frozenset(), frozenset({"deny"}), frozenset({"success"}), frozenset({"deny", "success"}))
    cases = safety_passes = no_negative = empty_relations = violations = 0
    for domain_mask, condition_mask in itertools.product(range(8), repeat=2):
        for relation in itertools.product(choices, repeat=3):
            cases += 1
            domain = [i for i in range(3) if domain_mask & (1 << i)]
            negative = [i for i in domain if not condition_mask & (1 << i)]
            witnesses = [i for i in negative if "success" in relation[i]]
            outcome_pairs = [(i, outcome) for i in domain for outcome in relation[i]]
            oracle = not any(not condition_mask & (1 << i) and outcome == "success"
                             for i, outcome in outcome_pairs)
            verdict = not witnesses
            safety_passes += verdict
            no_negative += not negative
            empty_relations += not outcome_pairs
            violations += verdict != oracle
    return {"carrier": "three possible inputs; all domain and condition subsets; all deny/success outcome sets including empty",
            "relation_scope_assignments": cases, "safety_satisfied": safety_passes,
            "assignments_without_negative_input": no_negative, "assignments_without_any_execution": empty_relations,
            "violations": violations, "pass": violations == 0,
            "limit": "absence of forbidden success is not a liveness or usefulness result"}


def ledger(passes: int, failures: int, unresolved: int) -> dict:
    if min(passes, failures, unresolved) < 0:
        raise ValueError("Counts must be nonnegative")
    total = passes + failures + unresolved
    resolved = passes + failures
    return {"total": total, "resolved": resolved,
            "resolved_fraction": Fraction(passes, resolved) if resolved else None,
            "lower": Fraction(passes, total) if total else None,
            "upper": Fraction(passes + unresolved, total) if total else None}


def denominator_model() -> dict:
    assignments = completions = violations = 0
    for p, f, u in itertools.product(range(4), repeat=3):
        assignments += 1
        result = ledger(p, f, u)
        if not result["total"]:
            violations += result["lower"] is not None or result["upper"] is not None
            continue
        rates = [Fraction(p + k, p + f + u) for k in range(u + 1)]
        completions += len(rates)
        violations += result["lower"] != min(rates) or result["upper"] != max(rates)
    example = ledger(2, 1, 1)
    return {"carrier": "passes, failures and unresolved counts each 0..3; every possible resolution count",
            "ledger_assignments": assignments, "completion_counts": completions,
            "example_2_1_1": {k: str(v) if isinstance(v, Fraction) else v for k, v in example.items()},
            "violations": violations, "pass": violations == 0,
            "limit": "fixed-ledger identification bounds, not confidence intervals or population estimates"}


def has_cycle(edges: tuple[tuple[str, str], ...]) -> bool:
    vertices = set(itertools.chain.from_iterable(edges))
    indegree = {v: 0 for v in vertices}
    children = {v: [] for v in vertices}
    for left, right in edges:
        indegree[right] += 1
        children[left].append(right)
    queue = [v for v in vertices if not indegree[v]]
    visited = 0
    while queue:
        v = queue.pop(); visited += 1
        for child in children[v]:
            indegree[child] -= 1
            if not indegree[child]:
                queue.append(child)
    return visited != len(vertices)


def boundary_controls() -> dict:
    d = frozenset({0, 1})
    controls = {
        "in_scope_false_refutes": scoped_verdict(d, {0: True, 1: False}) == "refuted",
        "outside_false_does_not_refute": scoped_verdict(d, {0: True, 1: True, 2: False}) == "finite_model_established",
        "empty_domain_not_operational_success": scoped_verdict(frozenset(), {}) == "vacuous_domain",
        "empty_test_set_not_confirmation": scoped_verdict(d, {}) == "not_measured",
        "unknown_not_pass": scoped_verdict(d, {0: True, 1: None}) == "incomplete",
        "partial_success_not_universal": scoped_verdict(d, {0: True}) == "incomplete",
        "all_finite_cases_pass": scoped_verdict(d, {0: True, 1: True}) == "finite_model_established",
        "unknown_does_not_erase_real_refuter": scoped_verdict(d, {0: False, 1: None}) == "refuted",
        "cycle_not_acyclic_justification": has_cycle((('a', 'b'), ('b', 'a'))),
        "valid_dag_is_acyclic": not has_cycle((('a', 'c'), ('b', 'c'), ('c', 'd'))),
        "cycle_has_no_leaf_foundation": has_cycle((('a', 'a'),)),
        "changed_claim_does_not_repair_original": scoped_verdict(d, {0: True, 1: False}) == "refuted" and scoped_verdict(frozenset({0}), {0: True}) == "finite_model_established",
        "unknown_mandatory_is_not_discharged": not all(x is True for x in (True, None, True)),
        "zero_resolved_denominator_stays_undefined": ledger(0, 0, 3)["resolved_fraction"] is None,
        "zero_total_not_one_hundred_percent": ledger(0, 0, 0)["lower"] is None,
        "fixed_ledger_interval_exact": ledger(2, 1, 1)["lower"] == Fraction(1, 2) and ledger(2, 1, 1)["upper"] == Fraction(3, 4),
    }
    # Each witness compares an explicitly weakened strategy with the scoped rule.
    mutants = {}
    observed = {0: True, 1: True, 2: False}
    mutants["ignore_domain"] = (not all(observed.values())) and scoped_verdict(d, observed) != "refuted"
    observed = {0: True}
    mutants["tested_success_as_universal"] = all(observed.values()) and scoped_verdict(d, observed) == "incomplete"
    observed = {}
    mutants["empty_test_pass"] = all(observed.values()) and scoped_verdict(d, observed) == "not_measured"
    observations = [True, None]
    mutants["drop_unresolved_denominator"] = Fraction(sum(x is True for x in observations), sum(x is not None for x in observations)) != Fraction(sum(x is True for x in observations), len(observations))
    outcomes = ("deny", "success")
    mutants["one_outcome_as_all_executions"] = outcomes[0] != "success" and not all(x != "success" for x in outcomes)
    source, extraction = 5, 50
    produced, shared_oracle, separate_reference = extraction * 2, extraction * 2, source * 2
    mutants["shared_extraction_oracle"] = produced == shared_oracle and produced != separate_reference
    records = [("artifact-v1", "source"), ("artifact-v2", "rendered")]
    mutants["ignore_assessment_subject"] = records[0][0].split('-')[0] == records[1][0].split('-')[0] and records[0] != records[1]
    return {"checks": controls, "passed": sum(controls.values()), "total": len(controls),
            "weakened_strategy_witnesses": mutants, "distinguished": sum(mutants.values()), "strategies": len(mutants),
            "pass": all(controls.values()) and all(mutants.values()),
            "limit": "constructed witnesses, not mutations or incidents of a deployed implementation"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper", type=Path, default=Path(__file__).resolve().parents[1] / "papers/evidence-and-falsification/PAPER.md")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = {"record_type": "evidence-falsification-bounded-checks/1",
                  "source_commit": SOURCE_COMMIT, "source_sha256": SOURCE_SHA256,
                  "document": document_checks(args.paper), "universal_scope": universal_model(),
                  "deduction": deduction_model(), "admission": admission_model(),
                  "denominators": denominator_model(), "controls": boundary_controls()}
        result["pass"] = all(result[k]["pass"] for k in ("document", "universal_scope", "deduction", "admission", "denominators", "controls"))
        result["not_established"] = ["general proof by finite enumeration", "independent evaluation", "actual semantic extraction", "runtime conformance", "statistical or causal superiority", "full repository CI", "merged source or deployed website"]
        output = json.dumps(result, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(output, encoding="utf-8")
        print(output, end="")
        return 0 if result["pass"] else 1
    except (OSError, UnicodeError, ValueError, KeyError) as error:
        print(f"Verification input error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

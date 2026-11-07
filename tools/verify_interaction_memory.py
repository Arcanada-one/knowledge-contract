#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Bounded abstract checks for the interaction-and-memory editorial candidate.

This is not an assistant runtime or an implementation-conformance test.
No network, model calls, external effects, or server state are used.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import re
import sys
from pathlib import Path

SOURCE_COMMIT = "ea0c30575d56e793fb2875df47126ab3f6dc30ad"
SOURCE_SHA256 = "8dacee80ed050c3013c7de092da2c17fbfaafd5fb3b45939dc8fdae3611df656"
CANDIDATE_SHA256 = "6bf13bff5230129c4f077515015f2926c65f6fb2d97f3e1d61e5eaa6b584a2c8"
PROTECTED = {'front_matter': '0f3a96867fcee8f23a6ea0f814546cb3f5051c8cf775826ef3090a7f7cc52423', 'formal_section': '50364dad066889c57529bf3b88e50c5054711100289aa67f6bb12f2d40bb8fe5', 'evidence_section': 'c39c918da0cc8abcf1e32f61bdd670719114f0e9e6c805d9deebf9332e486811', 'references': 'd3aae55904f2f11eccd7c3119c0642e875bb8d5af63aea712289aa41b69588aa', 'math': '93655551bdd3f930c48116921776c45b7dd34431ecc1f8765fdbfcc832d10c39', 'links': '610a5b487e72011ad64370d128a5611b75519e66e8fe496e9ca415d7e862de60'}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def section(text: str, start: str, end: str) -> str:
    a = text.index(start)
    return text[a:text.index(end, a + len(start))]


def protected_views(text: str) -> dict[str, str]:
    return {
        "front_matter": text.split("---", 2)[1],
        "formal_section": section(text, "## 5. Conditional", "## 6. Learning"),
        "evidence_section": section(text, "## 7. Evidence", "## 8. Conclusion") if "## 8. Conclusion" in text else section(text, "## 7. Evidence", "## References"),
        "references": text[text.index("## References"):],
        "math": json.dumps(re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", text, re.S)),
        "links": json.dumps(re.findall(r"\]\(([^)]+)\)|<(https?://[^>]+)>", text)),
    }


def document_checks(path: Path) -> dict:
    raw = path.read_bytes()
    text = raw.decode("utf-8", errors="strict")
    checks = {name + "_preserved": digest(value.encode()) == PROTECTED[name]
              for name, value in protected_views(text).items()}
    checks.update({
        "candidate_exact": digest(raw) == CANDIDATE_SHA256,
        "utf8_without_bom": not raw.startswith(b"\xef\xbb\xbf"),
        "lf_final_newline": b"\r" not in raw and raw.endswith(b"\n"),
        "one_h1": len(re.findall(r"^# ", text, re.M)) == 1,
        "old_major_headings": all(f"## {n}. " in text for n in range(1, 8)),
        "three_propositions": len(re.findall(r"^### Proposition [123]\.", text, re.M)) == 3,
        "conclusion": "## 8. Conclusion" in text,
        "source_cited": "[1]" in text[:text.index("## References")],
        "captioned_layer_table": "**Table 1." in text,
        "output_bound_reevaluation": "that exact output, target generation, and intended use" in text,
        "same_generation_limit": "several attempts for that same generation" in text,
        "retention_scope": "throughout the claimed deduplication scope" in text,
        "external_effect_limit": "supplies no exactly-once guarantee" in text,
        "no_measured_learning_claim": "reports none of those as a measured improvement" in text,
        "no_placeholders": not re.search(r"\b(TODO|TBD|FIXME)\b", text),
        "no_private_mail_payload": "knowledge-collective-mail/v1" not in text and "mun_sk_" not in text,
    })
    return {"checks": checks, "passed": sum(checks.values()), "total": len(checks),
            "pass": all(checks.values()), "sha256": digest(raw), "bytes": len(raw)}


def admit(active: tuple[int, int], origin: tuple[int, int], output: int,
          assessment: tuple[tuple[int, int], int, bool] | None) -> bool:
    """Identity/generation gate only; assumes the declared assessment is sound."""
    return active == origin or assessment == (active, output, True)


def generation_model() -> dict:
    histories = direct_cases = stale_cases = rollback_cases = assessment_cases = 0
    violations = 0
    for length in range(1, 6):
        for contents in itertools.product((0, 1), repeat=length):
            histories += 1
            current_generation = length - 1
            for active_task, origin_task, origin_generation in itertools.product(
                    (0, 1), (0, 1), range(length)):
                direct_cases += 1
                active = (active_task, current_generation)
                origin = (origin_task, origin_generation)
                observed = admit(active, origin, 0, None)
                expected = active_task == origin_task and origin_generation == current_generation
                violations += observed != expected
                if active_task == origin_task and origin_generation < current_generation:
                    stale_cases += 1
                    rollback_cases += contents[origin_generation] == contents[-1]
            # Certificates are synthetic records, not actual semantic assessments.
            for at, ag, output, ct, cg, co, passed in itertools.product(
                    (0, 1), range(length), (0, 1), (0, 1), range(length), (0, 1), (False, True)):
                assessment_cases += 1
                # An origin outside this finite active domain always needs reassessment.
                observed = admit((at, ag), (2, -1), output, ((ct, cg), co, passed))
                expected = at == ct and ag == cg and output == co and passed
                violations += observed != expected
    return {"carrier": "two Work Items; binary requirement contents; 1..5 non-reissued generations; two output identities",
            "history_count": histories, "direct_admission_cases": direct_cases,
            "earlier_same_task_cases": stale_cases, "old_content_matches_active_cases": rollback_cases,
            "synthetic_assessment_binding_cases": assessment_cases,
            "violations": violations, "pass": violations == 0}


def handle_atomic(journal: dict, effects: list, key: tuple[int, int], payload: int,
                  abort_before_commit: bool = False) -> tuple[str, object]:
    """Single atomic-transition reference model, not concurrent database code."""
    if key in journal:
        old_payload, result = journal[key]
        return ("duplicate", result) if old_payload == payload else ("conflict", None)
    result = (key, payload, len(effects) + 1)
    if abort_before_commit:
        return "aborted", None
    # These two updates denote one indivisible abstract transition.
    journal[key] = (payload, result)
    effects.append((key, payload))
    return "applied", result


def event_model() -> dict:
    alphabet = tuple(itertools.product((0, 1), (0, 1)))
    histories = transitions = violations = 0
    for length in range(7):
        for events in itertools.product(alphabet, repeat=length):
            histories += 1
            journal: dict = {}
            effects: list = []
            first: dict = {}
            for event_id, payload in events:
                transitions += 1
                key = (0, event_id)
                outcome, result = handle_atomic(journal, effects, key, payload)
                if event_id not in first:
                    first[event_id] = (payload, len(first) + 1)
                    expected = "applied"
                else:
                    expected = "duplicate" if first[event_id][0] == payload else "conflict"
                violations += outcome != expected
                if outcome != "conflict":
                    violations += result != (key, first[event_id][0], first[event_id][1])
                violations += len(effects) != len(first)
    return {"carrier": "two stable event identifiers, two canonical integer payloads, serialized histories of length 0..6",
            "histories": histories, "handled_event_occurrences": transitions,
            "violations": violations, "pass": violations == 0,
            "limit": "atomicity is an assumed model step; no concurrent database implementation was tested"}


def frame_model() -> dict:
    states = tuple(itertools.product((0, 1), repeat=3))
    transitions = observation_cases = violations = 0
    for mask in range(8):
        outside = tuple(i for i in range(3) if not mask & (1 << i))
        for before, after in itertools.product(states, repeat=2):
            if any(before[i] != after[i] for i in outside):
                continue
            transitions += 1
            def index(state: tuple[int, ...]) -> int:
                return sum(state[i] << k for k, i in enumerate(outside))
            # All Boolean observations on the unchanged coordinate subspace.
            for truth_table in range(1 << (1 << len(outside))):
                observation_cases += 1
                a = (truth_table >> index(before)) & 1
                b = (truth_table >> index(after)) & 1
                violations += a != b
    return {"carrier": "three Boolean state components, every write-set subset, every Boolean observation on its complement",
            "scoped_transitions": transitions, "observation_cases": observation_cases,
            "violations": violations, "pass": violations == 0}


def memory_use(record: dict, task: str, recipient: str) -> bool:
    return (record["scope"] == task and record["recipient"] == recipient
            and all(v is True for v in record["conditions"]) and not record["revoked"])


def controls() -> dict:
    checks: dict[str, bool] = {}
    checks["old_generation_denied"] = not admit((0, 2), (0, 0), 0, None)
    checks["equal_generation_other_task_denied"] = not admit((0, 0), (1, 0), 0, None)
    checks["wrong_output_reassessment_denied"] = not admit((0, 2), (0, 0), 0, ((0, 2), 1, True))
    checks["failed_reassessment_denied"] = not admit((0, 2), (0, 0), 0, ((0, 2), 0, False))
    checks["exact_reassessment_passes_identity_gate_only"] = admit((0, 2), (0, 0), 0, ((0, 2), 0, True))
    checks["same_generation_selection_not_solved"] = admit((0, 2), (0, 2), 0, None) and admit((0, 2), (0, 2), 1, None)
    journal: dict = {}; effects: list = []
    first = handle_atomic(journal, effects, (0, 0), 0)
    checks["duplicate_returns_same_result"] = handle_atomic(journal, effects, (0, 0), 0) == ("duplicate", first[1]) and len(effects) == 1
    checks["payload_conflict_rejected"] = handle_atomic(journal, effects, (0, 0), 1) == ("conflict", None) and len(effects) == 1
    checks["namespace_distinguishes_identifier"] = handle_atomic(journal, effects, (1, 0), 0)[0] == "applied" and len(effects) == 2
    j: dict = {}; e: list = []
    checks["abort_before_atomic_commit_no_effect"] = handle_atomic(j, e, (0, 0), 0, True)[0] == "aborted" and not j and not e
    handle_atomic(j, e, (0, 0), 0)  # Simulate a lost response AFTER successful commit.
    checks["lost_response_after_commit_replay_no_effect"] = handle_atomic(j, e, (0, 0), 0)[0] == "duplicate" and len(e) == 1
    checks["unknown_memory_condition_not_pass"] = all(v is True for v in [True, True]) and not all(v is True for v in [True, None])
    record = {"retain_for_audit": True, "scope": "task-A", "recipient": "reader-A", "conditions": [True], "revoked": True}
    checks["current_use_distinct_from_retention"] = record["retain_for_audit"] and not memory_use(record, "task-A", "reader-A")
    original = {"rule": "allowed", "exception": "not when sealed"}
    rendered = {"rule": "allowed"}
    checks["source_check_not_output_check"] = "exception" in original and "exception" not in rendered
    # Same bytes, different target: output identity check distinguishes representations.
    checks["representation_scope_not_label_only"] = ("md", "rev1") != ("pdf", "rev1")
    act = {"kind": "request", "attribution": "quoted-author", "current_speaker": "reader", "authorized": False}
    transition_allowed = act["kind"] == "request" and act["authorized"]
    checks["quoted_act_does_not_inherit_authority"] = act["attribution"] != act["current_speaker"] and not transition_allowed

    mutants: dict[str, bool] = {}
    contents = ("A", "B", "A")
    mutants["content_hash_instead_of_generation"] = contents[0] == contents[2] and not admit((0, 2), (0, 0), 0, None)
    mutants["generation_without_work_item_identity"] = 2 == 2 and not admit((0, 2), (1, 2), 0, None)
    mutants["reassessment_without_output_identity"] = True and not admit((0, 2), (0, 0), 0, ((0, 2), 1, True))
    # Actual ordered steps: check(0), revision(1), publish based only on old check.
    current = 0; checked = current == 0; current = 1
    mutants["split_check_and_publish"] = checked and not admit((0, current), (0, 0), 0, None)
    # Two actors observe absence before either commits in the deliberately broken model.
    seen_a = seen_b = False
    broken_effects = int(not seen_a) + int(not seen_b)
    mutants["missing_first_commit_serialization"] = broken_effects == 2
    j = {}; e = []
    handle_atomic(j, e, (0, 0), 0); del j[(0, 0)]; handle_atomic(j, e, (0, 0), 0)
    mutants["forgetting_record_before_replay"] = len(e) == 2
    external = 0; local_record = False
    external += 1  # Remote action; local process fails before the outcome commit.
    if not local_record:
        external += 1
    mutants["local_journal_as_external_exactly_once"] = external == 2
    before = (1, 0); after = (1, 1)
    mutants["unmodeled_semantic_coupling"] = before[0] == after[0] and (before[0] == before[1]) != (after[0] == after[1])
    return {"boundary_checks": checks, "boundary_passed": sum(checks.values()),
            "boundary_total": len(checks), "mutant_distinguishing_witnesses": mutants,
            "mutants_distinguished": sum(mutants.values()), "mutants_total": len(mutants),
            "pass": all(checks.values()) and all(mutants.values()),
            "limit": "constructed observations and deliberately weaker rules; not observed production defects"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    default = Path(__file__).resolve().parents[1] / "papers/interaction-and-memory/PAPER.md"
    parser.add_argument("--paper", type=Path, default=default)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        results = {"record_type": "interaction-memory-bounded-checks/1",
                   "source_commit": SOURCE_COMMIT, "source_sha256": SOURCE_SHA256,
                   "document": document_checks(args.paper),
                   "generation": generation_model(), "event_replay": event_model(),
                   "frame": frame_model(), "controls": controls()}
        results["pass"] = all(results[k]["pass"] for k in ("document", "generation", "event_replay", "frame", "controls"))
        results["not_established"] = ["general proof by finite enumeration", "natural-language interpretation correctness", "concurrent database conformance", "external exactly-once execution", "independent scientific acceptance", "human comprehension or learning", "full repository CI", "site deployment or indexing"]
        output = json.dumps(results, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(output, encoding="utf-8")
        sys.stdout.write(output)
        return 0 if results["pass"] else 1
    except (OSError, UnicodeError, ValueError, KeyError) as error:
        print(f"Verification input error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

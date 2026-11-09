#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Corpus controls for tools/assessed_coverage_oracle.py (Layer S, S01–S22).

Each fixture pins exactly one expected verdict and reason set before execution.
A deny-everything stub must fail the positive cases. Mutation targets from the
Agent-Brain packet section 5 are reported as killed / survived / equivalent.
"""
from __future__ import annotations

import copy
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any, Callable

try:
    from tools import assessed_coverage_oracle as aco
except ImportError:  # `cd tools && python3 -B -m unittest test_assessed_coverage_oracle`
    import assessed_coverage_oracle as aco

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "tools" / "assessed_coverage_oracle.py"
FIX_DIR = ROOT / "tools" / "fixtures" / "assessed-coverage"
ORACLE_SOURCE = ROOT / "tools" / "assessed_coverage_oracle.py"

POSITIVE_CASES = ("S01", "S04", "S09", "S16", "S20")

NOT_AN_ASSERTION = (
    b"ImportError",
    b"ModuleNotFoundError",
    b"FileNotFoundError",
    b"SyntaxError",
    b"NameError",
)


def load_fixture(path: Path) -> tuple[dict, dict]:
    document = json.loads(path.read_text(encoding="utf-8"))
    expected = document["expected"]
    working = {key: value for key, value in document.items() if key != "expected"}
    return working, expected


def reason_set(codes: list[str]) -> set[str]:
    return set(codes)


class FixtureCorpusTests(unittest.TestCase):
    def test_every_fixture_matches_pinned_expected(self) -> None:
        paths = sorted(FIX_DIR.glob("*.json"))
        self.assertGreaterEqual(len(paths), 22)
        for path in paths:
            with self.subTest(case=path.name):
                working, expected = load_fixture(path)
                report = aco.evaluate_document(working)
                self.assertEqual(
                    report["closure_verdict"],
                    expected["closure_verdict"],
                    path.name,
                )
                self.assertEqual(
                    report["member_verdicts"],
                    expected["member_verdicts"],
                    path.name,
                )
                self.assertTrue(
                    reason_set(expected["reason_codes"]) <= reason_set(report["reason_codes"]),
                    f"{path.name}: expected reasons {expected['reason_codes']} not in {report['reason_codes']}",
                )
                self.assertEqual(report["effects_authorized"], False)
                self.assertEqual(report["scope"], "synthetic_semantics_only")
                self.assertEqual(
                    report["missing_members"],
                    expected.get("missing_members", []),
                    path.name,
                )
                self.assertEqual(
                    report["unresolved_dependencies"],
                    expected.get("unresolved_dependencies", []),
                    path.name,
                )
                if "addressed_members" in expected:
                    self.assertEqual(
                        report["addressed_members"],
                        expected["addressed_members"],
                        path.name,
                    )

    def test_cli_exit_codes_for_pass_fail_unknown(self) -> None:
        cases = {
            "S01.json": 0,
            "S11.json": 1,
            "S02.json": 3,
        }
        for name, code in cases.items():
            with self.subTest(case=name):
                result = subprocess.run(
                    [sys.executable, "-B", str(CLI), "--input", str(FIX_DIR / name)],
                    cwd=ROOT,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=False,
                )
                self.assertEqual(result.returncode, code, result.stderr)
                report = json.loads(result.stdout)
                self.assertEqual(report["effects_authorized"], False)

    def test_caller_trusted_boolean_is_never_a_premise(self) -> None:
        working, _ = load_fixture(FIX_DIR / "S15a-caller-boolean.json")
        report = aco.evaluate_document(working)
        self.assertEqual(report["closure_verdict"], "unknown")
        self.assertIn("caller_boolean_not_premise", report["reason_codes"])

    def test_reserved_output_keys_in_input_are_rejected(self) -> None:
        working, _ = load_fixture(FIX_DIR / "S01.json")
        working["closure_verdict"] = "pass"
        working["effects_authorized"] = True
        report = aco.evaluate_document(working)
        self.assertEqual(report["closure_verdict"], "fail")
        self.assertIn("reserved_key_in_input", report["reason_codes"])
        self.assertIs(report["effects_authorized"], False)


class DenyEverythingStubTests(unittest.TestCase):
    """A deny-everything implementation must fail the positive cases."""

    def test_deny_everything_fails_positive_cases(self) -> None:
        def deny_everything(_document: dict) -> dict:
            return aco.seal_report(
                aco.outcome(
                    "fail",
                    ["deny_everything"],
                    member_verdicts={},
                    addressed_members=[],
                    missing_members=[],
                    unresolved_dependencies=[],
                    conflicts=[],
                    bindings={},
                )
            )

        for case_id in POSITIVE_CASES:
            path = next(FIX_DIR.glob(f"{case_id}*.json"))
            working, expected = load_fixture(path)
            self.assertEqual(expected["closure_verdict"], "pass", case_id)
            denied = deny_everything(working)
            self.assertNotEqual(
                denied["closure_verdict"],
                expected["closure_verdict"],
                f"deny stub must not satisfy {case_id}",
            )
            self.assertEqual(denied["closure_verdict"], "fail")


def is_assertion_kill(result: subprocess.CompletedProcess) -> bool:
    return (
        result.returncode != 0
        and b"FAIL: " in result.stderr
        and not any(marker in result.stderr for marker in NOT_AN_ASSERTION)
    )


def scratch_run_oracle(source_text: str) -> subprocess.CompletedProcess:
    with tempfile.TemporaryDirectory() as temp:
        scratch = Path(temp)
        tools = scratch / "tools"
        tools.mkdir()
        (tools / "assessed_coverage_oracle.py").write_text(source_text, encoding="utf-8")
        shutil.copytree(FIX_DIR, tools / "fixtures" / "assessed-coverage")
        # Minimal test module: fixture corpus + positives only (fast mutation loop).
        test_src = '''#!/usr/bin/env python3
import json
import unittest
from pathlib import Path
import assessed_coverage_oracle as aco
FIX = Path(__file__).resolve().parent / "fixtures" / "assessed-coverage"
POSITIVE = ("S01", "S04", "S09", "S16", "S20")
class T(unittest.TestCase):
    def test_fixtures(self):
        for path in sorted(FIX.glob("*.json")):
            doc = json.loads(path.read_text())
            exp = doc["expected"]
            working = {k:v for k,v in doc.items() if k != "expected"}
            report = aco.evaluate_document(working)
            self.assertEqual(report["closure_verdict"], exp["closure_verdict"], path.name)
            self.assertEqual(report["member_verdicts"], exp["member_verdicts"], path.name)
            self.assertTrue(set(exp["reason_codes"]) <= set(report["reason_codes"]), path.name)
            self.assertEqual(report["effects_authorized"], False)
    def test_positives_still_pass(self):
        for case in POSITIVE:
            path = next(FIX.glob(case + "*.json"))
            doc = json.loads(path.read_text())
            report = aco.evaluate_document({k:v for k,v in doc.items() if k != "expected"})
            self.assertEqual(report["closure_verdict"], "pass", case)
if __name__ == "__main__":
    unittest.main()
'''
        (tools / "test_assessed_coverage_oracle_scratch.py").write_text(test_src, encoding="utf-8")
        return subprocess.run(
            [
                sys.executable,
                "-B",
                "-m",
                "unittest",
                "-f",
                "test_assessed_coverage_oracle_scratch",
            ],
            cwd=tools,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            check=False,
        )


Mutator = Callable[[str], str]


def _replace_once(source: str, old: str, new: str, name: str) -> str:
    if old not in source:
        raise AssertionError(f"mutant {name} no longer applies; needle missing")
    return source.replace(old, new, 1)


MUTANTS: dict[str, Mutator] = {
    # any-member: treat missing member as discharged if any other passes
    "any-member": lambda s: _replace_once(
        s,
        'member_verdicts[member_id] = MEMBER_MISSING\n            reasons.append(f"missing_assessment:{member_id}")',
        'member_verdicts[member_id] = MEMBER_DISCHARGED\n            reasons.append("any_member_shortcut")',
        "any-member",
    ),
    # any-evidence conjunction: one satisfied component is enough
    "any-evidence-conjunction": lambda s: _replace_once(
        s,
        "for component in components:\n        ok, category, component_reasons, origin = _component_satisfied(",
        "for component in components[:1]:\n        ok, category, component_reasons, origin = _component_satisfied(",
        "any-evidence-conjunction",
    ),
    # one-to-one cardinality: refuse shared evidence across members
    "one-to-one-cardinality": lambda s: _replace_once(
        s,
        "return MEMBER_DISCHARGED, reasons",
        'if len([1 for other in (assessment.get("evidence_refs") or [])]) >= 0:\n'
        '        # Mutant: shared evidence id across members fails even when legitimate.\n'
        '        pass\n'
        '    used = getattr(_evaluate_member_rule, "_used_evidence", set())\n'
        '    refs = set(assessment.get("evidence_refs") or [])\n'
        '    if used.intersection(refs):\n'
        '        return MEMBER_FAIL, reasons + ["one_to_one_cardinality"]\n'
        '    used.update(refs)\n'
        '    _evaluate_member_rule._used_evidence = used\n'
        "    return MEMBER_DISCHARGED, reasons",
        "one-to-one-cardinality",
    ),
    # shared reference: ignore missing member-specific entailment
    "shared-reference": lambda s: _replace_once(
        s,
        "if not isinstance(entailments, list) or not entailments:\n"
        "        return MEMBER_UNKNOWN, reasons + [\"member_entailment_unchecked\"]\n"
        "    matched = False\n"
        "    for entailment in entailments:\n"
        "        if not isinstance(entailment, dict):\n"
        "            continue\n"
        "        if entailment.get(\"member_id\") != member_id:\n"
        "            continue\n"
        "        checked, checked_malformed = bool_field(entailment, \"checked\")\n"
        "        if checked_malformed:\n"
        "            return MEMBER_FAIL, reasons + checked_malformed\n"
        "        if checked is True:\n"
        "            matched = True\n"
        "            break\n"
        "    if not matched:\n"
        "        return MEMBER_UNKNOWN, reasons + [\"member_entailment_unchecked\"]",
        "matched = True  # mutant: shared reference alone discharges",
        "shared-reference",
    ),
    # alias counting: treat aliases as covering every missing mandatory member
    "alias-counting": lambda s: _replace_once(
        s,
        "# Alias records never inflate required-member coverage (S06).\n"
        "    # keep: alias_coverage_guard\n"
        "    _ = assessments  # assessments already reconciled by qualified identity",
        "# Mutant: aliases inflate required-member coverage.\n"
        "    if any(isinstance(a.get(\"member_aliases\"), list) and a.get(\"member_aliases\") for a in assessments):\n"
        "        for member_id in list(member_ids):\n"
        "            if member_verdicts.get(member_id) == MEMBER_MISSING:\n"
        "                member_verdicts[member_id] = MEMBER_DISCHARGED\n"
        "        reasons[:] = [r for r in reasons if not str(r).startswith(\"missing_assessment:\")]\n"
        "        missing_members[:] = []",
        "alias-counting",
    ),
    # producer optional: suppress required-profile gap
    "producer-optional": lambda s: _replace_once(
        s,
        'if profile not in interpretable:\n'
        '                # Producer optional flag cannot suppress a trusted required profile.\n'
        '                reasons.append("required_profile_uninterpretable")',
        'if profile not in interpretable:\n'
        '                if inventory.get("producer_marks_optional") is True:\n'
        '                    continue\n'
        '                reasons.append("required_profile_uninterpretable")',
        "producer-optional",
    ),
    # missing-as-empty: absent requirements become empty justified set
    "missing-as-empty": lambda s: _replace_once(
        s,
        'if "requirements" not in document:\n        return None, ["mandatory_inventory_absent"], "absent"',
        'if "requirements" not in document:\n        return {"trusted_test_premise": True, "revision": "inferred", "members": [], "empty_set_justification": "inferred"}, [], "empty_justified"',
        "missing-as-empty",
    ),
    # skipped binding: ignore binding mismatches
    "skipped-binding": lambda s: _replace_once(
        s,
        "if not isinstance(assessment_binding, dict):\n"
        "        return UNKNOWN, [\"assessment_binding_missing\"]\n"
        "    if not bindings_equal(assessment_binding, binding_b0):\n"
        "        return FAIL, [\"binding_mismatch\"]",
        "if False and not isinstance(assessment_binding, dict):\n"
        "        return UNKNOWN, [\"assessment_binding_missing\"]\n"
        "    if False and not bindings_equal(assessment_binding, binding_b0):\n"
        "        return FAIL, [\"binding_mismatch\"]",
        "skipped-binding",
    ),
    # missing binding treated as discharged (P01 revert)
    "missing-binding-ok": lambda s: _replace_once(
        s,
        "if not isinstance(assessment_binding, dict):\n"
        "        return UNKNOWN, [\"assessment_binding_missing\"]\n"
        "    if not bindings_equal(assessment_binding, binding_b0):\n"
        "        return FAIL, [\"binding_mismatch\"]",
        "if not isinstance(assessment_binding, dict):\n"
        "        return None, []  # mutant: absent binding is fine\n"
        "    if not bindings_equal(assessment_binding, binding_b0):\n"
        "        return FAIL, [\"binding_mismatch\"]",
        "missing-binding-ok",
    ),
    # skip revision pinning (P05 revert)
    "skip-revision-pin": lambda s: _replace_once(
        s,
        "if pin_reasons:\n"
        "        return outcome(\n"
        "            UNKNOWN,\n"
        "            pin_reasons,\n",
        "if False and pin_reasons:\n"
        "        return outcome(\n"
        "            UNKNOWN,\n"
        "            pin_reasons,\n",
        "skip-revision-pin",
    ),
    # ignore malformed reason classification (P06/P07 revert)
    "ignore-malformed-reason": lambda s: _replace_once(
        s,
        'FAIL_REASON_CODES = frozenset({\n    "malformed_input",',
        'FAIL_REASON_CODES = frozenset({\n    "malformed_input_disabled_for_mutant",',
        "ignore-malformed-reason",
    ),
    # skip NA evidence resolution (P08 revert)
    "skip-na-evidence-resolve": lambda s: _replace_once(
        s,
        "evidence = evidence_index.get(evidence_id)\n"
        "    if evidence is None:\n"
        "        return MEMBER_UNKNOWN, [\"na_evidence_missing\"]\n"
        "    category, evidence_reasons = _evidence_current_use(\n"
        "        evidence,\n"
        "        evaluation_time,\n"
        "        expected_reviewer_revision,\n"
        "        expected_rule_revision,\n"
        "    )\n"
        "    if category is not None:\n"
        "        return (MEMBER_FAIL if category == FAIL else MEMBER_UNKNOWN), evidence_reasons",
        "evidence = evidence_index.get(evidence_id)\n"
        "    if False and evidence is None:\n"
        "        return MEMBER_UNKNOWN, [\"na_evidence_missing\"]\n"
        "    category, evidence_reasons = None, []\n"
        "    if False:\n"
        "        category, evidence_reasons = _evidence_current_use(\n"
        "            evidence,\n"
        "            evaluation_time,\n"
        "            expected_reviewer_revision,\n"
        "            expected_rule_revision,\n"
        "        )\n"
        "    if category is not None:\n"
        "        return (MEMBER_FAIL if category == FAIL else MEMBER_UNKNOWN), evidence_reasons",
        "skip-na-evidence-resolve",
    ),
    # skip trusted inventory string-list shape (P09/P10 revert)
    "skip-profile-shape": lambda s: _replace_once(
        s,
        "if not isinstance(value, list) or not all(is_non_empty_string(item) for item in value):\n"
        "        return None, [\"malformed_input\"]\n"
        "    return list(value), []",
        "if not isinstance(value, list):\n"
        "        return [], []  # mutant: ignore malformed shape\n"
        "    return [item for item in value if is_non_empty_string(item)], []",
        "skip-profile-shape",
    ),
    # absent current-use signals read as clean (P11 revert)
    "skip-current-use-signals": lambda s: _replace_once(
        s,
        "# Absent current-use signals are not clean (P11).\n"
        "    if (\n"
        "        \"valid_from\" not in provenance\n"
        "        or \"valid_to\" not in provenance\n"
        "        or \"service_status\" not in provenance\n"
        "        or \"revoked_for_required_use\" not in provenance\n"
        "    ):\n"
        "        return UNKNOWN, [\"evidence_current_use_unverified\"]\n"
        "    service = provenance.get(\"service_status\")\n"
        "    if service == \"denied\":\n"
        "        return FAIL, [\"required_use_denied\"]\n"
        "    if service == \"unavailable\":\n"
        "        return UNKNOWN, [\"evidence_service_unavailable\"]\n"
        "    if service != \"available\":\n"
        "        return UNKNOWN, [\"evidence_current_use_unverified\"]\n"
        "    if provenance.get(\"revoked_for_required_use\") is True:\n"
        "        return FAIL, [\"evidence_revoked_for_required_use\"]\n"
        "    if not isinstance(provenance.get(\"revoked_for_required_use\"), bool):\n"
        "        return UNKNOWN, [\"evidence_current_use_unverified\"]",
        "# Mutant: absent current-use signals read as clean/available.\n"
        "    service = provenance.get(\"service_status\") or \"available\"\n"
        "    if service == \"denied\":\n"
        "        return FAIL, [\"required_use_denied\"]\n"
        "    if service == \"unavailable\":\n"
        "        return UNKNOWN, [\"evidence_service_unavailable\"]\n"
        "    if False and service != \"available\":\n"
        "        return UNKNOWN, [\"evidence_current_use_unverified\"]\n"
        "    if provenance.get(\"revoked_for_required_use\") is True:\n"
        "        return FAIL, [\"evidence_revoked_for_required_use\"]",
        "skip-current-use-signals",
    ),
    # lexicographic time compare (P13 revert)
    "lex-time-compare": lambda s: _replace_once(
        s,
        "eval_dt = parse_rfc3339(evaluation_time)\n"
        "    from_dt = parse_rfc3339(valid_from)\n"
        "    to_dt = parse_rfc3339(valid_to)\n"
        "    if eval_dt is None or from_dt is None or to_dt is None:\n"
        "        return UNKNOWN, [\"time_unparsable\"]\n"
        "    if eval_dt < from_dt or eval_dt > to_dt:\n"
        "        return FAIL, [\"evidence_validity_excludes_evaluation_time\"]",
        "if is_non_empty_string(valid_from) and is_non_empty_string(evaluation_time):\n"
        "        if evaluation_time < valid_from:\n"
        "            return FAIL, [\"evidence_validity_excludes_evaluation_time\"]\n"
        "    if is_non_empty_string(valid_to) and is_non_empty_string(evaluation_time):\n"
        "        if evaluation_time > valid_to:\n"
        "            return FAIL, [\"evidence_validity_excludes_evaluation_time\"]\n"
        "    if False:\n"
        "        return UNKNOWN, [\"time_unparsable\"]",
        "lex-time-compare",
    ),
    # first-wins assessment order (P14a revert)
    "first-wins-assessment": lambda s: _replace_once(
        s,
        "candidates_by_member.setdefault(qualified, []).append(assessment)",
        "if qualified not in candidates_by_member:\n"
        "            candidates_by_member[qualified] = [assessment]  # mutant: first-wins",
        "first-wins-assessment",
    ),
    # digest/revision-only evidence identity (P19 revert)
    "digest-only-evidence-identity": lambda s: _replace_once(
        s,
        "# Same id with any differing field is an identity conflict (S18/P19).\n"
        "            # Byte-identical duplicates may collapse. Conflicting identities are\n"
        "            # unusable: drop the id so order cannot choose a winner.\n"
        "            prior = index[evidence_id]\n"
        "            if prior != record:\n"
        "                reasons.append(\"evidence_identity_conflict\")\n"
        "                del index[evidence_id]\n"
        "                conflicted.add(evidence_id)",
        "prior = index[evidence_id]\n"
        "            if (\n"
        "                prior.get(\"immutable_bytes_digest\") != record.get(\"immutable_bytes_digest\")\n"
        "                or prior.get(\"revision_claim\") != record.get(\"revision_claim\")\n"
        "            ):\n"
        "                reasons.append(\"evidence_identity_conflict\")\n"
        "                # mutant: keep first record; digest/revision-only conflict",
        "digest-only-evidence-identity",
    ),
    # ignored revocation
    "ignored-revocation": lambda s: _replace_once(
        s,
        'if provenance.get("revoked_for_required_use") is True:\n        return FAIL, ["evidence_revoked_for_required_use"]',
        'if False and provenance.get("revoked_for_required_use") is True:\n        return FAIL, ["evidence_revoked_for_required_use"]',
        "ignored-revocation",
    ),
    # caller boolean trusted
    "caller-boolean": lambda s: _replace_once(
        s,
        "# keep: caller_boolean_guard — a bare trusted=true is never a premise (S15a).\n"
        "    caller_boolean = (\n"
        "        isinstance(provenance, dict)\n"
        "        and provenance.get(\"trusted\") is True\n"
        "        and not _mark_trusted(assessment)\n"
        "    )\n"
        "    if caller_boolean:\n"
        "        return UNKNOWN, [\"caller_boolean_not_premise\"]\n"
        "    if not _mark_trusted(assessment):\n"
        "        return UNKNOWN, [\"assessment_not_trusted_premise\"]",
        "# Mutant: honor caller trusted=true as a premise.\n"
        "    if isinstance(provenance, dict) and provenance.get(\"trusted\") is True:\n"
        "        pass\n"
        "    elif not _mark_trusted(assessment):\n"
        "        return UNKNOWN, [\"assessment_not_trusted_premise\"]",
        "caller-boolean",
    ),
    # ungrounded NA
    "ungrounded-na": lambda s: _replace_once(
        s,
        'evidence_id = decision.get("evidence_id")\n'
        '    if not is_non_empty_string(evidence_id):\n'
        '        return MEMBER_UNKNOWN, ["na_evidence_missing"]\n'
        '    evidence = evidence_index.get(evidence_id)\n'
        '    if evidence is None:\n'
        '        return MEMBER_UNKNOWN, ["na_evidence_missing"]\n'
        '    category, evidence_reasons = _evidence_current_use(\n'
        '        evidence,\n'
        '        evaluation_time,\n'
        '        expected_reviewer_revision,\n'
        '        expected_rule_revision,\n'
        '    )\n'
        '    if category is not None:\n'
        '        return (MEMBER_FAIL if category == FAIL else MEMBER_UNKNOWN), evidence_reasons',
        '# Mutant: accept ungrounded NA without resolving evidence.\n'
        '    evidence_id = decision.get("evidence_id")\n'
        '    _ = (evidence_id, evidence_index, evaluation_time)\n'
        '    if False:\n'
        '        return MEMBER_UNKNOWN, ["na_evidence_missing"]',
        "ungrounded-na",
    ),
    # last-write dedup conflicting identities
    "last-write-dedup": lambda s: _replace_once(
        s,
        "if assessment_id in index:\n"
        "            # Same id with any differing field is an identity conflict (F1).\n"
        "            # Claimed digest/revision equality does not prove content equality.\n"
        "            # Byte-identical duplicates may collapse. Conflicting identities are\n"
        "            # unusable: drop the id so order cannot choose a winner.\n"
        "            prior = index[assessment_id]\n"
        "            if prior != assessment:\n"
        "                reasons.append(\"assessment_identity_conflict\")\n"
        "                del index[assessment_id]\n"
        "                conflicted.add(assessment_id)\n"
        "            continue\n"
        "        index[assessment_id] = assessment",
        "if assessment_id in index:\n"
        "            # mutant: last write wins, no conflict reason\n"
        "            index[assessment_id] = assessment\n"
        "            continue\n"
        "        index[assessment_id] = assessment",
        "last-write-dedup",
    ),
    # F1 revert: digest/revision-only assessment identity (pre-round-5)
    "digest-only-assessment-identity": lambda s: _replace_once(
        s,
        "if assessment_id in index:\n"
        "            # Same id with any differing field is an identity conflict (F1).\n"
        "            # Claimed digest/revision equality does not prove content equality.\n"
        "            # Byte-identical duplicates may collapse. Conflicting identities are\n"
        "            # unusable: drop the id so order cannot choose a winner.\n"
        "            prior = index[assessment_id]\n"
        "            if prior != assessment:\n"
        "                reasons.append(\"assessment_identity_conflict\")\n"
        "                del index[assessment_id]\n"
        "                conflicted.add(assessment_id)\n"
        "            continue\n"
        "        index[assessment_id] = assessment\n"
        "    return list(index.values()), reasons",
        "if assessment_id in index:\n"
        "            prior = index[assessment_id]\n"
        "            if (\n"
        "                prior.get(\"immutable_bytes_digest\") != assessment.get(\"immutable_bytes_digest\")\n"
        "                or prior.get(\"revision_claim\") != assessment.get(\"revision_claim\")\n"
        "            ):\n"
        "                reasons.append(\"assessment_identity_conflict\")\n"
        "                # mutant: keep first; digest/revision-only; still append both below\n"
        "                continue\n"
        "        index[assessment_id] = assessment\n"
        "    # mutant: rebuild out including duplicates with matching claimed digests\n"
        "    out = []\n"
        "    seen = set()\n"
        "    for assessment in assessments if isinstance(assessments, list) else []:\n"
        "        if not isinstance(assessment, dict):\n"
        "            continue\n"
        "        aid = assessment.get(\"assessment_id\")\n"
        "        if aid in conflicted:\n"
        "            continue\n"
        "        if aid in index:\n"
        "            out.append(assessment)\n"
        "    return out, reasons",
        "digest-only-assessment-identity",
    ),
    # F2 revert: coincident support times ignore established applicability violation
    "skip-applicability-coincident": lambda s: _replace_once(
        s,
        "common = set.intersection(*(times_by_member[member_id] for member_id in times_by_member))\n"
        "    if common:\n"
        "        if applicability_fail:\n"
        "            return False, [\"applicability_violation_established\"]\n"
        "        return True, []\n"
        "    # No single snapshot covers every assessment-discharged member.\n"
        "    if applicability_fail:\n"
        "        return False, [\n"
        "            \"temporal_support_incompatible_fail\",\n"
        "            \"applicability_violation_established\",\n"
        "        ]\n"
        "    return False, [\"temporal_support_incoherent\"]",
        "common = set.intersection(*(times_by_member[member_id] for member_id in times_by_member))\n"
        "    if common:\n"
        "        return True, []  # mutant: ignore established applicability when times coincide\n"
        "    # No single snapshot covers every assessment-discharged member.\n"
        "    if applicability_fail:\n"
        "        return False, [\"temporal_support_incompatible_fail\"]\n"
        "    return False, [\"temporal_support_incoherent\"]",
        "skip-applicability-coincident",
    ),
    # temporal union
    "temporal-union": lambda s: _replace_once(
        s,
        "common = set.intersection(*(times_by_member[member_id] for member_id in times_by_member))\n"
        "    if common:\n"
        "        if applicability_fail:\n"
        "            return False, [\"applicability_violation_established\"]\n"
        "        return True, []\n"
        "    # No single snapshot covers every assessment-discharged member.\n"
        "    if applicability_fail:\n"
        "        return False, [\n"
        "            \"temporal_support_incompatible_fail\",\n"
        "            \"applicability_violation_established\",\n"
        "        ]\n"
        "    return False, [\"temporal_support_incoherent\"]",
        "common = set.intersection(*(times_by_member[member_id] for member_id in times_by_member))\n"
        "    if True:  # mutant: union incompatible historical supports\n"
        "        return True, []\n"
        "    return False, [\"temporal_support_incoherent\"]",
        "temporal-union",
    ),
    # harmless-addition: ignore unresolved conflicts
    "harmless-addition": lambda s: _replace_once(
        s,
        'if record["established"]:\n            has_fail = True\n            reasons.append("mandatory_conflict_established")\n        else:\n            has_unknown = True\n            reasons.append("mandatory_conflict_unresolved")',
        'if False and record["established"]:\n            has_fail = True\n            reasons.append("mandatory_conflict_established")\n        else:\n            if False:\n                has_unknown = True\n                reasons.append("mandatory_conflict_unresolved")',
        "harmless-addition",
    ),
    # copies-as-independent
    "copies-as-independent": lambda s: _replace_once(
        s,
        "if len(set(origins)) != len(origins):\n            # Sameness established via equal origin_id.\n            return MEMBER_FAIL, reasons + [\"independence_same_origin\"]",
        "if False and len(set(origins)) != len(origins):\n            return MEMBER_FAIL, reasons + [\"independence_same_origin\"]",
        "copies-as-independent",
    ),
    # Q1 revert: temporal coherence uses only the first candidate per member
    "temporal-first-candidate": lambda s: _replace_once(
        s,
        "coherent, temporal_reasons = _support_times_coherent(\n"
        "        trusted_temporal_candidates, assessment_discharged\n"
        "    )",
        "first_only = {\n"
        "        mid: ([cands[0]] if cands else [])\n"
        "        for mid, cands in trusted_temporal_candidates.items()\n"
        "    }\n"
        "    coherent, temporal_reasons = _support_times_coherent(first_only, assessment_discharged)",
        "temporal-first-candidate",
    ),
    # Q6 revert: absent/mixed support_time treated as coherent
    "skip-support-time-required": lambda s: _replace_once(
        s,
        "# Trusted established applicability violation is FAIL on its own (F2/F3):\n"
        "    # timestamp intersection cannot negate it; it dominates missing-support UNKNOWN.\n"
        "    # A valid authorised NA for the same member also cannot erase it.\n"
        "    if applicability_fail and missing_support:\n"
        "        return False, [\"applicability_violation_established\"]\n"
        "    # Any discharging assessment without demonstrated support time ⇒ unverified\n"
        "    # (covers all-absent and mixed missing/present; order-invariant).\n"
        "    if missing_support:\n"
        "        return False, [\"temporal_support_unverified\"]\n"
        "    if not times_by_member:\n"
        "        if applicability_fail:\n"
        "            return False, [\"applicability_violation_established\"]\n"
        "        return True, []",
        "# Mutant: absent/mixed support_time is treated as coherent.\n"
        "    if not times_by_member:\n"
        "        return True, []",
        "skip-support-time-required",
    ),
    # F3 revert: established-violation scanned only for assessment-discharged members
    "skip-applicability-na-mask": lambda s: _replace_once(
        s,
        "# F3: scan established-violation over every admitted trusted B0-bound\n"
        "    # assessment, not only over assessment-discharged members.\n"
        "    for _member_id, candidates in trusted_candidates_by_member.items():\n"
        "        for assessment in candidates:\n"
        "            flag, flag_malformed = bool_field(\n"
        "                assessment, \"applicability_violation_established\"\n"
        "            )\n"
        "            if flag_malformed:\n"
        "                return False, flag_malformed\n"
        "            if flag is True:\n"
        "                applicability_fail = True\n"
        "    for member_id in assessment_discharged_members:\n"
        "        candidates = trusted_candidates_by_member.get(member_id) or []\n"
        "        times: set[datetime] = set()\n"
        "        for assessment in candidates:\n"
        "            support_time = assessment.get(\"support_time\")\n"
        "            if not is_non_empty_string(support_time):\n"
        "                continue\n"
        "            parsed = parse_rfc3339(support_time)\n"
        "            if parsed is None:\n"
        "                return False, [\"time_unparsable\"]\n"
        "            times.add(parsed)\n"
        "        if not times:\n"
        "            missing_support = True\n"
        "        else:\n"
        "            times_by_member[member_id] = times",
        "# Mutant: only assessment-discharged members expose established-violation (NA masks).\n"
        "    for member_id in assessment_discharged_members:\n"
        "        candidates = trusted_candidates_by_member.get(member_id) or []\n"
        "        times: set[datetime] = set()\n"
        "        for assessment in candidates:\n"
        "            flag, flag_malformed = bool_field(\n"
        "                assessment, \"applicability_violation_established\"\n"
        "            )\n"
        "            if flag_malformed:\n"
        "                return False, flag_malformed\n"
        "            if flag is True:\n"
        "                applicability_fail = True\n"
        "            support_time = assessment.get(\"support_time\")\n"
        "            if not is_non_empty_string(support_time):\n"
        "                continue\n"
        "            parsed = parse_rfc3339(support_time)\n"
        "            if parsed is None:\n"
        "                return False, [\"time_unparsable\"]\n"
        "            times.add(parsed)\n"
        "        if not times:\n"
        "            missing_support = True\n"
        "        else:\n"
        "            times_by_member[member_id] = times",
        "skip-applicability-na-mask",
    ),
    # Q8 revert: NA short-circuits before assessment integrity
    "na-before-assessments": lambda s: _replace_once(
        s,
        "# Q8: evaluate every submitted assessment candidate for integrity\n"
        "        # BEFORE the NA discharge decision. A valid NA does not sanitize a\n"
        "        # wrong-bound / failing companion in the same scoped collection.\n"
        "        candidates = candidates_by_member.get(member_id) or []\n"
        "        definition = member_defs.get(member_id)\n"
        "        saw_binding_mismatch = False\n"
        "        saw_member_fail = False\n"
        "        saw_member_unknown = False\n"
        "        saw_discharged = False\n"
        "        for assessment in candidates:",
        "# Mutant: NA short-circuits before assessment integrity (pre-Q8).\n"
        "        na_verdict_early, na_reasons_early = _na_decision_for(\n"
        "            member_id,\n"
        "            document,\n"
        "            binding_b0,\n"
        "            evidence_index,\n"
        "            evaluation_time,\n"
        "            expected_reviewer_revision,\n"
        "            expected_rule_revision,\n"
        "        )\n"
        "        if na_verdict_early is not None:\n"
        "            member_verdicts[member_id] = na_verdict_early\n"
        "            reasons.extend(na_reasons_early)\n"
        "            continue\n"
        "        candidates = candidates_by_member.get(member_id) or []\n"
        "        definition = member_defs.get(member_id)\n"
        "        saw_binding_mismatch = False\n"
        "        saw_member_fail = False\n"
        "        saw_member_unknown = False\n"
        "        saw_discharged = False\n"
        "        for assessment in candidates:",
        "na-before-assessments",
    ),
    # Q2 revert: first matching NA decision wins
    "na-first-match": lambda s: _replace_once(
        s,
        "saw_fail = False\n"
        "    saw_unknown = False\n"
        "    saw_na = False\n"
        "    reasons: list[str] = []\n"
        "    matched = False\n"
        "    for decision in decisions:\n"
        "        if not isinstance(decision, dict):\n"
        "            continue\n"
        "        if decision.get(\"member_id\") != member_id:\n"
        "            continue\n"
        "        matched = True\n"
        "        verdict, decision_reasons = _evaluate_one_na_decision(\n"
        "            decision,\n"
        "            binding_b0,\n"
        "            evidence_index,\n"
        "            evaluation_time,\n"
        "            expected_reviewer_revision,\n"
        "            expected_rule_revision,\n"
        "        )\n"
        "        reasons.extend(decision_reasons)\n"
        "        if verdict == MEMBER_FAIL:\n"
        "            saw_fail = True\n"
        "        elif verdict == MEMBER_UNKNOWN:\n"
        "            saw_unknown = True\n"
        "        elif verdict == MEMBER_NA:\n"
        "            saw_na = True\n"
        "    if not matched:\n"
        "        return None, []\n"
        "    if saw_fail:\n"
        "        return MEMBER_FAIL, reasons\n"
        "    if saw_unknown:\n"
        "        return MEMBER_UNKNOWN, reasons\n"
        "    if saw_na:\n"
        "        return MEMBER_NA, reasons\n"
        "    return MEMBER_UNKNOWN, reasons or [\"na_scope_unverified\"]",
        "for decision in decisions:\n"
        "        if not isinstance(decision, dict):\n"
        "            continue\n"
        "        if decision.get(\"member_id\") != member_id:\n"
        "            continue\n"
        "        return _evaluate_one_na_decision(\n"
        "            decision,\n"
        "            binding_b0,\n"
        "            evidence_index,\n"
        "            evaluation_time,\n"
        "            expected_reviewer_revision,\n"
        "            expected_rule_revision,\n"
        "        )\n"
        "    return None, []",
        "na-first-match",
    ),
    # Q4 revert: accept unmarked member rule definitions
    "skip-member-trust-mark": lambda s: _replace_once(
        s,
        "# Spec §2: each member keeps its exact rule from the trusted snapshot.\n"
        "        if not _mark_trusted(definition):\n"
        "            if definition.get(\"trusted\") is True:\n"
        "                reasons.append(\"caller_boolean_not_premise\")\n"
        "            else:\n"
        "                reasons.append(\"member_rule_not_trusted_premise\")\n"
        "            continue",
        "# Mutant: unmarked member rules are accepted.\n"
        "        if False and not _mark_trusted(definition):\n"
        "            reasons.append(\"member_rule_not_trusted_premise\")\n"
        "            continue",
        "skip-member-trust-mark",
    ),
    # Q5 revert: non-bool require_independent_origins treated as not required
    "string-independence-ok": lambda s: _replace_once(
        _replace_once(
            s,
            "# Present non-bool independence flag is a malformed trusted rule (Q5).\n"
            "        _, indep_malformed = bool_field(rule, \"require_independent_origins\")\n"
            "        if indep_malformed:\n"
            "            reasons.extend(indep_malformed)\n"
            "            continue\n"
            "        out[member_id] = definition",
            "# Mutant: ignore non-bool independence flag at definition load.\n"
            "        out[member_id] = definition",
            "string-independence-ok/defs",
        ),
        "require_independent, indep_malformed = bool_field(rule, \"require_independent_origins\")\n"
        "    if indep_malformed:\n"
        "        return MEMBER_FAIL, reasons + indep_malformed\n"
        "    if require_independent is True:",
        "if rule.get(\"require_independent_origins\") is True:  # mutant: string \"true\" disables check",
        "string-independence-ok/eval",
    ),
    # Q7 revert: absent NA binding is fine
    "skip-na-binding-required": lambda s: _replace_once(
        s,
        "# NA binding must be an object matching B0 (Q7); absent/non-object ⇒ unknown.\n"
        "    decision_binding = decision.get(\"binding\")\n"
        "    if not isinstance(decision_binding, dict):\n"
        "        return MEMBER_UNKNOWN, [\"na_binding_missing\"]\n"
        "    if not bindings_equal(decision_binding, binding_b0):\n"
        "        return MEMBER_FAIL, [\"na_scope_mismatch\"]",
        "# Mutant: absent NA binding is fine; only mismatch fails.\n"
        "    decision_binding = decision.get(\"binding\")\n"
        "    if decision_binding is not None and not bindings_equal(decision_binding, binding_b0):\n"
        "        return MEMBER_FAIL, [\"na_scope_mismatch\"]",
        "skip-na-binding-required",
    ),
}


class MutationHarnessTests(unittest.TestCase):
    def test_unmutated_baseline_passes(self) -> None:
        source = ORACLE_SOURCE.read_text(encoding="utf-8")
        result = scratch_run_oracle(source)
        self.assertEqual(
            result.returncode,
            0,
            "baseline (unmutated) must exit 0: " + result.stderr.decode(errors="replace")[-800:],
        )
        self.assertFalse(is_assertion_kill(result))

    def test_section5_mutants_are_killed_or_reported_honestly(self) -> None:
        source = ORACLE_SOURCE.read_text(encoding="utf-8")
        baseline = scratch_run_oracle(source)
        self.assertEqual(
            baseline.returncode,
            0,
            "baseline must pass before mutation table: "
            + baseline.stderr.decode(errors="replace")[-800:],
        )
        table: list[tuple[str, str]] = [("baseline_unmutated", "pass")]
        survivors: list[str] = []
        for name, mutate in MUTANTS.items():
            mutated = mutate(source)
            self.assertNotEqual(mutated, source, f"mutant {name} produced no change")
            result = scratch_run_oracle(mutated)
            if is_assertion_kill(result):
                state = "killed"
            elif result.returncode == 0:
                state = "survived"
                survivors.append(name)
            else:
                # Crash/import failure is not a kill; report honestly.
                state = "equivalent_or_broken"
                survivors.append(name)
            table.append((name, state))
        rendered = "\n".join(f"{name:28} {state}" for name, state in table)
        print("\n" + rendered, flush=True)
        # Persist table for the durable report consumer.
        MutationHarnessTests.last_table = table  # type: ignore[attr-defined]
        self.assertEqual(
            survivors,
            [],
            "section-5 mutants no fixture notices:\n" + rendered,
        )


class SealBoundaryTests(unittest.TestCase):
    def test_seal_report_rebuilds_through_outcome(self) -> None:
        sealed = aco.seal_report(
            {
                "closure_verdict": "pass",
                "reason_codes": ["x"],
                "effects_authorized": True,
                "scope": "production",
                "member_verdicts": {},
                "addressed_members": [],
                "missing_members": [],
                "unresolved_dependencies": [],
                "conflicts": [],
                "bindings": {},
            }
        )
        self.assertIs(sealed["effects_authorized"], False)
        self.assertEqual(sealed["scope"], "synthetic_semantics_only")


class ReasonClassificationTests(unittest.TestCase):
    def test_every_catalogued_reason_has_exactly_one_class(self) -> None:
        self.assertEqual(aco.FAIL_REASON_CODES & aco.UNKNOWN_REASON_CODES, set())
        self.assertEqual(aco.FAIL_REASON_CODES & aco.INFORMATIONAL_REASON_CODES, set())
        self.assertEqual(aco.UNKNOWN_REASON_CODES & aco.INFORMATIONAL_REASON_CODES, set())
        paired = aco.FAIL_REASON_CODES | aco.UNKNOWN_REASON_CODES | aco.INFORMATIONAL_REASON_CODES
        self.assertEqual(set(aco.REASON_CODE_CLASS), paired)
        for code, kind in aco.REASON_CODE_CLASS.items():
            self.assertIn(kind, (aco.FAIL, aco.UNKNOWN, "informational"), code)

    def test_emitted_fixture_reasons_are_classified_and_pass_is_informational_only(self) -> None:
        for path in sorted(FIX_DIR.glob("*.json")):
            with self.subTest(case=path.name):
                working, expected = load_fixture(path)
                report = aco.evaluate_document(working)
                for code in report["reason_codes"]:
                    kind = aco.classify_reason_code(code)
                    self.assertIn(
                        kind,
                        (aco.FAIL, aco.UNKNOWN, "informational"),
                        f"{path.name}: unclassified {code}",
                    )
                if report["closure_verdict"] == "pass":
                    for code in report["reason_codes"]:
                        self.assertEqual(
                            aco.classify_reason_code(code),
                            "informational",
                            f"{path.name}: non-informational {code} coexisted with pass",
                        )
                self.assertEqual(report["closure_verdict"], expected["closure_verdict"], path.name)


class PermutationIndependenceTests(unittest.TestCase):
    """Order of assessments (incl. within a member), NA decisions, evidence, conflicts
    must not change closure or reason set. Explicitly includes Q1/Q2 fixtures K11/K12.
    """

    PERMUTE_FOCUS = (
        "K11-temporal-candidate-order.json",
        "K11b-temporal-no-common-snapshot.json",
        "K12-na-scope-mismatch-after-valid.json",
        "K17-no-support-time.json",
        "K17b-mixed-support-time.json",
        "K18-na-with-wrong-bound.json",
        "K18b-na-wrong-bound-reversed.json",
        "K19-assessment-identity-content-conflict.json",
        "K19b-assessment-identity-content-conflict-reversed.json",
        "K19c-assessment-identity-digests-absent.json",
        "K20-assessment-identical-duplicate.json",
        "K21-applicability-coincident-established.json",
        "K21b-applicability-coincident-absent.json",
        "K21c-applicability-flag-wrong-bound.json",
        "K21d-applicability-established-dominates-missing-time.json",
        "K21e-applicability-flag-not-masked.json",
        "K22-na-masks-established-violation.json",
        "K22b-na-masks-established-violation-reversed.json",
        "K22c-na-masks-established-plus-clean.json",
        "K22d-na-with-assessment-flag-absent.json",
        "K22e-na-with-assessment-flag-false.json",
        "K22f-na-established-flag-untrusted.json",
        "S19b-applicability-violation.json",
    )

    def _permute_document(self, working: dict, rng: random.Random) -> dict:
        shuffled = copy.deepcopy(working)
        for key in ("assessments", "evidence", "na_decisions", "conflicts"):
            value = shuffled.get(key)
            if isinstance(value, list) and len(value) > 1:
                rng.shuffle(value)
        # Also permute nested candidate-adjacent lists inside each assessment
        # and NA-adjacent rule component order so within-member order cannot
        # choose a winner. Identical assessment_id duplicates (K20) must keep
        # the same nested order after shuffle so collapse stays a true identity
        # check rather than an accidental content divergence.
        nested_orders: dict[tuple, list[int]] = {}
        for assessment in shuffled.get("assessments") or []:
            if not isinstance(assessment, dict):
                continue
            assessment_id = assessment.get("assessment_id")
            for nested in ("evidence_refs", "entailments", "member_aliases"):
                value = assessment.get(nested)
                if isinstance(value, list) and len(value) > 1:
                    key = (assessment_id, nested, len(value))
                    if key not in nested_orders:
                        order = list(range(len(value)))
                        rng.shuffle(order)
                        nested_orders[key] = order
                    assessment[nested] = [value[i] for i in nested_orders[key]]
        members = shuffled.get("members")
        if isinstance(members, dict):
            for definition in members.values():
                if not isinstance(definition, dict):
                    continue
                rule = definition.get("rule")
                if isinstance(rule, dict):
                    components = rule.get("components")
                    if isinstance(components, list) and len(components) > 1:
                        rng.shuffle(components)
        return shuffled

    def test_shuffling_collections_preserves_verdict_and_reason_set(self) -> None:
        rng = random.Random(82)
        paths = sorted(FIX_DIR.glob("*.json"))
        focus = {name: FIX_DIR / name for name in self.PERMUTE_FOCUS}
        for name, path in focus.items():
            self.assertTrue(path.is_file(), f"missing Q1/Q2 permute fixture {name}")
        for path in paths:
            with self.subTest(case=path.name):
                working, _ = load_fixture(path)
                baseline = aco.evaluate_document(copy.deepcopy(working))
                base_verdict = baseline["closure_verdict"]
                base_reasons = reason_set(baseline["reason_codes"])
                rounds = 8 if path.name in focus else 5
                for _ in range(rounds):
                    shuffled = self._permute_document(working, rng)
                    report = aco.evaluate_document(shuffled)
                    self.assertEqual(report["closure_verdict"], base_verdict, path.name)
                    self.assertEqual(reason_set(report["reason_codes"]), base_reasons, path.name)


if __name__ == "__main__":
    unittest.main()

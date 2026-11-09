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
        "        if entailment.get(\"checked\") is True:\n"
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
        "        if evidence is None:\n"
        "            return MEMBER_UNKNOWN, [\"na_evidence_missing\"]\n"
        "        category, evidence_reasons = _evidence_current_use(\n"
        "            evidence,\n"
        "            evaluation_time,\n"
        "            expected_reviewer_revision,\n"
        "            expected_rule_revision,\n"
        "        )\n"
        "        if category is not None:\n"
        "            return (MEMBER_FAIL if category == FAIL else MEMBER_UNKNOWN), evidence_reasons",
        "evidence = evidence_index.get(evidence_id)\n"
        "        if False and evidence is None:\n"
        "            return MEMBER_UNKNOWN, [\"na_evidence_missing\"]\n"
        "        category, evidence_reasons = None, []\n"
        "        if False:\n"
        "            category, evidence_reasons = _evidence_current_use(\n"
        "                evidence,\n"
        "                evaluation_time,\n"
        "                expected_reviewer_revision,\n"
        "                expected_rule_revision,\n"
        "            )\n"
        "        if category is not None:\n"
        "            return (MEMBER_FAIL if category == FAIL else MEMBER_UNKNOWN), evidence_reasons",
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
        '        if not is_non_empty_string(evidence_id):\n'
        '            return MEMBER_UNKNOWN, ["na_evidence_missing"]\n'
        '        evidence = evidence_index.get(evidence_id)\n'
        '        if evidence is None:\n'
        '            return MEMBER_UNKNOWN, ["na_evidence_missing"]\n'
        '        category, evidence_reasons = _evidence_current_use(\n'
        '            evidence,\n'
        '            evaluation_time,\n'
        '            expected_reviewer_revision,\n'
        '            expected_rule_revision,\n'
        '        )\n'
        '        if category is not None:\n'
        '            return (MEMBER_FAIL if category == FAIL else MEMBER_UNKNOWN), evidence_reasons',
        '# Mutant: accept ungrounded NA without resolving evidence.\n'
        '        evidence_id = decision.get("evidence_id")\n'
        '        _ = (evidence_id, evidence_index, evaluation_time)\n'
        '        if False:\n'
        '            return MEMBER_UNKNOWN, ["na_evidence_missing"]',
        "ungrounded-na",
    ),
    # last-write dedup conflicting identities
    "last-write-dedup": lambda s: _replace_once(
        s,
        "if assessment_id in by_id:\n"
        "            prior = by_id[assessment_id]\n"
        "            if (\n"
        "                prior.get(\"immutable_bytes_digest\") != assessment.get(\"immutable_bytes_digest\")\n"
        "                or prior.get(\"revision_claim\") != assessment.get(\"revision_claim\")\n"
        "            ):\n"
        "                reasons.append(\"assessment_identity_conflict\")\n"
        "                continue\n"
        "        by_id[assessment_id] = assessment",
        "if assessment_id in by_id:\n"
        "            prior = by_id[assessment_id]\n"
        "            if (\n"
        "                prior.get(\"immutable_bytes_digest\") != assessment.get(\"immutable_bytes_digest\")\n"
        "                or prior.get(\"revision_claim\") != assessment.get(\"revision_claim\")\n"
        "            ):\n"
        "                by_id[assessment_id] = assessment\n"
        "                # mutant: last write wins, no conflict reason\n"
        "        by_id[assessment_id] = assessment",
        "last-write-dedup",
    ),
    # temporal union
    "temporal-union": lambda s: _replace_once(
        s,
        "if len(unique) == 1:\n        return True, []\n    # Incompatible historical supports — never union them.",
        "if len(unique) >= 1:\n        return True, []\n    # Mutant unions incompatible historical supports.",
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
    def test_shuffling_collections_preserves_verdict_and_reason_set(self) -> None:
        rng = random.Random(82)
        list_keys = ("assessments", "evidence", "na_decisions", "conflicts")
        for path in sorted(FIX_DIR.glob("*.json")):
            with self.subTest(case=path.name):
                working, _ = load_fixture(path)
                baseline = aco.evaluate_document(copy.deepcopy(working))
                base_verdict = baseline["closure_verdict"]
                base_reasons = reason_set(baseline["reason_codes"])
                for _ in range(5):
                    shuffled = copy.deepcopy(working)
                    for key in list_keys:
                        value = shuffled.get(key)
                        if isinstance(value, list) and len(value) > 1:
                            rng.shuffle(value)
                    report = aco.evaluate_document(shuffled)
                    self.assertEqual(report["closure_verdict"], base_verdict, path.name)
                    self.assertEqual(reason_set(report["reason_codes"]), base_reasons, path.name)


if __name__ == "__main__":
    unittest.main()

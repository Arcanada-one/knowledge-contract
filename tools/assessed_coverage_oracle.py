#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Finite Layer-S assessed-coverage oracle (synthetic semantics only).

Network-free evaluator over one trusted fixture snapshot. Derives the
qualified mandatory member set R* from fixture-marked trusted premises,
evaluates each member's entire declared rule, and emits a sealed report with
``effects_authorized: false`` and ``scope: synthetic_semantics_only``.

This is not production admission, Auth, budget, dispatch fencing, or Layer N
integration. A caller boolean such as ``trusted=true`` is never a premise.

CLI exit codes: 0 pass, 1 fail, 3 unknown / incomplete inspectable, 2 usage.
A missing report must never be read as pass.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

SUPPORTED_SCOPE = "synthetic_semantics_only"
MAX_INPUT_BYTES = 512 * 1024

PASS = "pass"
FAIL = "fail"
UNKNOWN = "unknown"

MEMBER_DISCHARGED = "discharged"
MEMBER_NA = "not_applicable"
MEMBER_FAIL = "fail"
MEMBER_UNKNOWN = "unknown"
MEMBER_MISSING = "missing_assessment"

# Reason codes that may appear alongside pass. Every other emitted code must
# classify as fail or unknown and cannot be ignored when shaping the closure.
INFORMATIONAL_REASON_CODES = frozenset({
    "all_mandatory_members_discharged",
    "empty_set_justified",
    "not_applicable_authorized",
})

FAIL_REASON_CODES = frozenset({
    "malformed_input",
    "reserved_key_in_input",
    "reserved_key_in_requirements",
    "reserved_key_in_member",
    "reserved_key_in_evidence",
    "reserved_key_in_assessment",
    "reserved_key_in_na_decision",
    "reserved_key_in_conflict",
    "binding_identity_incomplete",
    "evidence_identity_conflict",
    "assessment_identity_conflict",
    "invalid_provenance",
    "required_use_denied",
    "evidence_revoked_for_required_use",
    "evidence_validity_excludes_evaluation_time",
    "binding_mismatch",
    "independence_same_origin",
    "na_scope_mismatch",
    "mandatory_conflict_established",
    "temporal_support_incompatible_fail",
    "applicability_violation_established",
    "input_unreadable",
    "input_too_large",
    "duplicate_json_key",
})

UNKNOWN_REASON_CODES = frozenset({
    "binding_missing",
    "mandatory_inventory_absent",
    "requirements_not_trusted_premise",
    "requirements_revision_missing",
    "requirements_member_duplicate",
    "empty_set_unjustified",
    "member_definitions_missing",
    "member_definition_missing",
    "member_rule_missing",
    "member_rule_incomplete",
    "member_rule_not_trusted_premise",
    "caller_boolean_not_premise",
    "evidence_not_trusted_premise",
    "evidence_provenance_missing",
    "evidence_service_unavailable",
    "unrecognized_reviewer_revision",
    "unrecognized_rule_revision",
    "reviewer_revision_unpinned",
    "rule_revision_unpinned",
    "assessment_binding_missing",
    "assessment_not_trusted_premise",
    "conjunction_incomplete",
    "evidence_missing",
    "predicate_unsatisfied",
    "evidence_origin_missing",
    "assessment_evidence_refs_missing",
    "independence_unresolved",
    "member_entailment_unchecked",
    "na_not_trusted_premise",
    "na_missing_authority",
    "na_scope_unverified",
    "na_rule_missing",
    "na_evidence_missing",
    "na_binding_missing",
    "mandatory_conflict_unresolved",
    "temporal_support_incoherent",
    "temporal_support_unverified",
    "evaluation_time_missing",
    "required_profile_uninterpretable",
    "unresolved_mandatory_dependency",
    "closure_incomplete",
    "evidence_current_use_unverified",
    "time_unparsable",
    "no_reason_recorded",
})

REASON_CODE_CLASS = {
    **{code: FAIL for code in FAIL_REASON_CODES},
    **{code: UNKNOWN for code in UNKNOWN_REASON_CODES},
    **{code: "informational" for code in INFORMATIONAL_REASON_CODES},
}

BINDING_FIELDS = (
    "work_item_revision",
    "requirements_revision",
    "contract_revision",
    "contract_profile",
    "actor",
    "action",
    "project",
    "environment",
    "subject",
    "resource",
    "intended_recipient",
    "effective_request_digest",
    "operation_key",
)

REPORT_RESERVED_INPUT_KEYS = frozenset({
    "closure_verdict",
    "reason_codes",
    "also_reason_codes",
    "effects_authorized",
    "execution_granted",
    "proof_promoted",
    "scope",
    "member_verdicts",
    "addressed_members",
    "missing_members",
    "unresolved_dependencies",
    "conflicts",
    "bindings",
})

class DuplicateKeyError(ValueError):
    """Raised when JSON object_pairs_hook sees a repeated key."""


def reject_duplicate_keys(pairs: list[tuple[Any, Any]]) -> dict:
    result: dict = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and value != ""


def classify_reason_code(code: str) -> str:
    """Return fail, unknown, or informational for one emitted reason code."""
    if code in REASON_CODE_CLASS:
        return REASON_CODE_CLASS[code]
    if code.startswith("missing_assessment:"):
        return UNKNOWN
    return UNKNOWN


def parse_rfc3339(value: Any) -> datetime | None:
    """Parse RFC 3339 timestamps that carry an explicit offset (Z or ±hh:mm)."""
    if not is_non_empty_string(value):
        return None
    text = value
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    elif len(text) < 6 or text[-6] not in "+-" or text[-3] != ":":
        return None
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed


def string_list_field(container: dict, key: str) -> tuple[list[str] | None, list[str]]:
    """Absent key => empty list. Present non-list / non-strings => malformed_input."""
    if key not in container:
        return [], []
    value = container.get(key)
    if not isinstance(value, list) or not all(is_non_empty_string(item) for item in value):
        return None, ["malformed_input"]
    return list(value), []


def bool_field(container: dict, key: str) -> tuple[bool | None, list[str]]:
    """Exact-type boolean from a trusted premise.

    Absent => (None, []). Exact bool => (value, []). Present non-bool =>
    malformed_input (string \"true\" is not a boolean).
    """
    if key not in container:
        return None, []
    value = container.get(key)
    if not isinstance(value, bool):
        return None, ["malformed_input"]
    return value, []


def identity_tuple(fields: tuple[str, ...], obj: Any) -> tuple[Any, ...] | None:
    """Typed identity: every field must be a non-empty string before equality."""
    if not isinstance(obj, dict):
        return None
    values: list[Any] = []
    for field in fields:
        value = obj.get(field)
        if not is_non_empty_string(value):
            return None
        values.append(value)
    return tuple(values)


def bindings_equal(left: Any, right: Any) -> bool:
    left_id = identity_tuple(BINDING_FIELDS, left)
    right_id = identity_tuple(BINDING_FIELDS, right)
    if left_id is None or right_id is None:
        return False
    return left_id == right_id


def outcome(closure_verdict: str, reason_codes: list[str], **fields: Any) -> dict:
    """Trusted result constructor: every emitted report is built here."""
    codes = [code for code in reason_codes if is_non_empty_string(code)]
    # Preserve order, drop duplicates.
    seen: set[str] = set()
    ordered: list[str] = []
    for code in codes:
        if code not in seen:
            seen.add(code)
            ordered.append(code)
    if not ordered:
        ordered = ["no_reason_recorded"]
    report = {
        "closure_verdict": closure_verdict,
        "reason_codes": ordered,
        "reason_code": ordered[0],
    }
    report.update(fields)
    report["scope"] = SUPPORTED_SCOPE
    report["effects_authorized"] = False
    report["execution_granted"] = False
    report["proof_promoted"] = False
    report["synthetic_semantics_only"] = True
    return report


def seal_report(report: Any) -> dict:
    """Final trusted boundary before emission."""
    if not isinstance(report, dict):
        return outcome(
            FAIL,
            ["malformed_input"],
            detail="evaluator produced a non-object report",
            member_verdicts={},
            addressed_members=[],
            missing_members=[],
            unresolved_dependencies=[],
            conflicts=[],
            bindings={},
        )
    verdict = report.get("closure_verdict")
    codes = report.get("reason_codes")
    if not is_non_empty_string(verdict):
        return outcome(
            FAIL,
            ["malformed_input"],
            detail="evaluator report missing non-empty closure_verdict",
            member_verdicts={},
            addressed_members=[],
            missing_members=[],
            unresolved_dependencies=[],
            conflicts=[],
            bindings={},
        )
    if not isinstance(codes, list) or not codes:
        primary = report.get("reason_code")
        codes = [primary] if is_non_empty_string(primary) else ["malformed_input"]
    extra = {
        key: value
        for key, value in report.items()
        if key not in (
            "closure_verdict",
            "reason_codes",
            "reason_code",
            "scope",
            "effects_authorized",
            "execution_granted",
            "proof_promoted",
            "synthetic_semantics_only",
        )
    }
    return outcome(verdict, list(codes), **extra)


def _mark_trusted(obj: Any) -> bool:
    """True only when the fixture marks a trusted test premise."""
    return isinstance(obj, dict) and obj.get("trusted_test_premise") is True


def _load_binding(document: dict) -> tuple[dict | None, list[str]]:
    binding = document.get("binding_b0")
    if not isinstance(binding, dict):
        return None, ["binding_missing"]
    if identity_tuple(BINDING_FIELDS, binding) is None:
        return None, ["binding_identity_incomplete"]
    return binding, []


def _requirements_inventory(document: dict) -> tuple[dict | None, list[str], str | None]:
    """Return (inventory, reasons, mode).

    mode is one of: present, absent, empty_justified, empty_unjustified, malformed.
    """
    if "requirements" not in document:
        return None, ["mandatory_inventory_absent"], "absent"
    requirements = document.get("requirements")
    if not isinstance(requirements, dict):
        return None, ["malformed_input"], "malformed"
    if not _mark_trusted(requirements):
        return None, ["requirements_not_trusted_premise"], "malformed"
    if REPORT_RESERVED_INPUT_KEYS.intersection(requirements.keys()):
        return None, ["reserved_key_in_requirements"], "malformed"
    revision = requirements.get("revision")
    if not is_non_empty_string(revision):
        return None, ["requirements_revision_missing"], "malformed"
    if "members" not in requirements:
        return None, ["mandatory_inventory_absent"], "absent"
    members = requirements.get("members")
    if not isinstance(members, list):
        return None, ["malformed_input"], "malformed"
    for member in members:
        if not is_non_empty_string(member):
            return None, ["malformed_input"], "malformed"
    if len(members) != len(set(members)):
        return None, ["requirements_member_duplicate"], "malformed"
    justification = requirements.get("empty_set_justification")
    if members == []:
        if is_non_empty_string(justification):
            return requirements, [], "empty_justified"
        return requirements, ["empty_set_unjustified"], "empty_unjustified"
    return requirements, [], "present"


def _member_defs(document: dict, member_ids: list[str]) -> tuple[dict[str, dict], list[str]]:
    members = document.get("members")
    if members is None:
        if not member_ids:
            return {}, []
        return {}, ["member_definitions_missing"]
    if not isinstance(members, dict):
        return {}, ["malformed_input"]
    out: dict[str, dict] = {}
    reasons: list[str] = []
    for member_id in member_ids:
        definition = members.get(member_id)
        if not isinstance(definition, dict):
            reasons.append("member_definition_missing")
            continue
        # Spec §2: each member keeps its exact rule from the trusted snapshot.
        if not _mark_trusted(definition):
            if definition.get("trusted") is True:
                reasons.append("caller_boolean_not_premise")
            else:
                reasons.append("member_rule_not_trusted_premise")
            continue
        if REPORT_RESERVED_INPUT_KEYS.intersection(definition.keys()):
            reasons.append("reserved_key_in_member")
            continue
        rule = definition.get("rule")
        if not isinstance(rule, dict):
            reasons.append("member_rule_missing")
            continue
        components = rule.get("components")
        if not isinstance(components, list) or not components:
            reasons.append("member_rule_incomplete")
            continue
        ok = True
        for component in components:
            if not isinstance(component, dict):
                ok = False
                break
            if not is_non_empty_string(component.get("predicate")):
                ok = False
                break
            if not is_non_empty_string(component.get("evidence_id")):
                ok = False
                break
        if not ok:
            reasons.append("member_rule_incomplete")
            continue
        # Present non-bool independence flag is a malformed trusted rule (Q5).
        _, indep_malformed = bool_field(rule, "require_independent_origins")
        if indep_malformed:
            reasons.extend(indep_malformed)
            continue
        out[member_id] = definition
    return out, reasons


def _evidence_index(document: dict) -> tuple[dict[str, dict], list[str]]:
    records = document.get("evidence")
    if records is None:
        return {}, []
    if not isinstance(records, list):
        return {}, ["malformed_input"]
    index: dict[str, dict] = {}
    conflicted: set[str] = set()
    reasons: list[str] = []
    for record in records:
        if not isinstance(record, dict):
            reasons.append("malformed_input")
            continue
        if REPORT_RESERVED_INPUT_KEYS.intersection(record.keys()):
            reasons.append("reserved_key_in_evidence")
            continue
        evidence_id = record.get("evidence_id")
        if not is_non_empty_string(evidence_id):
            reasons.append("malformed_input")
            continue
        if evidence_id in conflicted:
            reasons.append("evidence_identity_conflict")
            continue
        if evidence_id in index:
            # Same id with any differing field is an identity conflict (S18/P19).
            # Byte-identical duplicates may collapse. Conflicting identities are
            # unusable: drop the id so order cannot choose a winner.
            prior = index[evidence_id]
            if prior != record:
                reasons.append("evidence_identity_conflict")
                del index[evidence_id]
                conflicted.add(evidence_id)
            continue
        index[evidence_id] = record
    return index, reasons


def _assessment_list(document: dict) -> tuple[list[dict], list[str]]:
    assessments = document.get("assessments")
    if assessments is None:
        return [], []
    if not isinstance(assessments, list):
        return [], ["malformed_input"]
    index: dict[str, dict] = {}
    conflicted: set[str] = set()
    reasons: list[str] = []
    for assessment in assessments:
        if not isinstance(assessment, dict):
            reasons.append("malformed_input")
            continue
        if REPORT_RESERVED_INPUT_KEYS.intersection(assessment.keys()):
            reasons.append("reserved_key_in_assessment")
            continue
        assessment_id = assessment.get("assessment_id")
        if not is_non_empty_string(assessment_id):
            reasons.append("malformed_input")
            continue
        if assessment_id in conflicted:
            # Same conflicted id again: still a conflict; identity stays unusable.
            reasons.append("assessment_identity_conflict")
            continue
        if assessment_id in index:
            # Same id with any differing field is an identity conflict (F1).
            # Claimed digest/revision equality does not prove content equality.
            # Byte-identical duplicates may collapse. Conflicting identities are
            # unusable: drop the id so order cannot choose a winner.
            prior = index[assessment_id]
            if prior != assessment:
                reasons.append("assessment_identity_conflict")
                del index[assessment_id]
                conflicted.add(assessment_id)
            continue
        index[assessment_id] = assessment
    return list(index.values()), reasons


def _qualified_member_id(assessment: dict, known: set[str]) -> str | None:
    """Reconcile aliases to a single qualified member id."""
    aliases: list[str] = []
    member_id = assessment.get("member_id")
    if is_non_empty_string(member_id):
        aliases.append(member_id)
    extra = assessment.get("member_aliases")
    if isinstance(extra, list):
        for alias in extra:
            if is_non_empty_string(alias):
                aliases.append(alias)
    qualified = [alias for alias in aliases if alias in known]
    if not qualified:
        return None
    # Aliases of the same member collapse; distinct known ids do not inflate coverage.
    unique = sorted(set(qualified))
    if len(unique) != 1:
        return None
    return unique[0]


def _evidence_current_use(
    evidence: dict,
    evaluation_time: str,
    expected_reviewer_revision: str | None,
    expected_rule_revision: str | None,
) -> tuple[str | None, list[str]]:
    """Return (hard_fail_or_unknown_reason_category, reasons).

    category is FAIL, UNKNOWN, or None when usable.
    """
    if not _mark_trusted(evidence):
        # Bare caller trusted boolean is never a premise.
        provenance = evidence.get("provenance")
        if isinstance(provenance, dict) and provenance.get("trusted") is True:
            return UNKNOWN, ["caller_boolean_not_premise"]
        return UNKNOWN, ["evidence_not_trusted_premise"]
    provenance = evidence.get("provenance")
    if not isinstance(provenance, dict):
        return UNKNOWN, ["evidence_provenance_missing"]
    invalid_proven, invalid_malformed = bool_field(provenance, "invalid_provenance_proven")
    if invalid_malformed:
        return FAIL, invalid_malformed
    if invalid_proven is True:
        return FAIL, ["invalid_provenance"]
    # Absent current-use signals are not clean (P11).
    if (
        "valid_from" not in provenance
        or "valid_to" not in provenance
        or "service_status" not in provenance
        or "revoked_for_required_use" not in provenance
    ):
        return UNKNOWN, ["evidence_current_use_unverified"]
    service = provenance.get("service_status")
    if service == "denied":
        return FAIL, ["required_use_denied"]
    if service == "unavailable":
        return UNKNOWN, ["evidence_service_unavailable"]
    if service != "available":
        return UNKNOWN, ["evidence_current_use_unverified"]
    if provenance.get("revoked_for_required_use") is True:
        return FAIL, ["evidence_revoked_for_required_use"]
    if not isinstance(provenance.get("revoked_for_required_use"), bool):
        return UNKNOWN, ["evidence_current_use_unverified"]
    valid_from = provenance.get("valid_from")
    valid_to = provenance.get("valid_to")
    eval_dt = parse_rfc3339(evaluation_time)
    from_dt = parse_rfc3339(valid_from)
    to_dt = parse_rfc3339(valid_to)
    if eval_dt is None or from_dt is None or to_dt is None:
        return UNKNOWN, ["time_unparsable"]
    if eval_dt < from_dt or eval_dt > to_dt:
        return FAIL, ["evidence_validity_excludes_evaluation_time"]
    reviewer_revision = provenance.get("reviewer_revision")
    rule_revision = provenance.get("rule_revision")
    if expected_reviewer_revision is not None and is_non_empty_string(expected_reviewer_revision):
        if not is_non_empty_string(reviewer_revision):
            return UNKNOWN, ["unrecognized_reviewer_revision"]
        if reviewer_revision != expected_reviewer_revision:
            return UNKNOWN, ["unrecognized_reviewer_revision"]
    if expected_rule_revision is not None and is_non_empty_string(expected_rule_revision):
        if not is_non_empty_string(rule_revision):
            return UNKNOWN, ["unrecognized_rule_revision"]
        if rule_revision != expected_rule_revision:
            return UNKNOWN, ["unrecognized_rule_revision"]
    return None, []


def _assessment_trust(
    assessment: dict,
    binding_b0: dict,
    expected_reviewer_revision: str | None,
    expected_rule_revision: str | None,
) -> tuple[str | None, list[str]]:
    provenance = assessment.get("provenance")
    # keep: caller_boolean_guard — a bare trusted=true is never a premise (S15a).
    caller_boolean = (
        isinstance(provenance, dict)
        and provenance.get("trusted") is True
        and not _mark_trusted(assessment)
    )
    if caller_boolean:
        return UNKNOWN, ["caller_boolean_not_premise"]
    if not _mark_trusted(assessment):
        return UNKNOWN, ["assessment_not_trusted_premise"]
    if REPORT_RESERVED_INPUT_KEYS.intersection(assessment.keys()):
        return FAIL, ["reserved_key_in_assessment"]
    assessment_binding = assessment.get("binding")
    if not isinstance(assessment_binding, dict):
        return UNKNOWN, ["assessment_binding_missing"]
    if not bindings_equal(assessment_binding, binding_b0):
        return FAIL, ["binding_mismatch"]
    if isinstance(provenance, dict):
        invalid_proven, invalid_malformed = bool_field(provenance, "invalid_provenance_proven")
        if invalid_malformed:
            return FAIL, invalid_malformed
        if invalid_proven is True:
            return FAIL, ["invalid_provenance"]
    if expected_reviewer_revision is not None:
        reviewer_revision = None
        if isinstance(provenance, dict):
            reviewer_revision = provenance.get("reviewer_revision")
        if not is_non_empty_string(reviewer_revision):
            reviewer_revision = assessment.get("reviewer_revision")
        if not is_non_empty_string(reviewer_revision) or reviewer_revision != expected_reviewer_revision:
            return UNKNOWN, ["unrecognized_reviewer_revision"]
    if expected_rule_revision is not None:
        rule_revision = None
        if isinstance(provenance, dict):
            rule_revision = provenance.get("rule_revision")
        if not is_non_empty_string(rule_revision):
            rule_revision = assessment.get("rule_revision")
        if not is_non_empty_string(rule_revision) or rule_revision != expected_rule_revision:
            return UNKNOWN, ["unrecognized_rule_revision"]
    return None, []


def _component_satisfied(
    component: dict,
    evidence_index: dict[str, dict],
    bound_evidence_ids: set[str],
    evaluation_time: str,
    expected_reviewer_revision: str | None,
    expected_rule_revision: str | None,
) -> tuple[bool, str | None, list[str], str | None]:
    """Return (ok, category, reasons, origin_id)."""
    evidence_id = component.get("evidence_id")
    predicate = component.get("predicate")
    if evidence_id not in bound_evidence_ids:
        return False, UNKNOWN, ["conjunction_incomplete"], None
    evidence = evidence_index.get(evidence_id)
    if evidence is None:
        return False, UNKNOWN, ["evidence_missing"], None
    category, reasons = _evidence_current_use(
        evidence,
        evaluation_time,
        expected_reviewer_revision,
        expected_rule_revision,
    )
    if category is not None:
        return False, category, reasons, evidence.get("origin_id") if isinstance(evidence.get("origin_id"), str) else None
    satisfies = evidence.get("satisfies")
    if not isinstance(satisfies, list) or predicate not in satisfies:
        return False, UNKNOWN, ["predicate_unsatisfied"], None
    origin = evidence.get("origin_id")
    if not is_non_empty_string(origin):
        return False, UNKNOWN, ["evidence_origin_missing"], None
    return True, None, [], origin


def _evaluate_member_rule(
    member_id: str,
    definition: dict,
    assessment: dict,
    evidence_index: dict[str, dict],
    evaluation_time: str,
    expected_reviewer_revision: str | None,
    expected_rule_revision: str | None,
) -> tuple[str, list[str]]:
    """Return (member_verdict, reasons)."""
    rule = definition.get("rule") or {}
    components = rule.get("components") or []
    refs = assessment.get("evidence_refs")
    if not isinstance(refs, list):
        return MEMBER_UNKNOWN, ["assessment_evidence_refs_missing"]
    bound_ids = {ref for ref in refs if is_non_empty_string(ref)}
    # Submitted "accepted" labels never override evaluated rule completeness.
    origins: list[str] = []
    reasons: list[str] = []
    saw_fail = False
    saw_unknown = False
    for component in components:
        ok, category, component_reasons, origin = _component_satisfied(
            component,
            evidence_index,
            bound_ids,
            evaluation_time,
            expected_reviewer_revision,
            expected_rule_revision,
        )
        reasons.extend(component_reasons)
        if not ok:
            if category == FAIL:
                saw_fail = True
            else:
                saw_unknown = True
            continue
        if origin is not None:
            origins.append(origin)
    if saw_fail:
        return MEMBER_FAIL, reasons
    if saw_unknown:
        return MEMBER_UNKNOWN, reasons
    require_independent, indep_malformed = bool_field(rule, "require_independent_origins")
    if indep_malformed:
        return MEMBER_FAIL, reasons + indep_malformed
    if require_independent is True:
        # Copies/aliases/renditions share origin_id; independence requires distinct origins.
        if len(origins) != len(components):
            return MEMBER_UNKNOWN, reasons + ["independence_unresolved"]
        if len(set(origins)) != len(origins):
            # Sameness established via equal origin_id.
            return MEMBER_FAIL, reasons + ["independence_same_origin"]
        # Optional explicit markers that copies are not independent.
        for evidence_id in bound_ids:
            evidence = evidence_index.get(evidence_id) or {}
            if evidence.get("copy_of") in bound_ids or evidence.get("rendition_of") in bound_ids:
                return MEMBER_FAIL, reasons + ["independence_same_origin"]
            aliases = evidence.get("aliases_of")
            if isinstance(aliases, list) and any(item in bound_ids for item in aliases):
                return MEMBER_FAIL, reasons + ["independence_same_origin"]
    # Shared observation supports a member only through a checked member-specific
    # entailment (S05 / P02–P04). Absent, empty, or unchecked ⇒ unknown.
    entailments = assessment.get("entailments")
    if not isinstance(entailments, list) or not entailments:
        return MEMBER_UNKNOWN, reasons + ["member_entailment_unchecked"]
    matched = False
    for entailment in entailments:
        if not isinstance(entailment, dict):
            continue
        if entailment.get("member_id") != member_id:
            continue
        checked, checked_malformed = bool_field(entailment, "checked")
        if checked_malformed:
            return MEMBER_FAIL, reasons + checked_malformed
        if checked is True:
            matched = True
            break
    if not matched:
        return MEMBER_UNKNOWN, reasons + ["member_entailment_unchecked"]
    return MEMBER_DISCHARGED, reasons


def _scan_na_decisions(document: dict) -> list[str]:
    """Record malformation reasons for the na_decisions collection."""
    decisions = document.get("na_decisions")
    if decisions is None:
        return []
    if not isinstance(decisions, list):
        return ["malformed_input"]
    reasons: list[str] = []
    for decision in decisions:
        if not isinstance(decision, dict):
            reasons.append("malformed_input")
            continue
        if REPORT_RESERVED_INPUT_KEYS.intersection(decision.keys()):
            reasons.append("reserved_key_in_na_decision")
            continue
        if not is_non_empty_string(decision.get("member_id")):
            reasons.append("malformed_input")
    return reasons


def _evaluate_one_na_decision(
    decision: dict,
    binding_b0: dict,
    evidence_index: dict[str, dict],
    evaluation_time: str,
    expected_reviewer_revision: str | None,
    expected_rule_revision: str | None,
) -> tuple[str, list[str]]:
    """Evaluate a single NA decision for one member. Returns (verdict, reasons)."""
    if not _mark_trusted(decision):
        if isinstance(decision.get("provenance"), dict) and decision["provenance"].get("trusted") is True:
            return MEMBER_UNKNOWN, ["caller_boolean_not_premise"]
        return MEMBER_UNKNOWN, ["na_not_trusted_premise"]
    authorized, auth_malformed = bool_field(decision, "authorized")
    if auth_malformed:
        return MEMBER_FAIL, auth_malformed
    if authorized is not True:
        return MEMBER_UNKNOWN, ["na_missing_authority"]
    scope_matches, scope_malformed = bool_field(decision, "binding_scope_matches_b0")
    if scope_malformed:
        return MEMBER_FAIL, scope_malformed
    established_mismatch, established_malformed = bool_field(
        decision, "scope_mismatch_established"
    )
    if established_malformed:
        return MEMBER_FAIL, established_malformed
    if scope_matches is not True:
        # Proven scope mismatch is fail when the fixture marks it established.
        if established_mismatch is True:
            return MEMBER_FAIL, ["na_scope_mismatch"]
        return MEMBER_UNKNOWN, ["na_scope_unverified"]
    if not is_non_empty_string(decision.get("rule_id")):
        return MEMBER_UNKNOWN, ["na_rule_missing"]
    evidence_id = decision.get("evidence_id")
    if not is_non_empty_string(evidence_id):
        return MEMBER_UNKNOWN, ["na_evidence_missing"]
    evidence = evidence_index.get(evidence_id)
    if evidence is None:
        return MEMBER_UNKNOWN, ["na_evidence_missing"]
    category, evidence_reasons = _evidence_current_use(
        evidence,
        evaluation_time,
        expected_reviewer_revision,
        expected_rule_revision,
    )
    if category is not None:
        return (MEMBER_FAIL if category == FAIL else MEMBER_UNKNOWN), evidence_reasons
    # NA binding must be an object matching B0 (Q7); absent/non-object ⇒ unknown.
    decision_binding = decision.get("binding")
    if not isinstance(decision_binding, dict):
        return MEMBER_UNKNOWN, ["na_binding_missing"]
    if not bindings_equal(decision_binding, binding_b0):
        return MEMBER_FAIL, ["na_scope_mismatch"]
    return MEMBER_NA, ["not_applicable_authorized"]


def _na_decision_for(
    member_id: str,
    document: dict,
    binding_b0: dict,
    evidence_index: dict[str, dict],
    evaluation_time: str,
    expected_reviewer_revision: str | None,
    expected_rule_revision: str | None,
) -> tuple[str | None, list[str]]:
    """Aggregate every NA decision for the member (order-invariant).

    Any established scope mismatch ⇒ fail. Otherwise unknown reasons dominate a
    valid NA. A sole valid NA discharges the member.
    """
    decisions = document.get("na_decisions")
    if decisions is None:
        return None, []
    if not isinstance(decisions, list):
        return None, ["malformed_input"]
    saw_fail = False
    saw_unknown = False
    saw_na = False
    reasons: list[str] = []
    matched = False
    for decision in decisions:
        if not isinstance(decision, dict):
            continue
        if decision.get("member_id") != member_id:
            continue
        matched = True
        verdict, decision_reasons = _evaluate_one_na_decision(
            decision,
            binding_b0,
            evidence_index,
            evaluation_time,
            expected_reviewer_revision,
            expected_rule_revision,
        )
        reasons.extend(decision_reasons)
        if verdict == MEMBER_FAIL:
            saw_fail = True
        elif verdict == MEMBER_UNKNOWN:
            saw_unknown = True
        elif verdict == MEMBER_NA:
            saw_na = True
    if not matched:
        return None, []
    if saw_fail:
        return MEMBER_FAIL, reasons
    if saw_unknown:
        return MEMBER_UNKNOWN, reasons
    if saw_na:
        return MEMBER_NA, reasons
    return MEMBER_UNKNOWN, reasons or ["na_scope_unverified"]


def _collect_conflicts(document: dict) -> tuple[list[dict], list[str], bool, bool]:
    """Return (conflicts, reasons, has_fail_conflict, has_unknown_conflict)."""
    conflicts = document.get("conflicts")
    if conflicts is None:
        return [], [], False, False
    if not isinstance(conflicts, list):
        return [], ["malformed_input"], False, True
    out: list[dict] = []
    reasons: list[str] = []
    has_fail = False
    has_unknown = False
    for conflict in conflicts:
        if not isinstance(conflict, dict):
            reasons.append("malformed_input")
            has_unknown = True
            continue
        if REPORT_RESERVED_INPUT_KEYS.intersection(conflict.keys()):
            reasons.append("reserved_key_in_conflict")
            has_fail = True
            continue
        if not is_non_empty_string(conflict.get("conflict_id")):
            reasons.append("malformed_input")
            has_unknown = True
            continue
        resolved, resolved_malformed = bool_field(conflict, "resolved")
        established, established_malformed = bool_field(conflict, "established")
        if resolved_malformed or established_malformed:
            reasons.extend(resolved_malformed + established_malformed)
            has_fail = True
            continue
        record = {
            "conflict_id": conflict.get("conflict_id"),
            "kind": conflict.get("kind"),
            "resolved": resolved is True,
            "established": established is True,
        }
        out.append(record)
        if record["resolved"]:
            continue
        if record["established"]:
            has_fail = True
            reasons.append("mandatory_conflict_established")
        else:
            has_unknown = True
            reasons.append("mandatory_conflict_unresolved")
    return out, reasons, has_fail, has_unknown


def _support_times_coherent(
    trusted_candidates_by_member: dict[str, list[dict]],
    assessment_discharged_members: list[str],
) -> tuple[bool, list[str]]:
    """Temporal coherence for members discharged by assessment (not NA).

    Rule (Q1 / Q6): every assessment-discharged member must demonstrate at
    least one ``support_time`` on a trusted binding-matched candidate. A
    coherent snapshot is one support_time present for every such member. If
    any assessment-discharged member lacks a support_time — including the
    mixed missing/present case — emit ``temporal_support_unverified``; do not
    intersect over a partial mandatory set. Members discharged only by a
    valid NA are exempt from the common-snapshot obligation. Incompatible
    declared times still yield ``temporal_support_incoherent`` (or
    ``temporal_support_incompatible_fail`` when an applicability violation is
    established).

    F3: a trusted B0-bound ``applicability_violation_established: true`` is an
    independent FAIL premise over *every* admitted trusted candidate, including
    assessments for members later discharged by a valid authorised NA. NA does
    not erase that established contradiction.
    """
    times_by_member: dict[str, set[datetime]] = {}
    applicability_fail = False
    missing_support = False
    # F3: scan established-violation over every admitted trusted B0-bound
    # assessment, not only over assessment-discharged members.
    for _member_id, candidates in trusted_candidates_by_member.items():
        for assessment in candidates:
            flag, flag_malformed = bool_field(
                assessment, "applicability_violation_established"
            )
            if flag_malformed:
                return False, flag_malformed
            if flag is True:
                applicability_fail = True
    for member_id in assessment_discharged_members:
        candidates = trusted_candidates_by_member.get(member_id) or []
        times: set[datetime] = set()
        for assessment in candidates:
            support_time = assessment.get("support_time")
            if not is_non_empty_string(support_time):
                continue
            parsed = parse_rfc3339(support_time)
            if parsed is None:
                return False, ["time_unparsable"]
            times.add(parsed)
        if not times:
            missing_support = True
        else:
            times_by_member[member_id] = times
    # Trusted established applicability violation is FAIL on its own (F2/F3):
    # timestamp intersection cannot negate it; it dominates missing-support UNKNOWN.
    # A valid authorised NA for the same member also cannot erase it.
    if applicability_fail and missing_support:
        return False, ["applicability_violation_established"]
    # Any discharging assessment without demonstrated support time ⇒ unverified
    # (covers all-absent and mixed missing/present; order-invariant).
    if missing_support:
        return False, ["temporal_support_unverified"]
    if not times_by_member:
        if applicability_fail:
            return False, ["applicability_violation_established"]
        return True, []
    common = set.intersection(*(times_by_member[member_id] for member_id in times_by_member))
    if common:
        if applicability_fail:
            return False, ["applicability_violation_established"]
        return True, []
    # No single snapshot covers every assessment-discharged member.
    if applicability_fail:
        return False, [
            "temporal_support_incompatible_fail",
            "applicability_violation_established",
        ]
    return False, ["temporal_support_incoherent"]


def _closure_from_reasons(
    reasons: list[str],
    member_verdicts: dict[str, str],
    unresolved_dependencies: list[str],
    fail_conflict: bool,
    unknown_conflict: bool,
) -> tuple[str, list[str]]:
    """Derive closure from classified reasons; informational codes alone may pass."""
    working = list(reasons)
    saw_fail = fail_conflict or any(
        verdict == MEMBER_FAIL for verdict in member_verdicts.values()
    )
    saw_unknown = unknown_conflict or bool(unresolved_dependencies) or any(
        verdict in (MEMBER_UNKNOWN, MEMBER_MISSING) for verdict in member_verdicts.values()
    )
    for code in working:
        kind = classify_reason_code(code)
        if kind == FAIL:
            saw_fail = True
        elif kind == UNKNOWN:
            saw_unknown = True
    if saw_fail:
        return FAIL, working
    if saw_unknown:
        return UNKNOWN, working
    if all(
        verdict in (MEMBER_DISCHARGED, MEMBER_NA) for verdict in member_verdicts.values()
    ) and not unresolved_dependencies:
        working.append("all_mandatory_members_discharged")
        return PASS, working
    working.append("closure_incomplete")
    return UNKNOWN, working


def evaluate(document: dict) -> dict:
    """Evaluate one fixture snapshot; always returns a sealed-shaped report dict."""
    if not isinstance(document, dict):
        return outcome(
            FAIL,
            ["malformed_input"],
            detail="document must be an object",
            member_verdicts={},
            addressed_members=[],
            missing_members=[],
            unresolved_dependencies=[],
            conflicts=[],
            bindings={},
        )
    if REPORT_RESERVED_INPUT_KEYS.intersection(
        key for key in document.keys() if key not in ("expected",)
    ) and any(
        key in document and key in REPORT_RESERVED_INPUT_KEYS
        for key in (
            "closure_verdict",
            "effects_authorized",
            "execution_granted",
            "member_verdicts",
        )
    ):
        # Input must not pre-supply evaluator output keys that shape the verdict.
        if document.get("closure_verdict") is not None or document.get("effects_authorized") is not None:
            return outcome(
                FAIL,
                ["reserved_key_in_input"],
                detail="fixture input must not supply evaluator output keys",
                member_verdicts={},
                addressed_members=[],
                missing_members=[],
                unresolved_dependencies=[],
                conflicts=[],
                bindings={},
            )

    reasons: list[str] = []
    binding_b0, binding_reasons = _load_binding(document)
    reasons.extend(binding_reasons)
    if binding_b0 is None:
        return outcome(
            FAIL if "binding_identity_incomplete" in binding_reasons else UNKNOWN,
            reasons or ["binding_missing"],
            member_verdicts={},
            addressed_members=[],
            missing_members=[],
            unresolved_dependencies=[],
            conflicts=[],
            bindings={},
        )

    evaluation_time = document.get("evaluation_time")
    if not is_non_empty_string(evaluation_time):
        return outcome(
            UNKNOWN,
            ["evaluation_time_missing"],
            member_verdicts={},
            addressed_members=[],
            missing_members=[],
            unresolved_dependencies=[],
            conflicts=[],
            bindings={"b0": binding_b0},
        )
    if parse_rfc3339(evaluation_time) is None:
        return outcome(
            UNKNOWN,
            ["time_unparsable"],
            member_verdicts={},
            addressed_members=[],
            missing_members=[],
            unresolved_dependencies=[],
            conflicts=[],
            bindings={"b0": binding_b0},
        )

    # Spec §2 pins reviewer and rule revisions; absence does not skip the check (P05).
    pin_reasons: list[str] = []
    if "reviewer_revision" not in document or not is_non_empty_string(document.get("reviewer_revision")):
        pin_reasons.append("reviewer_revision_unpinned")
    if "rule_revision" not in document or not is_non_empty_string(document.get("rule_revision")):
        pin_reasons.append("rule_revision_unpinned")
    expected_reviewer_revision = document.get("reviewer_revision")
    expected_rule_revision = document.get("rule_revision")
    if pin_reasons:
        return outcome(
            UNKNOWN,
            pin_reasons,
            member_verdicts={},
            addressed_members=[],
            missing_members=[],
            unresolved_dependencies=[],
            conflicts=[],
            bindings={"b0": binding_b0},
        )

    inventory, inv_reasons, inv_mode = _requirements_inventory(document)
    reasons.extend(inv_reasons)

    # Required constraint-bearing profiles must be interpretable from trusted premises.
    # Present-but-malformed trusted inventory fields fail closed (P09/P10).
    if isinstance(inventory, dict):
        required_profiles, profile_reasons = string_list_field(inventory, "required_profiles")
        interpretable, interpretable_reasons = string_list_field(inventory, "interpretable_profiles")
        dependencies_field, dependency_reasons = string_list_field(inventory, "dependencies")
        shape_reasons = profile_reasons + interpretable_reasons + dependency_reasons
        if shape_reasons:
            return outcome(
                FAIL,
                reasons + shape_reasons,
                member_verdicts={},
                addressed_members=[],
                missing_members=[],
                unresolved_dependencies=[],
                conflicts=[],
                bindings={"b0": binding_b0},
            )
        assert required_profiles is not None and interpretable is not None
        for profile in required_profiles:
            if profile not in interpretable:
                # Producer optional flag cannot suppress a trusted required profile.
                reasons.append("required_profile_uninterpretable")
        producer_optional = inventory.get("producer_marks_optional")
        if producer_optional is True and "required_profile_uninterpretable" in reasons:
            # Keep the gap; do not honor producer optional.
            pass

    if inv_mode in ("absent", "empty_unjustified", "malformed"):
        verdict = FAIL if "malformed_input" in inv_reasons or "reserved_key_in_requirements" in inv_reasons else UNKNOWN
        return outcome(
            verdict,
            reasons or ["mandatory_inventory_unresolved"],
            member_verdicts={},
            addressed_members=[],
            missing_members=[],
            unresolved_dependencies=list((inventory or {}).get("dependencies") or [])
            if isinstance(inventory, dict) and isinstance((inventory or {}).get("dependencies"), list)
            else [],
            conflicts=[],
            bindings={"b0": binding_b0},
        )

    assert inventory is not None
    if "required_profile_uninterpretable" in reasons:
        return outcome(
            UNKNOWN,
            reasons,
            member_verdicts={},
            addressed_members=[],
            missing_members=[],
            unresolved_dependencies=list(inventory.get("dependencies") or [])
            if isinstance(inventory.get("dependencies"), list)
            else [],
            conflicts=[],
            bindings={"b0": binding_b0},
        )

    member_ids = list(inventory.get("members") or [])
    dependencies, dependency_reasons = string_list_field(inventory, "dependencies")
    if dependency_reasons:
        return outcome(
            FAIL,
            reasons + dependency_reasons,
            member_verdicts={},
            addressed_members=[],
            missing_members=[],
            unresolved_dependencies=[],
            conflicts=[],
            bindings={"b0": binding_b0},
        )
    assert dependencies is not None
    unresolved_dependencies = [dep for dep in dependencies if dep not in member_ids]
    if unresolved_dependencies:
        reasons.append("unresolved_mandatory_dependency")

    if inv_mode == "empty_justified":
        conflicts, conflict_reasons, fail_conflict, unknown_conflict = _collect_conflicts(document)
        reasons.extend(conflict_reasons)
        reasons.extend(_scan_na_decisions(document))
        closure, reasons = _closure_from_reasons(
            reasons,
            {},
            unresolved_dependencies,
            fail_conflict,
            unknown_conflict,
        )
        if closure == PASS:
            reasons = [code for code in reasons if code != "all_mandatory_members_discharged"]
            reasons.append("empty_set_justified")
        return outcome(
            closure,
            reasons,
            member_verdicts={},
            addressed_members=[],
            missing_members=[],
            unresolved_dependencies=[] if closure == PASS else unresolved_dependencies,
            conflicts=conflicts,
            bindings={"b0": binding_b0},
            empty_set_justification=inventory.get("empty_set_justification"),
        )

    member_defs, member_def_reasons = _member_defs(document, member_ids)
    reasons.extend(member_def_reasons)
    evidence_index, evidence_reasons = _evidence_index(document)
    reasons.extend(evidence_reasons)
    assessments, assessment_reasons = _assessment_list(document)
    reasons.extend(assessment_reasons)
    reasons.extend(_scan_na_decisions(document))

    conflicts, conflict_reasons, fail_conflict, unknown_conflict = _collect_conflicts(document)
    reasons.extend(conflict_reasons)

    known_members = set(member_ids)
    addressed: list[str] = []
    candidates_by_member: dict[str, list[dict]] = {}
    for assessment in assessments:
        qualified = _qualified_member_id(assessment, known_members)
        if qualified is None:
            continue
        if qualified not in addressed:
            addressed.append(qualified)
        candidates_by_member.setdefault(qualified, []).append(assessment)

    member_verdicts: dict[str, str] = {}
    # Trusted + binding-matched candidates per member for order-invariant temporal coherence.
    trusted_temporal_candidates: dict[str, list[dict]] = {
        member_id: [] for member_id in member_ids
    }

    for member_id in member_ids:
        # Q8: evaluate every submitted assessment candidate for integrity
        # BEFORE the NA discharge decision. A valid NA does not sanitize a
        # wrong-bound / failing companion in the same scoped collection.
        candidates = candidates_by_member.get(member_id) or []
        definition = member_defs.get(member_id)
        saw_binding_mismatch = False
        saw_member_fail = False
        saw_member_unknown = False
        saw_discharged = False
        for assessment in candidates:
            trust_category, trust_reasons = _assessment_trust(
                assessment,
                binding_b0,
                expected_reviewer_revision,
                expected_rule_revision,
            )
            reasons.extend(trust_reasons)
            if "binding_mismatch" in trust_reasons:
                saw_binding_mismatch = True
                saw_member_fail = True
                continue
            if trust_category == FAIL:
                saw_member_fail = True
                continue
            if trust_category == UNKNOWN:
                saw_member_unknown = True
                continue
            # Trusted and binding-matched: eligible for temporal coherence (Q1).
            trusted_temporal_candidates[member_id].append(assessment)
            if definition is None:
                saw_member_unknown = True
                # member_defs already recorded the specific rejection reason.
                already = {
                    "member_rule_not_trusted_premise",
                    "caller_boolean_not_premise",
                    "malformed_input",
                    "member_rule_incomplete",
                    "member_rule_missing",
                    "reserved_key_in_member",
                    "member_definition_missing",
                    "member_definitions_missing",
                }
                if not already.intersection(reasons):
                    reasons.append("member_definition_missing")
                continue
            verdict, rule_reasons = _evaluate_member_rule(
                member_id,
                definition,
                assessment,
                evidence_index,
                evaluation_time,
                expected_reviewer_revision,
                expected_rule_revision,
            )
            reasons.extend(rule_reasons)
            if verdict == MEMBER_FAIL:
                saw_member_fail = True
            elif verdict == MEMBER_UNKNOWN:
                saw_member_unknown = True
            elif verdict == MEMBER_DISCHARGED:
                saw_discharged = True

        assessment_verdict: str | None = None
        if candidates:
            if saw_binding_mismatch or saw_member_fail:
                assessment_verdict = MEMBER_FAIL
            elif saw_discharged:
                assessment_verdict = MEMBER_DISCHARGED
            else:
                assessment_verdict = MEMBER_UNKNOWN

        na_verdict, na_reasons = _na_decision_for(
            member_id,
            document,
            binding_b0,
            evidence_index,
            evaluation_time,
            expected_reviewer_revision,
            expected_rule_revision,
        )

        if assessment_verdict == MEMBER_FAIL:
            member_verdicts[member_id] = MEMBER_FAIL
            # Retain NA justification/reasons as evidence alongside the fail.
            if na_verdict is not None:
                reasons.extend(na_reasons)
            continue
        if na_verdict is not None:
            member_verdicts[member_id] = na_verdict
            reasons.extend(na_reasons)
            continue
        if not candidates:
            member_verdicts[member_id] = MEMBER_MISSING
            reasons.append(f"missing_assessment:{member_id}")
            continue
        member_verdicts[member_id] = assessment_verdict or MEMBER_UNKNOWN

    # Diagnostic addressed coverage: members with any candidate assessment.
    # Missing assessment is diagnostic; NA without an assessment is still valid discharge.
    missing_members = [
        member_id
        for member_id in member_ids
        if member_id not in candidates_by_member
        and member_verdicts.get(member_id) != MEMBER_NA
    ]

    # Alias records never inflate required-member coverage (S06).
    # keep: alias_coverage_guard
    _ = assessments  # assessments already reconciled by qualified identity

    # Q6: only assessment-discharged members require demonstrated support times.
    # NA-discharged members are exempt from the common-snapshot obligation.
    assessment_discharged = [
        member_id
        for member_id in member_ids
        if member_verdicts.get(member_id) == MEMBER_DISCHARGED
    ]
    coherent, temporal_reasons = _support_times_coherent(
        trusted_temporal_candidates, assessment_discharged
    )
    reasons.extend(temporal_reasons)
    if not coherent and "temporal_support_incompatible_fail" in temporal_reasons:
        fail_conflict = True
    if not coherent and "applicability_violation_established" in temporal_reasons:
        fail_conflict = True
    if not coherent and "temporal_support_incoherent" in temporal_reasons:
        unknown_conflict = True
    if not coherent and "temporal_support_unverified" in temporal_reasons:
        unknown_conflict = True
    if "malformed_input" in temporal_reasons:
        fail_conflict = True
    if "time_unparsable" in temporal_reasons:
        unknown_conflict = True

    closure, reasons = _closure_from_reasons(
        reasons,
        member_verdicts,
        unresolved_dependencies,
        fail_conflict,
        unknown_conflict,
    )

    return outcome(
        closure,
        reasons,
        member_verdicts=member_verdicts,
        addressed_members=addressed,
        missing_members=missing_members,
        unresolved_dependencies=unresolved_dependencies,
        conflicts=conflicts,
        bindings={"b0": binding_b0},
    )


def evaluate_document(document: dict) -> dict:
    return seal_report(evaluate(document))


def load_json_path(path: Path) -> tuple[dict | None, dict | None]:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        return None, outcome(FAIL, ["input_unreadable"], detail=str(exc),
                             member_verdicts={}, addressed_members=[], missing_members=[],
                             unresolved_dependencies=[], conflicts=[], bindings={})
    if len(raw) > MAX_INPUT_BYTES:
        return None, outcome(FAIL, ["input_too_large"], detail=f"max {MAX_INPUT_BYTES} bytes",
                             member_verdicts={}, addressed_members=[], missing_members=[],
                             unresolved_dependencies=[], conflicts=[], bindings={})
    try:
        document = json.loads(raw.decode("utf-8"), object_pairs_hook=reject_duplicate_keys)
    except DuplicateKeyError as exc:
        return None, outcome(FAIL, ["duplicate_json_key"], detail=str(exc),
                             member_verdicts={}, addressed_members=[], missing_members=[],
                             unresolved_dependencies=[], conflicts=[], bindings={})
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        return None, outcome(FAIL, ["malformed_input"], detail=str(exc),
                             member_verdicts={}, addressed_members=[], missing_members=[],
                             unresolved_dependencies=[], conflicts=[], bindings={})
    if not isinstance(document, dict):
        return None, outcome(FAIL, ["malformed_input"], detail="document must be an object",
                             member_verdicts={}, addressed_members=[], missing_members=[],
                             unresolved_dependencies=[], conflicts=[], bindings={})
    return document, None


def exit_code_for(report: dict) -> int:
    verdict = report.get("closure_verdict")
    if verdict == PASS:
        return 0
    if verdict == FAIL:
        return 1
    if verdict == UNKNOWN:
        return 3
    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Finite Layer-S assessed-coverage oracle (synthetic semantics only).",
    )
    parser.add_argument("--input", required=True, help="Path to one JSON fixture snapshot")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        code = exc.code
        return code if isinstance(code, int) else 2
    path = Path(args.input)
    document, early = load_json_path(path)
    if early is not None:
        report = seal_report(early)
        print(json.dumps(report, indent=2, sort_keys=True))
        return exit_code_for(report)
    assert document is not None
    # Strip expected block so input expectations never shape the verdict.
    working = {key: value for key, value in document.items() if key != "expected"}
    report = evaluate_document(working)
    print(json.dumps(report, indent=2, sort_keys=True))
    return exit_code_for(report)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

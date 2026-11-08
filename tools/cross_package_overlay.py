#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Bounded producer-side preparation for a two-package cross-package relation overlay.

Draft model of reference/relations/CROSS-PACKAGE-OVERLAY.md section 3. This is
not a released wire schema, not independent scientific review, not production
validation, and not authorization or an execution grant. book-package/2 is
unchanged. Python standard library only.

Default deny: every unknown or missing field is a typed refusal. A passing
status is returned only after every A10 condition is positively established.
Rendition relation edges and non-canonical endpoints are out of scope (AC4).

NOT_MEASURED:
- live Muneral producer package admission or KCLIVE-08 task closure
- independent scientific peer review of candidate relations
- production authorization, delivery or durable effect identity
- rendition/K8 sidecar endpoint verification
- multi-package overlays beyond exactly two canonical English packages
- released cross-package-relations wire schema registration

CLI exit codes: 0 accepted/complete inspectable report, 1 typed refusal
(always with a JSON report), 2 usage, 3 incomplete-but-inspectable
(`inspectable_unresolved`). A missing report must never be read as pass.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, NamedTuple

SUPPORTED_PROFILE = "cross-package-relations/0.1"
CANONICAL_LANGUAGE = "en"
MAX_INPUT_BYTES = 256 * 1024
DIGEST_FIELDS = ("algorithm", "value", "byte_domain", "source_revision")
# Overlay §2 eight-part endpoint identity (all mandatory for inspection).
ENDPOINT_REQUIRED_STRING_FIELDS = (
    "package_id",
    "release_id",
    "component_id",
    "object_id",
    "representation_id",
    "source_anchor",
)
ENDPOINT_REQUIRED_FIELDS = ENDPOINT_REQUIRED_STRING_FIELDS  # compatibility alias
PACKAGE_ID_FIELDS = ("package_id", "release_id")
REQUIRED_PIN_KEYS = frozenset({"A", "B"})
PERMISSION_BOOL_FIELDS = ("permitted", "accessible", "revoked")
SHA256_HEX = re.compile(r"^[0-9a-f]{64}$")
ACCEPTED_REVIEW_VERDICTS = frozenset({"accepted"})
PASS_STATUSES = frozenset({
    "inspectable",
    "prerequisite_closure_complete",
    "accepted",
})
INCOMPLETE_STATUSES = frozenset({
    "inspectable_unresolved",
})
# Rendition relation edges are out of scope for this preparation (AC4).
RELATION_KINDS = frozenset({
    "quotes",
    "compares_with",
    "supports_under",
    "contradicts_under",
    "requires_for_use",
    "related_to",
})
PREMISE_OVERLAP_FIELDS = (
    ("units", "peer_units"),
    ("quantifier_scope", "peer_quantifier_scope"),
    ("conditions", "peer_conditions"),
    ("valid_time", "peer_valid_time"),
)
# Review records must not carry evaluator-output keys. Presence is malformed_input;
# those keys never shape the verdict and are never merged into a report.
REVIEW_OUTPUT_RESERVED_KEYS = frozenset({
    "status",
    "reason_code",
    "also_reason_code",
    "effects_authorized",
    "execution_granted",
    "proof_promoted",
    "bounded_preparation",
    "released_schema",
})
# Identity / binding fields that belong on reviews, never on sealed reports.
REPORT_FORBIDDEN_REVIEW_KEYS = frozenset({
    "reviewer",
    "author",
    "relation_id",
    "reviewed_edge_revision",
    "verdict",
    "independent",
    "pins",
    "pin_manifest_digests",
    "evidence",
    "scope",
})


class DuplicateKeyError(ValueError):
    """Raised when JSON object_pairs_hook sees a repeated key."""


class ReviewSelection(NamedTuple):
    """Tagged return from independent-review selection.

    Exactly one of ``refusal`` or ``review`` is set. Callers must branch on
    these fields — never on whether a dict contains ``status`` or similar
    caller-controlled keys.
    """

    refusal: dict | None = None
    review: dict | None = None

def reject_duplicate_keys(pairs: list[tuple[Any, Any]]) -> dict:
    result: dict = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def pins_complete(pins: Any) -> bool:
    return isinstance(pins, dict) and set(pins.keys()) == REQUIRED_PIN_KEYS


def permission_key(package_id: str, release_id: str) -> str:
    return f"{package_id}@{release_id}"


def _digest_tuple(digest: Any) -> tuple:
    if not isinstance(digest, dict):
        return (None, None, None, None)
    return (
        digest.get("algorithm"),
        digest.get("value"),
        digest.get("byte_domain"),
        digest.get("source_revision"),
    )


def endpoint_identity(endpoint: dict) -> tuple:
    return (
        endpoint.get("package_id"),
        _digest_tuple(endpoint.get("package_manifest_digest")),
        endpoint.get("release_id"),
        endpoint.get("component_id"),
        endpoint.get("object_id"),
        endpoint.get("representation_id"),
        _digest_tuple(endpoint.get("representation_digest")),
        endpoint.get("source_anchor"),
    )


def package_identity(package: dict) -> tuple:
    return (
        package.get("package_id"),
        package.get("release_id"),
        _digest_tuple(package.get("package_manifest_digest")),
    )


def outcome(status: str, reason_code: str, **fields: Any) -> dict:
    """Trusted result constructor: every emitted report is built here.

    Non-authorizing flags are fixed by the evaluator. Caller- or input-supplied
    values for those keys are ignored. Input review objects must never be
    returned or merged into a report.
    """
    report = {"status": status, "reason_code": reason_code}
    report.update(fields)
    # Fixed by the evaluator — never taken from input or **fields.
    report["bounded_preparation"] = True
    report["released_schema"] = False
    report["execution_granted"] = False
    report["proof_promoted"] = False
    report["effects_authorized"] = False
    return report


def refuse(reason_code: str, **fields: Any) -> dict:
    return outcome("refused", reason_code, **fields)


def seal_report(report: Any) -> dict:
    """Final trusted boundary before emission.

    Rebuilds through ``outcome`` so authority flags stay false and review-shaped
    keys cannot leak even if a future path mishandles an input object.
    """
    if not isinstance(report, dict):
        return refuse(
            "malformed_input",
            detail="evaluator produced a non-object report",
        )
    status = report.get("status")
    reason_code = report.get("reason_code")
    if not isinstance(status, str) or status == "":
        return refuse(
            "malformed_input",
            detail="evaluator report missing non-empty status",
        )
    if not isinstance(reason_code, str) or reason_code == "":
        return refuse(
            "malformed_input",
            detail="evaluator report missing non-empty reason_code",
        )
    extra = {
        key: value
        for key, value in report.items()
        if key not in ("status", "reason_code")
        and key not in REPORT_FORBIDDEN_REVIEW_KEYS
    }
    # outcome() re-fixes authority / preparation flags regardless of extras.
    return outcome(status, reason_code, **extra)
def digest_complete(digest: Any) -> bool:
    if not isinstance(digest, dict):
        return False
    return all(digest.get(field) not in (None, "") for field in DIGEST_FIELDS)


def digest_malformed(digest: Any, label: str = "package_manifest_digest") -> str | None:
    """Return a detail string when digest shape/type/format is malformed."""
    if digest is None:
        return None
    if not isinstance(digest, dict):
        return f"{label} must be an object"
    for field in DIGEST_FIELDS:
        if field not in digest:
            continue
        value = digest.get(field)
        if value in (None, ""):
            continue
        if not isinstance(value, str):
            return f"{label}.{field} must be a non-empty string"
        if field == "algorithm" and value != "sha256":
            return f"{label}.algorithm must be 'sha256'"
        if field == "value" and SHA256_HEX.fullmatch(value) is None:
            return f"{label}.value must be 64 lowercase hex characters"
    return None


def digests_equal(left: Any, right: Any) -> bool:
    """True only when both digests are complete, well-typed, and byte-identical.

    Missing or malformed fields on either side never count as equal.
    """
    if not digest_complete(left) or not digest_complete(right):
        return False
    if digest_malformed(left) is not None or digest_malformed(right) is not None:
        return False
    return _digest_tuple(left) == _digest_tuple(right)


def is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and value != ""


def require_non_empty_string(value: Any, label: str) -> dict | None:
    if value is None or value == "":
        return None
    if not isinstance(value, str):
        return refuse("malformed_input", detail=f"{label} must be a non-empty string")
    return None


def require_present_non_empty_string(value: Any, label: str) -> dict | None:
    """Refuse when a required identity is missing, empty, or not a string."""
    if not is_non_empty_string(value):
        return refuse("malformed_input", detail=f"{label} must be a non-empty string")
    return None


def path_type_malformed(owner: dict, label: str) -> dict | None:
    if "path" not in owner:
        return None
    if not isinstance(owner.get("path"), str):
        return refuse("malformed_input", detail=f"{label}.path must be a string when present")
    return None


def path_has_translations_segment(path: Any) -> bool:
    if path is None:
        return False
    if not isinstance(path, str):
        return False
    normalized = path.replace("\\", "/").lower()
    return any(segment == "translations" for segment in normalized.split("/") if segment)


def is_canonical_english_package(package: dict) -> bool:
    return package.get("language") == CANONICAL_LANGUAGE and package.get("canonical") is True


def package_rendition_qualified(package: dict) -> bool:
    """True when the package affirmatively declares a non-canonical/rendition side."""
    language = package.get("language")
    if language is not None and language != CANONICAL_LANGUAGE:
        return True
    if package.get("canonical") is False:
        return True
    if path_has_translations_segment(package.get("path")):
        return True
    return False


def validate_package_representations(package: dict, label: str) -> dict | None:
    """Require package.representations map (KC-SWE interpretation of overlay §2).

    Pending KC-Brain confirmation: endpoint representation identity resolves against
    what the pinned package declares, not an invented literal id vocabulary.
    """
    reps = package.get("representations")
    if not isinstance(reps, dict) or len(reps) == 0:
        return refuse(
            "malformed_input",
            side=label,
            detail=(
                f"package {label} requires a non-empty representations map: "
                "representation_id -> {representation_digest, language}"
            ),
        )
    for rep_id, entry in reps.items():
        if not isinstance(rep_id, str) or rep_id == "":
            return refuse(
                "malformed_input",
                side=label,
                detail=f"package {label} representations keys must be non-empty strings",
            )
        if not isinstance(entry, dict):
            return refuse(
                "malformed_input",
                side=label,
                detail=f"package {label} representations[{rep_id!r}] must be an object",
            )
        digest = entry.get("representation_digest")
        digest_bad = digest_malformed(digest, f"packages.{label}.representations[{rep_id}].representation_digest")
        if digest_bad is not None:
            return refuse("malformed_input", side=label, detail=digest_bad)
        if not digest_complete(digest):
            return refuse(
                "malformed_input",
                side=label,
                detail=(
                    f"package {label} representations[{rep_id!r}].representation_digest "
                    "requires algorithm, value, byte_domain, source_revision"
                ),
            )
        if digest.get("source_revision") != package.get("release_id"):
            return refuse(
                "malformed_input",
                side=label,
                detail=(
                    f"package {label} representations[{rep_id!r}].representation_digest."
                    "source_revision must equal package release_id"
                ),
            )
        language = entry.get("language")
        if not isinstance(language, str) or language == "":
            return refuse(
                "malformed_input",
                side=label,
                detail=f"package {label} representations[{rep_id!r}].language must be a non-empty string",
            )
        if language != CANONICAL_LANGUAGE:
            return refuse(
                "rendition_endpoint_refused",
                side=label,
                representation_id=rep_id,
                detail=(
                    "G11 preparation accepts only canonical English representations "
                    "(declared representation language must be 'en')"
                ),
            )
    return None


def bind_endpoint_representation(endpoint: dict, package: dict, label: str) -> dict | None:
    """Refuse when endpoint representation is not the package-declared binding."""
    reps = package.get("representations")
    if not isinstance(reps, dict):
        return refuse(
            "malformed_input",
            side=label,
            detail=f"package for endpoint {label} lacks representations map",
        )
    rep_id = endpoint.get("representation_id")
    declared = reps.get(rep_id)
    if not isinstance(declared, dict):
        return refuse(
            "representation_identity_mismatch",
            side=label,
            representation_id=rep_id,
            detail="endpoint representation_id must be a key in its package representations map",
        )
    declared_digest = declared.get("representation_digest")
    endpoint_digest = endpoint.get("representation_digest")
    if not digests_equal(endpoint_digest, declared_digest):
        return refuse(
            "representation_identity_mismatch",
            side=label,
            representation_id=rep_id,
            detail="endpoint representation_digest must equal the package-declared digest for that id",
        )
    declared_language = declared.get("language")
    endpoint_language = endpoint.get("language")
    if endpoint_language not in (None, "") and endpoint_language != declared_language:
        return refuse(
            "rendition_endpoint_refused",
            side=label,
            detail="endpoint.language must equal the package-declared representation language",
        )
    return None


def pins_equal(left: Any, right: Any) -> bool:
    """True only when both pins carry non-empty string A/B releases that match.

    Missing, empty, or non-string values on either side never count as equal.
    """
    if not pins_complete(left) or not pins_complete(right):
        return False
    for side in ("A", "B"):
        lv = left.get(side)
        rv = right.get(side)
        if not is_non_empty_string(lv) or not is_non_empty_string(rv):
            return False
        if lv != rv:
            return False
    return True


def permission_flags_malformed(state: dict) -> bool:
    """True when any required permission flag is missing or not a real boolean."""
    for field in PERMISSION_BOOL_FIELDS:
        if field not in state or not isinstance(state.get(field), bool):
            return True
    return False


def review_is_self_authored(review: dict, overlay: dict, pkg_a: dict, pkg_b: dict) -> bool:
    """Refuse when reviewer equals a stated author, or author is stated without reviewer."""
    reviewer = review.get("reviewer")
    review_author = review.get("author")
    package_authors = [
        source for source in (overlay.get("author"), pkg_a.get("author"), pkg_b.get("author"))
        if is_non_empty_string(source)
    ]
    if is_non_empty_string(review_author):
        if not is_non_empty_string(reviewer):
            return True
        if reviewer == review_author:
            return True
    if is_non_empty_string(reviewer) and reviewer in package_authors:
        return True
    return False


def evaluate(overlay: dict, context: dict) -> dict:
    """Evaluate one candidate overlay record plus explicit consumer context."""
    try:
        return _evaluate(overlay, context)
    except Exception as exc:  # noqa: BLE001 — never raise on any JSON value
        return refuse(
            "malformed_input",
            detail=f"unexpected evaluation error: {type(exc).__name__}: {exc}",
        )


def _evaluate(overlay: dict, context: dict) -> dict:
    """Inner evaluator; callers use evaluate() which refuses on unexpected errors."""
    if not isinstance(overlay, dict) or not isinstance(context, dict):
        return refuse("malformed_input", detail="overlay and context must be objects")

    profile = overlay.get("overlay_profile")
    if profile != SUPPORTED_PROFILE:
        return refuse(
            "unsupported_profile",
            requested_profile=profile,
            supported_profile=SUPPORTED_PROFILE,
            permissive_fallback=False,
        )

    packages = overlay.get("packages")
    if not isinstance(packages, dict) or set(packages) != {"A", "B"}:
        return refuse("malformed_input", detail="packages must contain exactly A and B")
    pkg_a = packages.get("A")
    pkg_b = packages.get("B")
    if not isinstance(pkg_a, dict) or not isinstance(pkg_b, dict):
        return refuse("malformed_input", detail="package A and B must be objects")

    # Two DISTINCT packages are required; a same-id revision pair belongs to A6, not overlay.
    for label, package in (("A", pkg_a), ("B", pkg_b)):
        for field in PACKAGE_ID_FIELDS:
            value = package.get(field)
            if value is None or value == "":
                return refuse("malformed_input", detail=f"package {label} requires non-empty {field}")
            bad = require_non_empty_string(value, f"packages.{label}.{field}")
            if bad is not None:
                return bad
        path_bad = path_type_malformed(package, f"packages.{label}")
        if path_bad is not None:
            return path_bad
        digest = package.get("package_manifest_digest")
        digest_bad = digest_malformed(digest)
        if digest_bad is not None:
            return refuse("malformed_input", side=label, detail=digest_bad)
        if not digest_complete(digest):
            return refuse(
                "incomplete_release_pin",
                side=label,
                detail="each package requires package_manifest_digest with algorithm, value, byte_domain, source_revision",
            )
        reps_bad = validate_package_representations(package, label)
        if reps_bad is not None:
            return reps_bad

    if pkg_a.get("package_id") == pkg_b.get("package_id"):
        return refuse(
            "same_package_both_sides",
            package_id=pkg_a.get("package_id"),
            detail="cross-package overlay requires two distinct package_id values",
        )
    if package_identity(pkg_a) == package_identity(pkg_b):
        return refuse("same_package_both_sides", package_identity=list(package_identity(pkg_a)))

    if package_rendition_qualified(pkg_a) or package_rendition_qualified(pkg_b):
        return refuse(
            "rendition_endpoint_refused",
            detail="only canonical English package endpoints are accepted in this preparation",
        )
    if not is_canonical_english_package(pkg_a) or not is_canonical_english_package(pkg_b):
        return refuse(
            "canonical_language_required",
            detail="both packages must affirmatively assert language='en' and canonical=true",
        )

    relation = overlay.get("relation")
    if not isinstance(relation, dict):
        return refuse("malformed_input", detail="relation must be an object")
    kind = relation.get("kind")
    if kind == "rendition_of":
        return refuse(
            "rendition_endpoint_refused",
            detail="rendition relation edges are out of scope for this preparation (AC4)",
        )
    if not isinstance(kind, str) or kind not in RELATION_KINDS:
        return refuse("malformed_input", detail=f"unsupported relation kind: {kind!r}")

    from_ep = relation.get("from")
    to_ep = relation.get("to")
    if not isinstance(from_ep, dict) or not isinstance(to_ep, dict):
        return refuse("malformed_input", detail="from and to endpoints required")

    for label, endpoint in (("from", from_ep), ("to", to_ep)):
        path_bad = path_type_malformed(endpoint, f"relation.{label}")
        if path_bad is not None:
            return path_bad
        missing = []
        for field in ENDPOINT_REQUIRED_STRING_FIELDS:
            value = endpoint.get(field)
            if value is None or value == "":
                missing.append(field)
                continue
            bad = require_non_empty_string(value, f"relation.{label}.{field}")
            if bad is not None:
                return bad
        ep_digest = endpoint.get("package_manifest_digest")
        rep_digest = endpoint.get("representation_digest")
        if ep_digest is None or ep_digest == "":
            missing.append("package_manifest_digest")
        if rep_digest is None or rep_digest == "":
            missing.append("representation_digest")
        if missing:
            return refuse(
                "incomplete_release_pin",
                side=label,
                missing_fields=missing,
                detail=(
                    "endpoint requires the complete eight-part identity: package_id, "
                    "package_manifest_digest, release_id, component_id, object_id, "
                    "representation_id, representation_digest, source_anchor"
                ),
            )
        digest_bad = digest_malformed(ep_digest, "package_manifest_digest")
        if digest_bad is not None:
            return refuse("malformed_input", side=label, detail=digest_bad)
        if not digest_complete(ep_digest):
            return refuse(
                "incomplete_release_pin",
                side=label,
                missing_fields=["package_manifest_digest"],
                detail="endpoint package_manifest_digest requires algorithm, value, byte_domain, source_revision",
            )
        rep_bad = digest_malformed(rep_digest, "representation_digest")
        if rep_bad is not None:
            return refuse("malformed_input", side=label, detail=rep_bad)
        if not digest_complete(rep_digest):
            return refuse(
                "incomplete_release_pin",
                side=label,
                missing_fields=["representation_digest"],
                detail="endpoint representation_digest requires algorithm, value, byte_domain, source_revision",
            )
        if rep_digest.get("source_revision") != endpoint.get("release_id"):
            return refuse(
                "representation_identity_mismatch",
                side=label,
                detail="representation_digest.source_revision must equal endpoint release_id",
            )

    if path_has_translations_segment(from_ep.get("path")) or path_has_translations_segment(to_ep.get("path")):
        return refuse(
            "rendition_endpoint_refused",
            detail="endpoint path segment 'translations' is out of scope",
        )

    # from must match package A; to must match package B exactly (id before digest).
    if from_ep.get("package_id") != pkg_a.get("package_id") or from_ep.get("release_id") != pkg_a.get("release_id"):
        return refuse(
            "endpoint_package_mismatch",
            side="from",
            detail="from endpoint must match package A package_id and release_id",
        )
    if to_ep.get("package_id") != pkg_b.get("package_id") or to_ep.get("release_id") != pkg_b.get("release_id"):
        return refuse(
            "endpoint_package_mismatch",
            side="to",
            detail="to endpoint must match package B package_id and release_id",
        )
    if not digests_equal(from_ep.get("package_manifest_digest"), pkg_a.get("package_manifest_digest")):
        return refuse(
            "endpoint_digest_mismatch",
            side="from",
            detail="endpoint package_manifest_digest must equal its package digest",
        )
    if not digests_equal(to_ep.get("package_manifest_digest"), pkg_b.get("package_manifest_digest")):
        return refuse(
            "endpoint_digest_mismatch",
            side="to",
            detail="endpoint package_manifest_digest must equal its package digest",
        )

    # Representation identity resolves against the matched package declaration (§2 / R1).
    bind_from = bind_endpoint_representation(from_ep, pkg_a, "from")
    if bind_from is not None:
        return bind_from
    bind_to = bind_endpoint_representation(to_ep, pkg_b, "to")
    if bind_to is not None:
        return bind_to

    id_from = endpoint_identity(from_ep)
    id_to = endpoint_identity(to_ep)
    identities = [list(id_from), list(id_to)]

    grounding_raw = relation.get("grounding")
    if grounding_raw is None:
        grounding: dict = {}
    elif not isinstance(grounding_raw, dict):
        return refuse("malformed_input", detail="relation.grounding must be an object when present")
    else:
        grounding = grounding_raw

    from_anchor = grounding.get("from_anchor")
    to_anchor = grounding.get("to_anchor")
    if kind == "contradicts_under":
        # A4: missing side stays one_sided_contradiction; present anchors must match endpoints.
        if from_anchor not in (None, "") and to_anchor not in (None, ""):
            if not isinstance(from_anchor, str) or not isinstance(to_anchor, str):
                return refuse(
                    "malformed_input",
                    detail="grounding.from_anchor and grounding.to_anchor must be strings",
                )
            if from_anchor != from_ep.get("source_anchor") or to_anchor != to_ep.get("source_anchor"):
                return refuse(
                    "malformed_input",
                    detail="grounding anchors must equal endpoint source_anchor values",
                )
    else:
        if not isinstance(grounding_raw, dict):
            return refuse(
                "malformed_input",
                detail="relation.grounding with from_anchor and to_anchor is required",
            )
        if not isinstance(from_anchor, str) or not from_anchor or not isinstance(to_anchor, str) or not to_anchor:
            return refuse(
                "malformed_input",
                detail="grounding.from_anchor and grounding.to_anchor must be non-empty strings",
            )
        if from_anchor != from_ep.get("source_anchor") or to_anchor != to_ep.get("source_anchor"):
            return refuse(
                "malformed_input",
                detail="grounding anchors must equal endpoint source_anchor values",
            )

    assertions = relation.get("assertions") if isinstance(relation.get("assertions"), dict) else {}
    lineage = relation.get("lineage") if isinstance(relation.get("lineage"), list) else []
    assessment = overlay.get("assessment") if isinstance(overlay.get("assessment"), dict) else {}

    request_pins = context.get("request_pins")
    if not pins_complete(request_pins):
        return refuse(
            "request_pin_mismatch",
            request_pins=request_pins if isinstance(request_pins, dict) else None,
            detail="request_pins must contain exactly keys A and B",
        )
    overlay_pins = {"A": pkg_a.get("release_id"), "B": pkg_b.get("release_id")}
    if not pins_equal(request_pins, overlay_pins):
        return refuse(
            "request_pin_mismatch",
            request_pins=dict(request_pins),
            overlay_pins=overlay_pins,
            detail="request_pins must select exactly the releases the overlay packages describe",
        )

    permissions = context.get("permissions") if isinstance(context.get("permissions"), dict) else {}
    reviews = context.get("reviews") if isinstance(context.get("reviews"), list) else []
    published = context.get("published_releases") if isinstance(context.get("published_releases"), list) else []
    mandatory = context.get("mandatory_dependencies")
    task_requirements = context.get("task_requirements")
    unit_scope_aligned = context.get("unit_scope_aligned")

    def pin_state(side: str, package: dict) -> dict:
        release = request_pins.get(side)
        key = permission_key(package["package_id"], release)
        state = permissions.get(key)
        if not isinstance(state, dict):
            return {"permitted": False, "revoked": False, "accessible": False, "missing": True}
        return state

    state_a = pin_state("A", pkg_a)
    state_b = pin_state("B", pkg_b)

    reviewed_pins = assessment.get("reviewed_pins") if isinstance(assessment.get("reviewed_pins"), dict) else {}

    def require_current_permissions() -> dict | None:
        """Affirmative permitted+accessible and not revoked for BOTH pins."""
        for side, state in (("A", state_a), ("B", state_b)):
            if state.get("missing") is True:
                return refuse(
                    "endpoint_not_permitted",
                    side=side,
                    detail="current permission must affirmatively be permitted=true and accessible=true",
                )
            if permission_flags_malformed(state):
                return refuse(
                    "malformed_input",
                    side=side,
                    detail="permitted, accessible and revoked must all be present real booleans",
                )
            if state.get("revoked") is True:
                return refuse(
                    "current_use_revoked",
                    side=side,
                    historical_record_retained=bool(state.get("historically_inspectable", True)),
                )
            if state.get("accessible") is not True:
                return refuse("endpoint_inaccessible", side=side)
            if state.get("permitted") is not True:
                return refuse(
                    "endpoint_not_permitted",
                    side=side,
                    detail="current permission must affirmatively be permitted=true and accessible=true",
                )
        return None

    def require_independent_review(
        *, as_unresolved_when_missing: bool = False,
    ) -> ReviewSelection:
        """A10/R2: independent scoped review bound to this exact edge and manifest bytes.

        Returns a tagged ``ReviewSelection``: either an evaluator refusal/outcome
        or the accepted input review. Callers must not infer the kind from dict
        keys such as ``status``.
        """
        def as_refusal(report: dict) -> ReviewSelection:
            return ReviewSelection(refusal=report, review=None)

        def as_review(selected: dict) -> ReviewSelection:
            return ReviewSelection(refusal=None, review=selected)

        for review in reviews:
            if not isinstance(review, dict):
                continue
            pins = review.get("pins")
            if pins is None:
                continue
            if not pins_complete(pins):
                return as_refusal(refuse(
                    "request_pin_mismatch",
                    review_pins=pins if isinstance(pins, dict) else None,
                    detail="review pins must contain exactly keys A and B",
                ))
        matching = [
            review for review in reviews
            if isinstance(review, dict) and pins_equal(review.get("pins"), request_pins)
        ]
        if not matching:
            if reviewed_pins and not pins_equal(reviewed_pins, request_pins):
                return as_refusal(refuse(
                    "review_pin_mismatch",
                    reviewed_pins=reviewed_pins,
                    request_pins=request_pins,
                    detail="reviewed A1/B1 pair cannot discharge a request that selects a different pin",
                ))
            if as_unresolved_when_missing:
                return as_refusal(outcome(
                    "inspectable_unresolved",
                    "no_bound_edge_review",
                    endpoint_identities=identities,
                    detail="contradicts_under retention requires a bound independent review of this edge",
                ))
            return as_refusal(refuse(
                "review_missing",
                detail="independent scoped review whose pins equal the request pins is required",
            ))
        # Reject pin-matching reviews that smuggle evaluator-output keys.
        for review in matching:
            reserved = sorted(REVIEW_OUTPUT_RESERVED_KEYS.intersection(review))
            if reserved:
                return as_refusal(refuse(
                    "malformed_input",
                    reserved_keys=reserved,
                    detail=(
                        "review must not carry evaluator output-reserved keys; "
                        f"found {reserved}"
                    ),
                ))
        # Typed edge identities before equality: overlay side must be present
        # non-empty strings; a review missing typed identity cannot bind.
        expected_revision = overlay.get("overlay_revision")
        expected_relation_id = relation.get("relation_id")
        revision_bad = require_present_non_empty_string(
            expected_revision, "overlay_revision",
        )
        if revision_bad is not None:
            return as_refusal(revision_bad)
        relation_bad = require_present_non_empty_string(
            expected_relation_id, "relation.relation_id",
        )
        if relation_bad is not None:
            return as_refusal(relation_bad)
        bound = []
        for review in matching:
            review_relation_id = review.get("relation_id")
            review_revision = review.get("reviewed_edge_revision")
            if not is_non_empty_string(review_relation_id):
                continue
            if not is_non_empty_string(review_revision):
                continue
            if (
                review_relation_id == expected_relation_id
                and review_revision == expected_revision
            ):
                bound.append(review)
        if not bound:
            if as_unresolved_when_missing:
                return as_refusal(outcome(
                    "inspectable_unresolved",
                    "no_bound_edge_review",
                    endpoint_identities=identities,
                    detail="no pin-matching review is bound to this relation_id and reviewed_edge_revision",
                ))
            return as_refusal(refuse(
                "review_edge_mismatch",
                detail=(
                    "among pin-matching reviews, none bind relation_id and "
                    "reviewed_edge_revision to the evaluated edge"
                ),
            ))
        verdicts = {review.get("verdict") for review in bound}
        if len(verdicts) > 1:
            return as_refusal(refuse(
                "review_verdict_conflict",
                verdicts=sorted(str(item) for item in verdicts),
                detail="multiple bound reviews for this edge disagree on verdict",
            ))
        matched = bound[0]
        reviewer = matched.get("reviewer")
        if not isinstance(reviewer, str) or reviewer == "":
            if as_unresolved_when_missing:
                return as_refusal(outcome(
                    "inspectable_unresolved",
                    "no_bound_edge_review",
                    endpoint_identities=identities,
                    detail="bound review requires a non-empty string reviewer identity",
                ))
            return as_refusal(refuse(
                "review_missing",
                detail="matching review requires a present non-empty string reviewer identity",
            ))
        if matched.get("independent") is not True:
            return as_refusal(refuse(
                "review_not_independent",
                detail="matching review must affirmatively set independent=true",
            ))
        if review_is_self_authored(matched, overlay, pkg_a, pkg_b):
            return as_refusal(refuse(
                "review_not_independent",
                detail="reviewer identity must be present and distinct from author / package author",
            ))
        relation_author = overlay.get("author")
        if is_non_empty_string(relation_author) and reviewer == relation_author:
            return as_refusal(refuse(
                "review_not_independent",
                detail="reviewer must differ from the overlay/relation author",
            ))
        verdict = matched.get("verdict")
        if verdict not in ACCEPTED_REVIEW_VERDICTS:
            return as_refusal(refuse(
                "review_not_accepted",
                verdict=verdict,
                detail="matching review verdict must be accepted",
            ))
        expected_scope = assessment.get("scope")
        review_scope = matched.get("scope")
        if not is_non_empty_string(review_scope):
            return as_refusal(refuse(
                "review_scope_incompatible",
                review_scope=review_scope,
                assessment_scope=expected_scope,
                detail="review scope must be a present non-empty string compatible with the assessed edge scope",
            ))
        if expected_scope not in (None, ""):
            if not is_non_empty_string(expected_scope):
                return as_refusal(refuse(
                    "malformed_input",
                    detail="assessment.scope must be a non-empty string when present",
                ))
            if review_scope != expected_scope:
                return as_refusal(refuse(
                    "review_scope_incompatible",
                    review_scope=review_scope,
                    assessment_scope=expected_scope,
                    detail="review scope must be present and compatible with the assessed edge scope",
                ))
        pin_digests = matched.get("pin_manifest_digests")
        if not isinstance(pin_digests, dict) or set(pin_digests.keys()) != REQUIRED_PIN_KEYS:
            return as_refusal(refuse(
                "review_pin_mismatch",
                detail="review pin_manifest_digests must contain exact keys A and B",
            ))
        if not digests_equal(pin_digests.get("A"), pkg_a.get("package_manifest_digest")):
            return as_refusal(refuse(
                "review_pin_mismatch",
                side="A",
                detail="review pin_manifest_digests.A must equal package A manifest bytes",
            ))
        if not digests_equal(pin_digests.get("B"), pkg_b.get("package_manifest_digest")):
            return as_refusal(refuse(
                "review_pin_mismatch",
                side="B",
                detail="review pin_manifest_digests.B must equal package B manifest bytes",
            ))
        return as_review(matched)
    def bound_incompatibility_evidence(review: dict) -> str | None:
        evidence = review.get("evidence")
        if isinstance(evidence, str) and evidence.strip():
            return evidence.strip()
        return None

    def mandatory_closure_result() -> dict | None:
        """A9: closure is complete only against a trusted requirements revision R."""
        # Absent requirements and absent discharges: no A9 claim.
        if task_requirements is None and mandatory is None:
            return None

        if task_requirements is None:
            return outcome(
                "inspectable_unresolved",
                "requirements_revision_missing",
                endpoint_identities=identities,
                use_closure_complete=False,
                external_effects=0,
                unresolved_mandatory=True,
                effects_authorized=False,
                detail="caller discharges alone cannot prove closure without trusted requirements revision R",
            )
        if not isinstance(task_requirements, dict):
            return refuse(
                "malformed_input",
                detail="task_requirements must be an object with revision and members",
            )

        revision = task_requirements.get("revision")
        members = task_requirements.get("members")
        empty_justification = task_requirements.get("empty_set_justification")
        if not isinstance(revision, str) or not revision.strip():
            return outcome(
                "inspectable_unresolved",
                "requirements_revision_missing",
                endpoint_identities=identities,
                use_closure_complete=False,
                external_effects=0,
                unresolved_mandatory=True,
                effects_authorized=False,
                detail="task_requirements.revision R must be a non-empty string",
            )
        if not isinstance(members, list):
            return refuse(
                "malformed_input",
                detail="task_requirements.members must be a list of qualified member identity strings",
            )
        for member in members:
            if not isinstance(member, str) or not member:
                return refuse(
                    "malformed_input",
                    detail="each task_requirements.members entry must be a non-empty string",
                )
        if len(members) != len(set(members)):
            return refuse(
                "malformed_input",
                detail="task_requirements.members must not contain duplicate qualified identities",
            )

        if len(members) == 0:
            if not isinstance(empty_justification, str) or not empty_justification.strip():
                return outcome(
                    "inspectable_unresolved",
                    "use_closure_incomplete",
                    endpoint_identities=identities,
                    use_closure_complete=False,
                    external_effects=0,
                    unresolved_mandatory=True,
                    effects_authorized=False,
                    requirements_revision=revision,
                    detail=(
                        "explicit empty requirements set requires non-empty "
                        "empty_set_justification; absent set is a missing task_requirements key"
                    ),
                )
            if mandatory is None:
                discharges: list = []
            elif not isinstance(mandatory, list):
                return refuse(
                    "malformed_input",
                    detail="mandatory_dependencies must be a list when present",
                )
            else:
                discharges = mandatory
            if discharges:
                return outcome(
                    "inspectable_unresolved",
                    "requirements_unknown_member",
                    endpoint_identities=identities,
                    use_closure_complete=False,
                    external_effects=0,
                    unresolved_mandatory=True,
                    effects_authorized=False,
                    requirements_revision=revision,
                    detail="justified empty requirements set cannot carry discharge members",
                )
            return outcome(
                "prerequisite_closure_complete",
                "prerequisite_closure_complete",
                endpoint_identities=identities,
                use_closure_complete=True,
                effects_authorized=False,
                requirements_revision=revision,
                empty_requirements_set=True,
                detail="consequential effects still require current authority, delivery and durable effect identity",
            )

        if mandatory is None:
            return outcome(
                "inspectable_unresolved",
                "use_closure_incomplete",
                endpoint_identities=identities,
                use_closure_complete=False,
                external_effects=0,
                unresolved_mandatory=True,
                effects_authorized=False,
                requirements_revision=revision,
                omitted_members=list(members),
                detail="requirements members are present but no discharge list was supplied",
            )
        if not isinstance(mandatory, list):
            return refuse(
                "malformed_input",
                detail="mandatory_dependencies must be a list of objects with id and boolean discharged",
            )

        seen_ids: list[str] = []
        for item in mandatory:
            if not isinstance(item, dict):
                return refuse(
                    "malformed_input",
                    detail="each mandatory_dependencies member must be an object with id and boolean discharged",
                )
            member_id = item.get("id")
            if not isinstance(member_id, str) or not member_id:
                return refuse(
                    "malformed_input",
                    detail="each mandatory_dependencies member requires a non-empty id",
                )
            if not isinstance(item.get("discharged"), bool):
                return refuse(
                    "malformed_input",
                    detail="mandatory_dependencies.discharged must be a real boolean",
                )
            seen_ids.append(member_id)

        required = set(members)
        discharge_ids = set(seen_ids)
        if len(seen_ids) != len(discharge_ids):
            return outcome(
                "inspectable_unresolved",
                "requirements_member_duplicate_discharge",
                endpoint_identities=identities,
                use_closure_complete=False,
                external_effects=0,
                unresolved_mandatory=True,
                effects_authorized=False,
                requirements_revision=revision,
                detail="duplicate discharge aliases cannot stand in for distinct required members",
            )
        unknown = sorted(discharge_ids - required)
        if unknown:
            return outcome(
                "inspectable_unresolved",
                "requirements_unknown_member",
                endpoint_identities=identities,
                use_closure_complete=False,
                external_effects=0,
                unresolved_mandatory=True,
                effects_authorized=False,
                requirements_revision=revision,
                unknown_members=unknown,
            )
        omitted = sorted(required - discharge_ids)
        if omitted:
            return outcome(
                "inspectable_unresolved",
                "use_closure_incomplete",
                endpoint_identities=identities,
                use_closure_complete=False,
                external_effects=0,
                unresolved_mandatory=True,
                effects_authorized=False,
                requirements_revision=revision,
                omitted_members=omitted,
            )

        missing_witness = []
        unresolved = []
        for item in mandatory:
            if item.get("discharged") is not True:
                unresolved.append(item)
                continue
            witness = item.get("witness_ref")
            if not isinstance(witness, str) or not witness.strip():
                missing_witness.append(item.get("id"))
        if missing_witness:
            return outcome(
                "inspectable_unresolved",
                "discharge_witness_missing",
                endpoint_identities=identities,
                use_closure_complete=False,
                external_effects=0,
                unresolved_mandatory=True,
                effects_authorized=False,
                requirements_revision=revision,
                members_missing_witness=missing_witness,
                detail=(
                    "discharged:true requires a non-empty witness_ref reference; "
                    "the reference is recorded, not proof of admission (NOT_MEASURED)"
                ),
            )
        if unresolved:
            return outcome(
                "inspectable_unresolved",
                "use_closure_incomplete",
                endpoint_identities=identities,
                use_closure_complete=False,
                external_effects=0,
                unresolved_members=unresolved,
                unresolved_mandatory=True,
                effects_authorized=False,
                requirements_revision=revision,
            )
        return outcome(
            "prerequisite_closure_complete",
            "prerequisite_closure_complete",
            endpoint_identities=identities,
            use_closure_complete=True,
            # Preparation never authorizes effects (overlay §6 A9b).
            effects_authorized=False,
            requirements_revision=revision,
            detail="consequential effects still require current authority, delivery and durable effect identity",
        )

    def prefer_unresolved_mandatory(primary: dict) -> dict:
        """Early returns keep an unresolved mandatory reason when one exists."""
        # Typed refusals (access, malformed identity, one-sided) stay refusals.
        if primary.get("status") == "refused":
            return primary
        mandatory_report = mandatory_closure_result()
        if mandatory_report is None:
            return primary
        if mandatory_report.get("status") == "refused":
            return mandatory_report
        if mandatory_report.get("reason_code") == "prerequisite_closure_complete":
            # Complete closure does not override an independent A5/A3 outcome.
            return primary
        # Incomplete mandatory wins as the exit reason, preserving the primary code.
        report = dict(mandatory_report)
        report["unresolved_mandatory"] = True
        if primary.get("reason_code") and primary.get("reason_code") != report.get("reason_code"):
            report["also_reason_code"] = primary.get("reason_code")
        if primary.get("both_facts_retained") is True:
            report["both_facts_retained"] = True
        if "endpoint_identities" not in report and "endpoint_identities" in primary:
            report["endpoint_identities"] = primary["endpoint_identities"]
        return report

    # A6b early: assessment/review pins that disagree with the request.
    if reviewed_pins:
        if not pins_complete(reviewed_pins) or not pins_equal(reviewed_pins, request_pins):
            return refuse(
                "review_pin_mismatch",
                reviewed_pins=reviewed_pins,
                request_pins=request_pins,
                detail="reviewed A1/B1 pair cannot discharge a request that selects a different pin",
            )

    # Current permission is required before every positive / inspectable branch.
    permission_refusal = require_current_permissions()
    if permission_refusal is not None:
        return permission_refusal

    # A4 / A5: contradiction path. Review binding is evaluated inside so a missing
    # bound review becomes inspectable_unresolved rather than a hard refuse.
    if kind == "contradicts_under":
        if not from_anchor or not to_anchor:
            missing = "from" if not from_anchor else "to"
            return refuse(
                "one_sided_contradiction",
                missing_side=missing,
                candidate_preserved=True,
            )
        # KC-SWE field map (coordinator Round 7): common applicability domain is
        # nonempty common_assumption only — not assertions.conditions.
        common_assumption = assertions.get("common_assumption")
        if common_assumption in (None, ""):
            common_assumption = grounding.get("common_assumption")
        harmonized = assertions.get("harmonized") is True
        if not isinstance(common_assumption, str) or not common_assumption.strip():
            return prefer_unresolved_mandatory(outcome(
                "inspectable_unresolved",
                "common_assumption_missing",
                endpoint_identities=identities,
                both_facts_retained=True,
                detail=(
                    "contradicts_under retention requires a non-empty common_assumption "
                    "domain on the relation (assertions or grounding); conditions is an "
                    "overlap pair, not the domain field"
                ),
            ))
        common_assumption = common_assumption.strip()
        missing_overlap = []
        unequal_overlap = []
        for left_key, right_key in PREMISE_OVERLAP_FIELDS:
            left = assertions.get(left_key)
            right = assertions.get(right_key)
            # Missing/empty/non-string on either side is unproven overlap, never equality.
            if not is_non_empty_string(left) or not is_non_empty_string(right):
                if not is_non_empty_string(right):
                    missing_overlap.append(right_key)
                else:
                    missing_overlap.append(left_key)
                continue
            if left != right:
                unequal_overlap.append(right_key)
        if unequal_overlap:
            # Unequal context is unsupported alignment, not a typed refusal that
            # the statements cannot conflict (KC-Brain / Agent-Brain A5).
            return prefer_unresolved_mandatory(outcome(
                "inspectable_unresolved",
                "premise_alignment_unsupported",
                endpoint_identities=identities,
                mismatched_fields=unequal_overlap,
                both_facts_retained=True,
                detail=(
                    "unequal unit/time/scope/conditions pairs mean unsupported premise "
                    "alignment in this preparation, not proof that no conflict exists"
                ),
            ))
        if missing_overlap or not harmonized:
            return prefer_unresolved_mandatory(outcome(
                "inspectable_unresolved",
                "premise_overlap_unproven",
                endpoint_identities=identities,
                missing_fields=missing_overlap,
                harmonized_assertion=harmonized,
                both_facts_retained=True,
                detail=(
                    "harmonized:true is an author assertion, not proof; affirmative "
                    "peer overlap fields are required"
                ),
            ))
        review_selection = require_independent_review(as_unresolved_when_missing=True)
        if review_selection.refusal is not None:
            return prefer_unresolved_mandatory(review_selection.refusal)
        matched_review = review_selection.review
        if not isinstance(matched_review, dict):
            return prefer_unresolved_mandatory(refuse(
                "malformed_input",
                detail="internal review selection returned neither refusal nor review",
            ))
        if bound_incompatibility_evidence(matched_review) is None:
            return prefer_unresolved_mandatory(outcome(
                "inspectable_unresolved",
                "no_bound_incompatibility_assessment",
                endpoint_identities=identities,
                both_facts_retained=True,
                detail=(
                    "retained contradicts_under requires a non-empty evidence string on "
                    "the R2-bound accepted review explaining why both propositions cannot "
                    "hold in the common_assumption domain; the evaluator validates record "
                    "presence and binding only and does not prove natural-language "
                    "incompatibility"
                ),
            ))
        return prefer_unresolved_mandatory(outcome(
            "inspectable",
            "contradicts_under_retained",
            endpoint_identities=identities,
            both_facts_retained=True,
            winner_selected=False,
            harmonized=True,
            common_assumption=common_assumption,
            effects_authorized=False,
            nl_incompatibility_proven=False,
            detail=(
                "record/bindings validated only; evaluator does not prove "
                "natural-language incompatibility"
            ),
        ))

    review_selection = require_independent_review()
    if review_selection.refusal is not None:
        return review_selection.refusal
    # Accepted review is used only for binding checks above; never emitted.

    # A9 unresolved members must surface even when A3 lineage would otherwise return.
    mandatory_early = mandatory_closure_result()
    if mandatory_early is not None and mandatory_early.get("unresolved_mandatory") is True:
        return mandatory_early
    if mandatory_early is not None and mandatory_early.get("status") == "refused":
        return mandatory_early
    if mandatory_early is not None and mandatory_early.get("reason_code") == "use_closure_incomplete":
        return mandatory_early

    # A2 / R3: comparison requires affirmative evidence for all PREMISE_OVERLAP_FIELDS.
    # unit_scope_aligned must not stand in for any missing field (same constant as A5).
    if kind == "compares_with":
        missing_comparability = []
        unequal_time_conditions = []
        unequal_unit_scope = []
        for left_key, right_key in PREMISE_OVERLAP_FIELDS:
            left = assertions.get(left_key)
            right = assertions.get(right_key)
            # Missing/empty/non-string on either side never counts as equal.
            if not is_non_empty_string(left) or not is_non_empty_string(right):
                if not is_non_empty_string(right):
                    missing_comparability.append(right_key)
                else:
                    missing_comparability.append(left_key)
                continue
            if left != right:
                if right_key in ("peer_conditions", "peer_valid_time"):
                    unequal_time_conditions.append(right_key)
                else:
                    unequal_unit_scope.append(right_key)
        if unequal_time_conditions:
            return refuse(
                "conditions_incompatible",
                mismatched_fields=unequal_time_conditions,
                detail="comparison refuses incompatible peer valid_time or conditions",
            )
        if (
            missing_comparability
            or unequal_unit_scope
            or unit_scope_aligned is not True
        ):
            return outcome(
                "inspectable_unresolved",
                "unit_scope_unresolved",
                endpoint_identities=identities,
                missing_fields=missing_comparability,
                mismatched_fields=unequal_unit_scope,
                detail=(
                    "comparison unresolved until all PREMISE_OVERLAP_FIELDS pairs are "
                    "present and equal; unit_scope_aligned does not waive missing fields"
                ),
            )

    # A3: copied/translated support collapses to one lineage family.
    derivative_kinds = {"quotes", "rendition_of", "derivative", "quotation"}
    lineage_derivative = any(
        isinstance(item, dict) and item.get("kind") in derivative_kinds for item in lineage
    )
    support_kind = grounding.get("support_kind")
    if support_kind in {"quotation", "derivative"} or lineage_derivative:
        return outcome(
            "inspectable",
            "single_lineage_family",
            endpoint_identities=identities,
            independent_support_count=1,
            lineage_family_count=1,
        )

    # A9 completed closure (after lineage), still never authorizes effects.
    if mandatory_early is not None:
        return mandatory_early

    # A1: same local object id across distinct full pins — preserve both.
    if from_ep.get("object_id") == to_ep.get("object_id") and id_from != id_to:
        return outcome(
            "inspectable",
            "local_id_collision_preserved",
            endpoint_identities=identities,
            same_object_inferred=False,
            self_support_inferred=False,
        )

    # A6a: newer immutable revision published, but R still pins the reviewed pair.
    if published and reviewed_pins and pins_equal(request_pins, reviewed_pins):
        return outcome(
            "inspectable",
            "publication_non_revoking",
            endpoint_identities=identities,
            applicable_pins=dict(request_pins),
            published_releases=list(published),
            review_transferred_to_b2=False,
        )

    # A10 / general positive inspection control — only after every condition above.
    return outcome(
        "inspectable",
        "scoped_inspection_ok",
        endpoint_identities=identities,
        execution_granted=False,
        proof_promoted=False,
        applicable_pins=dict(request_pins),
    )


def evaluate_document(document: dict) -> dict:
    if not isinstance(document, dict):
        return seal_report(refuse("malformed_input", detail="document must be an object"))
    overlay = document.get("overlay")
    context = document.get("context")
    if overlay is None or context is None:
        return seal_report(refuse(
            "malformed_input",
            detail="document requires overlay and context",
        ))
    return seal_report(evaluate(overlay, context))


def load_input(path: Path) -> tuple[dict | None, dict]:
    try:
        with path.open("rb") as handle:
            raw = handle.read(MAX_INPUT_BYTES + 1)
    except OSError as exc:
        return None, refuse("malformed_input", detail=f"cannot read input: {exc}")
    if len(raw) > MAX_INPUT_BYTES:
        return None, refuse(
            "malformed_input",
            detail=f"input exceeds MAX_INPUT_BYTES={MAX_INPUT_BYTES}",
            size=len(raw),
        )
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        return None, refuse("malformed_input", detail=f"utf-8 decode failed: {exc}")
    try:
        document = json.loads(text, object_pairs_hook=reject_duplicate_keys)
    except DuplicateKeyError as exc:
        return None, refuse("malformed_input", detail=str(exc))
    except json.JSONDecodeError as exc:
        return None, refuse("malformed_input", detail=f"json decode failed: {exc}")
    if not isinstance(document, dict):
        return None, refuse("malformed_input", detail="top-level JSON must be an object")
    return document, {}


def report_exit_code(report: dict) -> int:
    if not isinstance(report, dict) or "status" not in report or "reason_code" not in report:
        return 1
    status = report.get("status")
    if status in PASS_STATUSES:
        return 0
    if status in INCOMPLETE_STATUSES:
        return 3
    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cross_package_overlay.py",
        description="Bounded G11 cross-package overlay preparation (draft model, not a released schema).",
    )
    parser.add_argument("--input", "-i", help="Path to JSON document {overlay, context}")
    parser.add_argument("input_positional", nargs="?", help="Path to JSON document")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv[1:] if argv is not None else None)
    path_value = args.input or args.input_positional
    if not path_value:
        parser.print_usage(sys.stderr)
        print("error: --input PATH is required", file=sys.stderr)
        return 2

    try:
        path = Path(path_value)
        document, early = load_input(path)
        if document is None:
            report = seal_report(early)
        else:
            report = evaluate_document(document)
    except Exception as exc:  # noqa: BLE001 — CLI must never crash without a report
        report = seal_report(refuse(
            "malformed_input",
            detail=f"unexpected evaluation error: {type(exc).__name__}: {exc}",
        ))

    # Always emit a JSON report for evaluated inputs; usage errors alone may omit it.
    sys.stdout.write(json.dumps(report, sort_keys=True, ensure_ascii=False) + "\n")
    return report_exit_code(report)

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

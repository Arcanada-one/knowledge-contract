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
from typing import Any

SUPPORTED_PROFILE = "cross-package-relations/0.1"
CANONICAL_LANGUAGE = "en"
MAX_INPUT_BYTES = 256 * 1024
DIGEST_FIELDS = ("algorithm", "value", "byte_domain", "source_revision")
ENDPOINT_REQUIRED_FIELDS = ("package_id", "release_id", "object_id", "source_anchor")
PACKAGE_ID_FIELDS = ("package_id", "release_id")
REQUIRED_PIN_KEYS = frozenset({"A", "B"})
PERMISSION_BOOL_FIELDS = ("permitted", "accessible", "revoked")
SHA256_HEX = re.compile(r"^[0-9a-f]{64}$")
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


class DuplicateKeyError(ValueError):
    """Raised when JSON object_pairs_hook sees a repeated key."""


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
    report = {"status": status, "reason_code": reason_code}
    report.update(fields)
    report.setdefault("bounded_preparation", True)
    report.setdefault("released_schema", False)
    report.setdefault("execution_granted", False)
    report.setdefault("proof_promoted", False)
    return report


def refuse(reason_code: str, **fields: Any) -> dict:
    return outcome("refused", reason_code, **fields)


def digest_complete(digest: Any) -> bool:
    if not isinstance(digest, dict):
        return False
    return all(digest.get(field) not in (None, "") for field in DIGEST_FIELDS)


def digest_malformed(digest: Any) -> str | None:
    """Return a detail string when digest shape/type/format is malformed."""
    if digest is None:
        return None
    if not isinstance(digest, dict):
        return "package_manifest_digest must be an object"
    for field in DIGEST_FIELDS:
        if field not in digest:
            continue
        value = digest.get(field)
        if value in (None, ""):
            continue
        if not isinstance(value, str):
            return f"package_manifest_digest.{field} must be a non-empty string"
        if field == "algorithm" and value != "sha256":
            return "package_manifest_digest.algorithm must be 'sha256'"
        if field == "value" and SHA256_HEX.fullmatch(value) is None:
            return "package_manifest_digest.value must be 64 lowercase hex characters"
    return None


def require_non_empty_string(value: Any, label: str) -> dict | None:
    if value is None or value == "":
        return None
    if not isinstance(value, str):
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


def pins_equal(left: Any, right: Any) -> bool:
    if not pins_complete(left) or not pins_complete(right):
        return False
    for side in ("A", "B"):
        if left.get(side) != right.get(side):
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
        if source not in (None, "")
    ]
    if review_author not in (None, ""):
        if reviewer in (None, ""):
            return True
        if reviewer == review_author:
            return True
    if reviewer not in (None, "") and reviewer in package_authors:
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
        for field in ENDPOINT_REQUIRED_FIELDS:
            value = endpoint.get(field)
            if value is None or value == "":
                missing.append(field)
                continue
            bad = require_non_empty_string(value, f"relation.{label}.{field}")
            if bad is not None:
                return bad
        if missing:
            return refuse(
                "incomplete_release_pin",
                side=label,
                missing_fields=missing,
                detail="endpoint requires package_id, release_id, object_id, source_anchor",
            )
        ep_digest = endpoint.get("package_manifest_digest")
        if "package_manifest_digest" in endpoint:
            digest_bad = digest_malformed(ep_digest)
            if digest_bad is not None:
                return refuse("malformed_input", side=label, detail=digest_bad)

    if path_has_translations_segment(from_ep.get("path")) or path_has_translations_segment(to_ep.get("path")):
        return refuse(
            "rendition_endpoint_refused",
            detail="endpoint path segment 'translations' is out of scope",
        )

    # from must match package A; to must match package B exactly.
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

    def require_independent_review() -> dict | None:
        """A10: independent scoped review whose pins equal the request pins."""
        for review in reviews:
            if not isinstance(review, dict):
                continue
            pins = review.get("pins")
            if pins is None:
                continue
            if not pins_complete(pins):
                return refuse(
                    "request_pin_mismatch",
                    review_pins=pins if isinstance(pins, dict) else None,
                    detail="review pins must contain exactly keys A and B",
                )
        matching = [
            review for review in reviews
            if isinstance(review, dict) and pins_equal(review.get("pins"), request_pins)
        ]
        if not matching:
            if reviewed_pins and not pins_equal(reviewed_pins, request_pins):
                return refuse(
                    "review_pin_mismatch",
                    reviewed_pins=reviewed_pins,
                    request_pins=request_pins,
                    detail="reviewed A1/B1 pair cannot discharge a request that selects a different pin",
                )
            return refuse(
                "review_missing",
                detail="independent scoped review whose pins equal the request pins is required",
            )
        matched = matching[0]
        if matched.get("independent") is not True:
            return refuse(
                "review_not_independent",
                detail="matching review must affirmatively set independent=true",
            )
        if review_is_self_authored(matched, overlay, pkg_a, pkg_b):
            return refuse(
                "review_not_independent",
                detail="reviewer identity must be present and distinct from author / package author",
            )
        return None

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

    review_refusal = require_independent_review()
    if review_refusal is not None:
        return review_refusal

    # A4: one-sided contradiction.
    if kind == "contradicts_under":
        if not from_anchor or not to_anchor:
            missing = "from" if not from_anchor else "to"
            return refuse(
                "one_sided_contradiction",
                missing_side=missing,
                candidate_preserved=True,
            )
        common_assumption = (
            assertions.get("conditions")
            or assertions.get("common_assumption")
            or grounding.get("common_assumption")
            or grounding.get("conditions")
        )
        # Default False: harmonized must be affirmatively true with a stated assumption.
        harmonized = assertions.get("harmonized") is True
        if not common_assumption or not harmonized:
            return refuse(
                "common_assumption_required",
                detail="contradicts_under requires an explicit common assumption and harmonized=true",
            )
        return outcome(
            "inspectable",
            "contradicts_under_retained",
            endpoint_identities=identities,
            both_facts_retained=True,
            winner_selected=False,
            harmonized=True,
            common_assumption=common_assumption,
        )

    # A2: unit/scope mismatch left unresolved.
    peer_units = assertions.get("peer_units")
    peer_scope = assertions.get("peer_quantifier_scope")
    units = assertions.get("units")
    scope = assertions.get("quantifier_scope")
    mismatched = False
    if peer_units is not None and units is not None and peer_units != units:
        mismatched = True
    if peer_scope is not None and scope is not None and peer_scope != scope:
        mismatched = True
    if unit_scope_aligned is False:
        mismatched = True
    if kind == "compares_with" and mismatched:
        return outcome(
            "inspectable_unresolved",
            "unit_scope_unresolved",
            endpoint_identities=identities,
            detail="comparison unresolved until a reviewed conversion/scope rule is supplied",
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

    # A9: mandatory dependency closure under shared R/context.
    if mandatory is not None:
        if not isinstance(mandatory, list):
            return refuse(
                "malformed_input",
                detail="mandatory_dependencies must be a list of objects with id and boolean discharged",
            )
        for item in mandatory:
            if not isinstance(item, dict):
                return refuse(
                    "malformed_input",
                    detail="each mandatory_dependencies member must be an object with id and boolean discharged",
                )
            if item.get("id") in (None, ""):
                return refuse(
                    "malformed_input",
                    detail="each mandatory_dependencies member requires a non-empty id",
                )
            if not isinstance(item.get("discharged"), bool):
                return refuse(
                    "malformed_input",
                    detail="mandatory_dependencies.discharged must be a real boolean",
                )
        unresolved = [item for item in mandatory if item.get("discharged") is not True]
        if unresolved:
            return outcome(
                "inspectable_unresolved",
                "use_closure_incomplete",
                endpoint_identities=identities,
                use_closure_complete=False,
                external_effects=0,
                unresolved_members=unresolved,
                effects_authorized=False,
            )
        if mandatory:
            return outcome(
                "prerequisite_closure_complete",
                "prerequisite_closure_complete",
                endpoint_identities=identities,
                use_closure_complete=True,
                # Preparation never authorizes effects (overlay §6 A9b).
                effects_authorized=False,
                detail="consequential effects still require current authority, delivery and durable effect identity",
            )

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
        return refuse("malformed_input", detail="document must be an object")
    overlay = document.get("overlay")
    context = document.get("context")
    if overlay is None or context is None:
        return refuse("malformed_input", detail="document requires overlay and context")
    return evaluate(overlay, context)


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
            report = early
        else:
            report = evaluate_document(document)
    except Exception as exc:  # noqa: BLE001 — CLI must never crash without a report
        report = refuse(
            "malformed_input",
            detail=f"unexpected evaluation error: {type(exc).__name__}: {exc}",
        )

    # Always emit a JSON report for evaluated inputs; usage errors alone may omit it.
    sys.stdout.write(json.dumps(report, sort_keys=True, ensure_ascii=False) + "\n")
    return report_exit_code(report)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

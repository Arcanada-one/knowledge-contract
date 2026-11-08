#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Bounded producer-side preparation for a two-package cross-package relation overlay.

Draft model of reference/relations/CROSS-PACKAGE-OVERLAY.md section 3. This is
not a released wire schema, not independent scientific review, not production
validation, and not authorization or an execution grant. book-package/2 is
unchanged. Python standard library only.

NOT_MEASURED:
- live Muneral producer package admission or KCLIVE-08 task closure
- independent scientific peer review of candidate relations
- production authorization, delivery or durable effect identity
- rendition/K8 sidecar endpoint verification
- multi-package overlays beyond exactly two canonical English packages
- released cross-package-relations wire schema registration

CLI exit codes: 0 accepted/inspectable report, 1 typed refusal (always with a
JSON report), 2 usage. A missing report must never be read as pass.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

SUPPORTED_PROFILE = "cross-package-relations/0.1"
CANONICAL_LANGUAGE = "en"
MAX_INPUT_BYTES = 256 * 1024
PASS_STATUSES = frozenset({
    "inspectable",
    "inspectable_unresolved",
    "prerequisite_closure_complete",
    "accepted",
})
RELATION_KINDS = frozenset({
    "quotes",
    "rendition_of",
    "compares_with",
    "supports_under",
    "contradicts_under",
    "requires_for_use",
    "related_to",
})


def permission_key(package_id: str, release_id: str) -> str:
    return f"{package_id}@{release_id}"


def endpoint_identity(endpoint: dict) -> tuple:
    digest = endpoint.get("package_manifest_digest") or {}
    rep = endpoint.get("representation_digest") or {}
    return (
        endpoint.get("package_id"),
        (digest.get("algorithm"), digest.get("value"), digest.get("byte_domain"), digest.get("source_revision")),
        endpoint.get("release_id"),
        endpoint.get("component_id"),
        endpoint.get("object_id"),
        endpoint.get("representation_id"),
        (rep.get("algorithm"), rep.get("value"), rep.get("byte_domain"), rep.get("source_revision")),
        endpoint.get("source_anchor"),
    )


def package_identity(package: dict) -> tuple:
    digest = package.get("package_manifest_digest") or {}
    return (
        package.get("package_id"),
        package.get("release_id"),
        (digest.get("algorithm"), digest.get("value"), digest.get("byte_domain"), digest.get("source_revision")),
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


def is_rendition_endpoint(endpoint: dict, package: dict | None = None) -> bool:
    language = endpoint.get("language")
    if language is None and package is not None:
        language = package.get("language")
    path = str(endpoint.get("path") or (package or {}).get("path") or "")
    canonical_flag = endpoint.get("canonical")
    if canonical_flag is None and package is not None:
        canonical_flag = package.get("canonical")
    if language is not None and language != CANONICAL_LANGUAGE:
        return True
    if canonical_flag is False:
        return True
    if "translations/" in path.replace("\\", "/"):
        return True
    return False


def evaluate(overlay: dict, context: dict) -> dict:
    """Evaluate one candidate overlay record plus explicit consumer context."""
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

    if package_identity(pkg_a) == package_identity(pkg_b):
        return refuse("same_package_both_sides", package_identity=list(package_identity(pkg_a)))
    if pkg_a.get("package_id") == pkg_b.get("package_id") and pkg_a.get("release_id") == pkg_b.get("release_id"):
        return refuse("same_package_both_sides", package_id=pkg_a.get("package_id"))

    relation = overlay.get("relation")
    if not isinstance(relation, dict):
        return refuse("malformed_input", detail="relation must be an object")
    kind = relation.get("kind")
    if kind not in RELATION_KINDS:
        return refuse("malformed_input", detail=f"unsupported relation kind: {kind!r}")

    from_ep = relation.get("from")
    to_ep = relation.get("to")
    if not isinstance(from_ep, dict) or not isinstance(to_ep, dict):
        return refuse("malformed_input", detail="from and to endpoints required")

    if is_rendition_endpoint(from_ep, pkg_a) or is_rendition_endpoint(to_ep, pkg_b):
        return refuse(
            "rendition_endpoint_refused",
            detail="only canonical English package endpoints are accepted in this preparation",
        )
    # Also refuse if package records themselves are rendition-qualified even when
    # endpoints omit language/path (caller may pin the package side only).
    if is_rendition_endpoint({"language": pkg_a.get("language"), "path": pkg_a.get("path"), "canonical": pkg_a.get("canonical")}) or \
       is_rendition_endpoint({"language": pkg_b.get("language"), "path": pkg_b.get("path"), "canonical": pkg_b.get("canonical")}):
        return refuse(
            "rendition_endpoint_refused",
            detail="package side is rendition-qualified",
        )

    id_from = endpoint_identity(from_ep)
    id_to = endpoint_identity(to_ep)
    identities = [list(id_from), list(id_to)]

    grounding = relation.get("grounding") if isinstance(relation.get("grounding"), dict) else {}
    assertions = relation.get("assertions") if isinstance(relation.get("assertions"), dict) else {}
    lineage = relation.get("lineage") if isinstance(relation.get("lineage"), list) else []
    assessment = overlay.get("assessment") if isinstance(overlay.get("assessment"), dict) else {}

    request_pins = context.get("request_pins") if isinstance(context.get("request_pins"), dict) else {}
    permissions = context.get("permissions") if isinstance(context.get("permissions"), dict) else {}
    reviews = context.get("reviews") if isinstance(context.get("reviews"), list) else []
    published = context.get("published_releases") if isinstance(context.get("published_releases"), list) else []
    mandatory = context.get("mandatory_dependencies")
    unit_scope_aligned = context.get("unit_scope_aligned")

    # Permission / revocation / accessibility for the request pins.
    def pin_state(side: str, package: dict) -> dict:
        release = request_pins.get(side) or package.get("release_id")
        key = permission_key(package["package_id"], release)
        state = permissions.get(key)
        if not isinstance(state, dict):
            return {"permitted": False, "revoked": False, "accessible": False, "missing": True}
        return state

    state_a = pin_state("A", pkg_a)
    state_b = pin_state("B", pkg_b)

    reviewed_pins = assessment.get("reviewed_pins") if isinstance(assessment.get("reviewed_pins"), dict) else {}
    if not reviewed_pins and reviews:
        first = reviews[0]
        if isinstance(first, dict) and isinstance(first.get("pins"), dict):
            reviewed_pins = first["pins"]

    # A6c: revoked current use (bytes may remain historically inspectable).
    for side, state in (("A", state_a), ("B", state_b)):
        if state.get("revoked") is True or state.get("permitted") is False and state.get("historically_inspectable"):
            if state.get("revoked") is True:
                return refuse(
                    "current_use_revoked",
                    side=side,
                    historical_record_retained=bool(state.get("historically_inspectable", True)),
                )

    # A7: digest may resolve but current authorization denies read.
    for side, state in (("A", state_a), ("B", state_b)):
        if state.get("accessible") is False and state.get("revoked") is not True:
            return refuse("endpoint_inaccessible", side=side)

    # A6b: request pins select a release the scoped review did not cover.
    if reviewed_pins and request_pins:
        for side in ("A", "B"):
            if side in reviewed_pins and side in request_pins and reviewed_pins[side] != request_pins[side]:
                return refuse(
                    "review_pin_mismatch",
                    reviewed_pins=reviewed_pins,
                    request_pins=request_pins,
                    detail="reviewed A1/B1 pair cannot discharge a request that selects a different pin",
                )

    # A4: one-sided contradiction.
    if kind == "contradicts_under":
        from_anchor = grounding.get("from_anchor")
        to_anchor = grounding.get("to_anchor")
        if not from_anchor or not to_anchor:
            missing = "from" if not from_anchor else "to"
            return refuse(
                "one_sided_contradiction",
                missing_side=missing,
                candidate_preserved=True,
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

    # A5: true two-sided conditioned contradiction retains both facts.
    if kind == "contradicts_under":
        return outcome(
            "inspectable",
            "contradicts_under_retained",
            endpoint_identities=identities,
            both_facts_retained=True,
            winner_selected=False,
            harmonized=bool(assertions.get("harmonized", True)),
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
    if isinstance(mandatory, list):
        unresolved = [
            item for item in mandatory
            if isinstance(item, dict) and not item.get("discharged")
        ]
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
                effects_authorized=bool(context.get("current_authority_for_effects")),
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
    if published and reviewed_pins and request_pins == reviewed_pins:
        if state_a.get("permitted") and state_b.get("permitted") and state_a.get("accessible") and state_b.get("accessible"):
            return outcome(
                "inspectable",
                "publication_non_revoking",
                endpoint_identities=identities,
                applicable_pins=dict(request_pins),
                published_releases=list(published),
                review_transferred_to_b2=False,
            )

    # A10 / general positive inspection control.
    return outcome(
        "inspectable",
        "scoped_inspection_ok",
        endpoint_identities=identities,
        execution_granted=False,
        proof_promoted=False,
        applicable_pins=dict(request_pins) if request_pins else {
            "A": pkg_a.get("release_id"),
            "B": pkg_b.get("release_id"),
        },
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
        raw = path.read_bytes()
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
        document = json.loads(text)
    except json.JSONDecodeError as exc:
        return None, refuse("malformed_input", detail=f"json decode failed: {exc}")
    if not isinstance(document, dict):
        return None, refuse("malformed_input", detail="top-level JSON must be an object")
    return document, {}


def report_exit_code(report: dict) -> int:
    if not isinstance(report, dict) or "status" not in report or "reason_code" not in report:
        return 1
    if report.get("status") in PASS_STATUSES:
        return 0
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

    path = Path(path_value)
    document, early = load_input(path)
    if document is None:
        report = early
    else:
        report = evaluate_document(document)

    # Always emit a JSON report for evaluated inputs; usage errors alone may omit it.
    sys.stdout.write(json.dumps(report, sort_keys=True, ensure_ascii=False) + "\n")
    return report_exit_code(report)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

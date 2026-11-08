#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Corpus controls for tools/cross_package_overlay.py (G11-A1..A10 + negatives).

Fixtures are built in temporary directories at test time. Asserts typed reason
codes and CLI exit codes from CROSS-PACKAGE-OVERLAY.md section 6. A missing
JSON report must never be treated as a pass.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

try:
    from tools import cross_package_overlay as cpo
except ImportError:  # `cd tools && python3 -B -m unittest test_cross_package_overlay`
    import cross_package_overlay as cpo

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "tools" / "cross_package_overlay.py"
MAX_BYTES = cpo.MAX_INPUT_BYTES

DIGEST_A1 = {
    "algorithm": "sha256",
    "value": "a" * 64,
    "byte_domain": "package-manifest",
    "source_revision": "A1",
}
DIGEST_B1 = {
    "algorithm": "sha256",
    "value": "b" * 64,
    "byte_domain": "package-manifest",
    "source_revision": "B1",
}
DIGEST_B2 = {
    "algorithm": "sha256",
    "value": "c" * 64,
    "byte_domain": "package-manifest",
    "source_revision": "B2",
}


def representation_digest_obj(release_id: str, *, value: str | None = None) -> dict:
    return {
        "algorithm": "sha256",
        "value": value or ("d" * 64),
        "byte_domain": "object-bytes",
        "source_revision": release_id,
    }


def pkg(package_id: str, release_id: str, digest: dict, *, language: str = "en",
        path: str = "objects/o.json",
        representation_id: str = "canonical-en",
        representation_digest_value: str | None = None,
        representation_language: str | None = None) -> dict:
    """Package fixture with required representations map (KC-SWE §2 interpretation)."""
    rep_language = language if representation_language is None else representation_language
    return {
        "package_id": package_id,
        "package_manifest_digest": dict(digest),
        "release_id": release_id,
        "language": language,
        "canonical": language == "en",
        "path": path,
        "representations": {
            representation_id: {
                "representation_digest": representation_digest_obj(
                    release_id, value=representation_digest_value,
                ),
                "language": rep_language,
            },
        },
    }


def endpoint(package: dict, object_id: str, *, component_id: str = "main",
             representation_id: str = "canonical-en", source_anchor: str = "s1",
             representation_digest: str | None = None, path: str | None = None) -> dict:
    package_digest = package.get("package_manifest_digest")
    reps = package.get("representations") if isinstance(package.get("representations"), dict) else {}
    declared = reps.get(representation_id) if isinstance(reps.get(representation_id), dict) else None
    if declared and isinstance(declared.get("representation_digest"), dict) and representation_digest is None:
        rep_digest = dict(declared["representation_digest"])
    else:
        rep_digest = representation_digest_obj(
            package["release_id"], value=representation_digest,
        )
    return {
        "package_id": package["package_id"],
        "package_manifest_digest": dict(package_digest) if isinstance(package_digest, dict) else package_digest,
        "release_id": package["release_id"],
        "component_id": component_id,
        "object_id": object_id,
        "representation_id": representation_id,
        "representation_digest": rep_digest,
        "source_anchor": source_anchor,
        "language": package["language"],
        "path": path if path is not None else package.get("path", "objects/o.json"),
    }


def base_packages():
    a = pkg("pkg-alpha", "A1", DIGEST_A1)
    b = pkg("pkg-beta", "B1", DIGEST_B1)
    return a, b


def overlay_record(*, kind: str, from_ep: dict, to_ep: dict, packages: tuple[dict, dict],
                   grounding: dict | None = None, lineage: list | None = None,
                   assertions: dict | None = None, profile: str = cpo.SUPPORTED_PROFILE,
                   assessment: dict | None = None, relation_id: str = "rel-1") -> dict:
    a, b = packages
    return {
        "overlay_profile": profile,
        "overlay_revision": "ov-1",
        "purpose": "bounded-inspection",
        "intended_consumer": "kclive-preparation",
        "author": "kc-swe-fixture",
        "packages": {"A": a, "B": b},
        "relation": {
            "relation_id": relation_id,
            "kind": kind,
            "from": from_ep,
            "to": to_ep,
            "assertions": assertions or {
                "polarity": "affirmative",
                "modality": "claim",
                "attribution": "author",
                "quantifier_scope": "all-applicable",
                "conditions": "shared-load-limit",
                "units": "kg",
                "valid_time": "2026",
            },
            "grounding": grounding if grounding is not None else {
                "from_anchor": from_ep["source_anchor"],
                "to_anchor": to_ep["source_anchor"],
                "support_kind": "independent_review",
            },
            "lineage": lineage if lineage is not None else [],
        },
        "assessment": assessment or {
            "reviewer": "fixture-reviewer",
            "role": "scoped-reviewer",
            "verdict": "accepted",
            "scope": "inspection-only",
            "reviewed_edge_revision": "ov-1",
            "reviewed_pins": {
                "A": a["release_id"],
                "B": b["release_id"],
            },
            "time": "2026-11-08T00:00:00Z",
            "uncertainty": "none-recorded",
        },
    }


def bound_review(*, pins: dict | None = None, digests: tuple[dict, dict] | None = None,
                 relation_id: str = "rel-1", reviewed_edge_revision: str = "ov-1",
                 reviewer: str = "fixture-reviewer", author: str = "fixture-author",
                 verdict: str = "accepted", scope: str = "inspection-only",
                 independent: bool = True, evidence: str | None = None,
                 **extra: object) -> dict:
    """Independent scoped review with complete release + manifest-byte pins."""
    a_digest, b_digest = digests or (DIGEST_A1, DIGEST_B1)
    review = {
        "pins": pins or {"A": "A1", "B": "B1"},
        "pin_manifest_digests": {
            "A": dict(a_digest),
            "B": dict(b_digest),
        },
        "independent": independent,
        "author": author,
        "reviewer": reviewer,
        "verdict": verdict,
        "scope": scope,
        "relation_id": relation_id,
        "reviewed_edge_revision": reviewed_edge_revision,
    }
    if evidence is not None:
        review["evidence"] = evidence
    review.update(extra)
    return review


INCOMPATIBILITY_EVIDENCE = (
    "On the shared applicability domain, x <= 10 and x > 10 cannot both hold."
)


def comparable_assertions(**overrides: object) -> dict:
    """Affirmative comparability evidence for compares_with / contradicts_under."""
    assertions = {
        "polarity": "affirmative",
        "modality": "claim",
        "attribution": "author",
        "quantifier_scope": "all-applicable",
        "peer_quantifier_scope": "all-applicable",
        "conditions": "shared-load-limit",
        "peer_conditions": "shared-load-limit",
        "units": "kg",
        "peer_units": "kg",
        "valid_time": "2026",
        "peer_valid_time": "2026",
    }
    assertions.update(overrides)
    return assertions


def a5_conflict_assertions(**overrides: object) -> dict:
    """Equal-overlap contradicts_under assertions with an explicit common_assumption."""
    assertions = comparable_assertions(
        polarity="conflict",
        attribution="both-sides",
        quantifier_scope="same-subject",
        peer_quantifier_scope="same-subject",
        conditions="shared-assumption-load",
        peer_conditions="shared-assumption-load",
        common_assumption="shared-domain-x-on-same-referent",
        harmonized=True,
        from_proposition="x <= 10",
        to_proposition="x > 10",
    )
    assertions.update(overrides)
    return assertions


def task_requirements_record(
    *,
    revision: str = "R1",
    members: list | None = None,
    empty_set_justification: str | None = None,
) -> dict:
    """Trusted requirements set (context.task_requirements); absent key ≠ empty set."""
    record: dict = {
        "revision": revision,
        "members": ["A", "B"] if members is None else list(members),
    }
    if empty_set_justification is not None:
        record["empty_set_justification"] = empty_set_justification
    return record


def discharge(member_id: str, *, discharged: bool = True, witness_ref: str | None = "wit-1",
              **extra: object) -> dict:
    item: dict = {"id": member_id, "discharged": discharged}
    if witness_ref is not None:
        item["witness_ref"] = witness_ref
    item.update(extra)
    return item


def context_record(*, request_pins: dict | None = None, permissions: dict | None = None,
                   reviews: list | None = None, published_releases: list | None = None,
                   mandatory_dependencies: list | None = None,
                   task_requirements: dict | None = None,
                   current_authority_for_effects: bool = False,
                   unit_scope_aligned: bool | None = None) -> dict:
    a, b = base_packages()
    pins = request_pins or {"A": "A1", "B": "B1"}
    default_perms = {
        cpo.permission_key(a["package_id"], "A1"): {
            "permitted": True, "revoked": False, "accessible": True,
        },
        cpo.permission_key(b["package_id"], "B1"): {
            "permitted": True, "revoked": False, "accessible": True,
        },
    }
    ctx = {
        "request_pins": pins,
        "permissions": permissions if permissions is not None else default_perms,
        "reviews": reviews if reviews is not None else [bound_review()],
        "published_releases": published_releases or [],
        "mandatory_dependencies": mandatory_dependencies,
        "current_authority_for_effects": current_authority_for_effects,
    }
    if task_requirements is not None:
        ctx["task_requirements"] = task_requirements
    if unit_scope_aligned is not None:
        ctx["unit_scope_aligned"] = unit_scope_aligned
    return ctx


def payload(overlay: dict, context: dict) -> dict:
    return {"overlay": overlay, "context": context}


def run_cli(data: dict | bytes, *, as_bytes: bool = False) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "input.json"
        if as_bytes:
            path.write_bytes(data)  # type: ignore[arg-type]
        else:
            path.write_text(json.dumps(data), encoding="utf-8")
        return subprocess.run(
            [sys.executable, "-B", str(CLI), "--input", str(path)],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
        )


def require_report(test: unittest.TestCase, result: subprocess.CompletedProcess[str]) -> dict:
    test.assertTrue(result.stdout.strip(), f"missing report stdout; stderr={result.stderr!r}")
    report = json.loads(result.stdout)
    test.assertIn("status", report)
    test.assertIn("reason_code", report)
    return report


class CorpusG11Tests(unittest.TestCase):
    def test_g11_a1_local_id_collision_preserves_two_endpoints(self):
        a, b = base_packages()
        from_ep = endpoint(a, "o-17", source_anchor="a-o17")
        to_ep = endpoint(b, "o-17", source_anchor="b-o17")
        ov = overlay_record(
            kind="compares_with", from_ep=from_ep, to_ep=to_ep, packages=(a, b),
            assertions=comparable_assertions(),
        )
        result = run_cli(payload(ov, context_record(unit_scope_aligned=True)))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(report["reason_code"], "local_id_collision_preserved")
        self.assertEqual(report["status"], "inspectable")
        self.assertFalse(report["same_object_inferred"])
        self.assertEqual(len(report["endpoint_identities"]), 2)
        self.assertNotEqual(report["endpoint_identities"][0], report["endpoint_identities"][1])

    def test_g11_a2_unit_scope_mismatch_unresolved(self):
        a, b = base_packages()
        from_ep = endpoint(a, "claim-1")
        to_ep = endpoint(b, "claim-1")
        assertions = {
            "polarity": "affirmative",
            "modality": "claim",
            "attribution": "author",
            "quantifier_scope": "present-population",
            "conditions": "load-limit",
            "units": "kg",
            "valid_time": "2026",
            "peer_units": "lb",
            "peer_quantifier_scope": "historical-population",
        }
        ov = overlay_record(
            kind="compares_with", from_ep=from_ep, to_ep=to_ep, packages=(a, b), assertions=assertions,
        )
        result = run_cli(payload(ov, context_record(unit_scope_aligned=False)))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 3, result.stderr + result.stdout)
        self.assertEqual(report["reason_code"], "unit_scope_unresolved")
        self.assertEqual(report["status"], "inspectable_unresolved")

    def test_g11_a3_copied_support_one_lineage_family(self):
        a, b = base_packages()
        from_ep = endpoint(a, "stmt-1", source_anchor="a1")
        to_ep = endpoint(b, "stmt-copy", source_anchor="b1")
        lineage = [
            {"kind": "quotes", "origin": "pkg-alpha@A1:stmt-1", "revision": "A1"},
            {"kind": "rendition_of", "origin": "pkg-beta@B1:stmt-copy", "revision": "B1-tr"},
        ]
        grounding = {
            "from_anchor": "a1",
            "to_anchor": "b1",
            "support_kind": "quotation",
        }
        ov = overlay_record(
            kind="supports_under", from_ep=from_ep, to_ep=to_ep, packages=(a, b),
            lineage=lineage, grounding=grounding,
        )
        result = run_cli(payload(ov, context_record()))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(report["reason_code"], "single_lineage_family")
        self.assertEqual(report["independent_support_count"], 1)

    def test_g11_a4_one_sided_contradiction_refused(self):
        a, b = base_packages()
        from_ep = endpoint(a, "p1")
        to_ep = endpoint(b, "p2")
        grounding = {"from_anchor": "a1", "to_anchor": None, "support_kind": "observation"}
        ov = overlay_record(
            kind="contradicts_under", from_ep=from_ep, to_ep=to_ep, packages=(a, b), grounding=grounding,
        )
        result = run_cli(payload(ov, context_record()))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["reason_code"], "one_sided_contradiction")
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["missing_side"], "to")

    def test_g11_a5_two_sided_contradiction_retains_both(self):
        a, b = base_packages()
        from_ep = endpoint(a, "p1")
        to_ep = endpoint(b, "p2")
        ov = overlay_record(
            kind="contradicts_under", from_ep=from_ep, to_ep=to_ep, packages=(a, b),
            assertions=a5_conflict_assertions(),
        )
        ctx = context_record(reviews=[bound_review(evidence=INCOMPATIBILITY_EVIDENCE)])
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(report["reason_code"], "contradicts_under_retained")
        self.assertTrue(report["both_facts_retained"])
        self.assertFalse(report.get("winner_selected", False))
        self.assertFalse(report.get("effects_authorized", False))

    def test_g11_a6a_b2_publication_does_not_revoke_b1(self):
        a, b = base_packages()
        from_ep = endpoint(a, "x")
        to_ep = endpoint(b, "y")
        ov = overlay_record(kind="supports_under", from_ep=from_ep, to_ep=to_ep, packages=(a, b))
        ctx = context_record(
            request_pins={"A": "A1", "B": "B1"},
            published_releases=["B2"],
        )
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(report["reason_code"], "publication_non_revoking")
        self.assertEqual(report["applicable_pins"], {"A": "A1", "B": "B1"})
        self.assertFalse(report["review_transferred_to_b2"])

    def test_g11_a6b_request_pins_b2_review_stays_on_b1(self):
        a = pkg("pkg-alpha", "A1", DIGEST_A1)
        b2 = pkg("pkg-beta", "B2", DIGEST_B2)
        from_ep = endpoint(a, "x")
        to_ep = endpoint(b2, "y")
        ov = overlay_record(
            kind="supports_under", from_ep=from_ep, to_ep=to_ep, packages=(a, b2),
            assessment={
                "reviewer": "fixture-reviewer",
                "role": "scoped-reviewer",
                "verdict": "accepted",
                "scope": "inspection-only",
                "reviewed_edge_revision": "ov-1",
                "reviewed_pins": {"A": "A1", "B": "B1"},
                "time": "2026-11-08T00:00:00Z",
                "uncertainty": "none-recorded",
            },
        )
        perms = {
            cpo.permission_key("pkg-alpha", "A1"): {
                "permitted": True, "revoked": False, "accessible": True,
            },
            cpo.permission_key("pkg-beta", "B2"): {
                "permitted": True, "revoked": False, "accessible": True,
            },
        }
        ctx = context_record(
            request_pins={"A": "A1", "B": "B2"},
            permissions=perms,
            reviews=[{
                "pins": {"A": "A1", "B": "B1"},
                "verdict": "accepted",
                "scope": "inspection-only",
                "reviewed_edge_revision": "ov-1",
            }],
        )
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["reason_code"], "review_pin_mismatch")
        self.assertEqual(report["status"], "refused")

    def test_g11_a6c_revoked_b1_refuses_current_use(self):
        a, b = base_packages()
        from_ep = endpoint(a, "x")
        to_ep = endpoint(b, "y")
        ov = overlay_record(kind="supports_under", from_ep=from_ep, to_ep=to_ep, packages=(a, b))
        perms = {
            cpo.permission_key("pkg-alpha", "A1"): {
                "permitted": True, "revoked": False, "accessible": True,
            },
            cpo.permission_key("pkg-beta", "B1"): {
                "permitted": False, "revoked": True, "accessible": False,
                "historically_inspectable": True,
            },
        }
        result = run_cli(payload(ov, context_record(permissions=perms)))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["reason_code"], "current_use_revoked")
        self.assertTrue(report.get("historical_record_retained", False))

    def test_g11_a7_inaccessible_endpoint_refuses_closure(self):
        a, b = base_packages()
        from_ep = endpoint(a, "x")
        to_ep = endpoint(b, "y")
        ov = overlay_record(kind="supports_under", from_ep=from_ep, to_ep=to_ep, packages=(a, b))
        perms = {
            cpo.permission_key("pkg-alpha", "A1"): {
                "permitted": True, "revoked": False, "accessible": True,
            },
            cpo.permission_key("pkg-beta", "B1"): {
                "permitted": True, "revoked": False, "accessible": False,
            },
        }
        result = run_cli(payload(ov, context_record(permissions=perms)))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["reason_code"], "endpoint_inaccessible")

    def test_g11_a8_unknown_profile_refused(self):
        a, b = base_packages()
        from_ep = endpoint(a, "x")
        to_ep = endpoint(b, "y")
        ov = overlay_record(
            kind="supports_under", from_ep=from_ep, to_ep=to_ep, packages=(a, b),
            profile="cross-package-relations/9",
        )
        result = run_cli(payload(ov, context_record()))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["reason_code"], "unsupported_profile")
        self.assertFalse(report.get("permissive_fallback", True))

    def test_g11_a9a_unresolved_mandatory_dependency(self):
        a, b = base_packages()
        from_ep = endpoint(a, "x")
        to_ep = endpoint(b, "y")
        ov = overlay_record(kind="requires_for_use", from_ep=from_ep, to_ep=to_ep, packages=(a, b))
        ctx = context_record(
            task_requirements=task_requirements_record(),
            mandatory_dependencies=[
                discharge("A"),
                discharge("B", discharged=False, witness_ref=None, state="unknown"),
            ],
            current_authority_for_effects=False,
        )
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 3, result.stderr + result.stdout)
        self.assertEqual(report["reason_code"], "use_closure_incomplete")
        self.assertEqual(report["status"], "inspectable_unresolved")
        self.assertFalse(report["use_closure_complete"])
        self.assertEqual(report["external_effects"], 0)
        self.assertTrue(report.get("unresolved_mandatory"))

    def test_g11_a9b_completed_dependency_still_needs_authority(self):
        a, b = base_packages()
        from_ep = endpoint(a, "x")
        to_ep = endpoint(b, "y")
        ov = overlay_record(kind="requires_for_use", from_ep=from_ep, to_ep=to_ep, packages=(a, b))
        ctx = context_record(
            task_requirements=task_requirements_record(),
            mandatory_dependencies=[discharge("A"), discharge("B")],
            current_authority_for_effects=False,
        )
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(report["reason_code"], "prerequisite_closure_complete")
        self.assertTrue(report["use_closure_complete"])
        self.assertFalse(report["effects_authorized"])

    def test_g11_a10_positive_supported_pair(self):
        a, b = base_packages()
        from_ep = endpoint(a, "x")
        to_ep = endpoint(b, "y")
        # Genuine positive: complete eight-part endpoint identity, bound review,
        # and (for comparison vocabulary) affirmative comparability evidence.
        ov = overlay_record(
            kind="compares_with", from_ep=from_ep, to_ep=to_ep, packages=(a, b),
            assertions=comparable_assertions(),
        )
        result = run_cli(payload(ov, context_record(unit_scope_aligned=True)))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(report["reason_code"], "scoped_inspection_ok")
        self.assertEqual(report["status"], "inspectable")
        self.assertFalse(report.get("execution_granted", False))
        self.assertFalse(report.get("proof_promoted", False))
        for side in (from_ep, to_ep):
            for field in (
                "package_id", "package_manifest_digest", "release_id", "component_id",
                "object_id", "representation_id", "representation_digest", "source_anchor",
            ):
                self.assertIn(field, side)
        self.assertFalse(report.get("effects_authorized", False))


class NegativeControls(unittest.TestCase):
    def test_rendition_endpoint_refused(self):
        a = pkg("pkg-alpha", "A1", DIGEST_A1, language="en")
        b = pkg("pkg-beta", "B1", DIGEST_B1, language="ru", path="translations/ru/objects/o.json")
        from_ep = endpoint(a, "x")
        to_ep = endpoint(b, "y", path="translations/ru/objects/o.json")
        ov = overlay_record(kind="supports_under", from_ep=from_ep, to_ep=to_ep, packages=(a, b))
        result = run_cli(payload(ov, context_record()))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["reason_code"], "rendition_endpoint_refused")

    def test_same_package_both_sides_refused(self):
        a = pkg("pkg-alpha", "A1", DIGEST_A1)
        from_ep = endpoint(a, "x", source_anchor="s-a")
        to_ep = endpoint(a, "y", source_anchor="s-b")
        ov = overlay_record(kind="supports_under", from_ep=from_ep, to_ep=to_ep, packages=(a, a))
        result = run_cli(payload(ov, context_record()))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["reason_code"], "same_package_both_sides")

    def test_malformed_json_refused_with_report(self):
        result = run_cli(b"{not-json", as_bytes=True)
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["reason_code"], "malformed_input")
        self.assertEqual(report["status"], "refused")

    def test_usage_exit_code_without_input(self):
        result = subprocess.run(
            [sys.executable, "-B", str(CLI)],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
        )
        self.assertEqual(result.returncode, 2)

    def test_oversized_input_refused_with_report(self):
        huge = b'{"overlay":{"x":"' + (b"y" * (MAX_BYTES + 10)) + b'"}}'
        result = run_cli(huge, as_bytes=True)
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["reason_code"], "malformed_input")


class FailClosedRound2Tests(unittest.TestCase):
    """KC-SWE round-2 fail-closed probes (cases 1-13). Red on 06d02dfd."""

    def _supported_pair(self):
        a, b = base_packages()
        from_ep = endpoint(a, "x")
        to_ep = endpoint(b, "y")
        ov = overlay_record(kind="supports_under", from_ep=from_ep, to_ep=to_ep, packages=(a, b))
        return a, b, ov

    def test_r2_01_b_not_permitted_refused(self):
        a, b, ov = self._supported_pair()
        perms = {
            cpo.permission_key(a["package_id"], "A1"): {
                "permitted": True, "revoked": False, "accessible": True,
            },
            cpo.permission_key(b["package_id"], "B1"): {
                "permitted": False, "revoked": False, "accessible": True,
            },
        }
        result = run_cli(payload(ov, context_record(permissions=perms)))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["reason_code"], "endpoint_not_permitted")

    def test_r2_02_missing_review_refused(self):
        _, _, ov = self._supported_pair()
        result = run_cli(payload(ov, context_record(reviews=[])))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["reason_code"], "review_missing")

    def test_r2_03_non_independent_matching_review_refused(self):
        _, _, ov = self._supported_pair()
        reviews = [
            bound_review(pins={"A": "A0", "B": "B0"}, independent=True),
            bound_review(independent=False),
        ]
        result = run_cli(payload(ov, context_record(reviews=reviews)))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["reason_code"], "review_not_independent")

    def test_r2_04_rendition_of_relation_refused(self):
        a, b = base_packages()
        from_ep = endpoint(a, "x")
        to_ep = endpoint(b, "y")
        ov = overlay_record(kind="rendition_of", from_ep=from_ep, to_ep=to_ep, packages=(a, b))
        result = run_cli(payload(ov, context_record()))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["reason_code"], "rendition_endpoint_refused")

    def test_r2_05_missing_language_canonical_refused(self):
        a, b = base_packages()
        from_ep = endpoint(a, "x")
        to_ep = endpoint(b, "y")
        for package in (a, b):
            package.pop("language", None)
            package.pop("canonical", None)
        from_ep.pop("language", None)
        to_ep.pop("language", None)
        ov = overlay_record(kind="supports_under", from_ep=from_ep, to_ep=to_ep, packages=(a, b))
        result = run_cli(payload(ov, context_record()))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["reason_code"], "canonical_language_required")

    def test_r2_06_incomplete_release_pins_refused(self):
        a, b = base_packages()
        from_ep = endpoint(a, "x")
        to_ep = endpoint(b, "y")
        a.pop("package_manifest_digest")
        b.pop("package_manifest_digest")
        from_ep.pop("release_id")
        to_ep.pop("release_id")
        ov = overlay_record(kind="supports_under", from_ep=from_ep, to_ep=to_ep, packages=(a, b))
        result = run_cli(payload(ov, context_record()))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["reason_code"], "incomplete_release_pin")

    def test_r2_07_from_endpoint_into_package_b_refused(self):
        a, b = base_packages()
        from_ep = endpoint(b, "x")
        to_ep = endpoint(b, "y")
        ov = overlay_record(kind="supports_under", from_ep=from_ep, to_ep=to_ep, packages=(a, b))
        result = run_cli(payload(ov, context_record()))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["reason_code"], "endpoint_package_mismatch")

    def test_r2_08_contradicts_without_common_assumption_unresolved(self):
        a, b = base_packages()
        from_ep = endpoint(a, "p1")
        to_ep = endpoint(b, "p2")
        assertions = {
            "polarity": "conflict",
            "modality": "claim",
            "attribution": "both-sides",
            "quantifier_scope": "same-subject",
            "peer_quantifier_scope": "same-subject",
            "units": "kg",
            "peer_units": "kg",
            "valid_time": "2026",
            "peer_valid_time": "2026",
            "conditions": "shared-assumption-load",
            "peer_conditions": "shared-assumption-load",
            "harmonized": True,
        }
        ov = overlay_record(
            kind="contradicts_under", from_ep=from_ep, to_ep=to_ep, packages=(a, b),
            assertions=assertions,
        )
        ctx = context_record(reviews=[bound_review(evidence=INCOMPATIBILITY_EVIDENCE)])
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(report["status"], "inspectable_unresolved")
        self.assertEqual(report["reason_code"], "common_assumption_missing")
        self.assertNotEqual(report["reason_code"], "contradicts_under_retained")

    def test_r2_09_a9b_closure_with_b_not_permitted_refused(self):
        a, b = base_packages()
        from_ep = endpoint(a, "x")
        to_ep = endpoint(b, "y")
        ov = overlay_record(kind="requires_for_use", from_ep=from_ep, to_ep=to_ep, packages=(a, b))
        perms = {
            cpo.permission_key(a["package_id"], "A1"): {
                "permitted": True, "revoked": False, "accessible": True,
            },
            cpo.permission_key(b["package_id"], "B1"): {
                "permitted": False, "revoked": False, "accessible": True,
            },
        }
        ctx = context_record(
            permissions=perms,
            task_requirements=task_requirements_record(),
            mandatory_dependencies=[discharge("A"), discharge("B")],
        )
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["reason_code"], "endpoint_not_permitted")

    def test_r2_10_a3_lineage_with_b_not_permitted_refused(self):
        a, b = base_packages()
        from_ep = endpoint(a, "stmt-1", source_anchor="a1")
        to_ep = endpoint(b, "stmt-copy", source_anchor="b1")
        lineage = [{"kind": "quotes", "origin": "pkg-alpha@A1:stmt-1", "revision": "A1"}]
        grounding = {"from_anchor": "a1", "to_anchor": "b1", "support_kind": "quotation"}
        ov = overlay_record(
            kind="supports_under", from_ep=from_ep, to_ep=to_ep, packages=(a, b),
            lineage=lineage, grounding=grounding,
        )
        perms = {
            cpo.permission_key(a["package_id"], "A1"): {
                "permitted": True, "revoked": False, "accessible": True,
            },
            cpo.permission_key(b["package_id"], "B1"): {
                "permitted": False, "revoked": False, "accessible": True,
            },
        }
        result = run_cli(payload(ov, context_record(permissions=perms)))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["reason_code"], "endpoint_not_permitted")

    def test_r2_11_same_package_id_two_releases_refused(self):
        a = pkg("pkg-alpha", "A1", DIGEST_A1)
        b = pkg("pkg-alpha", "A2", DIGEST_B2)
        from_ep = endpoint(a, "x")
        to_ep = endpoint(b, "y")
        ov = overlay_record(kind="supports_under", from_ep=from_ep, to_ep=to_ep, packages=(a, b))
        perms = {
            cpo.permission_key("pkg-alpha", "A1"): {
                "permitted": True, "revoked": False, "accessible": True,
            },
            cpo.permission_key("pkg-alpha", "A2"): {
                "permitted": True, "revoked": False, "accessible": True,
            },
        }
        ctx = context_record(
            request_pins={"A": "A1", "B": "A2"},
            permissions=perms,
            reviews=[bound_review(
                pins={"A": "A1", "B": "A2"},
                digests=(DIGEST_A1, DIGEST_B2),
            )],
        )
        ov["assessment"]["reviewed_pins"] = {"A": "A1", "B": "A2"}
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["reason_code"], "same_package_both_sides")

    def test_r2_12_translations_path_case_refused(self):
        a, b = base_packages()
        b["path"] = "Translations/ru/x"
        from_ep = endpoint(a, "x")
        to_ep = endpoint(b, "y", path="Translations/ru/x")
        ov = overlay_record(kind="supports_under", from_ep=from_ep, to_ep=to_ep, packages=(a, b))
        result = run_cli(payload(ov, context_record()))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["reason_code"], "rendition_endpoint_refused")

    def test_r2_13_load_input_caps_read_before_size_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "huge.json"
            # Write more than MAX+1 so an uncapped read would load the whole file.
            path.write_bytes(b"{" + (b"y" * (MAX_BYTES + 4096)) + b"}")
            document, report = cpo.load_input(path)
            self.assertIsNone(document)
            self.assertEqual(report["reason_code"], "malformed_input")
            self.assertEqual(report["status"], "refused")
            self.assertLessEqual(report.get("size", MAX_BYTES + 1), MAX_BYTES + 1)


class FailClosedRound3Tests(unittest.TestCase):
    """KC-SWE round-3 remaining open paths (findings 1-8). Red on 17033619."""

    def _supported_pair(self):
        a, b = base_packages()
        from_ep = endpoint(a, "x")
        to_ep = endpoint(b, "y")
        ov = overlay_record(kind="supports_under", from_ep=from_ep, to_ep=to_ep, packages=(a, b))
        return a, b, ov

    def test_r3_01_request_pin_diverges_from_overlay(self):
        a, b, ov = self._supported_pair()
        # Match the KC-SWE probe shape: no assessment reviewed_pins that would
        # short-circuit before request-vs-overlay pin comparison.
        ov["assessment"].pop("reviewed_pins", None)
        perms = {
            cpo.permission_key(a["package_id"], "A2"): {
                "permitted": True, "revoked": False, "accessible": True,
            },
            cpo.permission_key(b["package_id"], "B1"): {
                "permitted": True, "revoked": False, "accessible": True,
            },
        }
        ctx = context_record(
            request_pins={"A": "A2", "B": "B1"},
            permissions=perms,
            reviews=[bound_review(pins={"A": "A2", "B": "B1"})],
        )
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["reason_code"], "request_pin_mismatch")

    def test_r3_02_partial_request_and_review_pins(self):
        _, _, ov = self._supported_pair()
        ov["assessment"].pop("reviewed_pins", None)
        ctx = context_record(
            request_pins={"A": "A1"},
            reviews=[bound_review(pins={"A": "A1"})],
        )
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["reason_code"], "request_pin_mismatch")

    def test_r3_03a_mandatory_dependencies_as_strings_malformed(self):
        a, b = base_packages()
        from_ep = endpoint(a, "x")
        to_ep = endpoint(b, "y")
        ov = overlay_record(kind="requires_for_use", from_ep=from_ep, to_ep=to_ep, packages=(a, b))
        ctx = context_record(
            task_requirements=task_requirements_record(),
            mandatory_dependencies=["A", "B"],
        )
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["reason_code"], "malformed_input")

    def test_r3_03b_discharged_string_false_malformed(self):
        a, b = base_packages()
        from_ep = endpoint(a, "x")
        to_ep = endpoint(b, "y")
        ov = overlay_record(kind="requires_for_use", from_ep=from_ep, to_ep=to_ep, packages=(a, b))
        ctx = context_record(
            task_requirements=task_requirements_record(),
            mandatory_dependencies=[
                discharge("A"),
                {"id": "B", "discharged": "false", "witness_ref": "wit-b"},
            ],
        )
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["reason_code"], "malformed_input")

    def test_r3_04_effects_authorized_never_from_caller(self):
        a, b = base_packages()
        from_ep = endpoint(a, "x")
        to_ep = endpoint(b, "y")
        ov = overlay_record(kind="requires_for_use", from_ep=from_ep, to_ep=to_ep, packages=(a, b))
        ctx = context_record(
            task_requirements=task_requirements_record(),
            mandatory_dependencies=[discharge("A"), discharge("B")],
            current_authority_for_effects=True,
        )
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(report["reason_code"], "prerequisite_closure_complete")
        self.assertFalse(report["effects_authorized"])

    def test_r3_05a_use_closure_incomplete_exit_3(self):
        a, b = base_packages()
        from_ep = endpoint(a, "x")
        to_ep = endpoint(b, "y")
        ov = overlay_record(kind="requires_for_use", from_ep=from_ep, to_ep=to_ep, packages=(a, b))
        ctx = context_record(
            task_requirements=task_requirements_record(),
            mandatory_dependencies=[
                discharge("A"),
                discharge("B", discharged=False, witness_ref=None, state="unknown"),
            ],
        )
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(report["status"], "inspectable_unresolved")
        self.assertEqual(report["reason_code"], "use_closure_incomplete")

    def test_r3_05b_unit_scope_unresolved_exit_3(self):
        a, b = base_packages()
        from_ep = endpoint(a, "claim-1")
        to_ep = endpoint(b, "claim-1")
        assertions = {
            "polarity": "affirmative",
            "modality": "claim",
            "attribution": "author",
            "quantifier_scope": "present-population",
            "conditions": "load-limit",
            "units": "kg",
            "valid_time": "2026",
            "peer_units": "lb",
            "peer_quantifier_scope": "historical-population",
        }
        ov = overlay_record(
            kind="compares_with", from_ep=from_ep, to_ep=to_ep, packages=(a, b), assertions=assertions,
        )
        result = run_cli(payload(ov, context_record(unit_scope_aligned=False)))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(report["status"], "inspectable_unresolved")
        self.assertEqual(report["reason_code"], "unit_scope_unresolved")

    def test_r3_06_self_review_not_independent(self):
        _, _, ov = self._supported_pair()
        reviews = [bound_review(author="same-person", reviewer="same-person")]
        result = run_cli(payload(ov, context_record(reviews=reviews)))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["reason_code"], "review_not_independent")

    def test_r3_07_non_boolean_permission_flags_malformed(self):
        a, b, ov = self._supported_pair()
        perms = {
            cpo.permission_key(a["package_id"], "A1"): {
                "permitted": True, "revoked": False, "accessible": True,
            },
            cpo.permission_key(b["package_id"], "B1"): {
                "permitted": True, "revoked": "true", "accessible": True,
            },
        }
        result = run_cli(payload(ov, context_record(permissions=perms)))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["reason_code"], "malformed_input")

    def test_r3_08_duplicate_json_keys_malformed(self):
        a, b, ov = self._supported_pair()
        data = payload(ov, context_record())
        text = json.dumps(data)
        # Force a duplicate "permitted" key inside the B1 permission object.
        needle = '"pkg-beta@B1": {"permitted": true, "revoked": false, "accessible": true}'
        replacement = (
            '"pkg-beta@B1": {"permitted": false, "revoked": false, '
            '"accessible": true, "permitted": true}'
        )
        self.assertIn(needle, text)
        raw = text.replace(needle, replacement, 1).encode("utf-8")
        result = run_cli(raw, as_bytes=True)
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["reason_code"], "malformed_input")

    def test_r3_regression_backslash_translations_path(self):
        a, b = base_packages()
        from_ep = endpoint(a, "x")
        to_ep = endpoint(b, "y", path="translations\\ru\\x")
        ov = overlay_record(kind="supports_under", from_ep=from_ep, to_ep=to_ep, packages=(a, b))
        result = run_cli(payload(ov, context_record()))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["reason_code"], "rendition_endpoint_refused")

    def test_r3_regression_dotdot_translations_path(self):
        a, b = base_packages()
        b["path"] = "papers/../translations/ru/x"
        from_ep = endpoint(a, "x")
        to_ep = endpoint(b, "y", path="papers/../translations/ru/x")
        ov = overlay_record(kind="supports_under", from_ep=from_ep, to_ep=to_ep, packages=(a, b))
        result = run_cli(payload(ov, context_record()))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["reason_code"], "rendition_endpoint_refused")


class FailClosedRound4Tests(unittest.TestCase):
    """KC-SWE round-4 strict input types / no-crash (findings 1-6). Red on a51dbab."""

    def _supported_pair(self):
        a, b = base_packages()
        from_ep = endpoint(a, "x")
        to_ep = endpoint(b, "y")
        ov = overlay_record(kind="supports_under", from_ep=from_ep, to_ep=to_ep, packages=(a, b))
        return a, b, ov

    def test_r4_01_non_object_package_manifest_digest_malformed(self):
        a, b, ov = self._supported_pair()
        ov["packages"]["A"]["package_manifest_digest"] = "not-an-object"
        result = run_cli(payload(ov, context_record()))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["reason_code"], "malformed_input")

    def test_r4_02_unhashable_relation_kind_malformed(self):
        a, b, ov = self._supported_pair()
        ov["relation"]["kind"] = ["supports_under"]
        result = run_cli(payload(ov, context_record()))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["reason_code"], "malformed_input")

    def test_r4_03_digest_algorithm_and_value_must_be_sha256_hex(self):
        a, b, ov = self._supported_pair()
        ov["packages"]["A"]["package_manifest_digest"]["algorithm"] = "x"
        ov["packages"]["A"]["package_manifest_digest"]["value"] = "x"
        result = run_cli(payload(ov, context_record()))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["reason_code"], "malformed_input")

    def test_r4_04_digest_fields_reject_non_strings(self):
        a, b, ov = self._supported_pair()
        ov["packages"]["B"]["package_manifest_digest"]["byte_domain"] = 0
        ov["packages"]["B"]["package_manifest_digest"]["source_revision"] = True
        result = run_cli(payload(ov, context_record()))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["reason_code"], "malformed_input")

    def test_r4_05_endpoint_ids_reject_non_strings(self):
        a, b, ov = self._supported_pair()
        ov["relation"]["from"]["object_id"] = 0
        ov["relation"]["to"]["source_anchor"] = True
        result = run_cli(payload(ov, context_record()))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["reason_code"], "malformed_input")

    def test_r4_06_accessible_missing_refused(self):
        a, b, ov = self._supported_pair()
        perms = {
            cpo.permission_key(a["package_id"], "A1"): {
                "permitted": True, "revoked": False,
            },
            cpo.permission_key(b["package_id"], "B1"): {
                "permitted": True, "revoked": False, "accessible": True,
            },
        }
        result = run_cli(payload(ov, context_record(permissions=perms)))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertIn(report["reason_code"], {
            "malformed_input", "endpoint_inaccessible", "endpoint_not_permitted",
        })

    def test_r4_07_grounding_required_and_must_match_endpoints(self):
        a, b, ov = self._supported_pair()
        ov["relation"].pop("grounding", None)
        result = run_cli(payload(ov, context_record()))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["reason_code"], "malformed_input")

        a, b, ov = self._supported_pair()
        ov["relation"]["grounding"]["from_anchor"] = "different-from-endpoint"
        result = run_cli(payload(ov, context_record()))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["reason_code"], "malformed_input")

    def test_r4_08_path_non_string_malformed(self):
        a, b, ov = self._supported_pair()
        ov["packages"]["A"]["path"] = 0
        result = run_cli(payload(ov, context_record()))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["reason_code"], "malformed_input")

    def test_r4_09_cli_unexpected_exception_prints_refusal(self):
        """Guard: unexpected evaluate errors still emit a refusal report and exit 1."""
        a, b, ov = self._supported_pair()
        data = payload(ov, context_record())
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "input.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            injector = (
                "import sys\n"
                "import tools.cross_package_overlay as m\n"
                "m.evaluate_document = lambda d: (_ for _ in ()).throw("
                "RuntimeError('injected'))\n"
                "sys.argv = ['cross_package_overlay.py', '--input', sys.argv[1]]\n"
                "raise SystemExit(m.main(sys.argv))\n"
            )
            result = subprocess.run(
                [sys.executable, "-B", "-c", injector, str(path)],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                check=False,
                timeout=30,
            )
            report = require_report(self, result)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(report["status"], "refused")
            self.assertEqual(report["reason_code"], "malformed_input")


class FailClosedRound5Tests(unittest.TestCase):
    """KC-Brain semantic findings G11-R1/R2/R3 + A3/A5 cautions. Red on 1e5db531."""

    IDENTITY_FIELDS = (
        "component_id",
        "representation_id",
        "representation_digest",
        "package_manifest_digest",
    )

    def _a10_positive(self):
        a, b = base_packages()
        from_ep = endpoint(a, "x")
        to_ep = endpoint(b, "y")
        ov = overlay_record(
            kind="compares_with", from_ep=from_ep, to_ep=to_ep, packages=(a, b),
            assertions=comparable_assertions(),
        )
        ctx = context_record(unit_scope_aligned=True)
        return a, b, ov, ctx

    def test_r5_r1_minus_each_identity_component_refused(self):
        for field in self.IDENTITY_FIELDS:
            with self.subTest(field=field):
                _, _, ov, ctx = self._a10_positive()
                ov["relation"]["from"].pop(field, None)
                result = run_cli(payload(ov, ctx))
                report = require_report(self, result)
                self.assertEqual(result.returncode, 1, field)
                self.assertEqual(report["status"], "refused", field)
                self.assertEqual(report["reason_code"], "incomplete_release_pin", field)
                self.assertNotEqual(report["reason_code"], "scoped_inspection_ok", field)

    def test_r5_r1_valid_but_different_endpoint_digest_refused(self):
        a, b, ov, ctx = self._a10_positive()
        other = {
            "algorithm": "sha256",
            "value": "e" * 64,
            "byte_domain": "package-manifest",
            "source_revision": "A1",
        }
        ov["relation"]["from"]["package_manifest_digest"] = other
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["reason_code"], "endpoint_digest_mismatch")

    def test_r5_r1_representation_identity_mismatch_refused(self):
        _, _, ov, ctx = self._a10_positive()
        ov["relation"]["to"]["representation_digest"]["source_revision"] = "OTHER-REL"
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["reason_code"], "representation_identity_mismatch")

    def test_r5_r2_missing_reviewer_not_scoped_ok(self):
        _, _, ov, ctx = self._a10_positive()
        ctx["reviews"] = [bound_review(reviewer="")]
        ctx["reviews"][0].pop("reviewer")
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertNotEqual(report.get("reason_code"), "scoped_inspection_ok")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["reason_code"], "review_missing")

    def test_r5_r2_declined_verdict_not_scoped_ok(self):
        _, _, ov, ctx = self._a10_positive()
        ctx["reviews"] = [bound_review(verdict="declined")]
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["reason_code"], "review_not_accepted")
        self.assertNotEqual(report["reason_code"], "scoped_inspection_ok")

    def test_r5_r2_rejected_verdict_not_scoped_ok(self):
        _, _, ov, ctx = self._a10_positive()
        ctx["reviews"] = [bound_review(verdict="rejected")]
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["reason_code"], "review_not_accepted")

    def test_r5_r2_reviewed_edge_revision_mismatch(self):
        _, _, ov, ctx = self._a10_positive()
        ctx["reviews"] = [bound_review(reviewed_edge_revision="other-ov")]
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["reason_code"], "review_edge_mismatch")

    def test_r5_r2_relation_id_mismatch(self):
        _, _, ov, ctx = self._a10_positive()
        ctx["reviews"] = [bound_review(relation_id="rel-other")]
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["reason_code"], "review_edge_mismatch")

    def test_r5_r2_scope_unrelated(self):
        _, _, ov, ctx = self._a10_positive()
        ctx["reviews"] = [bound_review(scope="execution-grant")]
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["reason_code"], "review_scope_incompatible")

    def test_r5_r2_same_releases_different_manifest_bytes(self):
        _, _, ov, ctx = self._a10_positive()
        other = {
            "algorithm": "sha256",
            "value": "f" * 64,
            "byte_domain": "package-manifest",
            "source_revision": "B1",
        }
        ctx["reviews"] = [bound_review(digests=(DIGEST_A1, other))]
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["reason_code"], "review_pin_mismatch")

    def test_r5_r3_missing_comparability_unresolved(self):
        a, b = base_packages()
        from_ep = endpoint(a, "x")
        to_ep = endpoint(b, "y")
        assertions = {
            "polarity": "affirmative",
            "modality": "claim",
            "attribution": "author",
            "quantifier_scope": "all-applicable",
            "conditions": "shared-load-limit",
            "units": "kg",
            "valid_time": "2026",
        }
        ov = overlay_record(
            kind="compares_with", from_ep=from_ep, to_ep=to_ep, packages=(a, b),
            assertions=assertions,
        )
        result = run_cli(payload(ov, context_record()))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(report["status"], "inspectable_unresolved")
        self.assertEqual(report["reason_code"], "unit_scope_unresolved")
        self.assertNotEqual(report["reason_code"], "scoped_inspection_ok")

    def test_r5_r3_incompatible_time_conditions_refused(self):
        a, b = base_packages()
        from_ep = endpoint(a, "x")
        to_ep = endpoint(b, "y")
        ov = overlay_record(
            kind="compares_with", from_ep=from_ep, to_ep=to_ep, packages=(a, b),
            assertions=comparable_assertions(
                peer_valid_time="1999",
                peer_conditions="other-population",
            ),
        )
        result = run_cli(payload(ov, context_record(unit_scope_aligned=True)))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["reason_code"], "conditions_incompatible")

    def test_r5_a3_unresolved_mandatory_preserved(self):
        a, b = base_packages()
        from_ep = endpoint(a, "stmt-1", source_anchor="a1")
        to_ep = endpoint(b, "stmt-copy", source_anchor="b1")
        lineage = [
            {"kind": "quotes", "origin": "pkg-alpha@A1:stmt-1", "revision": "A1"},
            {"kind": "rendition_of", "origin": "pkg-beta@B1:stmt-copy", "revision": "B1-tr"},
        ]
        grounding = {
            "from_anchor": "a1",
            "to_anchor": "b1",
            "support_kind": "quotation",
        }
        ov = overlay_record(
            kind="supports_under", from_ep=from_ep, to_ep=to_ep, packages=(a, b),
            lineage=lineage, grounding=grounding,
        )
        ctx = context_record(
            task_requirements=task_requirements_record(),
            mandatory_dependencies=[
                discharge("A"),
                discharge("B", discharged=False, witness_ref=None, state="unknown"),
            ],
        )
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(report["status"], "inspectable_unresolved")
        self.assertEqual(report["reason_code"], "use_closure_incomplete")
        self.assertFalse(report["use_closure_complete"])
        self.assertEqual(report["external_effects"], 0)
        self.assertTrue(report.get("unresolved_mandatory"))
        self.assertTrue(any(item.get("id") == "B" for item in report.get("unresolved_members", [])))

    def test_r5_a5_harmonized_alone_unproven(self):
        a, b = base_packages()
        from_ep = endpoint(a, "p1")
        to_ep = endpoint(b, "p2")
        assertions = {
            "polarity": "conflict",
            "modality": "claim",
            "attribution": "both-sides",
            "quantifier_scope": "same-subject",
            "conditions": "shared-assumption-load",
            "common_assumption": "shared-domain-x-on-same-referent",
            "units": "kg",
            "valid_time": "2026",
            "harmonized": True,
        }
        ov = overlay_record(
            kind="contradicts_under", from_ep=from_ep, to_ep=to_ep, packages=(a, b),
            assertions=assertions,
        )
        result = run_cli(payload(ov, context_record()))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(report["status"], "inspectable_unresolved")
        self.assertEqual(report["reason_code"], "premise_overlap_unproven")
        self.assertNotEqual(report["reason_code"], "contradicts_under_retained")

    def test_r5_a5_overlap_without_bound_review_unresolved(self):
        a, b = base_packages()
        from_ep = endpoint(a, "p1")
        to_ep = endpoint(b, "p2")
        ov = overlay_record(
            kind="contradicts_under", from_ep=from_ep, to_ep=to_ep, packages=(a, b),
            assertions=a5_conflict_assertions(),
        )
        result = run_cli(payload(ov, context_record(reviews=[])))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(report["status"], "inspectable_unresolved")
        self.assertEqual(report["reason_code"], "no_bound_edge_review")


class FailClosedRound6Tests(unittest.TestCase):
    """KC-SWE round-6 findings on 1cd98f18: R3 full PREMISE_OVERLAP, R1 package map, R2 selection."""

    def _a10_positive(self):
        a, b = base_packages()
        from_ep = endpoint(a, "x")
        to_ep = endpoint(b, "y")
        ov = overlay_record(
            kind="compares_with", from_ep=from_ep, to_ep=to_ep, packages=(a, b),
            assertions=comparable_assertions(),
        )
        ctx = context_record(unit_scope_aligned=True)
        return a, b, ov, ctx

    def test_r6_r3_missing_peer_valid_time_unresolved_despite_aligned(self):
        a, b, ov, ctx = self._a10_positive()
        del ov["relation"]["assertions"]["peer_valid_time"]
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(report["status"], "inspectable_unresolved")
        self.assertEqual(report["reason_code"], "unit_scope_unresolved")
        self.assertNotEqual(report["reason_code"], "scoped_inspection_ok")

    def test_r6_r3_missing_peer_conditions_unresolved_despite_aligned(self):
        a, b, ov, ctx = self._a10_positive()
        del ov["relation"]["assertions"]["peer_conditions"]
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(report["status"], "inspectable_unresolved")
        self.assertEqual(report["reason_code"], "unit_scope_unresolved")

    def test_r6_r3_missing_valid_time_unresolved_despite_aligned(self):
        a, b, ov, ctx = self._a10_positive()
        del ov["relation"]["assertions"]["valid_time"]
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(report["status"], "inspectable_unresolved")
        self.assertEqual(report["reason_code"], "unit_scope_unresolved")

    def test_r6_r3_missing_conditions_unresolved_despite_aligned(self):
        a, b, ov, ctx = self._a10_positive()
        del ov["relation"]["assertions"]["conditions"]
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(report["status"], "inspectable_unresolved")
        self.assertEqual(report["reason_code"], "unit_scope_unresolved")

    def test_r6_r1_undeclared_representation_id_refused(self):
        a, b, ov, ctx = self._a10_positive()
        ov["relation"]["from"]["representation_id"] = "ru-draft"
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["reason_code"], "representation_identity_mismatch")
        self.assertNotEqual(report["reason_code"], "scoped_inspection_ok")

    def test_r6_r1_declared_but_different_digest_refused(self):
        a, b, ov, ctx = self._a10_positive()
        ov["relation"]["to"]["representation_digest"] = representation_digest_obj(
            "B1", value="e" * 64,
        )
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["reason_code"], "representation_identity_mismatch")

    def test_r6_r1_declared_representation_language_ru_refused(self):
        a = pkg("pkg-alpha", "A1", DIGEST_A1, representation_language="ru")
        b = pkg("pkg-beta", "B1", DIGEST_B1)
        from_ep = endpoint(a, "x")
        to_ep = endpoint(b, "y")
        ov = overlay_record(
            kind="compares_with", from_ep=from_ep, to_ep=to_ep, packages=(a, b),
            assertions=comparable_assertions(),
        )
        result = run_cli(payload(ov, context_record(unit_scope_aligned=True)))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["reason_code"], "rendition_endpoint_refused")

    def test_r6_r1_endpoint_language_mismatch_refused(self):
        a, b, ov, ctx = self._a10_positive()
        ov["relation"]["from"]["language"] = "ru"
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["reason_code"], "rendition_endpoint_refused")

    def test_r6_r1_missing_representations_map_malformed(self):
        a, b, ov, ctx = self._a10_positive()
        del ov["packages"]["A"]["representations"]
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["reason_code"], "malformed_input")

    def test_r6_r2_other_relation_first_then_own_accepted(self):
        a, b, ov, ctx = self._a10_positive()
        ctx["reviews"] = [
            bound_review(relation_id="rel-other"),
            bound_review(),
        ]
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(report["reason_code"], "scoped_inspection_ok")

    def test_r6_r2_own_first_then_other_accepted(self):
        a, b, ov, ctx = self._a10_positive()
        ctx["reviews"] = [
            bound_review(),
            bound_review(relation_id="rel-other"),
        ]
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(report["reason_code"], "scoped_inspection_ok")

    def test_r6_r2_disagreeing_bound_reviews_refused(self):
        a, b, ov, ctx = self._a10_positive()
        ctx["reviews"] = [
            bound_review(verdict="accepted", reviewer="rev-a", author="author-a"),
            bound_review(verdict="declined", reviewer="rev-b", author="author-b"),
        ]
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["reason_code"], "review_verdict_conflict")
        self.assertNotEqual(report["reason_code"], "scoped_inspection_ok")


class FailClosedRound7Tests(unittest.TestCase):
    """KC-Brain / Agent-Brain A5+A9 semantic decisions. Red on 8f9e1be8."""

    def _a5_payload(self, assertions: dict, *, reviews=None, **ctx_extra):
        a, b = base_packages()
        from_ep = endpoint(a, "p1")
        to_ep = endpoint(b, "p2")
        ov = overlay_record(
            kind="contradicts_under", from_ep=from_ep, to_ep=to_ep, packages=(a, b),
            assertions=assertions,
        )
        if reviews is None:
            reviews = [bound_review(evidence=INCOMPATIBILITY_EVIDENCE)]
        return ov, context_record(reviews=reviews, **ctx_extra)

    def test_r7_a5_compatible_bounds_without_incompatibility_evidence_not_retained(self):
        # x <= 10 vs x >= 5: equal metadata + harmonized, but no incompatibility explanation.
        assertions = a5_conflict_assertions(
            from_proposition="x <= 10",
            to_proposition="x >= 5",
        )
        ov, ctx = self._a5_payload(
            assertions,
            reviews=[bound_review()],  # accepted R2 binding, empty/absent evidence
        )
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(report["status"], "inspectable_unresolved")
        self.assertEqual(report["reason_code"], "no_bound_incompatibility_assessment")
        self.assertNotEqual(report["reason_code"], "contradicts_under_retained")

    def test_r7_a5_unequal_time_windows_unresolved_not_refused(self):
        assertions = a5_conflict_assertions(
            valid_time="[0,10]",
            peer_valid_time="[5,15]",
        )
        ov, ctx = self._a5_payload(assertions)
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(report["status"], "inspectable_unresolved")
        self.assertEqual(report["reason_code"], "premise_alignment_unsupported")
        self.assertNotEqual(report["reason_code"], "conditions_incompatible")
        self.assertTrue(report.get("both_facts_retained"))

    def test_r7_a5_empty_common_assumption_unresolved(self):
        assertions = a5_conflict_assertions(common_assumption="")
        ov, ctx = self._a5_payload(assertions)
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(report["status"], "inspectable_unresolved")
        self.assertEqual(report["reason_code"], "common_assumption_missing")

    def test_r7_a5_missing_common_assumption_unresolved(self):
        assertions = a5_conflict_assertions()
        del assertions["common_assumption"]
        ov, ctx = self._a5_payload(assertions)
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(report["status"], "inspectable_unresolved")
        self.assertEqual(report["reason_code"], "common_assumption_missing")

    def test_r7_a5_positive_retained_with_evidence_no_winner(self):
        assertions = a5_conflict_assertions()
        ov, ctx = self._a5_payload(assertions)
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(report["reason_code"], "contradicts_under_retained")
        self.assertTrue(report["both_facts_retained"])
        self.assertFalse(report.get("winner_selected", False))
        self.assertFalse(report.get("effects_authorized", False))

    def test_r7_a9_all_discharged_without_requirements_revision_unresolved(self):
        a, b = base_packages()
        ov = overlay_record(
            kind="requires_for_use",
            from_ep=endpoint(a, "x"), to_ep=endpoint(b, "y"), packages=(a, b),
        )
        ctx = context_record(
            mandatory_dependencies=[discharge("A"), discharge("B")],
        )
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(report["status"], "inspectable_unresolved")
        self.assertIn(report["reason_code"], {
            "use_closure_incomplete", "requirements_revision_missing",
        })
        self.assertNotEqual(report["reason_code"], "prerequisite_closure_complete")
        self.assertTrue(report.get("unresolved_mandatory"))

    def test_r7_a9_omitted_member_unresolved(self):
        a, b = base_packages()
        ov = overlay_record(
            kind="requires_for_use",
            from_ep=endpoint(a, "x"), to_ep=endpoint(b, "y"), packages=(a, b),
        )
        ctx = context_record(
            task_requirements=task_requirements_record(members=["A", "B"]),
            mandatory_dependencies=[discharge("A")],
        )
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(report["status"], "inspectable_unresolved")
        self.assertEqual(report["reason_code"], "use_closure_incomplete")
        self.assertTrue(report.get("unresolved_mandatory"))

    def test_r7_a9_duplicate_discharge_aliases_unresolved(self):
        a, b = base_packages()
        ov = overlay_record(
            kind="requires_for_use",
            from_ep=endpoint(a, "x"), to_ep=endpoint(b, "y"), packages=(a, b),
        )
        ctx = context_record(
            task_requirements=task_requirements_record(members=["A", "B"]),
            mandatory_dependencies=[
                discharge("A", witness_ref="wit-a1"),
                discharge("A", witness_ref="wit-a2"),
            ],
        )
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(report["status"], "inspectable_unresolved")
        self.assertIn(report["reason_code"], {
            "use_closure_incomplete", "requirements_member_duplicate_discharge",
        })

    def test_r7_a9_unknown_extra_member_unresolved(self):
        a, b = base_packages()
        ov = overlay_record(
            kind="requires_for_use",
            from_ep=endpoint(a, "x"), to_ep=endpoint(b, "y"), packages=(a, b),
        )
        ctx = context_record(
            task_requirements=task_requirements_record(members=["A", "B"]),
            mandatory_dependencies=[
                discharge("A"), discharge("B"), discharge("C"),
            ],
        )
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(report["status"], "inspectable_unresolved")
        self.assertIn(report["reason_code"], {
            "use_closure_incomplete", "requirements_unknown_member",
        })

    def test_r7_a9_discharged_without_witness_unresolved(self):
        a, b = base_packages()
        ov = overlay_record(
            kind="requires_for_use",
            from_ep=endpoint(a, "x"), to_ep=endpoint(b, "y"), packages=(a, b),
        )
        ctx = context_record(
            task_requirements=task_requirements_record(members=["A", "B"]),
            mandatory_dependencies=[
                discharge("A"),
                {"id": "B", "discharged": True},
            ],
        )
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(report["status"], "inspectable_unresolved")
        self.assertIn(report["reason_code"], {
            "use_closure_incomplete", "discharge_witness_missing",
        })

    def test_r7_a9_explicit_empty_set_complete(self):
        a, b = base_packages()
        ov = overlay_record(
            kind="requires_for_use",
            from_ep=endpoint(a, "x"), to_ep=endpoint(b, "y"), packages=(a, b),
        )
        ctx = context_record(
            task_requirements=task_requirements_record(
                members=[],
                empty_set_justification="R1 intentionally requires no overlay members",
            ),
            mandatory_dependencies=[],
        )
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(report["reason_code"], "prerequisite_closure_complete")
        self.assertFalse(report["effects_authorized"])

    def test_r7_a9_empty_set_without_justification_unresolved(self):
        a, b = base_packages()
        ov = overlay_record(
            kind="requires_for_use",
            from_ep=endpoint(a, "x"), to_ep=endpoint(b, "y"), packages=(a, b),
        )
        ctx = context_record(
            task_requirements=task_requirements_record(members=[]),
            mandatory_dependencies=[],
        )
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(report["status"], "inspectable_unresolved")
        self.assertEqual(report["reason_code"], "use_closure_incomplete")

    def test_r7_a3_early_return_keeps_unresolved_mandatory(self):
        a, b = base_packages()
        from_ep = endpoint(a, "stmt-1", source_anchor="a1")
        to_ep = endpoint(b, "stmt-copy", source_anchor="b1")
        ov = overlay_record(
            kind="supports_under", from_ep=from_ep, to_ep=to_ep, packages=(a, b),
            lineage=[{"kind": "quotes", "origin": "pkg-alpha@A1:stmt-1", "revision": "A1"}],
            grounding={
                "from_anchor": "a1", "to_anchor": "b1", "support_kind": "quotation",
            },
        )
        ctx = context_record(
            task_requirements=task_requirements_record(),
            mandatory_dependencies=[
                discharge("A"),
                discharge("B", discharged=False, witness_ref=None, state="unknown"),
            ],
        )
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(report["status"], "inspectable_unresolved")
        self.assertEqual(report["reason_code"], "use_closure_incomplete")
        self.assertTrue(report.get("unresolved_mandatory"))
        self.assertNotEqual(report["reason_code"], "single_lineage_family")

    def test_r7_a5_early_return_keeps_unresolved_mandatory(self):
        assertions = a5_conflict_assertions()
        ov, ctx = self._a5_payload(
            assertions,
            task_requirements=task_requirements_record(),
            mandatory_dependencies=[
                discharge("A"),
                discharge("B", discharged=False, witness_ref=None, state="unknown"),
            ],
        )
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(report["status"], "inspectable_unresolved")
        self.assertEqual(report["reason_code"], "use_closure_incomplete")
        self.assertTrue(report.get("unresolved_mandatory"))
        self.assertNotEqual(report["reason_code"], "contradicts_under_retained")


if __name__ == "__main__":
    unittest.main()

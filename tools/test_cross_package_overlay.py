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


def pkg(package_id: str, release_id: str, digest: dict, *, language: str = "en", path: str = "objects/o.json") -> dict:
    return {
        "package_id": package_id,
        "package_manifest_digest": digest,
        "release_id": release_id,
        "language": language,
        "canonical": language == "en",
        "path": path,
    }


def endpoint(package: dict, object_id: str, *, component_id: str = "main",
             representation_id: str = "canonical-en", source_anchor: str = "s1",
             representation_digest: str | None = None, path: str | None = None) -> dict:
    return {
        "package_id": package["package_id"],
        "package_manifest_digest": package["package_manifest_digest"],
        "release_id": package["release_id"],
        "component_id": component_id,
        "object_id": object_id,
        "representation_id": representation_id,
        "representation_digest": {
            "algorithm": "sha256",
            "value": representation_digest or ("d" * 64),
            "byte_domain": "object-bytes",
            "source_revision": package["release_id"],
        },
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


def context_record(*, request_pins: dict | None = None, permissions: dict | None = None,
                   reviews: list | None = None, published_releases: list | None = None,
                   mandatory_dependencies: list | None = None,
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
        "reviews": reviews if reviews is not None else [{
            "pins": {"A": "A1", "B": "B1"},
            "independent": True,
            "verdict": "accepted",
            "scope": "inspection-only",
            "reviewed_edge_revision": "ov-1",
        }],
        "published_releases": published_releases or [],
        "mandatory_dependencies": mandatory_dependencies,
        "current_authority_for_effects": current_authority_for_effects,
    }
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
        ov = overlay_record(kind="compares_with", from_ep=from_ep, to_ep=to_ep, packages=(a, b))
        result = run_cli(payload(ov, context_record()))
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
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(report["reason_code"], "unit_scope_unresolved")
        self.assertEqual(report["status"], "inspectable_unresolved")

    def test_g11_a3_copied_support_one_lineage_family(self):
        a, b = base_packages()
        from_ep = endpoint(a, "stmt-1")
        to_ep = endpoint(b, "stmt-copy")
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
        assertions = {
            "polarity": "conflict",
            "modality": "claim",
            "attribution": "both-sides",
            "quantifier_scope": "same-subject",
            "conditions": "shared-assumption-load",
            "units": "kg",
            "valid_time": "2026",
            "harmonized": True,
        }
        ov = overlay_record(
            kind="contradicts_under", from_ep=from_ep, to_ep=to_ep, packages=(a, b), assertions=assertions,
        )
        result = run_cli(payload(ov, context_record()))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(report["reason_code"], "contradicts_under_retained")
        self.assertTrue(report["both_facts_retained"])
        self.assertFalse(report.get("winner_selected", False))

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
            mandatory_dependencies=[
                {"id": "A", "discharged": True},
                {"id": "B", "discharged": False, "state": "unknown"},
            ],
            current_authority_for_effects=False,
        )
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(report["reason_code"], "use_closure_incomplete")
        self.assertEqual(report["status"], "inspectable_unresolved")
        self.assertFalse(report["use_closure_complete"])
        self.assertEqual(report["external_effects"], 0)

    def test_g11_a9b_completed_dependency_still_needs_authority(self):
        a, b = base_packages()
        from_ep = endpoint(a, "x")
        to_ep = endpoint(b, "y")
        ov = overlay_record(kind="requires_for_use", from_ep=from_ep, to_ep=to_ep, packages=(a, b))
        ctx = context_record(
            mandatory_dependencies=[
                {"id": "A", "discharged": True},
                {"id": "B", "discharged": True},
            ],
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
        ov = overlay_record(kind="supports_under", from_ep=from_ep, to_ep=to_ep, packages=(a, b))
        result = run_cli(payload(ov, context_record()))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(report["reason_code"], "scoped_inspection_ok")
        self.assertEqual(report["status"], "inspectable")
        self.assertFalse(report.get("execution_granted", False))
        self.assertFalse(report.get("proof_promoted", False))


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
            {"pins": {"A": "A0", "B": "B0"}, "independent": True},
            {"pins": {"A": "A1", "B": "B1"}, "independent": False},
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

    def test_r2_08_contradicts_without_common_assumption_refused(self):
        a, b = base_packages()
        from_ep = endpoint(a, "p1")
        to_ep = endpoint(b, "p2")
        assertions = {
            "polarity": "conflict",
            "modality": "claim",
            "attribution": "both-sides",
            "quantifier_scope": "same-subject",
            "units": "kg",
            "valid_time": "2026",
        }
        ov = overlay_record(
            kind="contradicts_under", from_ep=from_ep, to_ep=to_ep, packages=(a, b),
            assertions=assertions,
        )
        result = run_cli(payload(ov, context_record()))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["reason_code"], "common_assumption_required")

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
            mandatory_dependencies=[
                {"id": "A", "discharged": True},
                {"id": "B", "discharged": True},
            ],
        )
        result = run_cli(payload(ov, ctx))
        report = require_report(self, result)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["status"], "refused")
        self.assertEqual(report["reason_code"], "endpoint_not_permitted")

    def test_r2_10_a3_lineage_with_b_not_permitted_refused(self):
        a, b = base_packages()
        from_ep = endpoint(a, "stmt-1")
        to_ep = endpoint(b, "stmt-copy")
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
            reviews=[{
                "pins": {"A": "A1", "B": "A2"},
                "independent": True,
                "verdict": "accepted",
                "scope": "inspection-only",
                "reviewed_edge_revision": "ov-1",
            }],
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


if __name__ == "__main__":
    unittest.main()

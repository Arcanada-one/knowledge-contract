#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Maintain stable requirement identifiers and a faithful register; test references do not certify conformance.

--assign numbers new normative sentences without renumbering existing IDs; --update rewrites the register.
The normal invocation is read-only and fails on missing IDs, duplicates or a stale register.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTER = "engineering/specifications/requirements.json"
PREFIXES = {
    "knowledge-contract-core": "KCC", "contract-family": "KOP", "semantic-types": "SEM", "context-package": "CTX",
    "compiled-artifact-contract": "CKA", "artifact-registry": "REG", "status-model": "STA",
    "cache-identity-and-invalidation": "CCH", "reuse-policy": "RUS", "knowledge-evolution": "EVO", "book-package": "BPK", "pipeline": "PIP",
    "location-registry": "LOC", "private-artifact-registry": "PAR",
}
NORMATIVE = re.compile(r"\b(?:MUST|SHALL|SHOULD|MAY|REQUIRED|RECOMMENDED|OPTIONAL)\b")
ID = re.compile(r"^\*\*([A-Z]+-R[0-9]{3,})\.\*\*\s+", re.S)


def targets(root):
    rows = [(root / f"engineering/specifications/{slug}/SPECIFICATION.md", prefix) for slug, prefix in PREFIXES.items()]
    rows.append((root / "appendices/api-integration/APPENDIX.md", "API"))
    return rows


def sentences(paragraph):
    return re.split(r"(?<=[.!?])\s+(?=[A-Z`“‘(])", paragraph.strip())


def assign(path: Path, prefix: str):
    text = path.read_text()
    used = [int(v) for v in re.findall(r"\*\*" + re.escape(prefix) + r"-R([0-9]+)\.\*\*", text)]
    next_id = max(used, default=0) + 1
    chunks = []
    in_fence = False
    for chunk in text.strip().split("\n\n"):
        if chunk.lstrip().startswith("```") or in_fence:
            if sum(1 for line in chunk.splitlines() if line.startswith("```")) % 2:
                in_fence = not in_fence
            chunks.append(chunk)
            continue
        if not NORMATIVE.search(chunk) or ID.match(chunk):
            chunks.append(chunk)
            continue
        if chunk.startswith(("#", "|", "---")):
            raise ValueError(f"{path}: normative language in a heading/table needs an explicit prose requirement")
        bucket = []
        for sentence in sentences(chunk):
            if NORMATIVE.search(sentence):
                if bucket:
                    chunks.append(" ".join(bucket))
                    bucket = []
                chunks.append(f"**{prefix}-R{next_id:03d}.** {sentence}")
                next_id += 1
            else:
                bucket.append(sentence)
        if bucket:
            chunks.append(" ".join(bucket))
    path.write_text("\n\n".join(chunks) + "\n")


def test_references(prefix, text):
    # These are narrow regression examples. Unlisted obligations still need implementation-specific evidence.
    matches = []
    references = {
        "BPK": [
            (("no parent traversal or symlinks",), "tools/test_book_package_review.py::RightsAndProjectionTests.test_component_directory_symlink_is_rejected_but_regular_nesting_is_valid"),
            (("non-author", "Restricted or unknown", "nonempty `publishable_layers`", "author_open"), "tools/test_book_package_review.py::RightsAndProjectionTests.test_license_cannot_override_restricted_or_unknown_class"),
            (("candidate_projection(package_directory)", "validate a private immutable byte snapshot", "raw manifest"), "tools/test_book_package_review.py::RightsAndProjectionTests.test_projection_binds_its_own_rendering_and_rejects_raw_inputs"),
            (("first matching row", "derived `package_status`"), "tools/test_book_package_review.py::ReviewReadinessTests.test_total_decision_table_over_all_status_dimensions"),
            (("negative", "same-session", "Same-session", "reviewer MUST", "result MUST"), "tools/test_book_package_review.py::ReviewReadinessTests.test_negative_partial_same_session_or_same_identity_review_cannot_be_ready"),
            (("Extraction `pass`", "applicable passing check"), "tools/test_book_package_review.py::ReviewReadinessTests.test_empty_unknown_or_failed_checks_cannot_establish_extraction_pass"),
            (("MUST state the inapplicability reason",), "tools/test_book_package_review.py::ReviewReadinessTests.test_not_applicable_requires_explicit_reason"),
            (("Payload headings", "public Markdown renderer"), "tools/test_book_package_review.py::LedgerAndRenderingTests.test_full_records_survive_rendering_and_cannot_inject_heading"),
            (("overlaps the edit", "dependency list cannot"), "tools/test_book_package_review.py::LedgerAndRenderingTests.test_accepted_edit_detects_overlap_without_producer_dependency_list"),
            (("stale or rejected endpoint",), "tools/test_book_package_review.py::LedgerAndRenderingTests.test_relation_to_rejected_endpoint_cannot_stay_reviewed"),
            (("duplicate object member",), "tools/test_book_package_review.py::LedgerAndRenderingTests.test_duplicate_json_keys_and_nonfinite_values_are_refused"),
        ],
        "CCH": [
            (("one linearizable decision", "head update and increment", "late worker MUST NOT"), "tools/test_contract_profile.py::PublicationRaceTests.test_revocation_between_read_and_publish_blocks_old_and_new_worker"),
            (("MUST NOT be reused", "restart, restore"), "tools/test_contract_profile.py::PublicationRaceTests.test_rollback_uses_new_generation_and_cannot_create_aba"),
            (("new_epoch` MUST", "revoked` events MUST"), "tools/test_contract_profile.py::ExchangeTests.test_change_event_monotonicity_and_revocation"),
        ],
        "STA": [
            (("single strict UTF-8",), "tools/test_contract_profile.py::ExchangeTests.test_duplicate_members_nonfinite_bom_and_isolated_surrogates_are_rejected"),
            (("Identity comparisons MUST include",), "tools/test_contract_profile.py::ExchangeTests.test_record_hash_is_exact_bytes_not_implicit_canonical_value"),
        ],
        "API": [
            (("gate record conforming",), "tools/test_index_release_receipt.py::IndexReceiptSchemaTests.test_all_2187_check_state_and_decision_combinations"),
            (("Receipt validation MUST reject omitted checks",), "tools/test_index_release_receipt.py::IndexReceiptSchemaTests.test_each_required_check_cannot_be_omitted"),
        ],
    }
    for needles, reference in references.get(prefix, []):
        if any(needle in text for needle in needles):
            matches.append(reference)
    return matches


def collect(root: Path):
    rows, problems, seen = [], [], set()
    for path, prefix in targets(root):
        section, in_fence = "", False
        for chunk in path.read_text().strip().split("\n\n"):
            if chunk.lstrip().startswith("```") or in_fence:
                if sum(1 for line in chunk.splitlines() if line.startswith("```")) % 2:
                    in_fence = not in_fence
                continue
            if chunk.startswith("##"):
                section = chunk.lstrip("# ").splitlines()[0]
            match = ID.match(chunk)
            if NORMATIVE.search(chunk) and match is None:
                problems.append(f"{path.relative_to(root)}: unnumbered normative paragraph in {section}")
            if match is None:
                continue
            rid = match[1]
            if rid in seen or not rid.startswith(prefix + "-R"):
                problems.append(f"{path.relative_to(root)}: duplicate or wrong-prefix ID {rid}")
            seen.add(rid)
            text = chunk[match.end():].strip()
            if not NORMATIVE.search(text):
                problems.append(f"{rid}: numbered clause has no normative keyword")
            refs = test_references(prefix, text)
            rows.append({"id": rid, "document": str(path.relative_to(root)), "section": section, "text": text,
                         "automated_test_references": refs,
                         "verification_scope": "finite regression examples; not a conformance certificate" if refs else "implementation-specific evidence required"})
    return {"schema": "KCRequirementRegister/v1", "edition": "1.1", "requirements": rows}, problems


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=ROOT)
    parser.add_argument("--assign", action="store_true")
    parser.add_argument("--update", action="store_true")
    parser.add_argument("--specifications-only", action="store_true", help="assign IDs only in specifications while another editor owns the API appendix")
    args = parser.parse_args()
    if args.assign:
        for path, prefix in targets(args.root):
            if not args.specifications_only or prefix != "API":
                assign(path, prefix)
    expected, problems = collect(args.root)
    path = args.root / REGISTER
    if args.update and not problems:
        path.write_text(json.dumps(expected, ensure_ascii=False, indent=2) + "\n")
    elif not problems:
        if not path.exists() or json.loads(path.read_text()) != expected:
            problems.append("requirement register missing or stale; regenerate with --update after review")
    for problem in problems:
        print("REQUIREMENT_REGISTER_FAIL " + problem)
    if not problems:
        print(f"REQUIREMENT_REGISTER_PASS requirements={len(expected['requirements'])}")
    return int(bool(problems))


if __name__ == "__main__":
    raise SystemExit(main())

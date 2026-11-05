#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Build the synthetic DocumentClassification/v1 fixtures: twelve boundary cases of kc-doc-class/1 and the one-defect mutants (every byte invented here).

`python3 tools/document_classification_fixture.py write` regenerates schemas/fixtures/document-classification/; the unit tests rebuild the same bytes
in memory and fail if the committed files drift. The twelve valid files cover the boundary cases of the canon; passing them is a statement about those
cases only, not about the accuracy of any classifier. Each negative variant is a MUTANT of a valid file: one change, one expected refusal code.
"""

from __future__ import annotations

import copy
import hashlib
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_document_classification as cdc  # noqa: E402

FIXTURE_ROOT = cdc.REPO / "schemas" / "fixtures" / "document-classification"


def sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def dump(record: dict) -> bytes:
    return (json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode()


def make(label: str, status: str, cls, candidates: list, reason: str | None, basis: tuple[str, str], coverage: str = "complete", coverage_note: str | None = None) -> dict:
    record = {
        "schema": "DocumentClassification/v1", "document_id": "d_" + sha(f"source:{label}"), "taxonomy_id": cdc.TAXONOMY_ID, "canon_sha256": cdc.canon_digest(),
        "status": status, "class": cls, "candidates": candidates, "coverage": coverage,
        "classifier": {"name": "synthetic-classifier", "version": "0.0.0", "method": "rule-based reading of the representation named in the evidence"},
        "evidence": [{"representation_sha256": sha(f"representation:{label}"), "basis": {"kind": basis[0], "name": basis[1]}}],
        "confidence": {"status": "not_measured", "reason": "no calibrated assessment exists for this classifier"},
    }
    if reason:
        record["reason"] = reason
    if coverage_note:
        record["coverage_note"] = coverage_note
    return record


# The twelve boundary cases: (file name, record).
CASES: list[tuple[str, dict]] = [
    ("01-complete-book-with-evidenced-identity", make("c01", "classified", "book", ["book"], None, ("feature", "title page, imprint and chapter structure"))),
    ("02-same-book-saved-as-pdf-from-a-drive", make("c02", "classified", "book", ["book"], None, ("feature", "title page, imprint and chapter structure"))),
    ("03-chapter-with-verified-parent-book", make("c03", "classified", "book", ["book"], "a chapter whose parent book identity is verified", ("selector", "parent-book citation on the first page"),
                                                  "partial", "one chapter of the parent book")),
    ("04-standalone-preprint-or-long-report", make("c04", "classified", "paper", ["paper"], None, ("feature", "abstract, numbered sections and reference list"))),
    ("05-journal-issue-of-several-independent-papers", make("c05", "classified", "other", ["other"], "a complete journal issue of independent papers, no separate book identity",
                                                            ("feature", "issue contents list"))),
    ("06-contextual-chat-or-email-archive", make("c06", "classified", "export", ["export"], None, ("feature", "message records with participants, order and timestamps"))),
    ("07-labelled-dialogue-corpus-with-dataset-manifest", make("c07", "classified", "dataset", ["dataset"], None, ("selector", "dataset manifest and per-record labels"))),
    ("08-database-csv-with-described-columns", make("c08", "classified", "dataset", ["dataset"], None, ("rule", "header row with a column description file"))),
    ("09-paper-containing-tables-and-appendices", make("c09", "classified", "paper", ["paper"], "tables and measurement appendices belong to the paper", ("feature", "paper structure"))),
    ("10-recognised-invoice-or-slide-deck", make("c10", "classified", "other", ["other"], "a recognised invoice", ("feature", "invoice header and line items"))),
    ("11-unreadable-scan-without-metadata", make("c11", "unknown", None, [], "the scan is unreadable and carries no metadata", ("feature", "no recognisable text layer"), "not_measured")),
    ("12-unresolved-book-versus-report-evidence", make("c12", "ambiguous", None, ["book", "paper"], "the evidence supports both a book and a long report",
                                                       ("feature", "front matter without an imprint"), "not_measured")),
]


def variants() -> dict[str, bytes]:
    files: dict[str, bytes] = {f"valid/{name}": dump(record) for name, record in CASES}
    book = copy.deepcopy(CASES[0][1])
    ambiguous = copy.deepcopy(CASES[11][1])
    unknown = copy.deepcopy(CASES[10][1])

    def mutant(name: str, base: dict, edit) -> None:
        record = copy.deepcopy(base)
        edit(record)
        files[f"invalid/{name}"] = dump(record)

    mutant("classified_without_a_class", book, lambda r: r.update({"class": None}))
    mutant("classified_candidates_do_not_equal_the_class", book, lambda r: r.update({"candidates": ["paper"]}))
    mutant("classified_with_two_candidates", book, lambda r: r.update({"candidates": ["book", "paper"]}))
    mutant("classified_with_no_candidate", book, lambda r: r.update({"candidates": []}))
    mutant("ambiguous_with_a_class", ambiguous, lambda r: r.update({"class": "book"}))
    mutant("ambiguous_with_one_candidate", ambiguous, lambda r: r.update({"candidates": ["book"]}))
    mutant("ambiguous_with_duplicate_candidates", ambiguous, lambda r: r.update({"candidates": ["book", "book"]}))
    mutant("ambiguous_without_a_reason", ambiguous, lambda r: r.pop("reason"))
    mutant("ambiguous_with_other_as_a_candidate", ambiguous, lambda r: r.update({"candidates": ["book", "other"]}))
    mutant("unknown_with_a_class", unknown, lambda r: r.update({"class": "book"}))
    mutant("unknown_with_candidates", unknown, lambda r: r.update({"candidates": ["book"]}))
    mutant("unknown_without_a_reason", unknown, lambda r: r.pop("reason"))
    mutant("other_hiding_an_ambiguity", ambiguous, lambda r: r.update({"status": "classified", "class": "other"}))
    mutant("other_hiding_an_unknown", unknown, lambda r: r.update({"class": "other"}))
    mutant("class_outside_the_taxonomy", book, lambda r: r.update({"class": "invoice", "candidates": ["invoice"]}))
    mutant("not_measured_confidence_with_a_score", book, lambda r: r["confidence"].update({"score": 0.97}))
    mutant("measured_confidence_without_a_method", book, lambda r: r.update({"confidence": {"status": "measured", "score": 0.9, "version": "1", "interpretation": "share of agreeing rules"}}))
    mutant("no_evidence", book, lambda r: r.update({"evidence": []}))
    mutant("evidence_digest_not_hex", book, lambda r: r["evidence"][0].update({"representation_sha256": "abc"}))
    mutant("evidence_without_a_basis", book, lambda r: r["evidence"][0].pop("basis"))
    mutant("coverage_missing", book, lambda r: r.pop("coverage"))
    mutant("document_id_not_a_digest", book, lambda r: r.update({"document_id": "d_book"}))
    mutant("unknown_field", book, lambda r: r.update({"rights_class": "author_open"}))
    mutant("taxonomy_digest_wrong", book, lambda r: r.update({"canon_sha256": "0" * 64}))
    mutant("taxonomy_is_the_proposal_label", book, lambda r: r.update({"taxonomy_id": "kc-doc-class/0"}))
    mutant("taxonomy_is_a_later_label", book, lambda r: r.update({"taxonomy_id": "kc-doc-class/2"}))
    files["invalid/duplicate_member"] = files["valid/01-complete-book-with-evidenced-identity"].replace(b'"status": "classified"', b'"status": "classified",\n  "status": "classified"', 1)
    files["invalid/not_json"] = b"not json\n"
    return files


EXPECTED = {
    **{f"valid/{name}": None for name, _ in CASES},
    "invalid/classified_without_a_class": "DCL-SCHEMA", "invalid/classified_candidates_do_not_equal_the_class": "DCL-SCHEMA",
    "invalid/classified_with_two_candidates": "DCL-SCHEMA", "invalid/classified_with_no_candidate": "DCL-SCHEMA", "invalid/ambiguous_with_a_class": "DCL-SCHEMA",
    "invalid/ambiguous_with_one_candidate": "DCL-SCHEMA", "invalid/ambiguous_with_duplicate_candidates": "DCL-SCHEMA", "invalid/ambiguous_without_a_reason": "DCL-SCHEMA",
    "invalid/ambiguous_with_other_as_a_candidate": "DCL-SCHEMA", "invalid/unknown_with_a_class": "DCL-SCHEMA", "invalid/unknown_with_candidates": "DCL-SCHEMA",
    "invalid/unknown_without_a_reason": "DCL-SCHEMA", "invalid/other_hiding_an_ambiguity": "DCL-SCHEMA", "invalid/other_hiding_an_unknown": "DCL-SCHEMA", "invalid/class_outside_the_taxonomy": "DCL-SCHEMA",
    "invalid/not_measured_confidence_with_a_score": "DCL-SCHEMA", "invalid/measured_confidence_without_a_method": "DCL-SCHEMA", "invalid/no_evidence": "DCL-SCHEMA",
    "invalid/evidence_digest_not_hex": "DCL-SCHEMA", "invalid/evidence_without_a_basis": "DCL-SCHEMA", "invalid/coverage_missing": "DCL-SCHEMA",
    "invalid/document_id_not_a_digest": "DCL-SCHEMA", "invalid/unknown_field": "DCL-SCHEMA", "invalid/taxonomy_digest_wrong": "DCL-CANON",
    "invalid/taxonomy_is_the_proposal_label": "DCL-TAXONOMY", "invalid/taxonomy_is_a_later_label": "DCL-TAXONOMY", "invalid/duplicate_member": "DCL-READ",
    "invalid/not_json": "DCL-READ",
}


def write() -> None:
    if FIXTURE_ROOT.exists():
        shutil.rmtree(FIXTURE_ROOT)
    for name, data in variants().items():
        target = FIXTURE_ROOT / f"{name}.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    (FIXTURE_ROOT / "README.md").write_text(
        "# Synthetic document classification results\n\nEvery file here is invented for this repository. `valid/` holds twelve results, one for each boundary case of the "
        "`kc-doc-class/1` canon (`engineering/specifications/pipeline/document-classes.json`); passing them is a statement about those cases only, not about the accuracy "
        "of any classifier. Each file under `invalid/` is a mutant of a valid one with one defect and one expected refusal code (see `EXPECTED` in "
        "`tools/document_classification_fixture.py`). Regenerate with\n`python3 tools/document_classification_fixture.py write`; the unit tests fail if the committed files drift, "
        "and they also fail if the canon file changes without the fixtures being regenerated (every file carries the digest of the canon).\n", encoding="utf-8")


if __name__ == "__main__":
    if sys.argv[1:] == ["write"]:
        write()
    else:
        print("usage: document_classification_fixture.py write", file=sys.stderr)
        raise SystemExit(2)

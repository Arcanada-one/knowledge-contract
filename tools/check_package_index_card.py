#!/usr/bin/env python3
"""Validate PackageIndexCard/v1 and PackageIngestReceipt/v1 JSON (repo-only)."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SOURCE_ID = re.compile(r"^d_[0-9a-f]{64}$")
PACKAGE_ID = re.compile(r"^d_[0-9a-f]{64}/[A-Za-z0-9][A-Za-z0-9._@+-]{0,119}$")
SLUG = re.compile(r"^[a-z0-9][a-z0-9-]{2,95}$")
EXPORTER = re.compile(r"^pkg-[a-f0-9]{12}-[a-f0-9]{8}$")
SOURCE_PATH = re.compile(
    r"^articles/book-packages/pkg-[a-f0-9]{12}-[a-f0-9]{8}/(document|readable|knowledge)\.md$"
)
SHA = re.compile(r"^[0-9a-f]{64}$")
PUB = frozenset({"public_domain", "author_open", "third_party_restricted", "unknown"})
LAYERS = frozenset({"document", "readable", "knowledge"})


def refuse(code: str, detail: str) -> None:
    raise SystemExit(f"{code}: {detail}")


def check_card(card: dict) -> None:
    if card.get("schema") != "PackageIndexCard/v1":
        refuse("IDX-SCHEMA", "schema must be PackageIndexCard/v1")
    if not SOURCE_ID.match(card.get("source_id", "")):
        refuse("IDX-SOURCE", "source_id must be d_<sha256>")
    if not PACKAGE_ID.match(card.get("package_id", "")):
        refuse("IDX-PACKAGE", "package_id must be d_<sha256>/<pipeline-version>")
    if not card["package_id"].startswith(card["source_id"] + "/"):
        refuse("IDX-PACKAGE", "package_id must start with source_id/")
    if not SLUG.match(card.get("package_slug", "")):
        refuse("IDX-SLUG", "package_slug invalid")
    if not EXPORTER.match(card.get("exporter_path_slug", "")):
        refuse("IDX-EXPORTER", "exporter_path_slug invalid")
    span = card.get("span")
    if not isinstance(span, dict) or "kind" not in span:
        refuse("IDX-SPAN", "span.kind required")
    if card.get("publication_state") not in PUB:
        refuse("IDX-PUB", "publication_state invalid")
    if card.get("layer") not in LAYERS:
        refuse("IDX-LAYER", "layer invalid")
    if not SOURCE_PATH.match(card.get("source_path", "")):
        refuse("IDX-PATH", "source_path must match X6 book-package grammar")
    if not SHA.match(card.get("content_sha256", "")):
        refuse("IDX-HASH", "content_sha256 must be sha256 hex")
    if not isinstance(card.get("damage_places"), int) or card["damage_places"] < 0:
        refuse("IDX-DAMAGE", "damage_places must be int >= 0")
    if card.get("kc2_admission") != "not_measured":
        refuse("IDX-ADMISSION", "kc2_admission must be not_measured")
    if card["damage_places"] > 0 and card.get("damage_status") == "clean":
        refuse("IDX-DAMAGE", "damaged_presented_as_clean")
    if card["damage_places"] > 0 and card.get("knowledge_ready") is True:
        refuse("IDX-DAMAGE", "damaged_presented_as_knowledge_ready")
    licence = card.get("licence")
    if not isinstance(licence, str) or not licence.strip():
        refuse("IDX-LICENCE", "licence required")


def check_receipt(doc: dict) -> None:
    if doc.get("schema") != "PackageIngestReceipt/v1":
        refuse("IDX-SCHEMA", "schema must be PackageIngestReceipt/v1")
    if doc.get("kc2_admission") != "not_measured":
        refuse("IDX-ADMISSION", "kc2_admission must be not_measured")
    counts = doc.get("counts")
    required = {
        "packages_seen",
        "cards_staged",
        "skipped_unchanged",
        "refused",
        "tombstoned",
        "edges_planned",
        "not_measured",
    }
    if not isinstance(counts, dict) or set(counts) < required:
        refuse("IDX-COUNTS", "counts missing required keys")
    for card in doc.get("cards") or []:
        check_card(card)
    for key in ("live_search", "live_s3_resolve", "live_edges_query"):
        val = doc.get(key, "not_measured")
        if val not in ("not_measured", "measured"):
            refuse("IDX-LIVE", f"{key} must be not_measured or measured")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path", type=Path)
    args = ap.parse_args()
    raw = args.path.read_text(encoding="utf-8")
    doc = json.loads(raw)
    schema = doc.get("schema")
    if schema == "PackageIndexCard/v1":
        check_card(doc)
    elif schema == "PackageIngestReceipt/v1":
        check_receipt(doc)
    else:
        refuse("IDX-SCHEMA", f"unknown schema {schema!r}")
    print("ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())

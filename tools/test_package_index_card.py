"""Finite checks for PackageIndexCard/v1 validator."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools" / "check_package_index_card.py"


def run_checker(doc: dict) -> subprocess.CompletedProcess[str]:
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
        json.dump(doc, fh)
        path = fh.name
    return subprocess.run(
        [sys.executable, str(CHECKER), path],
        capture_output=True,
        text=True,
        check=False,
    )


# Frozen source-derived fixture bytes; expected results from owner report, not CI.
FROZEN_S4_CASES_JSON = r'''[
  {
    "name": "strict-control",
    "digest": "1c87bcf28e3d04b2b8f8f13f5da0dc505079d400fbc58af41b828fd5c899ee87",
    "code": "PASS",
    "exit": 0,
    "wire": "{\"cards\":[],\"counts\":{\"cards_staged\":0,\"edges_planned\":0,\"not_measured\":0,\"packages_seen\":0,\"refused\":0,\"skipped_unchanged\":0,\"tombstoned\":0},\"dry_run\":true,\"edges\":[],\"finished_at\":\"2026-11-24T08:56:20Z\",\"kc2_admission\":\"not_measured\",\"live_edges_query\":\"not_measured\",\"live_s3_resolve\":\"not_measured\",\"live_search\":\"not_measured\",\"run_id\":\"synthetic-c303\",\"schema\":\"PackageIngestReceipt/v1\",\"started_at\":\"2026-11-24T08:56:20Z\",\"tool\":{\"name\":\"fixture\",\"version\":\"1\"}}\n"
  },
  {
    "name": "count-substitution",
    "digest": "e5b45f0ffb21323d4e6bd5b44664917576f1073aa32bb79fbc8783b66c156e72",
    "code": "IDX-STRUCTURE",
    "exit": 1,
    "wire": "{\"cards\":[],\"counts\":{\"cards_staged\":0,\"edges_planned\":0,\"not_measured\":0,\"refused\":0,\"skipped_unchanged\":0,\"tombstoned\":0,\"unexpected\":0},\"dry_run\":true,\"edges\":[],\"finished_at\":\"2026-11-24T08:56:20Z\",\"kc2_admission\":\"not_measured\",\"live_edges_query\":\"not_measured\",\"live_s3_resolve\":\"not_measured\",\"live_search\":\"not_measured\",\"run_id\":\"synthetic-c303\",\"schema\":\"PackageIngestReceipt/v1\",\"started_at\":\"2026-11-24T08:56:20Z\",\"tool\":{\"name\":\"fixture\",\"version\":\"1\"}}\n"
  },
  {
    "name": "count-boolean",
    "digest": "e85f754d0eb2ba795e2f6d571012aafddf01e780dbea6f8b3eaba71b11284fbe",
    "code": "IDX-STRUCTURE",
    "exit": 1,
    "wire": "{\"cards\":[],\"counts\":{\"cards_staged\":0,\"edges_planned\":0,\"not_measured\":0,\"packages_seen\":false,\"refused\":0,\"skipped_unchanged\":0,\"tombstoned\":0},\"dry_run\":true,\"edges\":[],\"finished_at\":\"2026-11-24T08:56:20Z\",\"kc2_admission\":\"not_measured\",\"live_edges_query\":\"not_measured\",\"live_s3_resolve\":\"not_measured\",\"live_search\":\"not_measured\",\"run_id\":\"synthetic-c303\",\"schema\":\"PackageIngestReceipt/v1\",\"started_at\":\"2026-11-24T08:56:20Z\",\"tool\":{\"name\":\"fixture\",\"version\":\"1\"}}\n"
  },
  {
    "name": "count-negative",
    "digest": "cb55f0039caf0dcf0137d1a894e1ae7bbdabf944d9caf39760c6b2e9d6d800a8",
    "code": "IDX-STRUCTURE",
    "exit": 1,
    "wire": "{\"cards\":[],\"counts\":{\"cards_staged\":0,\"edges_planned\":0,\"not_measured\":0,\"packages_seen\":-1,\"refused\":0,\"skipped_unchanged\":0,\"tombstoned\":0},\"dry_run\":true,\"edges\":[],\"finished_at\":\"2026-11-24T08:56:20Z\",\"kc2_admission\":\"not_measured\",\"live_edges_query\":\"not_measured\",\"live_s3_resolve\":\"not_measured\",\"live_search\":\"not_measured\",\"run_id\":\"synthetic-c303\",\"schema\":\"PackageIngestReceipt/v1\",\"started_at\":\"2026-11-24T08:56:20Z\",\"tool\":{\"name\":\"fixture\",\"version\":\"1\"}}\n"
  },
  {
    "name": "count-string",
    "digest": "b6513b6105c6ef6401b7fc1ed92d544e47d56ba669dd4188f54a15b21c0a9c60",
    "code": "IDX-STRUCTURE",
    "exit": 1,
    "wire": "{\"cards\":[],\"counts\":{\"cards_staged\":0,\"edges_planned\":0,\"not_measured\":0,\"packages_seen\":\"0\",\"refused\":0,\"skipped_unchanged\":0,\"tombstoned\":0},\"dry_run\":true,\"edges\":[],\"finished_at\":\"2026-11-24T08:56:20Z\",\"kc2_admission\":\"not_measured\",\"live_edges_query\":\"not_measured\",\"live_s3_resolve\":\"not_measured\",\"live_search\":\"not_measured\",\"run_id\":\"synthetic-c303\",\"schema\":\"PackageIngestReceipt/v1\",\"started_at\":\"2026-11-24T08:56:20Z\",\"tool\":{\"name\":\"fixture\",\"version\":\"1\"}}\n"
  },
  {
    "name": "missing-dry-run",
    "digest": "a2b7d04d3ce1d9214c1d1cef3f00c63969ad8d62135913501fba25650accf499",
    "code": "IDX-STRUCTURE",
    "exit": 1,
    "wire": "{\"cards\":[],\"counts\":{\"cards_staged\":0,\"edges_planned\":0,\"not_measured\":0,\"packages_seen\":0,\"refused\":0,\"skipped_unchanged\":0,\"tombstoned\":0},\"edges\":[],\"finished_at\":\"2026-11-24T08:56:20Z\",\"kc2_admission\":\"not_measured\",\"live_edges_query\":\"not_measured\",\"live_s3_resolve\":\"not_measured\",\"live_search\":\"not_measured\",\"run_id\":\"synthetic-c303\",\"schema\":\"PackageIngestReceipt/v1\",\"started_at\":\"2026-11-24T08:56:20Z\",\"tool\":{\"name\":\"fixture\",\"version\":\"1\"}}\n"
  },
  {
    "name": "null-cards",
    "digest": "c036098468fe598576b6d29dc0fff7e819bc711fbd033c84ef61d51ea87ebf26",
    "code": "IDX-STRUCTURE",
    "exit": 1,
    "wire": "{\"cards\":null,\"counts\":{\"cards_staged\":0,\"edges_planned\":0,\"not_measured\":0,\"packages_seen\":0,\"refused\":0,\"skipped_unchanged\":0,\"tombstoned\":0},\"dry_run\":true,\"edges\":[],\"finished_at\":\"2026-11-24T08:56:20Z\",\"kc2_admission\":\"not_measured\",\"live_edges_query\":\"not_measured\",\"live_s3_resolve\":\"not_measured\",\"live_search\":\"not_measured\",\"run_id\":\"synthetic-c303\",\"schema\":\"PackageIngestReceipt/v1\",\"started_at\":\"2026-11-24T08:56:20Z\",\"tool\":{\"name\":\"fixture\",\"version\":\"1\"}}\n"
  },
  {
    "name": "malformed-edge",
    "digest": "619fe29863798f10b63243e527a15195ab9a3d0fde69e1d34d426b416e8a845c",
    "code": "IDX-STRUCTURE",
    "exit": 1,
    "wire": "{\"cards\":[],\"counts\":{\"cards_staged\":0,\"edges_planned\":0,\"not_measured\":0,\"packages_seen\":0,\"refused\":0,\"skipped_unchanged\":0,\"tombstoned\":0},\"dry_run\":true,\"edges\":[{\"edge_type\":\"relation\",\"source_path\":\"x\",\"target_path\":\"x\"}],\"finished_at\":\"2026-11-24T08:56:20Z\",\"kc2_admission\":\"not_measured\",\"live_edges_query\":\"not_measured\",\"live_s3_resolve\":\"not_measured\",\"live_search\":\"not_measured\",\"run_id\":\"synthetic-c303\",\"schema\":\"PackageIngestReceipt/v1\",\"started_at\":\"2026-11-24T08:56:20Z\",\"tool\":{\"name\":\"fixture\",\"version\":\"1\"}}\n"
  },
  {
    "name": "tool-extra-key",
    "digest": "c6bb3a5d824316ec84ab99153cbcbeb7e9e6255f60ef1a3e9be3169ad30d3160",
    "code": "IDX-STRUCTURE",
    "exit": 1,
    "wire": "{\"cards\":[],\"counts\":{\"cards_staged\":0,\"edges_planned\":0,\"not_measured\":0,\"packages_seen\":0,\"refused\":0,\"skipped_unchanged\":0,\"tombstoned\":0},\"dry_run\":true,\"edges\":[],\"finished_at\":\"2026-11-24T08:56:20Z\",\"kc2_admission\":\"not_measured\",\"live_edges_query\":\"not_measured\",\"live_s3_resolve\":\"not_measured\",\"live_search\":\"not_measured\",\"run_id\":\"synthetic-c303\",\"schema\":\"PackageIngestReceipt/v1\",\"started_at\":\"2026-11-24T08:56:20Z\",\"tool\":{\"name\":\"fixture\",\"unexpected\":\"x\",\"version\":\"1\"}}\n"
  },
  {
    "name": "producer-extra-negatives",
    "digest": "cbd35573eab266cd80625eb63f10d5a29ee0828c95514131656789627f30e02b",
    "code": "IDX-STRUCTURE",
    "exit": 1,
    "wire": "{\"cards\":[],\"counts\":{\"cards_staged\":0,\"edges_planned\":0,\"not_measured\":0,\"packages_seen\":0,\"refused\":0,\"skipped_unchanged\":0,\"tombstoned\":0},\"dry_run\":true,\"edges\":[],\"finished_at\":\"2026-11-24T08:56:20Z\",\"kc2_admission\":\"not_measured\",\"knowledge_admitted\":false,\"live_edges_query\":\"not_measured\",\"live_s3_resolve\":\"not_measured\",\"live_search\":\"not_measured\",\"run_id\":\"synthetic-c303\",\"runtime_authorized\":false,\"schema\":\"PackageIngestReceipt/v1\",\"started_at\":\"2026-11-24T08:56:20Z\",\"tool\":{\"name\":\"fixture\",\"version\":\"1\"}}\n"
  },
  {
    "name": "missing-count-only",
    "digest": "f32a234e473c60e33bec7fe2ef97939dca0e37964b388d549f6793d802366c82",
    "code": "IDX-STRUCTURE",
    "exit": 1,
    "wire": "{\"cards\":[],\"counts\":{\"cards_staged\":0,\"edges_planned\":0,\"not_measured\":0,\"refused\":0,\"skipped_unchanged\":0,\"tombstoned\":0},\"dry_run\":true,\"edges\":[],\"finished_at\":\"2026-11-24T08:56:20Z\",\"kc2_admission\":\"not_measured\",\"live_edges_query\":\"not_measured\",\"live_s3_resolve\":\"not_measured\",\"live_search\":\"not_measured\",\"run_id\":\"synthetic-c303\",\"schema\":\"PackageIngestReceipt/v1\",\"started_at\":\"2026-11-24T08:56:20Z\",\"tool\":{\"name\":\"fixture\",\"version\":\"1\"}}\n"
  },
  {
    "name": "direct-valid",
    "digest": "f116500f72619139438452b14a1ebdc8dd3864634b0b148becedc0e1b7a41ccd",
    "code": "PASS",
    "exit": 0,
    "wire": "{\"content_sha256\":\"cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc\",\"damage_places\":0,\"damage_status\":\"clean\",\"exporter_path_slug\":\"pkg-aaaaaaaaaaaa-bbbbbbbb\",\"kc2_admission\":\"not_measured\",\"knowledge_ready\":false,\"layer\":\"readable\",\"licence\":\"public_domain\",\"package_id\":\"d_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/book-package-2@r1\",\"package_slug\":\"pilot-s4-index-book\",\"publication_state\":\"public_domain\",\"schema\":\"PackageIndexCard/v1\",\"source_id\":\"d_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\",\"source_path\":\"articles/book-packages/pkg-aaaaaaaaaaaa-bbbbbbbb/readable.md\",\"span\":{\"kind\":\"full_document\"}}\n"
  },
  {
    "name": "nested-valid",
    "digest": "06d156a036e081a30238a9b3ade95bce0670082f9eb1f07514bd6cfb122b1ef5",
    "code": "PASS",
    "exit": 0,
    "wire": "{\"cards\":[{\"content_sha256\":\"cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc\",\"damage_places\":0,\"damage_status\":\"clean\",\"exporter_path_slug\":\"pkg-aaaaaaaaaaaa-bbbbbbbb\",\"kc2_admission\":\"not_measured\",\"knowledge_ready\":false,\"layer\":\"readable\",\"licence\":\"public_domain\",\"package_id\":\"d_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/book-package-2@r1\",\"package_slug\":\"pilot-s4-index-book\",\"publication_state\":\"public_domain\",\"schema\":\"PackageIndexCard/v1\",\"source_id\":\"d_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\",\"source_path\":\"articles/book-packages/pkg-aaaaaaaaaaaa-bbbbbbbb/readable.md\",\"span\":{\"kind\":\"full_document\"}}],\"counts\":{\"cards_staged\":0,\"edges_planned\":0,\"not_measured\":0,\"packages_seen\":0,\"refused\":0,\"skipped_unchanged\":0,\"tombstoned\":0},\"dry_run\":true,\"edges\":[],\"finished_at\":\"2026-11-24T08:56:20Z\",\"kc2_admission\":\"not_measured\",\"live_edges_query\":\"not_measured\",\"live_s3_resolve\":\"not_measured\",\"live_search\":\"not_measured\",\"run_id\":\"synthetic-c303\",\"schema\":\"PackageIngestReceipt/v1\",\"started_at\":\"2026-11-24T08:56:20Z\",\"tool\":{\"name\":\"fixture\",\"version\":\"1\"}}\n"
  },
  {
    "name": "direct-source-package-mismatch",
    "digest": "1bec165f1d9fd9034e66e37007fd9edf60260b3b7f3661cb9db7fb0a3ccc594c",
    "code": "IDX-PACKAGE",
    "exit": 1,
    "wire": "{\"content_sha256\":\"cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc\",\"damage_places\":0,\"damage_status\":\"clean\",\"exporter_path_slug\":\"pkg-aaaaaaaaaaaa-bbbbbbbb\",\"kc2_admission\":\"not_measured\",\"knowledge_ready\":false,\"layer\":\"readable\",\"licence\":\"public_domain\",\"package_id\":\"d_bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb/book-package-2@r1\",\"package_slug\":\"pilot-s4-index-book\",\"publication_state\":\"public_domain\",\"schema\":\"PackageIndexCard/v1\",\"source_id\":\"d_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\",\"source_path\":\"articles/book-packages/pkg-aaaaaaaaaaaa-bbbbbbbb/readable.md\",\"span\":{\"kind\":\"full_document\"}}\n"
  },
  {
    "name": "nested-source-package-mismatch",
    "digest": "79b3a693d6ec3833cffb6410ea93aa4be7daaa1f803f5bc8c4adca763610a166",
    "code": "IDX-PACKAGE",
    "exit": 1,
    "wire": "{\"cards\":[{\"content_sha256\":\"cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc\",\"damage_places\":0,\"damage_status\":\"clean\",\"exporter_path_slug\":\"pkg-aaaaaaaaaaaa-bbbbbbbb\",\"kc2_admission\":\"not_measured\",\"knowledge_ready\":false,\"layer\":\"readable\",\"licence\":\"public_domain\",\"package_id\":\"d_bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb/book-package-2@r1\",\"package_slug\":\"pilot-s4-index-book\",\"publication_state\":\"public_domain\",\"schema\":\"PackageIndexCard/v1\",\"source_id\":\"d_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\",\"source_path\":\"articles/book-packages/pkg-aaaaaaaaaaaa-bbbbbbbb/readable.md\",\"span\":{\"kind\":\"full_document\"}}],\"counts\":{\"cards_staged\":0,\"edges_planned\":0,\"not_measured\":0,\"packages_seen\":0,\"refused\":0,\"skipped_unchanged\":0,\"tombstoned\":0},\"dry_run\":true,\"edges\":[],\"finished_at\":\"2026-11-24T08:56:20Z\",\"kc2_admission\":\"not_measured\",\"live_edges_query\":\"not_measured\",\"live_s3_resolve\":\"not_measured\",\"live_search\":\"not_measured\",\"run_id\":\"synthetic-c303\",\"schema\":\"PackageIngestReceipt/v1\",\"started_at\":\"2026-11-24T08:56:20Z\",\"tool\":{\"name\":\"fixture\",\"version\":\"1\"}}\n"
  },
  {
    "name": "direct-damaged-clean",
    "digest": "11bb28fd384ba3467ac39f02f45decf0886e2ac61e66713c092cf86bfe62e80e",
    "code": "IDX-DAMAGE",
    "exit": 1,
    "wire": "{\"content_sha256\":\"cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc\",\"damage_places\":1,\"damage_status\":\"clean\",\"exporter_path_slug\":\"pkg-aaaaaaaaaaaa-bbbbbbbb\",\"kc2_admission\":\"not_measured\",\"knowledge_ready\":false,\"layer\":\"readable\",\"licence\":\"public_domain\",\"package_id\":\"d_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/book-package-2@r1\",\"package_slug\":\"pilot-s4-index-book\",\"publication_state\":\"public_domain\",\"schema\":\"PackageIndexCard/v1\",\"source_id\":\"d_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\",\"source_path\":\"articles/book-packages/pkg-aaaaaaaaaaaa-bbbbbbbb/readable.md\",\"span\":{\"kind\":\"full_document\"}}\n"
  },
  {
    "name": "nested-damaged-clean",
    "digest": "7c6a9dbd4742d50aad738f9ca89cea3751bbd8b1ee72bc61b22667e619b31aae",
    "code": "IDX-DAMAGE",
    "exit": 1,
    "wire": "{\"cards\":[{\"content_sha256\":\"cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc\",\"damage_places\":1,\"damage_status\":\"clean\",\"exporter_path_slug\":\"pkg-aaaaaaaaaaaa-bbbbbbbb\",\"kc2_admission\":\"not_measured\",\"knowledge_ready\":false,\"layer\":\"readable\",\"licence\":\"public_domain\",\"package_id\":\"d_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/book-package-2@r1\",\"package_slug\":\"pilot-s4-index-book\",\"publication_state\":\"public_domain\",\"schema\":\"PackageIndexCard/v1\",\"source_id\":\"d_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\",\"source_path\":\"articles/book-packages/pkg-aaaaaaaaaaaa-bbbbbbbb/readable.md\",\"span\":{\"kind\":\"full_document\"}}],\"counts\":{\"cards_staged\":0,\"edges_planned\":0,\"not_measured\":0,\"packages_seen\":0,\"refused\":0,\"skipped_unchanged\":0,\"tombstoned\":0},\"dry_run\":true,\"edges\":[],\"finished_at\":\"2026-11-24T08:56:20Z\",\"kc2_admission\":\"not_measured\",\"live_edges_query\":\"not_measured\",\"live_s3_resolve\":\"not_measured\",\"live_search\":\"not_measured\",\"run_id\":\"synthetic-c303\",\"schema\":\"PackageIngestReceipt/v1\",\"started_at\":\"2026-11-24T08:56:20Z\",\"tool\":{\"name\":\"fixture\",\"version\":\"1\"}}\n"
  },
  {
    "name": "direct-damaged-ready",
    "digest": "967b67b8871469f9da94f948adf3710bb003aad8406450665f556e16755ace21",
    "code": "IDX-DAMAGE",
    "exit": 1,
    "wire": "{\"content_sha256\":\"cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc\",\"damage_places\":1,\"damage_status\":\"damaged\",\"exporter_path_slug\":\"pkg-aaaaaaaaaaaa-bbbbbbbb\",\"kc2_admission\":\"not_measured\",\"knowledge_ready\":true,\"layer\":\"readable\",\"licence\":\"public_domain\",\"package_id\":\"d_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/book-package-2@r1\",\"package_slug\":\"pilot-s4-index-book\",\"publication_state\":\"public_domain\",\"schema\":\"PackageIndexCard/v1\",\"source_id\":\"d_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\",\"source_path\":\"articles/book-packages/pkg-aaaaaaaaaaaa-bbbbbbbb/readable.md\",\"span\":{\"kind\":\"full_document\"}}\n"
  },
  {
    "name": "nested-damaged-ready",
    "digest": "4795c42c9d7a0c9981eafc4686ad1ecd25d6948ea56c4f58369973083c759874",
    "code": "IDX-DAMAGE",
    "exit": 1,
    "wire": "{\"cards\":[{\"content_sha256\":\"cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc\",\"damage_places\":1,\"damage_status\":\"damaged\",\"exporter_path_slug\":\"pkg-aaaaaaaaaaaa-bbbbbbbb\",\"kc2_admission\":\"not_measured\",\"knowledge_ready\":true,\"layer\":\"readable\",\"licence\":\"public_domain\",\"package_id\":\"d_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/book-package-2@r1\",\"package_slug\":\"pilot-s4-index-book\",\"publication_state\":\"public_domain\",\"schema\":\"PackageIndexCard/v1\",\"source_id\":\"d_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\",\"source_path\":\"articles/book-packages/pkg-aaaaaaaaaaaa-bbbbbbbb/readable.md\",\"span\":{\"kind\":\"full_document\"}}],\"counts\":{\"cards_staged\":0,\"edges_planned\":0,\"not_measured\":0,\"packages_seen\":0,\"refused\":0,\"skipped_unchanged\":0,\"tombstoned\":0},\"dry_run\":true,\"edges\":[],\"finished_at\":\"2026-11-24T08:56:20Z\",\"kc2_admission\":\"not_measured\",\"live_edges_query\":\"not_measured\",\"live_s3_resolve\":\"not_measured\",\"live_search\":\"not_measured\",\"run_id\":\"synthetic-c303\",\"schema\":\"PackageIngestReceipt/v1\",\"started_at\":\"2026-11-24T08:56:20Z\",\"tool\":{\"name\":\"fixture\",\"version\":\"1\"}}\n"
  },
  {
    "name": "direct-blank-licence",
    "digest": "f0b803794d0a9ce5be30d8b4bc20749ce0b071dd912bb65f84f1950b6a8e231b",
    "code": "IDX-LICENCE",
    "exit": 1,
    "wire": "{\"content_sha256\":\"cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc\",\"damage_places\":0,\"damage_status\":\"clean\",\"exporter_path_slug\":\"pkg-aaaaaaaaaaaa-bbbbbbbb\",\"kc2_admission\":\"not_measured\",\"knowledge_ready\":false,\"layer\":\"readable\",\"licence\":\"   \",\"package_id\":\"d_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/book-package-2@r1\",\"package_slug\":\"pilot-s4-index-book\",\"publication_state\":\"public_domain\",\"schema\":\"PackageIndexCard/v1\",\"source_id\":\"d_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\",\"source_path\":\"articles/book-packages/pkg-aaaaaaaaaaaa-bbbbbbbb/readable.md\",\"span\":{\"kind\":\"full_document\"}}\n"
  },
  {
    "name": "nested-blank-licence",
    "digest": "70e32542e1f9a04879b941b7264efb1689e29f7d4959816a6bb251ce51b68ff9",
    "code": "IDX-LICENCE",
    "exit": 1,
    "wire": "{\"cards\":[{\"content_sha256\":\"cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc\",\"damage_places\":0,\"damage_status\":\"clean\",\"exporter_path_slug\":\"pkg-aaaaaaaaaaaa-bbbbbbbb\",\"kc2_admission\":\"not_measured\",\"knowledge_ready\":false,\"layer\":\"readable\",\"licence\":\"   \",\"package_id\":\"d_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/book-package-2@r1\",\"package_slug\":\"pilot-s4-index-book\",\"publication_state\":\"public_domain\",\"schema\":\"PackageIndexCard/v1\",\"source_id\":\"d_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\",\"source_path\":\"articles/book-packages/pkg-aaaaaaaaaaaa-bbbbbbbb/readable.md\",\"span\":{\"kind\":\"full_document\"}}],\"counts\":{\"cards_staged\":0,\"edges_planned\":0,\"not_measured\":0,\"packages_seen\":0,\"refused\":0,\"skipped_unchanged\":0,\"tombstoned\":0},\"dry_run\":true,\"edges\":[],\"finished_at\":\"2026-11-24T08:56:20Z\",\"kc2_admission\":\"not_measured\",\"live_edges_query\":\"not_measured\",\"live_s3_resolve\":\"not_measured\",\"live_search\":\"not_measured\",\"run_id\":\"synthetic-c303\",\"schema\":\"PackageIngestReceipt/v1\",\"started_at\":\"2026-11-24T08:56:20Z\",\"tool\":{\"name\":\"fixture\",\"version\":\"1\"}}\n"
  },
  {
    "name": "direct-damaged-honest",
    "digest": "6767a097cc61c364b0a8b4e947f0ebe2e6c3f4095085dbc9e8f20122aeac5ef7",
    "code": "PASS",
    "exit": 0,
    "wire": "{\"content_sha256\":\"cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc\",\"damage_places\":1,\"damage_status\":\"damaged\",\"exporter_path_slug\":\"pkg-aaaaaaaaaaaa-bbbbbbbb\",\"kc2_admission\":\"not_measured\",\"knowledge_ready\":false,\"layer\":\"readable\",\"licence\":\"public_domain\",\"package_id\":\"d_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/book-package-2@r1\",\"package_slug\":\"pilot-s4-index-book\",\"publication_state\":\"public_domain\",\"schema\":\"PackageIndexCard/v1\",\"source_id\":\"d_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\",\"source_path\":\"articles/book-packages/pkg-aaaaaaaaaaaa-bbbbbbbb/readable.md\",\"span\":{\"kind\":\"full_document\"}}\n"
  },
  {
    "name": "nested-damaged-honest",
    "digest": "2d60cd1186ada0cbb82d48feb6fe3dfc2c03dfd9a55c65a33f890b596885d066",
    "code": "PASS",
    "exit": 0,
    "wire": "{\"cards\":[{\"content_sha256\":\"cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc\",\"damage_places\":1,\"damage_status\":\"damaged\",\"exporter_path_slug\":\"pkg-aaaaaaaaaaaa-bbbbbbbb\",\"kc2_admission\":\"not_measured\",\"knowledge_ready\":false,\"layer\":\"readable\",\"licence\":\"public_domain\",\"package_id\":\"d_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/book-package-2@r1\",\"package_slug\":\"pilot-s4-index-book\",\"publication_state\":\"public_domain\",\"schema\":\"PackageIndexCard/v1\",\"source_id\":\"d_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\",\"source_path\":\"articles/book-packages/pkg-aaaaaaaaaaaa-bbbbbbbb/readable.md\",\"span\":{\"kind\":\"full_document\"}}],\"counts\":{\"cards_staged\":0,\"edges_planned\":0,\"not_measured\":0,\"packages_seen\":0,\"refused\":0,\"skipped_unchanged\":0,\"tombstoned\":0},\"dry_run\":true,\"edges\":[],\"finished_at\":\"2026-11-24T08:56:20Z\",\"kc2_admission\":\"not_measured\",\"live_edges_query\":\"not_measured\",\"live_s3_resolve\":\"not_measured\",\"live_search\":\"not_measured\",\"run_id\":\"synthetic-c303\",\"schema\":\"PackageIngestReceipt/v1\",\"started_at\":\"2026-11-24T08:56:20Z\",\"tool\":{\"name\":\"fixture\",\"version\":\"1\"}}\n"
  },
  {
    "name": "integral-float-direct",
    "digest": "e84b5bccd0ef3559994c21e6eb46f67467faa05eea64b8c9c72596685deee1b5",
    "code": "IDX-DAMAGE",
    "exit": 1,
    "wire": "{\"content_sha256\":\"cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc\",\"damage_places\":0.0,\"damage_status\":\"clean\",\"exporter_path_slug\":\"pkg-aaaaaaaaaaaa-bbbbbbbb\",\"kc2_admission\":\"not_measured\",\"knowledge_ready\":false,\"layer\":\"readable\",\"licence\":\"public_domain\",\"package_id\":\"d_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/book-package-2@r1\",\"package_slug\":\"pilot-s4-index-book\",\"publication_state\":\"public_domain\",\"schema\":\"PackageIndexCard/v1\",\"source_id\":\"d_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\",\"source_path\":\"articles/book-packages/pkg-aaaaaaaaaaaa-bbbbbbbb/readable.md\",\"span\":{\"kind\":\"full_document\"}}\n"
  },
  {
    "name": "integral-float-nested",
    "digest": "a439714566c87cef34b777b3c3ba041a59816eb0275e519405572631561243bd",
    "code": "IDX-DAMAGE",
    "exit": 1,
    "wire": "{\"cards\":[{\"content_sha256\":\"cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc\",\"damage_places\":0.0,\"damage_status\":\"clean\",\"exporter_path_slug\":\"pkg-aaaaaaaaaaaa-bbbbbbbb\",\"kc2_admission\":\"not_measured\",\"knowledge_ready\":false,\"layer\":\"readable\",\"licence\":\"public_domain\",\"package_id\":\"d_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/book-package-2@r1\",\"package_slug\":\"pilot-s4-index-book\",\"publication_state\":\"public_domain\",\"schema\":\"PackageIndexCard/v1\",\"source_id\":\"d_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\",\"source_path\":\"articles/book-packages/pkg-aaaaaaaaaaaa-bbbbbbbb/readable.md\",\"span\":{\"kind\":\"full_document\"}}],\"counts\":{\"cards_staged\":0,\"edges_planned\":0,\"not_measured\":0,\"packages_seen\":0,\"refused\":0,\"skipped_unchanged\":0,\"tombstoned\":0},\"dry_run\":true,\"edges\":[],\"finished_at\":\"2026-11-24T08:56:20Z\",\"kc2_admission\":\"not_measured\",\"live_edges_query\":\"not_measured\",\"live_s3_resolve\":\"not_measured\",\"live_search\":\"not_measured\",\"run_id\":\"synthetic-c303\",\"schema\":\"PackageIngestReceipt/v1\",\"started_at\":\"2026-11-24T08:56:20Z\",\"tool\":{\"name\":\"fixture\",\"version\":\"1\"}}\n"
  },
  {
    "name": "invalid-timestamp",
    "digest": "ea62b2e17b0929efbdff3ab585b4c9ab3b7115870441339462b4ae64cd9efcfb",
    "code": "IDX-STRUCTURE",
    "exit": 1,
    "wire": "{\"cards\":[],\"counts\":{\"cards_staged\":0,\"edges_planned\":0,\"not_measured\":0,\"packages_seen\":0,\"refused\":0,\"skipped_unchanged\":0,\"tombstoned\":0},\"dry_run\":true,\"edges\":[],\"finished_at\":\"2026-11-24T08:56:20Z\",\"kc2_admission\":\"not_measured\",\"live_edges_query\":\"not_measured\",\"live_s3_resolve\":\"not_measured\",\"live_search\":\"not_measured\",\"run_id\":\"synthetic-c303\",\"schema\":\"PackageIngestReceipt/v1\",\"started_at\":\"invalid-date\",\"tool\":{\"name\":\"fixture\",\"version\":\"1\"}}\n"
  }
]'''


class PackageIndexCardTests(unittest.TestCase):
    def test_valid_card_passes(self) -> None:
        card = {
            "schema": "PackageIndexCard/v1",
            "source_id": "d_" + "a" * 64,
            "package_id": "d_" + "a" * 64 + "/book-package-2@r1",
            "package_slug": "pilot-s4-index-book",
            "exporter_path_slug": "pkg-" + "a" * 12 + "-" + "b" * 8,
            "span": {"kind": "full_document"},
            "licence": "public_domain;own_layers=CC-BY-4.0",
            "publication_state": "public_domain",
            "layer": "readable",
            "source_path": "articles/book-packages/pkg-" + "a" * 12 + "-" + "b" * 8 + "/readable.md",
            "content_sha256": "c" * 64,
            "damage_places": 0,
            "damage_status": "clean",
            "knowledge_ready": False,
            "kc2_admission": "not_measured",
        }
        result = run_checker(card)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_damaged_as_clean_refused(self) -> None:
        card = {
            "schema": "PackageIndexCard/v1",
            "source_id": "d_" + "a" * 64,
            "package_id": "d_" + "a" * 64 + "/book-package-2@r1",
            "package_slug": "pilot-s4-index-book",
            "exporter_path_slug": "pkg-" + "a" * 12 + "-" + "b" * 8,
            "span": {"kind": "full_document"},
            "licence": "public_domain",
            "publication_state": "public_domain",
            "layer": "readable",
            "source_path": "articles/book-packages/pkg-" + "a" * 12 + "-" + "b" * 8 + "/readable.md",
            "content_sha256": "c" * 64,
            "damage_places": 5,
            "damage_status": "clean",
            "knowledge_ready": False,
            "kc2_admission": "not_measured",
        }
        result = run_checker(card)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("damaged_presented_as_clean", result.stderr)

    def test_frozen_s4_cli_cases(self) -> None:
        # C303/C304 + KC-SWE C304/C305 replay. Raw bytes retain JSON 0.0.
        # Integral floats are schema-valid integers but intentionally refused by
        # the existing domain checker (IDX-DAMAGE); do not normalize them.
        cases = json.loads(FROZEN_S4_CASES_JSON)
        self.assertEqual(len(cases), 26)
        self.assertEqual(len({case["name"] for case in cases}), 26)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "case.json"
            for case in cases:
                with self.subTest(case=case["name"]):
                    wire = case["wire"].encode("utf-8")
                    self.assertEqual(hashlib.sha256(wire).hexdigest(), case["digest"])
                    path.write_bytes(wire)
                    result = subprocess.run(
                        [sys.executable, str(CHECKER), str(path)],
                        capture_output=True, text=True, check=False, timeout=30,
                    )
                    self.assertEqual(result.returncode, case["exit"], result.stderr + result.stdout)
                    if case["code"] == "PASS":
                        self.assertEqual(result.stdout.strip(), "ok")
                        self.assertEqual(result.stderr, "")
                    else:
                        self.assertTrue(result.stderr.startswith(case["code"] + ":"), result.stderr)
                        self.assertEqual(result.stdout, "")
                        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()

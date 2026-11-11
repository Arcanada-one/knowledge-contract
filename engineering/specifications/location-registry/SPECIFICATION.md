---
sources: none
name: "location-registry"
title: "Location Registry: Stable Ids and Copy Addresses"
artifact: "engineering-specification"
edition: "1.1"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "Repository-only engineering contract for content ids, package ids and a location registry that holds host/volume/path for each copy so cards and database records never embed paths."
---

# Location Registry: Stable Ids and Copy Addresses

**Author:** Pavel Valentov · **Status:** repository-only engineering document, not part of publication edition 1.1

| Implementation component | Scope |
| --- | --- |
| [Schema](../../../schemas/location-registry.schema.json) | `LocationRegistry/v1`, `LocationRegistryRow/v1`, `LocationVerifyReceipt/v1` |
| DEVS tools (`arcanada-workspace` `dev-tools/location-registry/`) | JSONL registry beside the Source Library store; SQL DDL for arcana-dbs; on-demand verifier + receipt |
| Rematch | KC-PIPE-S1 Source Library store layout and content ids — do not duplicate store import |

## 1. Purpose and boundary

Database records (graph, vector, text) and index cards name where a source lives by **id**, not by path. Programs resolve an id through the location registry to learn which server, disk and path hold a copy.

This specification fixes:

- the stable **source id** and **package id**;
- the **location registry** row for each physical copy;
- the obligation that cards and derived records carry ids only;
- the **verifier** that re-hashes registered copies and emits a run receipt.

It reuses and does not replace the [pipeline](../pipeline/SPECIFICATION.md) document key (`PIP-R002`), the [book package](../book-package/SPECIFICATION.md) identity fields, or the Source Library store layout (KC-PIPE-S1). It invents no X5 clean package and no KC2 admission (`kc2_admission` remains `not_measured`). Index ingest cards that cite these ids are specified separately in [package-index-ingest](../package-index-ingest/SPECIFICATION.md).

This document is a repository-only engineering contract. It is not in the publication catalogue. Live population of the registry for an imported library, and a live scheduled verifier run with zero unexplained mismatches, are measured separately; until measured they are `not_measured`, never pass or fail.

## 2. Stable identifiers

**LOC-R001.** The source id of an original MUST be `d_` followed by the lowercase hexadecimal SHA-256 of the exact bytes of that original, identical to the pipeline key (`PIP-R002`).

A changed byte string is a new source id. Human-facing names (slug, work, edition, representation, books-library `package_id`) are names that map to the source id in other registries; they are not the content key for location rows of originals.

**LOC-R002.** The package id for a derived package tree MUST be the source id, a single `/`, and the pipeline or tool version string that produced that tree (for example `d_<sha256>/book-package-2` or `d_<sha256>/<tool>@<version>`), matching the Source Library path key `packages/<source-id>/<pipeline-version>/`.

**LOC-R003.** A location (holder host, volume, path, Drive id, URL) MUST NEVER be used as a source id, package id, or card identity. A move of bytes MUST leave the id unchanged and MUST change only the registry row for that copy.

## 3. Location registry

The registry is the only authorised place that stores paths for Source Library copies. Index cards, graph nodes, vector records and text chunks carry ids and may note a role hint (`primary`); the filesystem path for the original or package lives only in the registry.

**LOC-R004.** Each physical copy MUST have exactly one registry row whose required fields are: `object_kind` (`original` or `package`), `object_id` (source id or package id per §2), `holder_host`, `volume`, `path`, `role` (`primary`, `mirror` or `backup`), `size_bytes`, `verified_at` (UTC timestamp or null when never verified), and `verified_sha256` (lowercase hex SHA-256 of the bytes at `path`, or null when never verified).

**LOC-R005.** For `object_kind=original`, `verified_sha256` when present MUST equal the 64-hex digest embedded in `object_id` after the `d_` prefix. For `object_kind=package`, `verified_sha256` when present MUST equal the SHA-256 of the package tree's declared root digest file or of the bytes the verifier is configured to hash for that row; a missing configuration MUST leave verification `not_measured`, not invent a digest.

**LOC-R006.** At most one row per `(object_id, role=primary)` MAY exist for a given holder contour; additional copies MUST use `mirror` or `backup`. A move that changes path MUST update that one row (or replace it atomically); it MUST NOT mint a new object id.

**LOC-R007.** Consumers that need bytes MUST resolve `object_id` → registry row(s) and then open `path` on `holder_host`/`volume`. A consumer MUST NOT reconstruct a path from an id by string convention alone when a registry row exists for that contour.

## 4. Verifier and receipts

**LOC-R008.** A verifier run MUST, for each selected row, attempt to read the bytes at the registered path, compute SHA-256, and classify the row as `ok` (digest matches expectation), `missing` (path absent), `corrupt` (digest mismatch), or `not_measured` (path unreachable or hash skipped with an explicit reason). Unexplained mismatches are `corrupt` rows without an authorised exception record.

**LOC-R009.** Every verifier run MUST emit a `LocationVerifyReceipt/v1` with: run id, tool name and version, start and finish timestamps, the registry digest (SHA-256 of the exact registry file or query snapshot bytes), counts per classification, the list of non-`ok` rows (or a truncated list with an explicit truncation flag), and `kc2_admission` equal to `not_measured`.

**LOC-R010.** A scheduled production verifier with zero unexplained mismatches MAY be claimed only when a receipt for that run is measured. Absence of a live run is `not_measured`, never pass.

## 5. Relation to Source Library (S1) and cards

**LOC-R011.** The location registry MUST address copies held by the Source Library store (or an evidenced DEVS staging root with the same id rules) and MUST NOT re-implement store import, capacity budgets or Drive mirroring; those remain KC-PIPE-S1.

**LOC-R012.** An index card, library entry or database record that refers to an original or package MUST carry the source id and/or package id, and MAY carry registry role metadata, but MUST NOT carry the filesystem path; path resolution is a registry lookup.

## 6. Honesty and admission

**LOC-R013.** Producer records and receipts under this specification MUST keep `kc2_admission` as `not_measured`. This leaf MUST NOT invent a populated imported library, an X5 clean package, or knowledge admission.

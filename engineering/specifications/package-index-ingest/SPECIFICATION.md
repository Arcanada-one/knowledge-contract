---
sources: none
name: "package-index-ingest"
title: "Package Index Ingest: Cards, Vectors, Full Text and Relation Graph"
artifact: "engineering-specification"
edition: "1.1"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "Repository-only engineering contract for ingesting book packages into the Scrutator index with cards that carry source/package ids, span and licence/publication state, reusing the kb-feeder lane pattern."
---

# Package Index Ingest: Cards, Vectors, Full Text and Relation Graph

**Author:** Pavel Valentov · **Status:** repository-only engineering document, not part of publication edition 1.1

| Implementation component | Scope |
| --- | --- |
| [Schema](../../../schemas/package-index-card.schema.json) | `PackageIndexCard/v1`, `PackageIngestReceipt/v1` |
| DEVS tools (`arcanada-workspace` `dev-tools/kc-package-ingest/`) | Allowlist, manifest, stage, reconcile, tombstone, rollback |
| Rematch | Location registry ids (S2); Source Library store (S1); X6 `books_package` path/DAMAGED gate; kb-feeder allowlist/manifest/tombstone/rollback |

## 1. Purpose and boundary

Packages (Markdown + images + relation graph) enter Scrutator as chunked embeddings (vectors), full text and typed graph edges. Each **index card** carries source id, package id, span and licence/publication state. Paths are never stored on the card; the [location registry](../location-registry/SPECIFICATION.md) remains the only place with host/volume/path.

This specification invents no X5 clean package and no KC2 admission (`kc2_admission` remains `not_measured`). Live Scrutator upsert/search, live S3 id resolve and live edge query against production stay `not_measured` until measured.

## 2. Card identity

**IDX-R001.** A card's `source_id` MUST be `d_` + lowercase hex SHA-256 of the original bytes (`PIP-R002` / `LOC-R001`).

**IDX-R002.** A card's `package_id` MUST be the location-registry package id: `source_id` + `/` + pipeline/tool version (`LOC-R002`).

**IDX-R003.** A card MUST also carry the book-package `package_slug` and the exporter path slug `pkg-<12 hex of source sha>-<8 hex>` used by the X6 path grammar `articles/book-packages/<slug>/(document|readable|knowledge).md`.

**IDX-R004.** A card MUST carry a `span` (at least `full_document` for a whole layer), a `licence` string derived from the package rights record, and a `publication_state` in `{public_domain, author_open, third_party_restricted, unknown}`.

**IDX-R005.** Cards and staged Markdown MUST NOT embed filesystem paths of the Source Library; they name ids only.

## 3. Lane pattern (kb-feeder rematch)

**IDX-R006.** The ingest lane MUST support: package allowlist; content-hash manifest; reconciliation counts (`packages_seen`, `cards_staged`, `skipped_unchanged`, `refused`, `tombstoned`, `edges_planned`); tombstones for removed allowlist entries; rollback of a run's staged paths.

**IDX-R007.** A positive damage place count MUST NOT be staged as `damage_status=clean` or `knowledge_ready=true` (PIP-R013 / X6 `refuse_damaged_as_clean`).

**IDX-R008.** Relation graph edges MUST be planned from package `relations.jsonl` as Scrutator `EdgeCreateByPath` payloads (`edge_type` = relation type, `created_by` = `kc-package-ingest`). Live edge insertion and query are measured separately.

## 4. Receipt honesty

**IDX-R009.** Every `PackageIngestReceipt/v1` MUST set `kc2_admission` to `not_measured`, and MUST set `live_search`, `live_s3_resolve` and `live_edges_query` to `not_measured` unless a measured live probe is attached.

**IDX-R010.** Reconciliation counts on the receipt MUST match the lane's observed actions for that run.

## 5. Conformance

Structural checks: [schema](../../../schemas/package-index-card.schema.json) and DEVS unit tests under `dev-tools/kc-package-ingest/tests/`. A passing hermetic run does not claim production search, S3 resolve or edge query.

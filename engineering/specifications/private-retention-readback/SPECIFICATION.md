---
sources: none
name: "private-retention-readback"
title: "Private Retention and Exact Readback"
artifact: "engineering-specification"
edition: "1.1"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "Repository-only engineering contract for Live Lab private artifact retention, opaque-id resolution to allowlisted stored objects, exact-byte readback with digest binding, retention tombstones and corpus separation."
---

# Private Retention and Exact Readback

**Author:** Pavel Valentov · **Status:** repository-only engineering document, not part of publication edition 1.1

| Implementation component | Scope |
| --- | --- |
| [Schema](../../../schemas/private-retention-readback.schema.json) | Retention profile, exact-readback receipt, tombstone/unavailable record |
| [Checker](../../../tools/check_private_retention_readback.py) | Schema + RET identity/path/digest/auth rules |
| [Fixtures](../../../schemas/fixtures/private-retention-readback/) · [tests](../../../tools/test_private_retention_readback.py) | Positive exact readback and one-defect refusals |
| Workspace tools | `dev-tools/kc-private-retention/` (DEVS hermetic + arcana-dbs store binding) |

## 1. Purpose, boundary and rematch

This specification fixes how **private** Live Lab originals and permitted derivatives are retained and how an authorized caller obtains **exact bytes** with digest binding. It selects the already-authorized Source Library store and Location Registry addressing; it does not invent a second blob store, a public download CDN, or a Scrutator private-namespace consumer (KB-CONS-01 / KCLIVE-09).

**Rematch (reuse, do not duplicate):**

| Residual | Binding |
| --- | --- |
| KC-PIPE-S1 Source Library | Canonical store root `arcana-dbs:/srv/source-library`; id grammar `d_` + sha256 of original bytes; layout `originals/<sha[0:2]>/<sha>` and `packages/<source-id>/<pipeline-version>/` |
| KC-PIPE-S2 LocationRegistry | Opaque id → holder/volume/path rows (`LocationRegistry/v1`); cards never embed paths |
| KC-PIPE-S3 Retrieval | Authorized `GET /v1/kc/retrieve` gateway; live host fetch may remain `not_measured` until separately evidenced |
| KC-PIPE-X9d Private registry | Semantic private registration is a different plane; this leaf retains **source/result bytes**, not SkillPin admission |

`kc2_admission` is always `not_measured`. This leaf MUST NOT invent an X5 clean package or knowledge admission.

## 2. Retention profile

**RET-R001.** The Live Lab private retention profile MUST name the authorized store contour (`holder_host`, `volume`, `store_root`), the id grammar (`d_<sha256>` for originals; package ids per LOC-R002), the digest domain (`sha256` of exact original or declared package root bytes), and the review-period retention obligation. Declaring a folder in prose MUST NOT assert deployment; measured binding requires a store layout observation.

**RET-R002.** Originals and full OCR / package trees retained under the Source Library MUST remain separate from `kc-corpus` derived-artifact collection and from public publication catalogues. A private retention receipt MUST set `published_corpus_admission` to `not_applicable` or `not_measured` and MUST NOT claim public library acceptance.

**RET-R003.** Retention pins for acceptance evidence MUST survive ordinary capacity and restart checks for the declared review period. Capacity alerts remain S1/S5; this profile MUST NOT silently delete a pinned object without a tombstone.

## 3. Opaque id resolution and exact readback

**RET-R004.** Exact readback MUST accept only an opaque authorized object id (`d_<sha256>` or package id). It MUST resolve that id through the Location Registry when a registry row exists for the contour, otherwise through the Source Library allowlisted index (`index/by-id.jsonl` → `originals/<sha[0:2]>/<sha>` under the measured store root). Caller-supplied filesystem paths, Drive URLs or arbitrary fetch URLs MUST be refused.

**RET-R005.** A successful exact readback MUST recompute SHA-256 over the returned bytes, MUST require equality with the digest embedded in the original's source id (or the registry `verified_sha256` for a package), MUST record `size_bytes`, digest algorithm/domain, source/producer build when known, and MUST emit `PrivateExactReadbackReceipt/v1` with `content_exact=true`. A metadata-only HTTP 200 or a `content_hash` without body recompute is insufficient.

**RET-R006.** Exact readback MUST fail closed when the authorization required for the operation is absent. Private membership MUST NOT be disclosed to unauthorized callers (unknown and unauthorized both answer as unavailable / not_found at the gateway). Browser/final-origin access is out of scope for this leaf (KCLIVE-19/20/23).

## 4. Unavailability and collection

**RET-R007.** Intentionally collected or expired objects MUST produce an observable tombstone with state `collected` or `unavailable`, preserving the object id and prior digest when known. Consumers MUST surface that state and MUST NOT fabricate a green download or file link from historical metadata alone.

**RET-R008.** A missing path without a tombstone is `missing` (distinct from `collected`). Corrupt bytes (digest mismatch) are `corrupt` and MUST NOT be served as exact content.

## 5. Honesty and stage delivery

**RET-R009.** Every retention profile, readback receipt and tombstone record under this specification MUST carry `runtime_authorized=false`, `knowledge_admitted=false` and `kc2_admission=not_measured` until a separately measured runtime and admission exist.

**RET-R010.** Merge of implementation is stage/batch only (DEC-AUP-0167). An author leaf MUST NOT push to `main`, force-push, or claim DONE/admission from author evidence alone.

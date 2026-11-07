---
sources: none
name: "private-artifact-registry"
title: "Private Artifact Registry: Acceptance Gate, Readback, Retrieval and Use Witness"
artifact: "engineering-specification"
edition: "1.1"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "Repository-only engineering contract for registering accepted semantic artifacts on the private knowledge route, with identity readback, request retrieval, context delivery, use witnesses and separate authority boundaries."
---

# Private Artifact Registry: Acceptance Gate, Readback, Retrieval and Use Witness

**Author:** Pavel Valentov · **Status:** repository-only engineering document, not part of publication edition 1.1

| Implementation component | Scope |
| --- | --- |
| [Schema](../../../schemas/private-artifact-registry.schema.json) | Handoff, registry, readback, retrieval, delivery, use-witness and per-book outcome records |
| [Checker](../../../tools/check_private_registration.py) | Schema + PAR identity/acceptance/authority rules |
| [Fixtures](../../../schemas/fixtures/private-artifact-registry/) · [tests](../../../tools/test_private_registration.py) | Valid positive path and one-defect refusals |
| Workspace tools | `dev-tools/kc-private-registry/` (DEVS hermetic register/readback/retrieve/deliver/witness) |

## 1. Purpose, boundary and status

This specification fixes how an **accepted** semantic artifact (Role, Skill, Competency, Blueprint, Constraint or other canonical profile) enters the **private** knowledge route: what acceptance evidence is required, how the private registry names a revision, how identity readback and request retrieval work, how complete context is delivered, how a use witness is recorded, and how authority boundaries stay separate.

It reuses the [artifact registry](../artifact-registry/SPECIFICATION.md) identity rules and the pipeline document key `d_<sha256>` ([pipeline](../pipeline/SPECIFICATION.md) PIP-R002). It does **not** replace library acceptance of a `book-package/2`, published corpus admission, Scrutator index readback under a reader grant, or native task-run authority. Live Scrutator private-namespace binding and consumer delivery remain Agent-SWE work under KB-CONS-01; this document is the KC-SWE registration and hermetic evidence contract.

This document is a repository-only engineering contract. It is not in the publication catalogue. `kc2_admission` is always `not_measured` on every receipt.

## 2. Authority boundaries

**PAR-R001.** Every registration, readback, retrieval, delivery and use-witness receipt MUST carry an `authority_boundaries` object with exactly these keys, each valued `pass`, `fail`, `not_applicable` or `not_measured`, and MUST NOT treat any one of them as implying another: `source_rights`, `library_acceptance`, `private_registry_adoption`, `published_corpus_admission`, `index_readback`, `native_task_run_authority`.

**PAR-R011.** A successful private registration MAY set `private_registry_adoption` to `pass` for the hermetic or private-file route under test.

**PAR-R012.** It MUST leave `published_corpus_admission`, `index_readback` and `native_task_run_authority` as `not_measured` or `not_applicable` unless those authorities were separately measured.

**PAR-R013.** Library acceptance of a book package MUST NOT be recorded as private registry adoption.

## 3. Acceptance gate

**PAR-R002.** A private registration MUST refuse an artifact that lacks a pinned `SemanticAcceptanceRecord/v1` whose `result` is `supported`, whose `artifact_sha256` equals the SHA-256 of the exact artifact file bytes being registered, whose `assessor_id` is nonempty and distinct from `producer_id`, and whose `scope` names the permitted purpose and exclusions.

A mechanical schema or layout check is not semantic acceptance.

**PAR-R014.** An unreviewed X9c draft MUST be refused with reason `acceptance_missing` or `acceptance_insufficient` and MUST NOT appear as a registered revision.

**PAR-R003.** Registration of an accepted artifact MUST record: stable `artifact_id`, `revision`, `kind`, `path`, `sha256`, `byte_length`, `source_document_id` (`d_<sha256>` or an explicit `not_measured` with reason), the acceptance record digest, and a finite `dependency_closure` of required revisions (each with path, sha256 and role). A mutable `current` pointer MUST NOT substitute for a pinned revision.

## 4. Identity readback

**PAR-R004.** Readback by identity MUST return the registered revision whose `artifact_id` and `revision` match the request, MUST recompute the digest of the stored bytes and refuse on mismatch (`digest_mismatch`), and MUST emit a `PrivateReadbackReceipt/v1` carrying the matched fields and `kc2_admission` = `not_measured`.

## 5. Retrieval and context delivery

**PAR-R005.** Retrieval for a concrete request MUST select at most the registered revisions whose applicability covers the request (or refuse with `unsuitable_context`), MUST include every member of the primary artifact's `dependency_closure`, MUST record the observed byte/token budget and any truncation as measured values or `not_measured` with reason, and MUST NOT silently omit a required dependency.

**PAR-R006.** Complete context delivery MUST list every selected revision by identity, path and sha256, the request identifier, the recipient identifier, and the delivery outcome (`delivered` or a refusal code). Changing the recipient or the request outside applicability MUST refuse or reassess; it MUST NOT reuse a prior positive delivery receipt as current suitability.

## 6. Use witness and per-book outcomes

**PAR-R007.** A use witness for a book MUST record the selected/applied artifact identities, the concrete task or request, the resulting output digest or text hash, and an assessment (`applied`, `refused`, `reassessed`, `unresolved`) with reason. Generated Markdown alone is not a use witness.

**PAR-R008.** For every book in the declared cohort, the outcome record MUST carry either one inspectable use-witness receipt id or a precise `unresolved` outcome with `owner` and `blocking_reason`. A known blocked or unaccepted book is not a completed conversion.

## 7. Negative controls

**PAR-R009.** The hermetic suite MUST exercise and refuse or reassess each of: changed source bytes or source_document_id, changed request or recipient, missing dependency, malformed or unknown evidence, and unsuitable context. Each case MUST name the failing condition. Prior accepted revisions MUST remain readable after a refusal.

## 8. Honesty labels

**PAR-R010.** Every receipt MUST set `runtime_authorized` to `false` and `knowledge_admitted` to `false` while the native KC2 dispatcher route remains unwired, and MUST set `kc2_admission` to `not_measured`. A hermetic PASS is not live Scrutator index readback and is not native task-run authority.

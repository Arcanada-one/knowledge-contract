---
title: "Relation Overlay: A Bounded Cross-Package Meaning Profile"
short_title: "Relation Overlay"
artifact: "research-proposal"
status: "proposal; not a published or implemented exchange profile"
author: "Knowledge Contract research collective (KC-Brain)"
language: en
license: CC-BY-4.0
sources: none
updated: 2026-11-08
---

# Relation Overlay: A Bounded Cross-Package Meaning Profile

**Purpose.** Provide an independently reviewable **G11 scientific/semantic input** for Knowledge Collective Live Lab. It is a bounded model for relating statements belonging to **two separately immutable knowledge packages**. It does not amend the closed `book-package/2` schema, silently bless candidate claims, create a production API, or authorize multi-source action.

**Source boundaries.** The accepted Knowledge Contract edition 1.1 at commit `a0450428704fcd41b411203f2fc88c06c779610b` provides [Book Packages](../../engineering/specifications/book-package/SPECIFICATION.md), [Semantic Types](../../engineering/specifications/semantic-types/SPECIFICATION.md) and [Context Packages](../../engineering/specifications/context-package/SPECIFICATION.md). Book-package relations are **within one package**: relation types `defines`, `uses`, `variant_of`, `requires`, `compared_with`, `contradicts`, with separate evidence for both ends of a contradiction (BPK-R023–R025). The existing architecture does **not** contain an accepted generic cross-package wire profile. The Live Lab proposal [G11](https://github.com/Arcanada-one/arcanada-workspace/blob/d039996af7b250565229b64e71e43dde037326f1/documentation/plans/knowledge-collective-live-lab/implementation-contracts/2026-11-07/closure-audit/ENGINEERING-ADDENDUM.md#g11) calls for such a limited, reviewed overlay. This document is an original engineering-scientific synthesis of those internal sources; no external experimental results are claimed.

## 1. Scope and protected distinctions

An overlay relates selected **statement-level** objects in exactly two pinned packages A and B; the packages are not rewritten. It can record a candidate association, a reviewer-accepted relation in a defined scope, or a rejected/undetermined interpretation. It does **not** establish extraction correctness, causal independence, truth, applicability, policy permission or execution success.

Five distinctions are non-substitutable:

1. **Identity versus similarity.** Matching human-readable titles, text or local object IDs does not establish identity of source, edition, language, statement, unit or applicability.
2. **Quotation versus independent support.** A quotation, translation, copied dataset or derivative paraphrase inherits source lineage. Several repetitions cannot be counted as independent evidence.
3. **Navigation versus inference.** A link that helps find a source is not a deductive premise, proof, mandatory dependency or permission.
4. **Statement contradiction versus source corruption.** Opposing statements may contradict only after their quantified scope, conditions, units, time and attribution are aligned. An unavailable source is unresolved, not a counterexample.
5. **Review versus action.** A reviewed relation can help compose a context, but a valid, current, task-specific authority and discharged prerequisites remain separately necessary at the actual action boundary.

## 2. Qualified endpoints and release pins

For this candidate profile, an endpoint is the conceptual tuple:

`(package_id, package_manifest_digest, release_id, component_id, object_id, representation_id, representation_digest, source_anchor)`.

The digest must carry its algorithm, byte domain and exact source revision, not a bare hexadecimal string. `object_id` and `source_anchor` are **local to the specific pinned package/component/representation**. The name `release_id` alone is not a byte proof, and a readable title is not a locator.

A candidate overlay is valid for inspection only when both package manifests resolve to exact immutable bytes, the cited object records and source anchors exist at the specified representations, and the asserted source binding is unambiguous. Verification of a digest establishes byte identity, **not** the truth of the object or current access. If both endpoints share the same local object ID, they remain distinct because their complete qualified identities differ.

Package A and package B have their own rights, review, source coverage and release status. An overlay cannot upgrade them. A rejected or stale endpoint cannot be made current by a fresh overlay timestamp. Replacing an endpoint is a **new overlay revision with a fresh review obligation**, not mutation behind an old identity.

## 3. Minimal proposed data model (not a released wire schema)

The following fields are semantic obligations for a future explicit schema and validator; names below are illustrative and **not** registered production API fields:

- **Envelope:** `overlay_profile` and version (candidate `cross-package-relations/0.1`), immutable overlay revision, purpose, intended consumer, author, source manifest pins for A and B, declared supported relation vocabulary and review state.
- **Relation:** stable overlay-local relation ID; exactly one qualified `from` and `to` endpoint; directed relation kind; assertions with polarity, modality, attribution, quantifier/scope, applicable conditions, relevant units and valid-time window. No implicit unit conversion.
- **Grounding:** each edge retains source-specific `from` and `to` anchors, a declaration of whether the support is quotation, derivative, observation or independent review, and exact reviewer notes. Contradictions require **both** sides grounded; an omitted or invisible side is unresolved.
- **Lineage:** explicit `derived_from` or `rendition_of` origin and pinned revisions, when known, so repeated renderings are not misclassified as independent corroboration. Unknown lineage is marked unknown, never presumed independent.
- **Assessment:** reviewer identity/role, independently inspectable assessment evidence, reviewed edge revision, exact scope, recorded time, verdict and remaining uncertainty. A producer's `accepted` string is not independent review. Distinguish a valid structure from a reviewed scientific claim and from an admitted task-specific dependency.
- **Current check:** endpoint availability and permissions at the consumer boundary; permitted purpose; revoked/superseded/stale/unknown state; overlay profile support; required-dependency closure. Old immutable run records remain available without reviving a revoked current permission.

A producer may create a **candidate** overlay. A reviewer may accept *one stated edge under one stated interpretation* without accepting the entire source package or all downstream applications. The first implementation should accept exactly two package identities and a small explicit vocabulary. Unsupported relation kinds and versions fail closed rather than being mapped to approximate synonyms.

## 4. Relation vocabulary and inferential limits

| Candidate relation | Semantics | Forbidden inference |
| --- | --- | --- |
| `quotes` | A statement reproduces or explicitly attributes a passage in B. | A second independent confirmation or ownership transfer. |
| `rendition_of` | Versioned translation/representation relation, with its own rendition pin. | Byte identity or full semantic equivalence absent scoped review. |
| `compares_with` | Reviewable comparison under stated dimensions, conditions, units and time. | Claim of equivalence or superiority. |
| `supports_under` | Specific evidence is relevant to a specified proposition under recorded premises and scope. | Unconditional proof, causal independence or current authority. |
| `contradicts_under` | Two attributed propositions cannot both hold under their **explicitly harmonized** assumptions; both sides are evidenced. | That either source is false outside the shared domain. |
| `requires_for_use` | A trusted, task-bound requirements decision names an endpoint as mandatory for a particular use. | Authority derived merely from self-declared overlay edges. |

A generic `related_to` may be used **only for navigation** and never contributes to dependency or proof closure. A `requires_for_use` edge becomes mandatory only through independent trusted requirements, not because the overlay producer chose that label. The relation is evidence **about** a possible dependency; the authoritative requirement revision decides whether it is actually required.

## 5. Conservative evaluation and closure

Let `R` be the exact trusted task-requirements revision, `P_A,P_B` the pinned packages, `O` the pinned overlay and `t` the consumer check time. Define `usable(edge,R,t)` only if:

- the overlay version is supported; both exact source/package/object/anchor pins resolve without ambiguity;
- conditions, quantifiers, attribution, units and applicable time have been compared, not silently normalized;
- the edge's requested use fits its recorded review scope and accepted status, and required evidence is accessible;
- both endpoint access/revocation checks are current for the consumer and permitted purpose;
- any mandatory closure set arises from `R` and its trusted dependencies. An **inspectable** overlay may explicitly retain unresolved members, but an **actually completed use-closure** requires every mandatory member to be discharged under the **same applicable** `R`/context, with current permission checks. `usable` for inspection never means complete closure or authorizes effects.

If any requirement fails, return an explicit **partial, conflicting, stale, inaccessible, unsupported or unresolved** assessment with preserved causes; these labels describe a **proposal-level** decision taxonomy, not registered runtime error codes. No externally consequential operation follows solely from this relation evaluator. At action dispatch additionally check (i) complete mandatory context delivery, (ii) discharge of **all** individual prerequisites, and (iii) current authority/effect identity. A known fact for member A and unknown fact for member B in a two-member requirement is **not** success.

For contradiction `contradicts_under`, verify that premises genuinely overlap. For example, “load <= 10 kg” and “load > 10 kg” may conflict only if subject, measurement unit, time, quantification and applicability align; differing date or population can instead remove the contradiction. A source's refusal to speak on a condition is **not** evidence for its negation.

## 6. Finite, adversarial acceptance corpus (specification, not executed results)

| Case | Input | Expected bounded outcome |
| --- | --- | --- |
| G11-A1 local-ID collision | Both packages contain object `o-17` with different full pins. | Preserve two endpoints; no same-object or self-support inference. |
| G11-A2 unit/scope mismatch | Same wording but kilograms versus pounds, or present versus historical applicability. | Explicit unresolved comparison until a reviewed conversion/scope rule is supplied. |
| G11-A3 copied support | B quotes A; a translation of B repeats the same claim. | One lineage family, not three independent supports. |
| G11-A4 one-sided contradiction | Contradiction edge has only a from-side anchor. | Reject semantic acceptance; preserve candidate and missing-side reason. |
| G11-A5 true two-sided conflict | Both qualified endpoints conflict under a stated common assumption. | Retain both facts and a scoped `contradicts_under` record; do not silently select winner. |
| G11-A6a newer immutable revision | B1 remains immutable, accessible and permitted; a distinct B2 is published, but request `R` still pins A1/B1. | Publication of B2 alone does not revoke B1 or invalidate an otherwise applicable, scoped A1/B1 review. Do not transfer the review to B2. |
| G11-A6b revision-selected use | Request `R′` pins B2 rather than B1, with identical readable title/local ID. | The reviewed A1/B1 pair cannot discharge R′; new qualified endpoints and scoped review are required. |
| G11-A6c revoked original | B1 bytes remain historically inspectable but current-use permission for B1 has been revoked. | Refuse current use under R even with intact source hashes; historical record is retained without recreating authority. |
| G11-A7 revoked/inaccessible endpoint | Digest resolves but current authorization denies read. | No current multi-source closure; never infer source availability from historic hash. |
| G11-A8 unknown overlay profile | Unsupported `cross-package-relations/9`. | Explicit unsupported, no permissive fallback. |
| G11-A9a unresolved mandatory dependency | Task requires independently discharged A and B under a shared R/context; A is grounded, B unknown. | The overlay may be inspected with explicit unresolved B, but use-closure is incomplete and causes zero new external effects. |
| G11-A9b completed dependency positive control | Both A and B are independently discharged under the same current R/context, and both endpoints remain permitted. | This limited prerequisite closure may be reported complete; consequential effects still separately require current authority, delivery and durable effect identity. |
| G11-A10 positive supported pair | Two accessible pinned packages, source-specific anchors, compatible conditions, independent scoped review and current permitted read. | Scoped relation may be consumed for inspection; no promotion to proof or execution grant. |

The consumer's **positive control** must remain useful. A validator that rejects every relation is not conformant. A structure-only PASS is not a semantic review, a native admission result or a successful site demonstration. Real schemas/tests/runs and reviewer evidence must be cited separately when they exist.

## 7. Ownership, dependencies and stopping rules

- **KC-Brain:** author of this semantic candidate, exact examples, limits, and response to substantive scientific review. This note is not F02, F04 or a replacement for a published paper.
- **Agent-Brain:** separate architecture/semantic reviewer; check the vocabulary against the actual consumer and identify unsupported inferences.
- **KC-SWE:** after current K8 rendition-sidecar schema has stable reviewed endpoint identities, reconcile the *real native Muneral* producer task/owner (possibly KCLIVE-08) before undertaking one bounded validator; do not invent a UUID, broaden an admitted task silently or create duplicate workers.
- **Agent-SWE:** consumer work only through the already owned, eligible KCLIVE-09 / KB-CONS-01 boundary, and later KCLIVE-12 when multi-source context is explicitly in scope. Do not dispatch blocked readiness from an email or this document.

A reviewed single-source exact consumer pilot does **not** depend on G11. Multi-source reconciliation claims **do** require an accepted versioned overlay, producer readback, independent review and consumer evidence. The present output is **scientific/protocol design only**. No schema has been installed, no production validator run, no site published, no task accepted or closed and no index admitted as a result of this document.

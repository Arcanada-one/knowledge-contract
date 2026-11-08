---
name: "knowledge-evolution"
title: "Knowledge Evolution: Versioned Rules"
short_title: "Knowledge Evolution"
subtitle: "Versioned Rules"
previous_title: "Knowledge Evolution and Versioned Rules"
artifact: "engineering-specification"
edition: "1.1"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "Versioned creation rules, adoption, impact analysis, reassessment, migration and coherent publication."
---

<!-- markdownlint-disable-next-line MD033 -->
<a id="knowledge-evolution-and-versioned-rules"></a>

# Knowledge Evolution: Versioned Rules

**Author:** Pavel Valentov · **Publication edition:** 1.1

## 1. Purpose and conformance

This is an architectural requirement set. Interoperability requires a named representation profile; the implemented exchange subset is limited to [observations, change events and profile advertisements](../status-model/SPECIFICATION.md#8-bounded-exchange-profile), and the [book-package profile](../book-package/SPECIFICATION.md) has its own schema. No full-contract wire format or deployed runtime is implied.

**EVO-R001.** Every new knowledge or decision artifact MUST record the exact contracts, profiles and rules that materially governed its creation.

Reassessment under later rules is a new observation. The original derivation and revision remain traceable.

Capitalized requirements use [BCP 14](../../../reference/bibliography/BIBLIOGRAPHY.md#requirement-language). This specification governs changes to interpretation and admission rules as well as software versions. A named research direction does not by itself establish an implemented schema or executable validator. The [revision paper](../../../papers/revision-and-governance/PAPER.md) supplies the underlying model.

## 2. Creation basis

**EVO-R002.** A creation-basis record MUST identify the artifact revision, material source revisions, contract and profile definitions, relevant rule-set versions, transformation recipe, responsible actor, creation time or interval, and known gaps.

**EVO-R003.** References MUST resolve to immutable revisions or record the inability to resolve them.

Only actually used rules are included as creation inputs.

**EVO-R004.** A later adopted rule MUST NOT be inserted into the old basis as though it governed the original work.

Broad labels such as “latest contract” are insufficient when the exact revision is material.

**EVO-R005.** The implementation MUST distinguish content change from representation change, assessment change and governance change.

An updated assessment can change whether a use is admitted without modifying source bytes. A corrected interpretation produces a new semantic revision even if the original source is unchanged.

## 3. Change proposal and adoption

**EVO-R006.** Each proposal MUST identify the previous and proposed rule revisions, motivation, affected scope, expected compatibility, migration implications, evidence, objections and known unresolved questions.

Adoption requires the decision maker and authority specified by the governance policy. A contributor, editor or automated validator does not acquire that authority merely by producing a proposal.

**EVO-R007.** Conflicting adoption decisions MUST block the affected use until a decision maker with authenticated authority resolves the conflict or explicitly adopts a permissible narrower scope.

The unresolved conflict is `unknown_impact` with unknown eligibility and an `unresolved` operation outcome; a separate known prohibition yields `blocked` and refusal. The expected test result is no publication or admitted serve while the conflict is unresolved.

An adoption decision is evidence that a norm was accepted within its scope. It is not proof that every factual claim motivating that norm is true.

**EVO-R008.** The decision MUST retain links to the assessed proposal and any restrictions or effective date.

## 4. Impact analysis and reassessment

Impact analysis starts from declared dependency relations.

**EVO-R009.** Affected artifacts MUST be classified with the relevant new rule set and use scope.

The impact tokens are `compatible`, `restricted`, `requires_review`, `blocked` and `unknown_impact`, with the eligibility/decision mapping in the [status model](../status-model/SPECIFICATION.md#3-canonical-dimension-vocabularies). These are projections over individual observations, not permanent global truth labels.

**EVO-R010.** A compatibility result MUST state the preservation argument or tests.

Unknown dependency coverage cannot support a claim that every affected artifact was found. Conservative re-evaluation is required when an untracked dependency could change a mandatory obligation.

Reassessment records the old artifact, new rule set, relevant current state, method, results and limitations. A passing reassessment under a narrower test does not establish compatibility with a broader profile. Multiple assessments can coexist when their scopes differ.

## 5. Migration

A migration creates a new representation or revision with an explicit source link, mapping, validator results, losses and unresolved fields.

**EVO-R011.** It MUST preserve negation, conditions, attribution and applicable constraints or declare their loss.

**EVO-R012.** Missing capability or authority MUST remain unknown.

A migration cannot manufacture an execution attempt or successful result.

**EVO-R013.** If semantic equivalence has not been established, the migration MUST state that limit even when the new structure is valid.

Reversible byte transformation establishes only the declared representation property. Lossless semantic migration needs an interpretation-preservation argument within a defined domain.

## 6. Visibility and rollback

**EVO-R014.** Publication MUST select a coherent set of artifact revisions, catalogue entries and rendered representations.

**EVO-R015.** A pointer update MUST have an identified adoption decision and the complete atomic [publication guard](../cache-identity-and-invalidation/SPECIFICATION.md#5-guarded-publication-and-serving), including current authority and dependency epochs.

**EVO-R016.** The website, downloadable corpus and API index MUST expose their actual source revisions so a consumer can detect differences.

Rollback changes the selected current head; it does not erase the later revision or its observations.

**EVO-R017.** If a rule was withdrawn because of a known defect or disclosure restriction, a rollback MUST preserve that knowledge and MUST NOT silently reauthorize a previously blocked use.

## 7. Acceptance cases

Required cases include a rule revision with no content change; an affected artifact discovered through an indirect dependency; an unresolved impact due to incomplete dependencies; an invalid migration that loses a constraint; conflicting adoption decisions; a late publisher; and rollback after revocation.

**EVO-R018.** Each case MUST retain the historical creation basis and the separate current decision.

The [projection and revision study](../../studies/executable-projections-and-revision/STUDY.md) supplies bounded evidence about addressed changes and finite projections. The [conformance study](../../studies/contract-profile-conformance/STUDY.md) records limited migration checks. Their results do not establish automatic migration of arbitrary knowledge graphs or a deployed community governance service.

## 8. Publication and implementation versions

**EVO-R019.** The document edition, serialized profile, validator implementation, evidence protocol, service build and index snapshot MUST have separately identified versions.

Removing a development label from a manuscript does not change a deployed protocol. Conversely, an unfinished service feature does not prevent publication of a complete formal argument with explicit assumptions.

The [source map and compatibility record](../../../appendices/source-map/APPENDIX.md) identifies what this edition replaces and what historical wire versions remain unchanged. The [API integration appendix](../../../appendices/api-integration/APPENDIX.md) defines the observable publication boundaries without claiming an unverified contract-composition endpoint.

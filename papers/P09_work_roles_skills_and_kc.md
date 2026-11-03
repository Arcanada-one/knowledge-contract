---
artifact_id: MM_A0206
revision_id: MM_A0206-entry-en-r1
title_en: "Knowledge Contract v3: Synthesis of the General Model and a Professional Profile"
title_ru: "Контракт знаний v3: синтез общей модели и профессиональный профиль"
language: en
status: scientific draft
scientific_status: concept_draft
license: CC-BY-4.0
full_text: ru/P09_work_roles_skills_and_kc.md
---

# Knowledge Contract v3: Synthesis of the General Model and a Professional Profile

| Field | Value |
| --- | --- |
| Artifact id | MM_A0206 (permanent) |
| Entry page revision | MM_A0206-entry-en-r1 |
| Full text | [Russian original](ru/P09_work_roles_skills_and_kc.md), language: Russian |
| Status | scientific draft (`concept_draft`); not a finished result |
| Licence | CC BY 4.0 |

## Abstract

The paper proposes a general Knowledge Contract (KC) v3 interface linking addressable content to purpose, conditions, grounds, dependencies and rules of use. Nine core groups are extended by six selective profiles: professional, dialogue, document, reasoning, visual and reuse. The professional profile separates a unit of work (`WorkItem`), role (`Role`), skill description (`Skill`), solution scheme (`Blueprint`), executor capability, current authority, attempt and evidence. For a bounded interchange format the authors implemented a JSON Schema, consistency checks, consumer compatibility, evaluation of current use and migration of a subset of v2. The implementation is finite and works on trusted, already interpreted JSON inputs.

## Claims and their basis

- The authors' first run passed 35/35 contract scenarios. Basis type: finite-test; taken from the paper's table, not recounted.
- A control set passed 26/26 (6 permitted positive outcomes, 17 forbidden admissions, 3 migration checks). It was composed by a separate agent of the same research session, reading only the public interface; not external verification. Basis type: finite-test. One control intent is unmapped, five partly mapped.
- Two authors' cases and four control cases with false trusted inputs were accepted; they show the model boundary and stay outside the main figure. Basis type: finite-test (6 cases).
- A diagnostic ablation without part of the checks scored 3/9 against 9/9; it is not a strong baseline. An exploratory comparison with a strong plain form, prepared after the first results were disclosed, scored 9/9 on both sides. Advantage in correctness is not established. Basis type: finite-test (9 inputs).
- The distinctions among role, skill description, solution scheme, capability and authority are definitions. Basis type: authors-domain-assessment.
- The central proposal, that separate subjects, versions and obligations make acceptance of work more controllable, is a hypothesis; H01-H04 are planned, not executed. Basis type: hypothesis.

## Limits

- The validator does not establish that source markup is correct or that external authority is genuine.
- Speed and cost were not measured; nine groups and six profiles are not shown necessary or minimal.
- The check records no revision or hash of the contract itself; end-to-end conformance to a changed contract is left to later work.
- Authors, composer and assessors share one session; no organisational independence is established.
- Migration covers one historical shape; semantic equivalence stays `not_established`.

## Status and what is open

- The late research synthesis gate is open.
- Independent semantic review of this text has not been performed.
- The English page is a summary, not a translation, and does not replace the Russian original.
- Held inconsistencies: the paper says another team member composed the control set, the review says an agent of the same session (this page follows the review); a later note speaks of seven profiles, the paper lists six.

## Relation to the full text

The Russian full text is the terminology edition of 2026-11-03 (front matter and links aside). Its abstract understates executed results and the same-session caveat; this page follows the corrected, evidence-bound wording from the editorial review. The Russian text is published without the card corrections, so its abstract may differ from this page.

## Credit and licence

Based on Knowledge Contract Arcana, <https://contract.place> (CC BY 4.0). Licence: [CC BY 4.0](../LICENSE). Credit lines and how to cite: [ATTRIBUTION.md](../ATTRIBUTION.md); rights holder statement for the repository: [NOTICE](../NOTICE); third-party sources: [SOURCES.md](../SOURCES.md).

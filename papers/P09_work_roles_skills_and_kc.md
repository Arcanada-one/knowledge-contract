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

The paper proposes a general Knowledge Contract (KC) v3 interface linking addressable content to purpose, conditions, grounds, dependencies and rules of use. Nine core groups are extended by six selective profiles. The professional profile separates a unit of work (`WorkItem`), role (`Role`), skill description (`Skill`), solution scheme (`Blueprint`), executor capability, current authority, attempt and evidence. For a bounded interchange format the authors implemented a JSON Schema, consistency checks, consumer compatibility, evaluation of current use and migration of a subset of v2. The implementation is finite and works on trusted, already interpreted JSON inputs.

## Claims and their basis

- The authors' first run passed 35/35 contract scenarios. A control set passed 26/26. Basis type: finite-test. The control set was composed by a separate agent of the same research session from the public interface; it is not external verification. One control intent is unmapped and five are partly mapped.
- Two authors' cases and four control cases with false trusted inputs were accepted. They show the model boundary and stay outside the main figure. Basis type: finite-test.
- A diagnostic ablation without part of the checks scored 3/9 against 9/9; it is not a strong baseline. An exploratory comparison with a strong plain form, prepared after the first results were disclosed, scored 9/9 on both sides. Basis type: finite-test.
- A strong plain alternative for targeted revision gave the same result in 30 pairs, a negative result. Basis type: finite-test; the underlying report was not read.
- The distinctions among role, skill description, solution scheme, capability and authority are definitions. Basis type: authors-domain-assessment.
- RU10 cross-check, by the kit authors and one assistant: 107 entries of the r1 delivery use valid AKP forms. The r2 set has 110 entries, after three competence descriptions were added. In r1, 14 of 14 retained results were re-mapped to the contract. An empty `Blueprint` list in the first adapter was fixed. Basis type: authors-domain-assessment.
- The central proposal (more controllable acceptance of work) is a hypothesis; H01-H04 are planned, not executed. Basis type: hypothesis.

## Limits

- Source markup correctness and external authority are not established by the validator.
- Speed and cost were not measured; nine groups and six profiles are not shown minimal.
- The check records no revision or hash of the contract itself.
- Authors, composer and assessors share one session; no organisational independence is established.
- Migration covers one historical shape; semantic equivalence stays `not_established`. A native test was not run.

## Status and what is open

- The late research synthesis gate is open.
- Independent semantic review of this text has not been performed.
- The English page is a summary, not a translation, and does not replace the Russian original.
- Not integrated and still missing: the NAV reports, the TIM reports, MM_OBLIGATIONS_20261030 together with the previous-stage report, the runs behind section 7 of the knowledge-admission amendment (MM_KA0004), and the items ING-01 to ING-08.
- The crosswalk content is a one-assistant self-check, not independent confirmation.
- Held inconsistencies: the edition says another team member composed the control set, the review says an agent of the same session (this page follows the review); the amendment speaks of seven profiles, the edition lists six.

## Relation to the full text

The Russian full text is the unchanged terminology edition of 2026-11-03. Its abstract understates executed results; this page follows the corrected wording from the editorial review. The Russian text is published without the card corrections, so its abstract may differ from this page.

## Credit and licence

Based on Knowledge Contract Arcana, <https://contract.place> (CC BY 4.0). Licence: [CC BY 4.0](../LICENSE). Credit lines and how to cite: [ATTRIBUTION.md](../ATTRIBUTION.md); rights holder statement for the repository: [NOTICE](../NOTICE); third-party sources: [SOURCES.md](../SOURCES.md).

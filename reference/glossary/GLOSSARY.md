---
name: "glossary"
title: "Knowledge Contract Glossary"
artifact: "glossary"
edition: "1.0"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "Shared English definitions, Russian equivalents, technical spellings and distinctions between related concepts."
---

# Knowledge Contract Glossary

**Publication edition:** 1.0 · **Maintainer:** Pavel Valentov

This glossary defines the preferred vocabulary shared by the scientific papers and engineering specifications. Human-readable terms use ordinary words. Code identifiers remain literal when an interface requires them. A Russian equivalent helps trace the earlier manuscripts; it does not create a second entity.

## Knowledge and its representation

| Preferred term | Russian equivalent | Definition and boundary |
| --- | --- | --- |
| Knowledge Contract | Контракт знаний | A versioned specification of knowledge, intended use, grounds, dependencies, constraints and assessment obligations. Its existence does not establish truth or authorize execution. |
| Semantic object | Смысловой объект | An addressable, versioned interpretation with content, attribution, context and grounds. A retrieval chunk is a representation for search and need not have the same boundaries. |
| Source | Источник | Material from which an interpretation or observation is derived. Source authorship, authenticity, fidelity and truth are separate questions. |
| Source representation | Представление источника | A particular version of text, image, table, audio or other material. |
| Source fragment | Фрагмент источника | A region addressed within a specified source representation. Its locator must state the relevant selection convention. |
| Interpretation | Интерпретация | A reading of material under stated assumptions. Several readings can remain possible. |
| Attribution | Атрибуция | An association between addressed content and the person or system that stated, interpreted or assessed it. |
| Provenance | Происхождение | The trace of entities, activities and responsible agents involved in producing a record. Traceability alone does not prove correctness. |
| Ground | Основание | A source, observation, rule or argument that supports a specified claim under declared assumptions. |
| Context | Контекст | Conditions needed to interpret or use content: referents, scope, representation, time, exceptions, recipient and other relevant circumstances. |
| Applicability | Применимость | Suitability of a particular interpretation or artifact for a named use under current or explicitly historical conditions. |
| Constraint | Ограничение | A rule or condition restricting admissible interpretation, transformation, delivery or action. It is an explicit contract obligation, not a synonym for an acceptance criterion. |
| Protected property | Сохраняемое свойство | A specified observation or relation that a transformation is required to preserve. |
| Projection | Проекция | A selected representation for a purpose, with included and omitted units, transformation rules and losses made explicit. |
| Loss | Потеря | Information or distinctions not preserved by a transformation within a declared observation model. |

## Requirements, work and agency

| Preferred term | Russian equivalent | Definition and boundary |
| --- | --- | --- |
| Work Item | Единица работы | One goal-bearing unit with versioned requirements, constraints, assignments, attempts and acceptance criteria. `WorkItem` is the code spelling of this same concept, not another type. |
| Requirement | Требование | A condition the requested result or process must satisfy in a specified revision and scope. |
| Acceptance criterion | Критерий приёмки | A rule for deciding whether an observed result satisfies a named requirement. It must bind to the actual output and attempt. |
| Role | Роль | A named responsibility and decision scope. A role definition is distinct from an assignment to an executor. |
| Skill | Навык | A reusable description of a method or procedure and the conditions for using it. A `SKILL.md` file supplies instructions, not evidence that its reader can perform them. |
| Competency | Компетенция | A specified or assessed ability to achieve a class of results under stated conditions. A competency definition and evidence about a particular executor remain distinct records. |
| Capability | Способность исполнителя | The ability available to an identified executor in an actual environment, established to the degree supported by its assessment. |
| Blueprint | Схема решения | A reusable process or structural arrangement for achieving a result. It connects components, steps, dependencies, choices, constraints and acceptance obligations. |
| Assignment | Назначение | A binding of an executor to a responsibility or Work Item under a specified scope. |
| Authority | Полномочие | The legitimate scope of decisions or actions supplied by an identified authorization basis. |
| Grant | Разрешение | A concrete authorization with subject, action, resource, purpose, conditions and validity scope. |
| Attempt | Попытка исполнения | One addressed execution attempt bound to a Work Item, requirements, contract, actor and inputs. |
| Outcome | Исход | The result of an operation under its declared contract: success, partial, refused, failed or unresolved. |
| Effect observation | Наблюдение эффекта | What is established about an external change caused by an attempt. A timeout can leave this unknown. |

## Retrieval, composition and reuse

| Preferred term | Russian equivalent | Definition and boundary |
| --- | --- | --- |
| Candidate | Кандидат | A potentially useful retrieved item awaiting the checks needed for a particular use. |
| Coverage | Покрытие требований | Established support for the required slots of a named request at a named stage. Presence of a keyword is not semantic fulfilment. |
| Search assurance | Полнота процедуры поиска | A statement about the search procedure within its declared scope, separate from coverage of the selected answer. |
| Mandatory dependency | Обязательная зависимость | A relation requiring another pinned unit or condition for the specified use. |
| Dependency closure | Замыкание зависимостей | The least set containing selected roots and all their active mandatory dependencies within the declared graph. It cannot recover unrecorded edges. |
| Context package | Пакет контекста | Versioned selected knowledge with requirements, grounds, dependency closure, coverage, projection and resource account for a particular use. |
| Compiled artifact | Скомпилированный артефакт | A saved derivative of an extraction, selection, transformation or composition, with its producing recipe and dependencies. |
| Build recipe | Рецепт сборки | The declared inputs, transformation versions, parameters and material environment used to produce an artifact. |
| Content identity | Идентичность содержимого | Equality of exact bytes or canonical values within a declared hash domain. |
| Lookup identity | Ключ поиска кандидата | A descriptor used to find a reusable candidate. Matching it does not establish eligibility. |
| Admission | Допуск к применению | A decision that specified requirements and constraints permit a particular use under an identified policy and trust boundary. |
| Freshness | Актуальность по времени | Satisfaction of a specified temporal policy, distinct from semantic applicability and authorization. |
| Retention | Срок хранения | A storage policy for preserving bytes, distinct from how long their use remains valid. |
| Invalidation | Пересмотр пригодности | A change that requires eligibility or a derived state to be withdrawn or reconsidered. It need not delete the historical bytes. |
| Serve boundary | Момент фактической выдачи | The declared consistency point at which a selected result is actually released to a recipient. |
| Knowledge utility | Полезность знания | Task-, policy- and horizon-dependent benefit relative to a stated baseline and cost model. It is not an intrinsic scalar property of a document. |

## Evidence, versions and review

| Preferred term | Russian equivalent | Definition and boundary |
| --- | --- | --- |
| Evidence | Свидетельство | An addressed observation or record supporting a specified claim under a method and trust boundary. An assertion that a test passed is weaker than inspectable test outputs. |
| Assessment | Оценка | A method-bound judgment about a particular subject revision and property. |
| Counterexample | Контрпример | A case violating the conclusion of a stated claim while satisfying its relevant premises, or exposing that a needed premise was omitted. |
| Conformance | Соответствие спецификации | Satisfaction of specified structural or behavioral requirements in a declared scope. It does not establish every empirical benefit claimed for a system. |
| Reproduction | Воспроизведение | Running an available procedure again on its stated inputs and comparing outputs under declared criteria. Inspecting a retained report is not a rerun. |
| Replication | Независимое повторение | A separately conducted evaluation of a claim with its own implementation or observations. Independence must be described, not inferred from a different filename or agent role. |
| Revision | Редакция объекта | An immutable identified content state. |
| Edition | Издание корпуса документов | A coherent version of publications and their reading manifest. It is independent of a runtime protocol or service version. |
| Representation profile | Профиль представления | A versioned encoding and interpretation convention for a kind of artifact. |
| Current head | Текущая выбранная редакция | A mutable selection within an identified namespace and policy. A historical current marker does not prove present currency. |
| Adoption decision | Решение о принятии | A governance act accepting a norm or publication within an authority's scope. It is not a truth predicate. |
| Internal agent review | Внутренняя агентная рецензия | A recorded assessment by an agent, with its actual input, method and limitations. It is not independent external peer review. |
| Unknown | Не установлено | The available observations do not establish a value or verdict. It cannot be replaced with false, absent or pass without a justified rule. |
| Withheld | Не раскрывается | A value is not disclosed under a restriction. This does not assert that the value is absent. |

## Editorial rules for terminology

Use **Work Item** in English prose and `WorkItem` only for a literal identifier. Use “skill,” “competency,” “capability,” “role,” and “authority” only with the distinctions above. “Validated,” “verified,” “complete,” “current” and “independent” require an explicit subject and scope. Introduce an abbreviation only if repeated use saves meaningful reading effort.

The [artifact registry](../../engineering/specifications/artifact-registry/SPECIFICATION.md) defines file formats. The [status specification](../../engineering/specifications/status-model/SPECIFICATION.md) defines operational values. The [source map](../../appendices/source-map/APPENDIX.md) retains older names and identifiers solely for traceability.

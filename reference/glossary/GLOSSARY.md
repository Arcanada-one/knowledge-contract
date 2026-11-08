---
name: "glossary"
title: "Shared Vocabulary: Knowledge Contract Glossary"
short_title: "Shared Vocabulary"
subtitle: "Knowledge Contract Glossary"
previous_title: "Knowledge Contract Glossary"
artifact: "glossary"
edition: "1.1"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "Shared English definitions, Russian and Simplified Chinese equivalents, technical spellings and distinctions between related concepts."
---

<!-- markdownlint-disable-next-line MD033 -->
<a id="knowledge-contract-glossary"></a>

# Shared Vocabulary: Knowledge Contract Glossary

**Publication edition:** 1.1 · **Maintainer:** Pavel Valentov

This glossary defines the preferred vocabulary shared by the scientific papers, engineering specifications and engineering studies. Human-readable terms use ordinary words. Code identifiers remain literal when an interface requires them. Russian and Simplified Chinese (zh-Hans) equivalents identify the same defined concept, not additional entities. English remains the canonical definition language; the equivalents are project terminology, not a claim of international standardization or independent linguistic certification. Definitions describe an obligation or an observation; their presence in this glossary is not evidence that a particular implementation satisfies them.

## Knowledge and its representation

| Preferred term | Russian equivalent | Chinese equivalent (zh-Hans) | Definition and boundary |
| --- | --- | --- | --- |
| Knowledge Contract | Контракт знаний | 知识契约 | A versioned specification of knowledge, intended use, grounds, dependencies, constraints and assessment obligations. Its existence does not establish truth or authorize execution. |
| Semantic object | Смысловой объект | 语义对象 | An addressable, versioned interpretation with content, attribution, context and grounds. A retrieval chunk is a representation for search and need not have the same boundaries. |
| Source | Источник | 来源 | Material from which an interpretation or observation is derived. Source authorship, authenticity, fidelity and truth are separate questions. |
| Source representation | Представление источника | 来源表示 | A particular version of text, image, table, audio or other material. |
| Source fragment | Фрагмент источника | 来源片段 | A region addressed within a specified source representation. Its locator must state the relevant selection convention. |
| Interpretation | Интерпретация | 解释 | A reading of material under stated assumptions. Several readings can remain possible. |
| Attribution | Атрибуция | 归属标注 | An association between addressed content and the person or system that stated, interpreted or assessed it. |
| Provenance | Происхождение | 溯源 | The trace of entities, activities and responsible agents involved in producing a record. Traceability alone does not prove correctness. |
| Ground | Основание | 依据 | A source, observation, rule or argument that supports a specified claim under declared assumptions. |
| Context | Контекст | 上下文 | Conditions needed to interpret or use content: referents, scope, representation, time, exceptions, recipient and other relevant circumstances. |
| Applicability | Применимость | 适用性 | Suitability of a particular interpretation or artifact for a named use under current or explicitly historical conditions. |
| Constraint | Ограничение | 约束 | A rule or condition restricting admissible interpretation, transformation, delivery or action. It is an explicit contract obligation, not a synonym for an acceptance criterion. |
| Protected property | Сохраняемое свойство | 受保护性质 | A specified observation or relation that a transformation is required to preserve. |
| Projection | Проекция | 投影 | A selected representation for a purpose, with included and omitted units, transformation rules and losses made explicit. |
| Loss | Потеря | 损失 | Information or distinctions not preserved by a transformation within a declared observation model. |
| Uncertainty field | Поле неопределённости | 不确定性字段 | An explicit record of an unresolved reading, qualification or confidence limitation. Omitting the field from a delivered projection can remove information even when the source record retains it. |
| Generated and unreviewed | Сгенерировано, не проверено | 已生成且未经审查 | Two separate facts: a system produced content, and no qualifying review is established. A generated description is not an author statement; a later review must identify its subject and scope. Historical code may combine the two labels as `generated/unreviewed`. |

## Requirements, work and agency

| Preferred term | Russian equivalent | Chinese equivalent (zh-Hans) | Definition and boundary |
| --- | --- | --- | --- |
| Work Item | Единица работы | 工作项 | One goal-bearing unit with versioned requirements, constraints, assignments, attempts and acceptance criteria. `WorkItem` is the code spelling of this same concept, not another type. |
| Requirement | Требование | 要求 | A condition the requested result or process must satisfy in a specified revision and scope. |
| Acceptance criterion | Критерий приёмки | 验收标准 | A rule for deciding whether an observed result satisfies a named requirement. It must bind to the actual output and attempt. |
| Role | Роль | 角色 | A named responsibility and decision scope. A role definition is distinct from an assignment to an executor. |
| Skill | Навык | 技能 | A reusable description of a method or procedure and the conditions for using it. A `SKILL.md` file supplies instructions, not evidence that its reader can perform them. |
| Competency | Компетенция | 胜任能力 | A specified or assessed ability to achieve a class of results under stated conditions. A competency definition and evidence about a particular executor remain distinct records. |
| Capability | Способность исполнителя | 执行者能力 | The ability available to an identified executor in an actual environment, established to the degree supported by its assessment. |
| Blueprint | Схема решения | 方案蓝图 | A reusable process or structural arrangement for achieving a result. It connects components, steps, dependencies, choices, constraints and acceptance obligations. |
| Assignment | Назначение | 指派 | A binding of an executor to a responsibility or Work Item under a specified scope. |
| Authority | Полномочие | 权限 | The legitimate scope of decisions or actions supplied by an identified authorization basis. |
| Grant | Разрешение | 具体授权 | A concrete authorization with subject, action, resource, purpose, conditions and validity scope. |
| Attempt | Попытка исполнения | 执行尝试 | One addressed execution attempt bound to a Work Item, requirements, contract, actor and inputs. |
| Outcome | Исход | 结果状态 | The result of an operation under its declared contract: success, partial, refused, failed or unresolved. |
| Effect observation | Наблюдение эффекта | 效果观察 | What is established about an external change caused by an attempt. A timeout can leave this unknown. |
| Ready | Готово к выдаче | 就绪 | Availability or lifecycle readiness under a named profile. It is not an operation outcome and does not replace `success`, `partial`, `refused`, `failed` or `unresolved`. A ready informational result need not authorize execution. |
| Core and profile | Ядро и профиль | 核心与配置 | The core supplies common obligations; a profile adds a named, versioned set of representation or use conditions. A profile must not cancel a mandatory core condition. |
| Required profile | Обязательный профиль | 必需配置 | A profile whose interpretation is necessary for the intended use, including any profile carrying a mandatory constraint. An unknown required profile blocks that use. |
| Optional and opaque profile | Необязательный и непрозрачный профиль | 可选与不透明配置 | An optional profile may be preserved without interpretation only when no mandatory obligation depends on it. Opaque means its meaning is not interpreted; byte preservation is not conformance to its semantics. |

## Retrieval, composition and reuse

| Preferred term | Russian equivalent | Chinese equivalent (zh-Hans) | Definition and boundary |
| --- | --- | --- | --- |
| Candidate | Кандидат | 候选项 | A potentially useful retrieved item awaiting the checks needed for a particular use. |
| Coverage | Покрытие требований | 覆盖 | Established support for the required slots of a named request at a named stage. Presence of a keyword is not semantic fulfilment. |
| Search assurance | Полнота процедуры поиска | 搜索保证 | A statement about the search procedure within its declared scope, separate from coverage of the selected answer. |
| Mandatory dependency | Обязательная зависимость | 强制依赖 | A relation requiring another pinned unit or condition for the specified use. |
| Dependency closure | Замыкание зависимостей | 依赖闭包 | The least set containing selected roots and all their active mandatory dependencies within the declared graph. It cannot recover unrecorded edges. |
| Context package | Пакет контекста | 上下文包 | Versioned selected knowledge with requirements, grounds, dependency closure, coverage, projection and resource account for a particular use. |
| Package and task package | Пакет и пакет задачи | 包与任务包 | A package is a declared collection with an inventory and identity. A task package additionally binds selected content to a request and its obligations. Neither name implies a complete dependency closure or a small size. |
| Document passport | Паспорт документа | 文档档案 | The historical package's metadata record identifying a document, representation, source and related conditions. It is not an identity document or an independent certificate of correctness. |
| Operational closure | Операционное замыкание | 操作闭包 | The dependencies and bindings required to use a package in a named operation: for example, roles, skills, rules, criteria, source references and authority. A graph closure is sufficient only when that graph records every relevant obligation. |
| Compiled artifact | Скомпилированный артефакт | 编译制品 | A saved derivative of an extraction, selection, transformation or composition, with its producing recipe and dependencies. |
| Build recipe | Рецепт сборки | 构建配方 | The declared inputs, transformation versions, parameters and material environment used to produce an artifact. |
| Content identity | Идентичность содержимого | 内容身份 | Identity within a declared representation and hash domain. The current `sha256/raw-utf8-json-v1` exchange profile hashes exact UTF-8 JSON bytes; it does not promise equality for differently serialized values. |
| Lookup identity | Ключ поиска кандидата | 查找身份 | A key derived from a declared candidate descriptor. Finding the same key does not establish equality of descriptors or eligibility. |
| Candidate descriptor | Описание кандидата для повторного использования | 候选项描述符 | The fields that an implementation compares after lookup: subject and representation identities, producing recipe and dependencies, relevant request scope and requirements, temporal mode, recipient and permission scope. The selected profile declares required fields and comparison rules; a title or hash alone is not this comparison. |
| Admission | Допуск к применению | 准入 | A decision that specified requirements and constraints permit a particular use under an identified policy and trust boundary. |
| Freshness | Актуальность по времени | 时效性 | Satisfaction of a specified temporal policy, distinct from semantic applicability and authorization. |
| Retention | Срок хранения | 保留策略 | A storage policy for preserving bytes, distinct from how long their use remains valid. |
| Residency | Наличие в хранилище | 驻留状态 | The observed presence or absence of identified bytes at a storage location: `resident`, `evicted`, `absent` or `unknown`. It says nothing by itself about their freshness, truth or permitted use. |
| Artifact lifecycle | Жизненный цикл артефакта | 制品生命周期 | The states and events of preparation, assessment, use, supersession, revocation and storage. Retention is its storage part, not a synonym for the whole lifecycle. |
| Invalidation | Пересмотр пригодности | 失效处理 | A change that requires eligibility or a derived state to be withdrawn or reconsidered. It need not delete the historical bytes. |
| Serve boundary | Момент фактической выдачи | 实际交付边界 | The declared consistency point at which a selected result is actually released to a recipient. |
| Knowledge utility | Полезность знания | 知识效用 | Task-, policy- and horizon-dependent benefit relative to a stated baseline and cost model. It is not an intrinsic scalar property of a document. |

## Evidence, versions and review

| Preferred term | Russian equivalent | Chinese equivalent (zh-Hans) | Definition and boundary |
| --- | --- | --- | --- |
| Evidence | Свидетельство | 证据 | An addressed observation or record supporting a specified claim under a method and trust boundary. An assertion that a test passed is weaker than inspectable test outputs. |
| Assessment | Оценка | 评估 | A method-bound judgment about a particular subject revision and property. |
| Assessment result | Результат оценки | 评估结果 | `pass`, `fail`, `unknown` or `not_applicable` for one property in a defined scope. `not_applicable` discharges a mandatory condition only with an identified rule and justified applicability witness; it is not a substitute for unavailable evidence. |
| Trusted input | Доверенный вход | 可信输入 | A value accepted as a premise within a declared evaluation. Structural consistency of that value does not authenticate its external origin or truth. |
| Trust boundary | Граница доверия | 信任边界 | The point at which a source, actor or process is accepted for a stated kind of evidence or authority. A test must identify which inputs it checks and which it assumes. |
| Counterexample | Контрпример | 反例 | A case violating the conclusion of a stated claim while satisfying its relevant premises, or exposing that a needed premise was omitted. |
| Conformance | Соответствие спецификации | 符合性 | Satisfaction of specified structural or behavioral requirements in a declared scope. It does not establish every empirical benefit claimed for a system. |
| Reproduction | Воспроизведение | 复现 | Running an available procedure again on its stated inputs and comparing outputs under declared criteria. Inspecting a retained report is not a rerun. |
| Demonstration or illustration | Демонстрация или иллюстрация | 演示或示例 | An example constructed to expose a mechanism or counterexample. Re-running that example reproduces its own computation, not a historical experiment on different inputs. |
| Replication | Независимое повторение | 独立重复 | A separately conducted evaluation of a claim with its own implementation or observations. Independence must be described, not inferred from a different filename or agent role. |
| Qualification | Квалификация процедуры | 程序合格性确认 | Evidence that an identified implementation meets a declared finite acceptance procedure. Development and regression controls can qualify a bounded release; they do not establish performance on held-out data or general competence. |
| Preregistration | Предварительная фиксация протокола | 预先登记 | Recording intended inputs, criteria and analysis before the outcomes being evaluated are disclosed. A local timestamped plan is distinct from a publicly registered protocol; neither prevents all deviations or bias. |
| Masked review | Рецензирование с замаскированными условиями | 掩蔽条件审查 | Assessment using labels that hide the condition assignment from the assessor. The text can still reveal clues; masking neither proves blindness nor makes an agent judge independent or calibrated. |
| Positive control | Положительный контроль | 阳性对照 | A case designed to meet the admitted or successful condition, so an always-reject implementation cannot pass the suite. Its representativeness must be justified separately. |
| Stress or boundary case | Нагрузочный пример или проверка границы | 压力或边界用例 | A deliberately adverse case probing the limits of the model or its trusted premises. An expected false-input acceptance is reported as a boundary failure, separately from ordinary conformance counts. |
| Regression control | Регрессионная проверка | 回归控制 | A previously known case rerun after a change to detect a return of the tested defect. It is not an unseen challenge or a new independent observation. |
| Mutation check | Мутационная проверка | 变异检查 | Deliberately altering an implementation and checking whether the suite distinguishes the altered behavior. The declared mutants and any equivalent mutants bound the conclusion; killing a few mutants is not proof of general correctness. |
| Revision | Редакция объекта | 修订版 | An immutable identified content state. |
| Edition | Издание корпуса документов | 出版版本 | A coherent version of publications and their reading manifest. It is independent of a runtime protocol or service version. |
| Representation profile | Профиль представления | 表示配置 | A versioned encoding and interpretation convention for a kind of artifact. |
| Current head | Текущая выбранная редакция | 当前选定修订版 | A mutable selection within an identified namespace and policy. A historical current marker does not prove present currency. |
| Adoption decision | Решение о принятии | 采纳决定 | A governance act accepting a norm or publication within an authority's scope. It is not a truth predicate. |
| Internal agent review | Внутренняя агентная рецензия | 内部代理审查 | A recorded assessment by an agent, with its actual input, method and limitations. It is not independent external peer review. |
| Unknown | Не установлено | 未知 | The available observations do not establish a value or verdict. It cannot be replaced with false, absent or pass without a justified rule. |
| Withheld | Не раскрывается | 不予披露 | A value is not disclosed under a restriction. This does not assert that the value is absent. |

## Scoped mathematical notation

Symbols are local to the model named in each document. A shared letter does not identify a shared quantity. The following crosswalk prevents the earlier cost notation from being mistaken for the scientific utility model.

| Symbol | Scope and meaning | Cross-document boundary |
| --- | --- | --- |
| \(R(q)\) | Semantic-object and reuse papers: mandatory conditions of request \(q\) | Each condition requires a passed assessment or a justified non-applicability witness; no silent exclusion of unknown conditions |
| \(\mathrm{Roots}\) | Dependency-closure model: initially selected vertices | Distinct from \(R(q)\) and from a monetary reuse cost |
| \(h\) | Knowledge-utility paper: accounting or decision horizon | The retained reuse study used `h` for hit fraction; current explanatory text uses \(\rho\) for that fraction |
| \(V(k\mid\cdots)\), \(V_{\mathrm{set}}(S)\) | Utility paper and context-composition paper: task-conditioned or set value | The retained reuse program's `V` means validation cost, now written \(c_v\) in the study |
| \(N,G,B\) | Utility paper and reuse study: request count, cold admissible-path cost, preparation cost | Comparable only under the same horizon, quality requirements and cost boundary |
| \(c_{\mathrm{hit}}\) | Utility paper: complete cost of an admitted hit | Equals \(c_v+c_r\) in the study only for the stated all-hit simplified case, with no additional rebuilding, invalidation or storage cost |
| \(c_v,c_r,\rho\) | Reuse study: per-request validation, additional admitted-hit cost, usable-hit fraction | Historical data and code preserve their original keys `V`, `R`, `h`; new calculations state the mapping |
| \(F(N)\) | Reuse study: overhead over the accounting horizon | The closed fixed-cost break-even formula applies only when \(F\) and the other relevant parameters are independent of \(N\) |
| \(\rho(x)\) | Constrained-transformation paper: residual information retained for reconstruction | A function of an artifact; unrelated to the reuse study's scalar hit fraction |

## Editorial rules for terminology

Use **Work Item** in English prose and `WorkItem` only for a literal identifier. Use “skill,” “competency,” “capability,” “role,” and “authority” only with the distinctions above. “Validated,” “verified,” “complete,” “current” and “independent” require an explicit subject and scope. Introduce an abbreviation only if repeated use saves meaningful reading effort.

Quoted historical labels such as “independent review” remain unchanged in evidence. In the studies discussed here, the label often means a separately assigned agent within the same session or agent family, not independent external peer review. Current summaries state that actual scope. “Exact” identifies the compared bytes or observation; “all” identifies its finite denominator. Retained development, regression, stress and ordinary cases remain separate even when a historical summary combined them.

The [artifact registry](../../engineering/specifications/artifact-registry/SPECIFICATION.md) defines file formats. The [status specification](../../engineering/specifications/status-model/SPECIFICATION.md) defines operational values. The [source map](../../appendices/source-map/APPENDIX.md) retains older names and identifiers solely for traceability.

## Multilingual terminology policy

The three labels in each row refer to one concept under the English definition and its stated boundary. Translations retain negations, quantifiers, conditions, numerical values, formulas, requirement IDs, literal interface values and uncertainty. A translation or a short title is not a new scientific result, a conformance finding or an authorization. Quote historical wording faithfully and explain a changed preferred term outside the quotation.

Use the preferred Chinese label when introducing a technical term, with the English label in parentheses where ambiguity is possible. An established contextual alias may be used in running prose or a concise title only when the following distinctions remain explicit. This is a project-specific usage decision, not a claim that other disciplines use these words identically.

| Term or contrast | Chinese usage | Boundary to preserve |
| --- | --- | --- |
| Context; Context package | 上下文; 上下文包. 语境 and 语境包 are contextual aliases in meaning-oriented prose and existing short titles. | The alias does not create a second type or remove time, recipient, permission, representation or exception conditions. Use the same concept consistently within a document. |
| Authority; authorization basis; Grant | 权限; 授权依据; 具体授权 | Authority is the legitimate scope, not the basis that supplies it. The earlier draft label 权限依据 conflated those two notions; it is not the preferred label for Authority. A grant is a concrete authorization, not evidence that an action occurred. |
| Evidence; proof; Ground | 证据; 证明; 依据 | Evidence is an addressed record under a method; a proof is an argument under premises; a ground may be a source, observation, rule or argument. Do not translate every occurrence of evidence as proof. |
| Skill; Competency; Capability | 技能; 胜任能力; 执行者能力 | A reusable instruction, an ability specification or assessment, and an identified executor's actual ability are distinct. A skill file does not establish capability. |
| Coverage; Search assurance | 覆盖, expanded as 需求覆盖 when discussing requirements; 搜索保证 | Coverage concerns the selected answer's required slots. Search assurance describes the procedure within its declared scope, not universal completeness of retrieval. |
| Profile | 配置, expanded as 规范配置 when needed; 表示配置 for Representation profile | A profile is a named, versioned set of representation or use conditions, not merely mutable program settings. Required and optional profiles retain their different obligations. |
| Reproduction; Replication; Internal agent review | 复现; 独立重复; 内部代理审查 | Re-running the stated procedure is not an independent evaluation. A different agent role alone does not establish independence or external peer review. |
| Revision; Edition; Current head | 修订版; 出版版本; 当前选定修订版 | Immutable content identity, a coherent corpus edition and a mutable selected head are different objects. |
| Unknown; Withheld; absent | 未知; 不予披露; 不存在 | Lack of evidence, restricted disclosure and established absence are different statements. Neither unknown nor withheld may silently become absent, false or pass. |
| Ready; success; Admission | 就绪; 成功; 准入 | Lifecycle availability, an operation outcome and a scoped admission decision are separate. None implies an execution grant. |

Literal code identifiers and wire values remain unchanged: for example, `WorkItem`, `SKILL.md`, `generated/unreviewed`, `not_applicable`, `NOT_MEASURED` and `sha256/raw-utf8-json-v1`. Chinese explanations accompany them; they do not replace them inside code, schemas, receipts or evidence.

The [bounded foundations terminology supplement](../foundations/README.md#bounded-terminology-supplement) supplies Chinese equivalents for its seven additional local terms and links to their actual definitions. The [naming canon](../document-naming/NAMING.md) and [publication name register](../../DOCUMENTS.md) govern concise titles; a title alias does not override this glossary's technical definition.

Existing source-pinned translations and historical reviews remain bound to their original revisions. Aligning a draft rendition with this terminology requires an identified change and renewed review of the changed scope; do not silently repin an entire translation or transfer an earlier review to new bytes. Repository links are checked separately from the later site's locale routing, rendering, deployment and indexing.

---
title: "Check Names: Readable Verification Packages and Scenarios"
sources: ["Knowledge Contract project corpus and publication edition"]
status: reader-facing naming register; not a new test result
updated: 2026-11-09
---

# Check Names: Readable Verification Packages and Scenarios

[Clear Names](NAMING.md) · [Reading guide](../../READING.md) · [Research roadmap](../../ROADMAP.md)

This register supplies human-readable names for the existing verification specification. It does not create a new scientific paper, change any expected result or rename machine identifiers. The original [assessed-coverage specification](https://github.com/Arcanada-one/arcanada-workspace/pull/1886#issuecomment-6734249466) defines the exact premises and variants; [Knowledge Checks implementation proposal](https://github.com/Arcanada-one/knowledge-contract/pull/82) is a separate subject. The source specification describes 22 prepared finite scenario groups and six native integration groups. These numbers are not claims that 22 or six production tests passed.

## Knowledge Checks: Mandatory Requirements and Evidence Assessment

**Russian:** Проверки знаний: Обязательные требования и оценка свидетельств.

**Simplified Chinese:** 知识检验：强制要求与证据评估。

This package asks whether every mandatory requirement is satisfied by its entire declared checking rule or a properly justified exemption. Addressing a requirement is not discharging it. One observation can support several requirements through separate valid assessments, while a single requirement can need several independent observations. The finite package does not grant permission to execute an action.

| English scenario | Russian | Simplified Chinese | Technical locator | Boundary checked |
| --- | --- | --- | --- | --- |
| Complete Requirements | Полные требования | 完整要求 | `S01` | A complete, consistently bound positive case passes; effects remain unauthorized. |
| Missing Assessment | Недостающая оценка | 缺失评估 | `S02` | Missing assessment of one required member is unknown, not success of the whole set. |
| Joint Evidence | Совместные свидетельства | 联合证据 | `S03` | A conjunction remains incomplete when one necessary component is absent. |
| Shared Evidence | Общее свидетельство | 共享证据 | `S04` | One observation may satisfy two requirements through separately checked entailments when independent origins are not required. |
| Unsupported Reuse | Неподтверждённое использование | 无依据复用 | `S05` | Copying an evidence reference does not establish another requirement's assessment. |
| Duplicate Aliases | Повторные псевдонимы | 重复别名 | `S06` | Aliases of one member cannot replace another mandatory member. |
| Required Profile | Обязательный профиль | 必需配置 | `S07` | A producer cannot mark a required, unsupported constraint profile optional. |
| Unknown Requirements | Неизвестные требования | 未知要求 | `S08` | Missing requirements or an unjustified caller-supplied empty list remain unknown. |
| Justified Emptiness | Обоснованная пустота | 有据空集 | `S09` | A trusted, justified empty set may pass its exact informational scope without granting action authority. |
| Required Dependencies | Обязательные зависимости | 强制依赖 | `S10` | A required dependency omitted from the submitted list remains unresolved. |
| Conflicting Requirements | Противоречивые требования | 冲突要求 | `S11` | Established inconsistency of mandatory predicates is failure, not a last-write-wins choice. |
| Exact Binding | Точная привязка | 精确绑定 | `S12` | Wrong revision, actor, resource, environment, recipient or payload invalidates the reused assessment. |
| Current Validity | Текущая пригодность | 当前有效性 | `S13` | Revoked use or an expired validity interval fails current use without rewriting historical scientific assessment. |
| Access Distinctions | Недоступность и запрет | 不可用与拒绝 | `S14` | Unavailable evidence gives unknown; an authoritative denial gives failure. |
| Verified Provenance | Проверенное происхождение | 已验证溯源 | `S15` | Caller assertions of trust do not authenticate evidence; proven invalidity differs from missing verification. |
| Justified Exemption | Обоснованное исключение | 有据豁免 | `S16` | A valid, evidenced exemption retains the member and its justification. |
| Unsupported Exemption | Неподтверждённое исключение | 无据豁免 | `S17` | Missing exemption authority/evidence is unknown; a proven scope mismatch is failure. |
| Identity Conflict | Конфликт идентичности | 身份冲突 | `S18` | One qualified identity with conflicting immutable contents is a conflict, not a deduplication choice. |
| Coherent Support | Согласованная поддержка | 一致支持 | `S19` | Supports from incompatible historical states cannot be combined into a single current assessment. |
| Irrelevant Evidence | Несущественные свидетельства | 无关证据 | `S20` | Verified irrelevant optional evidence leaves the valid positive case unchanged. |
| New Conflict | Новое противоречие | 新增冲突 | `S21` | A new relevant conflict requires reassessment; adding arbitrary evidence is not unconditionally monotone. |
| Independent Origins | Независимые источники | 独立来源 | `S22` | Copies and translations of one origin are not independent origins when the rule requires independence. |

The original parameterized cases distinguish definite failure from unknown information. Each concrete fixture still needs one exact expected verdict and reasons fixed before execution. The concise descriptions above do not replace those premises or permit a runner to choose a result after observing it.

## Execution Checks: Authorization, Budget and Result Integrity

**Russian:** Проверки исполнения: Полномочия, бюджет и целостность результата.

**Simplified Chinese:** 执行检验：授权、预算与结果完整性。

These checks concern actual integrated execution, not the finite synthetic model. They require genuine source admission, authority, reservations, physical-send observations and retained results. No native pass is asserted by this naming register.

| English scenario | Russian | Simplified Chinese | Technical locator | Required boundary |
| --- | --- | --- | --- | --- |
| Action Authority | Полномочие действия | 行动权限 | `N01` | No current action authority means refusal and zero physical sends. |
| Funded Budget | Обеспеченный бюджет | 已落实预算 | `N02` | Missing, insufficient or unknown real reservation cannot permit dispatch. |
| Authorized Execution | Разрешённое исполнение | 获准执行 | `N03` | A useful positive has one authorized bound send and retained accounting/result evidence. |
| Current Permission | Действующее разрешение | 当前许可 | `N04` | Changes and revocation during waits must respect the accepted current-use and serialization rules. |
| Unknown Outcome | Неизвестный исход | 未知结果 | `N05` | An ambiguous outcome preserves original identity and hold; no invented second attempt or assumed release. |
| Authorized Replay | Разрешённое повторное чтение | 获准重读 | `N06` | Current read entitlement and separately established result integrity govern disclosure without a new call or charge. |

## Current communication rule

Write: “The specification **Knowledge Checks: Mandatory Requirements and Evidence Assessment**, containing 22 finite scenario groups, received a scoped semantic review. Implementation and execution evidence are reported separately.” Use this sentence only when the referenced review actually supports it.

Do not write: “S01–S22 is released”, “the N layer is complete”, or “all checks passed” when only a specification was reviewed. In Russian reports, use **Проверки знаний** and **Проверки исполнения** first. A technical range may follow only when a reader needs exact traceability.

Links to prior comments and fixtures keep their existing addresses. New display names are aliases of those same subjects, not replacements for historical identities or a second task system. The English, Russian and Chinese labels here are author-maintained presentation wording, not a native-speaker certificate or full translated specification.

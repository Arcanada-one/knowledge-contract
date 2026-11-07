---
name: "status-model"
title: "评估、执行与发布状态"
artifact: "engineering-specification"
edition: "1.1"
author: "Pavel Valentov"
language: "zh-Hans"
license: "CC-BY-4.0"
description: "彼此独立的评估、执行、效果、时效性、发布和审查状态。"
translation_of: "engineering/specifications/status-model/SPECIFICATION.md"
source_commit: "a0450428704fcd41b411203f2fc88c06c779610b"
source_git_blob: "4d3f405149c10b7e2bee6988c575bd82cae28b8b"
translation_status: "author-draft"
---

# 评估、执行与发布状态 {#assessment-execution-and-publication-states}

**作者：**Pavel Valentov · **出版版本：**1.1

## 1. 目的与符合性 {#1-purpose-and-conformance}

本文是一组架构要求。互操作性需要具名的表示配置；已实现的交换子集仅限于[观察、变更事件和配置通告](../status-model/SPECIFICATION.md#8-bounded-exchange-profile)，而[书籍包配置](../book-package/SPECIFICATION.md)具有自己的模式。这并不意味着已有完整契约的传输格式或已部署的运行时。

状态只有针对具名的对象、性质、修订版和范围才有意义。单个“已验证”标志无法忠实表示模式有效性、来源保真度、真实性、覆盖、授权、执行结果和出版审查。本规范区分这些问题，并定义状态转换义务。

大写要求用语遵循 [BCP 14](../../../reference/bibliography/BIBLIOGRAPHY.md#requirement-language)。

**STA-R001.** 配置必须（MUST）选择其目的所需的维度，并声明任何聚合规则。

不需要给每条记录附加所有可能维度。[证据论文](../../../papers/evidence-and-falsification/PAPER.md)解释为什么更强结论需要不同证据。

## 2. 观察记录 {#2-observation-record}

**STA-R002.** 每项观察必须（MUST）标识其对象和不可变修订版、评估性质、要求或标准修订版、方法、观察者、相关时间、结果、依据和限制。

没有对象的结果不是可转移的证据。

**STA-R003.** 如果方法信任提供的输入，而不是独立认证该输入，则必须（MUST）说明这一假设。

检查结果词汇为 `pass`、`fail`、`unknown` 和 `not_applicable`。最后一个值需要已经论证的不适用规则，而不是缺失数据。对于强制检查的合取集合，任何适用检查失败都会阻止接受；任何剩余的适用未知结果都会阻止“全部通过”的结论。

**STA-R004.** 一项肯定结果不得（MUST NOT）覆盖另一项必需性质的否定或未决结果。

## 3. 规范维度词汇 {#3-canonical-dimension-vocabularies}

**STA-R005.** 使用当前词元的配置必须（MUST）采用下列 snake_case 值，不得以一个维度承载另一维度的含义。

**STA-R006.** 旧配置只有通过明确且报告损失的适配器，才可以（MAY）保留其原始词法值。

| 维度 | 词元 |
| --- | --- |
| 信息可用性 | `known`, `unknown`, `not_applicable`, `withheld` |
| 覆盖 | `supported`, `partial`, `unsupported`, `conflicted`, `unknown` |
| 搜索保证 | `candidate_only`, `exhaustive_in_scope`, `incomplete_procedure` |
| 本地运行阶段 | `planned`, `ready`, `running`, `paused`, `finished` |
| 操作结果 | `success`, `partial`, `refused`, `failed`, `unresolved` |
| 停止原因 | `completed`, `clarification_needed`, `budget_insufficient`, `retrieval_limit`, `stale_evidence`, `precondition_not_met`, `cancelled`, `execution_error`, `reconciliation_pending` |
| 外部效果 | `none_established`, `known_effect`, `unknown_effect` |
| 制品生命周期 | `building`, `ready`, `quarantined`, `retired`, `failed` |
| 驻留状态 | `resident`, `evicted`, `absent`, `unknown` |
| 时效性 | `fresh`, `stale`, `expired`, `unknown` |
| 复用资格 | `eligible`, `ineligible`, `unknown` |
| 演化影响 | `compatible`, `restricted`, `requires_review`, `blocked`, `unknown_impact` |
| 复用决定 | `exact_reuse`, `revalidate`, `rebuild`, `instantiate`, `refuse`, `unresolved`, `serve_stale` |
| 用例证据 | `planned`, `illustrated`, `executed`, `evaluated` |
| 审查类别 | `editorial`, `internal_technical`, `independent_agent`, `external_peer` |

`unsupported` 始终指声明的已评估范围。`ready` 描述运行或制品可用性，不是成功操作结果。`none_established` 表示在观察范围内尚未确立任何效果，并不声称远程效果不存在。审查类别描述实际协议，而不是审查者的名称。另行指派代理进行的审查不是外部人工同行评审。

**STA-R007.** 历史标签必须（MUST）明确映射：`terminated` → 运行阶段 `finished`；`unsupported in scope` → 覆盖 `unsupported`；“incomplete execution of planned search” → `incomplete_procedure`；`not_measured` → 评估 `unknown`，原因为“no observation”。配置特定的质量状态，例如书籍包的 `reviewed`，保留其自身声明范围；它们不是 `pass` 的别名。

演化影响是准入的输入，而不是得到准入结论的捷径：

| 影响 | 使用资格和允许的下一项决定 |
| --- | --- |
| `compatible` | 在其他所有必需关卡通过前仍为 `unknown`；之后才具备政策允许的复用资格 |
| `restricted` | 原来的较宽请求不具备资格；另行标识的缩窄请求重新评估 |
| `requires_review` / `unknown_impact` | 资格未知；采用 `revalidate` 或 `unresolved`，尚无获准交付 |
| `blocked` | 不具备该用途的资格；采用 `refuse`，或对另外一个允许的重建或实例按其自身依据进行评估 |

## 4. 转换规则 {#4-transition-rules}

转换作用于同一个已识别尝试、生命周期实例、政策和用途范围。

**STA-R008.** 实现必须（MUST）遵循下列表格；未列出的转换被拒绝。

创建新的对象或尝试会开始一段新历史，而不是改变旧记录的含义。

**STA-R009.** 每次转换必须（MUST）记录触发观察、行动主体、先前状态和守卫检查结果。

### 执行阶段 {#execution-phase}

| 起始状态 | 事件和守卫条件 | 目标状态 | 是否终止状态？ |
| --- | --- | --- | --- |
| 尚无尝试 | 分配唯一尝试，并固定工作项和要求 | `planned` | 否 |
| `planned` | 确立派发所需的输入、能力和前置条件 | `ready` | 否 |
| `ready` | 在实际派发时重新检查当前权限和前置条件 | `running` | 否 |
| `running` | 按声明的暂停政策记录可恢复检查点 | `paused` | 否 |
| `paused` | 验证检查点、当前绑定和重新生效的派发守卫 | `running` | 否 |
| `planned` / `ready` | 在派发前取消、拒绝或失败；记录原因和实际效果观察 | `finished` | 是 |
| `running` / `paused` | 终止，并明确记录结果、原因和效果观察 | `finished` | 是 |

**STA-R010.** 已结束的尝试不得（MUST NOT）返回运行状态；重试应使用具有重复策略的新尝试。

后续核对向同一个历史尝试添加效果观察，而不假装发生了另一次执行。进程成功退出不能提供缺失的验收证据。

### 制品生命周期 {#artifact-lifecycle}

| 起始状态 | 事件和守卫条件 | 目标状态 | 是否终止状态？ |
| --- | --- | --- | --- |
| 尚无生命周期 | 分配构建记录 | `building` | 否 |
| `building` | 构建成功、必需检查和原子发布守卫全部通过 | `ready` | 否 |
| `building` | 构建失败；保留原因及任何明确标为部分结果的输出 | `failed` | 是 |
| `building` / `ready` | 获准的完整性、安全性或溯源调查暂停使用 | `quarantined` | 否 |
| `quarantined` | 原因解决、完成重新评估并通过当前发布守卫后，经授权解除隔离 | `ready` | 否 |
| `building` / `ready` / `quarantined` | 经授权撤回或取消，使本生命周期退役 | `retired` | 是 |

`quarantined` 表示调查具名问题期间暂停使用；只有政策授权的主体可以解除隔离。`retired` 表示此生命周期已撤回，不能再次就绪。`failed` 对于本次构建也是终止状态。替换或恢复会创建新的生命周期或采纳记录，并保留此前撤销和限制。相同字节不会抹去这些决定。

### 时效性与资格投影 {#freshness-and-eligibility-projections}

这些是不可变观察的投影，而不是对旧判断结果的编辑。

**STA-R011.** 新投影记录只有在保留此前显示所依据的观察时，才可以（MAY）替换当前显示。

| 维度：起始状态 | 触发条件与必需证据 | 目标状态 |
| --- | --- | --- |
| 时效性：任意 | 新的适用检查、有效时钟边界和当前政策确立新窗口 | `fresh` |
| 时效性：`fresh` | 达到软截止时间，但尚未超过任何硬截止时间 | `stale` |
| 时效性：`fresh` / `stale` | 达到硬截止时间或允许年龄界限 | `expired` |
| 时效性：任意 | 无法确立必需时间、政策或时序 | `unknown` |
| 资格：任意 | 该精确请求的每个当前强制关卡均已履行 | `eligible` |
| 资格：任意 | 一个已知强制限制未满足 | `ineligible` |
| 资格：任意 | 重要依赖、权限或评估变为未知 | `unknown` |

**STA-R012.** 过期或不具备资格的观察，不得（MUST NOT）仅因为另一条记录的时间戳更晚就被覆盖。

只有在当前政策下解决每个已知阻断原因，资格才可变为肯定。仅重新检查摘要不能刷新来源事件的年龄。[复用政策](../reuse-policy/SPECIFICATION.md)定义截止时间和决定语义。

驻留状态只随存储观察改变：存储并读回具名字节确立 `resident`；逐出回执确立 `evicted`；有界不存在检查确立 `absent`；缺少可信存储观察则为 `unknown`。

**STA-R013.** 这些转换本身不得（MUST NOT）改变真实性、审查、时效性或使用资格。

评估、覆盖、搜索保证、外部效果、审查和用例证据记录都是仅追加的观察。它们不会自动朝成功推进：没有新执行记录，示例不会成为已执行试验；未知效果只能由相关效果边界上的证据解决。冲突观察仍可寻址。单调增长的是观察历史、终止尝试和生命周期历史，以及不重复使用的[发布代次](../cache-identity-and-invalidation/SPECIFICATION.md#5-guarded-publication-and-serving)，而不是真实性或使用资格持续改善。

## 5. 科学与编辑状态 {#5-scientific-and-editorial-status}

完成的出版物可以陈述条件命题、报告有限结果，同时承认尚未回答的经验问题。出版版本号标识协调一致的文本，而不是所有未来应用的证明。

**STA-R014.** 词汇不得（MUST NOT）将“已发布”“已审查”“已实现”和“有效”视为同义。

**STA-R015.** 内部代理审查必须（MUST）标识审查者、输入修订版、方法和结论，并且必须（MUST）明确标注为内部代理审查。

它不构成独立的外部同行评审。有限测试报告需要实际输出；示例场景不是已执行测试。

**STA-R016.** 已执行但失败的试验仍是有用证据，必须（MUST）保留其否定结果。

## 6. 面向用户的投影 {#6-user-facing-projections}

**STA-R017.** 界面可以（MAY）概括这些维度，但概括必须（MUST）保留与用户决定有关的区别。

**STA-R018.** “已索引修订版 X”比不加限定的“当前”更精确。如果当前授权不在检查边界内，“对提供记录的检查已通过”不得（MUST NOT）变成“行动已获授权”。

**STA-R019.** 当用户决定是否重试时，超时后的未知效果必须（MUST）保持可见。

技术细节可以按需展开，但关键不确定性不能隐藏在肯定徽标之后。

## 7. 验收与证据 {#7-acceptance-and-evidence}

**STA-R020.** 测试必须（MUST）覆盖：模式通过但提供的依据为假、执行成功但结果标准未满足、运行结束但效果未知、制品仍驻留但已经撤销、正确的历史结果不具备当前任务资格，以及无法确立经验有效性的内部审查。

[符合性研究](../../studies/contract-profile-conformance/STUDY.md)展示可信输入前提为何重要。[编辑试点](../../studies/editorial-skill-pilot/STUDY.md)报告结构化条件和基线条件的观察评分相等。二者都不允许赋予一般有效性标签。观察与规则采纳之间的区别见[修订与治理](../../../papers/revision-and-governance/PAPER.md)。

## 8. 有界交换配置 {#8-bounded-exchange-profile}

[JSON Schema](../../../schemas/contract-observation.schema.json)、[验证器](../../../tools/check_contract_profile.py)、[示例](../../../schemas/fixtures/contract-observation/valid/)和[测试](../../../tools/test_contract_profile.py)定义具体交换子集：`kc-observation/1`、`kc-dependency-change/1` 和 `kc-profile-advertisement/1`。这是使用 [JSON](https://www.rfc-editor.org/rfc/rfc8259) 和 [JSON Schema 2020-12](https://json-schema.org/draft/2020-12/json-schema-core)的项目原创配置，而不是声称完整知识契约、执行器或 API 已实现互操作。

**STA-R021.** 交换记录必须（MUST）是单个严格的 UTF-8 JSON 对象，不含 BOM、任何深度上的重复成员名称、非有限数字词元或孤立 Unicode 代理项。

未知字段、配置和记录版本会被拒绝。

**STA-R022.** 用作代次或序列号的整数必须（MUST）处于 0 到 9,007,199,254,740,991 范围内。

时间戳字符串使用 UTC 秒格式 `YYYY-MM-DDTHH:MM:SSZ`，且必须具有有效日历日期；其他时钟模型需要其他配置。

| 记录 | 必需字段及含义 |
| --- | --- |
| `KCObservation/v1` | `observation_id`、`subject`、所评估的 `property`、固定的 `criterion`、方法 `id`/`version`、`observer`、`observed_at`、检查 `result`、文本 `scope`、`evidence_refs`、`trust_assumptions`、`limitations` |
| 对象、标准或证据引用 | `artifact_id`、不可变的 `revision`、`hash_domain`、精确的 `sha256` |
| `not_applicable` 观察 | 另需固定的 `inapplicability_rule`；存在此规则仅是结构证据，不是该规则适用的证明 |
| `KCDependencyChange/v1` | `event_id`、排序 `namespace`、`sequence`、`dependency_id`、旧／新代次和修订版、事件 `kind`、影响、观察者和时间；见缓存规范 |
| `KCProfileAdvertisement/v1` | `reader_id`、明确的 `read_profiles`、`write_profiles`、支持的 `hash_domains`；列表是能力声明，不是具体授权 |

**STA-R023.** 实现必须（MUST）在交换记录之前比较模式和配置支持情况。

**STA-R024.** 实现不得（MUST NOT）从对本子集的支持推断对整个契约族的支持。

范围字符串是精确的描述性绑定；自动判定两个范围字符串语义等价不属于本配置。

| 已登记哈希域 | 精确输入与相等性 |
| --- | --- |
| `sha256/raw-bytes-v1` | 对所引用文件的精确字节计算 SHA-256；不解码，不重写 |
| `sha256/raw-utf8-json-v1` | 对精确有效的交换 JSON 字节计算 SHA-256，包括空白；不进行规范化或 Unicode 归一化 |

**STA-R025.** 身份比较必须（MUST）同时包含哈希域和摘要。

对相等的 JSON 值重新序列化，可能改变字节身份，因此会创建新表示。

**STA-R026.** 本配置有意不定义值级规范 JSON 哈希；需要这种功能的配置必须（MUST）命名独立的程序和哈希域。

结构验证不认证观察者，不证明观察事实，也不准入行动。

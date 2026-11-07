---
name: "reuse-policy"
title: "复用政策：时间、授权与决策结果"
artifact: "engineering-specification"
edition: "1.1"
author: "Pavel Valentov"
language: "zh-Hans"
license: "CC-BY-4.0"
description: "时间模式、保守截止时间、授权、决策结果与保留边界。"
translation_of: "engineering/specifications/reuse-policy/SPECIFICATION.md"
source_commit: "a0450428704fcd41b411203f2fc88c06c779610b"
source_git_blob: "8bc1c4c0d7ca720dd2213411a2b2821eccbc446a"
translation_status: "author-draft"
---

# 复用政策：时间、授权与决策结果 {#reuse-policy-time-authorization-and-decision-outcomes}

**作者：**Pavel Valentov · **出版版本：**1.1

## 1. 目的与符合性 {#1-purpose-and-conformance}

本文是一组架构要求。互操作性需要具名的表示配置；已实现的交换子集仅限于[观察、变更事件和配置通告](../status-model/SPECIFICATION.md#8-bounded-exchange-profile)，而[书籍包配置](../book-package/SPECIFICATION.md)具有自己的模式。这并不意味着已有完整契约的传输格式或已部署的运行时。

**RUS-R014.** 复用政策决定保存的结果能否满足新请求、哪些内容必须（MUST）重新检查，以及适用哪些时间和权限约束。

它针对具体的制品、接收者、目的、要求修订版和观察时间起作用。

大写要求用语遵循 [BCP 14](../../../reference/bibliography/BIBLIOGRAPHY.md#requirement-language)。缓存命中只是候选项。[编译制品规范](../compiled-artifact-contract/SPECIFICATION.md)定义保存结果；[身份与失效处理](../cache-identity-and-invalidation/SPECIFICATION.md)定义其依赖和交付守卫。

## 2. 先准入，再判断时间 {#2-admission-before-timing}

**RUS-R001.** 在决定时效性之前，政策必须（MUST）确立与请求的语义兼容性、必需依赖的可用性、适用约束、当前披露授权以及任何行动特定授权。

新鲜但不适用的结果不具备使用资格。字节相同的对象不会继承另一个接收者的权限。

充分的现有授权在其范围内使用；本规范不要求在流水线每一步都向用户重复询问同一许可。但它要求检查授权仍然覆盖实际行动、对象和时间。

## 3. 时间模式 {#3-temporal-modes}

| 模式 | 承诺 | 持续存在的义务 |
| --- | --- | --- |
| 固定历史版本 | 将已识别的历史修订版明确描述为历史版本 | 当前披露授权及适用的硬性限制 |
| 当前 | 在交付边界上确立相关的当前来源和政策状态 | 按声明的一致性模型检查依赖、范围和权限 |
| 有界陈旧 | 在明确政策下允许指定的最大年龄 | 硬性限制、溯源、不确定性以及任何强制重新验证 |

**RUS-R002.** 服务可用性不得（MUST NOT）默默选择更弱的时间模式。

历史正确性不会授权披露已撤回或受限制记录。后台刷新本身不会使旧内容获得使用资格。

## 4. 时间模型与截止时间 {#4-time-model-and-deadlines}

**RUS-R003.** 政策必须（MUST）区分来源事件时间、来源观察时间、制品构建时间、检查时间、授权区间和存储时间。

更新摘要检查不会使旧事实变新。相关时钟及不确定性边界属于观察的一部分。

在有界区间模型中，检查发生于 `[checked.lower, checked.upper]` 内，请求时间位于 `[now.lower, now.upper]` 内。这里的检查是政策相关观察，不是一次存储触碰或无关摘要检查。

**RUS-R004.** 时间必须（MUST）使用同一声明时钟和单位。

**RUS-R005.** 边界和时长必须（MUST）有限；区间要求 lower ≤ upper，TTL 和允许的最大年龄要求非负值。

TTL 产生**软**截止时间 `checked.lower + ttl`，除非政策明确将此 TTL 分类为硬截止时间。

**RUS-R006.** 政策必须（MUST）标识每个截止时间的类别与依据。

有效硬截止时间是所有适用的有限硬截止时间的最小值，包括硬 TTL、授权到期和强制最大年龄边界。复用要求 `now.upper < effective_hard_deadline`；相等即关闭窗口。明确不存在任何硬限制，不等于限制未知，也不会免除其他关卡。

当 `now.upper >= soft_deadline` 时，软截止时间已到。此时新鲜度变为陈旧，并要求交付前执行 `revalidate`，除非请求明确允许有界陈旧交付。在有界陈旧模式下，保守年龄为 `now.upper - checked.lower`，仍以同一个政策相关检查为基准。`serve_stale` 要求年龄严格小于声明的最大年龄，没有硬到期或撤销，其他关卡全部履行，并记录刷新义务。

**RUS-R007.** 刷新失败不得（MUST NOT）重置任何一个截止时间。

**RUS-R008.** 无效区间（lower > upper）、确定在未来的检查（`checked.lower > now.upper`）、负时长、不兼容时钟或未知的强制边界，必须（MUST）产生 `unresolved`，不得进行获准交付。

**RUS-R009.** 当顺序本身是强制条件时，无法确立 `checked.upper <= now.lower` 的重叠区间也保持未决；实现不得（MUST NOT）根据点估计虚构时序。

这些区间规则不声称提供分布式因果顺序。

## 5. 决策结果 {#5-decision-outcomes}

以下词元是**复用决定**，与[状态模型](../status-model/SPECIFICATION.md#3-canonical-dimension-vocabularies)中的操作结果不同。

| 决定 | 必需行为 |
| --- | --- |
| `exact_reuse` | 仅在选定时间模式下，每项必需关卡及最终交付守卫均通过后交付 |
| `revalidate` | 获取当前观察；观察履行全部关卡之前，不进行获准交付 |
| `rebuild` | 按当前输入／规则生成新制品，并单独评估 |
| `instantiate` | 生成并评估带绑定参数的新模板实例 |
| `refuse` | 按允许的披露级别报告已知阻断条件 |
| `unresolved` | 报告缺失、无效或不能得出结论的强制观察；不得作为已准入内容交付 |
| `serve_stale` | 仅在明确的有界陈旧授权下交付，记录陈旧状态、界限、观察依据和刷新义务 |

**RUS-R010.** 陈旧回退不得（MUST NOT）隐藏已知语义无效、硬到期或撤销。

`serve_stale` 与 `revalidate` 不同：前者允许按声明的较弱时间承诺交付，后者不允许。选择重建或刷新计划，并不确立该计划已经成功完成。

## 6. 成本、保留与测量 {#6-cost-retention-and-measurement}

成本可以影响合格选项之间的选择，但不能为违反强制义务开脱。

**RUS-R011.** 效用估计必须（MUST）说明其任务、基线、时间范围、单位和纳入的成本。

**RUS-R012.** 构建、检索、验证、维护和集成成本不得（MUST NOT）重复计算。

计划节省在测量之前仍是估计。

保留是存储政策，而不是使用资格政策。受欢迎程度可以说明为何更久保留字节，却不会延长其依据的有效性。否定结果尤其需要明确语料范围和失效条件。

## 7. 验收与证据 {#7-acceptance-and-evidence}

必需用例包括：当前请求但来源当前版本证据不可用；披露权限撤销后的历史请求；未知时钟边界；恰好等于硬到期时间；软 TTL 与硬 TTL 的区别；无效和重叠时钟边界；从相关检查起算的有界年龄限制；明确允许及明确禁止的陈旧交付；刷新失败；权限改变的模板实例；以及违反强制约束的低成本选项。

[复用准入与成本研究](../../studies/reuse-admission-and-cost-controls/STUDY.md)区分形式检查和实测操作节省。[效用论文](../../../papers/knowledge-utility/PAPER.md)给出条件式成本结果和因果比较所需的假设。[RFC 5861](../../../reference/bibliography/BIBLIOGRAPHY.md#stale-http-responses)提供处理陈旧响应的 HTTP 类比；它不是知识或行动的授权政策。

## 8. 兼容性 {#8-compatibility}

任何示例 TTL 都不是普遍默认值。

**RUS-R013.** 部署必须（MUST）根据任务与风险选择并论证其政策。

导入旧记录时，应保留其原始观察；如果新政策需要来源中没有的信息，则添加未知值。没有额外证据，旧的通用有效性标志无法无损分解为时效性、使用资格和权限。

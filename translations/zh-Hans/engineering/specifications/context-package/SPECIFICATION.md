---
name: "context-package"
title: "语境包：覆盖、依赖与交付"
artifact: "engineering-specification"
edition: "1.1"
author: "Pavel Valentov"
language: "zh-Hans"
license: "CC-BY-4.0"
description: "对选定上下文、覆盖、强制依赖、预算和已观察交付的要求。"
translation_of: "engineering/specifications/context-package/SPECIFICATION.md"
source_commit: "161a01afb1b756adf059ea2e1cbdd0dca29d83a2"
source_git_blob: "30ca8d2e5b5dd0e38b30cdb46919f514771a01da"
translation_status: "author-draft"
---

<!-- markdownlint-disable-next-line MD033 -->
<a id="context-packages-coverage-dependencies-and-delivery"></a>

# 语境包：覆盖、依赖与交付 {#context-package-coverage-dependencies-and-delivery}

**作者：**Pavel Valentov · **出版版本：**1.1

## 1. 目的与符合性 {#1-purpose-and-conformance}

本文是一组架构要求。互操作性需要具名的表示配置；已实现的交换子集仅限于[观察、变更事件和配置通告](../../../../../engineering/specifications/status-model/SPECIFICATION.md#8-bounded-exchange-profile)，而[书籍包配置](../../../../../engineering/specifications/book-package/SPECIFICATION.md)具有自己的模式。这并不意味着已有完整契约的传输格式或已部署的运行时。

语境包是在资源预算内，为一个声明用途准备的、版本化的知识、条件与依据选择。它使人能够检查选择了什么、为什么足够或仍不完整、纳入了哪些依赖，以及接收者实际获得什么。

大写要求用语遵循 [BCP 14](../../../../../reference/bibliography/BIBLIOGRAPHY.md#requirement-language)。语境包支持回答、规划或执行阶段，但其本身不是行动授权，也不是预期结果已经发生的证据。覆盖与搜索完整性的形式区别见[检索与上下文组合](../../../../../papers/retrieval-and-context-composition/PAPER.md)。

## 2. 必需的包描述 {#2-required-package-description}

**CTX-R001.** 符合规范的包必须（MUST）包含或引用以下内容：自身身份和修订版；任务和要求修订版；目的和接收者；来源及语料快照；所选单元修订版；强制依赖闭包；槽位级覆盖；声明的搜索范围和搜索保证；适用约束；表示与交付要求；资源核算；以及支持其状态的观察。

**CTX-R002.** 每个要求槽位必须（MUST）标识所指对象（subject）、量词、必需条件和支持单元。

**CTX-R003.** 联合要求必须（MUST）针对同一个所指对象和修订版获得支持。

关于一个对象的某种性质的证据，加上另一个对象的另一种性质的证据，不能满足关于单个对象的合取要求。

**CTX-R004.** 包必须（MUST）标识被省略的要求和未解决的依赖。

如果必要依据受到访问限制，则经授权的摘要或替代物需要自身的论证。禁止默默删除依据，同时保留“已获得完整支持”的声明。

## 3. 选择与闭包 {#3-selection-and-closure}

选择从候选单元开始，并计算对当前用途有效的强制关系闭包。导航链接不会自动加入闭包。未知或缺失的必需端点会阻止“包完整”的声明。

**CTX-R005.** 即使存在环，有限集合论闭包仍然存在，但具体的可执行配置可以（MAY）要求依赖图无环。

**CTX-R006.** 这一限制必须（MUST）明确声明并检查。

此类配置拒绝一个环，并不意味着抽象闭包未定义。

增加单元可能引入新的依赖和成本。

**CTX-R007.** 组合器必须（MUST）在发生变化后重新计算闭包和预算。

**CTX-R008.** 它不得（MUST NOT）推断更长文本总是更安全或更有用：新增内容可能冲突、分散注意力、披露受保护信息，或者超过接收者的可用容量。

## 4. 覆盖与搜索保证 {#4-coverage-and-assurance}

候选集、已组装包和最终输出的覆盖分别评估。

**CTX-R009.** 每份报告必须（MUST）绑定自身所对应的阶段和所指对象修订版。

获得支持的候选集，并不使截断后的包也获得支持；获得支持的包，也不能证明答案正确使用了它。

| 覆盖值 | 在声明要求和范围内的含义 |
| --- | --- |
| supported | 每个强制槽位均具有所要求的、已确立的支持 |
| partial | 存在获得支持的部分，并明确列出缺失或未决义务 |
| unsupported | 在选定程序下，所评估范围没有提供所要求的支持 |
| conflicted | 实质上不兼容的依据阻止形成一个已获准入的结论 |
| unknown | 现有观察不能确立覆盖状态 |

搜索保证是独立维度：`candidate_only`、`exhaustive_in_scope` 或 `incomplete_procedure`，采用[规范词元定义](../../../../../engineering/specifications/status-model/SPECIFICATION.md#3-canonical-dimension-vocabularies)。要求两个例子的请求可以在没有穷尽搜索的情况下得到支持。要求全部匹配对象的请求则需要额外的完整性义务。

**CTX-R010.** 空的 top-k 结果不得（MUST NOT）报告为全局不存在的证明。

## 5. 预算与投影 {#5-budget-and-projection}

**CTX-R011.** 预算必须（MUST）计入实际交付上下文：系统和任务指令、相关历史、所选材料、工具描述、预计工具结果、输出预留，以及适用时的余量。

字符数并不是精确的词元数测量。

**CTX-R012.** 估算量和实测量必须（MUST）可区分，并指明分词器或测量方法。

**CTX-R013.** 投影必须（MUST）保留受保护单元、它们的关系，以及与任务相关的不确定性。

**CTX-R014.** 投影必须（MUST）标识排除的单元和损失。

即使输出能够精确重构所选字节，如果选择过程遗漏了例外，输出仍可能在语义上不完整。因此，字节相等与任务充分性需要不同检查。

**CTX-R015.** 当强制闭包无法容纳于预算时，组合器必须（MUST）返回部分结果、协商获准的更窄范围、采用具有保留论证的另一表示，或拒绝。

**CTX-R016.** 它不得（MUST NOT）为了满足限制而默默丢弃强制条件。

## 6. 交付与回执 {#6-delivery-and-receipt}

清单描述应当交付什么；回执记录在接收者边界上观察到了什么。媒体 URL 不能确立字节可用、已经显示、可辨读或已被理解。

**CTX-R017.** 交付检查必须（MUST）符合任务的表示要求以及读取方的已声明能力。

**CTX-R018.** 任何输出评估都必须（MUST）指出精确的已交付包和要求修订版。

接收或理解确认不是能力评估、执行同意或授权。

## 7. 验收与证据 {#7-acceptance-and-evidence}

**CTX-R019.** 验收用例必须（MUST）包括：未解决的依赖、跨对象合取、缺失的量词覆盖、因闭包而导致的预算溢出、被省略的必需媒体、过时的要求修订版，以及丢掉已支持条件的最终输出。

**CTX-R020.** 对每种情形，检查必须（MUST）区分包构建与下游使用。

[依赖闭包与交付研究](../../../../../engineering/studies/dependency-closure-and-package-delivery/STUDY.md)包含可执行的有限重放：在一个 110 节点依赖图上，对 12 个技能根节点的全部 4,096 个子集，以及 24,576 个单元素包含关系进行检查。这验证的是指定的图行为，而不是从任意来源提取依赖的完整性。[投影研究](../../../../../engineering/studies/executable-projections-and-revision/STUDY.md)考察下游表示，并报告所测最小性的局限。

## 8. 兼容性 {#8-compatibility}

历史覆盖字段只有与其所指对象和语义一起保留时才可导入。缺失的来源快照、预算测量或交付观察仍然是未知的。新的文档版本不会追溯性地把早期说明性示例升级为已经执行的包。术语定义见[术语表](../../../../../reference/glossary/GLOSSARY.md)。

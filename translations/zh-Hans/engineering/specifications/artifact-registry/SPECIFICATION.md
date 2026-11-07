---
name: "artifact-registry"
title: "制品登记、可读名称与文档格式"
artifact: "engineering-specification"
edition: "1.1"
author: "Pavel Valentov"
language: "zh-Hans"
license: "CC-BY-4.0"
description: "可读制品名称、规范 Markdown 格式、身份规则及专业制品的区别。"
translation_of: "engineering/specifications/artifact-registry/SPECIFICATION.md"
source_commit: "a0450428704fcd41b411203f2fc88c06c779610b"
source_git_blob: "1fe5680e0c0e9925191fea0d187f76d915625804"
translation_status: "author-draft"
---

# 制品登记、可读名称与文档格式 {#artifact-registry-readable-names-and-document-formats}

**作者：**Pavel Valentov · **出版版本：**1.1

## 1. 目的与符合性 {#1-purpose-and-conformance}

本文是一组架构要求。互操作性需要具名的表示配置；已实现的交换子集仅限于[观察、变更事件和配置通告](../status-model/SPECIFICATION.md#8-bounded-exchange-profile)，而[书籍包配置](../book-package/SPECIFICATION.md)具有自己的模式。这并不意味着已有完整契约的传输格式或已部署的运行时。

登记机制为人和代理提供可预测的方式，以查找、解释和修订制品。它将对象身份与标题、修订版、文件表示和当前评估分开。一个新的技术术语不会自动要求一张新的数据库表或一个新服务。

大写要求用语遵循 [BCP 14](../../../../../reference/bibliography/BIBLIOGRAPHY.md#requirement-language)。以下格式是项目约定，明确指定外部格式的情况除外。它们不声称是胜任能力、角色或方案蓝图的通用标准。

## 2. 名称、身份与修订版 {#2-names-identity-and-revisions}

**REG-R001.** 每个当前制品必须（MUST）位于其类型集合中名称唯一的目录内。

**REG-R002.** 目录名称使用有意义的小写词语，并以单个连字符分隔；读者必须（MUST）能够不查询内部编号就推断主题。

`r1`、`r10` 或 `p09` 等名称不能作为有效标题或当前规范短名。

**REG-R003.** 历史标识符可以（MAY）保留在溯源和迁移映射中。

主文件具有由类型决定的可预测名称。重命名保留溯源；如果旧路径已经发布，则提供兼容映射。不可变修订版标识某个具体内容状态。可变的“当前”指针是在另一项决定治理下作出的选择，而不是为每个请求创建的新身份。

## 3. 出版物格式 {#3-publication-formats}

| 集合 | 主文件 | 必需内容 |
| --- | --- | --- |
| `papers/<topic>/` | `PAPER.md` | 摘要、问题与贡献、定义、论证或结果、反例、局限，以及工程证据引用 |
| `engineering/specifications/<topic>/` | `SPECIFICATION.md` | 目的、符合性、模型、要求、失败处理、验收用例、兼容性、证据 |
| `engineering/studies/<topic>/` | `STUDY.md` | 问题、材料与权利、方法、实际结果、不利用例、可复现性、局限及断言链接 |
| `reference/glossary/` | `GLOSSARY.md` | 首选术语、定义、区别、别名和语言映射 |
| `reference/bibliography/` | `BIBLIOGRAPHY.md` | 已识别著作、第一手 URL 或 DOI，以及每个来源的作用 |
| `appendices/<topic>/` | `APPENDIX.md` | 具名的辅助主题、其范围、引用及与主要文档的关系 |

**REG-R004.** 当前出版物必须（MUST）出现在 `publication-catalog.json` 中。

目录记录类型、短名、路径、标题、摘要、语言和出版版本。它是阅读清单，而不是索引或执行内容的授权。

**REG-R005.** 每个主 Markdown 文件必须（MUST）具有 YAML 前置元数据，其中包含 `name`、`title`、`artifact`、`edition`、`author`、`language`、`license`，以及非空的 `description`。

来源通过仓库的来源登记表注册。

**REG-R006.** 主文件必须（MUST）包含一个描述性 H1 标题。

**REG-R007.** 版本和机器标识符属于元数据、兼容说明或溯源；它们不得（MUST NOT）主导阅读标题。

相对链接连接当前出版版本。历史断言链接到固定修订版。

## 4. 约束与专业制品 {#4-constraints-and-professional-artifacts}

专业工作配置沿用同一目录约定。只有实际制品存在时才创建集合；无需创建推测性的空目录。

| 制品 | 主文件 | 含义与必需章节 |
| --- | --- | --- |
| 角色 | `ROLE.md` | 职责；范围；允许的决定；必需技能或胜任能力；接口；责任归属 |
| 技能 | `SKILL.md` | 可复用过程；适用时机；输入；步骤；检查；约束；输出；支持资源 |
| 胜任能力 | `COMPETENCY.md` | 能力要求或已评估断言；主体；表现标准；评估条件；证据；有效性限制 |
| 方案蓝图 | `BLUEPRINT.md` | 解决方案结构或过程；预期结果；组件或步骤；依赖；选择；约束；验收 |
| 约束 | `CONSTRAINT.md` | 对象；范围；规范规则或条件；来源或权限；执行约束或检查；例外；失败行为 |
| 工作项 | `WORK_ITEM.md` | 目标；要求修订版；输入；指派；约束；计划；结果标准；尝试与结果 |

胜任能力定义说明什么能力算作符合要求。胜任能力评估将证据绑定到具体执行者和条件。角色文件或技能文件都不认证这种能力。方案蓝图组织工作，但不提供授权。约束应直接连接到所有适用制品，而不是埋在一般说明中，或被误认为可选建议。

对于技能，外部的 [Agent Skills 规范](https://agentskills.io/specification)规定 `SKILL.md` 文件名以及必需的 `name` 和 `description` 前置元数据。本项目使用该规范支持的 `metadata` 映射存放额外项目字段，而不是发明不兼容的必需顶层键。技能名称与其目录名称匹配。支持代码、引用和资源保留在技能目录内。上述正文标题是项目约定，不是 Agent Skills 强制规定的标题。

仓库指令使用 [AGENTS.md](https://agents.md/)，即普通的 Markdown 指令文件。它不是角色或代理身份的通用序列化格式。

**REG-R008.** 供应商特定的可执行代理配置必须（MUST）具有明确的适配器，并与可读角色定义保持分离。

## 5. 登记义务 {#5-registry-obligations}

**REG-R009.** 每个登记修订版必须（MUST）标识其类别、表示配置、身份、修订版、许可证或披露限制、溯源、必需依赖和适用观察。

**REG-R010.** 读取器必须（MUST）区分已知、未知、不适用和不予披露的信息。

**REG-R011.** 必需引用必须（MUST）解析到预期修订版，或报告依赖未解决。

历史上登记的 34 种制品类型描述的是一个示例登记表，并不确立知识只有这 34 种穷尽类别。其共通封套是这些示例的载体，而不是对所有未来契约的限制。[来源映射](../../../../../appendices/source-map/APPENDIX.md)在科学论证之外保留这一兼容背景。

## 6. 验收与迁移 {#6-acceptance-and-migration}

**REG-R012.** 登记检查必须（MUST）拒绝重复的规范名称、缺失的必需主文件、不兼容的前置元数据、损坏的当前链接以及不加说明的身份复用。

**REG-R013.** 重命名测试必须（MUST）展示旧路径指向何处，以及引用的不可变修订版如何仍可恢复。

未知的必需扩展会阻止使用；保留未知的可选数据，并不能确立这些数据已被解释。

**REG-R014.** 迁移必须（MUST）保留来源身份和原始修订版、记录映射，并披露无法映射的字段。

**REG-R015.** 迁移不得（MUST NOT）仅从制品存在就推断能力、具体授权或成功执行。

[修订论文](../../../papers/revision-and-governance/PAPER.md)解释这些区别；[编辑研究](../../../../../engineering/studies/editorial-skill-pilot/STUDY.md)记录了一次真实而有限的技能和蓝图使用，并未因它们存在就声称具有优势。

---
name: "source-map"
title: "来源历史：来源映射、早期版本与协议兼容性"
artifact: "appendix"
edition: "1.1"
author: "Pavel Valentov"
language: "zh-Hans"
license: "CC-BY-4.0"
description: "从早期语料的迁移、不可变历史、证据溯源与明确的协议兼容性边界。"
translation_of: "appendices/source-map/APPENDIX.md"
source_commit: "a0450428704fcd41b411203f2fc88c06c779610b"
source_git_blob: "668c939f1f43b9e61800cbb8f2b5ac07e18a49ef"
translation_status: "author-draft"
---

# 来源历史：来源映射、早期版本与协议兼容性 {#source-map-earlier-editions-and-protocol-compatibility}

**出版版本：** 1.1 · **来源审计日期：** 2026年11月4日

## 1. 本版改变了什么 {#1-what-this-edition-changes}

早期仓库包含十四个简短的英文论文入口页、十四篇篇幅长得多的俄文手稿、十个英文规范入口页和十篇俄文规范正文。长文本将科学论证、领域研究、迭代说明以及指向公开发布范围之外的支持记录的引用混合在一起。

本版把这些材料重新组织为八篇完整的英文科学论文、十一份工程规范、六项工程研究、共用的术语表与参考文献，以及两个辅助附录。科学结果、规范性要求和观察现在可以分别识别。早期迭代历史仍可通过仓库的不可变修订版恢复，而不再作为反复出现的交接章节混入当前阅读路径。

上一版出版物的精确快照是 [b50243b28e9ad7376e28c749a21479ef46ec9d60](https://github.com/Arcanada-one/knowledge-contract/tree/b50243b28e9ad7376e28c749a21479ef46ec9d60)。上一版网站快照是 [64ddd981296cb65390beecd802f1682618a7f080](https://github.com/Arcanada-one/contract-place-site/tree/64ddd981296cb65390beecd802f1682618a7f080)。这些引用是历史证据，不是可变主分支的别名。

独立审查针对的是位于 [ed2e188c89a1a50a187f3d55bf32baab54c87f7e](https://github.com/Arcanada-one/knowledge-contract/tree/ed2e188c89a1a50a187f3d55bf32baab54c87f7e) 的已发布1.0版。修正以该不可变基线为基础。历史证据及其来源哈希保持不变；修正后的解释和新的有限检查各自拥有独立记录。当前文档指出形式化结果所需的更强前提、观察的实际范围，以及下文介绍的不向后兼容的图书包配置。

## 2. 科学材料对应关系 {#2-scientific-crosswalk}

下列表格中指向当前文档的链接均指向固定修订版的英文原文。

| 早期手稿 | 当前科学材料归属 | 分离到工程部分的材料 |
| --- | --- | --- |
| 引言 | [语义对象与上下文](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/semantic-objects-and-context/PAPER.md) | [出版物清单](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/publication-catalog.json)和[API接口边界](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/appendices/api-integration/APPENDIX.md#2-documented-public-interface)；任何清单都不能确立实现符合性 |
| 语义对象与提取 | [语义对象与上下文](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/semantic-objects-and-context/PAPER.md) | [来源转录与不确定性](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/source-transcription-and-uncertainty/STUDY.md) |
| 上下文与适用性 | [语义对象与上下文](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/semantic-objects-and-context/PAPER.md) | [已声明依赖图与有限交付检查](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/STUDY.md) |
| 变换与迁移 | [受约束变换](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/constrained-transformations/PAPER.md) | [可执行投影与修订](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/STUDY.md) |
| 查询、检索与覆盖 | [检索与上下文组合](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/retrieval-and-context-composition/PAPER.md) | [覆盖与交付要求](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/specifications/context-package/SPECIFICATION.md)；不声称已开展有限的检索性能研究 |
| 预算约束下的上下文组合 | [检索与上下文组合](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/retrieval-and-context-composition/PAPER.md) | [交付记录数与故障控制](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/STUDY.md#delivered-record-counts-and-fault-controls)；这里计数的是图记录，不是测得的令牌或字节成本 |
| 对话与学习 | [交互与记忆](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/interaction-and-memory/PAPER.md) | [操作与任务绑定](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/specifications/contract-family/SPECIFICATION.md#2-common-contract-record)以及[定向修订案例](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/STUDY.md#targeted-revision-and-a-strong-alternative)；没有纵向对话或学习研究 |
| 推理与证据 | [证据与证伪](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/evidence-and-falsification/PAPER.md) | [检查器的信任边界与反例](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/contract-profile-conformance/STUDY.md#counterexamples-and-the-comparator) |
| 文档与记忆 | [交互与记忆](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/interaction-and-memory/PAPER.md) | [可读投影审计](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/source-transcription-and-uncertainty/STUDY.md)以及[单章节编辑试验](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/editorial-skill-pilot/STUDY.md) |
| 工作、角色、技能与知识契约 | [受控知识复用](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/controlled-knowledge-reuse/PAPER.md)和[修订与治理](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/revision-and-governance/PAPER.md) | [核心](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/specifications/knowledge-contract-core/SPECIFICATION.md)、[制品登记](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/specifications/artifact-registry/SPECIFICATION.md)和[配置符合性](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/contract-profile-conformance/STUDY.md) |
| 修订与准则 | [修订与治理](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/revision-and-governance/PAPER.md) | [版本化规则要求](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/specifications/knowledge-evolution/SPECIFICATION.md)和[范围有限的可寻址修订观察](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/STUDY.md#targeted-revision-and-a-strong-alternative) |
| 评估与证伪 | [证据与证伪](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/evidence-and-falsification/PAPER.md) | [主张—证据索引](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/evidence-index.json)、[普通案例与边界案例的分开计数](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/README.md#counting-and-interpretation)，以及[比较基线的平局结果](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/contract-profile-conformance/STUDY.md#counterexamples-and-the-comparator) |
| 编译、缓存与复用 | [受控知识复用](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/controlled-knowledge-reuse/PAPER.md) | [编译制品要求](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/specifications/compiled-artifact-contract/SPECIFICATION.md)、[失效处理](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/specifications/cache-identity-and-invalidation/SPECIFICATION.md)和[复用政策](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/specifications/reuse-policy/SPECIFICATION.md)；没有针对已部署系统的代际或幂等性实验 |
| 知识效用与资源经济性 | [知识效用](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/knowledge-utility/PAPER.md) | [合成准入检查与分析性成本](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/reuse-admission-and-cost-controls/STUDY.md)；没有测得的生产环境成本收益 |

早期版本的数字文件名仅作为兼容链接保留。它们指向当前科学材料归属，以及对应的精确早期英文和俄文文本。合并按主题进行，不会悄悄把未经检验的历史提案转换成已证明的主张。未得到当前论证或证据支持的历史主张仍是历史提案，可在来源快照中查阅。

## 3. 工程材料对应关系 {#3-engineering-crosswalk}

十个早期规范主题与下列当前文件一一对应：

| 早期主题 | 当前规范——英文原文 |
| --- | --- |
| Knowledge Contract v3 | [核心模型与准入](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/specifications/knowledge-contract-core/SPECIFICATION.md) |
| 契约族 | [知识操作](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/specifications/contract-family/SPECIFICATION.md) |
| 语义类型 | [语义类型与表示](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/specifications/semantic-types/SPECIFICATION.md) |
| 上下文包 | [覆盖、依赖与交付](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/specifications/context-package/SPECIFICATION.md) |
| 编译制品契约 | [编译制品与派生](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/specifications/compiled-artifact-contract/SPECIFICATION.md) |
| 制品登记 | [可读名称与文档格式](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/specifications/artifact-registry/SPECIFICATION.md) |
| 状态模型 | [评估、执行与发布状态](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/specifications/status-model/SPECIFICATION.md) |
| 缓存身份与失效处理 | [身份与失效处理](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/specifications/cache-identity-and-invalidation/SPECIFICATION.md) |
| 复用政策 | [时间、权限与结果](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/specifications/reuse-policy/SPECIFICATION.md) |
| 知识演化契约 | [版本化规则](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/specifications/knowledge-evolution/SPECIFICATION.md) |

新增的[图书包规范——英文原文](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/specifications/book-package/SPECIFICATION.md)源于上游修订版 [570f76b6d9a189295c3229254821c30748383965](https://github.com/Arcanada-one/knowledge-contract/tree/570f76b6d9a189295c3229254821c30748383965) 中加入的模式、验证器与合成测试样例。1.0版保留了这些上游字节。当前修正定义了不向后兼容的 **`book-package/2`** 配置和 **`KCBook*/v2`** 记录：审查结果绑定到实际审查对象、范围与准则；权利分类约束许可和导出的可接受方式；就绪状态遵循完整的已声明状态规则。这是明确的格式变更，而不是对历史 `v1` 记录的隐式重新解释。

最后经过审查的 `v1` 实现仍可在 [ed2e188c89a1a50a187f3d55bf32baab54c87f7e](https://github.com/Arcanada-one/knowledge-contract/tree/ed2e188c89a1a50a187f3d55bf32baab54c87f7e) 查阅。使用方必须（MUST）标明其接受的配置版本与模式版本。转换到 `v2` 需要一条具有新身份的记录，以及所有缺失的评估证据；重命名模式标记绝不能（MUST NOT）把旧审查、权利断言或状态变成新确立的事实。发布这些文档不会自动重新评估，也不会改变语料准入。

工程研究包含实际领域材料，包括历史上的烹饪、导航与电气示例。它们区分了可公开重放的程序、可检查的保留报告，以及不可获得的第三方来源语料。[证据索引——英文原文](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/evidence-index.json)记录每项主张的支持依据与限制；仅有导航链接并不是经验论证。

## 4. 协议兼容性 {#4-protocol-compatibility}

出版版本 **1.0** 标识最初接受审查的文档集合；当前出版物的版本在其目录与元数据中声明。二者都不是经过重命名的运行时协议。历史记录需要的下列标识符予以保留。以大写关键词表示的要求遵循 [BCP 14——英文原文](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/reference/bibliography/BIBLIOGRAPHY.md#requirement-language)。

| 标识符 | 实际范围 | 兼容性说明 |
| --- | --- | --- |
| `3.0.0-draft.1` | 早期目标知识契约架构 | 不能从编辑后的出版版本推断稳定协议已经发布 |
| `kc-synthesis/0.1` | 范围有限的解释型JSON核心与配置实现 | 保留的结果并未实现当前架构的全部要求 |
| `mm-envelope/0.1` | 历史登记系统与示例使用的通用载体 | 该载体及其34种制品类型既不是知识的穷尽分类，也不限制后续契约 |
| `i16-compiled-artifact/0.1` | 范围有限的编译制品表示 | 原始观察保留其原始配置与验证器范围 |
| `i17-reuse-policy/0.1` | 范围有限的时间与复用政策模型 | 区间计算不等于生产环境授权或分布式原子化提供 |
| `knowledge-evolution-metadata/0.2-proposal` | 早期演化元数据提案 | 发布架构要求并不声称迁移服务已部署 |
| 知识契约准入运行时 | 在明确公布的配置与政策下决定准入的服务边界 | 本出版物并未确立一个稳定且已部署的运行时版本；声称符合性时，操作者必须（MUST）提供实际实现及配置的身份 |
| `kc2_admission` | 历史图书记录字段名 | 它不是运行时或协议版本。该字段的存在不能确立准入，本出版物也不通过重命名它来暗示一个新运行时 |
| `KCBook*/v1` | 不可变1.0版基线中的图书记录 | 历史模式行为仍可在 `ed2e188c89a1a50a187f3d55bf32baab54c87f7e` 审计；转换不会追溯性地使其得到验证 |
| `book-package/2`, `KCBook*/v2` | 当前修正后的图书表示与验证器配置 | 不兼容的字段与决策变更需要明确迁移，并为缺失之处提供新证据；它们并不标识准入运行时 |

声称符合本版的实现必须（MUST）说明它满足哪些要求，并链接相应证据。模式、字段语义或交换格式版本的变更需要自己的迁移与兼容性记录。发布过程绝不能（MUST NOT）仅为删除历史开发标签而改写保留的原始证据。

## 5. 溯源与权利 {#5-provenance-and-rights}

每项研究的 `evidence/origin.json` 标识其证据文件的来源、精确输出哈希和转换状态。精确恢复的JSON与从保留HTML重建的可读文字视图区分开来。后者并不声称复现了不可获得的原始Markdown字节。

本仓库不重新分发第三方图书、页面图像或OCR语料。当前论证是自足的；可公开运行的示例使用原创合成数据或仅含元数据的图。来源访问受限会限制相应历史实验的独立复现，研究会在受影响的主张处明确说明这一限制。

项目文本仍采用 [CC BY 4.0](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/LICENSE)，代码仍采用 [Apache-2.0](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/LICENSE-CODE)。当前[来源登记表——英文原文](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/SOURCES.md)用具名的原始文献及明确的文档覆盖关系，替代了新版本此前笼统的来源描述。

## 6. 阅读与引用 {#6-reading-and-citation}

引用论文时，应注明人类可读的标题、作者、出版版本和不可变修订版；确有已发布DOI时，也可以引用该DOI。本版不会虚构DOI。论证应引用论文，要求应引用规范，观察应引用研究或精确证据记录。[术语表——英文原文](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/reference/glossary/GLOSSARY.md)统一解释共用术语，避免在每篇文章中重复完整定义。

## 7. 内部审查与验证 {#7-internal-review-and-verification}

[出版物审查——英文原文](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/reviews/publication-integrity/REVIEW.md)记录实际的科学与证据审查、精确输入身份、集成修正、本地检查，以及未执行的发布检查。它区分内部内容验收、外部同行评审，以及仓库、网站和语料准入的独立结果。

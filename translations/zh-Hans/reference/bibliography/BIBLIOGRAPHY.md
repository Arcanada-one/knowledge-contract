---
name: "bibliography"
title: "研究基础：原始文献与研究基础"
artifact: "bibliography"
edition: "1.1"
author: "Pavel Valentov"
language: "zh-Hans"
license: "CC-BY-4.0"
description: "具名原始文献，以及每项文献在当前版本中承担的确切概念或技术作用。"
translation_of: "reference/bibliography/BIBLIOGRAPHY.md"
source_commit: "a0450428704fcd41b411203f2fc88c06c779610b"
source_git_blob: "894c57511dc174bfad7bb5ac0157d35daceed8cf"
translation_status: "author-draft"
---

# 研究基础：原始文献与研究基础 {#primary-sources-and-research-foundations}

**出版版本：** 1.1 · **书目核验日期：** 2026年11月4日

以下条目标识当前版本实际使用的原始文献，并区分已确立的结果、外部格式与本项目自己的综合构建。被引来源提供所述概念或技术基础；它既不为知识契约背书，也不确立其实现的有效性。本出版物不复制第三方图书正文或来源页面图像。

## 溯源 {#provenance}

Luc Moreau、Paolo Missier，编。**PROV-DM: The PROV Data Model.** W3C推荐标准，2013年4月30日。[注明日期的规范](https://www.w3.org/TR/2013/REC-prov-dm-20130430/)。

用于区分溯源中的实体、活动与代理，以及区分溯源与对内容的判断。项目额外提出任务专属的适用性与准入义务；这些不是PROV-DM替本项目提出的主张。

## SKOS {#skos}

Alistair Miles、Sean Bechhofer，编。**SKOS Simple Knowledge Organization System Reference.** W3C推荐标准，2009年8月18日。[注明日期的规范](https://www.w3.org/TR/2009/REC-skos-reference-20090818/)。

用于概念、标签和知识组织关系。相同标签或概念关系并不能证明语义等价或真实性。

## 部分正确性 {#partial-correctness}

C. A. R. Hoare. **An Axiomatic Basis for Computer Programming.** *Communications of the ACM* 12(10)，1969，576–580、583。[DOI: 10.1145/363235.363259](https://doi.org/10.1145/363235.363259)。[作者所在机构的书目](https://www.cs.ox.ac.uk/people/publications/title/Tony.Hoare.html)。

用于通过前置条件、后置条件和推理规则对程序进行推理这一既有思想。变换论文将条件性保留推理应用于其明确界定的关系。论文中的组合论证并未被表述为替代程序逻辑的新方法，也不是终止性证明。

## 次模最大化 {#submodular-maximization}

George L. Nemhauser、Laurence A. Wolsey、Marshall L. Fisher. **An Analysis of Approximations for Maximizing Submodular Set Functions—I.** *Mathematical Programming* 14，1978，265–294。[DOI: 10.1007/BF01588971](https://doi.org/10.1007/BF01588971)。

用于在归一化、单调次模价值函数和基数限制下的经典贪心近似结果。上下文组合论文明确列出这些假设，并解释相互补充的知识单元为何可能违反次模性。该保证不被移用于任意预算、惩罚项或语义质量函数。

## 检索增强生成 {#retrieval-augmented-generation}

Patrick Lewis、Ethan Perez、Aleksandra Piktus、Fabio Petroni、Vladimir Karpukhin、Naman Goyal、Heinrich Küttler、Mike Lewis、Wen-tau Yih、Tim Rocktäschel、Sebastian Riedel、Douwe Kiela. **Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.** *Advances in Neural Information Processing Systems* 33，2020。[会议出版物](https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html)。[作者手稿](https://arxiv.org/abs/2005.11401)。

作为以检索材料为条件进行生成的原始参考文献。上下文组合论文研究明确的覆盖与保留义务；它不声称重复了所引实验，也不声称超越了其中的模型。

## 计算复杂性 {#computational-complexity}

Richard M. Karp. **Reducibility among Combinatorial Problems.** 收于 *Complexity of Computer Computations*，1972，85–103。[DOI: 10.1007/978-1-4684-2001-2_9](https://doi.org/10.1007/978-1-4684-2001-2_9)。

作为集合覆盖问题经典复杂性背景的原始来源。当前论文给出从有限覆盖问题到受限上下文选择实例的明确映射。这不意味着每个实际实例都困难，也不意味着有限精确搜索不可能。

## 程序切片 {#program-slicing}

Mark Weiser. **Program Slicing.** *IEEE Transactions on Software Engineering* SE-10(4)，1984，352–357。[原始论文](https://faculty.cc.gatech.edu/~harrold/6340/cs6340_fall2009/Readings/Weiser.Slicing.TSE.pdf)。

[语义对象与上下文论文——英文原文](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/semantic-objects-and-context/PAPER.md)用它指明后向切片所涉及的既有行为保留问题。论文给出受限的无环模型；它没有引入新的通用切片算法，也没有据此推断任意文本的语义保留。

## 真值维护 {#truth-maintenance}

Jon Doyle. **A Truth Maintenance System.** *Artificial Intelligence* 12(3)，1979，231–272。[出版方记录](https://www.sciencedirect.com/science/article/pii/0004370279900080)。[MIT报告版本，AI Memo 521](https://dspace.mit.edu/entities/publication/5377b306-4ecc-4687-b1f5-78cbb4a0543a)。

[修订与治理论文——英文原文](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/revision-and-governance/PAPER.md)将其用作有关记录理由、随假设变化修订信念的先行工作。项目的可达性论证识别可能受影响的评估；它不是Doyle系统的实现。

## 构建系统 {#build-systems}

Andrey Mokhov、Neil Mitchell、Simon Peyton Jones. **Build Systems à la Carte.** *Proceedings of the ACM on Programming Languages* 2(ICFP)，文章79，2018，1–29。[DOI: 10.1145/3236774](https://doi.org/10.1145/3236774)。[作者版本](https://simon.peytonjones.org/assets/pdfs/build-systems-original.pdf)。

[受控知识复用论文——英文原文](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/controlled-knowledge-reuse/PAPER.md)用它说明调度与重新构建之间的既有区别，以及相对于已声明依赖的正确性。与构建依赖一致，并不能确立来源的真实性、新任务的语义要求或当前权限。

## 视图与补集 {#views-and-complements}

François Bancilhon、Nicolas Spyratos. **Update Semantics of Relational Views.** *ACM Transactions on Database Systems* 6(4)，1981，557–575。[原始论文](https://cs.uwaterloo.ca/~david/cs848s18/constant-complement.pdf)。

[受约束变换论文——英文原文](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/constrained-transformations/PAPER.md)将其用作一种既有构造：视图与保留的补集共同确定数据库状态，并约束更新转换。该类比为保留残余信息提供动机；项目不声称自然语言投影满足这些视图更新定律。

## 理论变更 {#theory-change}

Carlos E. Alchourrón、Peter Gärdenfors、David Makinson. **On the Logic of Theory Change: Partial Meet Contraction and Revision Functions.** *The Journal of Symbolic Logic* 50(2)，1985，510–530。[DOI: 10.2307/2274239](https://doi.org/10.2307/2274239)。[出版方记录](https://www.cambridge.org/core/journals/journal-of-symbolic-logic/article/abs/on-the-logic-of-theory-change-partial-meet-contraction-and-revision-functions/7ED837BAD5FB6D9A7C77906D73527F9C)。

[修订与治理论文——英文原文](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/revision-and-governance/PAPER.md)用它区分逻辑收缩、逻辑修订与版本化制品、采纳决策。当前模型既没有定义AGM修订算子，也不声称满足AGM公设。

## 因果推断 {#causal-inference}

Judea Pearl. **Causal Inference in Statistics: An Overview.** *Statistics Surveys* 3，2009，96–146。[DOI: 10.1214/09-SS057](https://doi.org/10.1214/09-SS057)。[作者的机构存档](https://escholarship.org/uc/item/1sv6k47m)。

用于区分观察到的关联与基于干预、混杂假设的因果结论。因此，效用论文区分测得的任务评分与已识别的因果收益，不把小规模探索性比较视为总体估计。

## HTTP缓存 {#http-caching}

Roy T. Fielding、Mark Nottingham、Julian Reschke，编。**HTTP Caching.** RFC 9111，互联网标准，2022年6月。[RFC 9111](https://www.rfc-editor.org/rfc/rfc9111.html)。

作为HTTP缓存控制与时效性概念的参考文献。知识适用性、语义依赖闭包和行动授权仍是项目额外提出的义务。

## 过期HTTP响应 {#stale-http-responses}

Mark Nottingham. **HTTP Cache-Control Extensions for Stale Content.** RFC 5861，信息性文档，2010年5月。[RFC 5861](https://www.rfc-editor.org/rfc/rfc5861.html)。

作为stale-while-revalidate与stale-if-error行为的明确受限类比。该文档为信息性文档，其HTTP机制并不授权复用已撤销的知识或实施行动。

## 要求用语 {#requirement-language}

Scott Bradner. **Key Words for Use in RFCs to Indicate Requirement Levels.** RFC 2119，BCP 14，1997年3月。[RFC 2119](https://www.rfc-editor.org/rfc/rfc2119.html)。

Barry Leiba. **Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words.** RFC 8174，BCP 14，2017年5月。[RFC 8174](https://www.rfc-editor.org/rfc/rfc8174.html)。

工程规范在此意义上使用大写MUST、MUST NOT、SHOULD、SHOULD NOT和MAY。这些词的规范性约束针对是否符合所述项目规范；并不声称该规范是IETF标准。

## JSON交换与模式 {#json-exchange-and-schemas}

Tim Bray，编。**The JavaScript Object Notation (JSON) Data Interchange Format.** RFC 8259，互联网标准，2017年12月。[RFC 8259](https://www.rfc-editor.org/rfc/rfc8259)。

Austin Wright、Henry Andrews、Ben Hutton、Greg Dennis，编。**JSON Schema: A Media Type for Describing JSON Documents.** 草案2020-12。[官方核心规范](https://json-schema.org/draft/2020-12/json-schema-core)。

用于范围有限的观察、依赖变更、图书包与索引回执配置的交换语法和JSON Schema方言。模式验证已声明的数据结构与约束；它不认证观察的真实性，也不执行全部跨记录语义检查。精确字节哈希配置并不意味着JSON值的规范化。

## 智能体制品格式 {#agent-artifact-formats}

Agent Skills维护者。**Agent Skills Specification.** [官方规范](https://agentskills.io/specification)，查阅于2026年11月4日。

用于技能目录命名、必需的 `SKILL.md` 文件、其中的 `name` 与 `description` 元数据，以及受支持的扩展元数据。项目在保持该格式兼容性的同时，定义自己的额外阅读结构。

AGENTS.md维护者。**AGENTS.md.** [官方格式说明](https://agents.md/)，查阅于2026年11月4日。

用于仓库向编码智能体提供指令。该格式是普通Markdown，不规定智能体身份、胜任能力、角色或方案蓝图的通用模式。项目明确将这些制品的格式界定为自己的约定。

## 评估方法 {#evaluation-methods}

以下来源说明研究中使用的方法论区分。它们既不认证历史运行，也不补足缺失的测试样例，更不会把同一会话内的审查变成独立重复。

Brian A. Nosek、Charles R. Ebersole、Alexander C. DeHaven、David T. Mellor. **The Preregistration Revolution.** *Proceedings of the National Academy of Sciences* 115(11)，2018，2600–2606。[DOI: 10.1073/pnas.1708274114](https://doi.org/10.1073/pnas.1708274114)。[原始文章](https://pmc.ncbi.nlm.nih.gov/articles/PMC5856500/)。[编辑试验——英文原文](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/editorial-skill-pilot/STUDY.md)区分在保留输出产生之前固定的协议与在得知结果之后编写的分析。其本地记录的协议未在外部公共注册库登记。

Lianmin Zheng、Wei-Lin Chiang、Ying Sheng、Siyuan Zhuang、Zhanghao Wu、Yonghao Zhuang、Zi Lin、Zhuohan Li、Dacheng Li、Eric P. Xing、Hao Zhang、Joseph E. Gonzalez、Ion Stoica. **Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena.** *Advances in Neural Information Processing Systems 36, Datasets and Benchmarks Track*，2023。[作者手稿](https://arxiv.org/abs/2306.05685)。用于说明需要考察评判者偏差与一致性结论的边界。编辑研究和[投影研究——英文原文](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/STUDY.md)使用自己的粗粒度评分规则和掩蔽方式；它们不会继承被引基准的一致性或验证结果。

Richard A. DeMillo、Richard J. Lipton、Frederick G. Sayward. **Hints on Test Data Selection: Help for the Practicing Programmer.** *Computer* 11(4)，1978年4月，34–41。[出版方记录](https://ieeexplore.ieee.org/abstract/document/1646911)。[机构书目记录](https://www.cerias.purdue.edu/apps/reports_and_papers/view/919)。这是刻意实施程序变异的历史背景。项目报告其声明的变异体以及测试能否区分它们；有限变异结果并不代表一般性的测试充分性。

Alfred Tarski. **A Lattice-Theoretical Fixpoint Theorem and Its Applications.** *Pacific Journal of Mathematics* 5(2)，1955，285–309。[出版方原始文章](https://msp.org/pjm/1955/5-2/pjm-v5-n2-p11-s.pdf)。提供一般的不动点理论背景。[依赖研究——英文原文](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/STUDY.md)在已声明图的幂集上通过有限单调迭代计算最小闭包；其证明与实现检查并不确立每一项语义依赖都已记录。

National Institute of Standards and Technology. **SCLITE Scoring Package: Alignment and Scoring Documentation.** [官方SCTK文档](https://github.com/usnistgov/SCTK/blob/master/doc/sclite.htm)，查阅于2026年11月4日。用于参考文本与假设文本的对齐，以及词错误报告所依据的替换、删除与插入计数。[转录研究——英文原文](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/source-transcription-and-uncertainty/STUDY.md)明确给出字符和词的计量单位定义；由于所需参考文本与协议不可获得，没有报告实测CER或WER。

## 实验来源图书 {#experimental-source-books}

这些图书标识工程研究所使用的历史材料。它们不是新科学定理的来源，本出版物也不为其中的实用建议背书。实际处理的输入由保留的导出身份标识，而非仅由目录页面标识。

- **Книга о вкусной и здоровой пище**（*The Book of Tasty and Healthy Food*）。苏联食品工业部。莫斯科：Pishchepromizdat，1952。[国家电子图书馆记录](https://rusneb.ru/catalog/000199_000009_005811805/)。作为烹饪导出用于[转录研究——英文原文](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/source-transcription-and-uncertainty/STUDY.md)。保留的导出键 `molchanova` 和俄文标签“Молчанова”在项目报告中标识该输入；它们不表示独著归属。被引目录将食品工业部列为责任机构，本版不从导出键推断编辑者身份。
- **Навигация, лоция и мореходная астрономия**（*Navigation, Pilotage, and Nautical Astronomy*）。G. I. Fain。莫斯科：Transport，1977。[国家电子图书馆记录](https://rusneb.ru/catalog/000199_000009_007594442/)。用作导航导出；[保留的语料审计](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/source-transcription-and-uncertainty/evidence/corpus-audit-source.json)标识已处理的表示。
- **Сто схемных задач по автоматике**（*One Hundred Circuit Problems in Automation*）。V. A. Timofeev。列宁格勒：Sudostroenie，1964。这些是[保留的语料审计](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/source-transcription-and-uncertainty/evidence/corpus-audit-source.json)为自动化导出记录的书目信息。本次审查未确立针对这一确切版本、经独立核验的稳定目录记录；项目审计说明输入溯源，不等于外部书目确认。历史工程任务考察表示与保留，而非现代操作认证。

### 编辑输入 {#editorial-input}

Maxim Ilyakhov、Lyudmila Sarycheva。**Пиши, сокращай: Как создавать сильный текст**（*Write and Shorten: How to Create Strong Text*）。第4版，莫斯科：Alpina Publisher，2024，400个印刷页，**以上按所提供OCR书目行的记载**。[出版方作品页面](https://alpinabook.ru/catalog/book-pishi-sokrashchay-2025/)。不声称已独立核验所提供版本的ISBN。

[编辑试验——英文原文](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/editorial-skill-pilot/STUDY.md)使用了从该作品所提供OCR表示派生出的项目技能。同一派生包也在[依赖闭包研究——英文原文](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/STUDY.md)中接受考察；其[布局保留报告](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/evidence/layout-preservation-report.json)和[依赖图](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/evidence/dependency-graph.json)保留来源的记录名称与依赖元数据。

所提供文件的文件名含“2025”，数字输入则包含427条物理页面记录。这些描述与OCR书目行不同，不能认证版本。出版方当前页面标识作品，但不能认证私下提供的那个确切文件。本出版物分发试验自己的文本、评估和包元数据，而不分发图书或私有的来源派生工具集。

## 项目来源与证据 {#project-sources-and-evidence}

Pavel Valentov. **Knowledge Contract and Meaning Management: earlier publication corpus.** 仓库快照 [b50243b28e9ad7376e28c749a21479ef46ec9d60](https://github.com/Arcanada-one/knowledge-contract/tree/b50243b28e9ad7376e28c749a21479ef46ec9d60)。

[来源映射——英文原文](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/appendices/source-map/APPENDIX.md)记录从十四个早期论文文件和十份规范到当前阅读结构的迁移。[工程证据索引](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/evidence-index.json)将单项经验或分析性主张绑定到支持记录。每项研究说明哪些内容可公开重跑，哪些仅能作为保留报告查阅，以及哪些仍未测量。

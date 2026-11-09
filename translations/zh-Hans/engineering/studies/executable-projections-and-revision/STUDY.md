---
name: "executable-projections-and-revision"
title: "可执行投影：可寻址修订与图最小性的边界"
artifact: "engineering-study"
edition: "1.1"
author: "Pavel Valentov"
language: "zh-Hans"
license: "CC-BY-4.0"
description: "有限消费者检查、成对代理任务、可寻址修订与图最小性的边界。"
study_type: "finite-consumer-and-agent-case-study"
source_review_state: "internally-reviewed"
translation_of: "engineering/studies/executable-projections-and-revision/STUDY.md"
source_commit: "a0450428704fcd41b411203f2fc88c06c779610b"
source_git_blob: "2d247a01d4dbd6a1d1491d2b54464336c6fef190"
translation_status: "author-draft"
---

# 可执行投影：可寻址修订与图最小性的边界 {#executable-projections-addressable-revisions-and-the-limits-of-graph-minimality}

## 摘要 {#abstract}

本报告综合三个已完成的开发阶段：数据包读取、定向修订和可执行部分提取。第一阶段记录十二项标准违反；主层结果的重建状态为十项完整、38项部分、三项拒绝和六项不支持。后续开发与回归边界测试集在修订后的阅读器和评分规则下，38次调用满足全部772项已声明检查。定向修订比较将十个案例模板应用于三本书，产生三十个图与行式表示的配对案例，结果相同。随后，一个经过102项有限控制检查的消费者，从十个新代理响应中提取24个指定投影；响应组织为五个相关案例对。两种表示在全部五个主要案例中都成功，但使用的粗粒度评分规则在所评投影上已达到上限。这些有界结果并不确立图表示的优越性或一般语义完整性。事后发现表明：最小的可达实体集合，仍可能在实体文本内部含有不必要的断言。

## 问题与设计演进 {#question-and-design-progression}

工程问题是：消费者能否检索到有用的部分结果，而不默默丢弃其条件、不把新的评估当作原始溯源，也不按任意顺序解决身份歧义。科学论证见英文原文[《语境组装》](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/retrieval-and-context-composition/PAPER.md)、[《知识修订》](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/revision-and-governance/PAPER.md)和[《证据与证伪》](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/evidence-and-falsification/PAPER.md)。

各阶段改变了接口、映射、案例，有时也改变评估规则。因此，它们作为相关的开发研究来报告。连续阶段的分数不构成对某项单独干预所引起改进的受控估计。历史结果保持不变。

## 初始阅读器：四种不同的失败机制 {#initial-reader-four-distinct-failure-mechanisms}

保存的[初始阅读器研究](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/evidence/historical-reader-study-source.json)记录57次主层调用、786项满足和十二项违反的标准。其重建状态为十项完整、38项部分、三项拒绝、六项不支持。这些状态标签不能与满足全部义务互换。公开摘要未将每个主层状态绑定到预先声明的预期状态，因此不能确定38项部分结果以及九项拒绝／不支持结果中，哪些是计划内而非意外结果。案例级别的这一区分仍不可得。

另一个[图书层报告](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/source-transcription-and-uncertainty/evidence/historical-ocr-reader-report.json)记录十八次调用、252项满足和零项违反的标准：六个基础案例为完整结果，十二个刻意损坏或不完整的控制按设计为部分结果。调用、重建状态和嵌套标准具有不同分母；标准计数不是1,050个独立任务，也不是准确率估计。该阶段没有以原生模型为被试的试验，也没有人类受试者试验。

十二项违反分为四组。五项涉及地址解析到占位符与内容实际可用之间的区别。三项涉及记录与关系端点之间不一致的修订身份推导。两项涉及指向数据包内部的诊断指针与传输封套之间的区别。另外两项涉及在记录冲突时仍选择第一个候选项。

| 原始失败组 | 记录的违反数 | 后续修正范围 |
| --- | ---: | --- |
| 占位符地址与可用内容 | 5 | 契约／评分规则区分和阅读器变更：分开地址解析、内容状态及可用性 |
| 不一致的推导修订版 | 3 | 阅读器规范化，以及一致应用于记录与端点的显式推导规则 |
| 不明确的指针坐标空间 | 2 | 诊断输出和契约说明：标识数据包／封套空间及表示哈希 |
| 冲突时选择首个候选项 | 2 | 解析器行为和输出契约：保留候选集合及显式歧义 |

英文来源将这一表述作为原报告四组分析的摘要；本译文翻译该摘要。它并未把后续每项成功单独归因于代码或评分规则，因为两者都有变化，尤其是五个占位符案例。

这一分析很重要，因为这些违反并非都意味着内容丢失。在指针案例中，无效的外层哈希已被检测出，但诊断坐标系不明确。在占位符案例中，关系被保留，阅读器与判定基准对`resolved`的含义却不同。修订对这些机制的解释，并不会抹去已记录的违反。

## 修订阅读器的边界 {#revised-reader-boundaries}

后来的阅读器将地址解析、内容状态、内容可用性、适用性和权限分开。提供的空字符串、零或`false`不再被当作字段缺失。来源声明的修订版仍区别于推导修订版及其推导规则。诊断指针注明坐标空间和表示哈希。冲突候选项保留为明确集合，因此记录顺序不能默默创造唯一身份。

[边界报告](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/evidence/reader-boundary-report.json)包含38次开发调用：26个与修订同时准备的反例，以及来自早期失败的十二个回归案例。所有调用均满足声明的检查，总计772项满足、零项违反标准。一个成对置换控制保留了歧义与候选值哈希集合。修订后的映射和评分规则与较早版本不同，因此这既不是留出数据上的验收测试，也不是只更换测量工具的复测。历史记录中的“qualified”表示这些有限的声明边界得到检查，不确立任意未来数据包上的正确性。

## 定向修订与强替代方案 {#targeted-revision-and-a-strong-alternative}

[定向修订报告](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/evidence/targeted-revision-comparison.json)比较显式依赖图与含有相同实质依赖和条件的平面行。二者共用证据验证器与序列化器。实验差异在于如何选择受影响记录。这是刻意设置的强简单替代方案，而不是被剥夺相关信息的表示。

十种不同模板应用于三本书，产生三十个配对案例和六十次执行。六十次均得到预期结果；对于每个模板的三个图书实例，两种表示均一致。共享验证器和序列化器把比较限制在记录选择步骤，并帮助解释：一旦两个选择器选出相同记录，结果为何相同。三十个配对不代表三十种独立设计的机制。

| 模板类别 | 结果相同的成对图书实例 |
| --- | ---: |
| 来源或契约未改变 | 3/3 |
| 有效的表示映射 | 3/3 |
| 错误的表示映射 | 3/3 |
| 缺少表示映射 | 3/3 |
| 空表示映射 | 3/3 |
| 来源文本改变 | 3/3 |
| 图像字节改变 | 3/3 |
| 必需的不确定性得到保留 | 3/3 |
| 必需的不确定性被省略 | 3/3 |
| 必需的不确定性未知 | 3/3 |

输出包括36项映射未决评估和十二项契约未知评估，因为它们是特定控制中声明的结果。这些状态是可见结果，而不是隐藏在通过总数背后的失败。[可寻址性研究来源](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/evidence/addressability-study-source.json)描述了设计和共享机制；机器比较保留每个模板及每本书的身份。

来源变更产生单独的候选修订版，并保留旧记录与历史。新评估没有虚构当前使用权限。计时来自一次本地调用，包含共享解码，不是模型延迟或产品成本。该比较没有在所测范围内确立图表示的优势。

## 可执行投影契约 {#executable-projection-contract}

后续有限消费者接受同一契约的两种表示：节点加类型化边，或带类型化依赖的行。它将二者规范化，并从具名根节点计算必需闭包。关系区分内容要求、限定以及评估要求。来源附属项也区分内容支持与评估依据。用于评估卡片的证据，不得默默成为卡片内容所派生自的来源。

类型化身份携带记录与修订版标识符、创建契约和先前版本引用。评估另行标识其精确目标、评估契约与结论。请求可以在单独历史层中包含历史修订版。历史载荷及其出向关系得到保留，而不是被编辑成让旧记录符合新规则。

缺失地址、无效来源、格式错误输入，或超出声明实体预算的闭包，在该配置下会产生阻止结果，不提供可用的部分输出。明确表示的语义未知仍可以是有用内容；它本身不是模式错误。最小性相对于已声明关系而言。消费者不能仅因作者本应包含某项限定，就推断出被省略的限定。

## 新响应之前的消费者合格性检查 {#consumer-qualification-before-the-new-responses}

[合格性报告](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/evidence/consumer-qualification-report.json)记录51类控制的两种形式：102次执行，包含24项预期接受和78项预期阻止。全部与预期相符，规范化结果在全部51对中一致。另行编写、未导入消费者的验证程序计算预期结构闭包，并拒绝十二个刻意损坏的输出。验证程序与消费者在同一会话、同一代理家族内开发。代码路径分离有用，但不能确立外部独立性，也不能排除共享假设。

报告披露三项冻结前修正：为无效JSON类型增加显式防护；不再允许Python中布尔值与数字的相等性掩盖被保留JSON类型的变化；规范化输出明确保留关系和类型化链接。这些变更先于新的被研究响应。有限控制并不证明消费者对每种可能输入或任意非JSON的Python对象都正确。

## 五组代理案例对 {#five-agent-case-pairs}

下一阶段在取得十个来自新代理上下文的响应之前，固定了输入、请求、参考材料、评分规则、实现和运行顺序。每个案例及表示各有一个响应，不进行纠正性的被试重试。基于来源的任务有意彼此相关，只涉及四类来源，不是十个独立样本。

| 案例 | 部分提取必须保留的内容 | 观察结果 |
| --- | --- | --- |
| 未经审查的航海描述 | 有用描述及不确定记号、缺失上下文 | 两个主投影都保留不确定性与来源限制 |
| 实验性烹饪修订 | 已变更分支、其旧值及另一个独立分支 | 指定的当前、历史和独立分支提取分别保留相应绑定 |
| 已改变的评估契约 | 原创建契约与旧结论、新评估及经过合格性确认的新修订版 | 旧溯源保持完整，新评估与新修订版分开 |
| 航海表格 | 选定值、插值依据、符号及未知适用性 | 两种形式在全部指定视图中保留了指定值与依据 |
| 电路图像 | 可见模块与连接结构，不虚构数值信号 | 两种形式都保留定性观察及数值推断的限制 |

[实测结果记录](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/evidence/agent-projection-results.json)报告了24个可用投影，由前述另行编写的验证程序检查。每个投影在保真度和任务正确性两条评分轴上都取得最高分：全部24个投影的两条轴均达到上限。小于一个评分步长的差异无法由该工具分辨。对于每种形式，五个案例中的全部指定视图均成功，全部五组配对的主要结果相同。十个原始响应并不相同；结果分数一致，并不意味着表示相同，也不意味着在更精细评估下质量相同。

语义审查者看到了表示形式，参加过设计审查，并属于同一代理家族。没有人工专家审查。共有84项嵌套关键义务判断；它们不是84个独立实验。精确运行时模型修订版、解码参数、随机种子、词元消耗、延迟和计算成本均不可得。保存的输出由可见最终答案复制，而非原生API流捕获。因此，该研究提供的是观察到的代理案例系列，不是可复现的原生模型基准。

## 断言层级最小性的反例 {#counterexample-to-claim-level-minimality}

评估后发现，两个行式投影在共享适用性限定内部包含额外数值陈述。因此，提取一个选定表格值时也携带了另一个值，即使后者专属计算节点未被选中。额外值是正确的，冻结的评分规则允许额外正确内容。原始评分保持不变；这一观察另行记录。

这反驳了从实体级闭包推出断言级最小性的做法。最小可达节点集，不意味着节点内部每个句子都必要，也不意味着每个附带断言的全部依据都在投影中。后续契约可以给单个断言配置地址，或限制共享限定的作用域。该改进是反例的启示，不是本次运行已经展示的性质。

## 证据与复现边界 {#evidence-and-reproduction-boundaries}

精确机器摘要和保留的来源视图随研究提供；[origin.json](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/evidence/origin.json)区分原始JSON字节和重建的文字视图。[离线重放报告](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/evidence/offline-projection-replay-report.json)记录一次历史提取包重放，其中全部24个投影匹配并通过独立编写的验证程序。它明确报告没有新的被研究模型调用、OCR、原生试验或语义评估。该重放是对保存输出的确定性处理。

这一公开证据目录不含完整原始来源包、候选响应和冻结请求，也不含完整原生运行环境。具体而言，冻结的合成控制包、原始消费者、单独的验证程序及变异制品均未提供。它们的缺失是项目自有材料尚待恢复和发布的缺口，不是声称书籍权利禁止发布合成控制或软件。其绑定哈希与字节长度列在[恢复清单](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/historical-recovery-gaps.json)中；重写相似代码会产生新实验，而不是恢复历史实验。读者可以检查保存的数量与限制，但不能仅凭哈希推断完整重放环境。[公开闭包研究（英文原文）](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/STUDY.md)提供了一个可单独执行、仅使用元数据输入的图机制。

[投影研究来源](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/evidence/projection-study-source.json)、可寻址性来源及初始阅读器来源均为俄语文字视图。英文来源中的设计、四种失败机制、状态分布和限制，是对相关段落的英文摘要，并非经过完整独立审查的翻译；这一限制在本译文中保持。[证据语言索引](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/evidence-language-index.json)标识每个文件。代理评判的限制与[评估方法文献（英文原文）](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/reference/bibliography/BIBLIOGRAPHY.md#evaluation-methods)相关；本地评分规则并未复现那些基准。

## 结论 {#conclusion}

这些研究展示了在选定检索与修订操作中，对明确声明的内容、限定、评估角色和历史进行的有限保留。同时，它们提出了有用的反论据：简单表示可以得到相同结果；经过修正的评估器会改变分数的解释；图最小性不能约束文本内断言的数量。这些结果支持契约的明确义务，同时将比较有效性、任意根节点下的完整性、领域正确性以及产品使用授权留在已确立结论之外。定义汇总于[英文来源的术语表](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/reference/glossary/GLOSSARY.md)。

---
name: "dependency-closure-and-package-delivery"
title: "依赖闭包：可读制品布局与固定版本包的重放"
artifact: "engineering-study"
edition: "1.1"
author: "Pavel Valentov"
language: "zh-Hans"
license: "CC-BY-4.0"
description: "历史包证据与有限依赖图的公开穷举重放。"
study_type: "finite-graph-and-integration-evaluation"
source_review_state: "internally-reviewed"
translation_of: "engineering/studies/dependency-closure-and-package-delivery/STUDY.md"
source_commit: "a0450428704fcd41b411203f2fc88c06c779610b"
source_git_blob: "63078110074e82b47f76a8f132a3cfdcbfb555b1"
translation_status: "author-draft"
---

# 依赖闭包：可读制品布局与固定版本包的重放 {#dependency-closure-readable-artifact-layouts-and-a-pinned-package-replay}

## 摘要 {#abstract}

只有在选择某项制品时也交付其必需条件和依赖，任务包才有用。本研究在一个冻结的编辑知识包上考察这项义务；该包含110条记录和十二个技能根节点。保存的自测与44项普通检查的预期结果相符，其中21项预期接受、23项预期拒绝。另外两个结构边界反例按设计被接受，单独报告。依赖部分穷举了全部4,096个技能子集和24,576个单步包含对，与单独的不动点实现没有分歧。公开重放程序能够复现这一图计算部分，而不分发原书。后续元数据计算表明，实际编辑请求交付了110条记录中的108条，因此观察到的包并未展示小上下文。另一个迁移报告记录了全部110份载荷得到保留；一次固定版本的历史重放复现了尚需解决的预先准入决定。这些结果确立的是有界的图、布局和集成行为，而非语义完整性或代理的胜任能力。

## 交付问题 {#the-delivery-problem}

编辑技能可能依赖某条规则、该规则的适用条件、验收标准以及来源片段。仅选择顶层技能描述，可能省略使其适用的限定。消费者沿明确要求的依赖运行，并将导航另行处理。避免任意导航是一项设计动机，而不是这个包具有选择性或经济性的证据。保存的包源自所提供的Ilyakhov与Sarycheva著作《Пиши, сокращай》的OCR表示；[编辑来源说明（英文原文）](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/reference/bibliography/BIBLIOGRAPHY.md#editorial-input)标识了该材料。

本研究区分三种身份：制品的稳定身份、不可变的内容修订版，以及人类可读路径。重命名文件夹不必产生不同的知识。条件发生变化，则不能被当作外观性的重命名。科学义务见英文原文[《语境组装》](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/retrieval-and-context-composition/PAPER.md)、[《知识变换》](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/constrained-transformations/PAPER.md)和[《知识修订》](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/revision-and-governance/PAPER.md)。

## 模型与算法 {#model-and-algorithms}

设\(V\)为固定的有限制品记录集合，\(D(v)\)为记录\(v\)的必需依赖。对所选根集合\(S\)，预期闭包是满足下式的最小集合\(C(S)\)：

\[
S\subseteq C(S), \qquad v\in C(S)\Rightarrow D(v)\subseteq C(S).
\]

本次测试的配置只包含声明为`required`且使用`all`运算符的依赖组。允许选择替代项的依赖需要另一种选择政策，不能被默默解释成`all`。原始包加载时会检查依赖的身份、修订版、预期类型和载荷哈希。未知根节点和环会使消费者明确拒绝。

实现侧算法使用深度优先遍历，分别维护活动集合与已完成集合。参考实现反复计算

\[
S_{k+1}=S_k\cup\bigcup_{v\in S_k}D(v)
\]

直至集合不再增长。在有限图上，后者最多经过\(|V|\)次严格增长即终止。比较考察所声明依赖关系下的结果一致性、幂等性、单调性和并集等式。这些是图性质，不表示自然语言内容已经拥有完整的语义依赖模型。

## 穷举有限检查 {#exhaustive-finite-checks}

十二个可选择的技能根节点产生\(2^{12}=4,096\)个子集。自测检查每个子集，将消费者闭包与独立编写的参考实现比较，检查\(C(C(S))=C(S)\)，并检查该闭包是否等于各根节点闭包的并集。它还考察通过添加一个尚不存在的技能形成的每一对集合。这样的对共有\(12\cdot2^{11}=24,576\)个；每一对都必须满足较小集合的闭包包含于较大集合的闭包。

保存的[有限包自测](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/evidence/finite-package-selftest.json)记录了零项参考结果分歧、幂等性失败、并集失败或单调性失败。并集、幂等性和单调性是最小闭包的推论；对子集的遍历主要检查固定邻接关系上的实现，而不是提供数千项不同的语义观察。这些计数不是任务的独立样本，不能转换成任意知识完整的概率。

历史文件包含46行：44项普通检查，即21项预期接受和23项预期拒绝，以及两个被接受的信任边界反例。按[通用计数约定（英文原文）](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/README.md#counting-and-interpretation)，后两项不计入普通符合性。其他控制涉及过期审查绑定、受保护数字被修改、缺少变更依据、错误来源关系、遗漏关键限定、其他任务的上下文、过期的胜任能力依赖、在未提供执行者能力和权限的情况下尝试执行、包被篡改，以及不可变回执行为。合成的正面审查测试数据明确标记为合成，不构成真实审查者曾评估文本的证据。

两个被有意设计为通过的边界尤其有说明力。结构有效的规则可以陈述假命题。输出可以包含精确的受保护数字字符串，同时否定其含义。在相应的结构检查和字面保留检查中，检查器接受了这些输入。因此，结构符合性与精确字符串存在都不能替代语义审查。

## 图结果的公开复现 {#a-public-reproduction-of-the-graph-result}

[依赖图](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/evidence/dependency-graph.json)公开必需邻接数据和不透明顶点身份，不含制品正文、来源摘录、OCR或书籍图像。它在原始加载器检查冻结包引用的记录之后提取。文件记录其来源图、索引及加载器的哈希。提供的[重放程序](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/evidence/replay_closure.py)使用原始遍历规则，以及在同一出版流程中另行编写的不动点比较。这是算法分离，而非独立的外部重复研究。

在英文研究的目录中运行：

```bash
python3 evidence/replay_closure.py
```

[保存的公开重放结果](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/evidence/public-closure-replay.json)复现4,096次子集比较和24,576次包含检查，并拒绝未知根节点和构造出的环。这是对提取出的历史图进行的一次新重放，并不声称重跑全部46项历史检查、验证原书或观察新的模型响应。不需要额外Python软件包或网络调用。

## 交付记录数与故障控制 {#delivered-record-counts-and-fault-controls}

最小不动点方法的背景以及程序变异的有限作用，见[方法论参考文献（英文原文）](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/reference/bibliography/BIBLIOGRAPHY.md#evaluation-methods)。以下测量针对这一保存的有限图及这些已声明故障。

[审查后的图检查](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/checks/check_closure_size_and_mutations.py)在同一个110顶点、405边的图上计算闭包大小。其[保存的输出](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/checks/closure-size-and-mutation-check.json)覆盖每个技能、两个角色、两个方案蓝图，以及顶层代理根节点。计数描述记录数，而非字节、词元或注意力成本。可读名称来自保存的路径迁移；历史ID保留在机器结果中以供追溯。

| 所选根节点 | 交付记录数 |
| --- | ---: |
| 单个技能根节点 | 110条中的45–57条（40.9–51.8%） |
| 十二个技能合在一起 | 102 |
| 主编辑角色 | 105 |
| 审查角色 | 57 |
| 编辑方案蓝图 | 73 |
| 顶层助手 | 110 |
| 编辑试验：编辑方案蓝图加两个角色 | 108（98.2%） |

按历史选择器顺序，十二个单技能计数为45、57、45、49、53、51、51、47、49、55、53和45；输出将每个计数映射到可读名称。试验声明应用了十二个已交付技能中的五个。这并不展示依赖闭包能够产生紧凑的任务上下文。它确立的是声明闭包的交付；依赖粒度和角色级根节点能否减小包的规模，仍未测量。

同一个新检查测试三种明确的实现变异：不再拒绝环、跳过必需子节点，以及把未知根节点当作叶节点。两节点环、三节点链和未知根控制，将三种变异体全部与未修改遍历区分开来。这些是审查后进行的合成故障控制，与历史44项普通检查和两个边界反例分开。它们说明对这三种缺陷敏感，而非一般意义上的变异测试充分性。

```bash
python3 checks/check_closure_size_and_mutations.py
```

## 可读布局迁移 {#readable-layout-migration}

后来的编辑工具集布局以描述性路径替换代码式文件名，同时保留底层制品身份和载荷修订版。[保留报告](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/evidence/layout-preservation-report.json)记录了迁移工具关于全部110条记录字节相等以及来源字节不变的断言。每行存储一个哈希和`bytes_equal: true`，而不是分别观察到的旧、新两个哈希。因此，仅凭该报告无法独立重新确立两套字节序列。旧路径与新路径明确列出，使读者能区分报告中的位置迁移和修订；原始报告保留原样，没有添加虚构观察。

[布局符合性报告](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/evidence/layout-conformance-report.json)记录九项成功测试。其正面清单包括110份文档档案、110条记录、二十个操作闭包、四项约束、163个Markdown文件、1,294个本地链接和24个适配器。这些属于不同的清单单位，不能相加形成一个成功率。其他检查考察别名等价性、四十个来源定位符，以及将约束作为关键内容交付。

阴性控制删除约束档案、从交付中删除必需约束、引入无效slug、在更新文件哈希的同时破坏链接，以及造成索引与登记表不一致。每项都被预期的诊断类别拒绝。更新哈希却破坏链接的控制是一个有用反例：校验和在内部一致，并不意味着导航可用。

## 历史包重放 {#historical-package-replay}

一项集成门禁固定到较早的包，而非后来的布局。把该门禁用于文件夹成员已经变化的版本，就会比较不同对象。因此，保存的[历史重放](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/evidence/historical-package-replay.json)使用精确的早期目标清单和[声明环境](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/evidence/historical-replay-environment.json)。五个命令的退出码与预期序列一致：0、0、0、3、0。来源与临时重放副本各自保留了全部239个已检查载荷文件，均未改变。

退出码3属于预先准入。其预期决定是`needs_resolution`，待解决问题的代码是`R_EXPECTED_HEAD`。复现该决定意味着门禁复现了指定的未决条件，而不是包已被服务器接受。记录明确报告：没有新的模型运行、没有新的文本结果、没有外部语义审查、未评估服务器准入，而且生产就绪状态为假。

记录的环境为Linux上的Python 3.12.14，以及五个精确的依赖版本。该环境断言属于固定版本的历史重放。后来的布局也含有使用版本范围的依赖；匹配早期环境，并不能确立精确的后期环境。

## 断言、证据与边界 {#claim-evidence-and-boundary}

| 断言 | 证据 | 反例或故障控制 | 限制 |
| --- | --- | --- | --- |
| 必需闭包遵循声明的图 | 穷举子集重放和单独实现的不动点算法 | 未知根、环以及三个新实现变异体 | 声明图的完整性是外部前提 |
| 迁移工具报告内容未变 | 110项相等断言，每行一个哈希 | 布局与索引不一致 | 报告没有分别固定旧、新两套字节序列 |
| 约束确实得到交付 | 明确的关键约束检查 | 缺少档案或缺少交付 | 只覆盖四项已声明约束 |
| 包哈希相同意味着包可用 | 导航与预先准入检查 | 更新哈希后的坏链接；未决的预期头版本 | 完整性、导航和准入仍是不同事项 |
| 精确字符串意味着意义得到保留 | 使用同一数字字符串却刻意表达相反含义 | 字面检查接受了该内容 | 仍然需要语义审查者 |

## 结论 {#conclusion}

本研究提供可复现的有限依赖结果，以及可供检查的布局和包重放记录。它说明，可读制品名称能够与稳定身份并存，约束也可以在已交付闭包中保持可见。同时，它保留了理解这些结果所需的失败边界：完整图遍历可能遵循不完整的标注；交付的可能是几乎整个包；完好的包仍可能需要解决未决问题；保留字符串的修改仍可能改变含义。[编辑试验（英文原文）](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/editorial-skill-pilot/STUDY.md)另行评估实际文本。定义汇总于[英文来源的术语表](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/reference/glossary/GLOSSARY.md)。

原始报告身份保留在[origin.json](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/evidence/origin.json)。证据大多是使用英文键的JSON；原有俄语描述保留不变。[语言索引](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/evidence-language-index.json)标识各文件。本文的英文来源提供了错误规则和反转含义控制的英文摘要；这里翻译的是这些摘要，并未重新验证原始证据。新生成的图测量和变异结果在[更正记录](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/review-corrections.json)中分别标识。

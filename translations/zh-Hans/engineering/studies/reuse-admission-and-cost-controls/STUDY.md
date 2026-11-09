---
name: "reuse-admission-and-cost-controls"
title: "复用经济性：受控复用中的准入反例与缓存命中的成本"
artifact: "engineering-study"
edition: "1.1"
author: "Pavel Valentov"
language: "zh-Hans"
license: "CC-BY-4.0"
description: "可执行的准入反例，以及明确核算成本的解析盈亏平衡计算。"
study_type: "analytical-engineering-study"
source_review_state: "internally-reviewed"
translation_of: "engineering/studies/reuse-admission-and-cost-controls/STUDY.md"
source_commit: "a0450428704fcd41b411203f2fc88c06c779610b"
source_git_blob: "67ab4b55faf9f42df2d6d7214bbbe4f30c143a8e"
translation_status: "author-draft"
---

# 复用经济性：受控复用中的准入反例与缓存命中的成本 {#controlled-reuse-admission-counterexamples-and-the-cost-of-a-cache-hit}

## 摘要 {#abstract}

复用准备好的知识制品可以避免部分工作，但标识符匹配或命中率高，并不能确立复用适当或经济。本解析研究提出明确的准入条件，以及涉及缺失依赖、搜索范围变化、当前权限、时间边界和重叠成本主张的反例。同质成本模型给出一个有条件的盈亏平衡恒等式。公开代码提供算术演算示例，以及涵盖全部九类具名门禁的有限合成检查器，其中包括缺失门禁反例。它不报告实测模型节省、生产吞吐量或已部署的授权系统。贡献是可供检查的一组义务与反例，并明确区分解析推论和需要观察支持的经验主张。

## 问题与对象 {#question-and-objects}

问题在于：何时能够为新请求使用保留制品，而不丢失其要求、不夸大证据、也不隐藏验证成本。科学模型见英文原文[《知识复用》](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/controlled-knowledge-reuse/PAPER.md)和[《知识效用》](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/knowledge-utility/PAPER.md)。[保存的条件性质来源](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/reuse-admission-and-cost-controls/evidence/reuse-properties-source.json)记录了支撑本分析的原始假设、论证和反例。

一次构建可表示为

\[
\operatorname{Compile}(b,q,S)\rightarrow(a,D,E,L),
\]

其中\(b\)是配方，\(q\)是请求，\(S\)是声明的来源快照，\(a\)是准备好的修订版，\(D\)是其实质依赖，\(E\)是证据，\(L\)是覆盖、损失及停止信息。后续请求\(q'\)需要在当前政策和上下文下另行作出复用决定。相似性可以检索候选项，却不能确立适合性。

构建依赖解释制品如何产生。准入依赖决定现在能否提供或应用它。访问决定变化可以在不改变制品文本的情况下禁止交付。生成器版本变化不一定要求重建每个未受影响的制品。这些决定需要明确的相关性规则，而不是一个不加区分的时效性标记。

## 先准入，后优化 {#admission-before-optimization}

[状态模型（英文原文）](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/specifications/status-model/SPECIFICATION.md)区分`pass`、`fail`、`unknown`和`not_applicable`。一项强制义务由`pass`解除，或由`not_applicable`加上已识别规则及证明该精确范围内排除有效的证据解除。缺乏依据的排除、观察缺失，以及适用条件下的未知，均不能解除它。这里使用九类门禁：完整性、结果类别、任务要求、实质依赖等价、当前访问、时间政策、允许的变换、模态交付，以及预算。有限公开检查器有意将九项全部设为适用，因此要求每项都有明确`pass`，并拒绝没有适用性见证的`not_applicable`。它不从任意文本中推断适用性。

当请求明确允许部分内容且缺口保持可见时，部分内容可以获准。但这不会让附着于所选内容的条件变成可选。预测效用再高，也不能把失败的强制条件变成许可。经济优化只能在可准入替代方案集合内进行。

复用策略包括精确复用、模板实例化、重新验证后复用、重建、绕过缓存以及拒绝复用。这些策略不是第二套操作结果词汇：操作仍按契约报告`success`、`partial`、`refused`、`failed`或`unresolved`。决定重新验证，本身不等于允许在必要检查完成之前交付。实例化结果有自己的身份，并且必须在替换之后检查。

## 决定设计的反例 {#counterexamples-that-determine-the-design}

| 拟采用的捷径 | 反例 | 必需的区分 |
| --- | --- | --- |
| 列出的依赖未变，所以结果保留 | 遗漏的图例改变了未变数字或符号的含义 | 依赖完整性是实质前提，不是清单标签 |
| 否定答案具有空依赖集 | 穷举搜索未找到匹配后，又加入一个匹配条目 | 不存在、计数和精确top-k依赖搜索域成员及政策 |
| 已被接受的载荷可以发给另一个请求者 | 请求者、租户、资源范围或权限已改变 | 内容身份与当前交付权限不同 |
| 未过期缓存寿命可以覆盖权限服务不可用 | 权限结果变为未知期间，一项许可被撤销 | 当前权限未知，不默认继承旧成功 |
| 缓存的完成消息可以完成另一个任务 | 消息描述的是较早尝试和外部效果 | 保留内容不是新的执行事件 |
| 频繁读取证明持续有效 | 重复命中不增加来源评估 | 访问统计与验证时间不同 |

保留主张必然是有条件的。假设一个可靠的先前评估，在状态\(s_0\)下为请求\(q\)确立了制品\(a\)的性质\(P_1,\ldots,P_m\)。这些性质的完整依赖与解释接口必须在\(s_1\)中保持等价；每项性质对请求的依赖，必须经由已声明的组成部分因子化，而\(q\)与新请求\(q'\)在这些组成部分上相同。对于变换关系\(T(a,a')\)允许的每个输出\(a'\)，变换都必须保留这些性质。这些前提确立其保留；但是，为\(q'\)准入还要求保留性质能够推出\(q'\)的每项强制要求均被解除，在使用不适用性排除时有有效见证，并满足当前授权和交付义务。旧的已验证性质集不能为未覆盖的新要求提供正当依据。遗漏实际依赖，或无依据地假定旧评估可靠，会使一项前提失效；名为`complete_manifest`的布尔字段不能确立任一前提。[受控复用定理（英文原文）](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/controlled-knowledge-reuse/PAPER.md)给出相应的条件论证。

适合性还具有方向性。完整的非空集合可以通过允许的投影支持存在性答案。一个已知成员不能确立整个集合、其数量或不存在其他成员。对称的相似性分数不能提供缺失的蕴涵。

## 时间、并发与状态 {#time-concurrency-and-state}

制品生命周期、驻留状态、时效性和当前使用资格是不同评估。有效的保留修订版可能处于冷存储或暂时不可用；驻留且具有时效性的制品也可能不允许该请求者访问。历史答案可以有意使用固定的旧修订版，同时遵守当前访问限制。

严格当前政策需要声明一个一致性时点：在该点，相关来源头版本和权限被视为当前。有限陈旧政策需要明确允许的范围和年龄。两者都不能默默忽略已知撤回、损坏、不兼容或实质性未决缺口。缓存命中更新使用统计，不重置底层来源被检查的时间。[HTTP缓存时效性](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/reference/bibliography/BIBLIOGRAPHY.md#http-caching)与[陈旧响应扩展](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/reference/bibliography/BIBLIOGRAPHY.md#stale-http-responses)只提供有限技术类比，不授予绕过知识或权限检查的许可。

检查与交付之间也存在间隙。验证之后、提供结果之前，权限或依赖可能改变。实现必须说明其一致性边界，例如使用经过检查的纪元、租约或事务性发布协议。这些机制需要自身的并发测试。这里的解析义务不声称某个分布式服务已经正确实现它们。

## 精确成本模型 {#an-exact-cost-model}

考虑固定核算期内具有相等可准入质量、且核算类别互不重叠的同质请求。令\(N\)为请求数，\(G\)为冷启动可准入路径的成本，\(c_v\)为每个请求增加的候选搜索与准入成本，\(c_r\)为可用复用的其余成本，\(\rho\)为可用复用比例。令\(B\)、\(MG\)、\(I\)和\(S\)分别表示准备、额外后台构建、失效处理和存储成本。所有成本采用同一声明单位且非负，并且\(0\leq\rho\leq1\)。保留的1.0版示例使用\(V,R,h\)表示\(c_v,c_r,\rho\)；原始数据和代码保持不变。于是

\[
C_0=NG,
\]

\[
C_1=B+Nc_v+N\rho c_r+N(1-\rho)G+MG+I+S.
\]

以\(F(N)=B+MG+I+S\)表示开销；它可能在声明的核算期内随请求数变化。令\(d=\rho(G-c_r)-c_v\)，相减得到

\[
C_0-C_1=Nd-F(N).
\]

严格节省要求\(Nd>F(N)\)。闭式阈值\(\lfloor F/d\rfloor+1\)只适用于该核算期内开销\(F\)、预期命中比例\(\rho\)以及单位成本均独立于\(N\)，且\(d>0\)的情形。若\(d\leq0\)，在这个同质模型中增加请求数无法收回非负开销。对实际观察应使用整数命中数\(H_N\)：节省为\(H_N(G-c_r)-Nc_v-F(N)\)。分数形式的预期命中数不是观察到的事件数。若存储增长为\(S(N)=sN\)，其他固定开销\(F_0\)仅在\(d>s\)时能收回，阈值为\(\lfloor F_0/(d-s)\rfloor+1\)；\(d\leq s\)时不存在这种阈值。

| 虚构情景 | 参数 | 代数结果 |
| --- | --- | --- |
| 高命中率但验证昂贵 | \(N=100,\rho=0.9,G=10,c_r=1,c_v=9,F=0\) | 冷路径成本1,000；复用成本1,090；损失90 |
| 正边际收益且有准备成本 | \(N=100,\rho=0.9,G=10,c_r=1,c_v=1,F=100\) | 冷路径成本1,000；复用成本390；节省610 |
| 零边际收益 | \(N=100,\rho=0.5,G=10,c_r=2,c_v=4,F=100\) | 固定损失100仍然存在 |
| 存储随请求数增长 | 同样的正边际收益参数，但\(F(N)=100+8N\) | \(N=100\)时复用成本1,190；损失190；在这些恒定费率下没有盈利请求数 |

这些是以虚构成本单位计算的精确算术示例，不是价格、实测词元账单或项目性能估计。异质请求需要适当分层求和，不能代入不兼容的平均值。

## 效用与重复计算 {#utility-and-double-counting}

计算节省本身并不等于任务净价值。质量损失、额外审查、结果延迟和下游伤害，需要明确的效用政策与证据。如果它们的值未知，把它们设为零会产生缺乏依据的收益。如果一条路径违反硬约束，有利的货币估计也不能使其获准。

成本还需要共享基线。假设冷路径操作成本为十个单位，供应商缓存将其降为六个，使用准备好的制品将其降为一个。分别算出的两项节省——四个和九个——不能相加，变成从十单位操作中节省十三单位。如果制品命中消除了模型调用，那么该不存在调用上的供应商缓存节省并不是又一项观察到的收益。资源事件、重试、存储与共享基础设施需要互不重叠的核算，或明确的分摊规则。

仅凭引用数、交付制品数或完成任务数，不能推出因果贡献。例如，[编辑试验（英文原文）](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/editorial-skill-pilot/STUDY.md)在两种条件下均观察到可用输出，结果为平局。缺少资源和结果观察，就不能把它转化为实测经济收益。

## 公开示例与主张限制 {#public-examples-and-claim-limits}

修正后的[反例程序](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/reuse-admission-and-cost-controls/checks/check_admission_and_cost.py)列出全部九类强制门禁。它检查一项全部通过的阳性对照，以及27项单独的缺失、失败或未知门禁变异；还检查格式错误输入，包括仅含一个门禁的映射和无正当依据的`not_applicable`。所提供状态仍然只是本地输入，不会认证权限服务或确立现实世界适用性。精确有理数成本计算是恒等式的演算示例，包括线性增长的存储开销，不是经济假设的经验验证。小型依赖与不存在性模型在虚构输入上说明反例。

在英文研究目录中运行：

```bash
python3 checks/check_admission_and_cost.py
```

[保存的修正结果](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/reuse-admission-and-cost-controls/checks/admission-and-cost-check.json)是一项新的确定性演示。较早的[1.0版程序](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/reuse-admission-and-cost-controls/evidence/replay_reuse_counterexamples.py)与[结果](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/reuse-admission-and-cost-controls/evidence/public-reuse-counterexamples.json)作为历史证据逐字节保留：该程序只检查三个提供的门禁，在遗漏必需门禁时错误接受了非空子集。它的六项失败／未知控制不能确立缺失门禁义务。修正程序替代的是这一局部门禁演示，不改变任何历史模型结果。[更正记录](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/review-corrections.json)单独标识新文件。

原始性质来源是俄语渲染文字视图，其来源哈希与表示哈希分别记录于[origin.json](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/reuse-admission-and-cost-controls/evidence/origin.json)。英文来源中，上述准入条件、依赖反例和时间限制属于英文摘要与当前论证；本译文传达这些内容。加强后的新请求覆盖前提是一项明确更正，不是声称旧来源已经证明它。[证据语言索引](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/evidence-language-index.json)记录各文件语言。没有任何公开程序重新运行早期生产系统。

## 结论 {#conclusion}

受控复用需要两个决定：一条路径是否满足自身义务，以及它是否优于其他可准入路径。逻辑反例指出第一项决定中不能遗漏的输入；成本恒等式说明第二项决定需要测量什么。完成的解析结果恰恰因为允许否定答案而有用：缓存可以正确却不经济，可以在虚构假设下经济却在实践中尚未测量，也可以表面高效但不具备准入资格。术语汇总于[英文来源的术语表](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/reference/glossary/GLOSSARY.md)。

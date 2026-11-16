---
name: "semantic-bridge-conformance"
title: "来源规则检验：有限模型中的来源绑定、备选解读与操作组合"
short_title: "来源规则检验"
subtitle: "有限模型中的来源绑定、备选解读与操作组合"
artifact: "engineering-study"
edition: "1.1"
author: "Pavel Valentov"
language: "zh-Hans"
license: "CC-BY-4.0"
description: "针对给定解释实际执行的来源绑定、布尔预期结果判定和操作组合的有限检查，并保留发现的输入处理错误。"
study_type: "finite-implementation-evaluation"
review_state: "unreviewed"
source_review_state: "internally-reviewed; external independence not verified"
translation_of: "engineering/studies/semantic-bridge-conformance/STUDY.md"
source_commit: "8c7cd3bc1247998cb9554c568da26949da31b749"
source_git_blob: "a08166d551ca43c7e2e203d9408604ec43bd4799"
translation_status: "author-draft"
---

# 来源规则检验：有限模型中的来源绑定、备选解读与操作组合 {#source-rule-checks-finite-binding-alternatives-and-operation-composition}

## 问题与结果 {#question-and-result}

作用范围受限的使用程序，能否在可检查的计算中保留显式给定的规则、规则的例外、备选解读以及未知观察？[《语义桥接》规范](../../../../../engineering/specifications/semantic-bridge/SPECIFICATION.md)定义了被测试的配置。其输入是一份已编写的 UTF-8 来源，其中包含 `NOTE` 和 `RULE` 行，以及一个给定的解释包。它不是从不受限的自然语言文本中自动提取意义的工具。

在全部 64 种给定的可用性与取值配置下，该实现对三变量的全部 256 个布尔函数得到的结果，与另行编写的布尔掩码预期结果判定器一致：共 **16,384 条计算记录**。第二个完整有限族，在全部 16 种可用性配置下，覆盖二变量函数的全部 256 个有序对：共 **4,096 条计算记录**。四项集成检查将计算得到的表连接到现有的有限关系与结果集合几何 API。来源、解释包和过程检查保留拒绝、相关性以及尚未评估的性质。另一次输入审查发现并随后关闭了一个实际的 JSON 解码器缺陷；最初的失败记录仍可查阅。

这些是不同的有限空间和检查，不是独立的实证试验，也不是具备通用语言理解能力的证据。精确的程序身份、计数和执行限制保留在以下记录中。

## 材料、操作与假设 {#materials-operation-and-assumptions}

[实现](../../../../../tools/semantic_bridge.py)最多读取 65,536 字节的来源和 131,072 字节的解释包。每一条完整的 `RULE id: expression` 行恰好对应一种解读。来源摘要、字节选择器和引用的行必须一致；所有声明的规则单元都被保留。仅有有效的来源哈希，不能为删掉 `UNLESS suspended` 的截断前缀提供正当依据。

各个解读是同一查询的备选解释。每个局部原子都显式绑定到一个观察身份。已知值固定相应的布尔变量；未知值和不予披露的值都允许假与真，同时保留两者不同的可用性状态。同一观察的别名共享其值。求值器解析受支持语言的完整表达式，保留 `NOT`、`AND`、`OR` 以及定义的约定 `a UNLESS b = a AND NOT b`。最多四种解读在同一个有限世界网格上求值。

所观察的性质包括字节绑定、受控语言解析、有序真值表、可能值集合，以及同一世界中的分歧。给定的来源选择、解释、归属标注、指称对象和事实值仍然是假设。每份报告都将来源语义保真性、归属标注的真实性、现实世界中的真值和当前权限保持为 `NOT_ASSESSED`，同时保持 `effects_authorized=false`。计算得到的假值是有效的求值结果，不是过程错误。没有解读、存在不受支持的必需解读，或来源绑定无效时，都不会产生经计算的真值。

## 独立的预期结果方法 {#independent-expected-result-method}

[预期结果判定套件](../../../../../tools/test_semantic_bridge.py)从布尔真值掩码出发，将其编码为规范析取范式。它根据给定的已知、未知和不予披露记录筛选世界掩码。在计算预期结果时，它不使用实现本身的词法分析器、AST 遍历或求值器。对于备选解读，它对相应掩码取 XOR，并将结果限制在共同允许的世界内。

该预期结果判定器由一项与实现开发分开的任务编写。两者使用同一个控制器、模型家族和主机。这是实现结构与预期结果结构的分离，不是外部独立性，也不是对自然语言标注进行的盲法评估。公式编码、测试数据生成和预期结果代码，仍是可供检查的假设。

| 有限族 | 实际清单 | 观察结果 |
| --- | --- | --- |
| 三变量布尔函数 | 256 个函数 × 64 种可用性与取值配置 | 16,384 条记录；55,296 次已完成的世界求值；2,952 个 `TRUE`、2,952 个 `FALSE`、10,480 个 `UNDETERMINED` |
| 二变量备选解读对 | 256 个有序对 × 16 种可用性配置 | 4,096 条记录；18,432 次解读与世界组合求值；1,088 次一致，3,008 次同一世界中的分歧 |
| 可能值集合相同、条件行为不同 | 备选解读族的一个子集 | 984 条记录具有相同的可能值集合，但在同一世界中存在分歧 |
| 来源与过程检查 | 同一套件中的具名测试 | 精确单元、过时哈希、CRLF/UTF-8 选择器、不完整清单、不受支持的备选解读、严格 JSON、别名、常量、有限界限，以及实际 CLI 退出与报告行为 |

[有限运行回执](../../../../../engineering/studies/semantic-bridge-conformance/evidence/finite-oracle.json)记录这些实际计数和程序哈希。计数会与声明的完整清单核对；省略一个函数或一种可用性配置，不能在缩小分母后仍留下看似成功的结果。枚举覆盖的是以 DNF 编码的上述函数族，不是每一棵可接受的语法树，也不是每一种可能的来源字符串。

## 原创来源示例与实际 CLI 使用 {#original-source-examples-and-actual-cli-use}

四组另行编写的来源与解释包保存在[示例](../../../../../engineering/studies/semantic-bridge-conformance/evidence/examples/lending.en.txt)中。英语、俄语和简体中文的借用来源包含不同的原创 `NOTE` 文本，以及相同的、显式编写的受控规则。它们是示意性的语言版本，不是经过测量的翻译语料。精确的字节选择器随 UTF-8 输入而变化，并由实际使用程序检查。

[CLI 执行记录](../../../../../engineering/studies/semantic-bridge-conformance/evidence/example-cli-runs.json)保留四个新启动的本地进程的原样 stdout、来源和解释包哈希、退出码，以及实现身份。

| 来源 | 给定的不确定性 | 实际计算 |
| --- | --- | --- |
| [英语借用示例](../../../../../engineering/studies/semantic-bridge-conformance/evidence/examples/lending.en.txt) | 暂停状态未知；会员资格和培训均为真 | 两个世界，`UNDETERMINED`；单一解读内部没有分歧 |
| [俄语借用示例](../../../../../engineering/studies/semantic-bridge-conformance/evidence/examples/lending.ru.txt) | 相同的作者给定布尔假设 | 两个世界，`UNDETERMINED`；不作跨语言保真性结论 |
| [中文借用示例](../../../../../engineering/studies/semantic-bridge-conformance/evidence/examples/lending.zh-Hans.txt) | 相同的作者给定布尔假设 | 两个世界，`UNDETERMINED`；不作跨语言保真性结论 |
| [两种资格条件解读](../../../../../engineering/studies/semantic-bridge-conformance/evidence/examples/alternatives.en.txt) | 一个固定世界；两个给定作用域 | 一个世界、两个不同答案、`UNDETERMINED`，且解读之间有分歧 |

预期结果判定器还有三个原创的语言包装阳性测试用例，保存在其自己的回执中。它们是另一些输入，受控计算结果确定为真。这两组输入都不是恢复出的历史证据，也不是 LLM 提取运行。保留不透明的 `NOTE` 文本，不意味着已经解释了其中的指令、嵌套引用或必需媒体。

## 与代数和几何的连接 {#connection-to-algebra-and-geometry}

[四项集成测试](../../../../../tools/test_semantic_bridge_relations.py)将实际的桥接输出用作 [semantic_relations.py](../../../../../tools/semantic_relations.py) 的输入。它们的[实际运行回执](../../../../../engineering/studies/semantic-bridge-conformance/evidence/RELATIONS_INTEGRATION_RUN.json)和[原样测试日志](../../../../../engineering/studies/semantic-bridge-conformance/evidence/RELATIONS_INTEGRATION_TESTS.txt)在执行前后绑定两个模块和测试文件。其最大的载体集合有八个状态，未超过关系 API 现有的十二状态限制。

第一，借用规则的八世界表给出了从世界索引到布尔状态 `0=false`、`1=true` 的显式关系。观察 `(member AND trained, suspended)` 产生四个大小分别为 1、1、3、3 的类，以及相容的商关系。去掉暂停状态的观察后，会得到一对违反条件的代表元：保留的资格条件相同，例外状态不同，计算输出也不同。这是对现有代表元替换判据的实际使用。

第二，将该关系与另行计算的 `NOT flag` 关系复合，所得结果与直接计算借用规则的否定一致。当声明的中间布尔接口兼容时，商关系的复合与对具体结果取商一致。不兼容的载体集合会被拒绝。

第三，将第二个计算限制为已知 `flag=true`，会留下一个局部行，其索引为零，含义却是真。行号不能等同于语义上的布尔标签。向共享布尔载体集合的显式嵌入，给出一条成功路径和七个空像。非空结果集合的几何配置正确地拒绝这些空像。不存在成功的关系路径，不等于假值、观察到的拒绝或未知信息。

第四，两种资格条件解读具有相同的全局结果集合 `{false,true}`、为零的豪斯多夫距离，以及为零的集值利普希茨常数。然而，它们对齐后的表仍在八个共同世界中的两个世界上出现分歧。对汇总集合的投影丢弃了世界标签；这些集合之间距离为零，并不能确立条件可替换性。这与[《知识变换》](../../../../../papers/constrained-transformations/PAPER.md)和[《意义几何》](../../../../../papers/geometry-of-semantic-representations/PAPER.md)声明的观察范围一致，不是针对其条件性结果的反例。

## 已解决的输入失败与审查边界 {#resolved-input-failure-and-review-boundary}

[非作者审查](../../../../../reviews/semantic-bridge-20261114/non-author/REVIEW.md)保留了一个 5,341 字节的 JSON 解释包，其中一个字节选择器含有 5,000 位整数。最初的实现让 Python 整数转换的 `ValueError` 泄漏出来：退出码为 1，出现异常回溯，没有 JSON 结果。该文件小于解释包的字节上限，因此常规大小校验不能解决这一失败。

修正后的读取器保留其显式 `BridgeError` 代码，并将 JSON 解码器的其他 `ValueError` 和 `RecursionError` 失败规范化为结构化拒绝。同一个已保存的解释包现在产生退出码 2、`INVALID`、`malformed_json`，没有经计算的真值，且 stderr 为空。套件增加了一个在真实子进程中运行的回归测试，并显式固定 Python 的整数限制。原始模块、失败输出和修正后的输出分别保留；第一次失败没有被成功结果覆盖。

审查者在修正后的实现上完成了 30 个另行编写的输入与状态探测，在已检查的范围内没有发现尚存的阻断问题。这些探测与算术枚举不同，也不是对安全性或正确性的穷尽证明。[审查记录](../../../../../reviews/semantic-bridge-20261114/non-author/review-record.json)标识了精确的实现和规范草稿。随后分配了稳定的要求标识符，但没有改变条款含义。编辑审查还缩小了规范中关于下游准入的验收表格行的范围：该配置仍将权限保留为未评估状态，也没有实现下游准入使用程序；并未声称执行过此类操作。

## 复现与解释 {#reproduction-and-interpretation}

从仓库根目录运行：

```sh
python3 -B -m unittest tools.test_semantic_bridge tools.test_semantic_bridge_relations -v
python3 -B tools/run_semantic_bridge_controls.py --output /tmp/kc-semantic-bridge-new-run.json
python3 -B tools/semantic_bridge.py \
  --source engineering/studies/semantic-bridge-conformance/evidence/examples/lending.en.txt \
  --packet engineering/studies/semantic-bridge-conformance/evidence/examples/lending.en.packet.json
```

使用新的回执路径：有限运行器拒绝覆盖已有文件，并检查执行期间程序字节没有改变。其 `checkout_head` 是本地基准修订版，不是尚未提交的候选文件的身份；各程序的哈希标识实际计算。完整单元测试套件、审查探测和 CLI 演示各有记录，并非全部体现在有限运行器的回执中。

全部保留的证据文件由 [origin.json](../../../../../engineering/studies/semantic-bridge-conformance/evidence/origin.json)列出。初次集成运行只有运行后收集的源代码哈希，当时实现工作正在并行进行；该运行仍被明确标记为未绑定。一次新运行在执行前后均记录哈希，提供了可用的回执。任何保留的旧报告都不会被悄悄改标为对最终实现的检查。

该结果完成了《语义桥接》中来源绑定和受控计算的一个有限范围部分。一般性的人类意义到形式表示的保真性、量词、单位、时间、嵌套归属标注、必需媒体、完整制品集成以及智能体的实际使用，仍是开放问题。现有的智能体状态工作、发布决策、网站交付、索引准入和原生 KC2 准入各有独立标准。没有运行付费实验；成本为 `NOT_MEASURED`。

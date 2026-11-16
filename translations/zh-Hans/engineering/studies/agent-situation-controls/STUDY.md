---
name: "agent-situation-controls"
title: "上下文检查：情境状态与上下文投影的有限检查"
short_title: "上下文检查"
subtitle: "情境状态与上下文投影的有限检查"
artifact: "engineering-study"
edition: "1.1"
author: "Pavel Valentov"
language: "zh-Hans"
license: "CC-BY-4.0"
status: "research-draft"
description: "对小型情境状态模型实际执行的作者编写的有限检查，包括保留的开发缺陷和修正后的前提绑定。"
translation_of: "engineering/studies/agent-situation-controls/STUDY.md"
source_commit: "8c7cd3bc1247998cb9554c568da26949da31b749"
source_git_blob: "b875953c066fcbb99e1579f76dfcd29c5bc9ef9d"
source_review_state: "author-produced evidence; bounded same-controller review; independent acceptance NOT_VERIFIED"
translation_status: "author-draft"
sources:
  - "Knowledge Contract project corpus and publication edition"
---

# 上下文检查：情境状态与上下文投影的有限检查 {#context-controls-finite-checks-of-situation-state-and-context-projection}

**作者：** Pavel Valentov · **出版版本：** 1.1 · **审阅状态：** 作者生成的证据，经过同一控制器下的有限范围审阅及测试框架修复；独立验收为 NOT_VERIFIED。

## 1. 问题与有限主张 {#1-question-and-bounded-claim}

本研究考察一个小型确定性模型在明确编写的有限输入上，是否保持其声明的观测时间、作用范围、依赖关系及上下文预算规则。它配合拟议的[智能体情境](../../../../../papers/agent-situation/PAPER.md)架构。本研究不检验大语言模型（LLM）是否更好地理解环境、完成更多真实任务或节省资金。

修正后的实现与**作者编写的 21 个预期检查结果中的 21 个**一致，并检测到**三项故意停用的防护中的三项**，变异运行没有发生异常。最初的 18 项检查也全部通过，但后续审阅仍发现了一个真实的延迟推导缺陷。这两个事实都很关键：新增后的用例展示了修正，而最初错误的安心感则限制了任何有限检查通过结果所能确立的结论。

## 2. 材料与来源 {#2-materials-and-provenance}

本研究中的所有观测、预期值和程序均为这次有限演示新编写而成。研究未使用第三方数据集、私人账户、外部服务或实际运行的权限来源。代码遵循本仓库的 Apache-2.0 条款，原创文字和证据遵循其现有署名政策。

最初的[设计输入](../../../../../engineering/studies/agent-situation-controls/checks/DESIGN_INPUT.md)在本次工作会话的实现开始前记录了十八类拟定检查。这一先后顺序是作者记录，并非独立预注册。实现代理同时编写了运行程序和字面明确的[预期结果](../../../../../engineering/studies/agent-situation-controls/checks/expected.json)。第二个代理在同一控制器、同一模型家族下检查论文和代码，复现了两个缺陷，并复查了修正。这样的分工有助于审阅，但实际独立性仍为 NOT_VERIFIED。

[来源清单](../../../../../engineering/studies/agent-situation-controls/evidence/origin.json)通过精确的 SHA-256 和字节大小绑定每个当前证据文件。最初的三个条目保持不变；清单最初的精确字节保存在[历史来源清单](../../../../../engineering/studies/agent-situation-controls/development/inventory-baseline/origin.json)中。历史[内容清单](../../../../../engineering/studies/agent-situation-controls/MANIFEST.json)标识那次执行时的原型，包括保留的开发版本。原始[有限运行记录](../../../../../engineering/studies/agent-situation-controls/evidence/finite-run.json)包含源文件摘要、运行环境、命令、完整操作轨迹、预期结果、计数和限制。记录中的运行环境是 Python 3.12.14。历史执行记录和内容清单保持不变；当前来源清单加入了带日期的后续记录。原始运行程序的精确字节也保存在 [inventory-baseline](../../../../../engineering/studies/agent-situation-controls/development/inventory-baseline/README.md) 中；当前运行程序及其后续执行由[检查清单修复凭据](../../../../../engineering/studies/agent-situation-controls/evidence/20261114-inventory-receipt.json)单独绑定。

## 3. 模型与执行方法 {#3-model-and-execution-method}

参考模型使用一个非负整数时钟域，以及合成的作用范围和来源标签。它维护各生产者的序列顺序、带来源归属的值、显式的未知和冲突状态、TTL 策略及本地依赖版本绑定。其投影器计算必需闭包，检查就绪状态，并且只将可选记录放入剩余的抽象容量。

模型不发出外部请求。它没有身份认证、真实授权、效果派发器、LLM、分布式时钟协议或持久化恢复机制。来源标签只是测试样例标识。结构上就绪但权限值为“假”的样例不授权任何事项。

运行程序对照人工编写的预期结果进行评估；只要某项普通检查失败，或未能检测到一个预设的错误变体，它就以非零状态码退出。三个错误变体分别停用新鲜度检查、强制依赖闭包检查或作用范围检查。观测到的不一致是故意设置的负对照，并非意外的运行时异常。

| 检查组 | 用例 | 观测范围 |
| --- | --- | --- |
| 时间、不确定性与重放 | 1–4 | TTL 边界、真正的刷新、未知与假值/零的区别、重放时的数据年龄以及时钟异常 |
| 顺序与相互冲突的来源 | 5–7 | 较旧/相等的生产者序号、独立来源之间的冲突以及重复标识 |
| 依赖关系与事件相关性 | 8–10 | 相关更新与无关更新、心跳行为以及账户作用范围 |
| 上下文容量与遗漏 | 11–13 | 容量恰好容纳闭包、少一个单位时失败、未知的必需记录以及稳定的可选记录顺序 |
| 关键使用与未解决的结果 | 14–18 | 撤销样例、已变更的前提、过期兜底检查、定向刷新以及未知的效果结果 |
| 审阅补充的回归检查 | 19–21 | 绑定缺失/过时/不可能成立的延迟推导、有效的延迟正例以及拒绝被修改的快照 |

被比较的 87 个顶层结果字段是这些检查内部的嵌套检查，并非 87 个独立样本。三个变异体采用单独的分母；将它们与普通检查合并为一个成功百分比会造成误导。

## 4. 保留的失败与修正 {#4-preserved-failure-and-correction}

在原始模型中，派生观测会绑定到其到达时当前有效的依赖版本。审阅执行了以下序列：

1. 在时间 0 观测到 `a = old`。
2. 在时间 5 将其替换为 `a = new`。
3. 在时间 10 收到 `b = derived from OLD a`，其声明的观测时间为 0。
4. 请求一个需要 `b` 的上下文。

原始实现返回了 `KNOWN` 和 `READY`，将旧推导绑定到其前提的版本 2。最初的十八项检查没有涵盖这种到达顺序。[复现的反例](../../../../../engineering/studies/agent-situation-controls/development/v1/delayed-derivation-counterexample.json)、原始源代码及最初通过的运行记录仍保留在 [development/v1](../../../../../engineering/studies/agent-situation-controls/development/v1/README.md) 中。

修正要求显式的前提版本绑定，而不是在接收时进行绑定。绑定缺失会产生 `UNBOUND_DEPENDENCIES`；绑定过时会产生 `INVALIDATED`；若被绑定的前提首次接收时间晚于声明的推导时间，则产生 `INVALID_DERIVATION_TIME`。检查 20 确认，只要前提匹配且在相应时间已经可用，延迟推导仍可为 `READY`。因此，这项修正并非不加区分地拒绝所有延迟观测。

第二项审阅探测从已发出的快照中移除了版本条目，并更改了一个前提。旧校验器返回了 `VALID`。修正后的校验器将数据与本地已发出快照的规范内容比较，拒绝被修改或遗漏的版本绑定数据。这是进程内完整性检查，并非密码学认证或分布式安全边界。

[审阅记录](../../../../../reviews/agent-situation/20261114-REVIEW.md)保留了最初发现、精确的源文件哈希、修正处置及同一控制器下单独进行的复查。

## 5. 结果 {#5-results}

后续审阅发现，运行程序关于完整性的主张还有一个独立缺陷：仅移除最后一个已注册的可调用项，就会让截断式配对只执行 21 个样例中的 20 个，却仍报告成功。它还会计算全部 87 个样例字段，而不是已执行检查所对应的 84 个字段。这项遗漏探测并未否定历史上完整的 21/21 执行；缺陷涉及注册丢失后测试框架会接受什么。[检查清单审阅](../../../../../reviews/agent-situation/20261114-INVENTORY.md)记录了这一隔离探测及其修正。

后续版本在执行前校验声明的 ID、可调用项注册和样例之间的一一对应关系，按 ID 绑定负对照，检查完整的已执行检查清单，并统计实际执行的字段谓词检查。九项行为检查涵盖完整注册和重新排序的注册、缺失/多余/不匹配/重复条目，以及对未执行比较的计数。情境模型及其字面明确的预期结果均未改变。

| 观测 | 实际结果 | 解释 |
| --- | --- | --- |
| 最初的作者编写检查集 | 18/18 匹配 | 最初的检查集漏掉了一个真实的延迟推导缺陷 |
| 最初停用的防护 | 3/3 被检测到 | 所选的新鲜度、闭包和作用范围用例能够区分这些变体 |
| 审阅反例 | 过时推导错误地返回 READY | 一个超出最初检查集到达顺序覆盖范围的具体失败 |
| 修正后的作者编写检查集 | 21/21 匹配；0 项失败 | 十八项原始检查，加上三项明确标识的审阅补充检查 |
| 修正后的停用防护 | 3/3 被检测到；0 个异常 | 所选负对照仍具有区分能力 |
| 单独的内部复查 | 21/21 和 3/3 | 同一控制器下由非作者进行检查和执行；独立性为 NOT_VERIFIED |
| 检查清单遗漏探测 | 面对 21 个样例，报告 20/20 成功 | 独立的测试框架完整性与计数缺陷，作为不利证据保留 |
| 检查清单修复后的重放 | 21/21；3/3 个变异体；87 个已执行字段谓词检查 | 相同的有限模型和预期结果，注册经过校验 |
| 检查清单/计数检查 | 9/9 | 对修复后测试框架的单独行为检查；在同一控制器下编写 |
| 模型中的 LLM/网络/效果调用 | 0 | 未进行智能体表现或真实世界行动实验 |

这些结果仅确立记录中的有限谓词，不估计总体失败率，不证明完全正确性，不确立论文的实证假设，也不验证实际运行的消费者。没有测得 LLM 词元成本、资金节省或生产环境效用结果。

## 6. 不改写保留证据的复现 {#6-reproduction-without-rewriting-retained-evidence}

从仓库根目录将本研究复制到临时执行目录。运行程序会写入 JSON 报告和一份简要执行记录；在副本中运行可以保持已提交的历史证据不变。

```sh
KC_SITUATION_RUN="$(mktemp -d)"
cp -R engineering/studies/agent-situation-controls/. "$KC_SITUATION_RUN/"
python3 -B "$KC_SITUATION_RUN/checks/check_agent_situation.py" --evidence "$KC_SITUATION_RUN/evidence/finite-run.json"
python3 -B -m unittest discover -s engineering/studies/agent-situation-controls/checks -p test_inventory.py -v
```

预期终端摘要为 `FINITE_CONTROLS_PASS`，21/21 项检查通过，3/3 项停用防护被检测到。重放时的时间戳、运行环境字符串及命令路径可能不同；应比较声明的结果和源文件哈希，不应要求不同环境中的证据字节完全相同。

归档的开发版本故意保留缺陷。其最初的运行程序演示了原有的十八个通过用例；保留的反例指出被遗漏的行为。不要用修正后的结果覆盖该记录。

## 7. 限制与下一步研究 {#7-limits-and-next-research-step}

这些检查采用作者编写且参考了实现的情境。来源序列、版本计数器及时间都存在于单一进程中；没有独立的生产者证明。冲突采用保守方式处理，没有按权限对来源排序的解析器。推导时间可行性规则使用本模型的接收历史，可能比具有经过认证的历史证据的真实分布式系统更保守。

必需闭包的完整性受限于声明图的完整性。抽象整数预算并非词元计数。模型可能误解正确的上下文；一个始终拒绝的系统也可能显得保守却毫无用处。因此，拟议的[智能体实验](../../../../../roadmap/agent-situation/EXPERIMENT.md)纳入了有效完成、不必要拒绝、依据过时信息采取的行动及完整维护成本，并设置强的确定性基线。

该实验尚未执行。本研究支持对有限设计继续开发和审阅，并不支持规范性准入、扩大自主权限，或发表已经证明智能体改进的结论。

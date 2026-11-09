---
name: "source-transcription-and-uncertainty"
title: "不确定性保留：可复现的转录不等于保留不确定性"
artifact: "engineering-study"
edition: "1.1"
author: "Pavel Valentov"
language: "zh-Hans"
license: "CC-BY-4.0"
description: "保存的生成描述、丢失的不确定性，以及可复现的合成投影反例。"
study_type: "corpus-and-projection-audit"
source_review_state: "internally-reviewed"
translation_of: "engineering/studies/source-transcription-and-uncertainty/STUDY.md"
source_commit: "2b5bcff544fea5d1752ff009933e4ce0305dad8b"
source_git_blob: "8ca885fc3f144d89e95e4813868fd953450f1f71"
translation_status: "author-draft"
---

# 不确定性保留：可复现的转录不等于保留不确定性 {#reproducible-transcription-is-not-preservation-of-uncertainty}

## 摘要 {#abstract}

对三个图书导出包的审计发现，可读Markdown能够逐字节重建，同时却省略了附着于生成插图描述的全部153个明确记录的不确定性字段。底层结构化记录仍保持完好。另一个派生投影保留了全部153个字段，并把全部917条描述标记为已生成且未经审查；仅删除记录的插入内容，就能恢复原始可读字节。这是针对表示缺陷及其局部修正的一项已经完成的有限演示。它不测量OCR准确率、不验证描述，也不确立图存储优于实现相同规则的序列化器。本报告将语料观察、后续导出集成、未解决的溯源缺陷，以及一个公开的小型投影规则合成示例分开叙述。

## 问题与来源范围 {#question-and-source-scope}

问题在于，变换是否交付了与读者实际收到的内容相联系的限定。保存来源档案对审计是必要的，但不能使派生文档中被省略的限定变得可见。科学区分见英文原文[《意义与语境》](../../../../../papers/semantic-objects-and-context/PAPER.md)和[《知识变换》](../../../../../papers/constrained-transformations/PAPER.md)。

所研究的语料涵盖烹饪、航海和电气自动化。保存的来源审计标识了1952年版《Книга о вкусной и здоровой пище》、G. I. Fain于1977年出版的《Навигация, лоция и мореходная астрономия》，以及V. A. Timofeev于1964年出版的《Сто схемных задач по автоматике》。日期和页数描述的是观察到的版本，不确立建议在当下的适用性，也不授权实际使用。

| 导出类别 | 页锚点 | 导入的生成描述 | 非空不确定性字段 |
| --- | ---: | ---: | ---: |
| 烹饪 | 456 | 374 | 111 |
| 航海 | 289 | 319 | 16 |
| 电气自动化 | 154 | 224 | 26 |
| 总计 | 899 | 917 | 153 |

[结构化语料报告](../../../../../engineering/studies/source-transcription-and-uncertainty/evidence/structural-corpus-report.json)支持这些计数。页面、描述和不确定性字段是不同单位，不是1,969项经独立验证的观察；页锚点也不是针对该页的专家判断。

结构构建器与验证器共用一个词法表格检测器。因此，它们的表格计数一致，不构成对表格识别的独立验证。报告还记录，这次结构检查没有进行图像字节检查；声明图像哈希的一致性是元数据观察。

## 审计与变换方法 {#audit-and-transformation-method}

[语料审计](../../../../../engineering/studies/source-transcription-and-uncertainty/evidence/corpus-audit-source.json)检查了39个文件，每份导出十三个。其中33个文件的预期大小和哈希记录在导出回执中，全部匹配。其余README与回执文件由观察者固定身份；没有把任何回执视为能够认证其自身字节。

观察者从来源文档、编辑账本和结构化插图记录重建可读输出。目标可读文本用于比较，而非插入所生成的输出。重建覆盖174项记录的编辑、航海导出中的七项斜体包裹映射、三项从图注到图像替代文本的复制，以及生成描述。三个可读文件均与保存的目标逐字节相同。

映射在检查可用示例后才形成。这是已知数据上的重建，不是对生产者的盲式程序合格性确认。每项重放的编辑操作仍保留未经审查状态。可逆性确立了操作如何改变表示，并未确立编辑在语言上的正确性。

重要反例出现在插图投影中。可读模板输出描述、存在时的用途，以及识别出的图中文字，却不输出单独保存的`uncertain`字段。全部153个非空值均未出现在对应的可读描述中。这一发现针对该精确字段和投影，并不声称每条描述都没有任何审慎表述，也不声称JSON来源已经被毁坏。

## 将不确定性保留作为可检验义务 {#preserving-uncertainty-as-a-testable-obligation}

对于记录\(r\)及其明确限定\(u(r)\)，相关要求是：交付的投影应包含该限定，或者明确声明获准的损失。另一个对象的字节身份相同，不能满足这项要求。投影可以完全可复现，同时始终省略同一个字段。

因此，修正性派生结果引入了一条狭义规则：在每个生成描述之后插入声明的已生成／未经审查状态；当`uncertain`非空时，插入带明确标签的精确字段值。每次插入都关联输入行、记录哈希、资产身份、锚点和输出范围。来源文本和原始可读文件得到保留。

变换配置与预期计数在生成之前固定，但在审计已经揭示缺陷之后才制定。[派生报告](../../../../../engineering/studies/source-transcription-and-uncertainty/evidence/uncertainty-projection-source.json)记录如下结果：

| 义务 | 观察结果 | 边界 |
| --- | --- | --- |
| 保留已生成／未经审查状态 | 917/917条描述已标记 | 标签并不独立评估描述 |
| 保留每个非空不确定性值 | 153/153个精确值已交付 | 这些是未经审查的模型陈述，不是校准过的概率 |
| 保留之前的可读表示 | 仅删除声明的插入内容，即恢复三个原始文件 | 实验针对这一指定变换 |
| 保持来源输入不变 | 保存的全部39个来源文件哈希未变 | 完整性与来源正确性不同 |

这次变换没有新的OCR、被研究模型调用或人工领域审查。导入的模型描述原已存在于导出中。新调用数量为零，不能被解释为语料中没有模型生成材料。

## 各领域的后果 {#domain-specific-consequences}

三个领域暴露了不同依赖。烹饪指令中的限定可能属于某个配料分支或后续上菜操作；合并分支或移动动作，即使保留熟悉的词语，也可能改变程序。航海中的表格或示意图可能依赖图例、符号约定、前一页及对具体仪器的适用性。精确转录数值本身不能交付这些条件。在电路图中，可见连接能够支持定性描述，但在缺少输入值和运行上下文时，数值输出仍然未知。

这些示例用于形成工程义务，而非提出新的烹饪、航海或电路设计建议。后来的[投影研究（英文原文）](../../../../../engineering/studies/executable-projections-and-revision/STUDY.md)评估了涉及这些依赖的若干选定任务。两项研究均未把历史书籍的年代视为自动证明错误，也未把年代视为足以授权当代行动的理由。

## 溯源缺陷与后续集成 {#trace-defects-and-later-integration}

审计也发现了未解决的可寻址问题。在5,538个质量标记中，所观察映射寻址了5,518个；十六个表格或公式偏移和四个孤立标记仍未解决。某个标记消失，并不被计为OCR已修复；它可能反映文本变化、诊断变化，或缺少溯源。

另一个从原始数据到文档的分析，复现了烹饪和自动化导出的全部记录修正行。航海导出复现58行中的53行，剩余五行位于两个块内，无法唯一绑定到原始序列化。这些行并未被标记为五个OCR错误。证据不足以重建生产者的变换，这是另一类发现。

二十个未解决的质量标记加上这五个修正行，就是后续集成摘要中的25个未解决坐标轨迹。这一核对使清单相符，却不能把两类不同的溯源缺陷变成统一的OCR错误率。

后来的本地集成在两次运行中处理了同样的917条描述记录。每次都记录19,305项满足的字段检查和零项违反的字段检查，保留153个非空与764个空不确定性值。[集成摘要](../../../../../engineering/studies/source-transcription-and-uncertainty/evidence/local-export-integration-report.json)还保留最初控制结果：十六项中十五项得到预期结果。一个作者编写的控制在要求JSONL的地方提供了格式化JSON，导致拒绝发生在预期阶段之前。单独保存的修正随后测试了原本预期的缺少不确定性字段情形。替换后的控制区分了已验证新快照的可见性与尚未确认的持久性。

这项集成发生在导出之后，并未安装到上游OCR生产者中。没有测试物理断电持久性。七条被截断描述形成了定向审查队列；其余非空不确定性字段没有被自动等同于有缺陷或被截断的输出。

## 公开示例与保留证据 {#public-illustration-and-retained-evidence}

这里不再分发原书、OCR转录、提取的插图及完整的生成图书描述。项目编写的报告与汇总元数据使用可读文件名提供；[origin.json](../../../../../engineering/studies/source-transcription-and-uncertainty/evidence/origin.json)分别记录精确JSON身份和渲染文字表示的溯源。完整重放原始语料审计，需要指定的来源包以及原始运行器的完整依赖闭包；仅有报告并不能提供这些材料。

一个[修正后的公开示例](../../../../../engineering/studies/source-transcription-and-uncertainty/checks/demonstrate_uncertainty_projection.py)使用保留的1.0版程序中的四条虚构记录，其中两条具有非空不确定性。它将基础序列化器与[单独保存的字面目标](../../../../../engineering/studies/source-transcription-and-uncertainty/checks/synthetic-base.txt)比较，而不是让表达式与自身比较。修改描述的变异无法通过该比较。投影保留两个非空字段、标记全部四条记录、记录插入范围，并拒绝缺失的不确定性字段；精确删除这些插入内容能够恢复保存的目标，损坏插入范围则破坏恢复。这些是对虚构投影规则的有限检查，不是对历史“来源加编辑账本”流程的重建。在英文研究目录中运行：

```bash
python3 checks/demonstrate_uncertainty_projection.py
```

[保存的修正演示](../../../../../engineering/studies/source-transcription-and-uncertainty/checks/uncertainty-projection-check.json)是一项新的合成示例。[较早程序](../../../../../engineering/studies/source-transcription-and-uncertainty/evidence/replay_uncertainty_projection.py)和[较早结果](../../../../../engineering/studies/source-transcription-and-uncertainty/evidence/public-projection-demonstration.json)保持不变；其中`base_reconstruction_exact`谓词把相同构造与自身比较，未提供独立的重建证据。修正后的检查程序排除了这一推论。它的四条记录不替代917条历史描述，其检查也不加入历史语料总计。[更正记录](../../../../../engineering/studies/review-corrections.json)将新测试数据、代码和结果分别绑定。

语料审计与派生报告是俄语文字表示。在本研究的英文来源中，方法、缺失字段发现、坐标计数和程序合格性限制属于对相关段落的英文摘要；本译文翻译这些摘要，并未重新验证原始证据。原始来源没有被原地翻译或重写。[证据语言索引](../../../../../engineering/studies/evidence-language-index.json)记录每个文件的语言。

## 限制与结论 {#limits-and-conclusion}

语料的字符错误率（CER）与词错误率（WER）仍未测量。在声明对齐方式和参考单位划分后，两者分别把替换、删除和插入次数除以参考字符数或词数；历史审计既没有提供完整的标准转录，也没有提供这套测量协议。因此，`null`不意味着错误为零。[评估方法说明（英文原文）](../../../../../reference/bibliography/BIBLIOGRAPHY.md#evaluation-methods)列出了评分背景。

图像检查属于不同阶段和分母。较早的阅读器来源报告，在918幅已描述图像中检查了三幅选定PNG。后来的917条描述语料／结构审计没有检查图像字节。另一个可寻址性实验检查三幅选定JPEG，正如其[保留来源](../../../../../engineering/studies/executable-projections-and-revision/evidence/addressability-study-source.json)所述。它们都不是对整套图像的字节审计；较早的“三幅／918幅”观察不能重新归到后来的917记录检查中。既没有评估每一段OCR，也没有评估模型不确定性的校准。结构图构建产生了可寻址的来源结构，却没有因此提取出经过验证的语义知识图谱。

已经确立的工程结果是明确的：所选可读模板丢失了一个明确表示限定的字段；声明且可逆的投影在所检查的有限语料上保留了它。简单序列化器也能实现这一规则。证据支持明确的保留义务，并对把哈希等同于意义保留给出具体反例。它不确立更大架构的优越性。相关术语定义于[英文来源的术语表](../../../../../reference/glossary/GLOSSARY.md)。

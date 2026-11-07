---
name: "book-package"
title: "书籍包：来源身份、语义层与验证"
artifact: "engineering-specification"
edition: "1.1"
author: "Pavel Valentov"
language: "zh-Hans"
license: "CC-BY-4.0"
description: "具体的书籍包模式、可逆转换修订日志、语义层、权利边界和合成符合性检查。"
translation_of: "engineering/specifications/book-package/SPECIFICATION.md"
source_commit: "a0450428704fcd41b411203f2fc88c06c779610b"
source_git_blob: "f82c0b23c7f51949bb0127d8795d357e16229a4a"
translation_status: "author-draft"
---

# 书籍包：来源身份、语义层与验证 {#book-packages-source-identity-semantic-layers-and-validation}

**作者：**Pavel Valentov · **出版版本：**1.1

| 实现组件 | 范围 |
| --- | --- |
| [模式](../../../schemas/book-package.schema.json) | `book-package/2`，五类 `KCBook*/v2` 记录 |
| [验证器与投影](../../../tools/check_book_package.py) | 结构和跨文件检查、安全 Markdown 呈现、候选行 |
| [构建器](../../../tools/build_book_package.py) | 封装来源字节和提供的转换输出；不解释书籍 |
| [合成测试夹具](../../../schemas/fixtures/book-package/) | 虚构来源和负向记录；不含第三方书籍文本 |
| [符合性测试](../../../tools/test_book_package.py) · [审查回归测试](../../../tools/test_book_package_review.py) | 验证、可逆修订、权利、有界审查、呈现与状态推导 |

## 1. 目的与验证边界 {#1-purpose-and-validation-boundary}

书籍包将一个来源表示绑定到其转换结果、语义记录和审查观察。本规范定义已实现的 `book-package/2` 配置。大写要求用语遵循 [BCP 14](../../../reference/bibliography/BIBLIOGRAPHY.md#requirement-language)。记录验证不能确立转换保真度、语义真实性、实际审查独立性、出版权利或任务特定准入。

**BPK-R001.** 清单必须（MUST）声明 `validation_profile: book-package/2`，每条记录必须（MUST）使用对应的 `KCBookPackageManifest/v2`、`KCBookObject/v2`、`KCBookRelation/v2`、`KCBookEdit/v2` 或 `KCBookQuality/v2` 标签。

未知版本不受支持。

**BPK-R002.** 消费者不得（MUST NOT）默默将版本 1 记录重新解释为版本 2。

**知识契约准入运行时**依据[核心契约](../knowledge-contract-core/SPECIFICATION.md)决定用途。沿用的字面字段 `kc2_admission` 不是协议版本。

**BPK-R003.** 生产者记录中的此值必须（MUST）保持为 `not_measured`；生产者不能授予准入。

`not_measured` 映射为评估 `unknown`，理由为“no observation”，绝不能映射为 `pass`。

## 2. 布局与可逆修订 {#2-layout-and-reversible-edits}

```text
<package_id>/
  manifest.json
  document.md
  readable.md
  assets/
  edits.jsonl
  objects.jsonl
  relations.jsonl
  quality.json
```

**BPK-R004.** 包标识符必须（MUST）是可读的小写连字符短名，长度 3–96 个字符；禁止单个字母后紧跟数字的形式。

`release_id` 另行标识具体发行版。

**BPK-R005.** 组件路径必须（MUST）保持相对且位于包内，不得使用父目录穿越或符号链接。

`document.md` 是未修改的转换器输出。

**BPK-R006.** 接受的修订必须（MUST）以 `readable_md` 为目标；`asset_text` 没有受支持的摘要链语义，应被拒绝。

**BPK-R007.** 没有 `document_md` 和 `readable_md` 的包，不得（MUST NOT）包含已接受修订或已构建语义层。

**BPK-R008.** 每项已接受修订必须（MUST）具有非空原文和替换文本、锚点、依据、原因、行动主体、输入摘要和输出摘要。

**BPK-R009.** 在该步骤，原文必须（MUST）恰好出现一次，替换文本必须（MUST）在结果文本中恰好出现一次。

计数包含重叠出现：`aa` 在 `xaaay` 中出现两次。

**BPK-R010.** 按日志顺序应用已接受修订，必须（MUST）产生 `readable.md`；反向撤销这些修订，必须（MUST）精确恢复 `document.md`。

此基于搜索可逆性的配置不支持插入、删除或具有歧义的重复片段修订。

**BPK-R011.** JSON 读取器必须（MUST）拒绝任何深度上的重复对象成员名、非有限数字词元以及 UTF-8 BOM，使不同读取器不能从同一记录中选择不同权利或状态值。

**BPK-R012.** 所有比较和哈希必须（MUST）采用精确字节、严格 UTF-8 解码，并且不转换换行。

`\r\n`、`\r` 和 `\n` 保持不同。JSON Lines、`SHA256SUMS` 和检查列表只按 `\n` 分割；允许一个末尾换行，拒绝空 JSON Lines 和以 `\r` 结束的行。U+2028、U+0085 及其他控制字符不会成为额外记录分隔符。

修订生命周期为 `pending` → `accepted` 或 `rejected`；`stale` 表示基准不再匹配的过时提案，永不重放。已接受的日志条目不可变：后续纠正创建另一个条目或新的包发行版。过时提案所声明或与之重叠的依赖对象，在新的有效记录中重新评估前保持未决。

## 3. 身份与完整性观察 {#3-identity-and-integrity-observations}

`work_id` 标识作品，`edition_id` 标识版次和语言，`representation_id` 标识一个来源文件。翻译与不同版次保留各自身份和锚点，并以明确的 `related_works` 关系关联。表示记录来源摘要、大小、格式、完整性（`verified`、`mismatch`、`unverified`）和覆盖完整程度（`full`、`partial`、`bibliography_only`）。

**BPK-R013.** `verified` 或 `mismatch` 完整性声明必须（MUST）包含 `integrity_check`，其中有 `method`、`observer`、`checked_at`、`expected_sha256` 和 `observed_sha256`。

**BPK-R014.** 观察摘要必须（MUST）等于表示摘要。

已验证完整性要求预期与观察摘要相等；不匹配要求二者不同。

**BPK-R015.** 不得（MUST NOT）替换预期摘要来掩盖不匹配。

这是带归属的生产者观察。验证器检查其形状和内部一致性，不能认证预期摘要的权限依据，也不能重建不可用来源。构建器记录预期摘要是否由调用者提供。

**BPK-R016.** 生产环境消费者必须（MUST）在其声明信任边界上认证相关观察，然后才能将其作为来源完整性的证据。

**BPK-R017.** `document_md.input_sha256` 必须（MUST）等于表示摘要，并且其组件记录必须（MUST）注明转换器和版本。

没有受支持的转换器输出时，包保持 `adapter_required`；空文档或虚构文档不能替代转换。

## 4. 语义对象与侧面 {#4-semantic-objects-and-facets}

对象标识概念、断言、过程、图、表格、公式、代码块、示例或其他结构。

**BPK-R018.** 每个对象必须（MUST）保留其文本、语言、来源类别、至少一个来源锚点、状态，以及全部八个侧面字段：`representation_modes`、`content_kinds`、`discourse_functions`、`aboutness`、`source_position`、`semantic_operators`、`assessment_refs` 和 `governance_refs`。

限定信息在存在时承载条件和数值单位。

这些侧面实现[语义类型](../semantic-types/SPECIFICATION.md)的一个有限配置。表示模式包括 `text`、`image`、`audio`、`video`、`structured_data` 及其明确组合。来源立场为 `asserts`、`hypothesizes`、`presumes`、`denies`、`asks`、`reports_other_position`；`presumes` 表示预设，而不是假说的同义词。

**BPK-R019.** 运算符包括认识模态和义务模态、量词、否定、条件、例外和顺序；每个运算符必须（MUST）指出其作用域。

自由文本限定条件适用于整个对象，除非带作用域的运算符给出更精确的绑定。

十九种内容类别词元为 `definition`、`state_description`、`observation_measurement`、`generalization`、`explanatory_model`、`formal_model`、`procedure`、`structure_configuration`、`constraint_norm`、`goal_intent`、`preference_evaluation`、`argument_evidence`、`example`、`counterexample`、`question_problem_gap`、`narrative_episode`、`analogy_metaphor`、`hypothesis_interpretation` 和 `commitment_speech_act`。该词汇不是穷尽分类。

**BPK-R020.** 每个侧面必须（MUST）是带值的 `known`，或者是无值但有明确理由的 `unknown`、`not_applicable` 或 `withheld`。

按照该配置的基数规则，已知的表示模式、内容类别、话语功能和关于性不得为空。已知为空的运算符、评估引用或治理引用表示已经确立的空集合，只有在此含义下才被允许。

**BPK-R021.** 包审查中列出的对象必须（MUST）在已知的 `assessment_refs` 中包含该审查标识符；“已知为空”不能否认正在引用该对象的审查。

未知引用应保持未知，而非空值。

**BPK-R022.** `benchmark` 断言还必须（MUST）记录语料、设备、工具版本、设置、单位和模式。

结构上存在这些字段，不会验证其声明，也不会确立任务适用性。

## 5. 关系 {#5-relations}

关系连接同一包内两个存在且不同的对象，类别为 `defines`、`uses`、`variant_of`、`requires`、`compared_with` 或 `contradicts`。

**BPK-R023.** 每个关系必须（MUST）保留其条件、来源类别、证据、端点和状态。

每个关系至少有一个标为 `from`、`to` 或 `both` 的证据锚点。

**BPK-R024.** `contradicts` 关系必须（MUST）包含单独的 `from` 和 `to` 证据，防止单方面归属伪装成双方面发现。

**BPK-R025.** 连接过时或被拒绝端点的关系本身必须（MUST）为过时或被拒绝状态。

审查关系不会默默恢复其端点的有效性。

## 6. 证据锚点与来源格式 {#6-evidence-anchors-and-source-formats}

**BPK-R026.** 每个锚点必须（MUST）绑定与其清单相同的表示标识符和来源摘要。

已实现的格式到锚点映射是精确的：

| 锚点类别 | 精确格式词元 | 坐标 |
| --- | --- | --- |
| `page_bbox` | `pdf`, `djvu`, `ps` | 页码从 1 开始；具有正面积的边界框；原点和单位 |
| `spine_offset` | `epub` | `spine_item` 成员、可选元素路径、起止偏移 |
| `section_block` | `html`, `md`, `txt`, `tex` | 章节和块标识符 |
| `sheet_range` | `xlsx` | 工作表、单元格范围、`formula` / `cached_value` / `literal` 层 |
| `json_pointer` | `json` | RFC 6901 指针 |
| `slide_block` | `ppt`, `pptx` | 幻灯片编号和块标识符 |
| 无 | `zip`, `tar_gz`, `sevenz` | 仅保留不透明来源身份；不支持归档成员寻址 |

**BPK-R027.** 归档可以（MAY）作为需要适配器的不可用来源保留，但在本配置下不得（MUST NOT）承载转换器输出、修订或语义记录。

成员路径锚点需要单独版本化的扩展。DocC 不是格式词元；DocC JSON 文件使用 `json`。

验证器检查几何、顺序和声明的映射，不检查引用的来源位置是否存在或支持文本。提取另一表示会创建新绑定，不能据此复用先前表示的坐标。

## 7. 归属与安全呈现 {#7-attribution-and-safe-rendering}

来源类别为 `author_statement`、`editor_correction`、`generated_meaning`、`generated_description`、`our_experiment` 和 `model_inference`。

**BPK-R028.** 非作者来源必须（MUST）具有生成记录和 `presented_as_author: false`。

**BPK-R029.** 作者陈述不得（MUST NOT）携带生成记录。

对于作者陈述，`presented_as_author: true` 表示声称逐字引用；`false` 表示明确归属的转述。该标志本身从不确立引用保真度。

**BPK-R030.** 公共 Markdown 渲染器必须（MUST）保留每个对象和关系字段，包括限定信息、运算符作用域、来源立场、条件、锚点、生成和评估引用。

渲染器将每条完整记录输出为 JSON 字面量代码块，其围栏长度大于载荷中任何连续反引号。来源标签和记录标题由受控字段生成，并置于该容器之外。

**BPK-R031.** 载荷中的标题、HTML 或貌似来源标签的内容不得（MUST NOT）创建新的渲染记录结构。

每个非作者块都明确显示“GENERATED, not the author's statement”（“生成内容，并非作者陈述”）。

`document_md.contains_generated_text` 始终为 false；生成的意义和图像描述保持为独立派生物。缺失资源记录为 `missing_asset`，不得虚构路径或摘要。公共渲染器拒绝非 `author_open` 包。

## 8. 质量观察与就绪状态 {#8-quality-observations-and-readiness}

提取观察与语义观察保持分离，不存在合并评分。提取状态为 `pass`、`partial`、`adapter_required`、`failed`、`not_measured`。检查结果采用[状态模型](../status-model/SPECIFICATION.md)：`pass`、`fail`、`unknown`、`not_applicable`。每项检查都有唯一标识符和方法。

**BPK-R032.** `not_applicable` 检查必须（MUST）在 `detail` 中说明不适用原因。

**BPK-R033.** 提取 `pass` 必须（MUST）至少包含一项适用且通过的检查，没有失败或未知检查，并且在提供实际／预期单元数时，这两个数量相同。

空检查列表或全部不适用的检查列表不能证明提取成功。`adapter_required` 与已有转换器输出矛盾；`pass` 或 `partial` 与没有转换器输出矛盾。

CER 要么是已测量值，附带参照类别和样本量；要么为 `not_measured` 并取 null。Null 不是测得的零。语义状态为 `not_built`、`not_measured`、`built_unreviewed` 或 `reviewed`；前两者要求对象文件和关系文件为空。

**BPK-R034.** 每次语义审查必须（MUST）标识 `review_id`、`reviewer_id`、`producer_id`、审查者类型、独立性依据、时间、结果、已检查对象和关系的精确标识符，以及当前对象文件、关系文件和可读文件的摘要。

**BPK-R035.** `sample_size` 计数的是不同的已审查对象，而不是关系或检查列表条目，并且必须（MUST）等于对象 ID 列表长度。

审查不能指称不存在的记录。不能仅通过修改时间戳，将对旧字节的审查转移到新字节。

**BPK-R036.** `knowledge_ready` 配置要求**完整覆盖**，而不是统计抽样：每个对象和关系都必须（MUST）纳入，每条纳入记录都必须（MUST）为 `reviewed`，结果必须（MUST）为 `supported`，并且声明的审查者必须（MUST）是与生产者不同的人类或盲评代理。

同会话审查、部分支持、不支持结果以及遗漏记录，都不能获得此状态。

**BPK-R052.** 必须（MUST）至少存在一个对象。

较窄审查应如实保留为 `partial_pilot`。

这些检查验证声明范围、分离和字节绑定。它们不能证明人工审查实际发生，也不能证明身份独立。合成夹具使用明确虚构的审查者身份进行测试。观察认证属于消费方信任边界。

### 完整包状态决策表 {#total-package-status-decision-table}

**BPK-R037.** 验证器必须（MUST）计算下表中第一个匹配行，并要求其结果等于提交的 `package_status`。

所有格式良好的组合都有一个结果；相互矛盾的组件／检查声明还会另外被拒绝，而不是分配成功状态。

| 优先级 | 条件 | 推导状态 |
| --- | --- | --- |
| 1 | 来源完整性为 `mismatch`，即使完整程度只是书目级 | `blocked_integrity` |
| 2 | 完整程度为 `bibliography_only` | `bibliography_only` |
| 3 | 缺少转换器输出 | `adapter_required` |
| 4 | 语义层为 `not_built` 或 `not_measured`，对象和关系均为零 | `structure_only` |
| 5 | 完整且已验证的来源；提取通过；声明的完整独立审查支持所有已审查记录 | `knowledge_ready` |
| 6 | 其余任何格式良好的已转换包 | `partial_pilot` |

**BPK-R038.** `blocked_integrity`、`bibliography_only` 和 `adapter_required` 必须（MUST）同时省略文档组件和可读组件。

**BPK-R039.** `structure_only`、`partial_pilot` 和 `knowledge_ready` 必须（MUST）同时包含这两个组件。

因此，已审查但完整性未验证或来源覆盖不完整的包，可表示为 `partial_pilot`。即使文件在结构上存在，提取失败也必须保持可见。

## 9. 修订影响与重新评估 {#9-correction-impact-and-reassessment}

**BPK-R040.** 已接受纠正必须（MUST）使以下每个对象失效：在 `depends_on_objects` 中明确列出的对象，**或者**来源锚点与该修订重叠的对象。

生产者依赖列表不能覆盖重叠规则。章节／块和幻灯片／块采用精确匹配；区间与可比较页面框使用相交；JSON 指针使用相等或祖先关系。工作表范围保守地使同一工作表的整个范围失效；不可比较的几何被视为可能重叠。

**BPK-R041.** 受影响对象必须（MUST）保持过时或被拒绝，直到其 `reviewed_edit_ids` 明确列出已接受纠正，并且一项支持性的、声明独立的审查覆盖该对象以及当前可读和语义文件摘要。

引用未知或未接受的修订标识符会被拒绝。过时提案不能通过此已接受修订机制清除。依赖关系遵循第5节。这是声明的重新评估记录，不是生产者语义推理正确的证据。

## 10. 权利与出版层 {#10-rights-and-publication-layers}

`rights.license_class` 为 `author_open`、`third_party_restricted` 或 `unknown`。

**BPK-R042.** 只有 `author_open` 可以（MAY）声明包出版 `license`（`CC-BY-4.0` 或 `Apache-2.0`）和非空 `publishable_layers`。

**BPK-R043.** 权利受限或未知的作品必须（MUST）省略该许可证字段，并使出版层列表为空。

这既阻止通过文档文件携带书籍文本，也阻止通过语义分块携带。不能从提取、审查或生产者提供的许可证字符串推断引用额度或再版权利。

对其他方面有效的受限包进行私有处理，不属于公共投影范围。

**BPK-R044.** 投影函数必须（MUST）对此类包返回零行。

这一保守生产者规则实施仓库中排除第三方书籍文本的既定边界；它不是对其他场合可能用途的法律结论。任何另行创作的派生物都需要自身的来源／权利评估和出版决定。

## 11. 候选导出与准入运行时 {#11-candidate-export-and-admission-runtime}

**BPK-R045.** `candidate_projection(package_directory)` 必须（MUST）验证一个私有、不可变的字节快照，并从该快照本身计算渲染结果。

它不接受原始清单加上调用者自行选择的 Markdown。

**BPK-R046.** 验证失败、状态为 `blocked_integrity`、`bibliography_only` 或 `adapter_required`，或缺少允许的开放出版许可证时，必须（MUST）返回零行。

| 包元素 | 候选投影 |
| --- | --- |
| 允许的文档／可读 Markdown | 对其精确字节提出一行候选记录 |
| 允许的知识层 | 对完整受保护渲染提出一行 `knowledge.md` 候选记录 |
| JSON 记录、资源和质量文件 | 保留在包中，不作为独立 Markdown 导出行 |
| 未列出层或禁止状态／权利类别 | 不产生行 |
| 运行时准入 | 保持 `not_measured` |

各行标识 `articles/book-packages/<package_id>/<file>`、摘要、持有者、许可证、限制和 `status: proposed`。这些路径符合导出器路径语法，但不会自动加入允许列表。现有 `KnowledgeContractCandidateExport/v2` 导出器仍需要自身已经准入的范围、精确合并修订版和经过审查的出版决定。

**BPK-R047.** 生产者不得（MUST NOT）扩大该范围，也不得将候选行视为出版或运行时准入。

[API 集成附录](../../../appendices/api-integration/APPENDIX.md)区分仓库出版、索引准入和实际服务结果。本地符合性测试不声称实际消费者已经接受新配置。

## 12. 验证与证据限制 {#12-validation-and-evidence-limits}

JSON Schema 检查记录形状、固定词汇和条件字段。包验证器额外检查摘要与数量、身份和端点一致性、锚点映射与几何、字节精确的可逆重放、纠正影响、提取检查的合取、审查范围与文件绑定、完整状态推导，以及出版权利边界。

**BPK-R048.** 符合性测试集必须（MUST）保留每项回归的预期原因，包括负向审查、提取未知、绕过受限许可证、任意渲染、Markdown 结构注入、过时纠正、被拒绝端点和旧配置。

状态表测试枚举 3,240 种输入组合；枚举测试的是决策表，而不是 3,240 次历史书籍实验。结构不一致另行测试。

包不能确立来源保真度、真实性、真实审查独立性、未见来源几何、真实许可证持有权或下游准入。生成描述与其描述的媒体分离。链接的[转录研究](../../studies/source-transcription-and-uncertainty/STUDY.md)报告历史证据，并非对新传输配置的验证。

## 13. 兼容性与迁移 {#13-compatibility-and-migration}

版本 1 保留于不可变的[来源修订版 ed2e188c](https://github.com/Arcanada-one/knowledge-contract/tree/ed2e188c89a1a50a187f3d55bf32baab54c87f7e)。版本 2 有意更严格，增加观察、有界审查、可读包标识符、明确验证配置和语义词汇。

**BPK-R049.** 不得（MUST NOT）仅重写现有记录标签：缺失观察仍然缺失，不支持的修订仍不受支持，对旧字节的审查不能确立对迁移后字节的审查。

**BPK-R050.** 迁移必须（MUST）创建新的包发行版、保留原始修订版、标识每项映射或丢弃的不支持字段、重新验证摘要和修订，并取得任何新增必需审查。

**BPK-R051.** 迁移不得（MUST NOT）虚构完整性观察、审查者身份或作者归属。

V2 构建器在实际执行解释之前输出空语义层。出版版本、包配置、验证器构建和准入运行时版本保持为不同身份。

署名与许可证：Knowledge Contract Arcana，<https://contract.place>（CC BY 4.0）。参见[署名要求](../../../ATTRIBUTION.md)。

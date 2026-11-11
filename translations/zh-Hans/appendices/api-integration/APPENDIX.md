---
name: "api-integration"
title: "发布接口：API 集成与发布一致性"
artifact: "appendix"
edition: "1.1"
author: "Pavel Valentov"
language: "zh-Hans"
license: "CC-BY-4.0"
description: "已公布的读取接口、任务契约交付要求，以及仓库、阅读界面和索引之间的一致性。"
translation_of: "appendices/api-integration/APPENDIX.md"
source_commit: "a0450428704fcd41b411203f2fc88c06c779610b"
source_git_blob: "3f3c5e19093df1f5c1b0ff6b4c8b191a0a7c1de8"
translation_status: "author-draft"
---

# 发布接口：API 集成与发布一致性 {#api-integration-and-publication-consistency}

**出版版本：** 1.1 · **接口清单日期：** 2026年11月4日

## 1. 目的 {#1-purpose}

仓库发布知识与规范。网站呈现选定的不可变出版物。服务暴露机器接口。这些是相互关联、但具有不同版本与证据的产品。网站构建成功并不能确立服务已部署、搜索索引已更新，或完整的任务专属知识契约已获准入。

本附录规定这些边界之间的联系。[核心规范——英文原文](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/specifications/knowledge-contract-core/SPECIFICATION.md)提供就绪契约的义务；[上下文包规范——英文原文](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/specifications/context-package/SPECIFICATION.md)提供组合与交付要求。

第3至第7节采用 [BCP 14——英文原文](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/reference/bibliography/BIBLIOGRAPHY.md#requirement-language)定义要求。第2节是已记载读取接口的资料性清单，不声称任务契约服务或下述回执配置已经部署。要求标识符在本附录中保持稳定。

**API-R001.** 符合性声明必须（MUST）指明实现的配置、实现的精确修订版和已评估的要求；公布这些要求并不能确立符合性。

## 2. 已记载的公共接口 {#2-documented-public-interface}

公共网站描述了下列读取接口：

| 接口 | 已记载的作用 | 边界 |
| --- | --- | --- |
| `https://api.contract.place/v1/search` | 检索候选段落；供网站的匿名GET搜索使用 | 检索排序不确立正确性、完整性或任务准入 |
| `https://api.contract.place/v1/related` | 检索关联记录 | 关联或相似性不等于等价关系，也不提供权限授予 |
| `https://api.contract.place/v1/fetch` | 通过读取接口获取具有地址标识的记录 | 必须检查返回的修订版与表示 |
| `https://api.contract.place/mcp` | 通过MCP访问已记载的服务接口 | 工具可用不等于研究所描述的每项操作均已实现 |
| `https://api.contract.place/health` | 服务健康信息 | 健康状态不同于语料新鲜度和科学有效性 |

现有网站的 `llms.txt` 将读取模式命名为 `ContractPlaceRead/v1`。除实际观察到的网站搜索外，本附录不推断其他路由的HTTP方法、参数模式或身份认证行为。客户端应使用服务的实际API契约。交付任务专属契约的能力需要独立实现并测试的接口；本文没有确立 `/compose` 端点的存在。

## 3. 契约交付要求 {#3-contract-delivery-requirements}

**API-R002.** **请求绑定。** 提供就绪知识契约的服务必须（MUST）将请求绑定到任务及要求修订版、预期接收方与用途、适用约束、必需配置、时间模式和资源限额。

**API-R003.** 任何必需值未知时，服务必须（MUST）在声称已准许该用途之前报告缺口，或取得缺失信息。

**API-R004.** **响应与结果。** 响应必须（MUST）标识精确的契约与表示版本、选定的知识修订版、来源与依据、强制依赖闭包、覆盖情况、遗漏或未解决的义务、适用约束、评估，以及决策的信任边界。

**API-R005.** 操作结果必须（MUST）是 **`success`, `partial`, `refused`, `failed`, `unresolved`** 之一，含义遵循[状态模型——英文原文](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/specifications/status-model/SPECIFICATION.md#3-canonical-dimension-vocabularies)。

**API-R006.** `ready` 是可用性或生命周期状态，绝不能（MUST NOT）替代操作结果标记。

执行交付操作失败属于 `failed`；无法确立的结果或实质义务属于 `unresolved`。

**API-R007.** **准入范围。** 就绪可用的断言必须（MUST）以针对所声明用途的强制检查为依据。

非空JSON对象或成功搜索都不足以满足这一要求。支持阅读的响应，仍可能缺少执行所需的能力或授权依据。渲染出的技能说明不能补足这些缺失事实。

**API-R008.** **知识契约准入运行时**是负责此类决策的服务边界；必须（MUST）标明其实际实现版本与配置版本，而不能从出版版本或历史字段 `kc2_admission` 推断这些版本。

**API-R009.** **执行绑定。** 如果契约是为执行而签发的，系统随后必须（MUST）绑定实际尝试、行动主体、环境、契约修订版、输出、效果和验收证据。

知识交付与执行验收是不同操作。

## 4. 三种清单 {#4-three-manifests}

发布一致性需要三种可独立检查的身份：

| 清单 | 必需身份 |
| --- | --- |
| 仓库出版目录 | 同一个来源提交中的出版版本，以及规范文档路径与类型 |
| 网站出版清单 | 来源仓库的精确提交、出版版本、文档哈希、渲染器版本和生成的路由 |
| API索引清单 | 实际已索引的来源提交与内容哈希、构建身份、准入路径和适用决策 |

**网站身份。** 网站的来源提交固定在网站仓库的 `publication-manifest.json` 中。生成的 `publication.json` 将阅读路由绑定到来源哈希。

**API-R010.** 部署必须（MUST）从所声明的提交构建这些页面，并拒绝未提交或不匹配的来源树。

**限定仓库的比较。** API可能包含多个仓库或多个发布版本。

**API-R011.** 在比较某个结果的来源修订版与阅读界面的出版提交之前，客户端必须（MUST）先确立仓库身份。

本项目的规范仓库标识符是 **`https://github.com/Arcanada-one/knowledge-contract`**；修订版比较限定在这个标识符所指的仓库内。

**API-R012.** 这种比较绝不能（MUST NOT）应用于无关来源。

**API-R013.** 未知修订版和不同修订版必须（MUST）与匹配结果区分开来。

API返回一个“current”标签，本身并不能证明它与出版物相匹配。

在[已检查的网站适配器](https://github.com/Arcanada-one/contract-place-site/blob/cdca604245165bbec80ce3624fdc65e9cbde6a01/src/site/search.js)中，相关响应字段是 **`source_revision`** 和 **`citation.canonical_url`**。后者通过形如 `https://github.com/{owner}/{repository}/blob/{full-commit}/{path}` 的HTTPS GitHub URL提供仓库身份；适配器将识别出的所有者、仓库与修订版同固定版本的阅读界面进行比较。下述回执配置使用的规范化 `repository_url` 是操作者记录字段，并不声称后端已经返回同名字段。如果规范URL缺失、格式错误、指向另一主机，或没有标识不可变修订版，就不能确立出版物匹配。

**API-R014.** 客户端绝不能（MUST NOT）用不受信任的标题、分支标签或孤立的哈希替代这种身份。

**API-R015.** 如果URL中的修订版与 `source_revision` 冲突，客户端必须（MUST）报告不匹配。

在检查已公布的读取模式字段契约后，该契约仍是实际API表示的权威依据。

## 5. 观察到的不匹配与发布门槛 {#5-observed-mismatch-and-release-gate}

重组前的网站链接到较新的论文入口，而搜索检查却返回位于 `39e05969728ea7a51f162cdbefac32fd8f54dbb6` 的知识契约快照；该快照的README仍把出版文件夹描述为空。这是阅读界面与搜索证据之间的一致性不匹配，不是GitHub中不存在较新文档的证据。

阅读界面通过公开精确来源修订版，并显示搜索结果修订版是否与其匹配，处理呈现边界的问题。

**API-R016.** 刷新或提升后端索引是另一项操作。**准入治理。** 索引操作必须（MUST）采用仓库现有的出版决策与允许列表流程；目录条目不能替代这种批准。

发布本附录不会准许任何路径、刷新索引或改变允许列表。

**API-R017.** **发布门槛。** 在把一个发布版本描述为已一致地索引之前，操作者必须（MUST）针对精确来源修订版记录下列全部六项检查。

仅有健康检查不能通过这一门槛。缺失的观察是 `unknown`，不是 `pass`。

| 检查键 | 必需观察 |
| --- | --- |
| `admitted_snapshot` | 准入路径的哈希与决策引用同预期的不可变来源快照一致 |
| `index_snapshot` | 实际索引构建与清单标识该导出快照 |
| `reported_revision` | 返回结果的身份报告预期仓库与修订版 |
| `query_coverage` | 已声明查询集检索到指定的预期文档；选择和排除范围有记录 |
| `supersession` | 被移除或被替代记录具有所声明的观察状态；没有此类记录时须明确记录空清单 |
| `fetch_identity` | 获取每一个保留结果的身份时，返回的修订版与内容哈希同该结果报告的值一致 |

### 发布回执配置 {#release-receipt-profile}

**API-R018.** **回执。** 符合 **`KCIndexReleaseReceipt/v1`** 的门槛记录必须（MUST）满足[回执JSON Schema](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/appendices/api-integration/index-release-receipt.schema.json)及本文的语义检查。

这是本出版物新增的操作者记录交换配置，不是现有服务已输出该记录的证据。本附录没有提供生产环境回执，也不声称发生了新的部署或索引运行。

| 必需字段 | 表示与含义 |
| --- | --- |
| `schema` | 精确标记 `KCIndexReleaseReceipt/v1` |
| `repository_url`, `source_revision` | 规范HTTPS仓库URL和完整的40字符小写Git提交身份；一份回执覆盖一个仓库修订版 |
| `observed_at`, `observer`, `evidence_refs` | RFC 3339观察时间、承担责任的观察者身份，以及实际运行的持久证据引用 |
| `publication_manifest_sha256` | 用于比较的网站或出版清单的SHA-256 |
| `index_build_id`, `index_manifest_sha256` | 实际后端构建身份与精确清单哈希，而不是希望未来获得的值 |
| `admitted_paths` | 非空列表 `{path, sha256, decision_ref}`，对应精确的已准入来源文件 |
| `queries` | 非空的已声明列表 `{id, query, expected_paths, results}`；每项结果记录 `{record_id, path, source_revision, source_sha256, representation_sha256, canonical_url}` |
| `fetches` | 回读列表 `{record_id, source_revision, representation_sha256}`，覆盖每个保留的查询结果 |
| `superseded_records` | 列表 `{record_id, expected_status, observed_status, evidence_ref}`；`[]` 明确表示已检查的变更清单中没有此类记录 |
| `checks` | 全部六个具名检查结果，每个为 `pass`、`fail` 或 `unknown`；没有遗漏的检查 |
| `decision` | 只有全部检查通过才为 `pass`；否则，只要有检查失败就为 `fail`；若没有失败但至少一项未知，则为 `unknown` |
| `scope`, `limitations` | 查询选择理由、纳入或排除的路径，以及观察限制；限制可以是明确的空列表 |

**API-R019.** 查询ID、准入路径，以及每个结果列表或回读列表内部的记录ID必须（MUST）唯一。

**API-R020.** 同一条记录可以（MAY）被多个不同查询找到。

**API-R021.** 每个查询的预期路径必须（MUST）来自 `admitted_paths`；在 `query_coverage` 能够通过之前，每个预期路径都必须有匹配结果。

**API-R022.** 每个保留结果必须（MUST）标识所声明的仓库与 `source_revision`，且其来源路径与 `source_sha256` 必须同准入快照匹配。

`representation_sha256` 标识实际返回表示的精确字节，与整个来源文件的身份分开。

**API-R023.** 返回段落的服务必须（MUST）同时提供这两种绑定，否则须把相关检查保留为未知。

**API-R024.** 在 `fetch_identity` 能够通过之前，每个结果都必须（MUST）有匹配的获取身份和表示哈希。

**API-R025.** 在 `supersession` 能够通过之前，每个被替代记录的观察状态都必须（MUST）等于其所要求的状态。

仅有模式验证并不能确立这些对应关系、记录中观察的真实性，或执行索引的权限。

## 6. 客户端呈现 {#6-client-presentation}

**API-R026.** **呈现。** 默认结果视图应当（SHOULD）显示段落、人类可读的标题、来源链接和已索引的修订版。

**API-R027.** 关于准入、不确定性和评分语义的技术证据可以（MAY）放在可访问的详情区域中。

**API-R028.** 实质限制会改变用户决策时，必须（MUST）在相应位置保持可见。

**API-R029.** 在没有独立确立的校准及其适用范围时，绝不能（MUST NOT）把检索分数呈现为某项主张为真的概率。

**API-R030.** 科学阅读应当（SHOULD）无需API调用仍可进行：完整页面、公式、引用和证据链接作为选定的静态版本提供。

因此，API故障不必导致已发布的科学论证无法阅读。

## 7. 验收案例 {#7-acceptance-cases}

**API-R031.** **验收案例。** 集成必须（MUST）拒绝使用错误来源提交构建的网站、带有未提交变更的出版树、缺失的被引用文档，以及逸出出版范围的本地链接。

**API-R032.** 搜索呈现必须（MUST）区分匹配的知识契约修订版、较旧修订版、未知修订版，以及来自其他仓库的记录。

**API-R033.** 渲染必须（MUST）保留公式、表格、脚注和文档锚点。

**API-R034.** 回执验证必须（MUST）拒绝遗漏的检查、存在未通过检查却标为通过的决策、含糊的仓库或修订版身份、重复身份、缺失的预期路径，以及不匹配的获取回读。

**API-R035.** 契约交付验收套件还必须（MUST）覆盖缺失约束、强制但未知的配置、不完整闭包、预算不足、披露权限已撤销、来源证据过时，以及正确但不授权执行的信息性响应。

对于没有经过该套件检验的接口，本文不声称存在成功结果。

关于这些检查的证据性解释，请参见[证据与证伪](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/evidence-and-falsification/PAPER.md)、[受控复用](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/controlled-knowledge-reuse/PAPER.md)，以及[工程研究](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/README.md)的英文原文。

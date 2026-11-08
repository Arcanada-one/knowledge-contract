---
name: "api-integration"
title: "Publication Interfaces: API Integration and Publication Consistency"
short_title: "Publication Interfaces"
subtitle: "API Integration and Publication Consistency"
previous_title: "API Integration and Publication Consistency"
artifact: "appendix"
edition: "1.1"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "Published read interfaces, task-contract delivery requirements and consistency between repository, reader and index."
---

<!-- markdownlint-disable-next-line MD033 -->
<a id="api-integration-and-publication-consistency"></a>

# Publication Interfaces: API Integration and Publication Consistency

**Publication edition:** 1.1 · **Interface inventory date:** 4 November 2026

## 1. Purpose

The repository publishes knowledge and specifications. The website renders a selected immutable publication. The service exposes machine interfaces. These are related products with separate versions and evidence. A successful website build does not establish service deployment, a current search index, or admission of a complete task-specific Knowledge Contract.

This appendix defines the connection between those boundaries. The [core specification](../../engineering/specifications/knowledge-contract-core/SPECIFICATION.md) supplies the obligations for a ready contract; the [context-package specification](../../engineering/specifications/context-package/SPECIFICATION.md) supplies composition and delivery requirements.

Sections 3–7 define requirements using [BCP 14](../../reference/bibliography/BIBLIOGRAPHY.md#requirement-language). Section 2 is an informative inventory of the documented read surface, not a claim that a task-contract service or the receipt profile below has been deployed. Requirement identifiers remain stable within this appendix.

**API-R001.** Conformance MUST name the implemented profile, exact implementation revision and assessed requirements; publication of these requirements does not establish that conformance.

## 2. Documented public interface

The public site describes the following read surface:

| Interface | Documented role | Boundary |
| --- | --- | --- |
| `https://api.contract.place/v1/search` | Retrieve candidate passages; used by the site's anonymous GET search | Retrieval ranking does not establish correctness, completeness or task admission |
| `https://api.contract.place/v1/related` | Retrieve related records | A relation or similarity is not an equivalence or authority grant |
| `https://api.contract.place/v1/fetch` | Fetch an addressed record through the read interface | The returned revision and representation must be inspected |
| `https://api.contract.place/mcp` | MCP access to the documented service surface | Availability of a tool does not establish every operation described by the research |
| `https://api.contract.place/health` | Service health information | Health is distinct from corpus freshness and scientific validity |

The existing site's `llms.txt` names the read schema `ContractPlaceRead/v1`. This appendix does not infer HTTP methods, parameter schemas or authentication behavior for routes other than the observed site search. Clients use the service's actual API contract. A task-specific contract delivery capability requires its own implemented and tested interface; no `/compose` endpoint is established here.

## 3. Contract delivery requirements

**API-R002.** **Request binding.** A service offering a ready Knowledge Contract MUST bind the request to the task and requirements revision, intended recipient and use, applicable constraints, required profiles, temporal mode, and resource limits.

**API-R003.** Where any required value is unknown, it MUST report the gap or obtain the missing information before asserting admission for that use.

**API-R004.** **Response and outcome.** The response MUST identify the exact contract and representation versions, selected knowledge revisions, sources and grounds, mandatory dependency closure, coverage, omitted or unresolved obligations, applicable constraints, assessments and the decision's trust boundary.

**API-R005.** Its operation outcome MUST be one of **`success`, `partial`, `refused`, `failed`, `unresolved`**, with the [status model's meanings](../../engineering/specifications/status-model/SPECIFICATION.md#3-canonical-dimension-vocabularies).

**API-R006.** `ready` is an availability or lifecycle state; it MUST NOT replace an outcome token.

A failure to execute the delivery operation is `failed`; an outcome or material obligation that cannot be established is `unresolved`.

**API-R007.** **Admission scope.** A ready-for-use assertion MUST be backed by the mandatory checks for the declared use.

A nonempty JSON object or successful search is insufficient. A response that supports reading may still lack the capability or grant needed for execution. A rendered skill description cannot supply those missing facts.

**API-R008.** The **Knowledge Contract admission runtime** is the service boundary responsible for such a decision; its actual implementation and profile versions MUST be identified rather than inferred from the publication edition or the legacy field `kc2_admission`.

**API-R009.** **Execution binding.** If the contract is issued for execution, the system MUST subsequently bind the actual attempt, actor, environment, contract revision, outputs, effects and acceptance evidence.

Knowledge delivery and execution acceptance are separate operations.

## 4. Three manifests

Publication consistency requires three independently inspectable identities:

| Manifest | Required identity |
| --- | --- |
| Repository publication catalogue | Edition and the canonical document paths/types in one source commit |
| Website publication manifest | Exact source repository commit, edition, document hashes, renderer version and generated routes |
| API index manifest | Actual indexed source commits and content hashes, build identity, admitted paths and applicable decisions |

**Website identity.** The website's source commit is pinned in `publication-manifest.json` in the site repository. Its generated `publication.json` binds reader routes to source hashes.

**API-R010.** A deployment MUST build those pages from the declared commit and reject an uncommitted or mismatched source tree.

**Repository-scoped comparison.** The API may contain multiple repositories or releases.

**API-R011.** A client MUST establish repository identity before comparing a result's source revision with the reader's publication commit.

The canonical repository identifier for this project is **`https://github.com/Arcanada-one/knowledge-contract`**; a revision comparison is scoped to this identifier.

**API-R012.** It MUST NOT be applied to an unrelated source.

**API-R013.** Unknown and different revisions MUST be distinguished from a match.

An API-provided label of “current” alone is not proof of a matching publication.

In the [inspected site adapter](https://github.com/Arcanada-one/contract-place-site/blob/cdca604245165bbec80ce3624fdc65e9cbde6a01/src/site/search.js), the relevant response fields are **`source_revision`** and **`citation.canonical_url`**. The latter supplies repository identity through an HTTPS GitHub URL of the form `https://github.com/{owner}/{repository}/blob/{full-commit}/{path}`; the adapter compares the identified owner/repository and revision with the pinned reader. The normalized `repository_url` used by the receipt profile below is an operator-record field, not a claim that the backend already returns a field with that name. If the canonical URL is absent, malformed, points to another host or does not identify an immutable revision, a matching publication cannot be established.

**API-R014.** A client MUST NOT substitute an untrusted title, branch label or bare hash for that identity.

**API-R015.** If URL revision and `source_revision` conflict, it MUST report a mismatch.

The read schema's published field contract, once inspected, remains authoritative for the actual API representation.

## 5. Observed mismatch and release gate

The pre-restructure site linked the newer paper entries while a search inspection returned a Knowledge Contract snapshot at `39e05969728ea7a51f162cdbefac32fd8f54dbb6`, whose README still described publication folders as empty. That was a consistency mismatch between the reading surface and search evidence, not proof that the newer documents were absent from GitHub.

The reader addresses the presentation boundary by exposing its exact source revision and showing whether a search result's revision matches it.

**API-R016.** Refreshing or promoting the backend index is a separate operation. **Admission governance.** An indexing operation MUST use the repository's existing publication-decision and allowlist process; a catalogue entry is not a substitute for that approval.

Publishing this appendix does not admit paths, refresh an index or change an allowlist.

**API-R017.** **Release gate.** Before a release is described as consistently indexed, the operator MUST record all six checks below against the exact source revision.

A health check alone cannot pass this gate. A missing observation is `unknown`, not `pass`.

| Check key | Required observation |
| --- | --- |
| `admitted_snapshot` | Admitted path hashes and decision references agree with the intended immutable source snapshot |
| `index_snapshot` | The actual index build and manifest identify that exported snapshot |
| `reported_revision` | Returned result identities report the intended repository and revision |
| `query_coverage` | A declared query set retrieves the specified expected documents; selection and exclusions are recorded |
| `supersession` | Removed or superseded records have the declared observed status, including an explicit empty inventory when none apply |
| `fetch_identity` | Fetching every retained result identity returns the same revision and content hash reported for that result |

### Release receipt profile

**API-R018.** **Receipt.** A gate record conforming to **`KCIndexReleaseReceipt/v1`** MUST satisfy the [receipt JSON Schema](index-release-receipt.schema.json) and the semantic checks here.

It is a new operator interchange profile for this publication, not evidence that the existing service emits it. This appendix supplies no production receipt and claims no new deployment or index run.

| Required field | Representation and meaning |
| --- | --- |
| `schema` | Exact token `KCIndexReleaseReceipt/v1` |
| `repository_url`, `source_revision` | Canonical HTTPS repository URL and full 40-character lowercase Git commit identity; one receipt covers one repository revision |
| `observed_at`, `observer`, `evidence_refs` | RFC 3339 observation time, accountable observer identity and durable evidence references for the actual run |
| `publication_manifest_sha256` | SHA-256 of the website/publication manifest used for comparison |
| `index_build_id`, `index_manifest_sha256` | Actual backend build identity and exact manifest hash, not a desired future value |
| `admitted_paths` | Nonempty list of `{path, sha256, decision_ref}` for the exact admitted source files |
| `queries` | Nonempty declared list of `{id, query, expected_paths, results}`; each result records `{record_id, path, source_revision, source_sha256, representation_sha256, canonical_url}` |
| `fetches` | Readback list of `{record_id, source_revision, representation_sha256}` for every retained query result |
| `superseded_records` | List of `{record_id, expected_status, observed_status, evidence_ref}`; `[]` explicitly means that the inspected change inventory has no such records |
| `checks` | All six named gate outcomes, each `pass`, `fail` or `unknown`; no omitted check |
| `decision` | `pass` only if every check passed; otherwise `fail` if any check failed, and `unknown` when none failed but at least one is unknown |
| `scope`, `limitations` | The query selection rationale, included/excluded paths and limits of observation; limitations may be an explicitly empty list |

**API-R019.** Query IDs, admitted paths, and record IDs within each results or fetch list MUST be unique.

**API-R020.** The same record MAY be found by several different queries.

**API-R021.** Each query's expected paths MUST be drawn from `admitted_paths`; every expected path MUST have a matching result before `query_coverage` can pass.

**API-R022.** Each retained result MUST identify the declared repository and `source_revision`, and its source path and `source_sha256` MUST match the admitted snapshot.

`representation_sha256` identifies the exact returned representation bytes, separately from the whole source file.

**API-R023.** A service returning passages MUST provide both bindings or leave the relevant check unknown.

**API-R024.** Every result MUST have a matching fetch identity and representation hash before `fetch_identity` can pass.

**API-R025.** Every superseded record's observed status MUST equal its required status before `supersession` can pass.

Schema validation alone does not establish these correspondences, the truth of recorded observations or authority to index.

## 6. Client presentation

**API-R026.** **Presentation.** The default result view SHOULD show the passage, human title, source link and indexed revision.

**API-R027.** Technical evidence about admission, uncertainty and score semantics MAY be placed in an accessible details section.

**API-R028.** Material limits MUST remain visible where they change a user's decision.

**API-R029.** A retrieval score MUST NOT be presented as a probability that a claim is true without an independently established calibration and its scope.

**API-R030.** Scientific reading SHOULD remain possible without making API calls: full pages, equations, references and evidence links are served as the static selected edition.

API failure therefore need not remove the published scientific argument.

## 7. Acceptance cases

**API-R031.** **Acceptance cases.** The integration MUST reject a site build from the wrong source commit, a dirty publication tree, a missing referenced document and a local link escaping the publication.

**API-R032.** Search presentation MUST distinguish a matching Knowledge Contract revision, an older revision, an unknown revision and a record from another repository.

**API-R033.** Rendering MUST preserve equations, tables, footnotes and document anchors.

**API-R034.** Receipt validation MUST reject omitted checks, a passing decision with a nonpassing check, an ambiguous repository/revision identity, duplicate identities, missing expected paths, and a mismatched fetch readback.

**API-R035.** A contract-delivery acceptance suite MUST additionally exercise missing constraints, a mandatory unknown profile, incomplete closure, insufficient budget, revoked disclosure authority, stale source evidence, and a correct informational response that does not authorize execution.

No successful result is claimed here for an interface that has not undergone that suite.

For the evidential interpretation of these checks, see [evidence and falsification](../../papers/evidence-and-falsification/PAPER.md), [controlled reuse](../../papers/controlled-knowledge-reuse/PAPER.md), and the [engineering studies](../../engineering/studies/README.md).

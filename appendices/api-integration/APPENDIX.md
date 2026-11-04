---
name: "api-integration"
title: "API Integration and Publication Consistency"
artifact: "appendix"
edition: "1.0"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "Published read interfaces, task-contract delivery requirements and consistency between repository, reader and index."
---

# API Integration and Publication Consistency

**Publication edition:** 1.0 · **Interface inventory date:** 4 November 2026

## 1. Purpose

The repository publishes knowledge and specifications. The website renders a selected immutable publication. The service exposes machine interfaces. These are related products with separate versions and evidence. A successful website build does not establish service deployment, a current search index, or admission of a complete task-specific Knowledge Contract.

This appendix defines the connection between those boundaries. The [core specification](../../engineering/specifications/knowledge-contract-core/SPECIFICATION.md) supplies the obligations for a ready contract; the [context-package specification](../../engineering/specifications/context-package/SPECIFICATION.md) supplies composition and delivery requirements.

## 2. Documented public interface

The public site describes the following read surface:

| Interface | Documented role | Boundary |
| --- | --- | --- |
| `https://api.contract.place/v1/search` | Retrieve candidate passages; used by the site's anonymous GET search | Retrieval ranking does not establish correctness, completeness or task admission |
| `https://api.contract.place/v1/related` | Retrieve related records | A relation or similarity is not an equivalence or authority grant |
| `https://api.contract.place/v1/fetch` | Fetch an addressed record through the read interface | The returned revision and representation must be inspected |
| `https://api.contract.place/mcp` | MCP access to the documented service surface | Availability of a tool does not establish every operation described by the research |
| `https://api.contract.place/health` | Service health information | Health is distinct from corpus freshness and scientific validity |

The existing site's `llms.txt` names the read schema `ContractPlaceRead/v1`. This appendix does not infer HTTP methods, parameter schemas or authentication behavior for routes other than the observed site search. Clients must use the service's actual API contract. It also does not invent a `/compose` endpoint: a task-specific contract delivery capability requires its own implemented and tested interface.

## 3. Contract delivery requirements

A service offering a ready Knowledge Contract must bind the request to the task and requirements revision, intended recipient and use, applicable constraints, required profiles, temporal mode, and resource limits. Where any of those are required but unknown, it must report the gap or obtain the missing information.

The response must identify the exact contract and representation versions, selected knowledge revisions, sources and grounds, mandatory dependency closure, coverage, omitted or unresolved obligations, applicable constraints, assessments and the decision's trust boundary. It must expose a coherent distinction among ready-for-the-declared-use, partial, refused and unresolved outcomes.

“Ready” requires the mandatory checks for that use, not merely a nonempty JSON object or a successful search. A response that supports reading may still lack the capability or grant needed for execution. A rendered skill description cannot supply those missing facts.

If the contract is issued for execution, the system must subsequently bind the actual attempt, actor, environment, contract revision, outputs, effects and acceptance evidence. Knowledge delivery and execution acceptance are separate operations.

## 4. Three manifests

Publication consistency requires three independently inspectable identities:

| Manifest | Required identity |
| --- | --- |
| Repository publication catalogue | Edition and the canonical document paths/types in one source commit |
| Website publication manifest | Exact source repository commit, edition, document hashes, renderer version and generated routes |
| API index manifest | Actual indexed source commits and content hashes, build identity, admitted paths and applicable decisions |

The website's source commit is pinned in `publication-manifest.json` in the site repository. Its generated `publication.json` binds reader routes to source hashes. A deployment must build those pages from the declared commit and reject an uncommitted or mismatched source tree.

The API may contain multiple repositories or releases. The site compares a Knowledge Contract result's source revision with the reader's publication commit only within that repository. It must not apply that comparison to an unrelated source. Unknown or different revisions are shown as such. An API-provided label of “current” alone is not proof that the result matches the selected publication.

## 5. Observed mismatch and release gate

The pre-restructure site linked the newer paper entries while a search inspection returned a Knowledge Contract snapshot at `39e05969728ea7a51f162cdbefac32fd8f54dbb6`, whose README still described publication folders as empty. That was a consistency mismatch between the reading surface and search evidence, not proof that the newer documents were absent from GitHub.

The new reader addresses the presentation boundary by exposing its exact source revision and showing whether a search result's revision matches it. Refreshing or promoting the backend index is a separate operation. It must use the repository's existing publication-decision and allowlist process; a catalogue entry is not a substitute for that approval.

Before a release is described as consistently indexed, the operator must verify: admitted paths and hashes correspond to the intended source revision; indexing uses that exported snapshot; the service reports the actual revision; representative queries retrieve the new documents; removed or superseded entries have the recorded status; and the same result can be fetched by its returned identity. A health check alone cannot pass this gate.

## 6. Client presentation

The default result view should show the passage, human title, source link and indexed revision. Technical evidence about admission, uncertainty and score semantics can be placed in an accessible details section. Material limits must remain visible where they change a user's decision. A retrieval score is not a probability that a claim is true.

Scientific reading should remain possible without making API calls: full pages, equations, references and evidence links are served as the static selected edition. API failure therefore does not remove the published scientific argument.

## 7. Acceptance cases

The integration must reject a site build from the wrong source commit, a dirty publication tree, a missing referenced document and a local link escaping the publication. Search presentation must distinguish a matching Knowledge Contract revision, an older revision, an unknown revision and a record from another repository. Rendering must preserve equations, tables, footnotes and document anchors.

A future contract-delivery acceptance suite additionally needs missing constraints, a mandatory unknown profile, incomplete closure, insufficient budget, revoked disclosure authority, stale source evidence, and a correct informational response that does not authorize execution. No successful result is claimed here for an interface that has not undergone that suite.

For the evidential interpretation of these checks, see [evidence and falsification](../../papers/evidence-and-falsification/PAPER.md), [controlled reuse](../../papers/controlled-knowledge-reuse/PAPER.md), and the [engineering studies](../../engineering/studies/README.md).

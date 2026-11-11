---
title: Typed reading map of the Knowledge Contract corpus
sources: none
status: proposed reference view; not a release or execution graph
---

# Typed reading map of the Knowledge Contract corpus

## Purpose and source boundary

The [machine-readable map](corpus-map.json) connects nine identified manuscripts, sixteen shared terms, nine bounded claim summaries, six foundation manuscript units and twenty-five roadmap definitions. It is an authored reading and integration view, not exhaustive extraction of the corpus's meanings, a proof graph, a grant, or a second task tracker. Its 65 nodes have 99 explicitly typed reading/planning relations; the 45 original roadmap prerequisite-output edges remain a separate relation family. Counts describe this snapshot, not an experiment or coverage percentage.

The six editorial works are the prepared-knowledge, semantic-object, transformation, retrieval, interaction and evidence papers. The existing revision and utility papers are included because the former works explicitly refer to them. F01 supplies the human-meaning introduction. This does not claim that all nine manuscripts have been newly revised or accepted.

Each document identifies its own immutable repository revision. The roadmap and four revised editorial manuscripts now point to their accepted main commits, each verified byte-identical to the preceding proposal source object; F01 remains a research-draft proposal. These source-pin updates do not independently review meanings, turn the map into a fully accepted publication release, or admit F01 to the export/index scope. This mixed proposal snapshot is useful for review, but it is not a coherent accepted publication release. The dictionary of source pins is part of the artifact. A site must not substitute the latest branch contents while retaining an old map hash.

Definitions remain in the [shared glossary](../glossary/GLOSSARY.md). The short term texts in this map are reading summaries, not replacement normative definitions. Claim summaries name their source location, premises and non-implications. Full source arguments remain authoritative. In particular, C03's chain-preservation summary requires the initial state to satisfy `P1(x0)`; local preservation and compatible junctions alone do not discharge that premise. The existing [eighteen-relation F01 map](relations.json) is retained unchanged and referenced by its Git blob identity; its section-level relations are not silently overwritten or counted as new experimental observations.

## How to read the connected material

For the candidate read-only projection of this map (pinned blob `a7b2fb8c…`), see the [projection reader guide](CORPUS_MAP_PROJECTION_READING.md). That guide is interpretation authored by KC-Brain; it is not a second map, proof graph or acceptance decision.

Begin with F01's distinction between human expressions and a purpose-selected representation. Follow semantic objects and context to determine what the representation asserts and under which interpretation. Transformations then describe what an operation preserves. Retrieval and composition select support and require checks on the actual delivered representation. Interaction and memory bind results to tasks and revisions. Evidence specifies what an observation supports; revision distinguishes a changed object from a changed assessment or adopted rule. Prepared-knowledge reuse combines preserved artifact properties with current-use obligations. Utility compares only stated interventions and cost scopes; it does not override mandatory conditions.

This is a suggested reading route, not a new theorem or execution schedule. Reading cycles are legitimate: the reuse and transformation papers can explain each other's application boundaries. A circular argument cannot become justified merely because those reading links exist.

## Relation families

| Family | Interpretation | Forbidden inference |
| --- | --- | --- |
| `uses-term` | A reading crosswalk to a named shared concept | Identical runtime semantics or schema conformance |
| `states-bounded-claim` | The manuscript contains the summarized argument | Its premises were measured or independently accepted |
| `reading-interface` | An explicit conceptual cross-reference between papers | A proof rule or required task dependency |
| `has-candidate` | A full pinned manuscript candidate exists | Merge, release, deployment or index admission |
| `extends-existing-path` | A foundation unit develops the existing paper | The present editorial candidate completes all planned extension work |
| `addresses-planned-scope` | A foundation unit addresses a roadmap topic | The whole roadmap task has been completed or aliased |
| `informs-not-blocks` | One of the four advisory roadmap links | A mandatory execution gate |
| `roadmap_nodes.requires` | The 45 retained prerequisite-output definitions | Observed Muneral readiness, start or acceptance |

The default F01–F06 preparation order is stored separately. F labels are manuscript units, not work-item UUIDs. F02, F04, F05 and F06 remain planned targets; F03 is a planned extension at an existing path. They do not receive invented article URLs or catalogue entries. Explicit later author instructions retain the scope described in the pinned roadmap. The advanced RM-18 programme does not add geometry or hybrid-retrieval prerequisites to the separately authorized baseline Live Lab.

## F01 catalogue decision

Continue **publication context 1.1 with thirty catalogue documents, including nine papers**, keeping F01 visibly `research-draft` until its actual release decision. The catalogue already represents that proposal. Preserve every prior entry and its history. A new edition label 1.2 is not introduced merely to make a count check pass; the immutable source revision identifies the changed proposal. Document edition, runtime protocol and index snapshot remain different identities.

This decision does not itself change the validator or waive its failures. Required integration work is a narrow update of the reviewed catalogue/count fixtures and applicable export-boundary tests. A strict count of eight papers cannot validate this intentional ninth paper. Conversely, replacing the check with an unconditional pass or automatically admitting every catalogue path is not an acceptable repair. Retain negative cases for missing, duplicate, unknown-type and metadata-mismatched records. The corpus allowlist and historical exact-byte admission receipts are unchanged.

## Checks performed here

The offline [validator](../../tools/verify_corpus_map.py) checks identity uniqueness, immutable pin syntax, references, relation endpoint types, claim premises/limitations, planned versus existing objects, exact foundation coverage agreement, and acyclicity of the required-output subgraph. Its fourteen [unit controls](../../tools/test_verify_corpus_map.py) include broken endpoints, wrong relation types, a required-edge cycle, an allowed reading cycle, fabricated completion/review status and path escape. [Recorded results](../../reviews/corpus-map/RESULTS.md) identify the exact map hash and actual execution.

These are structural and integrity checks. They do not establish semantic completeness, the truth of a paper, independent scientific review, actual scheduler readiness or a website release. The optional `--repo` check reads pinned Git objects from a supplied local repository and never fetches or mutates it; that mode was not run in the isolated authoring environment. Connector reads of selected source files are separate observations. A source location written as a heading is a locator for review, not a claim that all browser anchors have been tested.

## Prepared engineering handoff and acceptance

KC-Brain owns the map's content and correction of semantic findings. Agent-Brain reviews the exact graph and claim summaries, especially sufficient-versus-necessary conditions, source status, planning boundaries and inference-versus-reading relations. Existing reviews of the full articles are not transferred into an independent verdict on this new synthesis.

KC-SWE receives the already written artifacts for necessary repository and site operations:

1. Reconcile the existing integration work; do not create a second research programme. Preserve the source pins or produce a separately identified, reviewed snapshot after source adoption.
2. Run the map validator and unit controls, then the repository's current checks in its mandated environment. Run optional source-object verification with all named commits available. Check actual source locations and links; report missing objects or ambiguous anchors rather than inventing success.
3. Perform the narrow nine-paper/thirty-document count integration while retaining the negative controls above. Do not mix this with an allowlist decision or weaken DCO/source checks.
4. Render a readable list and an optional graph with separate filters for documents, terms, claims, plans and required outputs. For each claim show plain meaning, premises, limits, source pin and proposal status. Do not make plan-only nodes clickable as nonexistent manuscripts. Do not infer task progress from edge presence.
5. Build the reading surface from the actual accepted source commit. A public proposal view, if used, must be explicitly labeled and must not masquerade as the accepted corpus. Return the source/site/build/deployment identities and actual served article/map URLs, verify content and source manifest, math/tables/links where applicable, keyboard/mobile reading and available download routes. A local build or HTTP success alone is insufficient.

This file is an original project integration note under the repository text licence. It reproduces no external-book text and changes no theorem, wire schema, task state, deployment or corpus admission by its existence.

---
title: "Knowledge Contract v2 source triage — negative results, semantic representations and provenance"
sources: none
status: "author-only claim-location screening; external primary source review NOT_MEASURED"
---

# Fifth claim-location triage: 12 further historical v2 entries

## Exact scope and evidence limit

This wave screens 12 additional historical IDs from [V2_REFERENCES.tsv](V2_REFERENCES.tsv), following [01](CLAIM_TRIAGE_WAVE_01.md), [02](CLAIM_TRIAGE_WAVE_02.md), [03](CLAIM_TRIAGE_WAVE_03.md) and [04](CLAIM_TRIAGE_WAVE_04.md). The accepted edition-1.1 manuscript comparison is pinned to `fb410a8460677b229d2240ba0fb27d184f48aa61`; F01 is a separate research draft. The repository paper paragraphs and historic bibliography inventory were read, **not** the twelve external primary works. All twelve remain `NOT_RECHECKED`, regardless of historical v2 labels and dated link checks. An author-only location comparison is neither a primary-source verification nor Agent-Brain's independent review.

`no-direct-claim` means no sentence currently warrants inserting the historic citation; the record remains in the v2 inventory. `candidate-limited` identifies a *possible new related-work comparison*, conditional on a fixed-edition primary reading and an exact matching sentence. A matching word or field does not establish a borrowed method or formal result.

| Historic ID and work | Exact target location / absence | Decision | Scope and material non-support |
| --- | --- | --- | --- |
| **V2-056** Barrault et al., *Large Concept Models* (2024) | `semantic-objects-and-context` §§2,4 defines explicit attributed object tuples and conditional results. | **no-direct-claim** | No sentence-representation language model is trained, used or benchmarked. The tuples are not identified with learned latent embeddings. |
| **V2-057** Peyrard et al., agentic semantic decoding position paper (2024) | `interaction-and-memory` §§2,6 interprets acts and limits claims about recorded learning. | **no-direct-claim** | It implements no semantic-decoding algorithm or evaluation from this position paper; local act semantics is not source-method conformance. |
| **V2-059** Paige, Cabot, Ernst, foreword on negative results (2017) | `evidence-and-falsification` §§5–7 requires retaining adverse cases and reporting unknown/unmeasured outcomes. | **candidate-limited** | A fixed primary reading might support a narrow *reporting-practice comparison*. A foreword cannot prove the manuscript's conditional theorems, checking completeness, runtime success or measured effectiveness. No new citation yet. |
| **V2-060** Priest, *The Logic of Paradox* (1979) | `retrieval-and-context-composition` §2 explicitly distinguishes reporting categories from a many-valued logic. | **no-direct-claim** | There is no paraconsistent consequence relation or four-valued formal semantics. Retain the historic classical `⟂` marker. |
| **V2-061** Ramanathan et al., Piranha feature-flag cleanup (2020) | `revision-and-governance` §§4–6 concerns adoption and historical identity. | **no-direct-claim** | No feature-flag debt, automated code removal or Piranha experiment is modelled or compared. |
| **V2-063** Reiter, closed-world databases (1978) | `retrieval-and-context-composition` §2 states unsupported-in-package does *not* imply false in the whole corpus. | **no-direct-claim** | The paper does not infer negation from database absence or assume a complete closed world. Retain the historic `⟂` marker. |
| **V2-066** Salehi, Erol-Kantarci, Niyato, semantic communication (2025) | `semantic-objects-and-context` §§2–3 treats source meaning, attribution and applicability. | **no-direct-claim** | No communication channel/encoder, transmission experiment or metric is specified. Source representation is not a replicated communication-system result. |
| **V2-067** Shapiro et al., conflict-free replicated data types (2011) | `interaction-and-memory` §5 Proposition 2 assumes atomic event records and scoped duplicate identity. | **no-direct-claim** | This is not a CRDT join algebra, an eventual-convergence theorem or a distributed-replication test. |
| **V2-068** von Wright, deontic logic (1951) | `revision-and-governance` §5 limits normative admission to authority/scope. | **no-direct-claim** | No modal obligations calculus or deontic inference is defined; adoption is expressly not a truth-preserving inference. |
| **V2-069** W3C PROV-O ontology (2013) | `semantic-objects-and-context` §1 and `revision-and-governance` §1 cite **PROV-DM** vocabulary. | **no-direct-claim** | A PROV-DM citation does not assert PROV-O RDF/OWL serialization, entailment, or conformance; no such graph is built here. |
| **V2-070** Wang et al., AgentDropout (2025) | `knowledge-utility` §§2–4 identifies costs, baseline and causal attribution. | **no-direct-claim** | No agent-elimination method or token-saving benchmark is implemented, reproduced or attributed. |
| **V2-071** Widdows, *Geometry and Meaning* (2004) | `constrained-transformations` §4 uses a finite Boolean signature and projection laws. | **no-direct-claim** | No geometric-semantic embedding or equivalence method from this book is defined; a mathematical projection is not evidence of that particular geometry. |

## Per-manuscript accounting

| Manuscript | Existing v2 citation in this wave | Added References | Held for primary reading | No present matching claim |
| --- | --- | ---: | --- | --- |
| `evidence-and-falsification` | none | 0 | V2-059 | none |
| `semantic-objects-and-context` | none | 0 | none | V2-056, V2-066, V2-069 |
| `interaction-and-memory` | none | 0 | none | V2-057, V2-067 |
| `revision-and-governance` | none | 0 | none | V2-061, V2-068 |
| `retrieval-and-context-composition` | none | 0 | none | V2-060, V2-063 |
| `knowledge-utility` | none | 0 | none | V2-070 |
| `constrained-transformations` | none | 0 | none | V2-071 |
| `controlled-knowledge-reuse`, proposed F01 | not newly assessed | 0 | none | no extrapolation |

This wave has exactly **12 distinct IDs**: **0 already present, 1 candidate-limited, 11 no-direct-claim**. Across five waves, **62/74** historical references have *author-level claim-location screening*, **12 remain**: V2-018/019/020/021/022/024/033/034/035/072/073/074. These counts are **not** full-text verification or accepted-citation counts; references appearing in several paper comparisons count once. The 74 inventory records and their old labels remain untouched.

No new paper references, mathematical changes, source registrations, release permissions, allowlists, site deployments, evidence assessments, indices or Muneral changes were made. The missing historic verification JSON was not reconstructed. To admit a citation, inspect the particular primary source passage and version, write its precise supported and unsupported scope and paper sentence, then seek an independent exact-byte review. Structural checks and CI do not replace scientific review.

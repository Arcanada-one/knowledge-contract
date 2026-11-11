---
title: "Knowledge Contract v2 source triage — test generation, provenance and covering bounds"
sources: none
status: "author-only surviving-claim screening; primary-source review NOT_MEASURED"
---

# Third claim-location triage: 12 additional historical v2 entries

## Source and verification boundary

This wave screens **twelve non-overlapping IDs** in [V2_REFERENCES.tsv](V2_REFERENCES.tsv) after [wave 01](CLAIM_TRIAGE_WAVE_01.md) (12 IDs) and [wave 02](CLAIM_TRIAGE_WAVE_02.md) (14 IDs). The source catalogue is the preserved v2 bibliography (74 entries), not a newly verified reference library. The comparison baseline is the accepted edition-1.1 manuscript tree at Knowledge Contract commit `fb410a8460677b229d2240ba0fb27d184f48aa61`. PR67's proposed changes are not silently substituted for that baseline. The ninth F01 remains a research draft.

I re-read the relevant **repository paper sections** and inventory entries. I did **not** read the full external articles, books or preprints in this wave, test their URLs, or independently revalidate the inherited v2 labels. All source-inspection depth for the rows below is `NOT_RECHECKED`. A historical “⟂”, dated check or claimed reading is retained as historical provenance only. A paper-level location is a *claim locator*, not proof that the outside work establishes the claim.

A `candidate-limited` record describes a possible *new, explicitly bounded related-work comparison*, conditional on actual primary-source inspection. `already-present` means the relevant source is already credited in the paper. `no-direct-claim` means the accepted paper contains no claim requiring this particular source; it does not delete the historical entry or deny possible future research relevance.

| V2 ID and historical topic | Surviving paper location or absence | Decision | Possible supported scope; crucial non-support |
| --- | --- | --- | --- |
| **V2-023** — Chvátal (1979), greedy set covering | `retrieval-and-context-composition` §4, Proposition 2 reduces a restricted composition instance to set cover; Proposition 3 explicitly bounds cardinality-greedy under submodularity. | **candidate-limited** | A reviewed Chvátal article might support a clearly distinguished *classical set-cover greedy* comparison. The paper's current approximation statement is a submodular cardinality result and cannot silently be justified by substituting a set-cover ratio. Historical **⟂** is retained. |
| **V2-025** — Çelik et al. (2019), mutation analysis for Coq | `evidence-and-falsification` §5 describes manually designed adverse cases and checks of enforcement. | **candidate-limited** | A future methods comparison could distinguish mutation analysis of proof artifacts from the paper's constructed logical examples. No Coq project, mutation operator, adequacy score or theorem mutation experiment is reported. |
| **V2-026** — Cordy et al. (2023), mutation model checking | `evidence-and-falsification` §§4–5 distinguish executable tests, exhaustive finite checks and refuting counterexamples. | **candidate-limited** | Primary reading might motivate a comparison to strengthening specifications using mutant models. The reported finite assignments are neither a mutation-model-checking experiment nor evidence of formal-specification completeness. |
| **V2-029** — Dinur and Steurer (2014), parallel repetition | `retrieval-and-context-composition` §4 gives a finite set-cover special case and a cardinality-greedy bound. | **no-direct-claim** | The paper invokes no parallel-repetition theorem, PCP gap amplification or hardness-of-approximation transfer from this result. A generic word “hardness” would not establish that relation. Historical **⟂** is retained. |
| **V2-031** — Farquhar et al. (2024), semantic entropy and hallucinations | `evidence-and-falsification` §2 separates assessment axes and §6 requires explicit comparators and denominators. | **no-direct-claim** | The manuscript defines no sampling-based semantic-entropy estimator and reports no hallucination-detection benchmark. Its categories for evidence status are not calibrated semantic uncertainty estimates. |
| **V2-032** — Feige (1998), logarithmic inapproximability for set cover | `retrieval-and-context-composition` §4, Proposition 2 concerns a *restricted* set-cover embedding. | **no-direct-claim** | The paper does not prove a sharp threshold, transfer Feige's complexity assumptions or derive a lower bound on its complete context-composition problem. NP-hardness of a special case is not a proof of this approximation threshold. Historical **⟂** is retained. |
| **V2-037** — Groth, Gibson and Velterop (2010), nanopublications | `semantic-objects-and-context` §2 defines attributed semantic objects, explicit grounding and interpretation. | **candidate-limited** | A primary reading could support a concise comparison between atomic assertion/provenance packaging and KC's explicit grounds. The paper neither encodes a nanopublication nor claims conformance to a nanopublication format or trustworthy assertion semantics. |
| **V2-038** — Jeong, Kim and Park (2025), *The Algebra of Meaning* preprint | `constrained-transformations` §4 uses finite propositional-model equivalence and reconstruction; `semantic-objects-and-context` §4 proves elementary conditional results. | **no-direct-claim** | Neither paper adopts a Montague-style compositional semantic algebra from this preprint or establishes a general algebra of human meaning. Similar titles and mathematical notation do not supply a source-to-claim relation; preprint status remains explicit. |
| **V2-039** — Johnson (1974), approximation algorithms | `retrieval-and-context-composition` §4 distinguishes the set-cover reduction from the submodular cardinality result. | **no-direct-claim** | No Johnson-specific approximation guarantee or algorithm is claimed or needed for the proof presented. The historical source can remain available for a later, actually written comparison. Historical **⟂** is retained. |
| **V2-040** — Karp (1972), combinatorial reducibility | `retrieval-and-context-composition` §1 explicitly credits set-cover difficulty, and §4 Proposition 2 gives the restricted embedding; existing References [2]. | **already-present** | The established source is acknowledged for classical complexity context. This paper proves its own restricted mapping; the reference neither validates actual semantic annotations nor says every practical retrieval task is computationally hard. No fresh full-text check is claimed. |
| **V2-041** — Howden (1982), weak mutation testing | `evidence-and-falsification` §5 discusses stopping and adverse-case construction. | **candidate-limited** | After reading the original, a precisely scoped comparison might illuminate distinctions between killing mutants and demonstrating completeness of a test set. Neither weak mutation nor a completeness theorem is implemented or measured here. |
| **V2-042** — W3C JSON-LD 1.1 (2020) | `semantic-objects-and-context` §2 describes a semantic-object record and cites PROV-DM/SKOS, not a JSON-LD serialization. | **no-direct-claim** | The project does not state a JSON-LD context, expansion/compaction algorithm, or JSON-LD 1.1 conformance for this theoretical object. JSON-shaped records alone do not justify this citation. |

## Reconciliation by paper

| Paper | Already in accepted paper | New references inserted | Held pending actual primary reading | No direct matching claim |
| --- | --- | ---: | --- | --- |
| `retrieval-and-context-composition` | V2-040 | 0 | V2-023 | V2-029, V2-032, V2-039 |
| `evidence-and-falsification` | none of this wave | 0 | V2-025, V2-026, V2-041 | V2-031 |
| `semantic-objects-and-context` | none of this wave | 0 | V2-037 | V2-042 |
| `constrained-transformations` | none of this wave | 0 | none | V2-038 |
| Remaining accepted papers and proposed F01 | not newly assessed | 0 | not assessed | no extrapolation |

**Accounting:** wave 03 has **12 distinct new IDs**: **1 already cited, 5 candidates for *possible* bounded comparisons, 6 without a matching current claim**. Across waves 01–03, **38/74** historical IDs have author-level claim-location screening; **36** remain. These are not 38 independently verified sources. Existing bibliography history retains all 74. This wave makes **zero** manuscript citation or mathematical/proof changes, and does not change source admission, export allowlists, released indexes, website pages, CI semantics or Muneral tasks.

## Requirements before any admission

For each held candidate, inspect an identifiable primary edition or dated institutional original, record precise sections and which claim that passage actually supports, and explicitly separate claims outside the citation's scope. Only then consider proposing a new limited related-work sentence and a per-sentence review record. Agent-Brain's subsequent exact-byte substantive review remains independent of the author's screening. A positive structural validator result or passed CI does not establish source authenticity, reviewer independence, scientific truth, live deployment or human acceptance.

The missing `bibliography-verification-20261007.json` is not synthesized from historical link checks; the v2 link-check script was reported as URL-reachability only. This report represents no new full-primary-text verification, independent replication or publication event.

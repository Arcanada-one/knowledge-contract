---
title: "Knowledge Contract v2 source triage — identity, semantic uncertainty and finite coverage"
sources: none
status: "author-only surviving-claim screening; external primary-source review NOT_MEASURED"
---

# Fourth claim-location triage: 12 additional historical v2 entries

## Method and verification boundary

This is a **new, non-overlapping screening wave** from the 74 preserved historical entries in [V2_REFERENCES.tsv](V2_REFERENCES.tsv), following [wave 01](CLAIM_TRIAGE_WAVE_01.md), [wave 02](CLAIM_TRIAGE_WAVE_02.md) and [wave 03](CLAIM_TRIAGE_WAVE_03.md). It examines V2-043 through V2-055 **except V2-047**, which was already considered in wave 01. No record is deleted from the inventory.

The paper comparison baseline is the accepted edition-1.1 Knowledge Contract source at `fb410a8460677b229d2240ba0fb27d184f48aa61`. F01, the ninth manuscript, remains a separate research draft. I reviewed the relevant repository paragraphs and inherited bibliography descriptions, **not** the full external works or their live URLs. Every row therefore has inspection depth `NOT_RECHECKED`. A v2 date, a historical link check or a bibliography label is provenance of the earlier claim, **not** independent source verification. In particular, neither a source title nor a shared technical term establishes that a cited result proves a current KC claim.

`already-present` identifies an existing citation; `candidate-limited` only proposes a future narrowly described related-work comparison after reading a primary edition; `no-direct-claim` explains why the current manuscript does not support inserting the historical source. These are not external-review verdicts, permissions to publish, or irreversible exclusions from historical bibliography.

| V2 record | Present paper locator or missing claim | Decision | Possible scope and explicit non-support |
| --- | --- | --- | --- |
| **V2-043** — Jain et al. (2020), mCoq mutation analysis | `evidence-and-falsification` §5 describes constructed adverse cases and finite logical checks, without a Coq verification project. | **candidate-limited** | After reading the paper, a *methods comparison* could distinguish mutation of proof projects from the constructed tests in KC. The current paper does not run mCoq, perform a Coq mutation campaign or report mutation adequacy; do not inherit its empirical conclusions. |
| **V2-044** — Kleene (1938), ordinal notation | `revision-and-governance` §4 and `semantic-objects-and-context` §4 prove bounded finite-graph properties. | **no-direct-claim** | No ordinal-notation system, recursive ordinal representation or transfinite termination argument appears in the accepted propositions. Finite iteration alone is not a claim relying on this work. |
| **V2-045** — Kuhn, Gal and Farquhar (2023), semantic uncertainty | `evidence-and-falsification` §2 separates evidential assessments; `interaction-and-memory` §7 limits observations about learning. | **no-direct-claim** | Neither paper estimates sequence-level semantic uncertainty from sampled language-model outputs, demonstrates paraphrase invariance or measures calibration. Qualitative uncertainty labels are not that estimator. |
| **V2-046** — Kuhn and Dumontier (2014), Trusty URIs | `revision-and-governance` §4 Proposition 1 reasons about an *assumed immutable pinned reference*; `controlled-knowledge-reuse` §3 distinguishes byte hashes from semantic truth. | **candidate-limited** | A primary reading may support a comparison with content-identifying persistent URIs. The proposition is conditional on an immutable revision identifier and does not implement Trusty URI generation, verification or decentralized persistence. A digest does not prove the source content true. |
| **V2-048** — Lan et al. (2021), semantic communication | `semantic-objects-and-context` §§2–3 defines object identity, interpretation and grounds. | **no-direct-claim** | No semantic communication channel, encoder/decoder, rate–distortion objective or channel performance is defined or evaluated. A term like “conveying meaning” does not establish method equivalence. |
| **V2-049** — Levenchuk, First Principles Framework repository | `controlled-knowledge-reuse` §2 and `semantic-objects-and-context` §2 define their own task-, role- and context-scoped structures. | **no-direct-claim** | No identified statement imports a specific theorem or definition from the pinned external repository. Its noted missing license also precludes copying implementation/text; citation alone does not solve copying rights or establish conformance. |
| **V2-050** — Lewis et al. (2020), retrieval-augmented generation | `retrieval-and-context-composition` §1 explicitly names the RAG formulation and cites the work as References [1]. | **already-present** | The citation supports historical architecture context (retrieval conditioning generation). The paper's extra delivery-preservation duties are its own defined obligations, not a result established by the NeurIPS experiment. No fresh full-text recheck is claimed here. |
| **V2-051** — Liang et al. (2022), lifelong-learning semantic communication | `interaction-and-memory` §6 distinguishes recording a correction from evidence of improved learning; `semantic-objects-and-context` §3 defines required applicability. | **no-direct-claim** | Neither paper implements continual training or reasons about the performance of a semantic communications link over time. No measured benefit or benchmark is reported. |
| **V2-052** — Liu et al. (2023), meaning representations from autoregressive trajectories | `semantic-objects-and-context` §4 proves conditional statements about explicit interpretations, not recovered autoregressive latent trajectories. | **no-direct-claim** | No trajectory representation is trained, extracted, validated or identified with the model's explicit semantic-object tuple. A conceptual “meaning representation” is not a replicated model result. |
| **V2-053** — Lovász (1975), integral/fractional cover ratios | `retrieval-and-context-composition` §4 Proposition 2 embeds a restricted finite set-cover instance; Proposition 3 requires monotone submodularity for cardinality-greedy. | **no-direct-claim** | The manuscript does not construct a fractional LP relaxation, prove an integrality gap or transfer a fractional-cover ratio to semantic selection. A reduction to set cover is insufficient for that bound. |
| **V2-054** — McCarthy (1980), circumscription | `revision-and-governance` §§3–5 distinguishes corrections, versioned norms and adoption. | **no-direct-claim** | No circumscription minimization predicate, nonmonotonic entailment calculus or implementation of that formalism is defined. Historical relevance to nonmonotonic reasoning is not evidence for the current version-adoption proposition. The inherited classical-source status is retained. |
| **V2-055** — Merkle (1979), authentication and hash-based systems | `controlled-knowledge-reuse` §3 explains byte identity under a declared serialization; `revision-and-governance` §4 assumes immutable pinned revisions. | **no-direct-claim** | Neither text specifies an authenticated Merkle tree, membership proof, authenticated directory or security reduction. A bare hash or Git revision name cannot be equated to the security claims of the thesis. |

## Paper-by-paper reconciliation

| Accepted paper | Existing historical citation in this wave | New citations inserted | Held for actual primary reading | Do not insert without a new matching claim |
| --- | --- | ---: | --- | --- |
| `retrieval-and-context-composition` | V2-050 | 0 | none | V2-053 |
| `evidence-and-falsification` | none of this wave | 0 | V2-043 | V2-045 |
| `revision-and-governance` | none of this wave | 0 | V2-046 (conditional comparison only) | V2-044, V2-054, V2-055 |
| `controlled-knowledge-reuse` | none of this wave | 0 | V2-046 (same **single** record, no extra count) | V2-049, V2-055 |
| `semantic-objects-and-context` | none of this wave | 0 | none | V2-048, V2-049, V2-051, V2-052 |
| `interaction-and-memory` | none of this wave | 0 | none | V2-045, V2-051 |
| Other accepted papers and F01 | not newly screened | 0 | none | no extrapolation |

**Accounting:** wave 04 includes **12 unique entries**, of which **1 already occurs in an accepted paper, 2 are candidates for a new *bounded* methods comparison, and 9 lack a direct surviving claim**. Across the four waves, **50/74 historical IDs have been screened at author level**, leaving **24**. These counts do **not** mean 50 sources have undergone full-text verification. Some records have multiple paper locators but count once.

The inventory remains intact; there are **zero** new manuscript references, changed proofs, model runs or scientific acceptance decisions in this wave. In particular, historical URL-reachability labels must not be converted to content-verification evidence or independent reviewer identities. The missing historical verification JSON is not reconstructed from guesses.

## Next admissible evidence

For either held candidate, obtain a fixed identifiable primary edition, read the exact relevant section, record its passage-level supported and unsupported scope, and then propose a *new, explicitly qualified manuscript sentence* with traceability to that source. A source-to-claim record must pin the actual document revision and evaluation depth. Agent-Brain must separately review any resulting exact manuscript bytes. Repository CI, syntactic graph validation and this author's triage do not replace that review, site publication or readback.

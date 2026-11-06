---
title: Knowledge Contract v2 citation recovery — first claim triage
sources: none
status: author-only claim-location triage; no new primary-text verification or manuscript citation
---

# First claim-to-reference triage: 12 historical v2 records

## Method and evidence boundary

This review follows [BASELINE.md](BASELINE.md) and [V2_REFERENCES.tsv](V2_REFERENCES.tsv). The 74 historical v2 bibliography paragraphs remain intact in the TSV; this first wave examines **12 identifiers**, not the whole bibliography, and makes **no assertion that the original works were newly read**. Historical verification labels from the pinned v2 blog are preserved but do not establish current independent primary-source checking.

The actual target texts were read at the accepted Knowledge Contract main commit `fb410a8460677b229d2240ba0fb27d184f48aa61`; the ninth F01 is a separate research-draft and is not edited here. Section anchors below are from the paper Markdown, not inferred browser anchors. Quoted fragments are locators, not evidence that the outside work proves them.

This is **candidate scope matching**, not permission to add citations. The decision classes below are: `already-present` (citation occurs in the target paper), `candidate-limited` (a future explicit related-work sentence might make a primary-source check relevant), and `no-direct-claim` (the existing sentence does not make the cited work's particular claim; do not pad). None of the last two is an irreversible deletion from the historical bibliography.

| v2 ID | Target manuscript and exact location / surviving claim | Triage decision | Supported scope to check, and explicit non-support |
| --- | --- | --- | --- |
| V2-001 — Alchourrón, Gärdenfors, Makinson (1985) | `revision-and-governance` §1: “study contraction and revision of logical theories under explicit postulates” | **already-present** as current References [3] | The bibliographic record, year and DOI match. Current paper explicitly limits its own revision model to versioned records, assessments and adoption; AGM does not certify those implementation decisions. Historical v2 “read edition” is not a new full-text recheck. |
| V2-002 — Dempster (1967) | `evidence-and-falsification` §4: “uncertainty estimates, and stopping conditions” | **no-direct-claim** | This paper does not derive belief-function or upper/lower-probability combination rules. Mention of uncertainty alone is not a reason to restore Dempster. |
| V2-003 — Dung (1995) | `evidence-and-falsification` §3: “justification graph contains claim nodes, premise nodes, and explicit inference applications” | **no-direct-claim** | A finite acyclic proof DAG with sound inference is not an abstract argumentation/attack-acceptability framework. Cite Dung only if an actual attack/defeat semantics is separately discussed and checked. |
| V2-012 — Beer et al. (2001) | `evidence-and-falsification` §3: “An empty domain makes a universal formula true vacuously” and “test set containing no relevant negative case” | **candidate-limited** | Temporal-model-checking vacuity is a plausible related-work comparison. It cannot on its own establish the paper's generic nonempty-test-set criteria or operational success; check primary text and add a narrowly described analogy only if useful. |
| V2-013 — Belnap (1977) | `retrieval-and-context-composition` §2: categories “supported, partial, unsupported, conflicted, and unknown” immediately say these are “not a universal many-valued logic” | **no-direct-claim** | These are reporting categories, not a stated Belnap truth algebra; citing it as their formal semantics would misattribute the current definitions. |
| V2-014 — Black, Okun, Yesha (2000) | `evidence-and-falsification` §4: “Adversarial cases should probe both the required conditions and the system's enforcement” | **candidate-limited** | Specification mutation may be relevant methodology, but the paper offers constructed cases and does not claim a mutation-operator implementation or coverage guarantee. A source-limited methods paragraph requires primary review. |
| V2-015 — Budd, Gopal (1985) | Same paper §4, requirement for negative/adverse cases | **candidate-limited** | Specification mutation is not interchangeable with a manually constructed countermodel or a theorem refutation. Do not infer that a reported finite case was a mutation-test experiment. |
| V2-017 — Buneman, Khanna, Tan (2001) | `semantic-objects-and-context` §1: “W3C PROV-DM describes provenance through entities, activities, and agents” | **no-direct-claim** | The paper does not characterize why/where database provenance; PROV-DM is already cited for its narrower vocabulary. A data-provenance algebra would need an actual new proposition/discussion, not a padded reference. |
| V2-028 — DeMillo, Lipton, Sayward (1978) | `evidence-and-falsification` §4: constructed adverse cases and independent checks | **candidate-limited** | Testing history could motivate a separately worded design rationale after full source review. The paper neither uses nor measures mutation-test selection techniques from this citation. |
| V2-036 — Green, Karvounarakis, Tannen (2007) | `semantic-objects-and-context` §2: source grounding/attribution | **no-direct-claim** | No provenance semiring is defined, computed or proved here. A grounding record is not automatically the polynomial provenance semantics of this work. |
| V2-047 — Kupferman, Vardi (2003) | `evidence-and-falsification` §3: vacuity and empty assessment domains | **candidate-limited** | Temporal-logic vacuity is a potential comparison, not primary validation of the general data/assessment protocol. Primary-source scope and exact matching prose remain to be checked. |
| V2-058 — Offutt (1992) | `evidence-and-falsification` §4: leakage, repeated/related test cases | **no-direct-claim** | No software-testing coupling-effect prediction is established or measured by the current text. Do not equate duplication/independence warnings with this particular theory. |

## Per-paper disposition in this wave

| Paper | Already present | New citations added | Held for primary reading | No matching present claim in this wave |
| --- | ---: | ---: | --- | --- |
| `revision-and-governance` | V2-001 (already References [3]) | 0 | none | none |
| `evidence-and-falsification` | 0 | 0 | V2-012, V2-014, V2-015, V2-028, V2-047 | V2-002, V2-003, V2-058 |
| `semantic-objects-and-context` | 0 | 0 | none | V2-017, V2-036 |
| `retrieval-and-context-composition` | 0 | 0 | none | V2-013 |
| Other five manuscripts, including proposed F01 | not assessed in this wave | 0 | not yet screened | no disposition inferred |

**Result:** 12/74 historic IDs screened against current claim locations; 1 is already cited, 5 are candidate-limited, 6 lack a direct matching current claim in this wave. No historical source was discarded or reclassified as independently verified. No bibliography text, mathematical claim, proof, source allowlist, catalogue, site or index was changed.

## Next evidence requirements

For each held candidate: obtain the full primary/official text or an identifiable precise excerpt, independently verify its author/version/section and supported result, then decide whether a **surviving actual claim** deserves a narrowly worded related-work sentence. If not, record `drop-with-reason` and retain the v2 historical citation in the audit. Source availability alone does not mean an applicable citation. Continue the other 62 identifiers and all nine manuscripts before calling the nine-paper restoration complete.

The missing historical `bibliography-verification-20261007.json` has not been recovered in this triage. No metadata-only substitute is represented as that file. The accepted source commit and this proposal branch are not a deployed contract.place publication.

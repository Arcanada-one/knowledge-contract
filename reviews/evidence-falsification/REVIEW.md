---
title: Evidence and falsification editorial review
sources: none
status: producer-reviewed; independent review outstanding
---

# Evidence and falsification: revision record

## Scope and exact subjects

This is the sixth existing manuscript in the author-directed editorial sequence. The target is [Evidence, Reasoning, and Falsification in Knowledge Systems](../../papers/evidence-and-falsification/PAPER.md), not a new empirical benchmark or a source-book conversion. KC-Brain authored the complete revision and its checking materials.

Pinned source: `ea0c30575d56e793fb2875df47126ab3f6dc30ad`, blob `a84e8250192936ea666b5f055da393ea5ac43966`, SHA-256 `95acb937c5aa68572eb60ec723d17c628bcd28a778490c09ef6b434ef0f63494`, 14,848 UTF-8 bytes.

Candidate: SHA-256 `926b29d227f9c576bc69834ae6f8a72d514fc3b5916bf66c966df5aee5a2ce28`, 22,620 UTF-8 bytes. Edition 1.1 is retained as publication context, not claimed as a newly released edition. Source merge, website rendering and index admission remain separate observations.

## Changes and rationale

| Area | Revision | Evidential status |
| --- | --- | --- |
| Abstract and question | Clarify the methodological contribution, deductive method and empirical limits | Exposition, not a new general truth algorithm |
| Five assessment axes | Present their existing meanings in a captioned table | Existing distinctions preserved; no statistical independence claim |
| Subject binding | Identify claim/artifact/implementation revision, configuration and representation | Scientific scope clarification; matching a digest does not prove truth or delivery |
| Evidence types | Tabulate immediate support and non-implications | Exposition and scope protection |
| Finite coverage | Distinguish complete finite coverage, empty domain, empty relevant tests and repeated cases | Scientific clarification; no count of real-world experiments |
| Review and oracle dependence | Explain self-review, non-blind review and shared-input errors | Procedure distinction; no independent verdict claimed by the producer |
| Refutation protocol | Separate premise-violating boundary cases from in-premise theorem refuters | Scientific clarification of the original conditional propositions |
| Execution quantifiers | Separate never-success claims from claims allowing a nonzero error probability | Logical scope clarification; no probability estimate introduced |
| Unresolved outcomes | Preserve denominators and show a fixed-ledger interval for unresolved results | New arithmetic illustration, explicitly not a confidence interval |
| Conclusion | State what this method establishes and what remains unmeasured | Bounded synthesis |

The entire original Section 3, both proposition statements and proofs, Section 7 including the implementation-exclusion formula and linked historical evidence, Section 8, front matter, title, bibliography, all mathematical expressions and link targets are unchanged. Original headings occur in the same order; Section 9 Conclusion and two captioned tables are added. No normative schema, requirement ID, historical raw record, catalogue entry or allowlist is changed.

## Scientific self-review

The induction argument remains conditional on true premises, sound rule semantics and satisfied side conditions in one model. A true conclusion observed under false or unknown premises does not establish that derivation, but a failed premise also does not logically force every possible conclusion to be false. Cyclic justifications are not silently admitted into the acyclic proof.

The universal-countermodel result requires an in-domain witness and the same predicate interpretation. Changing the domain after seeing a failure creates another claim; it does not revise the historical verdict on the original. Where membership or the oracle is unresolved, no definitive refutation is asserted without resolving it.

For finite checking, the model separates an empty domain, an untested nonempty domain, a partially tested domain without an observed counterexample, and a fully checked fixed finite domain. The word established is scoped to that finite model and trusted exact observations. It does not establish discovery of every relevant real input or soundness of a semantic oracle. Nondeterministic exclusion requires examination of every admitted outcome in the declared model, not one favorable sample. A nonzero-probability claim has a different refutation criterion from a claim of impossibility.

The denominator illustration uses two passes, one failure and one unresolved outcome: resolved-only fraction 2/3, confirmed fraction 2/4, possible final fraction from 1/2 to 3/4. These are exact statements about four records, not population inference. Different models' input configurations, executed occurrences and assertion counts are never added as interchangeable experiments.

The writing pass adapts the previously read task-brief, protected-meaning, condition-preservation, paragraph-structure and whole-result review methods. Their original applied-Russian profile is not claimed to have been validated generally for English scientific prose. No native toolkit execution, fresh validation of all source dependencies, superiority effect or new executor competency is asserted. No source-book text is reproduced.

## Actual checks and reproducibility

Run from repository root:

```sh
python3 -B tools/verify_evidence_falsification.py --paper papers/evidence-and-falsification/PAPER.md
```

[RESULTS.md](RESULTS.md) preserves the deterministic JSON from the actual local execution under Python 3.13.5. The standard-library checker makes no network, model or server calls. All 23 document conditions and 16 boundary controls passed; seven deliberately weakened strategies were distinguished by constructed witnesses.

The four finite families are explicitly bounded: 4,096 domain/test/truth assignments over four inputs; 4,096 truth-set assignments for a fixed four-node derivation skeleton over two worlds; 4,096 domain/condition/admission-relation assignments over three inputs; and 64 small result ledgers with 159 possible resolution counts. No violation was found within those carriers. Vacuous and no-execution cases are counted separately. Neither these enumerations nor a hash lock prove the paper's general propositions.

The same producer wrote the models and comparison procedures. The universal-scope model uses a set-based classifier and a bitmask comparison, but these are not independently authored oracles. The deduction model is a truth-set illustration, not a deployed inference engine. Deliberately weaker rules are constructed comparison strategies, not discovered mutations or bugs in production KC.

A second run reproduced JSON byte for byte. Appending an extra line to a separate copy caused the exact-candidate condition to fail and exit 1. This tests integrity-lock behavior, not complete semantic detection. Pandoc 3.1.11.1 parsed the complete manuscript, recognizing both tables and the mathematical expressions, and a separate heading comparison preserved the old heading order. That is a parser check, not the required full repository Pandoc 3.1.3 run, visual page inspection or journal-template compliance.

## Sources, acceptance and delivery

The two existing primary references remain unchanged: Hoare for conditional program-logic reasoning, PROV-DM for provenance vocabulary. W3C's official document was reread for that limited attribution; this revision adds no quotation or new external research claim. The DOI resolver for the Hoare record was inaccessible during this pass, so no claim of a fresh whole-paper reread is made. The original project reference is retained, not replaced with invented bibliographic details.

Agent-Brain is requested to review the entire exact candidate against the pinned original, especially quantifiers, vacuity, unknown outcomes, shared-oracle dependence and the limits of the fixed-ledger example. This file is producer self-review, not independent scientific acceptance or external academic peer review. Reader-comprehension results are not measured.

KC-SWE is requested only for the necessary current-head project/server checks and normal integration under AGENTS.md, not authorship. Run the new checker explicitly and compare its output with RESULTS.md; existing CI does not automatically establish that a newly added script ran. Preserve code/text licenses and lawful DCO, historical observations, publication decisions and index separation. A later content change requires renewed version binding and review rather than silently updating the content lock.

Canonical Markdown is the publication input. A downloadable chat PDF is not required to recover or OCR the manuscript. The existing site build must use the accepted immutable source revision, render its actual text/math/tables and verify the served manifest. Availability of a branch file is not evidence that the website already serves it.

---
sources: none
---

# Engineering Studies and Evidence

Six studies connect the scientific claims to actual finite checks, counterexamples, comparisons and analytical results. Each identifies its materials, unit of observation, available reproduction procedure and limits. The machine-readable [claim–evidence index](evidence-index.json) provides 24 explicit bindings; per-study origin records identify exact evidence bytes.

| Document | Subject |
| --- | --- |
| [Contract profiles: finite conformance, trust boundaries, and a strong simple comparator](contract-profile-conformance/STUDY.md) | Finite contract checks, false trusted-input counterexamples and an equal strong-comparator result. |
| [Dependency closure, readable artifact layouts, and a pinned package replay](dependency-closure-and-package-delivery/STUDY.md) | Historical package evidence and a public exhaustive replay of a finite dependency graph. |
| [Reproducible transcription is not preservation of uncertainty](source-transcription-and-uncertainty/STUDY.md) | Retained generated descriptions, lost uncertainty and a reproducible synthetic projection counterexample. |
| [Executable projections, addressable revisions, and the limits of graph minimality](executable-projections-and-revision/STUDY.md) | Finite consumer checks, paired agent tasks, addressed revision and the limits of graph minimality. |
| [Controlled reuse: admission counterexamples and the cost of a cache hit](reuse-admission-and-cost-controls/STUDY.md) | Executable admission counterexamples and an analytical break-even calculation with explicit costs. |
| [Editing a scientific section with a knowledge toolkit: a masked single-section comparison](editorial-skill-pilot/STUDY.md) | One preregistered editorial comparison, hash-pinned retained outputs, masked review and an observed tie. |

## Counting and interpretation

Ordinary conformance cases test an explicitly declared expected behavior. Positive controls require admission or a successful result; negative controls require rejection or another specified outcome. Cases deliberately supplying false trusted premises belong to a separate boundary series. An expected acceptance of a false premise is evidence of that boundary, not a semantic success in the ordinary denominator.

The contract-profile study therefore reports 35 author regression scenarios and 26 separately composed ordinary scenarios, alongside two and four accepted false-input cases. The package study reports 44 ordinary checks (21 expected acceptances and 23 expected rejections), alongside two accepted misleading-input cases. Its historical file has 46 rows; the raw rows remain unchanged. These suites probe different operations and inputs and are not pooled into a common success rate.

Calls, cases, criteria, records, graph subsets, page entries and source families are different units. Nested criteria remain nested: the editorial pilot's eight conceptual distinctions are part of protected claim 11 within a 19-claim checklist. Repeated or algebraically related checks do not become independent observations by increasing a counter. Development, regression, held-out evaluation and counterexample construction have different evidential force. Equal scores on a coarse rubric do not establish identical quality or a method's advantage.

## Languages and source access

The retained source prose and most agent reports are in Russian, with English code and field names. The current studies provide English accounts of their design, principal results, failure mechanisms and limitations. They are not a full independently reviewed translation of every source. The [evidence language index](evidence-language-index.json) records the representation, prose language, hash and English summary location for all 47 evidence files, without changing their bytes or origin records.

The [historical recovery inventory](historical-recovery-gaps.json) separates missing synthetic runners and fixtures from restricted source books. A copyright limitation is not used to explain missing project-authored code. Retained reports remain inspectable where full historical replay is unavailable.

## Reproduction and review corrections

The edition-1.0 replay programs and their stored outputs remain in each `evidence/` folder as historical records. Their interpretation is narrowed where review found a defect. New programs and inputs are versioned separately under `checks/`; the [correction manifest](review-corrections.json) identifies exact hashes, outcomes and the earlier records to which they relate.

| New check | What it establishes | Boundary |
| --- | --- | --- |
| [Closure size and declared mutants](dependency-closure-and-package-delivery/checks/check_closure_size_and_mutations.py) | Counts delivered records for the retained graph and distinguishes three explicit traversal defects | Record count is not byte size; the fault model is finite |
| [Admission gates and costs](reuse-admission-and-cost-controls/checks/check_admission_and_cost.py) | Rejects missing, failed and unknown mandatory gates in a nine-gate synthetic profile and recomputes cost examples | Gate inputs are not authenticated; no historical service or agent run is repeated |
| [Uncertainty projection illustration](source-transcription-and-uncertainty/checks/demonstrate_uncertainty_projection.py) | Compares new synthetic output with a separately stored target and exposes omitted qualifiers and a damaged restoration trace | It illustrates a mechanism on invented inputs; it does not reconstruct the historical source corpus |

The method references for fixed-point reasoning, preregistration, program mutation, agent judging and transcription scores are in the [shared bibliography](../../reference/bibliography/BIBLIOGRAPHY.md#evaluation-methods). Each study distinguishes that background from its own observations.

[Publication home](../../README.md) · [Shared glossary](../../reference/glossary/GLOSSARY.md)

---
name: "contract-profile-conformance"
title: "Contract Checks: Contract profiles: finite conformance, trust boundaries, and a strong simple comparator"
short_title: "Contract Checks"
subtitle: "Contract profiles: finite conformance, trust boundaries, and a strong simple comparator"
artifact: "engineering-study"
edition: "1.1"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "Finite contract checks, false trusted-input counterexamples and an equal strong-comparator result."
study_type: "finite-implementation-evaluation"
review_state: "internally-reviewed"
---

<!-- markdownlint-disable-next-line MD033 -->
<a id="contract-profiles-finite-conformance-trust-boundaries-and-a-strong-simple-comparator"></a>

# Contract Checks: Contract profiles: finite conformance, trust boundaries, and a strong simple comparator

## Abstract

This study examines whether a finite implementation of a Knowledge Contract follows its declared structural and application rules. The implementer's development fixtures matched 35 of 35 expected ordinary outcomes; this is regression evidence. A separately composed control suite, prepared without inspecting the implementation but within the same research session, matched 26 of 26. These results concern already interpreted JSON instances. The implementation also accepted two author and four control inputs whose trusted annotations were deliberately false. Those acceptances expose a trust boundary and are excluded from the ordinary totals. A subsequent strong plain-form checker matched the recorded Knowledge Contract decisions on all nine shared scenarios after its author knew their inputs and expected outcomes. This shows that a direct checker can encode the tested obligations; it establishes neither generalization nor an advantage of the larger representation. The complete retained result records accompany this report.

## Question and model

The practical question is whether a consumer can distinguish an adequately bound informational package from one that omits a required condition, uses evidence for another task, or lacks a current supplied permission. The tested carrier is `kc-synthesis/0.1`. Its nine logical groups represent identity, purpose, content, scope, grounds, dependencies, obligations, projection, and observations. Optional versioned profiles add professional work, dialogue, documents, reasoning, visual delivery, and reuse.

A profile extends the obligations of the core. It does not override them by appearing later in a file. If admission requires the core condition \(C_0\) and applicable profile conditions \(C_1,\ldots,C_n\), then

\[
\operatorname{Admit}(x) \Rightarrow \bigwedge_{i=0}^{n} C_i(x)
\Rightarrow C_0(x).
\]

This implication follows from the admission definition. Whether software implements that definition correctly is a separate question. Whether an external annotation is true is another. The [conditional-properties record](evidence/conditional-properties-source.json) states these distinctions and supplies counterexamples. Their theoretical setting is developed in [Evidence and falsification](../../../papers/evidence-and-falsification/PAPER.md) and [Constrained transformations](../../../papers/constrained-transformations/PAPER.md).

The implementation assumes that objects and relationships have already been interpreted. A supplied capability annotation, source availability, and a current authority decision are inputs. The checker does not independently interview an actor, authenticate an external grant, or establish a source's factual accuracy. An informational contract may omit the professional profile; an execution request has additional binding requirements. Unknown required profiles block use. Unknown optional profiles can be retained as opaque data with a diagnostic, which does not count as interpreting them.

## Design and unit of observation

The [evaluation protocol](evidence/evaluation-protocol-source.json) distinguishes a scenario from assertions nested inside it. The author prepared the interface and its own suite. A different agent in the same session prepared control intents before inspecting the implementation. After receiving the interface, that agent fixed concrete cases, expected outcomes, and a runner before its first import of the validator implementation. The retained [control review](evidence/control-review-source.json) describes this sequence.

There were 28 initial control intents: 24 ordinary and four trust-boundary stress intents. Interface mapping produced 26 ordinary concrete scenarios and four stress scenarios. The 26 comprise six expected positive outcomes, seventeen expected rejections, and three migration-preservation cases. Only four of the six positive outcomes are application admissions. One intent could not be mapped and five were only partially represented. These omissions remain part of the scope assessment; they are not additional passed cases.

| Operation in the retained control report | Ordinary cases | Expected positive outcomes | Expected rejections | Preservation-only cases |
| --- | ---: | ---: | ---: | ---: |
| Application assessment | 13 | 4 | 9 | 0 |
| Execution verification | 6 | 1 | 5 | 0 |
| Profile compatibility | 2 | 1 | 1 | 0 |
| Contract validation | 2 | 0 | 2 | 0 |
| Legacy migration | 3 | 0 | 0 | 3 |
| Total | 26 | 6 | 17 | 3 |

These are different predicates: a valid schema, an accepted execution, a compatible profile and permission for an application are not interchangeable decisions. The table is recomputed from the report's `operation` and expected-check fields. The four application positives are C01, C02, C06B and C18; C02B concerns execution, and C12 concerns compatibility.

The control composition is organizational separation within one session and agent family. It is not an external replication or independent domain review. Cases were deliberately selected to exercise mechanisms, so their proportions do not estimate error rates in a population of real tasks.

## Results

| Evaluation | Ordinary expected outcomes matched | False trusted inputs accepted | Meaning of the result |
| --- | ---: | ---: | --- |
| Author development fixtures | 35/35: 13 expected positives, 22 expected rejections | 2/2 | Regression evidence; separately disclosed trust-boundary stress |
| Separate control suite | 26/26 | 4/4 | Exact outcomes on the frozen concrete control cases |
| Strong plain-form comparison | 9/9 for each representation | Outside this comparison | Equal decisions on three allowed and six forbidden admissions |

These counts come from the exact [author report](evidence/author-conformance-report.json), [control report](evidence/separate-control-report.json), and [strong-comparator report](evidence/strong-plain-form-comparison.json). The reports retain input hashes, case rows, expected outcomes, and observations. Their bytes were recovered from the retained publication reader and checked against its source index; [origin.json](evidence/origin.json) records the identities and hashes.

Positive controls matter. A checker that rejects every input would avoid forbidden admissions but fail useful cases. The six positive control outcomes include a compact informational core, correctly bound work, exact synthetic execution evidence, a current grant despite a different revoked grant, an opaque optional profile, and an eligible reuse instance. Negative cases include missing capability, a mismatched or expired grant, changed requirements, absent declared imagery, unknown required profiles, lost conditions, and evidence bound to another attempt or output.

The migration cases concern a declared six-field legacy subset. They check retained original values, explicit gaps, and the absence of invented capability or authority. They do not demonstrate lossless migration of every previous contract implementation.

## Counterexamples and the comparator

The control stress cases deliberately supplied four internally consistent falsehoods: a positive capability annotation, a fabricated grant, false subject content, and an incorrect claim that a source was available. All four were admitted. This is a counterexample to the proposition that passing structural and binding checks establishes real competence, authorization, factual truth, or production access enforcement. It is not a successful semantic test merely because the interface's expected answer was acceptance.

Two comparators must also remain distinct. The initially registered diagnostic ablation checked field presence and simple form but omitted the cross-object conditions under investigation. It admitted all nine shared inputs, including all six forbidden ones; it therefore matched only the three expected positives, whereas the contract matched all nine. Its separate calibration rejected an empty task, but that input is outside the shared nine-case denominator. This establishes the effect of removing relational checks in that code. It is not a fair estimate of an advantage over a strong task form.

The subsequent strong checker received the same material information and directly checked current sources, work and requirements revisions, actor assignment, conditions, grants, and required capabilities. It used fixed fields rather than an extensible ontology and profile registry. It matched all nine expected outcomes, exactly as the stored contract run did. The comparator author knew the nine inputs and their expected outcomes from the first results. Equality is therefore an existence demonstration that a direct checker can encode these obligations, not a held-out test of generalization. Only the comparator was newly executed in this comparison; the contract side used its preserved first result. A later comparative evaluation needs unseen cases for both implementations.

The equality directly challenges a claim that the larger representation is necessary for these nine decisions. It leaves open different questions about exchange, maintenance, additional profiles, preparation effort, and scale. None of those outcomes was measured here.

## Claim, test, counterexample, and limit

| Claim | Model or test | Counterexample or rival explanation | Supported conclusion and limit |
| --- | --- | --- | --- |
| Profile composition preserves core obligations | Conjunctive admission and required-profile cases | An implementation silently overrides a core condition | The defined rule preserves the core; the finite suite checks selected implementations of it |
| Evidence must refer to the attempted work | Exact task, requirements, actor, attempt, output, and criterion bindings | Old evidence has a similar description but a different target | Tested mismatches are rejected; forged trusted bindings remain outside authentication |
| A skill description establishes capability | Separate description and capability inputs | A false capability annotation is accepted | The description alone is insufficient; input truth still needs an external basis |
| Contract conformance implies source truth | Schema and consistency checks | The admitted false-source stress case | This implication is refuted within the test design |
| The contract outperforms a strong simple form | Nine shared decisions | The direct checker makes the same decisions | No advantage is established on this shared domain |

## Reproduction and evidence boundaries

The accompanying files are sufficient to inspect all recorded results, separate the stress denominator, inspect the comparator decisions, and verify the provenance of retained JSON. The exact original runners, the thirty concrete control inputs and their oracle, the strong comparator code, and the frozen implementation are not included. This is an unresolved recovery and publication gap for project-authored synthetic material, not a third-party-book rights restriction. The locally available later implementation has a different hash from the one bound to this report and cannot substitute for it. Consequently this folder supplies inspectable retained reports rather than a complete historical rerun. Hashes identify artifacts; they do not replace missing code, authenticate an observer, or certify a result's meaning. The [recovery inventory](../historical-recovery-gaps.json) lists the exact missing identities and the evidence used to identify them.

The review did recover the exact [historical `kc-synthesis/0.1` schema](historical-recovery/contract-synthesis-0.1.schema.json), whose SHA-256 agrees with the author report. It is published separately, without changing the retained evidence inventory. Recovering this one input does not recover the missing implementation, concrete fixtures or runners and does not imply conformance to the current architecture.

Rendered prose sources are explicitly identified as text views recovered from the retained HTML. Their original Markdown source hashes are recorded separately from the hashes of those new views. They are not misrepresented as byte-identical Markdown reconstructions.

The retained conditional-properties, protocol and review narratives are in Russian; JSON keys are mainly English, with some Russian descriptions. The model, design and boundary paragraphs above are English summaries of the cited passages, including the same-session review scope and unmapped controls. They are summaries, not a certified translation of every source line. The [evidence language index](../evidence-language-index.json) identifies the language and preserved hash of each distributed file.

## Conclusion

The tested profile performed its declared finite structural and relational checks, including useful positive controls and prohibited admissions. The accepted false trusted inputs demonstrate why source admission, current authority, and semantic assessment need their own evidence. The strong-comparator tie further narrows the contribution: this study supplies a working representation and inspectable finite results, while leaving comparative practical benefit unestablished. These distinctions are prerequisites for a usable contract service, not unfinished text that should be concealed by an undifferentiated success label. Terminology is consolidated in the [glossary](../../../reference/glossary/GLOSSARY.md).

---
name: "editorial-skill-pilot"
title: "Editing a scientific section with a knowledge toolkit: a masked single-section comparison"
artifact: "engineering-study"
edition: "1.0"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "One preregistered editorial comparison, exact initial outputs, masked review and an observed tie."
study_type: "paired-editorial-process-pilot"
review_state: "internally-reviewed"
---

# Editing a scientific section with a knowledge toolkit: a masked single-section comparison

## Abstract

Two agents edited the same 804-word Russian scientific section under a common brief. One used the general brief alone; the other used an editorial toolkit containing task-specific skills and a process blueprint. Before the responses, the experiment fixed nineteen protected claims, eight conceptual distinctions, exact literals, source material, and a five-axis rubric. A separate agent reviewed anonymized outputs before their conditions were revealed. Both preserved the declared claims and distinctions, passed the editorial acceptance gate, and received eight points out of ten. The preference was a tie. A separate technical audit found a consistent trace linking the toolkit-assisted changes to declared rules and source ranges. The pilot therefore demonstrates an operational editing and traceability process on one real section. It does not demonstrate better writing than a strong common brief, isolate a causal effect of individual skills, or validate the scientific theory being edited.

## Question and scope

The user's practical question was whether newly created writing skills and a blueprint could guide an agent through a real publication task while preserving meaning. The selected unit was the complete working-definitions section of the project introduction: 804 words by whitespace counting, four subsections, and a table with eight distinctions. The input was Russian, so this pilot does not evaluate English translation quality. The toolkit was derived from Maxim Ilyakhov and Lyudmila Sarycheva’s *Пиши, сокращай*; the [bibliographic and input-identity note](../../../reference/bibliography/BIBLIOGRAPHY.md#editorial-input) identifies the work and the supplied representation without redistributing it.

The trial separated editorial quality from truth of the underlying scientific content. An editor could improve references, paragraph structure, and sentence clarity without establishing the correctness of a formal claim. The relevant scientific framing appears in [Constrained transformations](../../../papers/constrained-transformations/PAPER.md), [Evidence and falsification](../../../papers/evidence-and-falsification/PAPER.md), and [Knowledge utility](../../../papers/knowledge-utility/PAPER.md).

The exact [source section](evidence/source-section.txt), [shared context](evidence/source-context.txt), [common brief](evidence/common-editorial-brief.txt), and [original protocol](evidence/original-pilot-protocol.txt) are retained as historical text records. Their internal paths and terminology describe the original experiment; the present publication's navigation is provided by this report.

## Design and preregistration

The [preregistration](evidence/editorial-preregistration.json) predates the editor agents. It pins the inputs, identifies two conditions, permits one first completed response per condition, and specifies review with condition labels hidden until the written evaluation. The [protected-claim registry](evidence/protected-claims.json) contains nineteen claims, protected headings and anchors, link targets, numbers, versions, and 37 exact literals.

Both agents received the same input and brief in fresh task contexts. The baseline condition edited without reading the toolkit. The assisted condition used the readable-layout editorial package, five declared applied skills, and the process blueprint for editing existing text. The general brief already required meaning preservation, so the baseline was a substantive editorial alternative rather than an instruction to shorten text indiscriminately.

After the first responses were saved, another agent received the source and variants labeled alpha and beta without the editing logs or condition mapping. It issued the [masked review](evidence/masked-editorial-review.json). The subsequent [label reveal](evidence/condition-label-reveal.json) records alpha as baseline and beta as toolkit-assisted and states that review was completed before reveal. This is masking of condition labels, not proof that the reviewer could not infer a method from stylistic differences. All roles operated within the same agent environment; there was no independent human editorial panel.

## Results on the first completed responses

| Observation | Common-brief baseline | Toolkit-assisted editing |
| --- | ---: | ---: |
| Protected claims preserved | 19/19 | 19/19 |
| Conceptual table distinctions preserved | 8/8 | 8/8 |
| Exact protected literals present | 37/37 | 37/37 |
| Headings / anchors / link destinations | 5 / 5 / 3 | 5 / 5 / 3 |
| Sentence clarity, 0–2 | 2 | 2 |
| References and terminology, 0–2 | 2 | 2 |
| Coherence, 0–2 | 2 | 2 |
| Economy without loss, 0–2 | 1 | 1 |
| Scientific genre and reader, 0–2 | 1 | 1 |
| Total assigned by the reviewer | 8/10 | 8/10 |
| Words by whitespace | 830 | 820 |
| Editorial decision | Accepted within the declared scope | Accepted within the declared scope |

The [comparison result](evidence/editorial-comparison-results.json), exact [baseline response](evidence/baseline-edit.txt), and exact [assisted response](evidence/skill-assisted-edit.txt) accompany the report. The original [mechanical check](evidence/editorial-mechanical-checks.json) verifies hashes, literal presence, and document structure. The semantic preservation counts and stylistic scores come from the recorded agent review, not the mechanical checker.

Both responses were slightly longer than the original. Reduction in word count was not the declared target. Replacing compressed references with explicit nouns can increase length while reducing the reader's effort to reconstruct a reference. Consequently this trial supplies no general rule that successful editing must make a text shorter.

## What the edits changed

The assisted response made some list references explicit. Instead of asking the reader to connect the first, second, and third items to an earlier list, it named source context, interaction context, and application context directly. It also replaced a vague plural referent with the already defined object being described. These changes clarified existing relationships without adding another theoretical claim.

The section discussing a contract was divided into thematic paragraphs addressing the contract and package, version history, work objects, and the boundary of the research. Some technically dense material was preserved because its distinctions were protected. The masked reviewer identified local strengths in both variants rather than a consistent overall advantage. A repeated list remained in the baseline; a long contract definition remained in the assisted version. Neither was repaired after comparison to manufacture a better first-response result.

## Skill use and technical trace

The assisted route went through a brief, request, compiled Knowledge Contract, proposed edit, review, and registration. Five skills were declared applied: defining the editing task, precise rewording, preserving numbers and conditions, structuring sentences and paragraphs, and reviewing the result with its source trace. Required dependencies caused twelve skills and 108 records to be delivered. The other seven skills were not counted as applied merely because they were loaded.

The separate [technical audit](evidence/editorial-trace-audit.json) records twelve groups of material changes, twenty change grounds, and seven process grounds. It checked 49 unique input/output locators and 24 unique source ranges. Quotes, character and UTF-8 offsets, and line bindings matched, and all changed non-whitespace characters were covered by the recorded trace. It also checked agreement among request, input, contract, selected context, output, assessment, and receipt bindings.

These observations establish consistency and inspectability of the particular trace. They do not reveal every internal action of the editor or prove that a cited rule caused a wording choice. The source ranges included private third-party material and are not redistributed as excerpts in this publication. The published audit is the project's report of those checks, with a pinned source identity; it is not a replacement for independent access to the underlying book.

## Counterarguments and boundaries

The main rival explanation is that a sufficiently good common brief already supplied what this section needed. The observed tie is consistent with that explanation. It does not prove that the toolkit is useless on other tasks, but it prevents this pilot from being cited as evidence of superiority.

A second counterargument is that a complete-looking trace may accompany an incorrect edit. Mechanical equality, literal presence, and a consistent receipt do not establish meaning preservation. The [package-delivery study](../dependency-closure-and-package-delivery/STUDY.md) supplies an explicit negative example in which the protected numeric string remains while the sentence's meaning is negated. The editorial review addresses that distinct question here, within one section and one reviewer's judgment.

A third boundary concerns terminology. At the time of the pilot, the editors recorded an ambiguity between two spellings of the work-item entity rather than silently deciding that they denoted different things. The author subsequently clarified that the spellings refer to one entity. The present [glossary](../../../reference/glossary/GLOSSARY.md) uses that decision. Frozen pilot inputs and scores retain their historical bytes; they are not retroactively rewritten as if the clarification preceded the experiment.

There was one section and one first completed response per condition. Scores are qualitative rubric judgments, not calibrated population measurements. The trial did not record token usage, cost, or latency. It did not isolate the contribution of each skill, the blueprint, or the surrounding compiler. Native command-line clients were not used. The underlying scientific claims and all referenced literature were not revalidated by this editorial exercise.

## Public record checks

The supplied [replay checker](evidence/replay_editorial_checks.py) rechecks the public retained texts against the frozen source hash, original response hashes, exact literals, headings, anchor order, and link destinations:

```bash
python3 evidence/replay_editorial_checks.py
```

The [saved check](evidence/public-editorial-record-check.json) confirms those mechanical properties. It deliberately does not compute semantic fidelity or reproduce the eight-point ratings. Complete model-runtime identity and the full private toolkit source closure are not supplied, so executing this checker is not a new agent trial. [origin.json](evidence/origin.json) pins the distributed records and distinguishes original data from newly generated check results.

## Conclusion

The assisted editorial process worked on the selected real section: it produced an accepted text and an inspectable chain from task to changes and review. The baseline also worked, with the same protected-claim result and score. This completed pilot supports a narrow operational claim about usable process and traceability. A claim of better writing, lower cost, or improved scientific correctness requires a different and adequately observed comparison. The present result remains valuable without changing the tie into an advantage.

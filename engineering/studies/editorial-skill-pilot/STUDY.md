---
name: "editorial-skill-pilot"
title: "Editorial Pilot: Editing a scientific section with a knowledge toolkit: a masked single-section comparison"
short_title: "Editorial Pilot"
subtitle: "Editing a scientific section with a knowledge toolkit: a masked single-section comparison"
previous_title: "Editing a scientific section with a knowledge toolkit: a masked single-section comparison"
artifact: "engineering-study"
edition: "1.1"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "One preregistered editorial comparison, exact initial outputs, masked review and an observed tie."
study_type: "paired-editorial-process-pilot"
review_state: "internally-reviewed"
---

<!-- markdownlint-disable-next-line MD033 -->
<a id="editing-a-scientific-section-with-a-knowledge-toolkit-a-masked-single-section-comparison"></a>

# Editorial Pilot: Editing a scientific section with a knowledge toolkit: a masked single-section comparison

## Abstract

Two agents edited the same 804-word Russian scientific section. Both received the common brief, shared context, source section, protected-claim registry and scoring rubric. The assisted condition additionally used an editorial toolkit containing skills and a process blueprint. The shared checklist contained nineteen protected claims, including eight conceptual distinctions, and exact literals. A separate agent reviewed anonymized outputs before their conditions were revealed. Both complied with the supplied claim checklist, passed the editorial acceptance gate, and received eight points out of ten; preference was a tie. A technical audit found a mechanically consistent trace from assisted changes to declared rules and source ranges, with limitations in how specifically some rules supported the edit. The pilot demonstrates an operational editing and traceability process on one real section. It does not establish unaided meaning preservation, better writing than the shared structured brief, a causal effect of individual skills, or scientific validity of the text.

## Question and scope

The user's practical question was whether newly created writing skills and a blueprint could guide an agent through a real publication task while preserving meaning. The selected unit was the complete working-definitions section of the project introduction: 804 words by whitespace counting, four subsections, and a table with eight distinctions. The input was Russian, so this pilot does not evaluate English translation quality. The toolkit was derived from Maxim Ilyakhov and Lyudmila Sarycheva’s *Пиши, сокращай*; the [bibliographic and input-identity note](../../../reference/bibliography/BIBLIOGRAPHY.md#editorial-input) identifies the work and the supplied representation without redistributing it.

The trial separated editorial quality from truth of the underlying scientific content. An editor could improve references, paragraph structure, and sentence clarity without establishing the correctness of a formal claim. The relevant scientific framing appears in [Constrained transformations](../../../papers/constrained-transformations/PAPER.md), [Evidence and falsification](../../../papers/evidence-and-falsification/PAPER.md), and [Knowledge utility](../../../papers/knowledge-utility/PAPER.md).

The exact [source section](evidence/source-section.txt), [shared context](evidence/source-context.txt), [common brief](evidence/common-editorial-brief.txt), and [original protocol](evidence/original-pilot-protocol.txt) are retained as historical text records. Their internal paths and terminology describe the original experiment; the present publication's navigation is provided by this report.

## Design and preregistration

The [preregistration](evidence/editorial-preregistration.json) predates the editor agents. It pins the inputs, identifies two conditions, specifies one first completed response per condition, and requires review with condition labels hidden until the written evaluation. The [protected-claim registry](evidence/protected-claims.json) contains nineteen claims, protected headings and anchors, link targets, numbers, versions, and 37 exact literals. First-response status is the editor's declaration: the final bytes are hash-pinned, but no independent complete event log verifies that status, rereading before registration, or the absence of edits after self-review.

Both agents received the exact section, common brief, shared context and protected-claim registry in fresh task contexts. The brief disclosed the full scoring procedure, including five axes and the meanings of scores 0, 1 and 2. The baseline edited without reading the toolkit; the assisted condition additionally used the readable-layout package, five declared applied skills, and the process blueprint for editing existing text. The registry itself is a structured statement of obligations. The comparison therefore isolates the added toolkit and compiler route relative to a common structured brief, not a brief-only condition against a contract. Preservation counts measure compliance with a supplied checklist rather than discovery or unaided preservation of unstated meaning.

After the first responses were saved, another agent received the source and variants labeled alpha and beta without the editing logs or condition mapping. It issued the [masked review](evidence/masked-editorial-review.json). The subsequent [label reveal](evidence/condition-label-reveal.json) records alpha as baseline and beta as toolkit-assisted and states that review was completed before reveal. This is masking of condition labels, not proof that the reviewer could not infer a method from stylistic differences. All roles operated within the same agent environment; there was no independent human editorial panel.

## Results on the retained responses

| Observation | Common-brief baseline | Toolkit-assisted editing |
| --- | ---: | ---: |
| Protected claims preserved | 19/19 | 19/19 |
| Conceptual table distinctions preserved, nested within protected claim 11 | 8/8 | 8/8 |
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

The eight distinctions are included in the nineteen claims, not eight additional independent obligations. Both score vectors were `(2, 2, 2, 1, 1)`: the first three axes were at their ceiling, and the 0–2 scale was coarse. A difference smaller than one score step on an axis would not be resolved by this instrument. Equality of totals is a result under this rubric, not evidence of identical writing quality.

The review used identical `gate_reasoning` text for both variants, so that paragraph is templated reasoning rather than two independently developed arguments. The record also contains three examined issues per variant. Their English summaries are:

| Variant and issue | What the reviewer examined | Recorded disposition |
| --- | --- | --- |
| Baseline: ALPHA-STYLE-01 | A list of four distinctions is repeated when each is explained | Non-blocking redundancy; reflected in the economy score |
| Baseline: ALPHA-WORDING-01 | A phrase about non-identity became a phrase about lack of implication | Accepted within the supplied checklist's local meaning; no new formal precision claimed |
| Baseline: ALPHA-SOURCE-01 | Both historical Work Item spellings remain | Inherited ambiguity, not charged as a new defect |
| Assisted: BETA-SCOPE-01 | The working-profile qualifier moved before role, skill and blueprint together | No protected claim of unconditional scope was identified; no loss established within the brief |
| Assisted: BETA-STYLE-01 | A dense contract definition remains long | Non-blocking retained limitation |
| Assisted: BETA-SOURCE-01 | Both historical Work Item spellings remain | Inherited ambiguity, not charged as a new defect |

These dispositions expose the local judgment behind “preserved”; they do not settle a broader scientific interpretation that the checklist did not specify.

Both responses were slightly longer than the original. Reduction in word count was not the declared target. Replacing compressed references with explicit nouns can increase length while reducing the reader's effort to reconstruct a reference. Consequently this trial supplies no general rule that successful editing must make a text shorter.

## What the edits changed

The assisted response made some list references explicit. Instead of asking the reader to connect the first, second, and third items to an earlier list, it named source context, interaction context, and application context directly. It also replaced a vague plural referent with the already defined object being described. These changes clarified existing relationships without adding another theoretical claim.

The section discussing a contract was divided into thematic paragraphs addressing the contract and package, version history, work objects, and the boundary of the research. Some technically dense material was preserved because its distinctions were protected. The masked reviewer identified local strengths in both variants rather than a consistent overall advantage. A repeated list remained in the baseline; a long contract definition remained in the assisted version. Neither was repaired after comparison to manufacture a better first-response result.

## Skill use and technical trace

The assisted route went through a brief, request, compiled Knowledge Contract, proposed edit, review, and registration. Five skills were declared applied: defining the editing task, precise rewording, preserving numbers and conditions, structuring sentences and paragraphs, and reviewing the result with its source trace. Required dependencies caused twelve skills and 108 records to be delivered. The other seven skills were not counted as applied merely because they were loaded.

The separate [technical audit](evidence/editorial-trace-audit.json) records twelve groups of material changes, twenty change grounds, and seven process grounds. It checked 49 unique input/output locators and 24 unique source ranges. Quotes, character and UTF-8 offsets, and line bindings matched, and all changed non-whitespace characters were covered by the recorded trace. It also checked agreement among request, input, contract, selected context, output, assessment, and receipt bindings. The audit read fifteen source fragments covering nine cited rules. For the precision rule K10, making pronoun references explicit was an editorial application of a general principle, not a separately stated method in the book. The trace is mechanically consistent, while some changes have only general rule support. No visual PDF verification occurred, and the source OCR questions K02/F02 and K03/F03 remained open.

These observations establish consistency and inspectability of the particular trace. They do not reveal every internal action of the editor or prove that a cited rule caused a wording choice. The edited scientific section is the project's own text and is distributed here in full. The private third-party source is the writing guide underlying the toolkit's rules; its cited ranges and the private source-derived toolkit are not redistributed. The published audit reports those rule-source checks with a pinned source identity, rather than supplying the guide itself.

## Counterarguments and boundaries

One rival explanation is that the common brief, context, explicit checklist and disclosed rubric already supplied what this section needed. Another is that the baseline model may already have known the general editing method or similar principles through prior training; the experiment did not measure or exclude such exposure. The original protocol expressly avoided assuming that the model lacked general editing knowledge. Both explanations are compatible with the observed tie. A useful subsequent test would include project-specific rules unavailable in the common brief, a held-out task set, and a more discriminating or pairwise-preference assessment. The present result does not prove that the toolkit is useless, but cannot support a superiority claim.

A second counterargument is that a complete-looking trace may accompany an incorrect edit. Mechanical equality, literal presence, and a consistent receipt do not establish meaning preservation. The [package-delivery study](../dependency-closure-and-package-delivery/STUDY.md) supplies an explicit negative example in which the protected numeric string remains while the sentence's meaning is negated. The editorial review addresses that distinct question here, within one section and one reviewer's judgment.

A third boundary concerns terminology. At the time of the pilot, the editors recorded an ambiguity between two spellings of the work-item entity rather than silently deciding that they denoted different things. The author subsequently clarified that the spellings refer to one entity. The present [glossary](../../../reference/glossary/GLOSSARY.md) uses that decision. Frozen pilot inputs and scores retain their historical bytes; they are not retroactively rewritten as if the clarification preceded the experiment.

There was one section and one retained response per condition, each declared first-completed by its editor. Scores are qualitative rubric judgments, not calibrated population measurements. The trial did not record token usage, cost, or latency. It did not isolate the contribution of each skill, the blueprint, or the surrounding compiler. Native command-line clients were not used. The underlying scientific claims and all referenced literature were not revalidated by this editorial exercise. The methodological distinctions between preregistered and post-hoc work, and between masked labels and a validated judge, are discussed in the [methodological references](../../../reference/bibliography/BIBLIOGRAPHY.md#evaluation-methods).

## Public record checks

The supplied [replay checker](evidence/replay_editorial_checks.py) rechecks the public retained texts against the frozen source hash, original response hashes, exact literals, headings, anchor order, and link destinations:

```bash
python3 evidence/replay_editorial_checks.py
```

The [saved check](evidence/public-editorial-record-check.json) confirms those mechanical properties. It deliberately does not compute semantic fidelity or reproduce the eight-point ratings. Complete model-runtime identity and the full private toolkit source closure are not supplied, so executing this checker is not a new agent trial. [origin.json](evidence/origin.json) pins the distributed records and distinguishes original data from newly generated check results.

The source section, context, brief, protocol, edits and substantive review prose are Russian; JSON field names are mainly English. The descriptions of the two conditions, the six examined issues and the audit qualifications above are English summaries of the cited Russian passages, not a full independently reviewed translation. The [evidence language index](../evidence-language-index.json) identifies every file without rewriting its frozen bytes.

## Conclusion

The assisted editorial process worked on the selected real section: it produced an accepted text and an inspectable chain from task to changes and review. The baseline also worked, with the same protected-claim result and score. This completed pilot supports a narrow operational claim about usable process and traceability. A claim of better writing, lower cost, or improved scientific correctness requires a different and adequately observed comparison. The present result remains valuable without changing the tie into an advantage.

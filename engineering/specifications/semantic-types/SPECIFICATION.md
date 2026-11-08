---
name: "semantic-types"
title: "Semantic Types: Attribution, and Representations"
short_title: "Semantic Types"
subtitle: "Attribution, and Representations"
previous_title: "Semantic Types, Attribution, and Representations"
artifact: "engineering-specification"
edition: "1.1"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "Semantic facets, attribution, scoped operators, ambiguous readings and multimodal representations."
---

<!-- markdownlint-disable-next-line MD033 -->
<a id="semantic-types-attribution-and-representations"></a>

# Semantic Types: Attribution, and Representations

**Author:** Pavel Valentov · **Publication edition:** 1.1

## 1. Purpose and conformance

This is an architectural requirement set. Interoperability requires a named representation profile; the implemented exchange subset is limited to [observations, change events and profile advertisements](../status-model/SPECIFICATION.md#8-bounded-exchange-profile), and the [book-package profile](../book-package/SPECIFICATION.md) has its own schema. No full-contract wire format or deployed runtime is implied.

**SEM-R001.** This specification defines the distinctions an implementation MUST preserve when interpreting and representing knowledge.

Its facets organize content without claiming an exhaustive taxonomy of all human meaning. A procedure, a quoted procedure, and a deliberately incorrect procedural example may use similar words but support different uses.

Capitalized requirements use [BCP 14](../../../reference/bibliography/BIBLIOGRAPHY.md#requirement-language).

**SEM-R002.** A conforming profile MUST state its vocabulary, cardinalities and representation mapping.

The [scientific model](../../../papers/semantic-objects-and-context/PAPER.md) defines the separation between a source representation, interpretation, grounds and applicability.

## 2. Independent semantic dimensions

| Dimension | Information to retain |
| --- | --- |
| Representation | Text, image, audio, video, structured data or an explicit combination |
| Content kind | Definition, observation, description, model, procedure, structure, constraint, goal, argument, question or another declared kind |
| Discourse function | Explanation, instruction, quotation, illustration, counterexample, question or another contextual role |
| Aboutness | The entities, concepts or domains to which the content refers |
| Attribution | Who authored, reported, interpreted or assessed the addressed content |
| Source position | Whether a source asserts, hypothesizes, denies, asks or reports another position |
| Operators | Negation, quantification, modality, condition, exception, order and their exact scopes |
| Assessments | References to observations about fidelity, support or another stated property |
| Governance | Adoption and authority records, where relevant to the intended use |
| Applicability | Domain, time, recipient and other conditions under which the content may be used |

**SEM-R003.** A profile MAY store several dimensions in one structured record, but MUST NOT conflate their meanings.

A source position is not a truth value. An author's approval of a method is not current permission for a recipient to perform it. A generated image description is not the source image.

**SEM-R004.** For each required facet, the profile MUST distinguish known value, unknown value, justified not applicable, and withheld value.

Unknown is not an empty known list.

**SEM-R005.** Withheld indicates a disclosure boundary and MUST NOT be represented as evidence that no value exists.

## 3. Identity, granularity and relations

One source region can support several semantic objects; one semantic object can require several source regions.

**SEM-R006.** Extraction boundaries MUST follow the obligations of the intended interpretation.

A condition in a heading, a table unit or a diagram legend can be mandatory even if it falls outside a retrieved chunk.

**SEM-R007.** Source identity, semantic object identity, representation identity and retrieval chunk identity MUST remain distinguishable.

Rechunking an index need not change the interpreted semantic object. Correcting an interpretation does require a new semantic revision. A different rendering can preserve a semantic revision only when the claimed equivalence has a stated basis.

**SEM-R008.** Relations MUST identify their endpoints and kind.

A navigation link suggests further reading; a mandatory dependency says that a declared use requires the linked information.

**SEM-R009.** A vague association MUST NOT be silently upgraded to a proof premise, causal link or authority relation.

## 4. Scope and ambiguity

**SEM-R010.** Operators MUST bind to their actual scope.

“Not all members satisfy P” cannot be rewritten as “all members do not satisfy P.” An absence of permission is not an explicit prohibition, although either may prevent a particular action under its policy. A reported hypothesis is not an accepted conclusion.

**SEM-R011.** When several interpretations remain possible, an implementation MUST retain the alternatives or mark the interpretation unresolved.

Choosing one is permitted only with a recorded basis and a declaration of remaining uncertainty. A confidence score alone does not explain which interpretation was chosen or which distinction could change the answer.

## 5. Multimodal content and delivery

**SEM-R012.** A media reference MUST identify the representation revision and selector semantics.

**SEM-R013.** Required legends, ordering, coordinate conventions, units and joint components MUST be retained.

Delivery of a textual substitute is sufficient only when the task's protected observations can be established from that substitute.

OCR, a model-generated description, a human transcription and an original visual are separately attributable derivatives.

**SEM-R014.** A profile MUST record which was inspected.

Claims about transcription fidelity require a comparison method and a reference; merely preserving all generated descriptions does not measure their accuracy.

## 6. Validation obligations

**SEM-R015.** The conformance suite MUST include an attributed false assertion, a scoped negation, a quotation inside another quotation, a counterexample with tempting instructional wording, an unresolved alternative reading, and a required media dependency omitted from delivery.

The expected behavior is preservation or explicit refusal; fluent reconstruction is not a substitute for those checks.

Structural validation can check facet presence, vocabulary and references. It does not establish that the extractor found every relevant condition. Semantic fidelity therefore requires content-specific assessment and a stated inspection method.

## 7. Evidence and interoperability

The [transcription and uncertainty study](../../studies/source-transcription-and-uncertainty/STUDY.md) reports how generated descriptions and uncertainty were retained in readable projections. It explicitly separates that result from unmeasured OCR or interpretation accuracy. Domain examples belong to that engineering study.

[SKOS](../../../reference/bibliography/BIBLIOGRAPHY.md#skos) provides useful concepts, labels and relations; [PROV-DM](../../../reference/bibliography/BIBLIOGRAPHY.md#provenance) supplies provenance distinctions. This profile does not claim to replace either standard or to make their graphs prove content truth.

**SEM-R016.** Vocabulary mappings MUST state whether they are exact, broader, narrower or merely related.

See the [glossary](../../../reference/glossary/GLOSSARY.md) for the project's preferred terms.

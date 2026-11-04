---
artifact_id: KC3_ADJUDICATION_PROTOCOL
revision_id: KC3_ADJUDICATION_PROTOCOL-r1
title_en: "Adjudication protocol for reference answers and anchored lines"
language: en
status: protocol; no adjudication has been done
license: CC-BY-4.0
sources: none
---

# Adjudication protocol for reference answers and anchored lines

This protocol governs gate G-REF (the 21 knowledge questions) and gate G-L70 (the 70 short source-anchored lines) of the [pre-registration](KC3_PREREGISTRATION.md). It is written before any adjudication. The adjudicator is an agent that is not the author of this repository's package builder and not the converter's author, preferably of another model family, and works blind to every system answer.

## Inputs and blindness

The adjudicator receives the source representation (original bytes, hash-checked), the question or the line locator, and this protocol. It does not receive package objects, system answers, retrieval results or earlier adjudications of the same item by anyone else. Its session and model are recorded.

## Reference classes

- **Gold**: the adjudicator located the supporting span in the original source, read it in the original rendering (page image for page formats), and the answer or the line text is fully supported by that span. For a line, the text was read from the rendered page, not copied from a text layer.
- **Silver**: the answer or line is supported but one condition for gold failed, for example the span was read from a text layer only, or the language was read with a lookup. The failed condition is named.
- **Abstain**: the source does not contain the answer, the span cannot be located, or the rendering is unreadable for the adjudicator. Abstention is a result, not a failure; an abstained question becomes a negative case only if the source was surveyed completely within a stated scope, otherwise it stays `unknown`.

## Per item record

Item id, source representation id and hash, class (gold, silver, abstain), the span as an anchor of the kinds in the book package specification, the reference answer or line, the conditions the answer depends on, the reason for any downgrade, and the adjudicator session. A reference answer quotes at most 25 words of a source that is not openly licensed.

## Rules

1. A question whose draft wording presumes an answer the source does not give is refined to the source's actual topic before adjudication; the refinement is recorded with both texts.
2. Numbers, units, signs, negations and code are copied exactly. A reference answer that differs from the source in any of them is invalid.
3. Cross-language pairs (a question and its paraphrase in another language) are adjudicated separately and must point to the same evidence scope.
4. Every reference is frozen in a commit before any retrieval or package run. A later correction is a new revision with a note on what it affects; the earlier revision stays.

## Disagreements

A second adjudicator (another session, ideally another model family) reads a sample of 20 percent of items, at least 10, chosen by a recorded seed. An item where the two disagree on class, answer or span is set to abstain unless a recorded discussion round resolves it from the source alone. The disagreement rate is reported with the reference set; if it exceeds 20 percent of the sample, the whole set is `not_measured` for the checks that use it until the protocol or the items are revised.

## What this protocol does not establish

It does not make an agent adjudicator a human expert, it does not prove independence from the system under test beyond the recorded model family, and it does not cover scripts or layouts the adjudicator cannot read.

Credit and licence: Knowledge Contract Arcana, <https://contract.place> (CC BY 4.0). See [ATTRIBUTION.md](../ATTRIBUTION.md).

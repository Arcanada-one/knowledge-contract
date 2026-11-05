---
name: "context-package"
title: "Context Packages: Coverage, Dependencies, and Delivery"
artifact: "engineering-specification"
edition: "1.1"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "Requirements for selected context, coverage, mandatory dependencies, budgets and observed delivery."
---

# Context Packages: Coverage, Dependencies, and Delivery

**Author:** Pavel Valentov · **Publication edition:** 1.1

## 1. Purpose and conformance

This is an architectural requirement set. Interoperability requires a named representation profile; the implemented exchange subset is limited to [observations, change events and profile advertisements](../status-model/SPECIFICATION.md#8-bounded-exchange-profile), and the [book-package profile](../book-package/SPECIFICATION.md) has its own schema. No full-contract wire format or deployed runtime is implied.

A context package is a versioned selection of knowledge, conditions and grounds prepared for one declared use under a resource budget. It allows inspection of what was selected, why it is sufficient or incomplete, which dependencies were included, and what the recipient actually receives.

Capitalized requirements use [BCP 14](../../../reference/bibliography/BIBLIOGRAPHY.md#requirement-language). The package supports an answer, plan or execution stage. It is not itself a grant to act or evidence that the intended result occurred. See [retrieval and context composition](../../../papers/retrieval-and-context-composition/PAPER.md) for the formal distinction between coverage and search completeness.

## 2. Required package description

**CTX-R001.** A conforming package MUST contain or reference its identity and revision; task and requirements revision; purpose and recipient; source and corpus snapshots; selected unit revisions; mandatory dependency closure; slot-level coverage; declared search scope and assurance; applicable constraints; representation and delivery requirements; resource account; and the observations supporting its status.

**CTX-R002.** Each requirement slot MUST identify the subject, quantifier, required conditions and supporting units.

**CTX-R003.** Joint requirements MUST be supported for the same subject and revision.

Evidence for a property of one object and a different property of another cannot satisfy a conjunction about one object.

**CTX-R004.** The package MUST identify omitted requirements and unresolved dependencies.

If a necessary ground is restricted, an authorized summary or substitute requires its own justification. Silently removing the ground while retaining a claim of complete support is prohibited.

## 3. Selection and closure

Selection starts from candidate units and computes the closure of the mandatory relations active for this use. Navigation links do not automatically join the closure. Unknown or missing required endpoints prevent a complete-package claim.

**CTX-R005.** The finite set-theoretic closure exists even with cycles, but a particular executable profile MAY require an acyclic dependency graph.

**CTX-R006.** That restriction MUST be stated and checked.

Rejection of a cycle by such a profile is not a claim that the abstract closure is undefined.

Adding units can introduce new dependencies and costs.

**CTX-R007.** A composer MUST recalculate closure and budget after a change.

**CTX-R008.** It MUST NOT infer that a larger text is always safer or more useful: additional content may conflict, distract, disclose protected information or exceed the recipient's usable capacity.

## 4. Coverage and assurance

Coverage is assessed separately for candidate set, assembled package and final output.

**CTX-R009.** Each report MUST bind to its own stage and subject revision.

A supported candidate set does not make a truncated package supported; a supported package does not prove that an answer used it correctly.

| Coverage value | Meaning within the declared requirements and scope |
| --- | --- |
| supported | Every mandatory slot has the required established support |
| partial | A supported part exists, with named missing or unresolved obligations |
| unsupported | The evaluated scope provides no required support under the chosen procedure |
| conflicted | Material incompatible grounds prevent a single admitted conclusion |
| unknown | The available observations cannot establish the coverage state |

Search assurance is a separate dimension: `candidate_only`, `exhaustive_in_scope`, or `incomplete_procedure`, using the [canonical token definitions](../status-model/SPECIFICATION.md#3-canonical-dimension-vocabularies). A request for two examples may be supported without exhaustive search. A request for all matching objects requires an additional completeness obligation.

**CTX-R010.** An empty top-k result MUST NOT be reported as proof of global absence.

## 5. Budget and projection

**CTX-R011.** The budget MUST account for the actual delivery context: system and task instructions, relevant history, selected material, tool descriptions, anticipated tool results, output allowance and margin where applicable.

A character count is not an exact token measurement.

**CTX-R012.** Estimated and measured quantities MUST be distinguishable and identify the tokenizer or measurement method.

**CTX-R013.** A projection MUST retain protected units, their relations and task-relevant uncertainty.

**CTX-R014.** It MUST identify excluded units and losses.

An output that reconstructs the selected bytes exactly can still be semantically incomplete if selection omitted an exception. Byte equality and task sufficiency therefore require different checks.

**CTX-R015.** When the mandatory closure cannot fit, the composer MUST return a partial result, negotiate an allowed narrower scope, change representation with justified preservation, or refuse.

**CTX-R016.** It MUST NOT silently discard a mandatory condition to meet the limit.

## 6. Delivery and receipt

The manifest describes what should be delivered; a receipt records what was observed at the recipient boundary. A media URL does not establish byte availability, display, legibility or understanding.

**CTX-R017.** The delivery check MUST match the task's representation requirements and the declared reader capabilities.

**CTX-R018.** Any output assessment MUST name the exact delivered package and requirements revision.

An acknowledgement of receipt or comprehension is not a capability assessment, agreement to execute, or authorization.

## 7. Acceptance and evidence

**CTX-R019.** Acceptance cases MUST include an unresolved dependency, cross-object conjunction, missing quantifier coverage, a budget overflow caused by closure, omitted mandatory media, an outdated requirement revision, and a final output that drops a supported condition.

**CTX-R020.** For each, the check MUST distinguish package construction from downstream use.

The [dependency-closure and delivery study](../../studies/dependency-closure-and-package-delivery/STUDY.md) includes an executable finite replay of all 4,096 subsets of the 12 skill roots and 24,576 single-element inclusion relations on a 110-node dependency graph. This verifies the specified graph behavior, not the completeness of dependencies extracted from arbitrary sources. The [projection study](../../studies/executable-projections-and-revision/STUDY.md) examines downstream representations and reports the limits of measured minimality.

## 8. Compatibility

Legacy coverage fields can be imported only with their subject and semantics. Missing source snapshots, budget measurements or delivery observations remain unknown. A new document edition does not retrospectively upgrade earlier illustrative examples into executed packages. Terms are defined in the [glossary](../../../reference/glossary/GLOSSARY.md).

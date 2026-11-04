---
name: "knowledge-contract-core"
title: "Knowledge Contract: Core Model and Admission Requirements"
artifact: "engineering-specification"
edition: "1.0"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "The nine core groups, first-class constraints, profiles, admission and execution requirements."
---

# Knowledge Contract: Core Model and Admission Requirements

**Author:** Pavel Valentov · **Publication edition:** 1.0

## 1. Purpose and conformance

A Knowledge Contract binds a body of knowledge to its intended use, grounds, dependencies, constraints, and assessment. It lets a recipient inspect what is offered, which conditions matter, and what has actually been checked. It does not turn a source assertion into a fact or an instruction into permission to act.

This specification defines the architecture of a conforming implementation. Capitalized requirement words follow [BCP 14](../../../reference/bibliography/BIBLIOGRAPHY.md#requirement-language). Conformance MUST identify the implemented profile, its version, the reader, and the assessed scope. A claim of full conformance cannot rest on a schema check alone. Publication edition 1.0 is the edition of this document; serialized profiles retain their own versions. The [compatibility record](../../../appendices/source-map/APPENDIX.md#protocol-compatibility) identifies the existing bounded implementation without renaming it.

## 2. Core model

The contract has nine logical groups. A serializer MAY organize them differently if its mapping preserves their obligations.

| Group | Required meaning |
| --- | --- |
| Identity | Stable object identity, immutable revision, contract definition and representation profile versions |
| Purpose | Intended use, task and requirements revision, recipient, required profiles |
| Content | Addressable units, their semantic roles, source references and protected conditions |
| Scope | Conditions of applicability and explicit unknown, inapplicable or withheld values |
| Grounds | The source revision, locator, derivation and evidence supporting each relevant claim |
| Dependencies | Required relationships distinguished from optional reading links |
| Obligations | Preconditions, invariants, preservation duties, coverage requirements and acceptance obligations |
| Projection | Delivered representation, included and omitted units, declared losses and transformations |
| Observations | Assessments bound to a subject revision, method, observer, time and limitations |

An empty list MUST mean an established empty set within a declared scope. It MUST NOT stand for an unknown set. A profile MAY represent a genuinely irrelevant group as not applicable with a reason. It MUST NOT silently omit a required obligation because no evidence is available.

The contract's immutable content and the current decision to use it are distinct records. Revoking a grant changes admissibility for a use; it does not rewrite what the earlier contract said.

## 3. Constraints are first-class obligations

A **constraint** restricts an admissible interpretation, transformation, delivery or action. Each constraint MUST have an identity, subject, scope, predicate or human-readable rule, source of authority when relevant, severity, and a checking method or an explicit unresolved status. An implementation MUST retain its applicability conditions and dependencies. The [artifact registry](../artifact-registry/SPECIFICATION.md#4-constraints-and-professional-artifacts) defines the readable `CONSTRAINT.md` artifact.

Four distinctions are mandatory:

| Kind | Question | Example of an abstract rule |
| --- | --- | --- |
| Applicability condition | Under what circumstances does the knowledge apply? | The input belongs to the stated domain |
| Action constraint | What conduct is forbidden or bounded? | The operation may write only the named resource |
| Capability requirement | Can this executor perform the required method? | An assessment covers this skill and environment |
| Acceptance criterion | What demonstrates the requested result? | The delivered output satisfies the pinned criterion |

A constraint can also be an acceptance obligation, but the relationship MUST be explicit. Success at an output criterion does not excuse a prohibited action used to obtain it. A skill description does not establish capability. A role assignment does not by itself supply a grant.

When profiles compose, all applicable mandatory constraints MUST remain in force unless an identified authority has explicitly resolved a conflict within its authority. Load order, a later paragraph, or a more convenient result MUST NOT implicitly override a restriction. A contradiction blocks the affected use or produces a narrowed, explicitly permitted alternative.

## 4. Profiles and compatibility

The supported profile families are professional work, dialogue, documents, reasoning, visual representations, and reuse. Each profile declares its version, why it is present, whether it is required, and its payload. The need for a profile follows from the declared purpose and requirements; a parser is not assumed to infer it correctly from arbitrary natural language.

A reader MUST advertise supported representations and required extensions. An unknown required profile makes the contract unusable for that request. An unknown optional profile MAY be retained as opaque data, with the limitation reported. Preserving its bytes does not verify its semantics. Compatibility is directional: a new reader accepting an old record does not prove that an old reader can safely rewrite the new record.

## 5. Admission and execution

Admission MUST evaluate the exact contract revision, requirements, recipient, environment, applicable constraints, mandatory dependencies, and current authority. Each mandatory check yields pass, fail, unknown, or justified not applicable. Unknown MUST NOT be promoted to pass.

An execution additionally binds the Work Item revision, requirements revision, contract revision or digest, attempt, executor, relevant grants and capabilities, output identity, and criterion-specific evidence. Receipt of a plan is not execution. A successful process exit is not acceptance. If a remote effect is uncertain after a timeout, the attempt remains unresolved until reconciliation; a retry requires an explicit repeat policy.

A conforming execution adapter MUST validate evidence provenance at its declared trust boundary. A boolean supplied by an untrusted caller saying that evidence is trusted is insufficient. The existing finite model assumes a supplied context and does not provide that production trust boundary; this limitation is measured in the linked study.

## 6. Migration and failure handling

Migration creates a new representation and retains the source revision and transformation record. Missing conditions, grants or capabilities remain unknown. A free-text blueprint is not automatically converted into a process graph. Unmapped fields and semantic losses MUST be reported. Schema validity alone cannot justify `semantic_equivalence`.

Refusal reports SHOULD identify the failed obligation and an actionable reason without exposing protected grounds to an unauthorized recipient. An implementation MUST NOT create a success-shaped output when assembly, authorization, or evidence checking fails.

## 7. Acceptance cases and evidence

A conformance suite MUST include: a supported positive request; a missing required dependency; an unknown required profile; a conflicting constraint; an outdated requirement revision; an unauthorized executor; mismatched output evidence; a migration with unknown values; and a false claim of trusted evidence. Schema, internal consistency, applicability, and execution acceptance MUST be reported separately.

The [contract-profile study](../../studies/contract-profile-conformance/STUDY.md) reports 35/35 and 26/26 bounded scenario results, alongside false trusted-input acceptances and a 9/9 versus 9/9 baseline tie. These observations support finite conformance claims and expose the trust-boundary gap. They do not establish general task superiority or production authorization.

The scientific justification is developed in [controlled knowledge reuse](../../../papers/controlled-knowledge-reuse/PAPER.md), [evidence and falsification](../../../papers/evidence-and-falsification/PAPER.md), and the [shared glossary](../../../reference/glossary/GLOSSARY.md).

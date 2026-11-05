---
name: "contract-family"
title: "Contracts for Knowledge Operations"
artifact: "engineering-specification"
edition: "1.1"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "Common preconditions, invariants, postconditions, effects and evidence for knowledge operations."
---

# Contracts for Knowledge Operations

**Author:** Pavel Valentov · **Publication edition:** 1.1

## 1. Purpose and conformance

This is an architectural requirement set. Interoperability requires a named representation profile; the implemented exchange subset is limited to [observations, change events and profile advertisements](../status-model/SPECIFICATION.md#8-bounded-exchange-profile), and the [book-package profile](../book-package/SPECIFICATION.md) has its own schema. No full-contract wire format or deployed runtime is implied.

An operation contract states when an operation may run, what it preserves or changes, which outcomes are permitted, and what evidence supports the reported outcome. Its promise is local to a declared input, requirements revision and environment. Completing one operation does not necessarily satisfy the entire Work Item.

Capitalized requirements use [BCP 14](../../../reference/bibliography/BIBLIOGRAPHY.md#requirement-language).

**KOP-R001.** This document specifies operation semantics; a conforming adapter MUST also identify its representation profile and executable checks.

The [transformation paper](../../../papers/constrained-transformations/PAPER.md) supplies the conditional formal model.

## 2. Common contract record

**KOP-R002.** Every operation definition MUST identify the following:

| Field group | Required content |
| --- | --- |
| Definition | Operation name, immutable definition version and supported input/output profiles |
| Purpose | The local goal and its relationship to a Work Item and requirements revision |
| Inputs | Exact artifact revisions, cardinalities, relevant environment and missing-input behavior |
| Preconditions | Conditions that authorize and enable the attempt; checking methods and trust boundaries |
| Invariants | Properties preserved throughout the operation's declared observable scope |
| Postconditions | Conditions attached to each allowed outcome, including partial and refused outcomes |
| Effects | Read/write scope, external effects, repeat policy, reconciliation and compensation behavior |
| Resources | Budget, deadline, maximum attempts and stop rules |
| Evidence | Subject bindings, observation method and the limits of the evaluator |

**KOP-R003.** Preconditions, invariants and postconditions MUST remain separate.

A later successful observation does not establish that an invariant held at every earlier step. Evidence of an output's shape does not establish its semantic correctness.

## 3. Operation families

The following functional families organize implementations. They are responsibilities, not a requirement to deploy separate services.

| Family | Preservation obligation | Principal failure mode |
| --- | --- | --- |
| Acquire and address | Source identity, version, locator and acquisition provenance | An unavailable or substituted source is treated as observed |
| Interpret and extract | Attribution, negation, quantifiers, exceptions and unresolved readings | A source claim becomes an unqualified fact |
| Search and compare | Query semantics, scope, candidate provenance and comparison criterion | Similarity becomes equivalence or completeness |
| Select and compose | Mandatory dependency closure, joint identity, coverage and total budget | Necessary conditions disappear during shortening |
| Transform and render | Declared protected observations, representation requirements and losses | A readable description is substituted for essential media |
| Deliver and acknowledge | Recipient, representation, revision and delivery observation | A locator is mistaken for delivered content |
| Plan and execute | Work bindings, capability, authority, attempt identity and effects | A plan or timeout is mistaken for a known execution outcome |
| Assess and revise | Exact subject, method, new evidence and preserved history | A verdict is transferred to another revision |
| Store and reuse | Dependency pins, current applicability, authorization and invalidation | A cache hit bypasses the admission decision |

**KOP-R004.** An implementation MAY expose narrower operations within these families.

**KOP-R005.** Every exposed operation MUST state which of these responsibilities it owns and which it delegates.

**KOP-R006.** It MUST NOT hide a necessary responsibility between adapters.

## 4. Composition

**KOP-R007.** For operations A then B, every allowed successful output of A used by B MUST satisfy B's preconditions.

**KOP-R008.** A shared invariant MUST survive both transitions.

Failure to establish that relation leaves composition unresolved even when each operation passes its isolated tests.

**KOP-R009.** A semantic transformation MUST declare its protected observations: for example the truth conditions of a proposition, the order of procedural steps, or the labels and connections of a diagram.

Equality of those observations is a narrower claim than equality of all meanings.

**KOP-R010.** Lossy transformations MUST retain a loss account.

An inverse can be claimed only within a declared domain for which reconstruction has been justified.

Operations with effects require a separate composition policy. A local transaction around a record does not make an external service atomic.

**KOP-R011.** A timeout after dispatch MUST preserve an unknown-effect state until a domain-specific reconciliation establishes what occurred.

## 5. Outcomes and evidence

The outcome vocabulary is `success`, `partial`, `refused`, `failed` and `unresolved`, as defined in the [status model](../status-model/SPECIFICATION.md#3-canonical-dimension-vocabularies). `ready` is a lifecycle or run phase, not an operation outcome. Stop reasons explain why control ended; effect observations describe what is known about external changes.

**KOP-R012.** These dimensions MUST NOT be collapsed into a single completion flag.

A comparison operation can succeed by reporting non-equivalence. A refusal can correctly enforce a constraint without satisfying the user's original goal.

**KOP-R013.** Evidence MUST identify the definition version, input and output revisions, attempt, relevant requirements, checker and check result.

**KOP-R014.** An inherited observation MUST name the premise that permits inheritance.

**KOP-R015.** Checks of supplied claims and checks of independently observed conditions MUST be distinguishable.

## 6. Acceptance cases

**KOP-R016.** A conforming adapter MUST exercise valid input; invalid input; unknown mandatory preconditions; a protected-property violation; partial output; an exhausted budget; a stale requirement revision; and, for effectful operations, a timeout with uncertain effect.

**KOP-R017.** A composition test MUST include a valid A output that violates B's precondition.

The expected result is refusal or unresolved composition, not automatic continuation.

The [dependency and delivery study](../../studies/dependency-closure-and-package-delivery/STUDY.md) supplies a finite closure replay. The [executable projection study](../../studies/executable-projections-and-revision/STUDY.md) supplies bounded projection and revision evidence. Their finite results do not certify every family in this specification.

## 7. Representation and evolution

The architecture does not require a new global artifact type for each operation. A versioned definition can be represented as an addressed record linked from attempts and evidence.

**KOP-R018.** Legacy example envelopes remain interpretable under their original profiles; an adapter MUST disclose any loss when mapping them to this family.

An operation definition change creates a new version. Attempts keep the definition they used. Reassessment under the new definition is a new observation, not a retrospective claim that the earlier attempt followed it. See [knowledge evolution](../knowledge-evolution/SPECIFICATION.md) and the [status model](../status-model/SPECIFICATION.md).

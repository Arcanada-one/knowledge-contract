---
name: "compiled-artifact-contract"
title: "Compiled Knowledge Artifacts and Reproducible Derivation"
artifact: "engineering-specification"
edition: "1.0"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "Saved derivatives with exact inputs, recipes, dependency manifests, templates and output evidence."
---

# Compiled Knowledge Artifacts and Reproducible Derivation

**Author:** Pavel Valentov · **Publication edition:** 1.0

## 1. Purpose and conformance

A compiled knowledge artifact is a saved derivative produced by a declared extraction, selection, transformation or composition. It connects a result with its inputs, recipe, dependencies, requirements, output representation and evidence. Its availability can avoid repeated work, but availability alone does not justify reuse.

Capitalized requirements use [BCP 14](../../../reference/bibliography/BIBLIOGRAPHY.md#requirement-language). A conformance claim MUST identify the artifact kind, representation profile and checks performed. [Controlled knowledge reuse](../../../papers/controlled-knowledge-reuse/PAPER.md) provides the model; [cache identity](../cache-identity-and-invalidation/SPECIFICATION.md) and [reuse policy](../reuse-policy/SPECIFICATION.md) govern later applications.

## 2. Result kinds and minimum information

| Result kind | Additional minimum obligation |
| --- | --- |
| Retrieval result | Query semantics, searched snapshot, procedure limits and candidate identities |
| Selected context | Requirement coverage, mandatory closure, projection and resource account |
| Derived explanation or answer | Supported claims, intended audience, losses and required uncertainty |
| Dependency closure | Roots, relation policy, exact graph snapshot and unresolved edges |
| Parameterized template | Allowed substitutions, domain restrictions and instance validation rules |
| Scoped negative result | The exact negative claim, finite scope, completeness premise and invalidators |

These kinds do not exhaust all possible derivatives. An extension MUST state its additional obligations and compatibility rules.

## 3. Artifact and build records

The artifact MUST identify immutable output bytes or a precisely canonicalized structured value, its hash domain, representation profile, content identity, source and rule-set revisions, recipe identity, and the producing attempt. A content digest establishes equality within its encoding assumptions; it does not authenticate the author or establish source truth.

The build recipe MUST include exact input references, transformation definition versions, relevant parameters, and environment dependencies that can change the claimed result. A build identity records this declaration. Reproducibility additionally requires actual successful reruns under a stated equivalence criterion. A matching recipe hash does not prove that the recipe was executed or that nondeterministic outputs are equal.

An attempt record MUST distinguish planned, running and terminated execution; outcome; stop reason; output references if any; and observed effects. A failed attempt MUST NOT create a fictional successful artifact. Partial outputs can be retained as partial with their limitations.

## 4. Dependency manifest

The manifest MUST include each declared dependency's identity, revision, role, requirement status, relevant validity conditions and change sensitivity. Dependencies can include sources, selectors, profiles, rules, compiler versions, authority epochs, queries and requirements. Omitting a relevant dependency invalidates any claim that the manifest is complete for that use.

A result based on absence or exhaustive enumeration MUST bind the universe or index snapshot and completeness procedure. Adding a new matching item can invalidate a negative result even if none of its previously read positive inputs changed.

The manifest MUST distinguish a navigational citation from an operational dependency. It SHOULD explain why each operational dependency is material, so a reviewer can identify both missing dependencies and unjustified over-invalidation.

## 5. Templates and instances

A template defines allowed substitutions, protected structure and the conditions under which an instance may be produced. Every instance receives its own identity, bound parameters, requirements and admission decision. The template's age or prior acceptance does not automatically transfer to an instance.

Parameter substitution MUST NOT remove scope, change a protected quantifier or carry authority from one recipient to another without an explicit rule. Unvalidated parameters yield an unresolved or rejected instance. If instantiation changes the meaning outside the declared template domain, the result is a new derivation rather than a valid instance.

## 6. Evidence and publication boundary

Evidence MUST bind to the exact artifact and check. Structural validity, reconstruction equality, task sufficiency, current applicability and execution success remain separate observations. An artifact can be immutable and byte-correct while ineligible for a new request.

Publishing a mutable current pointer requires a guard against stale workers and changed dependencies. A build that finished successfully under an old generation MUST NOT overwrite a newer or revoked head. The final admission decision must be valid at the actual serve boundary, not only when the build began.

## 7. Acceptance cases and limits

A conformance suite MUST cover an altered input with an unchanged lookup key, a recipe change, an unsuccessful build, a template parameter outside its domain, a stale publication generation, a negative result invalidated by corpus growth, and evidence for the wrong output. The expected result must be an explicit new build, refusal, unresolved state or valid guarded reuse under a named policy.

The [reuse-admission study](../../studies/reuse-admission-and-cost-controls/STUDY.md) separates analytical policies, bounded checks and measured outcomes. The [projection study](../../studies/executable-projections-and-revision/STUDY.md) reports finite transformations and revision behavior. Neither establishes a deployed distributed cache or a general semantic equivalence solver.

## 8. Compatibility and migration

A migration MUST retain the old artifact and hash domain, identify the mapping and its losses, and create a new representation record. A new document edition does not change an existing binary or wire protocol. Earlier bounded profiles are named in the [compatibility appendix](../../../appendices/source-map/APPENDIX.md#protocol-compatibility); implementations claiming additional behavior require corresponding evidence.

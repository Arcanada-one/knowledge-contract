---
name: "status-model"
title: "Assessment, Execution, and Publication States"
artifact: "engineering-specification"
edition: "1.0"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "Independent assessment, execution, effect, freshness, publication and review states."
---

# Assessment, Execution, and Publication States

**Author:** Pavel Valentov · **Publication edition:** 1.0

## 1. Purpose and conformance

A status is meaningful only for a named subject, property, revision and scope. One “verified” flag cannot faithfully represent schema validity, source fidelity, truth, coverage, authorization, execution outcome and publication review. This specification separates those questions and defines their transition obligations.

Capitalized requirements use [BCP 14](../../../reference/bibliography/BIBLIOGRAPHY.md#requirement-language). A profile MUST select the dimensions needed for its purpose and declare any aggregation rule. It need not attach every possible dimension to every record. The [evidence paper](../../../papers/evidence-and-falsification/PAPER.md) explains why stronger conclusions need different evidence.

## 2. Observation record

Each observation MUST identify its subject and immutable revision, assessed property, requirements or criterion revision, method, observer, relevant time, result, grounds and limits. A result without a subject is not transferable evidence. If the method trusts supplied input rather than independently authenticating it, that assumption MUST be stated.

The check result vocabulary is `pass`, `fail`, `unknown`, and `not_applicable`. The last value requires a demonstrated inapplicability rule, not missing data. For a conjunctive set of mandatory checks, any applicable failure prevents acceptance; any remaining applicable unknown prevents an all-pass conclusion. A positive result MUST NOT overwrite a negative or unresolved result on another mandatory property.

## 3. Independent dimensions

| Dimension | Values or required distinction |
| --- | --- |
| Availability of a value | Known, unknown, justified not applicable, withheld |
| Coverage | Supported, partial, unsupported in scope, conflicted, unknown |
| Search assurance | Candidate-only, exhaustive in declared scope, incomplete procedure |
| Local run phase | Planned, ready, running, paused, finished |
| Operation outcome | Success, partial, refused, failed, unresolved |
| Stop reason | Completed, clarification needed, budget insufficient, retrieval limit, stale evidence, precondition not met, cancelled, execution error, reconciliation pending |
| External effect | No effect established, known effect, unknown effect, with the observed scope |
| Artifact lifecycle | Building, ready, quarantined, retired, failed |
| Residency | Resident, evicted, absent, unknown in a named storage location |
| Freshness | Fresh, stale, expired, unknown under a named policy and time |
| Reuse eligibility | Eligible, ineligible, unknown for a particular new use |
| Case evidence | Planned, illustrated, executed, evaluated, with the actual protocol and outcome |
| Publication and review | A fixed document edition; its publication decision; separate editorial, internal technical or external review observations |

The table is a semantic mapping. Existing wire profiles can retain different lexical values if their adapter declares an unambiguous mapping. Legacy labels MUST NOT be silently redefined.

## 4. Transition rules

Execution can move from ready to running only when the attempt's preconditions are established. Local termination records a stop reason and outcome; it does not determine an unobserved remote effect. A later reconciliation can add an observation about that attempt without claiming a second execution.

An artifact becomes ready only under its build and publication policy. A later dependency change can make it ineligible while its bytes remain resident and intact. Eviction changes residency, not the truth of content or its historical applicability. Revalidation creates a new observation; it does not change the immutable payload unless a new revision is produced.

A changed requirement, subject revision, environment or authority can invalidate the applicability of an earlier verdict. Reuse of that verdict requires an explicit preservation argument. The latest timestamp alone is not such an argument.

## 5. Scientific and editorial status

A completed publication can state conditional propositions and report bounded results while acknowledging unanswered empirical questions. Its edition number identifies a coherent text, not proof of all future applications. The vocabulary MUST not equate “published,” “reviewed,” “implemented,” and “effective.”

An internal agent review MUST identify the reviewer, input revision, method and conclusions, and MUST be labelled as such. It does not constitute independent external peer review. A finite test report requires actual outputs; an illustrated scenario is not an executed test. An executed failed trial remains useful evidence and MUST retain its negative result.

## 6. User-facing projections

Interfaces MAY summarize these dimensions, but the summary MUST preserve the distinctions relevant to the user's decision. “Indexed revision X” is more precise than an unqualified “current.” “Checks passed for the supplied record” must not become “the action is authorized” when current authorization was outside the checked boundary.

An unknown effect after a timeout must remain visible when a user decides whether to retry. Technical detail can be expanded on demand, but critical uncertainty cannot be hidden behind a positive badge.

## 7. Acceptance and evidence

Tests MUST cover a passed schema with false supplied grounds, successful execution with a failed result criterion, a finished run with unknown effect, a resident but revoked artifact, a correct historical result ineligible for a current task, and an internal review that does not establish empirical validity.

The [conformance study](../../studies/contract-profile-conformance/STUDY.md) demonstrates why a trusted-input premise matters. The [editorial pilot](../../studies/editorial-skill-pilot/STUDY.md) reports an equal observed score for the structured and baseline conditions. Neither result permits a general effectiveness label. See [revision and governance](../../../papers/revision-and-governance/PAPER.md) for the distinction between an observation and adoption of a rule.

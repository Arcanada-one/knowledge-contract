---
name: "status-model"
title: "Assessment, Execution, and Publication States"
artifact: "engineering-specification"
edition: "1.1"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "Independent assessment, execution, effect, freshness, publication and review states."
---

# Assessment, Execution, and Publication States

**Author:** Pavel Valentov · **Publication edition:** 1.1

## 1. Purpose and conformance

This is an architectural requirement set. Interoperability requires a named representation profile; the implemented exchange subset is limited to [observations, change events and profile advertisements](../status-model/SPECIFICATION.md#8-bounded-exchange-profile), and the [book-package profile](../book-package/SPECIFICATION.md) has its own schema. No full-contract wire format or deployed runtime is implied.

A status is meaningful only for a named subject, property, revision and scope. One “verified” flag cannot faithfully represent schema validity, source fidelity, truth, coverage, authorization, execution outcome and publication review. This specification separates those questions and defines their transition obligations.

Capitalized requirements use [BCP 14](../../../reference/bibliography/BIBLIOGRAPHY.md#requirement-language).

**STA-R001.** A profile MUST select the dimensions needed for its purpose and declare any aggregation rule.

It need not attach every possible dimension to every record. The [evidence paper](../../../papers/evidence-and-falsification/PAPER.md) explains why stronger conclusions need different evidence.

## 2. Observation record

**STA-R002.** Each observation MUST identify its subject and immutable revision, assessed property, requirements or criterion revision, method, observer, relevant time, result, grounds and limits.

A result without a subject is not transferable evidence.

**STA-R003.** If the method trusts supplied input rather than independently authenticating it, that assumption MUST be stated.

The check result vocabulary is `pass`, `fail`, `unknown`, and `not_applicable`. The last value requires a demonstrated inapplicability rule, not missing data. For a conjunctive set of mandatory checks, any applicable failure prevents acceptance; any remaining applicable unknown prevents an all-pass conclusion.

**STA-R004.** A positive result MUST NOT overwrite a negative or unresolved result on another mandatory property.

## 3. Canonical dimension vocabularies

**STA-R005.** A profile using the current tokens MUST use the snake_case values below without overloading one dimension with another.

**STA-R006.** An older profile MAY retain its original lexical values only through an explicit, loss-reporting adapter.

| Dimension | Tokens |
| --- | --- |
| Availability | `known`, `unknown`, `not_applicable`, `withheld` |
| Coverage | `supported`, `partial`, `unsupported`, `conflicted`, `unknown` |
| Search assurance | `candidate_only`, `exhaustive_in_scope`, `incomplete_procedure` |
| Local run phase | `planned`, `ready`, `running`, `paused`, `finished` |
| Operation outcome | `success`, `partial`, `refused`, `failed`, `unresolved` |
| Stop reason | `completed`, `clarification_needed`, `budget_insufficient`, `retrieval_limit`, `stale_evidence`, `precondition_not_met`, `cancelled`, `execution_error`, `reconciliation_pending` |
| External effect | `none_established`, `known_effect`, `unknown_effect` |
| Artifact lifecycle | `building`, `ready`, `quarantined`, `retired`, `failed` |
| Residency | `resident`, `evicted`, `absent`, `unknown` |
| Freshness | `fresh`, `stale`, `expired`, `unknown` |
| Reuse eligibility | `eligible`, `ineligible`, `unknown` |
| Evolution impact | `compatible`, `restricted`, `requires_review`, `blocked`, `unknown_impact` |
| Reuse decision | `exact_reuse`, `revalidate`, `rebuild`, `instantiate`, `refuse`, `unresolved`, `serve_stale` |
| Case evidence | `planned`, `illustrated`, `executed`, `evaluated` |
| Review kind | `editorial`, `internal_technical`, `independent_agent`, `external_peer` |

`unsupported` always refers to the declared evaluated scope. `ready` describes run or artifact availability and is not a successful operation outcome. `none_established` reports no established effect within the observed scope; it does not assert that no remote effect exists. Review kind describes the actual protocol, not the name of the reviewer. An independently tasked agent review is not external human peer review.

**STA-R007.** Legacy labels MUST map explicitly: `terminated` → run phase `finished`; `unsupported in scope` → coverage `unsupported`; “incomplete execution of planned search” → `incomplete_procedure`; `not_measured` → assessment `unknown` with reason “no observation.” Profile-specific quality states such as book-package `reviewed` retain their own declared scope; they are not aliases for `pass`.

Evolution impact is an input to admission, not a shortcut to its conclusion:

| Impact | Eligibility and permitted next decision |
| --- | --- |
| `compatible` | Still `unknown` until every other mandatory gate passes; then eligible for the policy's permitted reuse |
| `restricted` | Original broader request is ineligible; a separately identified narrowed request is assessed anew |
| `requires_review` / `unknown_impact` | Unknown eligibility; `revalidate` or `unresolved`, with no admitted serve yet |
| `blocked` | Ineligible for that use; `refuse`, or a distinct permissible rebuild/instance evaluated from its own grounds |

## 4. Transition rules

Transitions apply to the same identified attempt, lifecycle instance, policy and use scope.

**STA-R008.** Implementations MUST follow the tables; transitions not listed are rejected.

Creating a new subject or attempt starts a new history rather than changing the meaning of an old record.

**STA-R009.** Every transition MUST record the triggering observation, actor, prior state and guard result.

### Execution phase

| From | Event and guard | To | Terminal? |
| --- | --- | --- | --- |
| no attempt | Allocate a unique attempt with pinned Work Item and requirements | `planned` | no |
| `planned` | Establish inputs, capability and preconditions for dispatch | `ready` | no |
| `ready` | Recheck current authority and preconditions at actual dispatch | `running` | no |
| `running` | Record a resumable checkpoint under a declared pause policy | `paused` | no |
| `paused` | Validate checkpoint, current bindings and renewed dispatch guards | `running` | no |
| `planned` / `ready` | Cancel, refuse or fail before dispatch; record reason and actual effect observations | `finished` | yes |
| `running` / `paused` | Terminate with explicit outcome, reason and effect observations | `finished` | yes |

**STA-R010.** A finished attempt MUST NOT return to running; retry uses a new attempt with a repeat policy.

Later reconciliation adds effect observations to the same historical attempt without pretending another execution occurred. A successful process exit does not supply missing acceptance evidence.

### Artifact lifecycle

| From | Event and guard | To | Terminal? |
| --- | --- | --- | --- |
| no lifecycle | Allocate a build record | `building` | no |
| `building` | Successful build, required checks and the atomic publication guard all pass | `ready` | no |
| `building` | Build fails; retain cause and any explicitly partial output | `failed` | yes |
| `building` / `ready` | Authorized integrity, safety or provenance investigation suppresses use | `quarantined` | no |
| `quarantined` | Authorized release after cause resolution, complete reassessment and current publication guard | `ready` | no |
| `building` / `ready` / `quarantined` | Authorized withdrawal or cancellation retires this lifecycle | `retired` | yes |

`quarantined` means use is suspended while a named issue is investigated; only the policy's authorized actor can release it. `retired` means this lifecycle is withdrawn and cannot become ready again. `failed` is also terminal for this build. A replacement or reinstatement creates a new lifecycle/adoption record and retains prior revocations and restrictions. Identical bytes do not erase those decisions.

### Freshness and eligibility projections

These are projections of immutable observations, not edits to old verdicts.

**STA-R011.** New projection records MAY replace the current display only while preserving the observations on which earlier displays were based.

| Dimension: from | Trigger and required evidence | To |
| --- | --- | --- |
| Freshness: any | A new applicable check, valid clock bounds and current policy establish a new window | `fresh` |
| Freshness: `fresh` | Soft deadline reached while no hard deadline has expired | `stale` |
| Freshness: `fresh` / `stale` | A hard deadline or permitted age bound is reached | `expired` |
| Freshness: any | Mandatory time, policy or chronology cannot be established | `unknown` |
| Eligibility: any | Every current mandatory gate for this exact request is discharged | `eligible` |
| Eligibility: any | A known mandatory restriction fails | `ineligible` |
| Eligibility: any | A material dependency, authority or assessment becomes unknown | `unknown` |

**STA-R012.** An expired or ineligible observation MUST NOT be overwritten merely because another record has a later timestamp.

Eligibility can become positive only after every known blocking cause is resolved under the current policy. Rechecking a digest alone cannot renew source-event age. The [reuse policy](../reuse-policy/SPECIFICATION.md) defines deadline and decision semantics.

Residency changes only on storage observations: storing and reading back the named bytes establishes `resident`; an eviction receipt establishes `evicted`; a scoped absence check establishes `absent`; lack of trustworthy storage observation gives `unknown`.

**STA-R013.** These transitions MUST NOT change truth, review, freshness or eligibility by themselves.

Assessment, coverage, assurance, external effect, review and case-evidence records are append-only observations. They have no automatic success progression: an illustration never becomes an executed trial without a new execution record, and an unknown effect is resolved only by evidence from the relevant effect boundary. Conflicting observations remain addressable. The monotone properties are observation history, terminal attempt/lifecycle histories and non-reused [publication generations](../cache-identity-and-invalidation/SPECIFICATION.md#5-guarded-publication-and-serving), not steadily improving truth or eligibility.

## 5. Scientific and editorial status

A completed publication can state conditional propositions and report bounded results while acknowledging unanswered empirical questions. Its edition number identifies a coherent text, not proof of all future applications.

**STA-R014.** The vocabulary MUST NOT equate “published,” “reviewed,” “implemented,” and “effective.”

**STA-R015.** An internal agent review MUST identify the reviewer, input revision, method and conclusions, and MUST be labelled as such.

It does not constitute independent external peer review. A finite test report requires actual outputs; an illustrated scenario is not an executed test.

**STA-R016.** An executed failed trial remains useful evidence and MUST retain its negative result.

## 6. User-facing projections

**STA-R017.** Interfaces MAY summarize these dimensions, but the summary MUST preserve the distinctions relevant to the user's decision.

**STA-R018.** “Indexed revision X” is more precise than an unqualified “current.” “Checks passed for the supplied record” MUST NOT become “the action is authorized” when current authorization was outside the checked boundary.

**STA-R019.** An unknown effect after a timeout MUST remain visible when a user decides whether to retry.

Technical detail can be expanded on demand, but critical uncertainty cannot be hidden behind a positive badge.

## 7. Acceptance and evidence

**STA-R020.** Tests MUST cover a passed schema with false supplied grounds, successful execution with a failed result criterion, a finished run with unknown effect, a resident but revoked artifact, a correct historical result ineligible for a current task, and an internal review that does not establish empirical validity.

The [conformance study](../../studies/contract-profile-conformance/STUDY.md) demonstrates why a trusted-input premise matters. The [editorial pilot](../../studies/editorial-skill-pilot/STUDY.md) reports an equal observed score for the structured and baseline conditions. Neither result permits a general effectiveness label. See [revision and governance](../../../papers/revision-and-governance/PAPER.md) for the distinction between an observation and adoption of a rule.

## 8. Bounded exchange profile

The [JSON Schema](../../../schemas/contract-observation.schema.json), [validator](../../../tools/check_contract_profile.py), [examples](../../../schemas/fixtures/contract-observation/valid/) and [tests](../../../tools/test_contract_profile.py) define a concrete exchange subset: `kc-observation/1`, `kc-dependency-change/1` and `kc-profile-advertisement/1`. This is an original project profile using [JSON](https://www.rfc-editor.org/rfc/rfc8259) and [JSON Schema 2020-12](https://json-schema.org/draft/2020-12/json-schema-core), not a claim that a full Knowledge Contract, executor or API is interoperable.

**STA-R021.** An exchange record MUST be a single strict UTF-8 JSON object without a BOM, duplicate member names at any depth, non-finite number tokens or isolated Unicode surrogates.

Unknown fields, profiles and record versions are rejected.

**STA-R022.** Integers used as epochs or sequence numbers MUST be in 0 through 9,007,199,254,740,991.

Timestamp strings use UTC seconds `YYYY-MM-DDTHH:MM:SSZ` with a valid calendar date; other clock models require another profile.

| Record | Required fields and meaning |
| --- | --- |
| `KCObservation/v1` | `observation_id`, `subject`, assessed `property`, pinned `criterion`, method `id`/`version`, `observer`, `observed_at`, check `result`, textual `scope`, `evidence_refs`, `trust_assumptions`, `limitations` |
| Subject/criterion/evidence reference | `artifact_id`, immutable `revision`, `hash_domain`, exact `sha256` |
| `not_applicable` observation | Additionally, a pinned `inapplicability_rule`; presence is structural evidence only, not proof that the rule applies |
| `KCDependencyChange/v1` | `event_id`, ordering `namespace`, `sequence`, `dependency_id`, old/new epochs and revisions, event `kind`, impact, observer and time; see the cache specification |
| `KCProfileAdvertisement/v1` | `reader_id`, explicit `read_profiles`, `write_profiles`, supported `hash_domains`; lists are capability declarations, not authorization grants |

**STA-R023.** Implementations MUST compare schema/profile support before exchanging records.

**STA-R024.** They MUST NOT infer support for an entire contract family from support for this subset.

Scope strings are exact descriptive bindings; automated semantic equivalence of two scope strings is outside this profile.

| Registered hash domain | Exact input and equality |
| --- | --- |
| `sha256/raw-bytes-v1` | SHA-256 of the exact referenced file bytes; no decoding or rewriting |
| `sha256/raw-utf8-json-v1` | SHA-256 of the exact valid exchange JSON bytes, including whitespace; no canonicalization or Unicode normalization |

**STA-R025.** Identity comparisons MUST include both domain and digest.

Reserializing an equal JSON value can change byte identity and therefore creates a new representation.

**STA-R026.** This profile deliberately does not define value-level canonical JSON hashing; a profile that needs it MUST name a separate procedure and domain.

Structural validation does not authenticate an observer, prove an observation or admit an action.

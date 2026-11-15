---
name: "semantic-verification"
title: "Semantic Verification: Claims, Checks and Evidence"
short_title: "Semantic Verification"
subtitle: "Claims, Checks and Evidence"
artifact: "engineering-specification"
edition: "1.1"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
status: "research-draft"
description: "Verification packets that bind claims to exact subjects, methods, observations and limitations, with a bounded profile for assessment transfer."
sources:
  - "Knowledge Contract project corpus and publication edition"
  - "BCP 14"
---

# Semantic Verification: Claims, Checks and Evidence

**Author:** Pavel Valentov · **Publication edition:** 1.1 · **Status:** Research draft

## 1. Purpose and conformance

A check can be correct and still be used to support the wrong claim. A digest
comparison concerns identified bytes. A proof concerns its stated model. A
program test concerns the executed implementation and inputs. None of these
observations alone establishes source fidelity, current permission or practical
benefit.

This specification defines how to prepare and assess a verification packet: a
record that makes those connections inspectable. It operationalizes
[Evidence and Falsification](../../../papers/evidence-and-falsification/PAPER.md)
and reuses the [Status Model](../status-model/SPECIFICATION.md), the
[Knowledge Operations](../contract-family/SPECIFICATION.md) evidence obligations
and the existing [claim–evidence index](../../studies/evidence-index.json).
It defines no second status authority.

The document supplies requirements for packet preparation and assessment, plus
one bounded finite profile for checking whether a declared assessment can be
recovered from retained observations. It does not specify a general natural
language verifier, authenticate supplied facts or establish that a deployed
system conforms. A serialization or runtime claiming interoperability needs a
named representation profile and its own implemented interface.

Capitalized requirements use
[BCP 14](../../../reference/bibliography/BIBLIOGRAPHY.md#requirement-language).

**SVR-R001.** A conformance claim MUST identify the requirements, representation
profile, exact implementation revision and evaluated scope to which it applies.

Conformance to the finite transfer profile is narrower than conformance to
packet preparation, and neither establishes scientific truth in an
unexamined domain.

## 2. Claims, subjects and assessment dimensions

A claim is a proposition with a specified interpretation and scope. Its subject
may be a mathematical model, document revision, execution attempt, implementation
build or comparative result. Several claims about the same artifact can need
different evidence.

An assessment applies a named criterion to that subject. The canonical check
results are `pass`, `fail`, `unknown` and `not_applicable`, as defined by
STA-R002–R004. A known assessment result of `unknown` is different from a
missing assessment record. A result of `not_applicable` requires the criterion's
demonstrated exemption rule; it is not a substitute for missing information.

**SVR-R002.** Each packet MUST bind one identified claim or an explicitly
enumerated claim set to immutable subject and criterion revisions, stated
quantifiers, assumptions, scope and intended conclusions.

**SVR-R003.** A packet covering several properties MUST retain their individual
results, grounds and limits, and MUST declare any aggregate decision rule.

For example, source fidelity, formal computation, world truth, authorization
and task success are separate properties. The Semantic Bridge's SBR-R010
preserves this boundary: its computed `TRUE` is not an authorization and its
`NOT_ASSESSED` is not an assessment pass. Reusing that profile does not require
renaming its domain-specific output into the canonical check vocabulary.

An overall failure also loses information. The property vectors
`(pass, fail)` and `(fail, pass)` have the same conjunctive outcome but different
grounds and repair obligations.

## 3. Verification packet

The following is a logical record model. A profile may serialize it in several
linked records when their identities and relationships are explicit.

| Field group | Required meaning |
| --- | --- |
| Claim | Exact statement, kind, quantifiers, intended conclusion and excluded stronger conclusions |
| Subject | Artifact, model or attempt identity; immutable revision; relevant input, output and build identities |
| Criterion | Requirement or evaluation-rule revision; assessed property; acceptance and inapplicability rules |
| Profile and domain | Supported representations, carrier or population, admission rules, context, time horizon and exclusions |
| Assumptions | Mathematical premises, supplied facts, trust dependencies and unavailable information |
| Method | Proof-review procedure, executable command, test design, fidelity rubric or comparison protocol |
| Oracle | How the expected answer is justified; its inputs and shared dependencies with the producer |
| Intervention | Material change for an adverse case; unchanged or irrelevant-change positive control |
| Finite inventory | Cardinality formula, bounds, planned cases, actually attempted cases, coverage and correlation limits |
| Actual observation | Raw record, observer, relevant time, environment, exact execution and output; or explicit absence of a run |
| Assessment | Per-property result, reasoning, counterevidence, limits and any unresolved obligation |
| Transfer | Old and new subjects, retained observations, fixed criterion and the premise permitting inheritance |
| Review | Exact reviewed bytes, reviewer, information available to the reviewer and the actual independence boundary |
| Revision and disposition | Preserved predecessor, changed claim, reason, affected conclusions and follow-up state |

**SVR-R004.** The packet MUST supply the observation bindings required by
STA-R002 and KOP-R013, and MUST distinguish supplied assertions from
independently observed conditions as required by STA-R003 and KOP-R015.

**SVR-R005.** An unavailable mandatory observation MUST remain explicitly
unresolved with a reason; its absence MUST NOT be converted to a positive
assessment or an inapplicability exemption.

**SVR-R006.** Every evidence reference used to support an assessment MUST
identify the relevant record, immutable content identity and location within
that record sufficiently to reconstruct the stated inference.

A JSON pointer can identify a result within a JSON record. An exact source
section can identify a proof premise. A link to an entire repository without
the relevant revision and claim location is insufficient. Public study claims
use the existing evidence index and origin records; a navigational link is not
an empirical justification.

Record completeness, authenticity and substantive support are different
questions. A complete packet can honestly conclude `unknown`. A malformed
packet is a representation or preparation failure; it does not show that the
subject's scientific claim is false.

## 4. Preparation and assessment procedure

First identify the claim and the evidence that could distinguish it from a
plausible alternative. Freeze the interpretation, input rules and failure
criterion before inspecting the decisive outcomes. Then choose a method that
addresses that claim, preserve its inputs and execute only the authorized
bounded operation. Assess the observed result without rewriting the earlier
criterion.

**SVR-R007.** A packet MUST preserve the evaluated claim and procedure revisions,
the expected outcomes and all material deviations; a post-result change MUST
create an identified successor rather than overwrite the earlier evaluation.

**SVR-R008.** The oracle description MUST disclose shared inputs, algorithms,
annotations and other dependencies that could make agreement repeat one error.

Separate code can still depend on the same wrong source annotation. A rerun
with the same algorithm establishes reproducibility under its conditions; it
does not by itself provide a second justification for the expected answer.

**SVR-R009.** A claimed theorem counterexample MUST satisfy every stated
premise and violate the conclusion; a premise-breaking case MUST be classified
as a boundary case or implementation test.

**SVR-R010.** When usefulness or successful admission is part of the claim,
the evaluation MUST include an applicable positive control as well as the
relevant adverse controls.

An always-refusing system can satisfy a narrow exclusion property while being
useless. Conversely, a failure of one control is not evidence that every
operation fails. The assessment identifies which claim the observation affects.

**SVR-R011.** Original inputs, outputs, failed cases, comparator ties and
unresolved observations MUST remain traceable when a correction or new run is
reported.

## 5. Evidence methods and their limits

| Method | Minimum assessment obligation | Conclusion that the method alone does not establish |
| --- | --- | --- |
| Proof and proof review | Defined semantics, explicit premises and complete derivation; reviewer scope and gaps | That the premises describe a particular live system |
| Finite enumeration or model check | Exact finite carrier, generator, oracle, coverage and termination bound | Correctness outside the represented space |
| Implementation regression | Exact program/build, exercised entry point, inputs and expected versus observed behavior | Conformance of unexecuted paths or another build |
| Source fidelity assessment | Exact source and representation, justified reference reading, retained alternatives and omissions | World truth or source-author authority |
| Task outcome assessment | Identified task, attempt, current criterion and actual output at the relevant boundary | General capability or comparative benefit |
| Controlled comparison | Comparable acceptance conditions, intervention, baseline, outcome measure and uncertainty design | Causal benefit when the design cannot exclude the stated rivals |

**SVR-R012.** The packet MUST identify which of these methods actually supports
each conclusion and MUST distinguish imported production code, a standalone
reference model and a proposed unexecuted procedure.

An algorithm described beside a specification is not evidence of enforcement.
A test importing a production module is stronger evidence about that module
than a detached model, but only for the exercised configuration and cases.
Source reading alone does not establish that a runner loaded or used the
identified bytes.

**SVR-R013.** Empirical and comparative protocols MUST identify their units of
observation, sampling or case-selection rule, comparator, measures, uncertainty
interpretation, authorized resource bounds and stopping conditions.

No new model run, external effect or paid experiment is authorized by this
specification. A design can remain complete as a protocol while its execution
remains unperformed.

## 6. Finite verification passports

A finite passport identifies the space that was counted. Equal totals can
describe unrelated objects. The following examples illustrate that distinction;
the formulas do not by themselves assert that a new run occurred.

| Space | Cardinality and bound | Scope identity |
| --- | --- | --- |
| Directed graphs and root sets | At three labelled vertices with self-loops: \(2^{3^2}2^3=4,096\) graph/root pairs | The small-model scope in the roadmap experiment plan |
| Triples of Boolean functions | Two atoms have four assignments and sixteen Boolean functions; \(16^3=4,096\) ordered triples | The distinct historical Boolean-function scope identified in the same plan |
| Subsets of one frozen skill-root set | Twelve selectable roots: \(2^{12}=4,096\) subsets of the fixed extracted dependency graph | The retained Dependency Closure study; this does not enumerate all graphs |
| Retained-observation and assessment maps | Four labelled situations; \(2^4\) binary observation maps and \(4^4\) four-result assessment maps; \(2^4 4^4=4,096\) profiles | The finite transfer profile in Section 7 |

The first two scope identities are specified in the
[experiment plan](../../../roadmap/EXPERIMENTS.md#4-small-models-larger-models-and-code-under-test).
The third belongs to the
[Dependency Closure study](../../studies/dependency-closure-and-package-delivery/STUDY.md),
whose retained execution records have their own exact scope. These are not
interchangeable evidence for one another.

**SVR-R014.** A finite passport MUST record the carrier, generator, bounds and
cardinality derivation, and MUST keep calculated, planned, attempted, completed,
refused and unexecuted counts distinguishable.

The profile declares how those counters overlap. For example, a refusal can be
a completed expected negative case or an interrupted attempt, depending on the
frozen criterion. Report that definition rather than forcing every outcome
into an unexplained success total.

**SVR-R015.** A finite passport MUST identify vacuous cases, duplicate or
correlated configurations, and any quotienting or sampling used to reduce the
space.

The empty root set can be an intentional graph test. An empty empirical sample
does not establish useful behavior. Repeated labelings can provide distinct
program inputs without constituting independent empirical trials.

**SVR-R016.** A finite execution claim MUST report the actual stopping rule,
resources and observed completion, and MUST NOT substitute the calculated
cardinality for an executed-case count.

## 7. Bounded profile: assessment transfer

### 7.1 Fixed assessment and retained observations

Let \(S\) be a nonempty declared set of assessment situations. A situation
includes the subject revision, criterion, scope, relevant inputs, context and
time needed by the property being modeled. Let

\[
p:S\to A=p(S),\qquad v:S\to D
\]

be the retained observation and one fixed assessment function. In the finite
profile, \(D=\{\mathrm{pass},\mathrm{fail},\mathrm{unknown},
\mathrm{not\_applicable}\}\). These are stipulated model values. Their presence
does not establish that a corresponding real assessment was performed or
justified.

[Meaning Geometry, Proposition 2](../../../papers/geometry-of-semantic-representations/PAPER.md#proposition-2-recoverability-requires-agreement-on-representation-fibres)
already establishes the relevant factorization criterion. A unique function
\(\bar v:A\to D\) with \(v=\bar v\circ p\) exists exactly when

\[
p(s)=p(t)\Longrightarrow v(s)=v(t)\qquad(s,t\in S).
\]

This specification reuses that result; it makes no novelty claim for
factorization. [Knowledge Transformations, Proposition 4](../../../papers/constrained-transformations/PAPER.md#proposition-4-coherent-relations-descend-and-compose-exactly)
uses the same principle for sets of possible output observations.
[Knowledge Revision, Proposition 2](../../../papers/revision-and-governance/PAPER.md#proposition-2-checks-transfer-through-preserved-complete-inputs)
states the related complete-input condition for deterministic check results.
Equality of results still requires a separate justification of their soundness.

### 7.2 Maximal partial recovery

Failure of global factorization does not imply that every attained observation
is ambiguous. For an observation value \(a\), define

\[
D_a=\{v(s):s\in S,\ p(s)=a\},\qquad
U=\{a\in A:|D_a|=1\}.
\]

There is a unique partial function \(\bar v_U:U\to D\) assigning the sole
element of \(D_a\) to each \(a\in U\). It satisfies
\(v(s)=\bar v_U(p(s))\) on \(p^{-1}(U)\). It is the greatest sound partial map
by extension: every sound partial map on attained observations is its
restriction. Its domain is therefore maximal among subsets of attained
observations on which an exact assessment can be recovered.

This is an elementary corollary of the existing criterion. On each selected
fibre the value is constant, so the assignment is well-defined. Conversely,
if an exact factor is defined at an attained \(a\), every situation in that
fibre must receive that factor's value; hence \(D_a\) is a singleton and
\(a\in U\). The inverse image \(p^{-1}(U)\) retains whole fibres rather than
silently selecting a favourable representative.

An unattained query has \(D_a=\varnothing\) and is outside this domain. It does
not acquire a result by vacuous agreement. A singleton containing `unknown`
is determined as that model result; a singleton containing `not_applicable`
does not independently establish the exemption rule in a real application.

**SVR-R017.** A transfer application MUST identify the fixed claim, assessment
rule, situation domain and retained observations, and MUST establish the
premise permitting inheritance required by KOP-R014.

**SVR-R018.** A finite diagnostic claiming exact partial recovery MUST preserve
all stated assessment distinctions, use every supplied situation in the
queried fibre, and refuse an ambiguous or unattained query.

**SVR-R019.** A reported obstruction MUST retain at least two in-domain
situations with equal retained observations and different assessment values.

A collision refutes the proposed universal transfer from those observations.
It does not show that every particular execution failed. Adding a previously
omitted situation can change a singleton fibre into an ambiguous one, so a
result for a sample does not certify the completeness of the application model.

### 7.3 Diagnostic results and application evidence

The finite reference interface distinguishes `determined_in_model`,
`refused_ambiguous` and `refused_unattained`. These describe a diagnostic
operation; they do not replace the four canonical assessment values. A
determined diagnostic carries the model's value and the relevant fibre.

For example, take observations \((0,0,1)\) and assessments
\((\mathrm{pass},\mathrm{fail},\mathrm{unknown})\). Query 0 is ambiguous, query 1
is determined with value `unknown`, and query 2 is unattained. Reporting
`unknown` at query 1 faithfully preserves the stipulated model result without
claiming that an actual target was assessed.

**SVR-R020.** The diagnostic result MUST remain distinct from the assessment
value and from the evidence that the real target satisfies the model's
bindings, trust assumptions and criterion.

**SVR-R021.** A real-use inheritance claim MUST establish the relevant
source-to-target observation equality and application conditions; a modeled
factorization alone MUST NOT be reported as a fresh observation of the target.

Two runs can have identical retrieval records while their consumers use
different buffers. Retrieval integrity therefore does not determine the
claim that a particular consumer used those bytes. Likewise, identical
consumer inputs need not imply identical current grants. These are
constructed information-loss examples, not observations that a live consumer
or authorization check failed.

For a claim of actual consumer use, observe the effective input at the last
trusted invocation boundary before the named evaluation. Hashing a retrieved
file or an earlier buffer is insufficient when a later argument can differ.
Bind the retrieval receipt and its digests to the consumer revision, entry
point, attempt and call; retain the digest of the captured effective input
and the output produced by that same call. Identify the observer and what it
can actually attest. An output next to an input digest is not, by itself,
evidence that the output was derived from those bytes.

A useful adverse control supplies an oracle-distinguishable decoy to the
actual evaluation boundary while preserving the earlier retrieval record.
The expected changed result or explicit refusal must be justified without
using the consumer's answer as its own oracle. An applicable matched-input
case must also succeed. After a material required input changes, preserve the
old observation and capture the new input and explicit recovery separately;
do not retag the previous receipt. A relevant change and a harmless change
exercise different obligations. These controls support only the named
consumer and captured boundary under the observer's stated trust assumptions;
current permission and revocation remain separately assessed.

### 7.4 Calculated inventory for the four-situation profile

The 4,096 profiles in Section 6 divide as follows. “Partial only” means that
at least one attained fibre is constant and at least one is not.

| Binary observation fibre sizes | Observation maps | Global | Partial only | No determined attained fibre |
| --- | ---: | ---: | ---: | ---: |
| 4 | 2 | 8 | 0 | 504 |
| 1 and 3 | 8 | 128 | 1,920 | 0 |
| 2 and 2 | 6 | 96 | 576 | 864 |
| Total | 16 | 232 | 2,496 | 1,368 |

These are calculated cardinalities. For constant observations, four constant
assessment maps work and the remaining 252 do not. For a one-and-three split,
the singleton is always determined and the three-element fibre is constant
for 16 of the 256 assessment maps. For a two-and-two split, both fibres are
constant for 16 maps, exactly one for \(2\cdot4\cdot12=96\), and neither for
\(12^2=144\). Multiplying by the listed observation-map counts gives the table.

A reference oracle can independently enumerate the \(5^2=25\) partial maps
from the two observation labels into four assessment values, where the fifth
choice means undefined. Each candidate is required to be undefined at every
unattained label and to agree with \(v\) at every situation where it is defined.
The accepted candidates then have a unique greatest partial map by extension;
the diagnostic is compared with that map. Testing all candidates on every
profile gives 102,400 candidate-map checks. This is an oracle workload, not
102,400 independent observations or additional assessment profiles.

Querying both labels in each profile gives 8,192 observation queries over the
same space: 2,952 determined, 4,728 ambiguous and 512 unattained. Constant
observation maps contribute \(2\cdot4=8\) determined queries, one-and-three
splits contribute \(8(256+16)=2,176\), and two-and-two splits contribute
\(6(2\cdot4\cdot16)=768\). Only constant maps leave a label unattained,
contributing \(2\cdot256=512\) such queries. These query counts describe the
same profiles and do not add independent trials.

An execution receipt is needed before these calculated counts are described
as observed program results. Even a complete run of this space tests a finite
model; it does not discover omitted real-world situations, authenticate model
values or establish unrestricted semantic verification.

## 8. Failure behavior and acceptance cases

**SVR-R022.** A representation profile MUST distinguish malformed input,
unsupported representation, absent required evidence, resource exhaustion and
a substantive negative assessment, using the existing status dimensions
without silently collapsing their meanings.

**SVR-R023.** A result produced after an incomplete procedure MUST identify the
unexecuted scope and stopping reason and MUST NOT claim exhaustive coverage.

**SVR-R024.** A conformance packet MUST identify which acceptance cases below
were executed, their exact expected and observed outcomes, and any cases
outside its claimed profile.

| Case | Required distinction or expected behavior |
| --- | --- |
| Exact subject and criterion | Matching bindings permit assessment; changed material input or criterion needs a new justification |
| Missing mandatory observation | Remains unresolved; cannot become pass or an unexplained exemption |
| Supplied false fact | Correct computation over it does not establish source fidelity or world truth |
| Applicable positive case | Can succeed under the declared conditions; exposes an always-refusing implementation |
| Premise-preserving refuter | Refutes the specified universal conclusion |
| Premise-breaking case | Tests admission or scope; is not mislabeled a theorem refutation |
| Shared oracle error | Agreement is reported with the shared dependency, without an independent-validation claim |
| Finite count mismatch | Formula, actual inventory and observed counters are reconciled or the coverage claim is withheld |
| Ambiguous retained observation | The finite profile returns a valid collision witness and no determined assessment |
| Singleton unknown or inapplicability | Preserves the literal model result and its separate application-evidence obligation |
| Unattained observation | Refused without inventing a result |
| Domain extension | A newly added conflicting state invalidates the former fibre result for the expanded domain |
| Relevant versus irrelevant refinement | A refinement separating every conflicting pair in the queried fibre permits determination; a refinement retaining a conflicting pair still refuses |
| Mutated diagnostic | A defect that suppresses the intended distinction is caught by unchanged expected answers |
| Changed reviewer or execution setting | Records the actual separation and environment; no automatic independence or runtime transfer |

These are requirements for a claimed conformance scope, not a report that all
cases were executed by a deployed implementation. The finite transfer checker
addresses only its selected rows. Packet authenticity, source fidelity,
controlled comparison and live consumer binding need their own evidence.

## 9. Review, revisions and compatibility

**SVR-R025.** A review record MUST identify the exact subject bytes, review
method, reviewer access and material shared dependencies; it MUST distinguish
self-review, same-program rerun, separately structured review, independent
reproduction and external peer review.

**SVR-R026.** A changed claim, criterion, observation profile or material
application domain MUST receive an identified successor assessment, preserving
the earlier record and the scope it actually supported.

The complete-input transfer argument can justify retaining an unaffected
result when its premises hold. It does not authorize silently retagging an
old review to new bytes. A dependency graph can identify reassessment
candidates only relative to the dependencies represented; an affected candidate
does not automatically have a false conclusion.

**SVR-R027.** An adapter to a pre-existing observation or exchange profile MUST
declare its field and vocabulary mapping, loss and unresolved obligations;
publishing this specification MUST NOT be represented as deployment of that
adapter.

This draft does not change existing status tokens, evidence-index semantics,
historical reports or runtime protocols. Publication, source integration,
index admission, deployment and scientific acceptance retain their separate
records. The current-use conditions for permission remain necessary after a
check result has been transferred.

## 10. Sources and contribution boundary

The specification's inputs are the following existing project works at source
revision
[a5b3618034256f14f389c2c7de8da409c7c5310c](https://github.com/Arcanada-one/knowledge-contract/tree/a5b3618034256f14f389c2c7de8da409c7c5310c).
The [source inventory](SOURCE_MAP.json) records their exact blobs and the
sections used.

| Source | Role in this specification |
| --- | --- |
| Evidence and Falsification, Sections 2–5 | Claim types, assessment axes, counterexamples, reference independence and evaluation limits |
| Status Model, STA-R001–R004 and canonical dimensions | Existing observation bindings, four check results and separate status axes |
| Knowledge Operations, KOP-R013–R015 | Operation evidence, explicit inheritance premise and supplied-versus-observed inputs |
| Meaning Geometry, Proposition 2 | Existing global factorization criterion |
| Knowledge Transformations, Proposition 4 | Existing factorization of full sets of possible output observations |
| Knowledge Revision, Proposition 2 | Deterministic check transfer through complete preserved inputs, without a soundness inference |
| Semantic Bridge, SBR-R009–R011 | Same-world evaluation and separation of computed results from unassessed axes |
| Foundations plan, Semantic Verification; experiment plan, Section 4 | Existing work-package scope and distinct finite verification spaces |
| Dependency Closure study, fixed-root enumeration | Existing example of an actual finite result with its own retained graph and evidence |

The maximal partial-domain statement is an elementary application of the
existing factorization argument. The packet methodology is an engineering
proposal grounded in the project's existing evidence obligations. Neither is
presented as a new general theorem or as empirical evidence of improved agent
performance. Remaining implementation, authenticity, fidelity and comparative
obligations are explicit subjects for later scoped assessments.

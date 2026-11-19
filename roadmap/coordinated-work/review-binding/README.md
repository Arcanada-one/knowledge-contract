---
name: "coordinated-work-review-binding"
title: "Review Bindings: Preparing Evidence for Exact Claims"
short_title: "Review Bindings"
subtitle: "Preparing Evidence for Exact Claims"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
status: "repository-only-method-draft"
sources:
  - "Knowledge Contract project corpus and publication edition"
---

# Review Bindings: Preparing Evidence for Exact Claims

This method prepares a reviewable subject from exact programme, document,
criterion, applicability, evidence and review-policy inputs. Its offline result
describes preparation and record bindings. Scientific support, reviewer
authenticity and qualified review remain unresolved. The method is a
repository-only adapter to existing KC obligations; it adds no native artifact
kind, publication-catalogue entry or independent status authority.

The [execution graph](../plan/execution-graph.json) contains proposed paper
release contracts. Equality with an authored claim class or scope string can
detect a changed declaration. It does not establish that the declaration is
supported. Binding a complete document also makes changes outside its short
scope statement visible; assessing whether that document's claims are justified
still requires a suitable review.

## Interface and subject

The implementation entry point is
[`tools/prepare_cw_review.py`](../../../tools/prepare_cw_review.py).

| Operation | Bounded responsibility |
| --- | --- |
| `Artifact` | Retain exact immutable bytes with their identified revision, hash domain and digest |
| `bind_subject(...)` | Bind the graph, criterion, purpose, paper identity when applicable, full declared EN/RU/zh-Hans documents, applicability, evidence and review policy into one identified subject |
| `inspect_subject(...)` | Inspect that subject, supplied `KCObservation/v1` records, review materials and an optional predecessor descriptor; report bindings, unresolved obligations and changes |

**Typed preparation boundary.** Malformed list or dictionary inputs in the
`hash_domain`, evidence `origin` or review `purpose` selectors must produce
`Invalid`, not an incidental Python `TypeError` from hash-set or mapping
membership. These are malformed *representations*, not negative assessments of
any scientific claim. Positive legal string selectors are unchanged. The
`test_unhashable_enum_inputs_are_typed_preparation_refusals` regression checks
both container kinds for all three selectors; this is a bounded check, not a
guarantee about every malformed Python value or native admission.

`expected_source_ref` is a required argument selected separately from the packet.
The pure API compares the supplied graph bytes with that full reference and
reports its provenance as caller-selected, without authenticating the reference's
Git origin. The CLI obtains bytes from a local Git commit, checks its object type
and disables replacement objects and automatic network fetching. It does not
authenticate ownership of the local repository. Replacing the expected reference
explicitly selects a different subject; it does not transfer any old assessment.

For a paper result, the required output IDs come from that paper's contract in
the exact graph. The evidence map associates each supplied output with an
artifact, a location within it and a declared origin. An output ID or a planned
path alone does not provide the result. A locator makes a proposed inference
inspectable; its presence does not prove the inference.

The subject binds the full declared texts and the applicability and review-policy
inputs. Each language keeps its own content identity. A matching English source
pin does not certify a Russian or Chinese rendition. Review observations refer
to the completed subject; they are not included recursively in the bytes whose
assessment they record.

## Purpose determines the required preparation

An announcement describes the programme and its proposed work. Its preparation
does not require the future research outputs of every potential paper. The exact
announcement text, source programme and applicable criterion are still review
inputs. Selecting announcement as the purpose does not establish that arbitrary
prose is accurate or authorize publication.

A paper-result packet binds the particular claim and its required outputs. A
review, a conditional formal result and a bounded organizational-effect claim
retain their distinct obligations. A weaker or differently scoped conclusion
needs a separately identified subject and criterion. It cannot inherit a
stronger release contract merely by changing its label.

The [local validation record](VALIDATION.md) distinguishes the executed controls
and retained new reports from these preparation rules.

## Mapping and information limits

This adapter reuses the existing
[`KCObservation/v1` schema](../../../schemas/contract-observation.schema.json).
It does not add fields or status values to that schema.

| Existing KC mechanism | Adapter mapping and limit |
| --- | --- |
| Observation `subject` | The exact bound descriptor; equality establishes identity within the named byte domain |
| Observation `criterion` | The identified criterion revision; a supplied criterion is not automatically an authorized policy |
| Observation `scope` | The exact `observation_scope(subject, property)` string binds purpose, property, descriptor digest and full extent; semantic equivalence of different descriptions is unassessed |
| `evidence_refs` | Exact artifact references; the bound descriptor retains output associations, locators and declared origins that a bare reference does not express |
| `observer`, `method`, review materials | Supplied review identity and procedure remain inspectable; their authenticity, competence and actual independence are unestablished |
| Result and change | Mechanical checks use their declared result scope; `REVIEW_REQUIRED` is an adapter reason associated with `requires_review` and revalidation, not a new scientific verdict |

Hashes use the registered raw-byte domains. Reserializing a JSON value can change
its byte identity; the adapter does not infer semantic equivalence through an
unnamed normalization. Mapping a record preserves its supplied assertions and
limitations. It cannot recover an omitted assumption, authenticate an origin or
upgrade a source's evidence strength.

## Results and changes

A complete, correctly bound packet can pass preparation and binding checks.
`claim_support`, `qualified_review` and reviewer authenticity remain `unknown`;
the report retains `REVIEW_REQUIRED` and `effects_authorized: false`. A supplied
review with `result: pass`, different reviewer and producer IDs, a competence
description, a signature, or a successful CI record does not remove those holds.
The offline interface has no caller-controlled trust exception.

Missing mandatory material remains unresolved. Malformed input and mismatching
bindings are preparation failures; neither establishes that the scientific
claim is false. Supplied negative and unknown observations remain addressable
and cannot be erased by another supplied positive result.

A changed descriptor does not inherit observations bound to its predecessor.
Changes to text, purpose, domain, criterion, evidence or review policy produce a
new subject requiring review. The predecessor and its observations retain their
original scope. A later justified transfer would need its own identified
assessment; retagging an old review is not such an assessment.

Positive controls can establish that an unchanged, complete packet passes the
mechanical preparation checks. Adverse controls can change one binding while
preserving the others, including a stronger claim under the same class. A
synthetic complete review record tests handling of supplied records; it is never
a real approval. These are control designs, not reported execution results.

Each supplied observation also refers to one `kc-cw-review-context/1` artifact.
Its subject, criterion, property, scope, method and reviewer match the observation;
its access, shared dependencies, independence boundary and competence basis are
provided descriptions. These fields are checked for consistency, not certified.
An unrelated scope string or a generic context reused for a different property
does not satisfy the binding check. `announcement_accuracy` references the graph
and complete announcement texts; `review_protocol` references the review policy.

## Running and preserving the bounded result

Use the existing exchange validator dependency, `jsonschema==4.23.0`, and a local
checkout containing the named immutable commits. From the repository root:

```sh
python3 -B tools/prepare_cw_review.py --source-commit 9cbcd22fc215e8089363912dc531e42ef6845e29
python3 -B tools/reproduce_cw_scope_gap.py
python3 -B -m unittest tools.test_prepare_cw_review tools.test_reproduce_cw_scope_gap -v
python3 -O -B -m unittest tools.test_prepare_cw_review tools.test_reproduce_cw_scope_gap -v
```

The first command produces an inventory for the 16 proposed paper contracts. It
does not search for evidence elsewhere: unprovided results, manuscripts,
applicability descriptors and reviews remain absent from those packets. Exit zero
means that this report was prepared successfully; it does not mean publication
readiness. The JSON retains `REVIEW_REQUIRED` for every paper.

The historical reproduction executes pinned old and corrected checker bytes with
the pinned original inputs. It is a new synthetic reproduction of the two named
prose mutations, not recovered bytes of the unversioned c167 files, a rerun of
field research, or a claim that actual papers contained those statements.

## Continuation within the existing programme

This candidate supports the existing Work Items; it does not change their
proposed state, create native IDs or certify their completion.

| Existing Work Item | Bounded next output | Acceptance boundary |
| --- | --- | --- |
| CW-N10, CW-N30 | Review this adapter and define the declared resolver interface | Exact input/output profile, positive controls, adverse controls and a distinct trust boundary; no caller trust flag |
| CW-A06, CW-A07 | Appraise a bounded primary-source batch and retain claim/counterclaim cards | Full-text access, exact locations, quantifiers, assumptions, contradictory results and reviewer disposition; citation metadata alone is insufficient |
| CW-I02, CW-I03 | Fill the paper-specific claim-to-evidence matrix and complete manuscript | Every substantial claim in the full manuscript has an explicit scope and actual supporting or conflicting output; no inherited approval from the scope label |
| CW-I04 | Freeze the actual reproducibility package and its origin records | Results are retrievable at exact revisions; new synthetic controls and original observations remain distinguishable |
| CW-I05, CW-N31 | Obtain exact-version substantive and language-fidelity assessments | Actual protocol, access, reviewer competence grounds, limits and per-property results; changed EN/RU/zh-Hans bytes receive successor assessment |
| CW-N07 | Release the already prepared programme announcements through their own review and deployment path | Reviewed announcement bytes, exact merged build and public served readback; no dependency on completion of the future research |
| CW-N06 | Register through the existing authorized registrar route | Qualified native access, inventory, exact UUID/parent/dependency bindings and actual readback; offline templates remain proposals |

The scientific sequence is evidence and claim matrix → manuscript → frozen
package → substantive review → approved release and served verification. Bounded
source appraisal, adapter review and announcement release can proceed separately
within their declared prerequisites. Current-use resolution remains a separate
engineering obligation; retaining bytes after an evidence withdrawal does not
establish that the evidence remains admissible.

## Separate next stage: trusted resolution

A later adapter needs an explicit trust boundary for resolving actual review
records, their issuers, the applicable qualification requirements and evidence
of competence under the relevant conditions. It also needs the reviewed bytes,
method, access to evidence, material shared dependencies, current validity and
any revocation. A hash or a key supplied by the same untrusted packet is
insufficient to establish that boundary.

That stage requires its own implementation, positive and adverse controls, and
review. It is not implemented by this preparation method. Content acceptance,
rights, translation fidelity, native task readiness, publication and permission
for external effects retain separate decisions at their actual use boundaries.

## Sources and governing obligations

- [Semantic Verification](../../../engineering/specifications/semantic-verification/SPECIFICATION.md), SVR-R002–R008 and SVR-R025–R027: exact claims, evidence, review, successor assessments and explicit adapter losses.
- [Status Model](../../../engineering/specifications/status-model/SPECIFICATION.md), STA-R002–R004 and its bounded exchange profile: observation identity, supplied-input assumptions, separate results and registered hash domains.
- [Contract Core](../../../engineering/specifications/knowledge-contract-core/SPECIFICATION.md), KCC-R012–R017: required profiles, exact admission scope and the evidence trust boundary.
- [Cache Validity](../../../engineering/specifications/cache-identity-and-invalidation/SPECIFICATION.md), Sections 2–5: identity layers, material dependencies, change and the actual publication or serve boundary.
- [Artifact Registry](../../../engineering/specifications/artifact-registry/SPECIFICATION.md), Section 4: role, skill and competency distinctions.
- [Claim–evidence index](../../../engineering/studies/evidence-index.json): existing links from bounded claims to retained records, origins and limits.

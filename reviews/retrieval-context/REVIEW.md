---
title: Retrieval and context composition - revision and verification note
sources: ["Knowledge Contract project corpus and publication edition", "Lewis et al. 2020", "Karp 1972", "Nemhauser Wolsey Fisher 1978", "Editorial experimental input"]
status: candidate; producer self-review; independent review pending
---

# Retrieval and context composition: revision and verification note

## Scope and immutable inputs

This note accompanies the fourth existing manuscript in the current editorial sequence, [Retrieval, Coverage, and Context Composition under Resource Limits](../../papers/retrieval-and-context-composition/PAPER.md). It is a revision of an existing paper, not another foundations manuscript, a source-book conversion, an accepted new publication edition, or evidence of a deployed selector.

Baseline commit: `ea0c30575d56e793fb2875df47126ab3f6dc30ad`.
Baseline file Git blob: `1163fcb4223023919f63f26876d1702de359a1aa`.
Baseline file SHA-256: `6ebbb43bcdd09ba44b60d6b0e4fce9ec05dcd1550f1d8c43bf451379508b6773` (14,439 UTF-8 bytes).
Candidate SHA-256: `e457fadcb17424e15083504a2babb2646aedc8aec7370048cd77854a8c7af64f` (22,749 UTF-8 bytes).

The complete original is preserved in Git at the baseline. Only this paper and its verification artifacts are changed. Other manuscripts, historical reports, normative requirement identifiers, catalogue membership, admission decisions and index state are outside this change.

## Change ledger

| ID | Location | Change | Kind and acceptance question |
| --- | --- | --- | --- |
| RC01 | Abstract and Section 1 | State the research question, contribution and deductive method; distinguish four assessment boundaries | Expository; no new empirical superiority or approximation claim |
| RC02 | Section 2 | Add a labeled boundary table and distinguish unknown support from a passing assessment | Expository clarification; scopes and revisions must remain separate |
| RC03 | Section 3 | Declare the finite dependency universe and treat unavailable required revisions as unresolved obligations | Scientific scope clarification; graph completeness is not semantic completeness |
| RC04 | Section 3 | Introduce delivered support as a separately justified property of the actual representation | Scientific clarification; closure membership cannot certify loss during rendering |
| RC05 | Sections 3 and 5 | State componentwise resource limits, overhead, and shared-dependency accounting | Scientific clarification; no arithmetic across unrelated units, no claim that shared cost alone destroys submodularity |
| RC06 | Section 4 | Qualify early stopping: an incumbent exists only when one has actually passed; separate independent bounds | Scientific clarification; no unsupported infeasibility or optimality |
| RC07 | Section 4 | State the finite ground set and full-ground exhaustion convention for the classical greedy result | Scientific clarification; retain the original proposition and proof, no transfer to arbitrary knapsack constraints |
| RC08 | Sections 5 and 6 | Add discriminating constructed cost/delivery cases and concrete result-reporting obligations | New analytic illustrations, not observations of a production agent |
| RC09 | Section 7 | Link the new finite verification package without rewriting historical evidence | New verification record; not a historical rerun or an empirical selection study |
| RC10 | Section 8 | Add a conclusion distinguishing results from unmeasured questions | Expository; sufficient conditional claims remain bounded |

## Preserved material

The three original proposition statements and arguments are unchanged byte for byte. The front matter, title, bibliography, joint-ground counterexample, all original mathematical expressions, all original link targets and all old headings remain. The first and third proposition's surrounding explanation was extended, so their whole containing sections are not claimed to have unchanged bytes. One inline expression for delivered support, one verification-note link, a table and the conclusion are additions. Existing source and study limitations remain visible.

## Editorial method and limits

The producer used the previously read writing-editor methods for defining the reader/task, simplifying wording without changing meaning, protecting qualifications and numbers, organizing paragraphs, and reviewing the complete result against its source. They were adapted from a toolkit whose stated application profile is Russian practical prose. This pass does not re-certify that toolkit, generalize its efficacy to English scientific writing, reproduce source-book text, or claim an independent reading experiment. Clarity is not measured by shortening; the candidate is longer because it makes obligations and limitations explicit.

Scientific changes are listed separately above. General editorial rules do not prove mathematical results, justify a missing empirical finding, or permit silent changes to premises.

## Verification performed

The [checker](../../tools/verify_retrieval_context.py) uses Python's standard library. It prints the deterministic JSON retained in [RESULTS.md](RESULTS.md). It performs 22 document checks, 17 boundary controls and two finite enumerations. It compares the root-enumeration selector with a separately defined oracle over closed delivered sets. The oracle is algorithmically different but written and reviewed by the same producer; it is not independent peer review.

The selector model covers three revisions, all 64 directed graphs without self-loops (cycles are included), two nonempty conjunctive support groups, overhead zero or one, and budgets zero through seven. There are 50,176 graph/group-pair/overhead/budget instances, each with eight root selections. Exactly 11,328 instances are feasible and 38,848 infeasible within that declared profile. No disagreement with the closed-set oracle was found. All semantic validity and authority premises in this enumeration are fixed as satisfied; the code does not discover or certify them. Alternative groups and unknown validity are exercised by separate boundary controls, not falsely included in that exhaustive denominator.

The greedy model covers all 512 three-set/three-feature incidence matrices, two nonnegative weight profiles, and cardinality limits one through three: 3,072 instances. It checks every greedy tie resolution against the exact rational bound. No violation was found. This is only the weighted-coverage subclass, not an enumeration of all submodular functions and not a cost-constrained or mandatory-coverage algorithm guarantee.

Six deliberately faulty alternatives are distinguished by their fixtures: checking the closure instead of delivered content; double-counting shared dependencies; omitting rendering overhead; treating unknown validity as passed; labeling an interrupted enumeration infeasible; and adding incomparable budget components. These are mutations of abstract decision rules inside the harness, not mutations of production code. Their detection demonstrates that the corresponding controls discriminate those errors, not that every possible defect is detected.

Reproduce at the candidate revision:

```sh
python3 -B tools/verify_retrieval_context.py \
  --paper papers/retrieval-and-context-composition/PAPER.md
```

The checker binds the exact candidate hash and protected-block digests. A later editorial change requires a new recorded candidate and a reviewed update of these locks; silently refreshing the locks is not validation. The result contains no machine-dependent timestamps and can be compared exactly. Any assertion or input error exits unsuccessfully; the script does not overwrite stored results.

## Scientific self-review

Producer: KC-Brain. Independence: none. Full source and candidate were read, not only their diff. The protected propositions' proofs still establish their stated conditional conclusions. The new delivered-support requirement makes an already discussed boundary explicit rather than implying that graph validity proves it. The original lack of a deployed selection evaluation is not erased by the new synthetic checker.

A source-level issue remains intentionally outside this paper's result: an application must supply sound interpretations and support assessments for real documents. No schema, finite graph enumeration, source hash or count in this note supplies those semantics. The examples are not professional advice or observed human tasks.

Eight questions are prepared for a separate reader: What does complete enumeration certify? When is there a verified incumbent? Why can a closed selection fail delivery? Why can a rule and exception have zero individual marginal value? Why are shared cost and submodularity different questions? Which limits apply to the greedy bound? Why are vector resource limits not added? Which claims remain unmeasured? Responses are not yet observed; no comprehension score is assigned.

## Acceptance and remaining work

Local finite checks: passed for the stated inputs and this manuscript hash. Producer semantic review: completed with the changes disclosed above. Separate exact-version scientific review: pending. Repository-wide mandated checks: not claimed by this note; their actual CI/run records must be read separately. Public site build, deployment, live readback and index refresh: not performed by this artifact.

Review should focus on delivered-support preservation, the finite decision-space boundary, unknown assessments, vector budgets, the distinction between mandatory feasibility and optional approximation, and the new examples' scope. A reviewer must inspect these exact bytes and return concrete findings; an earlier article's review is not transferable. Text acceptance, source merge, site release and indexing are distinct.

## Sources and attribution

Pavel Valentov attribution and the existing text license are retained. The three primary references in the manuscript are unchanged. Publisher records for Lewis et al. (NeurIPS 2020), Karp (1972), and Nemhauser, Wolsey and Fisher (1978) were checked during preparation. The retrieved Springer abstract states the cardinality-greedy assumptions and bound. That source check is not represented as a new full-text peer review of the historical publications. Source works and the private editor toolkit are not redistributed.

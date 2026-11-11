---
title: Meaning research - verification and falsification plan
sources: none
status: proposed experiments - not observed results
updated: 2026-11-06
---

# Verification and falsification plan

> Editorial context (8 November 2026; execution direction updated 11 November): names replace opaque reader-facing labels; compatibility mappings are in [workstreams.json](workstreams.json). At the 8 November checkpoint the operator had paused engineering execution. The operator restored availability on 11 November; [Active Work](EXECUTION_STATUS.md) now governs current work. This document alone authorizes no deployment, costly experiment or unrestricted execution; task, review, access and budget gates still apply.

This is a prepared design for [the roadmap tasks](TASKS.md), not a report of new experiments. It combines exact mathematical obligations, bounded model checks, implementation tests and empirical studies without conflating their conclusions. The existing papers retain their own narrower evidence.

## 1. What can count as evidence

For every claim, record its immutable text, type, quantifiers, premises, representation/profile, observation space and scope. State the expected positive control, adversarial intervention, reference oracle, material error criterion, budget and stopping rule before the relevant evaluation. Record what was not measured.

A mathematical counterexample satisfies all stated assumptions and falsifies the conclusion. A case violating an assumption tests the boundary or an implementation's admission behavior. A defect in an extracted graph is not automatically a defect in a theorem about closure on the supplied graph. A passing schema cannot establish semantic completeness. An empty output relation and an all-rejecting system need explicit positive-path checks.

Report four distinct outcomes: supported within the inspected scope, refuted, inconclusive and not measured. Preserve raw inputs, outputs, failures, seeds, exact tool/model/build revisions and source rights. Producer self-review is not independent review; a second agent is not a human participant; a non-blind review is not a blinded study. A rerun of the same algorithm is not an independent oracle.

## 2. Hypotheses and their rejection conditions

| Study question | Target work | Planned observation and competing explanation | What would defeat the proposed claim |
| --- | --- | --- | --- |
| Can a bounded formal bridge retain the conditions needed for a stated use? | Semantic Bridge, Extraction Fidelity | Compare source-bound reference interpretations with converted objects; separate omissions, hallucinations and unresolved ambiguity. | A permitted conversion silently removes a required condition or forces an unjustified reading. |
| Does composition preserve the declared observations? | Transformation Algebra, Falsification Register | Check local contracts and both intermediate compatibility obligations against exact transitions. | All assumptions hold but endpoint observations differ; assumption failures are classified separately. |
| Are equivalence classes and partial operations well defined? | Transformation Algebra, Meaning Cases | Vary representatives under the same profile and inspect both domain membership and output observations. | Equivalent representatives change admissibility or produce inequivalent outputs under the declared law. |
| Does a residual really reconstruct, and is it useful? | Transformation Algebra, Meaning Cases, Practical Utility | Verify reconstruction separately from size, retrieval cost and applicability. | Reconstruction fails, or a claimed efficiency advantage disappears against the full-source/simple-residual baseline. |
| Can geometric similarity safely support the intended decision? | Semantic Geometry, Geometry Evaluation | Evaluate close contradictions, distant paraphrases and context-dependent neighbors with independently defined labels. | Similarity is used as equivalence or authorization and produces an unsafe acceptance; metric axioms claimed for a nonmetric measure fail. |
| Does hybrid retrieval improve useful safe use? | Hybrid Retrieval, Agent Application, Practical Utility | Compare useful accepted results, coverage, unsafe acceptance, refusal and total cost. | Apparent accuracy is caused by rejecting everything, test leakage, unequal requirements or weaker baselines. |
| Does the actual runtime enforce the specified boundary? | Theory Traceability, Runtime Conformance, Current Authority | Run named code/builds and observe the actual protected operation, not just an earlier refusal. | A malformed/stale/unauthorized artifact reaches the protected operation, or the instrumentation cannot distinguish the target boundary. |
| Does the editorial adaptation improve comprehension without changing the science? | Editorial Evaluation | Separate protected-claim review from observed reader responses and from stylistic preference. | A qualifier or quantifier changes, readers misunderstand a critical premise, or the ordinary baseline ties/wins. |

These are research questions and candidate assertions. They are not promised positive findings. A general proof, a bounded exhaustive result and a statistical estimate require different acceptance records.

## 3. Practical case families

The following 18 families are a coverage design, not 18 completed trials or a statistically sufficient sample. Each needs at least a valid instance, a materially changed adverse variant and an irrelevant-change control. Some families require many examples; empirical sample sizes are fixed later from the declared estimand, expected variability and resource budget, before held-out evaluation.

| Case family | Concrete example and intervention | Required distinction | Tasks |
| --- | --- | --- | --- |
| C01 Units | Convert 100 cm to 1 m; negative variant treats a temperature or different dimension as length. | Same quantity versus same number or label. | Semantic Bridge, Meaning Cases |
| C02 Scoped negation | Compare 'not every item passed' with 'no item passed'. | Different quantifier/negation scope. | Semantic Bridge, Extraction Fidelity |
| C03 Exception | Summarize a rule with an explicit exception; remove only the exception. | Fluent summary versus preserved applicability. | Meaning Cases, Extraction Fidelity |
| C04 Attribution | 'Source A claims P' versus 'P is established'. | Reporting a claim versus endorsing it. | Semantic Bridge, Extraction Fidelity |
| C05 Ambiguous reference | Two possible referents remain plausible; require the system to retain both or seek clarification. | Uncertainty versus forced false precision. | Semantic Bridge, Extraction Fidelity |
| C06 Context transfer | Keep the same words but change the recipient, purpose or isolation scope. | Topic similarity versus admissible use. | Meaning Cases, Agent Application |
| C07 Composition | First step preserves a value but discards units; second preserves the surviving string. | Local checks versus matching endpoint observations. | Transformation Algebra, Falsification Register |
| C08 Partial equivalence | Choose equivalent representatives, but let an operation accept only one. | Output equality versus domain congruence. | Transformation Algebra, Meaning Cases |
| C09 Residual | Project a two-field record and restore it with/without the omitted component. | Inverse with retained information versus impossible information recovery. | Transformation Algebra, Meaning Cases |
| C10 Contradictory grounds | Give inconsistent premises or two disagreeing sources. | Vacuous classical consequence versus justified operational recommendation. | Transformation Algebra, Falsification Register |
| C11 Negative query | Insert a visible matching record into the same search domain; controls insert outside, invisible or nonmatching records. | Definite invalidation versus an irrelevant change. | Meaning Cases, Current Authority |
| C12 Geometry chain | Points 0, 0.6, 1.2 with a similarity threshold 0.7; test transitive clustering. | Pairwise threshold similarity versus equivalence. | Semantic Geometry, Geometry Evaluation |
| C13 Representation collision | Deliberately map distinct action-relevant inputs to one representation. | Lost distinction versus a decision that requires it. | Semantic Bridge, Semantic Geometry |
| C14 Retrieval closure | Fetch a skill without its mandatory constraint, then fetch the complete pinned closure. | Index hit versus complete accepted context. | Hybrid Retrieval, Agent Application |
| C15 Exact readback | Return altered or reassembled bytes while retaining the old metadata hash. | Claimed hash versus recomputed body identity. | Hybrid Retrieval, Runtime Conformance |
| C16 Temporal race | Revoke permission between check and delivery; run a slow old writer after a newer publication. | Earlier observation versus the protected operation's state. | Current Authority |
| C17 Multimodal/language shift | Move a qualifier into a legend, table or translated clause. | Surface similarity versus preserved condition and uncertainty. | Extraction Fidelity, Cross-Language Meaning |
| C18 Economics and editing | Compare a useful cold path and a validated reuse/editing path with all costs and preserved claims. | Actual benefit versus a cheaper invalid output or merely shorter text. | Practical Utility, Editorial Evaluation |

Use low-risk original examples first. Domain-specific cases that could affect health, law, finance or safety need suitable expert evaluation and cannot obtain real-world authority from this benchmark.

## 4. Small models, larger models and code under test

For n labelled vertices with directed self-loops, enumerating every graph and root set gives `2^(n*n+n)` pairs. At n=3 this is 512 graphs times 8 root sets = 4096 pairs. Historical triples of Boolean functions on two atoms have a different 4096 count: 16 functions cubed. Keep their identities, programs and conclusions separate.

A verification passport explains why each chosen size exposes the targeted error. It records raw cases, equivalence/redundancy reductions, vacuous cases and semantically distinct families where known. Repeated graphs with the same reachability do not become independent empirical observations.

The first bounded expansion is n=1..4 where the exact oracle and time/memory budget permit it. Beyond that, use explicitly seeded generated cases, longer chains, cycles, disconnected graphs and deliberate mutants. A fixed four-iteration loop from a three-vertex illustration is not a general closure algorithm: the execution plan checks stopping at a fixed point or another justified bound. Never report a large space as run merely because its cardinality was computed.

Compare with an independently implemented oracle or independently justified formal specification. Exercise the real production function separately from the reference model. Record surviving mutants and non-covered paths. Select a proof assistant or bounded checker only after defining the claim/language; naming a tool does not prove unbounded correctness. Mathematical proof review is a separate deliverable.

## 5. Experimental discipline and stopping

Before a model/service run, freeze data partitions, model/tool versions, decoding settings, seed handling, maximum time/tokens/cost, primary and secondary measures, exclusion rules and the intervention plan. Use strong simple baselines under the same requirements. Do not tune on held-out cases. Repeated generations for one source are correlated observations, not a new independent source sample.

Reference annotations preserve legitimate alternatives and disagreement. An independent checker assesses source fidelity; a different correctness question may need a different oracle. Record sample-size rationale, uncertainty intervals or justified qualitative limits before evaluation. A pilot may estimate variability, but its tuned results are not the held-out result.

Stop an individual run for budget exhaustion, invalid inputs, missing rights, unsafe effects, unverifiable environment or a detected protocol violation. Preserve its partial evidence and classify the outcome honestly. Finding a counterexample can complete a research task while triggering correction of the affected publication. It does not justify declaring an unrelated pipeline failed.

## 6. Required handback

Each completed run returns the claim/case identifiers, pinned source/profile/build, exact input manifest, operation/command and environment, raw-output references, observed counters, positive and adverse outcomes, deviations, unresolved limits and the next scientific disposition. A scientist can read the study; an engineer can reproduce the operation. Publication adopts the actual supported or negative result through Corpus Integration, not the original optimistic hypothesis.

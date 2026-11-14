---
title: "Situation Experiments: A Proposed Evaluation Protocol"
status: "author-draft"
sources:
  - "Knowledge Contract project corpus and publication edition"
  - "The Preregistration Revolution"
  - "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena"
  - "Agent Situation — Wu et al. 2026"
  - "Agent Situation — Patel 2026"
  - "Agent Situation — Sheng et al. 2026"
  - "Agent Situation — Lin et al. 2026"
license: "CC-BY-4.0"
---

# Situation Experiments: A Proposed Evaluation Protocol

**Nonnormative proposal, 14 November 2026.** No LLM experiment, independent preregistration, or empirical superiority result is reported here. The inputs are [the authored design](ENGINEERING.md) and [primary-source literature matrix](../../papers/agent-situation/LITERATURE.md). The present prototype has a narrower scope than the proposed study: synthetic observations, finite state transitions, abstract projection costs, and no real permissions or effect execution. Same-controller review is not independent scientific acceptance.

## Questions and hypotheses

The study would ask whether explicit situation maintenance improves decisions under changing evidence, and whether adaptive maintenance adds value beyond a strong deterministic implementation.

| Hypothesis | Proposed comparison and falsifier |
| --- | --- |
| H1: Adaptive maintenance improves supported task success | Full condition versus deterministic typed state; no improvement, or a harmful cost/error tradeoff, contradicts the operational hypothesis |
| H2: Typed maintenance reduces obsolete or unsupported action proposals | Typed conditions versus matched recency and vector retrieval; equal or worse error rates fail to support it |
| H3: Selective refresh reduces unnecessary work without increasing missed critical changes | Adaptive versus fixed refresh; excess missed changes or no cost improvement contradicts it |
| H4: Individual guards address their declared failure mechanisms | Single-component ablations increase the corresponding error while matched positive cases remain interpretable; indistinguishable results expose insensitive tasks or unnecessary components |

H1 would be the primary confirmatory comparison. The pilot explores all four; it cannot establish their truth. Authorization violations remain separately visible and cannot be offset by average task utility.

## Conditions and common boundaries

All conditions would receive the same task, permitted observation interfaces, external events, and action vocabulary. A common sandbox gate would block forbidden effects. Evaluation would score the **proposal before that gate**, so protection supplied by the harness does not become an alleged agent achievement.

1. **Recency:** the most recent evidence fitting a 4,096-token evidence budget.
2. **Full history:** all available history, initially capped at 16,384 evidence tokens; an explicitly unequal-cost reference.
3. **Vector retrieval:** top-ranked raw observations within 4,096 tokens, with a frozen encoder and query construction.
4. **Deterministic typed state:** scope and source keys, sequence handling, observation-time TTL, conflicts, dependency closure, fixed optional ranking, relevant-event invalidation, and fixed pre-action freshness checks.
5. **Full proposed condition:** the same guards and store as condition 4, adding task-conditioned projection and selective refresh. The adaptive policy would be specified and frozen before evaluation; it is not implemented merely by naming this condition.

Conditions 1, 3, 4, and 5 would have equal evidence budgets and identical common instructions. Maintenance calls, retrieval, and storage are additional measured costs, not free services. The deterministic comparator retains the important correctness guards; it is not deliberately degraded to produce a favorable result.

Five isolated ablations would remove, one at a time, observation-time freshness, scope binding, conflict retention, required dependency closure, and critical-change invalidation from condition 5. Fixed refresh versus adaptive refresh is already isolated by conditions 4 and 5. Disabled-guard variants remain sandboxed and clearly labelled. Multi-component changes would require a separate condition.

## Stages, sample, and seeds

**Stage A: finite engineering controls.** The authored finite design identifies eighteen control families, with hand-authored expected outcomes, positive recovery and adverse cases. The separate [Context Controls report](../../engineering/studies/agent-situation-controls/STUDY.md) records actual implementation scope and execution. A disabled guard is checked against an expected failure that was not computed by the disabled implementation. Passing establishes only the recorded cases. Unsupported behavior is recorded separately.

**Stage B: exploratory LLM pilot.** A proposed initial sample is 40 episodes: four instances of each family below, comprising two adverse and two matched positive instances. Twenty additional development episodes, two per family, would be excluded from evaluation. This size is chosen for coverage and practical debugging, not as a power calculation.

Proposed generator seeds are `1101,1102` for development and `2101,2102,2103,2104` for pilot instances. Allocation/order seed is `6101`. The first model sampling seed is `7101`; a preselected, family-balanced ten-episode subset would also use `7102` to expose sampling sensitivity. Selection uses seed `6102`, before outcomes exist. Where provider seeding is unsupported, record that limitation and immutable request settings; a seed does not promise reproducibility across backend changes.

The initial plan totals 200 core episode-runs, 50 repeated core runs, and 200 ablation runs: **450 proposed episode-runs**, not 450 independent tasks. Each run would allow at most eight decision calls and two maintenance calls. Execution awaits a frozen model revision, priced monetary ceiling, and explicit experiment budget; this document authorizes no expenditure.

| Family | Adverse case and paired positive control |
| --- | --- |
| Cold start | Missing prerequisite or grant versus valid discoverable evidence |
| Time and replay | Stale replay, future timestamp, or backward clock versus a genuine fresh observation |
| Event ordering | Delayed lower sequence or inconsistent duplicate versus ordered/idempotent delivery |
| Conflict | Incompatible independent sources versus agreement or explicit authoritative resolution |
| Scope and revocation | Account switch or revoked fixture permission versus unchanged valid scope |
| Derived state | Changed critical dependency versus an unrelated update |
| Projection budget | Required closure one unit over budget versus exact fit |
| Lost notification | Dropped update with TTL backstop versus delivered update |
| Proactivity | Irrelevant heartbeat or unnecessary interruption versus relevant deadline/event |
| Uncertain outcome | Timed-out action without receipt versus a confirmed completion receipt |

The four instances would not cover every subcase exhaustively. Each instantiated subcase would be named in the manifest; uninstantiated cases remain untested. Prototype budget units remain abstract. LLM experiments would tokenize actual serialized context, including metadata, separately.

## Pairing, oracle, and annotation

Each episode would run in every condition from a fresh isolated environment. Condition order would be randomized within episode and balanced across families; model versions would not be interleaved across an unrecorded provider upgrade. A frozen logical-time event schedule and declared action latencies would determine the environment. Wall-clock latency would be measured separately. Different actions can reveal different observations; identical access does not imply forcing identical trajectories.

The outcome oracle would combine separately specified state-transition rules, authority scope, available evidence, and task acceptance criteria. It would judge what can be supported from accessible evidence, not reward a lucky answer to a hidden fact. A task with an available, affordable verification route would not count as unanswerable merely because an agent declined to use it. Expected values would be authored before implementation output inspection and checked for positive/adverse discrimination.

Before confirmatory use, non-author reviewers would independently inspect oracle rules and ambiguous episode labels. Two annotators would assess any necessary natural-language judgments from condition-masked, randomized traces; a third would adjudicate disagreements. Essential timing, provenance, and tool outcomes would remain visible. Reports would include initial agreement, disagreements, adjudication, and suspected unblinding. Style can reveal a condition, so masking is a limited control, not guaranteed blindness.

If qualified independent annotation is unavailable, results would be labelled author-graded and restricted accordingly. Another agent under the same controller is not an independent annotator. An LLM judge could provide an auxiliary score, with randomized presentation order, but would not determine the primary outcome; documented judge biases motivate that restriction.[2]

## Leakage, rights, and scope

Development and evaluation would use distinct task templates and entity/sequence combinations. Merely changing random names or seeds does not establish generalization. Expected answers, hidden state, future events, condition labels, and evaluator prompts would be excluded from agent-visible tools and retrieval stores. A manifest would record who saw evaluation material and when. Any prompt tuning after pilot inspection would be disclosed and tested later on new templates.

Public memory benchmarks would be external comparisons with pinned dataset versions, not assumed uncontaminated tests. Their licenses and permitted uses would be checked before import. Initial episodes would use synthetic accounts, documents, and permission fixtures in an offline sandbox, with no real credentials, personal data, messages, trades, or payments. A fixture called “grant” supplies simulated state; it conveys no real authority. Retrieved text cannot elevate itself into an instruction or permission.

## Outcomes, costs, and analysis

The primary episode outcome would be **supported resolution**: correct completion when feasible, or correctly justified abstention when completion cannot be supported within the declared permissions and resource limits, with no invalid action proposal. Report these two components separately to prevent indiscriminate refusal from appearing successful. Also report avoidable refusal, correct refusal, unsafe compliance, verification requests, and unresolved outcomes.

Secondary metrics would include stale-value use, cross-scope reuse, unsupported certainty, missed and false invalidations, recovery delay, projection omissions, and duplicated effects. Count both proposed and gate-blocked forbidden actions. Report joint success and all scenario denominators, not just marginal guard accuracies.

Cost accounting would include input/output and maintenance tokens, embedding/indexing, tool reads, refreshes, storage, latency, interruptions, and actual billed amounts. Cache hits and amortization assumptions would be explicit. A provisional pilot utility is `supported_resolution − 0.5×avoidable_refusal − 0.01×tool_reads − 0.05×unnecessary_interruptions`. These weights are engineering choices, not measured user preferences. Report the cost vector and sensitivity when cost penalties are multiplied by 0.25 and 4; authorization errors remain a separate exclusion from any beneficial-system claim.

The episode is the paired analysis unit; repeats remain clustered within episode. Pilot reports would show paired differences, discordant counts, family-stratified results, and uncertainty intervals with assumptions disclosed. Forty authored episodes cannot support a universal reliability claim. No significance-driven stopping or post hoc choice of the winning metric is planned.

## Stopping, revisions, and confirmation

The pilot would stop at its fixed run/call or monetary ceiling, a sandbox escape, a material oracle defect, or an unplanned model change. Crashes, timeouts, refusals, and incomplete blocks would remain in the manifest with distinct statuses. All allocated episodes would be accounted for; unresolved infrastructure outcomes would be bounded in sensitivity analyses rather than silently removed. Retries would preserve original attempts and use a frozen retry rule.

Defects discovered after outcomes are visible would receive a dated amendment and new evidence version. A repaired replay would not erase the original result. No extra episodes would be added merely to obtain a preferred conclusion.

**Stage C: confirmation** would use a newly frozen held-out sample, exact implementation/model pins, independent oracle review, and a prospectively fixed analysis. Sample size would be selected using a declared minimum practically useful effect and desired precision, informed by pilot discordance and cost estimates. Neither the pilot’s observed winning effect nor an arbitrary sample size is a power justification. Multiple confirmatory comparisons would require a declared multiplicity policy. External preregistration, if actually completed, would be identified by its real receipt; this local authored plan is not that receipt.[1]

## Attribution and novelty boundary

Close prior art includes LongMemEval-V2’s environment-specific memory and compact evidence gathering, Supersede’s current-value maintenance, EnvTrustBench’s freshness/provenance and action-guiding evidence tests, and Scroll’s programmatic projections (abstract inspected only). Live action decisions alone therefore do not establish novelty. The proposed contribution is this explicit Knowledge Contract integration and a measured comparison of its maintenance policy against strong alternatives. No “first situation model,” first agent memory, or first proactive assistance claim is supported.

The [source register](../../SOURCES.md) supplies attribution; the [literature matrix](../../papers/agent-situation/LITERATURE.md) distinguishes established findings from the proposed integration. This protocol is an authored prospective plan, not an external registration or execution receipt.

[1] Brian A. Nosek, Charles R. Ebersole, Alexander C. DeHaven, and David T. Mellor. *The preregistration revolution.* PNAS 115(11), 2600–2606, 2018. [Primary article](https://pmc.ncbi.nlm.nih.gov/articles/PMC5856500/), DOI:10.1073/pnas.1708274114. Used for the prospective/exploratory distinction.

[2] Lianmin Zheng and coauthors. *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena.* NeurIPS 2023 Datasets and Benchmarks; [arXiv:2306.05685v4](https://arxiv.org/abs/2306.05685v4), revised 2023-12-24. Used for judge limitations, not a transferred accuracy claim.

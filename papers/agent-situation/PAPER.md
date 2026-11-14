---
name: "agent-situation"
title: "Agent Situation: Initialization, Change, and Bounded Context"
short_title: "Agent Situation"
subtitle: "Initialization, Change, and Bounded Context"
artifact: "scientific-paper"
edition: "1.1"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
status: "research-draft"
description: "A proposed, evidence-scoped lifecycle for initializing an agent's situation, maintaining changes and projecting bounded context."
sources:
  - "Agent Situation — Endsley 1995"
  - "Agent Situation — Dey and Abowd 2000"
  - "Agent Situation — Dey 2001"
  - "Agent Situation — Kaelbling et al. 1998"
  - "Agent Situation — Huang et al. 2023"
  - "Agent Situation — Ahn et al. 2022"
  - "Agent Situation — Bongard et al. 2006"
  - "Agent Situation — ROS REP105"
  - "Agent Situation — ROS Clock and Time"
  - "Agent Situation — ROS QoS Jazzy"
  - "Agent Situation — Yao et al. 2023"
  - "Agent Situation — Park et al. 2023"
  - "Agent Situation — Packer et al. 2024"
  - "Agent Situation — Liu et al. 2024"
  - "Agent Situation — Wu et al. 2026"
  - "Agent Situation — Patel 2026"
  - "Agent Situation — Horvitz 1999"
  - "Agent Situation — Sheng et al. 2026"
  - "Agent Situation — Lin et al. 2026"
  - "Knowledge Contract project corpus and publication edition"
---

# Agent Situation: Initialization, Change, and Bounded Context

**Author:** Pavel Valentov · **Publication edition:** 1.1 · **Status:** research draft

## Abstract

An agent can retain a long conversation while losing track of the account it is using, an expired observation, a revised goal or an unresolved external action. We ask how an agent should establish and maintain a task-relevant account of its situation before and during interaction, and how that account should inform a limited model context. We propose a lifecycle that separates observations, interpreted situation state, candidate intentions, model-facing projections and effect authorization. Initialization produces a bounded, partially known state. Subsequent changes are reconciled through source-scoped revisions, event and expiry handling, and dependency invalidation. A projection preserves declared mandatory dependencies or reports that the requested view does not fit. The work synthesizes situation awareness, context-aware computing, partially observable control, robotic feedback and current agent-memory research. Its proposed contribution is the inspectable connection between these components within Knowledge Contract, rather than a new general theory of context or intelligence. Elementary conditional properties expose the guarantees available under explicit assumptions. A separate finite study tests a small authored implementation; a separately identified protocol proposes controlled agent comparisons. Neither establishes improved LLM task performance, complete environmental knowledge, independent scientific acceptance or production readiness.

**Keywords:** agent context; situation assessment; initialization; freshness; uncertainty; memory update; context projection.

## 1. Question, method and contribution

Consider an agent resuming work from a saved conversation. Its notes say that a repository change needs deployment. Meanwhile, another agent has deployed it, the active account has changed and a previous tool invocation has an unknown outcome. Replaying the transcript does not establish which observations remain applicable. Conversely, reading every reachable resource before responding can be expensive, intrusive and irrelevant.

The research question is: **which distinctions and update obligations let an agent maintain an inspectable, task-relevant situation while observing and communicating under finite resources?** A subsidiary empirical question asks whether the proposed maintenance policy improves valid task completion at an acceptable total cost relative to strong deterministic state management.

We make three proposed contributions: a profile-based initialization inventory; a lifecycle connecting evidence, change and context delivery; and a falsifiable evaluation programme that separates structural controls from agent performance. This is a targeted primary-source synthesis and design proposal. It is not an exhaustive systematic review or a priority claim. Search and inspection covered situation awareness, context-aware systems, partially observable planning, robotics, mixed initiative, agent memory and recent environmental-grounding work. The [literature matrix](LITERATURE.md) records inspected editions, uses and limitations, including an abstract-only source.

Within Knowledge Contract, [Meaning in Context](../semantic-objects-and-context/PAPER.md) already distinguishes situation, request and conditions of applicability. [Context Assembly](../retrieval-and-context-composition/PAPER.md) addresses selection, support, delivery and budget. [Interaction and Memory](../interaction-and-memory/PAPER.md) distinguishes conversation, durable memory and authorized transitions. This companion paper concentrates on the temporal lifecycle: establishing a partial state, detecting relevant change, invalidating dependent views and deciding when to observe or invoke a model. It reuses the [Context Package](../../engineering/specifications/context-package/SPECIFICATION.md) vocabulary rather than proposing a competing package protocol.

## 2. Foundations and nearest prior work

### 2.1 Situation and uncertainty

Endsley separates perception, comprehension relative to goals and projection of future status, with decisions and action performance treated separately. The relevant elements are system-specific; the theory does not establish one exhaustive questionnaire for all agents ([Endsley, 1995](https://doi.org/10.1518/001872095779049543)). We use this distinction to separate acquired observations, interpretations and forecasts, without claiming that machine records instantiate human awareness.

Dey and Abowd identify identity, location, activity and time as useful contextual indices ([2000](https://sites.cc.gatech.edu/fce/ctk/chiws/Dey.pdf)). Dey's context toolkit separates acquisition, interpretation and aggregation, supporting polling, subscriptions and history ([2001](https://doi.org/10.1007/s007790170019)). These are direct precedents for a runtime that maintains relevant context outside an individual message. Our expanded inventory and its order are engineering choices.

Partially observable planning supplies a precise reason to preserve uncertainty. A belief distribution can summarize observation and action history under the specified model; choosing only the most likely world state can lose information relevant to a decision ([Kaelbling, Littman and Cassandra, 1998](https://doi.org/10.1016/S0004-3702(98)00023-X)). That sufficiency result does not apply automatically to a natural-language summary, an uncalibrated confidence score or our finite record model.

### 2.2 Robot capabilities, partial startup and feedback

SayCan combines language-based usefulness with skill feasibility in the current situation. Its sponge example distinguishes an appropriate goal from an immediately executable primitive ([Ahn et al., 2022](https://arxiv.org/abs/2204.01691v2)). Inner Monologue feeds scene descriptions, execution feedback and human changes back into planning; the authors demonstrate replanning after failures and interruptions ([Huang et al., 2023](https://proceedings.mlr.press/v205/huang23c.html)). These are concrete precedents for capability observations and outcome-driven updates, within their tested settings.

Self-modeling also has a narrower empirical meaning than an agent declaring who it is. Bongard, Zykov and Lipson report a robot adapting an inferred body model and gait after structural damage ([2006](https://doi.org/10.1126/science.1133687)). In a software agent, an equivalent research question concerns measured tool availability and failure, not consciousness or reliable introspection.

ROS REP 105 permits a local frame while the global map remains unattached until localization is available ([Meeussen, 2010](https://www.ros.org/reps/rep-0105.html)). This is a useful precedent for partial initialization. ROS documentation also distinguishes clock domains and clock jumps, and separates message deadline, lifespan and liveliness ([Clock and Time](https://design.ros2.org/articles/clock_and_time.html); [Jazzy QoS](https://raw.githubusercontent.com/ros2/ros2_documentation/jazzy/source/Concepts/Intermediate/About-Quality-of-Service-Settings.rst)). Source silence, expired data and an absent real-world object are different states.

### 2.3 Agent memory and bounded context

ReAct interleaves decisions with external interaction and observations ([Yao et al., 2023](https://arxiv.org/abs/2210.03629v3)). Generative Agents combines memory retrieval, reflection and plan revision in a simulated social setting ([Park et al., 2023](https://arxiv.org/abs/2304.03442v2)). MemGPT explicitly manages limited main context and external memory ([Packer et al., 2024](https://arxiv.org/abs/2310.08560v2)). Thus persistent context, feedback and selective model input are established directions.

LongMemEval-V2 is especially close prior work: it evaluates environment-specific states, workflows, recurring difficulties and bounded evidence gathering. Its evaluation uses pre-collected browser trajectories and a fixed reader, rather than online maintenance and complete live task success ([Wu et al., 2026](https://arxiv.org/abs/2605.12493v1)). Supersede studies retaining current values under bounded memory; its limited scale sample and single small-model training run constrain general conclusions ([Patel, 2026](https://arxiv.org/abs/2606.27472v1)). We therefore distinguish remembering a fact, determining whether it is current and invalidating an action that depended on its earlier value.

EnvTrustBench tests misleading environmental observations, including stale or false operational evidence. Its authors emphasize provenance, freshness and the point at which evidence guides action; its controlled stress-test outcomes are not production incidence estimates ([Sheng et al., 2026](https://arxiv.org/abs/2605.08828v2)). This overlaps materially with our proposed obligations. Scroll's abstract describes a programmable session environment whose selected printed projections enter model context ([Lin et al., 2026](https://arxiv.org/abs/2608.21690v1)); we have not inspected its full method and use no performance claim from it.

The remaining hypothesis is consequently narrow: an explicit, versioned connection between initialization, observation maintenance, mandatory context dependencies and current effect prerequisites may improve a specified agent workflow. Its advantage over a well-engineered deterministic baseline remains unmeasured.

## 3. Objects and state distinctions

Let \(W_t\) denote the world at time \(t\), which the agent does not directly possess. An observation \(o\) is a source-attributed record about part of that world. A situation state \(S^g_t\), at generation \(g\), is a task-relative interpretation of retained observations and declared constraints. It can be incomplete or wrong. A model context \(C\) is a bounded projection of that state; it is neither the complete state nor the world.

A candidate intention \(I\) identifies a proposed step, the goal it serves, its trigger, prerequisites, expected outcome, resource allowance and stop conditions. Authorization \(A\) is a separate input supplied by applicable policy or an authoritative mechanism. A source claiming that an action is permitted does not create a grant.

A useful observation record contains:

- The entity and field being described, environment/account scope and source identity.
- A value, explicitly absent knowledge or unresolved alternatives; the type is defined by the relevant profile.
- Source revision or producer sequence, event identity, observation time, receipt time, effective interval when known and clock domain.
- Provenance role: observed, declared, derived or inferred; dependencies of derived records.
- Applicable refresh policy, access/sensitivity classification and evidence locator.

One overloaded status field cannot express all important distinctions. We propose separate axes:

| Axis | Illustrative states | Meaning |
| --- | --- | --- |
| Epistemic state | known, unknown, conflicted | What the available records support under the declared procedure |
| Freshness | fresh, stale, expired, not assessed | Whether an observation meets its use-specific age or revalidation rule |
| Access | available, unavailable, not observable | Whether the acquisition path can currently supply the observation |
| Applicability | applicable, not applicable, unresolved | Whether this field matters to the present profile and task |
| Provenance | observed, declared, derived, inferred | How the represented content was obtained |
| Authority assessment | current, revoked, unresolved | Separately evaluated permission evidence, never a grant created by the model |

These example vocabularies are a design proposal, not new normative Knowledge Contract dimensions. “Known” means established under a declared evidence procedure; it does not imply infallibility. An unknown boolean is distinct from false. A detail omitted from a prompt can remain known in storage. “Not applicable” needs a profile-based reason; it is not a convenient substitute for missing evidence. Numerical confidence is optional and meaningful only with a defined interpretation and calibration.

## 4. Initialization as bounded readiness

Initialization establishes enough state for the first permitted operation. It does not require discovering everything. The following ordered inventory is addressed primarily to trusted runtime metadata, authorized adapters and existing records. It is not a questionnaire that the user must answer at every session.

| Order | Question | Initial record and acquisition boundary |
| --- | --- | --- |
| 1 | Who is operating, and on whose behalf? | Instance/session identity, role, accountable principal and provenance of each assertion |
| 2 | Where does this operation apply? | Workspace, account, tenant, repository/revision or physical reference frame; live, test or simulated environment |
| 3 | What time and episode is this? | Clock domain, observed current time, timezone, startup/resume episode and deadlines |
| 4 | What is the present purpose? | Current request, continuing authorized goals, success criteria, priorities and stop conditions |
| 5 | Who else participates? | Verified senders, owners, recipients, collaborators and pending handoffs; asserted identity kept separate |
| 6 | What work is already in flight? | Current phase, pending operations, last processed event and unresolved external outcomes |
| 7 | Which entities and resources matter? | Task-relevant objects, their observed states, reference frames and evidence locations |
| 8 | What is currently usable? | Tools, versions, connection health, reader capabilities and actual availability evidence |
| 9 | What actions are currently permitted? | Applicable scope, constraints, grants, expiry and revocation source |
| 10 | Which knowledge is applicable? | Artifact revisions, assumptions, dependencies, prior findings and their original scope |
| 11 | What remains uncertain? | Missing, stale, inconsistent or unobservable facts; specific observations that could resolve them |
| 12 | What resources are available? | Time, storage, context/output budget, authorized expenditure and user-attention allowance |
| 13 | What changes should be monitored? | Relevant subscriptions, deadlines, refresh policies, expected outcomes and recovery cursors |

Profiles select and refine this inventory. A conversational assistant may need no physical location. A robot may need pose and battery state; a coding agent may need repository revision and pending build status. An agent without an authorized room sensor records the room as unobserved; it does not construct a scene from conversational plausibility.

A startup deadline prevents optional sources from blocking indefinitely. The result can be ready for a bounded response, ready only for observation, or unable to support a requested operation. Optional unknowns remain explicit. If the host provides no pre-message initialization hook, the implementation performs the available checks before the first relevant outward response or effect and records that timing limitation.

Resumption revalidates volatile assumptions. Loading saved role text does not establish current account scope; loading an earlier success record does not establish the current resource revision. Historical state remains useful evidence, but its applicability is assessed anew.

## 5. Change, refresh and candidate intentions

### 5.1 Reconcile observations before recomputing everything

A proposed update cycle first validates scope and source, deduplicates events, compares revisions within the producer's ordering domain and retains conflicts that lack a justified precedence rule. It then invalidates affected derived records and views. Different producers' sequence numbers are not directly comparable. A later arrival does not necessarily describe a later world state.

Message receipt, action completion, timer expiry, account changes and source-health changes can all trigger this cycle. Not every trigger requires a language-model call. A heartbeat can update channel health without refreshing an old fact. A task-relevant change can require a new projection without a broad rescan.

| Trigger | Targeted response | Failure to avoid |
| --- | --- | --- |
| New message or changed goal | Reconcile task, participants and affected plan dependencies | Treating an obsolete plan as the current instruction |
| New resource revision | Update the scoped observation and invalidate dependent conclusions | Reusing a finding from an incompatible revision |
| Tool outcome | Record acknowledgement separately from observed external completion | Turning “request accepted” into “effect completed” |
| Expiry without notification | Mark the relevant record stale and schedule acquisition when needed | Treating a quiet event stream as continued truth |
| Account or permission change | Invalidate affected contexts and recheck before an effect | Carrying an earlier account's capability or authority forward |
| Restart or clock discontinuity | Reassess affected age and ordering assumptions | Accepting a negative age as unusually fresh evidence |
| Budget pressure | Preserve mandatory closure or return an explicit fit failure | Deleting a decisive exception to shorten the prompt |

For a usable common clock, observation age is \(\Delta_o(t)=t-t_{\mathrm{observed}}\). Receipt time is retained for transport analysis but does not replace observation time. A policy may accept \(0\leq\Delta_o(t)<\tau_o\), with expiry at \(\tau_o\). This is a use-specific tolerance, not proof that the world remained unchanged. Unknown clock relations and discontinuities require explicit treatment.

### 5.2 Refresh is an allocation problem

We propose a hybrid policy: relevant events invalidate dependent state promptly; deadlines and TTLs provide a backstop; consequential actions revalidate their volatile critical prerequisites. Stable artifact descriptions, rapidly changing execution status and authorization are separate classes, with profile-specific acquisition rules.

There is no scientifically justified universal “refresh every answer” interval in the reviewed material. A useful decision compares the expected reduction in decision loss from another observation with its observation, latency, model and attention costs. Such a value-of-information estimate requires a probability/loss model; without one, a deterministic priority rule is an explicitly heuristic baseline. No invented confidence percentage supplies calibration.

Observation frequency, state-reduction frequency, projection frequency and LLM invocation frequency are distinct controls. A high-rate sensor can feed a small reducer; the model may be invoked only when a meaningful state transition changes the active task. Coalescing can reduce redundant updates. An exact duplicate of an already processed revocation may be suppressed idempotently; coalescing that loses an effective stop or revocation changes the required behavior and is unacceptable.

### 5.3 Proactivity remains a separate decision

Mixed-initiative work already studies acting, asking and remaining inactive under uncertain user goals and interruption costs ([Horvitz, 1999](https://doi.org/10.1145/302979.303030)). Our proposed intention queue applies that distinction to continuing tasks. An intention may be to refresh a needed stale fact, prepare a draft, resume authorized work when a dependency arrives, ask a necessary question or wait.

An intention records why a step serves an existing goal, what evidence triggered it and when it expires. It does not create a new goal authority. The alternatives include taking no action. An uncertain external outcome is not an automatic retry grant: repeating a non-idempotent operation can duplicate its effect. Before execution, the actual system rechecks applicable permissions, target state and operation-specific controls. The paper's finite model supplies no effect dispatcher.

## 6. Bounded model-facing context

Let \(R\) be the mandatory records for the current decision and \(\operatorname{cl}(R)\) their transitive dependency closure under the declared graph. Let \(c(x)\) be the measured or explicitly abstract cost of a delivered record. A projection \(P\) is structurally feasible when

\[
\operatorname{cl}(R)\subseteq P,\qquad
\sum_{x\in P}c(x)+B_{\mathrm{instructions}}+B_{\mathrm{history}}
+B_{\mathrm{tools}}+B_{\mathrm{output}}+B_{\mathrm{margin}}\leq B.
\]

The additive costs are declared abstract estimates or conservative bounds. A real token-fit claim additionally measures the complete serialized request with the actual reader/tokenizer, including formatting and all surrounding content. Character counts and the prototype's abstract integer units are not measured tokens. A fit calculation does not establish comprehension or factual correctness.

The view normally contains the current purpose and scope, controlling constraints, relevant supported observations, unresolved critical uncertainty, immediate dependencies, evidence handles and an omission account. Bulky history can remain outside the prompt with an authorized retrieval path. A delta is usable only when its base revision is known; otherwise the receiver needs a new snapshot.

If the mandatory closure does not fit, the result is an explicit inability to provide that view at that budget. Possible next steps include a smaller subtask, structured tool evaluation, a larger permitted budget or another observation. Silent truncation is not a valid projection of the same obligations.

Lost in the Middle shows that content position affected use in the evaluated models and tasks ([Liu et al., 2024](https://aclanthology.org/2024.tacl-1.9/)). Therefore testing only whether a fact was included is inadequate. The proposed evaluation also measures whether the agent used all relevant conditions jointly, handled contradictions and produced a valid action or answer.

## 7. Conditional properties and counterexamples

The following properties concern the declared representation. They are elementary deductions, not empirical claims about agents.

**Observation-age preservation.** Assume a fixed, valid observation timestamp and compatible monotone clock. If re-reading changes only receipt time, observation age is unchanged at the same evaluation time. Thus a stale observation cannot become fresh merely by being copied into memory again. This follows directly from the age definition. It fails as an assurance about the world if the producer falsified its observation time or the clock assumptions are wrong.

**Mandatory-closure preservation.** Assume the dependency graph contains every dependency declared mandatory for this decision and the projector either includes its closure or returns a fit/readiness failure. Any successful projection retains those declared dependencies. This follows from set inclusion in the feasibility rule. The property does not establish graph completeness: an unmodeled exception can still be lost, and a model may misinterpret an included condition.

**Revision-bound use.** Assume each material prerequisite change receives a distinct, non-reused revision token scoped to its source, resource and account; the context records these exact tokens; and the effect boundary revalidates the same scoped prerequisites against an authoritative current source. Under these assumptions, a changed prerequisite cannot pass an equality-based revision check as unchanged. This is a property of exact comparison, not of a language model's explanation. A source that changes content while reusing the token violates the premise and can defeat the check. It also does not prevent a later race between check and effect; atomic conditional operations, transactions or operation-specific concurrency control are needed where that race matters.

**Conflict preservation.** If incompatible independent observations have no applicable precedence rule, retaining a conflicted state avoids asserting that the most recently received one is established truth. It does not resolve the conflict. A rule that blocks every action would satisfy many rejection checks while being useless; successful ordinary cases and unnecessary refusal are therefore essential controls.

These counterexamples limit what a passing finite implementation can establish. A fluent situational summary, correct hash, recent timestamp or large context window is individually insufficient.

## 8. Evaluation programme and evidence boundary

The companion [Context Controls study](../../engineering/studies/agent-situation-controls/STUDY.md) reports the actually executed authored finite cases and discriminating controls of a small standard-library model. Those results concern its input predicates, state transitions and projection rules. They do not establish an LLM benefit, real permissions, production deployment or independent replication.

The [engineering design](../../roadmap/agent-situation/ENGINEERING.md) separates implemented mechanisms from proposed runtime adapters. The [experiment protocol](../../roadmap/agent-situation/EXPERIMENT.md) is unexecuted and defines a coverage pilot before any confirmatory study. The principal comparator is deterministic typed state with event invalidation and fixed TTLs, retaining the same scope, conflict and mandatory-dependency guards. Weaker transcript and retrieval baselines are informative but cannot alone justify the full proposal.

Candidate outcomes include valid task completion, obsolete-value use, mandatory-condition loss, unnecessary refusal, recovery delay, observation/model calls, actually metered tokens and total maintenance cost. Matched-budget baselines share the permitted environment, model, tool availability and evidence budget. The full-history condition is separately labelled as an unequal-cost reference; its larger allowance cannot support an equal-budget efficiency claim. Task families include partial startup, reordered or missing events, changed accounts, invalidated plans, conflicting sources, context overflow and uncertain external outcomes. Condition labels should be masked for discretionary scoring, with an oracle specified separately from the agent.

No agent-comparison effect size, cost saving or production benefit is reported here. Proposed sample sizes are coverage choices until a pilot supports a separate precision or power analysis.

## 9. Limitations and development decision

The inventory is profile-dependent and cannot prove completeness. Evidence acquisition can be wrong or compromised; timestamps and identities need trustworthy producers. A deterministic reducer can preserve a mistaken observation perfectly. More observation can cost more than it helps, and aggressive refusal can hide poor utility. An LLM can misuse a correct bounded view. The proposed priority and intention policies require empirical evaluation.

Several close 2026 sources are preprints; Scroll was inspected only at abstract level. The literature pass is targeted and may omit competing architectures. The companion finite checks are author-produced, with no external-controller independence claim. Broader runtime integration, interoperability, authorization enforcement and adoption remain separate work.

The present decision is to develop this as a companion research draft within the existing Agent Application roadmap. First stabilize the typed-state and projection controls; then conduct a bounded, reproducible pilot; then revise the paper against results and separate review. A new normative representation profile should be proposed only after its semantics, interoperability and failure behavior have sufficient evidence.

## References and source scope

The [literature matrix](LITERATURE.md) gives bibliographic records, exact inspected editions and individual claim limits for all nineteen external sources. The shared [bibliography](../../reference/bibliography/BIBLIOGRAPHY.md) and [source register](../../SOURCES.md) retain publication-level attribution. External works are linked and paraphrased; their figures, datasets and full texts are not redistributed.

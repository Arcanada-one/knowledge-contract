---
title: "Situation Literature: Primary Sources and Bounded Relevance"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
status: "research-draft"
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
---

# Situation Literature: Primary Sources and Bounded Relevance

## Question and scope

This note supports [Agent Situation: Initialization, Change, and Bounded Context](PAPER.md). The bounded question is which distinctions an agent should retain about its initial situation, subsequent changes and the context selected for a particular task. It connects existing work on situation awareness, contextual systems, partial observability, embodied feedback, interactive language agents and limited memory. It does not claim that the project originated these topics or that a record of an environment is the environment itself.

## Method and access boundaries

The synthesis uses 19 selected primary-source reading records assembled on 14 November 2026. Each record supplies a named work, edition or version, primary URL, inspected location, retrieval date, intended use and limiting qualification. The integration pass preserves those records' stated access scope. Selection was targeted to the research question: there is no registered systematic-review protocol, exhaustive database search, coverage estimate, publication-bias assessment or quantitative meta-analysis. The number 19 counts records, not independent replications or evidence of completeness.

A primary-paper URL and an inspected URL have different roles. Several inspected locations are official or author-maintained project/documentation pages; their presence is not a claim that every full methods section was read. The Lin et al. Scroll record is **abstract-only**: this note uses the stated programme of a programmable context environment and model-facing projections, and excludes full-method and performance claims. ROS pages and branches are **mutable documentation**, identified by access date; no unobserved immutable snapshot or reliable publication chronology is invented. Records labelled preprint retain that status.

The note reproduces no third-party figures, datasets, source code or extended text. It cites the original works and gives concise factual paraphrases. Third-party terms remain in force, including **CC-BY-NC-ND-4.0 for Sheng et al.** The licence on this note covers the project's original prose, not the linked sources.

## Situations, context and decision-relevant uncertainty

### Endsley 1995: Toward a Theory of Situation Awareness in Dynamic Systems

Separate perception, comprehension and projection; relevant elements depend on system and goals. Human situation-awareness theory; applying it to LLM state records is our analogy. [Endsley 1995](https://doi.org/10.1518/001872095779049543).

**Recorded source:** Mica R. Endsley. Human Factors 37(1), 32–64 (1995). **Inspected:** [recorded primary or official/project location](https://frankritter.com/ist521/papers/endsley95.pdf), 2026-11-14.

### Dey and Abowd 2000: Towards a Better Understanding of Context and Context-Awareness

Identity, location, activity and time as contextual indices; relevance rather than exhaustive enumeration. The proposed extended startup inventory is not their universal checklist. [Dey and Abowd 2000](https://sites.cc.gatech.edu/fce/ctk/chiws/Dey.pdf).

**Recorded source:** Anind K. Dey; Gregory D. Abowd. CHI 2000 context-awareness workshop; also GIT-GVU-99-22 (1999). **Inspected:** [recorded primary or official/project location](https://sites.cc.gatech.edu/fce/ctk/chiws/Dey.pdf), 2026-11-14.

### Dey 2001: Understanding and Using Context

Context widgets, polling/subscription, history, interpreters and aggregation. Architectural precedent, not evidence that inferred situations are always correct. [Dey 2001](https://doi.org/10.1007/s007790170019).

**Recorded source:** Anind K. Dey. Personal and Ubiquitous Computing 5(1), 4–7 (2001). **Inspected:** [recorded primary or official/project location](https://www.cc.gatech.edu/fce/ctk/pubs/PeTe5-1.pdf), 2026-11-14.

### Kaelbling et al. 1998: Planning and Acting in Partially Observable Stochastic Domains

Retain decision-relevant uncertainty; belief updates use actions and observations. Sufficiency applies to a correctly computed belief under a specified model, not an arbitrary summary. [Kaelbling et al. 1998](https://doi.org/10.1016/S0004-3702(98)00023-X).

**Recorded source:** Leslie Pack Kaelbling; Michael L. Littman; Anthony R. Cassandra. Artificial Intelligence 101, 99–134 (1998). **Inspected:** [recorded primary or official/project location](https://people.csail.mit.edu/lpk/papers/aij98-pomdp.pdf), 2026-11-14.

## Observed capability, frames and clocks

### Huang et al. 2023: Inner Monologue: Embodied Reasoning through Planning with Language Models

Feedback-driven replanning after action failure and human task changes. Reported robot domains, detectors, prompts and skills bound the evidence. [Huang et al. 2023](https://proceedings.mlr.press/v205/huang23c.html).

**Recorded source:** Wenlong Huang et al.. CoRL proceedings, PMLR 205, 1769–1782 (2023); preprint 2022. **Inspected:** [recorded primary or official/project location](https://inner-monologue.github.io/), 2026-11-14.

### Ahn et al. 2022: Do As I Can, Not As I Say: Grounding Language in Robotic Affordances

Combine task usefulness with current skill feasibility; sponge acquisition example. Feasibility does not establish authorization. [Ahn et al. 2022](https://arxiv.org/abs/2204.01691v2).

**Recorded source:** Michael Ahn et al.. arXiv:2204.01691v2, 16 August 2022. **Inspected:** [recorded primary or official/project location](https://say-can.github.io/), 2026-11-14.

### Bongard et al. 2006: Resilient Machines Through Continuous Self-Modeling

Robot self-model adaptation from actuation and sensation after structural damage. Bounded physical capability modeling, not consciousness or general introspective accuracy. [Bongard et al. 2006](https://doi.org/10.1126/science.1133687).

**Recorded source:** Josh Bongard; Victor Zykov; Hod Lipson. Science 314(5802), 1118–1121 (2006). **Inspected:** [recorded primary or official/project location](https://meclab.w3.uvm.edu/papers/2006_Science_Bongard.pdf), 2026-11-14.

### ROS REP105: REP 105: Coordinate Frames for Mobile Platforms

Local frame can be available while global localization is unknown at startup. Official convention; digital scope analogy is proposed; repository branch is mutable. [ROS REP105](https://www.ros.org/reps/rep-0105.html).

**Recorded source:** Wim Meeussen. Official ROS informational REP, created 2010; accessed 2026-11-14. **Inspected:** [recorded primary or official/project location](https://raw.githubusercontent.com/ros-infrastructure/rep/master/rep-0105.rst), 2026-11-14.

### ROS Clock and Time: Clock and Time

Distinct clock domains, uninitialized time and backward jumps. Documentation date metadata is inconsistent; no inferred publication chronology. [ROS Clock and Time](https://design.ros2.org/articles/clock_and_time.html).

**Recorded source:** Tully Foote. Official ROS 2 design document; accessed 2026-11-14. **Inspected:** [recorded primary or official/project location](https://design.ros2.org/articles/clock_and_time.html), 2026-11-14.

### ROS QoS Jazzy: Quality of Service settings

Separate deadline, lifespan and liveliness; stale request replay can repeat effects. Transport health and freshness policies do not establish semantic truth; mutable branch. [ROS QoS Jazzy](https://raw.githubusercontent.com/ros2/ros2_documentation/jazzy/source/Concepts/Intermediate/About-Quality-of-Service-Settings.rst).

**Recorded source:** ROS 2 documentation contributors. Official ROS 2 Jazzy documentation; accessed 2026-11-14. **Inspected:** [recorded primary or official/project location](https://raw.githubusercontent.com/ros2/ros2_documentation/jazzy/source/Concepts/Intermediate/About-Quality-of-Service-Settings.rst), 2026-11-14.

## Interaction, memory and bounded projections

### Yao et al. 2023: ReAct: Synergizing Reasoning and Acting in Language Models

Interleave interaction with external observations and revised decisions. Historical models/tasks; no general freshness or authorization contract. [Yao et al. 2023](https://arxiv.org/abs/2210.03629v3).

**Recorded source:** Shunyu Yao; Jeffrey Zhao; Dian Yu; Nan Du; Izhak Shafran; Karthik Narasimhan; Yuan Cao. ICLR 2023; arXiv:2210.03629v3. **Inspected:** [recorded primary or official/project location](https://arxiv.org/html/2210.03629v3), 2026-11-14.

### Park et al. 2023: Generative Agents: Interactive Simulacra of Human Behavior

Memory retrieval, reflection and plan changes in a simulated social environment. Behavioral believability is not factual reliability or authority. [Park et al. 2023](https://arxiv.org/abs/2304.03442v2).

**Recorded source:** Joon Sung Park; Joseph C. O'Brien; Carrie J. Cai; Meredith Ringel Morris; Percy Liang; Michael S. Bernstein. UIST 2023; arXiv:2304.03442v2. **Inspected:** [recorded primary or official/project location](https://arxiv.org/html/2304.03442v2), 2026-11-14.

### Packer et al. 2024: MemGPT: Towards LLMs as Operating Systems

Manage a limited main context using external memory and paging. Does not prove semantic preservation or correct supersession of every memory. [Packer et al. 2024](https://arxiv.org/abs/2310.08560v2).

**Recorded source:** Charles Packer; Sarah Wooders; Kevin Lin; Vivian Fang; Shishir G. Patil; Ion Stoica; Joseph E. Gonzalez. arXiv:2310.08560v2, 12 February 2024; preprint. **Inspected:** [recorded primary or official/project location](https://arxiv.org/html/2310.08560v2), 2026-11-14.

### Liu et al. 2024: Lost in the Middle: How Language Models Use Long Contexts

Position affects retrieval/use of relevant content in evaluated long-context tasks. Historical model set, not a universal current failure rate. [Liu et al. 2024](https://aclanthology.org/2024.tacl-1.9/).

**Recorded source:** Nelson F. Liu; Kevin Lin; John Hewitt; Ashwin Paranjape; Michele Bevilacqua; Fabio Petroni; Percy Liang. TACL 12, 157–173 (2024). **Inspected:** [recorded primary or official/project location](https://aclanthology.org/2024.tacl-1.9.pdf), 2026-11-14.

### Wu et al. 2026: LongMemEval-V2: Evaluating Long-Term Agent Memory Toward Experienced Colleagues

Environment-specific state, workflows, gotchas and compact evidence gathering; close prior art. Pre-collected browser trajectories and fixed-reader QA; not live end-to-end task success. [Wu et al. 2026](https://arxiv.org/abs/2605.12493v1).

**Recorded source:** Di Wu; Zixiang Ji; Asmi Kawatkar; Bryan Kwan; Jia-Chen Gu; Nanyun Peng; Kai-Wei Chang. arXiv:2605.12493v1, 12 May 2026; preprint. **Inspected:** [recorded primary or official/project location](https://arxiv.org/html/2605.12493v1), 2026-11-14.

### Patel 2026: Supersede: Diagnosing and Training the Memory-Update Gap in LLM Agents

Current-value maintenance under bounded memory should be measured separately from recall. Scale sample n=25; one small-model training run; no general model-size impossibility claim. [Patel 2026](https://arxiv.org/abs/2606.27472v1).

**Recorded source:** Vedant Patel. arXiv:2606.27472v1, 25 June 2026; preprint. **Inspected:** [recorded primary or official/project location](https://arxiv.org/html/2606.27472v1), 2026-11-14.

### Lin et al. 2026: Context as an Environment: Programmatic Context Management for Long-Horizon Agents

Abstract describes a programmable context environment and printed model-facing projections. Abstract inspected only; full-method and performance claims are not used. [Lin et al. 2026](https://arxiv.org/abs/2608.21690v1).

**Recorded source:** Yin Lin; Elaine Ang; Erkang Zhu; Bolin Ding; Jingren Zhou. arXiv:2608.21690v1, 21 August 2026; preprint. **Inspected:** [abstract](https://arxiv.org/abs/2608.21690v1), 2026-11-14.

## When to ask and when environmental evidence is inadequate

### Horvitz 1999: Principles of Mixed-Initiative User Interfaces

Acting, asking and inactivity under uncertain goals and interruption costs. LookOut case study; no calibrated universal LLM utility function. [Horvitz 1999](https://doi.org/10.1145/302979.303030).

**Recorded source:** Eric Horvitz. CHI 1999, 159–166. **Inspected:** [recorded primary or official/project location](https://erichorvitz.com/chi99horvitz.pdf), 2026-11-14.

### Sheng et al. 2026: When Agents Overtrust Environmental Evidence: An Extensible Agentic Framework for Benchmarking Evidence-Grounding Defects in LLM Agents

Controlled misleading/stale environmental evidence and provenance/freshness/action-guidance failures. Stress-test incidence is not production frequency; narrow case-specific oracle. [Sheng et al. 2026](https://arxiv.org/abs/2605.08828v2).

**Recorded source:** Strick Sheng; Ziyue Wang; Liyi Zhou. arXiv:2605.08828v2, 12 May 2026; preprint. **Inspected:** [recorded primary or official/project location](https://arxiv.org/html/2605.08828v2), 2026-11-14.

## What this supports in the draft

The selected works motivate separate treatment of observations, task relevance, uncertain state, current capability, clock/frame scope, change, memory maintenance and the representation passed to a model. Bringing those distinctions into one explicit situation record is the project's proposed synthesis. The readings do not establish that this particular record is complete, that its values are correct, that a projection preserves every required distinction, or that an action is authorized. Those judgments need their own declared scope and evidence.

The proposed finite controls examine constructed state and projection rules. They can expose a failure of a declared rule within the represented cases; they cannot by themselves measure real-world observation quality, semantic annotation accuracy, language-model task success, deployment reliability or a causal advantage over a strong simple alternative. The planned LLM trial belongs to a separate protocol and should retain an unexecuted status until actual observations exist.

The close memory-management and evidence-grounding work warrants a narrow contribution statement. In particular, the draft should distinguish current-value maintenance from recall, feasibility from authority, transport freshness from semantic validity, finite model checks from live use, and an abstract's announced architecture from an inspected implementation. Any later change in these readings should identify the changed source/version and the affected claim.

## Traceability

Each work is registered under its exact `Agent Situation — …` source name in [SOURCES.md](../../SOURCES.md) and listed in the [shared bibliography](../../reference/bibliography/BIBLIOGRAPHY.md#agent-situation-state-and-bounded-context). This note is a supporting research draft, not an additional catalogue paper or a normative specification.

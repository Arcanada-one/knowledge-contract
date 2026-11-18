# Coordinated Work: Organizational Needs, Competencies, and Resource-Constrained Agent Decisions

Research programme v0.1 · 18 November 2026

This programme investigates the knowledge an agent needs to make justified recommendations about organizational work: which needs should be served, which processes constrain the outcome, which competencies and resources are required, and how an intervention affects connected activities. Its proposed theoretical direction is a theory of coordinated organizational work. Establishing a new theory requires a distinct contribution, evaluation, and review beyond this programme.

The intended capability is an agent that distinguishes a shortage of qualified people from missing materials, inaccessible equipment, unsuitable scheduling, inadequate coordination, or insufficient evidence. A recommendation should explain the need, alternatives, assumptions, expected consequences, remaining uncertainty, and conditions for reconsideration. Increasing one department's activity is useful only when assessed against the organization's obligations and the effects on connected processes.

## Relationship to Knowledge Contract

The programme builds on existing work:

- [Agent Situation: Initialization, Change, and Bounded Context](../../papers/agent-situation/PAPER.md) supplies the general treatment of initialization, changing surroundings, and bounded context.
- [Context Assembly: Retrieval, Coverage, and Context Composition under Resource Limits](../../papers/retrieval-and-context-composition/PAPER.md) supplies the existing context-composition dependency.
- [Artifact Registry](../../engineering/specifications/artifact-registry/SPECIFICATION.md) supplies the distinction between professional knowledge artifacts and their registry treatment.

The contribution proposed here is an organizational decision profile over these mechanisms. A profile name, JSON field, or convenient domain class does not establish a new native KC artifact kind. Knowledge about permission is also not permission: execution requires the current authority applicable to the action and environment.

The current output is a research programme with supporting records and a limited numerical illustration. It is not a validated theory, an accepted normative KC extension, or evidence of publication on contract.place. No publication-catalogue entry is proposed at this stage. Source acceptance, scientific review, a catalogue entry, website publication, indexing, and authorization for agent execution are separate events.

## Research position

The relevant disciplines already include workforce planning, skills-based scheduling, queueing, production control, organizational cybernetics, causal inference, and constrained optimization. [Malone and Crowston (1994)](https://doi.org/10.1145/174666.174668) already develop an interdisciplinary coordination perspective around dependencies, including shared resources, producer–consumer relationships, simultaneity, and task decomposition. Classifying dependencies or combining these disciplines is therefore insufficient as a novelty claim. Likewise, [De Bruecker et al. (2015)](https://doi.org/10.1016/j.ejor.2014.10.038) review skills in workforce planning, and [Spearman and Zazanis (1992)](https://doi.org/10.1287/opre.40.3.521) investigate bounded work in process and alternative production-control policies.

The proposed contribution concerns the transition from knowledge to a justified organizational decision. Which evidence is necessary for a decision class? How do its scope, age, provenance, and uncertainty become model assumptions and constraints? How should missing evidence restrict a recommendation? Can resulting decisions improve on strong retrieval and operations-research baselines? The novelty and value of this particular KC knowledge profile remain unestablished; both must be assessed against existing coordination theory and newer approaches.

The target is a family of models with declared applicability. Quality includes coherent units and balances, feasible assignments, demand fulfillment, controlled workload, calibrated uncertainty, and recognition of model failure. A single model that is ideal for every company is not the acceptance criterion.

## Evidence available in this revision

The [corpus manifest](corpus/corpus_manifest.json) records:

| Measure | Recorded value |
| --- | ---: |
| Input bibliographic rows | 1,177 |
| Core records checked against primary scientific or official pages | 157 |
| Candidates extracted from two review bibliographies | 1,019 |
| Retained bibliographic records | 1,176 |
| Confirmed merge | 1 |
| Same-title/year identity groups awaiting review | 26 |
| Near-title pairs awaiting review | 4 |
| Completed full-text critical appraisals | 0 |

These are record counts. The number of unique scholarly works has not been established. An abstract or selected full-text passage is not a critical appraisal of an entire paper. The bulk candidate set is concentrated in personnel scheduling literature through 2012; this retrieval history must not determine the final theory's disciplinary weighting. Modern studies and other fields require further coverage.

The numerical [flow probe](probes/README.md) has executed revision 2: 10 scenarios, 100 periods, and 190 elementary checks with zero violations. Its independent fixtures and conservation bounds support a narrow implementation claim. They do not establish agent quality, staffing effectiveness, or empirical validity for a company. In particular, zero internal WIP can coexist with unmet customer needs.

## Potential scientific series

The following 16 sections are potential papers. Each requires an independently useful question, result, evidence, and limitations; the final partition should follow the review rather than a publication quota.

| Potential paper | Main question | Engineering companion |
| --- | --- | --- |
| Research map | What is known, and which gap remains testable? | Search, screening, corpus, and claim map |
| Organizational needs | How is a gap defined relative to an objective, conditions, and time? | Faceted need representation |
| Networks of work | Which dependencies connect tasks and departments? | Typed process graph |
| Resource semantics | How can resource types be combined without losing their distinct behavior? | Units, inventories, capacity, and availability schemas |
| Professional capabilities | How do occupation, role, task, capability, and evidence relate? | Classifier mappings and competency profiles |
| System performance | What constitutes improvement of the overall system? | Metrics and local-KPI counterexamples |
| Flow coordination | When should admission be limited or capacity expanded? | Queue, buffer, and release experiments |
| Team composition | Which combination and quantity of qualifications are needed? | Joint staffing and scheduling models |
| Capability development | How should hiring, training, and automation be compared? | Ramp-up, mentoring, and investment models |
| Environment and forecasts | How do external changes affect requirements? | Probabilistic forecasts and scenarios |
| Knowledge sufficiency | Which evidence is necessary for a particular decision? | Organizational Agent Situation profile |
| Justified choice | How does knowledge support an admissible action? | Preconditions, verifier, and decision record |
| Causal evaluation | How can worker, process, and environmental effects be separated? | Attribution and intervention protocols |
| Stable control | Under what conditions are overload and harmful oscillation controlled? | Conditional results and stress tests |
| Transfer across organizations | Which conclusions remain applicable in a new setting? | Held-out organizations and industries |
| Knowledge revision | How should outcomes and counterexamples change the model? | Versioned hypotheses, rules, and evidence |

## Work sequence and deliverables

The [roadmap](plan/roadmap_steps.json) contains 72 steps in nine phases, eight steps per phase: evidence corpus; classification; organization state; flow models; workforce decisions; forecasting and shocks; agent decision contracts; evaluation; integration and publication. Each step has a deliverable, acceptance condition, and dependencies. These entries are a planning artifact; they do not assert that external tasks have been created, people assigned, or budgets reserved. Muneral remains the execution system of record.

The next priority is identity resolution, selected full-text acquisition and appraisal, and the first traceable claim cards. Classification should be tested against cases while that work proceeds. Formal models should then develop separately for production, service queues, and project work, with explicit mappings between them.

Supporting documents:

- [Review protocol](REVIEW_PROTOCOL.md): source, version, identity, extraction, and appraisal rules.
- [Model profile](MODEL_PROFILE.md): classification facets, knowledge packages, startup procedure, and conditional admissibility.
- [Experiments](EXPERIMENTS.md): falsifiable hypotheses, comparison design, validation levels, and actual probe results.

Later manuscripts belong in `papers/`, specifications in `engineering/specifications/`, and completed empirical or computational studies in `engineering/studies/`, following the repository's review and release process. Each release should state its exact scope and distinguish findings from planned work.

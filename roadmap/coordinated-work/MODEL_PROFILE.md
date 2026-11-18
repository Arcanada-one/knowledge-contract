# Decision Profile: Organizational Knowledge and Admissible Actions

**Coordinated Work · research programme v0.1**

This document proposes a domain profile over [Agent Situation](../../papers/agent-situation/PAPER.md). It preserves the existing general treatment of identity, environment, time, changing context, and authority. Domain concepts require mappings to current KC entities and versioned compatibility conditions; the following vocabulary does not create native artifact kinds.

## Sixteen classification facets

A situation is described along multiple facets. They preserve distinct questions without assuming statistical independence. Unknown values and extensions are allowed. Industry alone does not determine process topology, and a job title does not establish an individual's capability.

| Facet | Initial distinctions |
|---|---|
| 1. Scale | Organization network, company, department, site, process, operation, Work Item |
| 2. Purpose | Delivery, service, support, development, governance, assurance, research |
| 3. Work regime | Flow, batch, continuous process, project, service queue, professional or creative work, mixed regime |
| 4. Dependencies | Sequence, branching, assembly, alternative route, rework, shared capacity, joint execution |
| 5. Origin of need | Obligation, demand, forecast, failure, risk, environmental change, development, information gap |
| 6. Gap type | Quantity, qualification, quality, timing, material, access, coordination, budget, resilience |
| 7. Resource type | Material, equipment, person-hours, competency, money, energy, space, tools, data, knowledge, permission |
| 8. Resource behavior | Consumable stock, renewable capacity, shared capacity, complementarity, limited substitution, non-rival information |
| 9. Professional entity | Occupation, position, Role, competency, Skill, Blueprint, individual, team |
| 10. Competency level | Task-specific performance criteria, assessment conditions, reliability, required support, mandatory credentials |
| 11. Performance | Accepted good output, quality, timing, cost, WIP, demand fulfillment, sustainable workload, recovery |
| 12. Decision horizon | Immediate action, shift, week, tactical period, hiring/training, capital change |
| 13. Constraint | Physical, temporal, resource, quality, competency, organizational, normative, authority |
| 14. Uncertainty | Random variability, missing knowledge, conflicting sources, stale evidence, drift, structural scenario |
| 15. Intervention | Change admission, route, priority, schedule, training, staffing, procurement, equipment, automation, service terms |
| 16. Knowledge status | Observation, source assertion, computation, forecast, scenario, hypothesis; separately freshness and applicability |

Existing classifications should be mapped by purpose. The [O*NET Content Model](https://www.onetcenter.org/content.html) organizes work-related characteristics, while the [ESCO–O*NET crosswalk](https://esco.ec.europa.eu/en/use-esco/other-crosswalks) supplies mappings rather than proof of equivalent individual ability. In the KC mapping, Role describes responsibility, Skill a reusable method, competency a required or evidenced capability under conditions, and Blueprint a solution structure. These are distinct from current permission to act.

Test the facets on unseen cases using representability, annotator agreement, exceptions, unknown fields, contradictory links, and preservation of decision-relevant distinctions. A large taxonomy is not evidence of completeness.

## State, knowledge, and resource accounting

Represent the organization with a typed graph or hypergraph connecting objectives, outcomes, processes, tasks, resources, roles, actors, and evidence. Dependencies include consumption, production, precedence, joint use, assignment, constraints, and support by evidence.

Let \(x_t\) be the organization's actual state, \(K_t\) its available observations and knowledge, \(u_t\) an action, and \(w_t\) external influences. The expression

\[
x_{t+1}=F(x_t,u_t,w_t)
\]

is a modeling template, not a completed universal transition function. Production, service, and project profiles need different concrete models. Knowledge about state is not identical to state; a confident statement can still be wrong.

Inventory and queue balances account separately for arrivals, processing, transfers, losses, returns, and rejection. Resource constraints require compatible units and calendars. Materials are consumed; available working time renews under a calendar; learning changes future capability; information can be copied; authority has scope and can be revoked. These behaviors cannot share one universal conservation law.

For multiple products or task classes, represent resource consumption, substitutions, joint requirements, routing, and setup explicitly. The minimum of nominal station capacities is not a sufficient model of an arbitrary network. [Little's law](https://doi.org/10.1287/opre.9.3.383) relates appropriate averages; it does not determine staffing or guarantee queue stability.

## Conditional admissibility

Let \(\Omega(K_t)\) be the states compatible with accepted observations and assumptions; let \(\mathcal U(x)\) contain actions satisfying the represented constraints in state \(x\). Let \(\mathcal A_t\) be the action set allowed by current authority and budget. Define:

\[
\mathcal U_K(t)=
\begin{cases}
\mathcal A_t\cap\displaystyle\bigcap_{x\in\Omega(K_t)}\mathcal U(x),
&\Omega(K_t)\ne\varnothing,\\
\varnothing,&\Omega(K_t)=\varnothing.
\end{cases}
\]

If the actual state belongs to the modeled set and the represented constraints are correct, membership in this intersection ensures those constraints for the considered action. This is a conditional admissibility construction. It does not establish recursive feasibility, future constraint satisfaction under unmodeled disturbances, or stability. Those require additional transition, uncertainty, and policy assumptions, as illustrated by the separate analysis of constrained control in [Mayne et al. (2000)](https://doi.org/10.1016/S0005-1098(99)00214-9).

An empty state set indicates inconsistent accepted information; execution of the domain action fails closed until the conflict is addressed. A nonempty state set with an empty admissible-action set indicates that no action satisfies all represented requirements and authority together. Diagnostic observation or escalation needs its own valid authorization; missing evidence does not grant permission.

The intersection is a familiar conservative construction, not claimed as new mathematics. Its conservatism may make additional observations or an explicitly authorized risk model necessary. [Bertsimas and Sim (2004)](https://doi.org/10.1287/opre.1030.0065) provide relevant prior work on robustness tradeoffs. The proposed research concerns traceable grounding of state sets and constraints in versioned knowledge, and whether that grounding improves decisions.

## Twelve knowledge packages

| Package | Required content and principal checks |
|---|---|
| Objectives and obligations | Recipient of the outcome, deadlines, quality, priorities; authoritative source and current version |
| Work map | Inputs, outputs, routes, dependencies, queues; process boundaries and cross-department links |
| Demand | Requests, completed service, unserved potential, forecast; period, censoring, scenario, uncertainty |
| Resources | Type, units, stock, capacity, reserves; availability and double counting |
| Occupations and roles | Duties and tasks; applicability to this work |
| Competencies | Capability conditions, evidence, validity period; coverage and evidence quality |
| Calendar | Shifts, absence, training, mentoring; overlapping assignments and usable hours |
| Performance | Processing-time, quality, and error distributions; task mix, team, and measurement context |
| Change options | Hiring, training, procurement, automation; lag, cost, risks, and ramp-up |
| External environment | Supply conditions, labor market, demand, scenarios; source, date, fact versus assumption |
| Rules and authority | Credentials, budget, action restrictions; current scope and revocation |
| Decision history | Alternatives, outcomes, counterexamples; exact versions and transfer limits |

Each item carries its subject, source, version, event/observation times, applicability interval, knowledge status, dependencies, and units where applicable. [PROV-DM](https://www.w3.org/TR/prov-dm/) supports provenance, [ORG](https://www.w3.org/TR/vocab-org/) organizational structure, and [SHACL](https://www.w3.org/TR/shacl/) expressed data constraints. Passing a schema does not establish factual truth or execution authority.

## Seven startup and operating steps

1. Identify the organization, environment, role, request, current time, and permitted action class.
2. Select the decision profile, such as role-capacity estimation or work admission.
3. Resolve required artifacts and check scope, versions, freshness, dependencies, and conflicts.
4. Establish readiness for observation, modeling, recommendation, or the specific authorized action.
5. Construct alternatives, including the current policy, and submit constraints to an external verifier.
6. Present expected effects, evidence, uncertainty, effects on neighboring processes, and stop conditions.
7. After an authorized action, observe outcomes and revise dependent knowledge while retaining history.

The required knowledge is bounded by the decision. A missing mentor calendar or unknown quality-control capacity should yield a specific evidence request, not a fabricated hiring recommendation.

## Staffing example and decision criteria

Suppose a month requires 1,200 hours at a specified quality, current qualified capacity is 960 hours, and an additional qualified worker can supply 120 net productive hours after ramp-up. The gap is 240 hours, equivalent to the capacity of two such workers. Converting this to FTE requires an explicit full-time basis; productive capacity is not automatically a contractual staffing unit.

Even under these stated assumptions, hiring remains one option. Check skill coverage, timing, task compatibility, shared tools, materials, downstream capacity, start dates, mentoring demands, and the durability of demand. Compare training, reassignment, procurement, process changes, and service adjustments where applicable.

Set obligations before ranking alternatives. Evaluate accepted output, served demand, quality, cost, delay, workload, risk, and future capability. Authorized stakeholders define priorities and acceptable compromises. A forecast predicts, a policy chooses, and a simulator estimates consequences under assumptions; evaluate them separately. Individual causal contribution cannot be inferred from correlations between worker identity and completed-task counts; the design must address causal identification, following appropriate methods such as [Hernán and Robins](https://miguelhernan.org/whatifbook).

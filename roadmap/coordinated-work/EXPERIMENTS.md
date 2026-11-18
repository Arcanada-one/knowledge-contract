# Experiments: Hypotheses, Comparators, and Evidence Levels

**Coordinated Work · research programme v0.1**

This plan distinguishes mathematical claims, implementation checks, model validity, agent performance, and organizational effects. Each experiment must identify which level it can support. A reproducible result from a deliberately simplified model cannot establish that the model represents a company.

## Twelve testable hypotheses

Operational definitions, primary metrics, acceptable tradeoffs, and rejection rules must be registered before confirmatory comparisons. The following are starting hypotheses; their outcome is unknown.

| Hypothesis | Comparison and observation | Evidence against the claim or its scope |
|---|---|---|
| 1. The domain profile improves admissibility | Strong ordinary RAG versus the profile, with matched information and budgets | No reliable improvement, or improvement explained by extra context alone |
| 2. Cross-process dependencies reduce local harm | Local-KPI policy versus a policy using connected-process objectives | Overall service, quality, or accepted output worsens under the declared tradeoffs |
| 3. Knowledge invalidation reduces stale decisions | Same profile with and without invalidation | Stale-action frequency does not improve; separately assess update cost and false blocks |
| 4. External verification improves constraint compliance | Prompt-only constraints versus an external verifier | No compliance improvement, or increased false acceptance/rejection defeats the registered objective |
| 5. Qualification-aware staffing improves feasibility | Joint skill coverage and scheduling versus aggregate workload division | Assignments remain infeasible or gains disappear in held-out settings |
| 6. Explicit action lags improve capacity decisions | Instantaneous availability assumption versus hiring, training, and mentoring lags | Predicted capacity or service fails to improve after hidden support costs are included |
| 7. Causal constraints reduce false attribution | Cases with identifiable effects and cases with insufficient identification | Confident unsupported attribution persists or appropriate abstention fails |
| 8. Explicit uncertainty improves decision quality | Probabilistic or robust decision versus a point estimate | No benefit under a predefined quality criterion and accepted conservatism tradeoff |
| 9. Selective clarification improves utility | Clarify selectively versus always act, always ask, and a simple threshold rule | Information cost and errors yield no advantage over the simple rule |
| 10. Model rankings transfer | Predicted intervention rankings versus independently observed held-out outcomes | Effect direction or decision ranking fails within the stated transfer scope |
| 11. Control meets a declared stability criterion | Loads, delays, and disturbances inside a specified operating region | The registered stability or recovery criterion is violated |
| 12. Evidence supports independent reproduction | Repeat using fixed source, data, configuration, and model versions | Material differences lack a recorded stochastic or environmental explanation |

For hypothesis 11, a finite queue increase or bounded oscillation alone does not refute asymptotic stability. A proof of unbounded growth requires appropriate mathematical premises. Exceeding registered queue-size or recovery-time limits in a finite trial refutes that operational criterion. These are different claims and must remain separate.

## Baselines, ablations, and design

Include the current human or simple organizational method, a well-tuned operations-research method, an LLM without retrieval, an LLM with strong ordinary RAG, and the complete KC profile. Provide comparable available information, computational and observation budgets, tool permissions, and reporting of failures. Disclose differences inherent to a treatment, rather than calling unequal information access an architecture effect.

Ablate process dependencies, freshness handling, uncertainty, competency evidence, and the external verifier separately. Account for interactions among components. A weak prompt or an untuned solver is not a sufficient control for a claim about knowledge contracts.

Primary outcomes include accepted good output, served and unserved demand, WIP, delay, quality, constraint violations, cost, human workload, agent cost, false refusals, and uncertainty calibration. Choose a primary decision criterion before examining results. Keep failures, timeouts, and unsuccessful attempts in the appropriate denominator. Determine sample sizes from meaningful effect sizes and dependence between observations; multiple runs of one scenario are not independent organizations.

Use three structurally distinct model families: production flow; service queues with multiple qualifications; and project work involving development, review, testing, and support. Renaming a factory station as a department does not create an independent service-domain test. Hold out organizations, task distributions, and environmental regimes where transfer is claimed. Prevent leakage from future outcomes into knowledge snapshots and forecasts.

For causal organizational effects, account for shared resources and spillovers between departments. Shadow-mode recommendations can test plausibility or forecasting, but cannot alone identify the effect of an intervention that was not performed. Observational comparisons require an explicit identification argument. Employee evaluation must distinguish individual actions from task mix, tooling, collaboration, and environmental constraints.

## Evidence levels

Progress through schema and invariant checks; conditional mathematical results; independently checked simulations; retrospective real data with time-respecting splits; shadow operation; a limited field pilot; and external reproduction. Advancement depends on the claim and its risks, not on a mechanical completion badge.

As emphasized by [Sargent (2013)](https://doi.org/10.1057/jos.2012.20), conceptual-model validity, data validity, operational validity, and implementation verification require distinct attention. A correct implementation can instantiate an unsuitable model. A helpful simulation policy can fail when the real process has omitted constraints.

## Executed flow probe: revision 2

The [probe README](probes/README.md) describes the reproduction commands and files. Revision 2 executed 10 scenarios for 10 periods each, producing 100 period records. Its verifier reports 190 elementary checks with zero failures. Revision 1 remains preserved with its inputs, code, results, and hashes; revision 2 adds explicit unserved-demand accounting and records its origin.

The model is a deterministic three-stage fluid line with one homogeneous good, zero initial inventories, constant inputs, unlimited buffers, and zero transit lag. Nominal processing capacity, availability, and work content are distinct. Supply is an availability ceiling. Demand is potential need / maximum customer acceptance per period; its unserved portion is measured but does not become a customer-order backlog. Admission limits are supplied by the experimenter, not selected by an agent or optimizer.

| Case | Material per period | Admission limit per period | Nominal capacities | Potential demand per period | Shipped to customer per period | End-of-run inventory or total unserved potential |
|---|---:|---:|---|---:|---:|---|
| Admit 80 | 80 | 80 | 100 / 60 / 90 | 70 | 60 | WIP 200; unserved 100 |
| Admit 60 | 80 | 60 | 100 / 60 / 90 | 70 | 60 | WIP 0; unserved 100 |
| Expand stages 1 and 3 | 80 | 80 | 160 / 60 / 180 | 70 | 60 | WIP 200; unserved 100 |
| Expand stage 2 to 85 | 80 | 70 | 100 / 85 / 90 | 70 | 70 | WIP 0; unserved 0 |
| Raise demand to 100 | 80 | 80 | 100 / 85 / 90 | 100 | 80 | WIP 0; unserved 200 |
| Admit 80 with demand 50 | 80 | 80 | 100 / 85 / 90 | 50 | 50 | Finished goods 300; unserved 0 |

In the last row, stage 3 produces 80 but only 50 are shipped each period. Shipment and physical production are intentionally distinguished. The remaining cases test a stage-3 bottleneck, fixed setup availability loss, fixed additional rework workload, and zero material availability.

With zero initial inventory and no scrap, every shipped unit must cross every stage. If supply is \(S\), acceptance is \(D\), nominal stage capacity is \(c_i\), availability is \(a_i\), and work per good unit is \(w_i\), conservation gives:

\[
Y(T)\le T\min\left(S,D,\frac{c_1a_1}{w_1},\frac{c_2a_2}{w_2},\frac{c_3a_3}{w_3}\right).
\]

This is a bound under the stated assumptions. The analytical module computes it independently of the simulator. Manual expected fixtures are also separate from the simulation output. The verifier checks balances, resource limits, reported totals, and potential-demand accounting. These checks can detect implementation inconsistencies without proving empirical representativeness.

The principal counterexample is explicit: admitting 60 eliminates internal accumulation but still leaves 10 potential units unserved per period when demand is 70. Zero WIP does not establish demand fulfillment, sufficient staffing, or organizational stability. Similarly, setup loss or additional work per item can make nominal capacity overstate deliverable capacity.

No measured benefit of KC, agent choice, hiring policy, or real-company control follows from this probe. Its purpose is a reproducible starting point with visible assumptions and counterexamples. Subsequent work must add nonzero processing times, finite buffers, uncertain arrivals, multiple products, shared resources, customer-backlog dynamics, and independent data before claims at broader evidence levels are evaluated.

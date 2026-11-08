---
name: "knowledge-utility"
title: "Knowledge Utility: Resource Accounting, and Lifecycle Decisions"
short_title: "Knowledge Utility"
subtitle: "Resource Accounting, and Lifecycle Decisions"
previous_title: "Knowledge Utility, Resource Accounting, and Lifecycle Decisions"
artifact: "scientific-paper"
edition: "1.1"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "Task-relative benefit, complete resource accounting, comparison baselines and limits of causal inference."
---

<!-- markdownlint-disable-next-line MD033 -->
<a id="knowledge-utility-resource-accounting-and-lifecycle-decisions"></a>

# Knowledge Utility: Resource Accounting, and Lifecycle Decisions

**Author:** Pavel Valentov · **Publication edition:** 1.1

## Abstract

Knowledge is useful relative to a task, recipient, policy, time horizon, and alternative. Truth, evidence quality, popularity, and utility therefore cannot be represented as one interchangeable score. This paper defines conditional utility and separates measured outcomes, predicted benefit, resource costs, and causal attribution. It gives conservation conditions for shared-cost allocation, shows why complementary contributions are generally nonadditive, and derives a restricted break-even condition for prepared knowledge. Lifecycle decisions are framed in terms of future marginal value subject to mandatory constraints, while storage retention remains distinct from residency and current eligibility. The contribution is an accounting and evaluation model that prevents common forms of double counting and unsupported attribution. It does not supply universal weights, prices, retention thresholds, or empirical claims that structured knowledge is always beneficial. Those quantities require explicit measurement under a stated intervention and comparison policy.

**Keywords:** knowledge utility; causal attribution; resource accounting; marginal value; retention; reuse economics.

## 1. Research question

A fact can be true and irrelevant to a task. A false claim can be useful as an object of investigation without becoming true. An expensive artifact can be worth retaining, while a frequently retrieved one can add little to outcomes. These cases show why “knowledge value” is not a permanent intrinsic score.

We ask: **how should a system assess the contribution and cost of knowledge without confusing truth, exposure, attribution, and usefulness?** The model below treats value as conditional and preserves the units and assumptions of each assessment.

The causal distinction is central. An observed association between access to an artifact and a good outcome does not alone identify the artifact's effect. Causal inference requires assumptions connecting observed data to the intervention being assessed [1]. Our contribution is to carry that discipline into knowledge selection, prepared-artifact reuse, and retention accounting.

## 2. Conditional utility and outcome vectors

For knowledge artifact \(k\), write

\[
V(k\mid q,c,\pi,h,b,r),
\]

where \(q\) is the task or task distribution, \(c\) the consumer and context, \(\pi\) the use and evaluation policy, \(h\) the observation horizon, \(b\) the baseline, and \(r\) the pinned artifact and policy revisions. These conditions are part of the claim. Changing them can change the value being estimated.

An outcome can be a vector: task quality, consumer effort, latency, uncertainty reduction, prevented harm, introduced harm, and future usefulness. Each component needs a definition, unit, observation method, and treatment of missing data. Predicted benefit, measured outcome, and unresolved assessment must remain distinct. Unknown is not zero.

A scalar score is legitimate only with an explicit mapping \(U\) from the outcome vector to a declared scalar scale. That mapping includes weights, trade-offs, and any monetary conversions. Different stakeholders can legitimately choose different mappings. Where no justified common scale exists, a partial comparison such as Pareto dominance is more informative than an unexplained total ranking. Subsequent comparisons keep \(U\) and the conditioning arguments fixed unless a policy change is explicitly being assessed.

Costs must be included once. One can define a net utility that already contains resource penalties, or subtract a separate cost measure from a gross benefit measure. Subtracting the same cost again produces an accounting error. A new weight or tariff policy creates a new assessment, rather than silently rewriting the meaning of an earlier score.

Truth, evidential support, source quality, applicability, and utility remain separate axes. Utility does not authorize a false factual claim, and low utility does not refute a proposition. These distinctions permit honest evaluation of investigation, correction, and rarely needed knowledge.

## 3. Resource accounting

A resource ledger records the operations that actually consume resources. Depending on the system, these can include input and output tokens, processor time, elapsed time, human effort, storage over time, network transfer, index updates, checks, retries, and reconstruction after eviction. The measurement unit and scope must be explicit.

Elapsed latency is not generally the sum of parallel operation durations. Logical artifacts are not physical replicas. A node count is not a monetary cost without a model connecting it to resources. Monetary amounts require a tariff revision, currency, date, and allocation policy. Billed, estimated, and predicted costs should not be merged into one unlabeled total.

A retry can incur real additional cost; a duplicated telemetry event does not. Stable event identity with payload-conflict handling separates these cases. Tokens, their priced estimate, and the corresponding invoice line are different views of a cost, not three independent charges.

### Proposition 1. Conservative shared-cost allocation prevents creation of cost

Let \(\mathcal E\) be a finite set of measured operations in one accounting scope and unit. For each operation \(e\), let its nonnegative cost \(c_e\), nonnegative consumer allocations \(a_{e,1},\ldots,a_{e,n_e}\), and nonnegative unallocated residual \(u_e\) satisfy

\[
\sum_{i=1}^{n_e}a_{e,i}+u_e=c_e.
\]

If every underlying operation and each of its allocated and residual parts are included exactly once, then

\[
\sum_{e\in\mathcal E}\left(\sum_{i=1}^{n_e}a_{e,i}+u_e\right)
=\sum_{e\in\mathcal E}c_e.
\]

**Proof.** Sum the per-operation equalities over \(\mathcal E\). Nonnegativity also gives \(a_{e,i}\leq c_e\) and \(u_e\leq c_e\) for every component, so an allocation cannot hide an excessive charge behind a negative share. ∎

The result is an accounting identity, not a uniquely fair allocation rule. It requires a closed accounting scope. Omitting shared infrastructure or counting the same event in two ledgers defeats the premises.

## 4. Contribution and causal attribution

Events such as found, selected, delivered, consumed, cited, and accepted describe different stages. A citation does not show that the cited artifact caused the outcome. Acceptance of a Work Item does not establish the separate usefulness of every attached source.

Let \(Y_w(\pi+k)\) denote the outcome for task \(w\) under a policy that offers artifact \(k\), and \(Y_w(\pi)\) the outcome under the same policy without that intervention. With the scalar mapping \(U\) from §2 and a fixed task distribution \(\mathcal D\), the artifact-specific contribution target is

\[
\Delta V(k)=\mathbb E_{w\sim\mathcal D}
\left[U(Y_w(\pi+k))-U(Y_w(\pi))\right].
\]

The policies differ only in access to \(k\) and its predeclared consequences. A comparison against a different baseline policy \(\pi_b\) is also meaningful, but estimates the whole policy contrast. If the new condition changes the model, review budget, interface, or task selection as well, attributing that contrast specifically to \(k\) requires additional identification. The conditioning arguments of §2 remain fixed in the displayed shorthand.

The expression defines a target; it does not identify it from arbitrary logs. Randomized assignment, paired task designs, or observational adjustment each require their own assumptions about assignment, interference, support, measurement, and the relevant population. Unrecorded selection effects can make a frequently used artifact appear beneficial because it is offered on easier tasks.

Observation, association, prediction, and causal estimate must therefore be labeled separately. A model's predicted gain can guide exploration but cannot be reported as an observed effect. The observation horizon also matters: immediate completion, delayed retention, and later reuse are different outcomes.

## 5. Complementarity, duplication, and exposure

Write \(V_{\mathrm{set}}(S)\) for the utility assessment of offering an artifact set \(S\), with all conditions from §2 fixed. This set function is distinct from the single-artifact notation \(V(k\mid q,c,\pi,h,b,r)\); its singleton values refer to the same assessed single-artifact interventions. Set utility need not equal the sum of its members' utility. Consider a rule and its necessary condition. Neither alone is useful for the permitted task, but the pair is. If

\[
V_{\mathrm{set}}(\varnothing)=V_{\mathrm{set}}(\{a\})=V_{\mathrm{set}}(\{b\})=0,
\qquad V_{\mathrm{set}}(\{a,b\})=1,
\]

then each leave-one-out contribution within the pair is one. Summing those contributions yields two, although the total gain is one. Marginal contribution therefore depends on the reference set, and summing several margins can double-count complementary value.

Redundant copies create a different problem. Splitting one informational artifact into multiple identifiers should not automatically create multiple independent contributions. Attribution requires a declared identity and coalition policy. An allocation rule can distribute a defined total; it cannot discover unobserved outcomes or establish a uniquely fair reward by itself.

Use frequency needs exposure and opportunity denominators. Low use can reflect narrow applicability, limited demand, poor retrieval, restricted access, or an immature observation period. If a ranking system suppresses artifacts with few uses, new artifacts may receive no opportunity to demonstrate value. This is a possible feedback mechanism, not proof that every ranking system exhibits it.

Evaluation can address the problem through a declared exploration budget, independent task samples, and separate reporting for new and mature artifacts. Such choices are policy decisions with costs and assumptions, not universal constants.

## 6. Reuse economics and lifecycle decisions

### Proposition 2. A simple reuse policy has a conditional break-even point

Suppose a valid cold execution costs \(G\) per request. Preparing an equally acceptable reusable artifact costs \(B\) once, and each admitted reuse costs \(c_{\mathrm{hit}}\), including its required checks. These costs are nonnegative and measured in the same unit over a fixed horizon \(h\). With \(N\geq1\) requests, no intervening invalidation, and no other costs, reuse is cheaper exactly when

\[
B+Nc_{\mathrm{hit}}<NG,
\quad\text{equivalently}\quad
N(G-c_{\mathrm{hit}})>B.
\]

**Proof.** Compare the total costs and rearrange the inequality. If \(G\leq c_{\mathrm{hit}}\), a positive preparation cost cannot be recovered under these assumptions. ∎

This result is deliberately narrow. In the [companion study's accounting model](../../engineering/studies/reuse-admission-and-cost-controls/STUDY.md), it is the special case with hit fraction \(\rho=1\), no rebuilds or additional invalidation and storage costs (\(M=I=S=0\)), and \(c_{\mathrm{hit}}=c_v+c_r\), where \(c_v\) is per-request validation and \(c_r\) is additional hit-path cost. Both formulas use the same horizon and cost scope. Storage, invalidation, rebuilding, coordination, failed attempts, and changing demand can alter the calculation. The two routes must satisfy the same relevant acceptance conditions; omitting required checks is not an economic improvement under that contract.

Lifecycle choices concern future marginal benefits, future costs, switching costs, and mandatory constraints. Past acquisition cost belongs in the historical ledger; a large historical expenditure does not by itself justify continued expensive residency.

**Retention** is the storage policy governing preservation or deletion of bytes. **Residency** concerns where those retained bytes are available, including whether reconstruction is needed. Search visibility, background preparation, and current-use eligibility are separate lifecycle decisions. Archiving a retained original, removing it from search, and withdrawing permission to use it therefore have different effects. A rarely used artifact may be necessary for reproducibility or a critical deadline. A negative utility estimate does not alone authorize destroying the only retained original.

Residency policies can use measured demand and rehydration cost, with hysteresis to avoid repeated switching. Thresholds must be calibrated to the workload and constraints. Popularity cannot override revocation, known corruption, or a mandatory scope restriction. The [controlled reuse paper](../controlled-knowledge-reuse/PAPER.md) defines admission before economic ranking.

## 7. Evaluation and falsification

A utility study should predeclare the task distribution, baseline, intervention, outcome rubric, horizon, resource scope, and treatment of unknown outcomes. It should record opportunity to use the knowledge, actual exposure, and downstream consumption separately. An ablation must remove the intended contribution without silently changing unrelated parts of the system.

Useful negative controls include repeated telemetry with one real operation, complementary artifacts whose summed margins overstate total gain, identical knowledge under multiple identifiers, and a policy change bundled with artifact access. Each reveals a specific attribution or accounting error.

For lifecycle policies, evaluation should include rare mandatory tasks, bursts of demand, changes of source state, and reconstruction after eviction, while measuring storage retention, residency, and eligibility separately. Results should state whether costs are observed or modeled and whether the policy was tuned on the same workload. A successful finite control does not establish optimal retention or residency for every future demand pattern.

The results of this paper are a conditional evaluation model, conservation and break-even properties, and counterexamples to additive or popularity-based shortcuts. No universal utility score or measured economic superiority is asserted. The [reuse admission and cost controls study](../../engineering/studies/reuse-admission-and-cost-controls/STUDY.md) contains finite admission counterexamples and exact cost arithmetic on synthetic inputs; it reports no measured model savings or production workload. The [editorial skill pilot](../../engineering/studies/editorial-skill-pilot/STUDY.md) supplies a separate exploratory comparison of document outputs, without a cost estimate.

The shared [glossary](../../reference/glossary/GLOSSARY.md) and [evidence and falsification paper](../evidence-and-falsification/PAPER.md) define the corresponding claim and measurement boundaries.

## References

1. Pearl, J. “Causal Inference in Statistics: An Overview.” *Statistics Surveys* 3, 2009, 96–146. <https://doi.org/10.1214/09-SS057>

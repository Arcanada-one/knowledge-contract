---
title: Retrieval-context finite verification results
sources: ["Knowledge Contract project corpus and publication edition", "Nemhauser Wolsey Fisher 1978"]
status: measured locally; synthetic bounded verification
---

# Retrieval-context finite verification results

Exact deterministic output of the [checker](../../tools/verify_retrieval_context.py), executed with Python 3.13.5. Read the [scope and interpretation](REVIEW.md) before citing counts. These are new finite abstract checks, not empirical agent trials or a production conformity result. The candidate hash is inside the record. No independent review, general theorem proof by enumeration, full repository CI or deployment is implied.

```json
{
  "boundaries": {
    "checks": {
      "alternative_valid_group_suffices": true,
      "complete_infeasibility_has_declared_scope": true,
      "cyclic_closure_terminates": true,
      "dependency_root_removal_not_delivery_removal": true,
      "early_stop_with_incumbent_not_optimal": true,
      "early_stop_without_incumbent_is_incomplete": true,
      "format_overhead_can_break_budget": true,
      "full_delivery_passes": true,
      "invalid_group_not_passed": true,
      "joint_group_needs_both": true,
      "joint_support_violates_diminishing_returns": true,
      "mandatory_coverage_not_downward_closed": true,
      "missing_dependency_rejected": true,
      "shared_dependency_charged_once": true,
      "truncated_exception_rejected": true,
      "unknown_group_not_passed": true,
      "vector_budget_not_compensated_by_other_units": true
    },
    "deliberate_faulty_alternatives_distinguished": {
      "adds_incommensurate_budgets": true,
      "closure_only_accepts_truncated_delivery": true,
      "double_counts_shared_dependency": true,
      "early_stop_called_infeasible": true,
      "ignores_render_overhead": true,
      "unknown_treated_as_valid": true
    },
    "mutation_scope": "six explicit faulty alternatives in this abstract harness, not production code mutations",
    "passed": 17,
    "total": 17
  },
  "candidate_sha256": "e457fadcb17424e15083504a2babb2646aedc8aec7370048cd77854a8c7af64f",
  "document": {
    "checks": {
      "classical_result_attribution": true,
      "conclusion_present": true,
      "delivered_support_explicit": true,
      "display_math_exact_order": true,
      "exact_candidate": true,
      "front_matter_exact": true,
      "greedy_finite_domain": true,
      "joint_ground_counterexample_exact": true,
      "no_incumbent_without_candidate": true,
      "no_placeholders": true,
      "old_headings_preserved": true,
      "one_title": true,
      "original_inline_math_exact_order": true,
      "original_links_exact_order": true,
      "original_title": true,
      "proposition_1_exact": true,
      "proposition_2_exact": true,
      "proposition_3_exact": true,
      "references_exact": true,
      "separate_verification_note": true,
      "utf8_lf_final_newline": true,
      "vector_budget_componentwise": true
    },
    "pass": true,
    "passed": 22,
    "total": 22
  },
  "greedy": {
    "all_tie_resolutions_checked": true,
    "arithmetic": "exact rational cardinality bound",
    "carrier": "3 selectable sets over 3 features; all 512 incidence matrices; two nonnegative weight profiles",
    "distinct_value_outcomes_across_instances": 3072,
    "instances": 3072,
    "limit": "weighted coverage subclass only, not all submodular functions or knapsack policies",
    "unit": "incidence/weight/cardinality instance",
    "violations": 0
  },
  "not_established": [
    "general proofs by enumeration",
    "semantic annotation correctness",
    "production selector conformance",
    "human comprehension",
    "editorial superiority",
    "repository-wide CI",
    "site deployment"
  ],
  "pass": true,
  "record_type": "retrieval-context-finite-verification/1",
  "selection": {
    "carrier": "3 revisions; 64 loop-free directed graphs (cycles allowed); two nonempty conjunctive groups",
    "cost_profile": "revision costs (1,2,3); fixed overhead 0 or 1; scalar budget 0..7; identity render",
    "disagreements_with_closed_set_oracle": 0,
    "feasible_instances": 11328,
    "infeasible_instances": 38848,
    "instances": 50176,
    "root_decisions_per_instance": 8,
    "unit": "graph/group-pair/overhead/budget instance"
  },
  "source_sha256": "6ebbb43bcdd09ba44b60d6b0e4fce9ec05dcd1550f1d8c43bf451379508b6773"
}
```

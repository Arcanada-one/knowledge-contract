---
title: "Transformation and Context Clarity: Synthetic example results"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
sources: none
status: "author-run finite examples; not independent acceptance"
---

# Transformation and Context Clarity: Synthetic example results

Original synthetic examples prepared by KC-Brain under Pavel Valentov's publication instruction. The [script](../../tools/check_transformations_context_editorial.py) is licensed Apache-2.0; this explanatory record is CC BY 4.0. No external dataset, source-book content or third-party program is incorporated.

The six groups passed in the assistant's local container. The JSON below preserves the expected and observed values with normalized formatting. The earlier candidate stored these same data in `example-checks.json` and the same program as `reviews/transformations-context-editorial/check_examples.py` at `d0b2c18ca16c0b78bb0f93c075b826f4555f20e5`. Moving the unchanged program to the established `tools/` directory and wrapping the result in a source-declared Markdown record changes neither the observations nor the code hash. This is not a historical study update, production test, formal proof, source-acceptance receipt or deployment.

```json
{
  "scope": "new_finite_synthetic_editorial_examples",
  "effects_authorized": false,
  "script_sha256": "290e54b164565eb0629a1128e17ed635cecbc1327a62e2241079579568a8e5b4",
  "case_groups": 6,
  "passed_groups": 6,
  "cases": [
    {
      "id": "E01-state-versus-observation",
      "expected": {"state_paths": [[0, 0, 0], [1, 1, 1]], "within_step_preservation": true, "endpoint_observations_equal": [false, false]},
      "observed": {"state_paths": [[0, 0, 0], [1, 1, 1]], "within_step_preservation": true, "endpoint_observations_equal": [false, false]},
      "pass": true,
      "scope": "Two Boolean states; two identity transitions; mismatched observation interface."
    },
    {
      "id": "E02-universal-output",
      "expected": {"positive_all_preserve": true, "favorable_sample_preserves": true, "all_branching_outputs_preserve": false},
      "observed": {"positive_all_preserve": true, "favorable_sample_preserves": true, "all_branching_outputs_preserve": false},
      "pass": true,
      "scope": "Two explicitly enumerated finite relations; a favorable sample is not universal preservation."
    },
    {
      "id": "E03-precondition-boundary",
      "expected": [[0, false, false], [1, true, true]],
      "observed": [[0, false, false], [1, true, true]],
      "pass": true,
      "scope": "Identity followed by constant-one; columns are input, second precondition, endpoint equality."
    },
    {
      "id": "E04-coherent-snapshot",
      "expected": {"union_covers": true, "one_incompatible_snapshot_covers": false, "one_compatible_snapshot_covers": true},
      "observed": {"union_covers": true, "one_incompatible_snapshot_covers": false, "one_compatible_snapshot_covers": true},
      "pass": true,
      "scope": "Two requirements; two incompatible fixed snapshots and a positive coherent snapshot."
    },
    {
      "id": "E05-intact-unit-cost-cover",
      "expected": {"comparisons": 32, "equal": true},
      "observed": {"comparisons": 32, "equal": true},
      "pass": true,
      "scope": "Eight subsets of three packages, budgets 0..3; literal intact payload and one cost unit per package."
    },
    {
      "id": "E06-lossful-delivery-control",
      "expected": {"candidate_covers": true, "delivered_covers": false, "declared_unit_cost": 2},
      "observed": {"candidate_covers": true, "delivered_covers": false, "declared_unit_cost": 2},
      "pass": true,
      "scope": "The same covering selection at budget two, with one required delivered coordinate deliberately removed."
    }
  ],
  "limits": "Not a proof, historical replay, semantic extraction evaluation, repository-wide test suite, model trial, or production admission."
}
```

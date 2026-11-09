---
title: "Meaning Geometry: Exact finite verification results"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
sources: none
status: "author-run synthetic checks; not independent acceptance"
---

# Meaning Geometry: Exact finite verification results

These original cases were designed and executed by KC-Brain under Pavel Valentov's instruction on 9 November 2026. They contain no external dataset, model call or server workload. The script uses Python's standard library and exact rational arithmetic. Run `python3 -B tools/check_meaning_geometry.py` from the repository root.

The full stdout below is preserved from the local Python 3.13.5 execution. Exit status was 0. Eight groups passed. Counts identify distinct finite domains and must not be added as independent trials. In particular, the 4,096 labelled-object triples and the 4,096 before/after observation quadruples are different spaces, neither a historical graph replay nor a production benchmark. Literal countermodels and positive cases are both present.

```json
{
  "scope": "finite synthetic checks of the declared observation geometry",
  "python": "3.13.5",
  "script_sha256": "4235ac9e8f7f97d6a361247e0f71d13c3fb4fbd0af7e5f4ef5be787c4e053ff7",
  "groups": [
    {
      "name": "Observation pseudometric and quotient",
      "counts": {
        "objects": 16,
        "observation_classes": 8,
        "ordered_pairs": 256,
        "ordered_triples": 4096
      },
      "result": "pass",
      "details": {}
    },
    {
      "name": "Restriction and normalization",
      "counts": {
        "nonempty_coordinate_subsets": 7,
        "pair_subset_comparisons": 448
      },
      "result": "pass",
      "details": {
        "full": "1/2",
        "normalized_restriction": "1"
      }
    },
    {
      "name": "Observation refinement",
      "counts": {
        "ordered_pair_comparisons": 64
      },
      "result": "pass",
      "details": {
        "alpha": "1/3"
      }
    },
    {
      "name": "Transformations and representation collisions",
      "counts": {
        "isometry_pairs": 256,
        "representation_fibres": 4
      },
      "result": "pass",
      "details": {
        "domain_saturation_counterexample": true,
        "hidden_bit_not_recoverable": true
      }
    },
    {
      "name": "Incomplete observations",
      "counts": {
        "domain_pairs": 81,
        "completion_pair_evaluations": 256,
        "joint_constrained_pairs": 2
      },
      "result": "pass",
      "details": {
        "independent_unknown_range": [
          "0",
          "1"
        ],
        "joint_actual_maximum": "0",
        "empty_set_refused": true
      }
    },
    {
      "name": "Similarity countermodels",
      "counts": {
        "threshold_triples": 1,
        "cosine_triples": 1,
        "boolean_valuations": 4
      },
      "result": "pass",
      "details": {
        "threshold_distances": [
          "1/2",
          "1/2",
          "1"
        ],
        "cosine_distances": [
          "1/2",
          "1/2",
          "3/2"
        ],
        "entailment_strictly_directed": true
      }
    },
    {
      "name": "Distance does not grant knowledge or authority",
      "counts": {
        "gate_counterexamples": 1,
        "unknown_marker_counterexamples": 1
      },
      "result": "pass",
      "details": {
        "gate_distance": "1/100",
        "recorded_unknown_distance": "0",
        "possible_latent_distance": "1"
      }
    },
    {
      "name": "Aligned context changes",
      "counts": {
        "ordered_before_after_quadruples": 4096
      },
      "result": "pass",
      "details": {}
    }
  ],
  "passed_groups": 8,
  "limits": "Exact rational examples, not a proof, independent review, semantic annotation validation, embedding benchmark, live-agent test, production execution or publication admission."
}
```

## Parsing observation

Pandoc 3.1.11.1 parsed the complete manuscript into a Markdown AST: one H1, 19 total headings with unique identifiers, 98 mathematical nodes including 17 displayed formulas. This is a local parser observation, not the repository's required Pandoc 3.1.3 check, HTML/MathML acceptance, visual PDF review or site deployment. No PDF was generated.

## Identity and limits

Manuscript SHA-256: `7a7e700bcccb7387ff5aaa7058ffe3f673c89c18793afe28a5a23abaa429d7e5`; Git blob: `74a9526e1aa0ed92f2ded13b4e6b45bb5f6f2339`; size: 26,431 UTF-8 bytes. Checker Git blob: `74fb9d011ce4a99051ded4993c28c2a4b8575421`. The exact executed checker SHA-256 is in stdout above. The separate proof text, observed finite cases and future model-specific measurements are different evidence classes. No separate reviewer, source admission, indexing or production conformance is asserted.

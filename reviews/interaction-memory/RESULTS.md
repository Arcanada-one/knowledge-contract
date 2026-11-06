---
title: Interaction and memory bounded-check results
sources: none
status: measured local abstract checks
---

# Measured bounded-check results

The producer ran `tools/verify_interaction_memory.py` against the exact candidate named below using Python 3.13.5. These are newly constructed abstract-model checks, not historical experiment reruns, concurrent database tests or independent scientific review. The retained output was reproduced byte for byte in a second run. The complete scope and caveats are in [REVIEW.md](REVIEW.md).

The verifier source SHA-256 at this observation is `2b3c432cdbe796178d5795ac983339bb98c38de45939163c14a4644a558a0431`.

```json
{
  "controls": {
    "boundary_checks": {
      "abort_before_atomic_commit_no_effect": true,
      "current_use_distinct_from_retention": true,
      "duplicate_returns_same_result": true,
      "equal_generation_other_task_denied": true,
      "exact_reassessment_passes_identity_gate_only": true,
      "failed_reassessment_denied": true,
      "lost_response_after_commit_replay_no_effect": true,
      "namespace_distinguishes_identifier": true,
      "old_generation_denied": true,
      "payload_conflict_rejected": true,
      "quoted_act_does_not_inherit_authority": true,
      "representation_scope_not_label_only": true,
      "same_generation_selection_not_solved": true,
      "source_check_not_output_check": true,
      "unknown_memory_condition_not_pass": true,
      "wrong_output_reassessment_denied": true
    },
    "boundary_passed": 16,
    "boundary_total": 16,
    "limit": "constructed observations and deliberately weaker rules; not observed production defects",
    "mutant_distinguishing_witnesses": {
      "content_hash_instead_of_generation": true,
      "forgetting_record_before_replay": true,
      "generation_without_work_item_identity": true,
      "local_journal_as_external_exactly_once": true,
      "missing_first_commit_serialization": true,
      "reassessment_without_output_identity": true,
      "split_check_and_publish": true,
      "unmodeled_semantic_coupling": true
    },
    "mutants_distinguished": 8,
    "mutants_total": 8,
    "pass": true
  },
  "document": {
    "bytes": 22061,
    "checks": {
      "candidate_exact": true,
      "captioned_layer_table": true,
      "conclusion": true,
      "evidence_section_preserved": true,
      "external_effect_limit": true,
      "formal_section_preserved": true,
      "front_matter_preserved": true,
      "lf_final_newline": true,
      "links_preserved": true,
      "math_preserved": true,
      "no_measured_learning_claim": true,
      "no_placeholders": true,
      "no_private_mail_payload": true,
      "old_major_headings": true,
      "one_h1": true,
      "output_bound_reevaluation": true,
      "references_preserved": true,
      "retention_scope": true,
      "same_generation_limit": true,
      "source_cited": true,
      "three_propositions": true,
      "utf8_without_bom": true
    },
    "pass": true,
    "passed": 22,
    "sha256": "6bf13bff5230129c4f077515015f2926c65f6fb2d97f3e1d61e5eaa6b584a2c8",
    "total": 22
  },
  "event_replay": {
    "carrier": "two stable event identifiers, two canonical integer payloads, serialized histories of length 0..6",
    "handled_event_occurrences": 30948,
    "histories": 5461,
    "limit": "atomicity is an assumed model step; no concurrent database implementation was tested",
    "pass": true,
    "violations": 0
  },
  "frame": {
    "carrier": "three Boolean state components, every write-set subset, every Boolean observation on its complement",
    "observation_cases": 3328,
    "pass": true,
    "scoped_transitions": 216,
    "violations": 0
  },
  "generation": {
    "carrier": "two Work Items; binary requirement contents; 1..5 non-reissued generations; two output identities",
    "direct_admission_cases": 1032,
    "earlier_same_task_cases": 392,
    "history_count": 62,
    "old_content_matches_active_cases": 196,
    "pass": true,
    "synthetic_assessment_binding_cases": 36672,
    "violations": 0
  },
  "not_established": [
    "general proof by finite enumeration",
    "natural-language interpretation correctness",
    "concurrent database conformance",
    "external exactly-once execution",
    "independent scientific acceptance",
    "human comprehension or learning",
    "full repository CI",
    "site deployment or indexing"
  ],
  "pass": true,
  "record_type": "interaction-memory-bounded-checks/1",
  "source_commit": "ea0c30575d56e793fb2875df47126ab3f6dc30ad",
  "source_sha256": "8dacee80ed050c3013c7de092da2c17fbfaafd5fb3b45939dc8fdae3611df656"
}
```

The model and comparison implementation have the same author. A zero violation count in the stated carriers does not establish a general mathematical theorem by enumeration or a guarantee about natural-language interpretation. Repository CI, separate review and deployed readback require their own records.

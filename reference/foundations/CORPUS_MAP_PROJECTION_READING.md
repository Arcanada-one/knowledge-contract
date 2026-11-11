---
title: Corpus map projection reader guide (candidate)
sources: none
status: proposed reader guide; not a release, proof graph or Muneral state
---

# Corpus map projection reader guide (candidate)

Authored by KC-Brain, 2026-11-10; input blob a7b2fb8cde305b8fe4145df1ee7d7179478fdd60; generator pin tools/project_corpus_map.py @ e5b92fad610322ac6c6518702ba152845fb504bb (commit e9cad2828ab44315a4f5941bbadd072e28ea074b).

- Input is `reference/foundations/corpus-map.json` at exact Git blob a7b2fb8cde305b8fe4145df1ee7d7179478fdd60, `record_type=knowledge-corpus-map/1`, `status=proposed-reference-view`. The output `knowledge-corpus-map-projection/1` is CANDIDATE, not a normative ontology, proof, runtime policy, publication decision or Muneral task state.
- Node groups retain disjoint, explicit types: documents (9 manuscript references), terms (16 reading summaries), claims (9 bounded authored summaries), foundation_units (6 prepared/planned manuscript units), roadmap_nodes (25 work *definitions*, not task identities). A node's label is never evidence for its truth or acceptance.
- Relation layer `uses-term` means a source cross-references a shared term; not identical semantics or runtime compliance. `states-bounded-claim` means a manuscript is associated with a premise-and-limitation-qualified claim summary; not proof or third-party corroboration. `reading-interface` means a directed reading connection; not a direct converse edge, inference or prerequisite. `has-candidate` means an identified draft/proposal exists; not release. `extends-existing-path` means editorial extension; not completed foundation. `addresses-planned-scope` is topical alignment; not task completion. `informs-not-blocks` is advice; not an execution gate.
- Planning layer `roadmap_nodes.requires` consists of 45 prerequisite-output *definition* edges and is never combined with 99 reading/semantic relations or promoted to a Muneral depends_on edge without independent reconciliation.
- A *direct edge* must match an explicitly pinned ordered (from,kind,to) triple. *Reachability* is transitive path existence and does not create a direct edge. A *strongly connected component* reports mutual reachability among participants, not all pairwise arrows or a circular proof. *Coverage* means inventory rows inspected relative to a declared denominator and scope, not correctness. *Scientific support* requires explicit premises, scope, and evidence in authoritative source; these reading edges cannot create such support.
- Retain exact provenance and claim premises/limitations, especially F01 C03's initial-state premise P1(x0). A source change, pin mismatch, unknown node, altered kind, or unverified conclusion must not be silently normalized, generalized or changed to an accepted status. Negative and mixed results remain visible.
- The candidate may expose 65 nodes / 99 typed relations / 45 separate planning edges and directed SCC participants {D01,D03,D05,D06,D07,D08}, but not synthesize absent D03->D05, D05->D03 or D06->D05 links. It may not claim exhaustive historical semantics; RM-01 still requires source-by-source claim inventory and disposition.

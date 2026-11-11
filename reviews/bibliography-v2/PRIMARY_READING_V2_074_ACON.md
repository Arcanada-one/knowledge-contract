---
title: "V2-074 ACON: fixed-edition primary reading and bounded claim comparison"
status: "author primary-text reading; proposed comparison only; not independently reviewed"
---

# V2-074 — ACON: primary reading at a fixed public edition

## Source and inspection boundary

- Historical ID: `V2-074` in `reviews/bibliography-v2/V2_REFERENCES.tsv` (Git blob `578bf2395846b6b262bd1d0a4b95811704ade749`).
- Primary text read: Minki Kang et al., *ACON: Optimizing Context Compression for Long-horizon LLM Agents*, arXiv:2510.00615**v3**, dated **1 June 2026**, HTML at <https://arxiv.org/html/2510.00615v3>. The arXiv page displays **CC BY 4.0**. The edition suffix is material; this note does not assume equivalence to v1 or v2.
- Inspection: author-led reading of the published primary HTML (abstract, §§1, 3.1–3.4, 4.1–4.2, conclusions and Appendix A); benchmark tables and limitations checked. No independent empirical reproduction, code execution, data audit or confirmation of peer-review acceptance. No third-party text is copied here.

## What this source does support

ACON explicitly applies two LLM-based context reductions: older action/observation history above a threshold (§3.2, eq. 3), and large current observations above another threshold (§3.2, eq. 4). Its compressor guidance is refined using contrasts between successful full-context and unsuccessful compressed-context agent trajectories (§3.3), without changing the base agent's weights. A student compressor can be trained separately (§3.4).

The empirical setting (§4.1) consists of AppWorld, OfficeBench and multi-objective QA. In the AppWorld comparison (§4.2, Table 1), the reported no-compression task score is 56.0 at 9.93k peak tokens, versus 56.5 at 7.33k peak tokens for ACON's history compression with two-stage guideline optimization (utility then compression, UT+CO). Average interaction steps rise from 16.14 to 22.82 in those rows. Those are **authors' benchmark measurements**, not our own and not per-task semantic-preservation certificates.

## Relevant exact manuscript boundaries

- `papers/retrieval-and-context-composition/PAPER.md`, edition 1.1, §3: a composition is feasible only when *the delivered representation* retains or validly transforms mandatory support; a root-closure list cannot discharge this requirement. §6 separates final-answer outcomes, representation checks and cost measurement.
- `papers/knowledge-utility/PAPER.md`, edition 1.1, §§2–4: utility is conditional on task, recipient, revision and baseline; actual resource costs, outcome metrics and causal attribution must be reported separately.

**Candidate comparison sentence for later editorial review, not inserted into either paper:** "Failure-guided compression such as ACON addresses empirical token/performance trade-offs for long-horizon agents; its measured aggregate task success does not certify that each mandatory condition is preserved in an individual delivered context." This is a comparison of objectives and evidence levels, **not** a claim that ACON implements Knowledge Contract support groups or that KC outperforms ACON.

## Non-support, counterevidence and editorial disposition

The source explicitly says compression may omit salient details (§3.2). OfficeBench Table 2 reports ACON history-utility optimization at 74.74 accuracy against 76.84 without compression; adding aggressive compression can reduce accuracy further (72.63). This directly counsels against any blanket "lossless" or "always improves accuracy" language. The authors note controlled benchmarks, added latency, limited cross-model testing and no formal prompt-optimization convergence guarantee (Appendix A). The paper supplies no per-claim `DeliveredSupports` theorem, KC-shaped dependency closure, semantic evidence audit, or causal estimate for this repository's system.

**Decision:** advance V2-074 from historical *not rechecked* to **one author-read public edition for this review note only**. Keep `V2_REFERENCES.tsv` and merged `knowledge-corpus-map/2` source-state pins unchanged; do not manufacture `claim_source_edges` or `evidence_assessments`. Do not alter canonical manuscript citations or the site before an exact-sentence proposal, separate Agent-Brain review and standard PR gates. This note is scientific comparison preparation, not a source-admission receipt.

## Reproducible links

- Source: <https://arxiv.org/html/2510.00615v3> (v3, June 1 2026, CC BY 4.0).
- Original claim-location screening: [wave 06](CLAIM_TRIAGE_WAVE_06.md), V2-074.
- Pinned comparison manuscript: `fb410a8460677b229d2240ba0fb27d184f48aa61` (existing accepted edition; re-pin at manuscript-edit time).

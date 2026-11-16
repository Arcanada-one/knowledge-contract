---
title: "Agent Situation Prototype: Predeclared Design Input"
status: "author-draft"
sources: none
license: "CC-BY-4.0"
---

# Agent Situation Prototype: Predeclared Design Input

Recorded before prototype implementation, 2026-11-14. This is an authored finite demonstration contract, not an independent preregistration or empirical agent evaluation.

## Scope

Implement a small Python-standard-library reference model of typed observations, per-source sequence handling, event/expiry invalidation and bounded context projection. No real tools, grants, effect execution, LLM calls, network, native admission or live autonomy are implemented. Structural readiness does not grant permission. All result provenance identifies authored finite evidence and native admission NOT_VERIFIED.

An observation retains key, scope, source identity, event id, producer sequence, value or explicit unknown/conflict, observation time and receipt time, TTL and dependencies. Multiple sources can disagree. Age is computed from observation time; arrival or replay does not renew it. Future observation timestamps or negative clock movement must be explicit invalid states. Independent source conflict is retained rather than arbitrarily selecting last arrival. Duplicate event ids with identical payloads are idempotent; nonidentical reuse is rejected/conflicted.

Projection takes scope, required keys, optional ranking, now and an abstract integer cost budget. It includes the transitive dependency closure of required keys or returns NOT_FIT/NOT_READY with reasons. Critical unknown/stale/conflicted inputs cannot silently become ready. Optional inputs do not displace required dependencies. A snapshot binds model generation; changed critical prerequisites invalidate it. Cost units are abstract, not measured LLM tokens.

A refresh planner distinguishes a relevant event, expiry without notification, an irrelevant heartbeat, and a pre-action freshness check. No claims about calibrated value of information or optimal scheduling.

## Predeclared adverse and positive controls

1. Freshness on either side of TTL and at the boundary, plus stale positive recovery after an actual new observation.
2. Unknown is preserved and is different from false or zero.
3. Receipt/replay cannot make an old observation fresh.
4. Future observation time / backward clock condition cannot yield a ready action context.
5. Lower producer sequence cannot roll back a newer value.
6. Conflicting independent observations remain a conflict.
7. Exact duplicate idempotency and inconsistent duplicate rejection.
8. Relevant dependency update invalidates a derived claim; unrelated update does not.
9. Heartbeat/message without relevant fact change does not refresh static observation time or request a model call.
10. Scope change cannot reuse a context from another account/workspace.
11. Required dependency closure fits at exact budget and returns NOT_FIT one unit below, without dropping a mandatory member.
12. Missing/unknown mandatory slot prevents readiness; irrelevant optional unknown may be omitted with explicit disclosure.
13. Stable optional ordering and deterministic projection under the same inputs.
14. A fixture representing revocation invalidates a dependent projection; the fixture is not a grant authority.
15. A changed critical generation is detected before hypothetical effect; unchanged snapshot stays valid.
16. TTL backstop requests observation when an event was lost.
17. Pre-action freshness is applied to declared critical dependencies; unrelated facts do not force blanket refresh.
18. Unknown external action outcome is retained as unknown, not successful and not an automatic retry grant.

Use hand-authored expected outcomes rather than only roundtrip tests. If a case is outside the implemented subset, report it as NOT_IMPLEMENTED and document the limitation. Prefer a clear, small correct subset to invented assurance. Include discriminating negative controls for at least time freshness, dependency closure and scope if feasible; a deliberately disabled guard should fail the corresponding independently expected case.

## Deliverable layout

Work only under:
agent-situation-research/prototype/

Provide checks/check_agent_situation.py (runner), reference implementation as needed, evidence/finite-run.json (actual run; inputs/outputs/counts/provenance/source digests), README.md (commands, supported subset, limitations). Print actual execution command and outcomes. No remote writes. Do not write STUDY.md yet: the root will interpret actual outputs separately.

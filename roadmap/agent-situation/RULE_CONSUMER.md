---
title: "Rule Consumption: Captured Inputs and Explicit Recovery"
language: en
license: CC-BY-4.0
sources: none
status: bounded offline implementation; separate scientific review pending
---

# Rule Consumption: Captured Inputs and Explicit Recovery

## Purpose and existing work

This third bounded Agent Situation adapter connects the [Repository Session](REPOSITORY_SESSION.md) to the [Semantic Bridge](../../engineering/specifications/semantic-bridge/SPECIFICATION.md). The observed source baseline is main `a5b3618034256f14f389c2c7de8da409c7c5310c`: the parent, observer, session and bridge were integrated through PR113, PR115, PR116 and PR118. Their older open proposal branches are not evidence that this source integration is missing.

The session previously tracked committed file identities; the bridge CLI independently read source and packet paths. The new [consumer](../../tools/repository_rule_consumer.py) supplies the missing composition: the exact bytes used in a calculation come from the fresh capture of the explicitly adopted required context. It does not change either component's scientific scope or introduce a new roadmap task. It prepares one local laboratory consumer under Agent Application; it does not close the advanced workstream or a Live Lab runtime dependency.

## File profile and operations

The profile contains exactly two distinct normalized relative paths: controlled source and interpretation packet. Both are observed and required. Task, scope, local repository address, producer label and abstract budget are frozen by the initial session profile. Source and packet roles remain fixed across its continuation. Neither the labels nor the local address digest authenticate an owner or establish a permission.

| Operation | Acquisition and adoption | Calculation |
| --- | --- | --- |
| `start` | One real capture through Session START; a ready context is explicitly adopted | None |
| `resume` | One real capture through Session RESUME; only successful explicit recovery replaces the adopted context | None |
| `evaluate` | One fresh Session PREFLIGHT against the supplied predecessor | Only a `VALID` preflight permits a new calculation |
| `inspect` | No new acquisition or adoption | Replays the retained bundle for internal consistency; returns `HISTORICAL_ONLY` |

After a changed required source or packet, preflight returns `INVALID` and the consumer returns `BLOCKED`, with `analysis=null`. Continuing from that published bundle returns `RESUME_REQUIRED` until a successful explicit resume. A replacement candidate being ready does not adopt it. An unrelated commit may change HEAD while the declared two-file context remains valid. Branch, HEAD and index are acquisition evidence, not additional implicit dependencies of this file-only profile.

For a valid evaluation, the consumer selects both byte strings from the final captured ledger entry. Each entry's blob, mode, size and SHA-256 must match its known projected dependency. It never reopens the working-tree source or packet. Thus coherent but uncommitted decoys cannot replace the calculation inputs. This does not observe or certify a clean working tree, atomic repository state, absence of unobserved changes, or freshness after the capture.

The additive `semantic_bridge.parse_packet_bytes()` API uses the same strict duplicate-key, nonfinite-number, UTF-8, integer-decoder and byte-limit policy as `read_packet()`. Existing file callers delegate to it. A parsed packet is still checked against the complete source-rule inventory and its exact source digest. Unknown and withheld observations, unsupported grammar, and attributed alternatives retain the original bridge meanings. `EVALUATED` describes a completed computation and may contain `TRUE`, `FALSE` or `UNDETERMINED`; it grants no permission.

## One consumption bundle

The `repository-rule-consumption/1` envelope contains the full Session receipt, the two input roles, capture/context/commit/tree and file identities, the complete bridge report when available, operation/result, implementation hashes and a declared predecessor link. Start, resume and blocked evaluation contain no new analysis. The nested session remains a `repository-session/1` receipt rather than a modified incompatible receipt.

`validate_bundle()` verifies the finite inventory, session replay, input binding and the retained result. For an evaluated historical bundle, it recomputes that old result from the retained bytes. A changed answer followed by a newly computed envelope hash therefore fails internal replay. This is not an independently structured scientific oracle or producer authentication. A party able to replace all records can create another internally consistent history. The predecessor consumer ID is a declared link; no unique external log, latest pointer, anti-fork service or complete observation history is provided.

The distinction matters when reporting work: a blocked fresh preflight performs **no new calculation on its fresh candidate**. Validating its predecessor may replay an older calculation. Inspecting a receipt can establish internal consistency, but cannot establish current readiness.

Runtime bounds are at most **32 captures** including the initial start and **32 MiB** for each serialized CLI input/output bundle. The actual capture inventory and declared sequence are bounded before replay. The bridge separately limits source to 64 KiB and packet to 128 KiB; the observer's original acquisition limits also remain in force. These are finite implementation limits, not a measured model-token, total latency or monetary budget.

## Publication and interrupted processes

The CLI publishes one complete new envelope outside the observed repository using the existing exclusive same-directory temporary-file/hard-link writer. Existing files and symlinks are never replaced. A successful output binds the observed session and computation in one file; there is no separately published success marker that could precede its evidence.

A crash before the final link leaves no completed destination bundle. The in-memory capture or failed preflight may be unrecorded; retry starts from the last published predecessor and acquires a new capture. A crash after publication may leave a complete bundle even if stdout was not received. Inspect that file instead of overwriting it. This protocol does not claim retention of every preflight across crashes, exactly-once execution, global serial history, directory-fsync/power-loss durability or continuity of external effects.

## Reproduce the finite laboratory

Run from a source checkout, choosing a new output directory outside it:

```sh
python3 -B -m unittest tools.test_repository_rule_consumer tools.test_repository_rule_lab -v
python3 -B tools/run_repository_rule_lab.py --output /tmp/kc-rule-lab-new-run
```

The [fixed case inventory](../../tools/fixtures/repository-rule-lab/cases.json) is checked before execution. The [runner](../../tools/run_repository_rule_lab.py) creates its own local synthetic Git repository and launches a fresh consumer process for each operation. It records the expected inventory before outcomes, raw stdout/stderr, Git commands, complete bundles, program hashes before/after, failed steps and unexecuted cases. Removing, repeating, reordering or injecting a case cannot produce a success-shaped reduced inventory. A completed report is `RUN.json`; existing runs are never overwritten.

The twelve steps form **one authored lifecycle**, with eleven captures and one historical inspection: start; unknown evaluation; uncommitted decoys; changed packet; repeated blocked evaluation; explicit resume; determinate true evaluation; unrelated commit; changed unsupported source; explicit recovery; unsupported calculation; historical inspection. They are not twelve independent trials, a language-model comparison or a measurement of source-interpretation fidelity.

The [retained execution and review](../../reviews/repository-rule-consumer-20261115/REVIEW.md) includes actual outcomes and two development findings. The first runner fixture omitted mandatory observation type/referent fields and was correctly refused. A separate code review found the capture limit was originally checked after historical replay; the corrected implementation checks the inventory before that work. Original attempts remain separate from their corrected reruns.

For an existing authorized local input pair, the public commands are:

```sh
python3 -B tools/repository_rule_consumer.py start \
  --repo /absolute/path/to/repository --source-path source.txt --packet-path packet.json \
  --task-id evaluate-rule --scope committed-rule-inputs --output /tmp/rule-start.json
python3 -B tools/repository_rule_consumer.py evaluate \
  --repo /absolute/path/to/repository --previous /tmp/rule-start.json --output /tmp/rule-evaluation.json
python3 -B tools/repository_rule_consumer.py resume \
  --repo /absolute/path/to/repository --previous /tmp/rule-evaluation.json --output /tmp/rule-resumed.json
```

Exit zero means a ready start/resume or evaluated computation. Exit one means blocked/unready/not-fit. Exit two means invalid or unsupported input/result, or a process/output error. Inspect the structured result and stderr; a true logical value is not the definition of process success. A resumed context still needs a subsequent fresh `evaluate` call.

## Laboratory boundary and next acceptance

This supplies an offline consumption seam between source, formal calculation and explicit agent state. It uses no LLM, network retrieval, native KC2 admission, real grant or external effect. `effects_authorized=false`, `history_complete=false` and the nested unobserved CI/effect/authority fields remain explicit. Billing is `NOT_MEASURED`.

Next acceptance is separate review of the exact source revision and a KC-SWE replay in the intended environment. The existing website can describe this finite result, while its live connection remains separately observed. Browser execution, desktop/mobile presentation, actual runtime consumer attachment, current authority, native admission and the proposed 450-run experiment have their own outstanding criteria. The present source change authorizes no experiment expenditure.

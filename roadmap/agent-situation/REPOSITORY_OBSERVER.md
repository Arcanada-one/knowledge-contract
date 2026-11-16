---
title: "Agent Situation: Offline Repository Observer"
status: "research-prototype; internal-review; external-review-pending"
language: "en"
license: "CC-BY-4.0"
sources:
  - "Agent Situation repository observer"
  - "Git object and index commands"
---

# Agent Situation: Offline Repository Observer

This bounded RM18 increment connects actual local Git observations to the existing finite situation model. It implements part of iteration 3 in the [engineering design](ENGINEERING.md). It does not complete RM18 or execute the [LLM experiment](EXPERIMENT.md). The reviewed research base is PR105 at `dec63e4631d1b02e7b22bbc2e780c41cd6a7bfd7`; this increment leaves that candidate's model, fixtures and historical study evidence unchanged.

## Implemented boundary

[`tools/repository_observer.py`](../../tools/repository_observer.py) reads an explicitly selected local repository root and one to 32 normalized relative file paths. It pins the starting commit, reads regular committed blobs directly, verifies their Git object identities and SHA-256 digests, records selected index metadata, and reads HEAD again. The receipt retains each command's arguments and timestamps; completed subprocesses also retain their return code and raw stdout/stderr. Spawn and timeout failures retain the exception class with no return code; partial timeout output is not preserved. Missing files, unsupported tree entries and unavailable reads are distinct observations.

| Observation | Interpretation |
| --- | --- |
| `status=OK` | The command sequence completed and the two observed HEAD values agree. This does not prove atomicity, a clean working tree, or absence of an intervening change. |
| `CHANGED_DURING_READ` | The two observed HEAD values differ; replay cannot use the capture as a ready file snapshot. |
| `UNAVAILABLE` | The capture could not be completed because a command or response validation failed. Previously collected bytes remain evidence; replay makes all selected file facts unknown. |
| File `PRESENT` | The pinned commit contains a supported regular blob within the size bound. |
| File `ABSENT`, `UNSUPPORTED` or `UNAVAILABLE` | Required file content remains unknown for projection, even if the outer command sequence completed. |
| `selected_index_b64` | Raw `git ls-files --stage -z` output for the selected paths. This is index metadata, not working-tree content. |
| `working_tree_state=NOT_OBSERVED` | Unstaged changes are not inspected. No clean/dirty conclusion is available. |

The adapter does not fetch, contact an API, call an LLM, execute an effect, or derive authority. It does not read untracked bodies or follow selected symlinks or submodules. Explicit caller-provided scope and producer labels are labels, not authenticated identities. Capture bounds are 32 paths, one MiB per regular blob and ten seconds per Git command; these are not a total runtime, memory or model-token budget.

Git configuration can affect commands. The adapter excludes ambient `GIT_*` overrides, global/system config, optional locks, filesystem-monitor hooks, object replacement and lazy fetching, and disallows transports. It reads committed objects without `--filters` or `--textconv`. This is a local research adapter, not a sandbox for an adversarial Git binary or repository. Raw diagnostics and selected committed content should be reviewed before sharing a receipt.

## Ledger and replay

`make_ledger()` records the ordered captures, explicit count, predecessor hashes and final hash. A fresh process verifies that complete structure before replay. Rewriting a capture without its digest, dropping an entry without updating the chain, or changing selected scope/path profiles is rejected. A party able to rewrite all records and hashes can construct another internally consistent ledger: the chain does not establish producer authenticity, a trusted current repository state, or complete observation history.

`replay_ledger()` instantiates the unchanged reference model and retains the recorded observation times. A selected file contributes a fact containing its blob identity, mode, size and SHA-256; its text stays in the ledger. The projector therefore demonstrates dependency tracking for file identities. It does not yet serialize the file bodies into an LLM context window, and its budget uses the finite model's abstract units, not token counts.

The bridge suppresses duplicate captures and unchanged facts from the same producer. A changed required file invalidates the previous context. An unrelated commit can change HEAD while leaving the file-only context valid. HEAD, branch and index metadata remain acquisition evidence; they are not automatically dependencies of the projected file-only context. A merge, release or effect-bound profile would need explicit current-HEAD, index, CI and authority dependencies before use.

Conflicting file values from different producer labels remain conflicted. A missing intermediate commit does not become a claim of complete history. `history_complete=false`, `not_observed=[ci, effect_outcome, authority]` and `readiness_grants_permission=false` remain explicit. An unobserved effect outcome is retained as an observation limit; this version does not reconcile a real effect.

## Run against an authorized local checkout

Choose paths that may be recorded and an output location outside the observed repository. Every output ledger must be a new file; the CLI uses exclusive creation so it cannot overwrite earlier evidence.

```sh
python3 -B tools/repository_observer.py observe \
  --repo /absolute/path/to/authorized-checkout \
  --scope repository-file-review --producer local-git \
  --path CITATION.cff --output /tmp/kc-observation-1.json

python3 -B tools/repository_observer.py observe \
  --repo /absolute/path/to/authorized-checkout \
  --scope repository-file-review --producer local-git \
  --path CITATION.cff --previous /tmp/kc-observation-1.json \
  --output /tmp/kc-observation-2.json

python3 -B tools/repository_observer.py replay \
  --input /tmp/kc-observation-2.json --path CITATION.cff
```

`observe` exits zero for a completed stable-HEAD capture, one for an observed Git failure or HEAD change, and two for invalid arguments/records or an output error. A zero capture exit does not assert that all selected files are present. `replay` exits zero when a ledger was processed; inspect its returned `READY`, `NOT_READY` or `NOT_FIT` context state separately. Invalid replay records or arguments exit nonzero.

## Verification and correction retained

The [11 integration checks](../../tools/test_repository_observer.py) use real temporary Git repositories and the public API/CLI. They cover cold start and byte identity; relevant versus unrelated changes; staged versus unobserved unstaged state; replay times and tampering; missing then created content; conflicting producers; an omitted intermediate commit; scope/path boundaries; unsupported symlinks; fresh-process replay and exclusive output; and a configured Git clean filter.

The last check comes from a real development defect. The initial implementation used `git status`, which could execute a repository-configured clean filter while examining changed working-tree content. A harmless marker proved that execution. The replacement reads selected index metadata with `git ls-files`; it explicitly gives up observing the working tree. The original implementation and actual failed probe are preserved alongside the [execution record and review](../../reviews/repository-observer-20261114/REVIEW.md). No second defect was added to that probe.

Run the actual integration boundary with:

```sh
python3 -B -m unittest tools.test_repository_observer -v
```

Normal publication-integrity CI runs the same tests. The retained sample observes two public files from a local checkout of the exact source revision recorded in its receipt; it is not evidence that this source revision remains current later. Review was performed by another agent under the same controller/model family and host. External acceptance, hostile-source security, real CI/effect observation, live grants, restart continuity for external effects, LLM performance, cost savings and production deployment remain unestablished.

## Primary command references

- [Git command and environment controls](https://git-scm.com/docs/git)
- [Object-tree listing](https://git-scm.com/docs/git-ls-tree)
- [Direct object reads](https://git-scm.com/docs/git-cat-file)
- [Index listing](https://git-scm.com/docs/git-ls-files)
- [Working-tree status semantics](https://git-scm.com/docs/git-status)

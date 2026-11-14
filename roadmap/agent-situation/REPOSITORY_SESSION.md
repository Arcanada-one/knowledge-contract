---
title: "Repository Session: Resume and Revalidate File Context"
status: "research-prototype; internal-review-complete; external-independence-not-verified"
language: "en"
license: "CC-BY-4.0"
sources:
  - "Agent Situation repository session"
  - "RFC 8259"
---

# Repository Session: Resume and Revalidate File Context

This second bounded RM18 adapter increment implements a local task lifecycle over the [Repository Observer](REPOSITORY_OBSERVER.md). It starts from the observer candidate at `880d4ea059e8110a81a37348c4cd17075f881780`. The observer, its eleven tests, the situation model and their retained evidence are unchanged. A separate source decision remains necessary for that stacked base; this increment does not upgrade its review or scientific status.

The problem addressed here is concrete: replaying a saved ledger can establish which file identities were ready at its recorded time, but that replay does not observe the checkout after a restart. A session makes the task profile and predecessor explicit and requires a fresh capture before producing a new resume or preflight result. It performs no LLM invocation, network request, deployment or external effect.

## Implemented API and result meanings

[`tools/repository_session.py`](../../tools/repository_session.py) provides:

| Entry point | Behavior |
| --- | --- |
| `make_profile(repo, task_id, scope, paths, required_paths, producer, budget)` | Freeze normalized selected paths, required paths, caller labels, an abstract projection budget and a digest of the resolved local root. The root digest is an address binding, not authenticated repository identity or ownership. |
| `start(repo, profile)` | Acquire one actual capture and issue its file-context receipt. |
| `resume(repo, profile, previous)` | Validate the predecessor and unchanged profile, acquire one actual capture, reconstruct the ledger and adopt the new file context. |
| `preflight(repo, profile, previous)` | Acquire one actual capture and check whether the predecessor's ready context remains valid. A newly ready replacement does not make an invalid predecessor valid. |
| `inspect_receipt(receipt)` | Validate a recorded receipt and return `HISTORICAL_ONLY` with `requires_fresh_capture=true`. It does not inspect Git. |

The selected profile allows one to 32 explicit regular-file paths; required paths must be a nonempty subset. The existing observer still determines whether a selected tree entry is supported and retains its one-MiB-per-blob and ten-second-per-command bounds. Working-tree content remains unobserved. The session does not infer clean/dirty state from the selected index.

`start` and `resume` return `READY`, `NOT_READY` or `NOT_FIT` for the new captured context. A successful resume explicitly adopts that context in `adopted_context_id`; a failed start/resume leaves no adopted ready context. A changed required file can produce a new `READY` candidate while `prior_validation` says `INVALID`. `preflight` returns `VALID` only when the adopted ready context survives the new observation and the new context is ready. If the required file changed, its result is `INVALID` even when the replacement candidate is ready.

Any failed preflight sets `resume_required=true` while retaining the former adopted anchor. Subsequent preflights continue to acquire fresh observations but return `RESUME_REQUIRED`; they do not adopt their new candidate. Only an explicit successful `resume` clears that state and adopts the new ready context. This conservative recovery rule also applies after a failed start/resume. Missing or unavailable evidence keeps the captured context `NOT_READY`; an insufficient abstract budget keeps it `NOT_FIT`, even when the operation result also indicates that resume is required.

All results are **as of the named capture**. Neither a successful preflight nor the two equal HEAD endpoint reads establish an atomic check-and-effect operation or prove that no change occurred afterward. `not_observed=[ci, effect_outcome, authority]`, `history_complete=false` and `readiness_grants_permission=false` are retained.

## Receipts, identity and restart

A receipt contains the frozen profile and digest, predecessor identity and ledger-prefix binding, complete hash-linked capture ledger, one declared operation per capture, final capture/time, implementation hashes, projected dependency identities and result. Validation replays both observations and the ordered operations to reconstruct the adopted anchor and resume-required state. It compares those derived fields rather than trusting stored `READY`, `VALID` or adoption flags. The session, observer and model hashes must match the loaded implementation; migration across implementation changes is not automatic.

The `context_id` is a SHA-256 digest of the frozen profile and semantic file-context fields. It names the currently projected candidate and can differ from `adopted_context_id` after a failed preflight. It excludes process-local `model_id`, generation counters, observation timestamps and unrelated HEAD changes. An unchanged required-file context therefore retains its identity across a new process or an unrelated commit. A receipt has its own digest, which includes its fresh observation and predecessor. Full selected file contents remain in the ledger; this increment does not serialize an LLM prompt or measure model tokens.

Every explicit resume/preflight call acquires one new observation, including when content is unchanged. Unchanged file facts are suppressed by the existing bridge, but a new observation receipt is retained. Two calls using the same predecessor create separate successors; this is not concurrent-writer election, an exactly-once action protocol or a claim of globally complete event history. A repeated capture identity is refused as a new session observation.

Checksums detect internally inconsistent records. A party able to rewrite all records and hashes can create another consistent history. Producer labels and local-root digests are not authentication. A standalone inspection checks the predecessor binding against the retained ledger prefix; it does not fetch a separately retained predecessor file or establish that such a file was published by a trusted producer.

JSON input rejects duplicate object member names recursively before profile or receipt interpretation, including names made identical by JSON escape decoding. It also rejects non-finite values and malformed/truncated JSON. This is a strict project input rule; it does not silently select the first or last duplicate value.

CLI output is created outside the observed repository. Complete bytes are flushed to a temporary file and published to a new path by an exclusive same-directory hard link; an existing output is never replaced. This avoids exposing a partly written destination through this writer on the tested filesystem. Power-loss durability, all filesystem implementations and recovery of abandoned temporary files are not established.

## Run an explicit local session

Choose an authorized checkout and output paths outside it. Reuse the same profile file and local root when resuming:

```sh
python3 -B tools/repository_session.py profile \
  --repo /absolute/path/to/authorized-checkout \
  --task-id review-citation --scope repository-file-review \
  --path CITATION.cff --output /tmp/kc-session-profile.json

python3 -B tools/repository_session.py start \
  --repo /absolute/path/to/authorized-checkout \
  --profile /tmp/kc-session-profile.json --output /tmp/kc-session-start.json

python3 -B tools/repository_session.py inspect --input /tmp/kc-session-start.json

python3 -B tools/repository_session.py resume \
  --repo /absolute/path/to/authorized-checkout \
  --profile /tmp/kc-session-profile.json \
  --previous /tmp/kc-session-start.json --output /tmp/kc-session-resume.json

python3 -B tools/repository_session.py preflight \
  --repo /absolute/path/to/authorized-checkout \
  --profile /tmp/kc-session-profile.json \
  --previous /tmp/kc-session-resume.json --output /tmp/kc-session-preflight.json
```

Capture commands exit zero only for `READY` or `VALID`; a completed but blocked observation is saved and exits one. Invalid input, a mismatched profile/implementation or an output error exits two. `inspect` exits zero when a historical receipt was processed successfully, including when its captured result was not ready. Its exit status does not establish present readiness.

## Finite completion boundary

The [integration checks](../../tools/test_repository_session.py) exercise actual temporary Git repositories and separate CLI processes. They cover fresh start; historical-only inspection; required versus unrelated changes; repeated preflight refusal without adoption; explicit resume after failed preflight or failed resume; unavailable and missing-file recovery; frozen profile/root matching; exactly one real acquisition per resume; predecessor preservation; malformed, duplicate-key and altered records; exclusive output; abstract-budget refusal; and the configured clean-filter boundary. A call counter wraps the real observer in one check; Git output and the reference model are not mocked.

The first internal review found a real missed transition: start at A, change the required file to B, fail preflight, then repeat preflight without resume. The predecessor implementation returned `READY → INVALID → VALID`, silently treating B as its new baseline. The [original source, actual failed trace and receipts](../../reviews/repository-session-20261114/REVIEW.md) are retained. The successor separates candidate and adopted identities and replays operation history; its regression requires `READY → INVALID → RESUME_REQUIRED` until explicit resume. No historical record is rewritten to describe this as an original success.

This defect gives an engineering illustration of the explicit intermediate-state requirement developed in [PR #108](https://github.com/Arcanada-one/knowledge-contract/pull/108): the observed candidate B alone is insufficient to decide the next preflight. Whether that context has been adopted, together with the recorded operations and resume-required state, changes the next permitted transition. This connection does not constitute formal verification of the whole agent runtime.

The [execution record](../../reviews/repository-session-20261114/REVIEW.md) binds actual tests and a separate process-lifecycle demonstration to implementation bytes. Normal publication-integrity CI runs the new session suite separately from the unchanged observer suite:

```sh
python3 -B -m unittest tools.test_repository_session tools.test_repository_observer -v
```

This establishes a bounded local file-context lifecycle. It does not complete RM18, run the 450-episode experiment, establish independent scientific acceptance, supply a production persistence service, authenticate hostile input, grant authority or reconcile real external outcomes. Replay cost grows with the retained ledger; no overall latency, memory or token-budget claim is made.

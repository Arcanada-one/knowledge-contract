---
title: "Repository Observer: Bounded Execution Review"
status: "same-controller-review-and-execution; external-review-pending"
sources: none
license: "CC-BY-4.0"
---

# Repository Observer: Bounded Execution Review

Date: 14 November 2026. Reviewer: `/root/research_review`, a non-author of the
adapter module and the author of its integration tests. The implementer and
reviewer share the parent controller, model family and host. This is internal
engineering review, not independent external acceptance.

**Disposition: no remaining blocking finding in the inspected offline adapter
scope.** The completion criterion is the implemented observation boundary and
its eleven behavioral checks, plus the actual two-file capture and replay below.
This closes one bounded implementation increment of RM18; it does not complete
RM18 or run its proposed LLM experiment. A later source change needs a new scoped
review rather than inheriting this verdict.

## Exact sources and provenance

The reviewed research base is [PR105](https://github.com/Arcanada-one/knowledge-contract/pull/105)
at `dec63e4631d1b02e7b22bbc2e780c41cd6a7bfd7`, tree
`d8b769c143bbf4252d580d6418f03545c6090b84`. The local implementation checkout
contains that prepared tree plus this increment, while its local Git HEAD is
`535c557a1c6bf90e156a17ca6d340a5c6dcd0a1f`. The local HEAD is not represented as
PR105's revision. File hashes bind the executed implementation.

| Executed source | SHA-256 |
| --- | --- |
| [Observer](../../tools/repository_observer.py) | `0de30dfec05fab77730d905aa04e58efa6a23f50a5fb12e669b3326b3f230cba` |
| [Integration checks](../../tools/test_repository_observer.py) | `6f57ea3ef038dfdce986641ca7710bc70547d9ebfcae7bed687c9fff678734cf` |
| [Existing situation model](../../engineering/studies/agent-situation-controls/situation.py) | `4c15d461e4d67de5984f40a94a7b92f70745c5fc9f2f39aa2681c287c31ed1c1` |

The [execution receipt](execution-receipt.json) records these sources, runtime,
commands, actual times, and hashes of retained execution evidence. It does not
hash itself or claim to authenticate the observing agent. All 27 retained files
under `engineering/studies/agent-situation-controls/` match the reviewed research
base byte for byte, including the model, fixtures, manifests and historical
records. Their individual hashes are retained in the receipt. The publication
catalogue and evidence index are also unchanged. This new operational review is
not a rewritten historical study or a new catalogue admission.

## Found defect, repair and preserved failure

The initial adapter invoked `git status`. In a real temporary Git repository,
a same-size modification to a tracked file caused that operation to run a
configured `filter.recording.clean` process. The harmless process created a
marker file while capture reported `OK`. This violated the intended read-only
capture boundary.

The [pre-fix source](../../tools/retained/repository_observer_filter/repository_observer_before_filter_fix.py),
SHA-256 `ab8724b9d026a1f24e8a908d57b62e829eb3b1f34e6147226ad41fa5e8dcae02`,
and the [standalone reproduction](../../tools/retained/repository_observer_filter/probe_configured_filter.py)
are retained. [The original probe JSON](pre-fix-filter-probe.json) is an exact
copy of the observed pre-fix result: the marker was absent before capture and
present afterward. Packaging did not rerun this predecessor or replace that
result. The probe uses the existing defect; it does not insert a second defect.
Its intentional marker effect stays inside its temporary directory.

The implementer removed `git status` and substituted selected index metadata
from `git ls-files --stage -z`. Captures now explicitly report
`working_tree_state: NOT_OBSERVED`. Committed content stays bound to the pinned
blob; index entries are separate evidence and give no clean/dirty conclusion
about unstaged files. The configured-filter regression in the final test run
passes without creating the marker. The rejection of the path `.` is included
in the path-boundary check.

Two documentation claims were also narrowed to match the code. Raw stdout and
stderr are retained for completed subprocesses; spawn or timeout failures retain
the exception class and no return code, and partial timeout output is not
preserved. `UNAVAILABLE` covers failed response validation as well as command
failure. These are documented limits, not additional counted tests.

## Behavioral completion checks

The actual [integration test log](integration-tests.txt) records **11 tests,
all passing**, in 1.120 seconds. The time is an observation from this run, not a
performance benchmark. The tests exercise real temporary Git repositories,
the public API and the CLI without mocking Git or the existing model.

| Obligation | Observed behavioral boundary |
| --- | --- |
| Cold start | Committed bytes, object identities, SHA-256 and sizes agree; unselected untracked and configuration bodies are excluded. |
| Relevant updates | A changed required blob invalidates its previous context; an unrelated commit leaves a file-only context valid. |
| Index and worktree | Staging changes selected index evidence without replacing the pinned committed content; unstaged state remains unobserved. |
| Replay | A fresh reducer preserves semantic counts and recorded observation times; an altered capture is rejected. |
| Missing content | A required absent file denies readiness; its actual committed creation recovers readiness. |
| Conflict | Different producer labels reporting different file values remain in conflict. |
| Missed event | Skipping an intermediate commit still permits a latest-file snapshot but never asserts complete event history. |
| Scope | Invalid paths and incompatible comparison profiles are rejected. |
| Unsupported entry | A committed symlink is not dereferenced. |
| Process restart | The CLI creates a new successor ledger without overwriting its predecessor, and a new process replays it. |
| Read-only regression | The previously configured clean filter is not executed by capture. |

These are eleven test methods, not eleven independent scientific samples.
Exploratory manual checks are excluded from the count. The command is:

```sh
python3 -B -m unittest tools.test_repository_observer -v
```

## Actual public-repository sample

An isolated local clone was checked out at source commit
`6a6f202f7f70be2ad3aea3369e45409761708596`. This is the observed sample source,
separate from both the research-base revision and the local implementation
checkout's older Git HEAD. Only the explicitly selected public files below were
captured. Evidence was written outside the observed clone.

| Path | Bytes | Git blob |
| --- | ---: | --- |
| `.markdownlint.json` | 68 | `77b58852250d18f3e8b35eeabd648cc4af8f0c19` |
| `CITATION.cff` | 835 | `f322022689b2bf2f80a0009e05a1832f6a3283e6` |

The [actual ledger](sample-ledger.json) contains one capture: starting and ending
HEAD equal that commit, capture status is `OK`, and both regular blobs are
present. The [replay output](sample-replay.json), produced by a new CLI process,
records two ingested facts and a `READY` file-identity context. The
[execution log](sample-execution.txt) retains the exact clone, checkout, capture
and replay commands and their outputs. This sample is an actual selected-source
observation, not another synthetic control case. Its `READY` result refers to
the selected file identities; file bodies remain in the ledger. The model's
process-local identifier does not establish cross-process identity.

No remote request, LLM call or external effect occurred during capture or
replay. Their output retains `history_complete=false`,
`not_observed=[ci, effect_outcome, authority]` and
`readiness_grants_permission=false`. The sample does not prove that the source
revision is still current elsewhere or that the whole repository was atomic.

## Repository validation and limits

The [validation log](validation-log.txt) records the publication, source and
requirement gates and the existing publication/source/separation/DCO/CI test
suites, using Pandoc 3.1.3. Their actual outcomes are recorded separately from the
eleven integration checks and the one-capture sample.

The final three gates passed, and all 93 existing suite tests passed. The first
source-gate run rejected one untracked generated Python bytecode file in the
study directory. Removing only that generated cache allowed the source gate to
pass; the initial failure and cleanup remain in the log. No retained study
source or evidence was changed to obtain the passing result.

The hash chain verifies internal consistency, not producer authenticity or a
complete history. A caller able to rewrite every record and digest can construct
another consistent ledger. Caller-provided scope and producer labels are not
authenticated identities. A changed HEAD between the two reads denies snapshot
readiness, but equal endpoints do not rule out intervening changes or establish
an atomic index observation.

This adapter does not observe CI, reconcile a real effect outcome, grant
authority, serialize a complete LLM prompt, or measure token costs. Its budget
uses the unchanged finite model's abstract units. It is not a security sandbox
for an adversarial Git binary or repository. Native admission, corpus admission,
production deployment, LLM quality or cost benefit, and external scientific
acceptance remain unestablished.

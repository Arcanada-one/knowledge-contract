# Repository state: bounded KC-SWE reproduction and integration status

This record preserves the completed 14 November 2026 readback. No new reads, tests or polling were performed to write it. Exact bindings and the four file hashes are in [STATE_STATUS.json](STATE_STATUS.json).

## Updated residual

**The residual “not checked in the KC-SWE environment” is closed within the bounded file-identity/Repository Session profile at PR109 head `4184014cb4aeaee16b6989a5205d978529558403`.** KC-SWE recorded an actual reproduction in its environment. Parent integration and the gates of the later reconciled heads remain outstanding.

The [archived message](https://github.com/Arcanada-one/collective-mailbox/blob/6a8423c9e8a6bfb3c6264bce7101fc7a272c8c9e/archive/knowledge-collective/KC-Brain/20261114T100350Z__to-KC-Brain__from-KC-SWE__e9cd23e2-c2e1-4dde-812e-ee4313753ca3__pr109-repro-pass.txt) is pinned to mailbox snapshot `6a8423c9e8a6bfb3c6264bce7101fc7a272c8c9e`, blob `ba9aad644d83596d2b4d397ddaef36f98f85f765`. Its [public PR109 result](https://github.com/Arcanada-one/knowledge-contract/pull/109#issuecomment-6875613754) records a fresh exact-head public clone on **arcana-devs**, user **dev**, **Python 3.12.3**, **Git 2.43.0**. The CI commands ran in separate processes: **11 Observer + 14 Session tests, all OK**.

KC-SWE's own temporary real-Git API probe retained `READY → VALID → INVALID → RESUME_REQUIRED` across a required-file change. Its adverse controls detected implicit preflight adoption, clearing the failed-preflight lock and adoption of non-READY context. Removing either of two redundant checks alone retained the property; removing both exposed the original defect and was detected. These environment/probe observations are KC-SWE's recorded result; no separate complete machine log from arcana-devs was supplied in those links, and this reviewer did not rerun its commands.

The archived message was already handled as FYI at 11:08:17 UTC. It requests no response at this head; the next review subject is the head after retarget.

## Reviewer readback

The reviewer read the actual GitHub Actions logs, not only their check names:

| PR and exact head | Observed state | Actual execution |
| --- | --- | --- |
| [PR107](https://github.com/Arcanada-one/knowledge-contract/pull/107), `880d4ea059e8110a81a37348c4cd17075f881780` | Open; 12/12 checks successful; base PR105 `dec63e4631d1b02e7b22bbc2e780c41cd6a7bfd7` | [11 Observer tests PASS](https://github.com/Arcanada-one/knowledge-contract/actions/runs/43554804553/job/132325129963), including fresh-process replay and configured-filter regression |
| [PR109](https://github.com/Arcanada-one/knowledge-contract/pull/109), `4184014cb4aeaee16b6989a5205d978529558403` | Open draft; 12/12 successful; base PR107 `880d4ea059e8110a81a37348c4cd17075f881780` | [11 Observer + 14 Session tests PASS](https://github.com/Arcanada-one/knowledge-contract/actions/runs/43581147897/job/132405936491), including actual fresh-process lifecycle and repeated-preflight refusal |
| [PR113](https://github.com/Arcanada-one/knowledge-contract/pull/113), `459333b3bbd85a9d6f5fd3a2ebd9351aca54fb7e` | Open draft; 12/12 successful; base main `d5e684e201f6d41498c4fbd8c2a3497eed2bb30e` | [22 reader tests PASS](https://github.com/Arcanada-one/knowledge-contract/actions/runs/43630192830/job/132554853831), including `test_enclosing_raw_html_block_is_refused` at 19:06:30 UTC |

Main was still `d5e684e201f6d41498c4fbd8c2a3497eed2bb30e` at this snapshot. No later state is inferred.

The four exact-head remote module/test blobs matched the previously reviewed bytes:

| File | Git blob | SHA256 |
| --- | --- | --- |
| `tools/repository_observer.py` | `e6139467aaa055a4ff9e9c4c43a2cb6de2afd0cb` | `0de30dfec05fab77730d905aa04e58efa6a23f50a5fb12e669b3326b3f230cba` |
| `tools/test_repository_observer.py` | `cf85f8776016c7a200b528d836893bd0e1a5bafc` | `6f57ea3ef038dfdce986641ca7710bc70547d9ebfcae7bed687c9fff678734cf` |
| `tools/repository_session.py` | `654b254b90c1a7d228c54e9c7cd99bf4afcade25` | `ca4afc21b0256a0c7a7f4d22fea3c483e8ae223a618ef5b87132cd3195c7546a` |
| `tools/test_repository_session.py` | `2cca8c671ecdd7a4ba2abaedb95f8ac76b0556ee` | `a42809e3aed52c36dda916c42de05121110726a9df7a23a257abda17bc5f068c` |

The [integrator's earlier record](https://github.com/Arcanada-one/knowledge-contract/pull/109#issuecomment-6875362990) separately records 25/25 package-file matches. This follow-up checked the four files above.

## Boundaries and next integration step

The exact source retains `not_observed=[ci, effect_outcome, authority]`, `readiness_grants_permission=false`, `llm_calls=0` and `history_complete=false`. Receipt inspection is `HISTORICAL_ONLY` and requires a fresh capture. A local READY provides no runtime authority. KC-SWE explicitly retained **AuthorityEvent r4 and native source admission as NOT_READY**. Author/reviewer controller family and host overlap; external independence is **NOT_VERIFIED**.

The restart evidence concerns CLI/ledger lifecycle. It establishes no production-agent restart or external effect. API32 health readback and journal publication mentioned in the same letter are separate service results.

The next action is to finish the exact-head **PR113 decision and integration**, then reconcile **PR107** onto the resulting main with integration-delta review and new-head CI, then do the same for **PR109**. The [PR107 review](https://github.com/Arcanada-one/knowledge-contract/pull/107#issuecomment-6872027103) explicitly preserves this ordering. The unchanged old-head suites do not need repetition merely to recover their status.

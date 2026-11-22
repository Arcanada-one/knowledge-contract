# Offline Rule Lab: Captured Inputs, Failures and Replay

## Delivered scope

This source increment begins at `a5b3618034256f14f389c2c7de8da409c7c5310c`, after the integrated Agent Situation, Observer, Session and Semantic Bridge work. It connects their existing file/context and formal-calculation boundaries through [Rule Consumption](../../roadmap/agent-situation/RULE_CONSUMER.md). No publication catalogue entry, corpus decision, allowlist, native admission or website connection is added.

The consumer uses one fresh preflight and computes only the captured committed source/packet bytes in its adopted required context. Changed mandatory bytes require explicit recovery. Unrelated commits need not invalidate this file-only context. Historical replay, valid calculation and authority remain different results.

## Actual finite observations

| Evidence | Observed result | Scope |
| --- | --- | --- |
| [Predeclared consumer cases](CONSUMER_CASES.json) and [actual unit run](consumer-tests/RUN.json) | 12 test methods PASS; code hashes unchanged during execution | Separately authored fixtures and expected results; real Git, public APIs and fresh CLI processes |
| [Lifecycle run](lab-run/RUN.json) | 12 planned, 12 executed, 12 passed; 11 captured operations and one historical inspection | One authored offline lifecycle, not 12 independent experiments |
| [Capture-limit correction](non-author/post-fix-cap/RESULT.json) | Consistent 32-entry input accepted; both 33-entry inputs refused before replay | Synthetic histories constructed from one actual seed capture; no claim of 32/33 actual observations |
| [Byte parser checks](non-author/PACKET_RESULT.json) | 7/7 bounded checks PASS | Valid JSON and strict malformed/duplicate/nonfinite/UTF-8/integer/size/type handling |

The complete lab inventory is also checked with a positive case and fifteen altered inventories: each of twelve missing cases, a duplicate, a reordering and an injected noncase. These are two unit-test methods with subcases. They are not added to the twelve lifecycle stages as independent episodes. The actual hosted invocation, when available, belongs to its exact PR revision and job log; this retained local report is not itself a hosted receipt.

The consumer, bridge, session, observer, finite model, runner and case inventory are pinned before and after the retained lifecycle. Core identities:

| Program | SHA-256 |
| --- | --- |
| Consumer | `17f591ee66540dc70d3a41f121fcfd2d00e72803ada7127fa95830dc4b1e524c` |
| Bridge including the additive byte API | `b8363fa17e9090f28e4010357b00f4527cf812b3740e5e6382ebd15624195e25` |
| Laboratory runner | `657935f1dbd49fde4eb74c5e85639a06220d6af8c239e07d96112c328ebbc831` |
| Fixed case inventory | `d6951b85137df601354df6b9687aa9694eff09a032792805b2cde4469392c61e` |

The checkout used for development has the exact signed source baseline and a shallow local history. The new uncommitted program identities above bind these runs; the baseline commit is not a claim that it already contained the new consumer. The full package manifest records the files submitted for review.

## Preserved failures

**Capture work was bounded too late.** The [non-author operational review](non-author/REVIEW.md) found that the first consumer replayed 33 retained entries before refusing its 32-capture limit. A falsely small declared sequence also reached that replay. The original consumer and three exact probe inputs remain under `non-author/baseline/` and `non-author/pre-fix-cap/`. The correction checks cheap shape, actual inventory and sequence before hashing/replay. The same probe keeps the legitimate 32-entry positive and shows zero replay entries for both over-limit inputs. It did not find a semantically accepted 33-capture result.

**The first laboratory fixture was invalid.** The [original lab run](development/initial-fixture-run/RUN.json) returned FAIL: 12 planned, 2 executed, 1 passed and 10 not executed. Its observation records lacked mandatory `referent` and `type` fields. The consumer correctly refused them. The retained original runner differs from its successor only by adding those fields; the declared expected outcomes and consumer validator were not weakened. The later successful run has its own identity and directory.

## Review and limits

[Consumer integration review](CONSUMER_REVIEW.md) and [operational review](non-author/REVIEW.md) were performed by different subtasks from the implementation author. They share the controller, model family and host. This separates authoring tasks and oracle structure; it does not establish external independence or separate-controller scientific acceptance.

The integration tests include a real standalone-CLI decoy calculation and the captured-byte consumer calculation. They also cover both required files, repeated blocking, explicit recovery, missing/recovered input, unknown/withheld values, strict packet parsing, scope/root binding, altered retained answers, output refusal and historical inspection. A simulated `os.link` failure checks absence of a published destination; it is not a real process-crash or power-loss experiment.

The writer publishes one complete exclusive file outside the observed repository. It does not guarantee survival of unrecorded preflights, directory-fsync durability, latest-history selection, anti-fork protection, producer authentication, exactly-once effects or a continuous current view. Both reports and nested receipts retain no authority, no LLM use and incomplete/unobserved external state.

Existing finite semantic evidence remains bound to its original programs. The additive byte API does not relabel old records as observations of the new program. The source PR runs the existing semantic suite again and adds consumer/lab steps to normal CI. The 450-run language-model plan is unexecuted; cost is `NOT_MEASURED`.

## Next use

The prepared input for KC-SWE is the exact source revision, the two reproduction commands in Rule Consumption, the fixed expected inventory and these retained outcomes. Separate exact-revision review and an intended-environment replay precede any broader release claim. A site journal entry can describe this result while retaining the live interface's unconnected state. No new execution-system task, runtime authority or paid experiment is inferred.

Rollback is a reviewed revert of this source increment. Previous evidence and already integrated source remain separately recoverable.

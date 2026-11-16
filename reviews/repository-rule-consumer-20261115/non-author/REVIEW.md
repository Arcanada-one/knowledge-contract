# Repository Rule Consumer: bounded non-author review

Reviewer: `/root/mailbox_status`, 15 November 2026. The reviewer did not author the new consumer or the additive packet-byte API. Author and reviewer share controller/workspace; external independence is **NOT_VERIFIED**.

## Scope and expectations

The review covers `tools/repository_rule_consumer.py` and the additive `parse_packet_bytes` change in `tools/semantic_bridge.py`. The existing Observer, Session and Agent Situation model were read as dependencies; they were not modified. Broad semantic-space tests and real-Git lifecycle controls belong to the separate test lane and were not repeated here.

`EXPECTATIONS.md` was recorded before probes. It covers early capture-count refusal, strict packet JSON, exclusive outside-repository publication and limited claim semantics. All commands in this review are local read/probe operations. No API writes, mailbox actions, deployment, model calls or grants were performed.

## Finding RC-01: capture bound was checked after replay

Baseline consumer SHA-256:

`11a1f99f3a1866ca59278f0b0d1d602b09a2afba025d656addfce0a5a7a8962f`

`validate_bundle` invoked `session.validate_receipt`, including full ledger replay, before comparing sequence with `MAX_CAPTURES=32`. Consequently the advertised count limit constrained accepted output but not replay work on untrusted input. A false small sequence also reached the larger ledger before its inventory mismatch was rejected.

`probe_capture_bound.py` starts with one actual temporary Git capture. It creates deliberately synthetic, structurally reconstructed 32/33-entry histories; these are hostile-input controls, **not claims of 32/33 actual observations**. The wrapper records the actual replay calls and executes the original replay function. The inputs and original modules were saved before the author correction.

Observed baseline results (`pre-fix-cap/RESULT.json`):

| Input | Outcome | Ledger entries actually replayed |
| --- | --- | --- |
| Consistent32 | Accepted | 32 |
| Consistent33 | Refused, capture bound exceeded | **33** |
| Claimed sequence2 with33 retained entries | Refused, inventory mismatch | **33** |

Each mutated bundle is approximately0.49MiB, below the32MiB input-byte ceiling. No oversized memory experiment was needed. This is an ordering/resource-contract defect, not acceptance of a semantically valid33-capture result.

Required correction: inspect bounded cheap shape, actual ledger-entry count and claimed sequence before digest/replay; neither a small forged sequence nor an oversized ledger may enter replay. A legitimate32-entry history remains accepted. The same script is the re-review criterion.

## Strict packet-byte API

Bridge SHA-256:

`b8363fa17e9090f28e4010357b00f4527cf812b3740e5e6382ebd15624195e25`

`probe_packet_bytes.py` passed7/7 focused controls at `PYTHONINTMAXSTRDIGITS=4300`: valid object; nested duplicate member; NaN; malformed UTF-8; a5000-digit integer; input beyond the131072-byte ceiling; non-bytes input. Duplicate/nonfinite codes were preserved; malformed UTF-8 and integer-limit failures became typed `BridgeError(malformed_json)`. `PACKET_RESULT.json` retains the exact expectations and outputs. This is API syntax/error handling evidence; it does not requalify the semantic evaluator or natural-language interpretation.

## Other source-review conclusions

- Both selected paths must be the complete required profile. Calculations read the fresh capture's committed byte records and compare their identities to the adopted dependencies; they do not reopen the worktree after preflight.
- A non-VALID preflight blocks evaluation. A READY candidate cannot replace the adopted context through evaluation; the consumer checks `resume_required` and the adopted-context identity before calculation.
- `EVALUATED` means the controlled calculation completed. FALSE or UNDETERMINED truth remains a legitimate evaluated result, not granted permission or proof of usefulness.
- Historical inspection reports `HISTORICAL_ONLY`, `requires_fresh_capture=true`, and no effect authority. Producer identity, complete history, current authority and real-world truth are not promoted by hash replay.
- New CLI output refuses an existing destination and requires a resolved destination outside the observed repository. The unchanged writer uses a same-directory flushed/fsynced temporary file and exclusive hard-link publication. This supports complete-new-file publication in the declared local profile. It does **not** establish parent-directory fsync/power-loss durability, authenticated provenance, unique global history or exactly-once execution. The separate lifecycle test lane probes refusal and simulated publication failure.
- The implementation hash binds selected code bytes. It is not a signature, trust anchor, currentness observation or proof that synthetic historical captures actually happened.

## Successor re-review and disposition

**Bounded PASS; RC-01 closed** on consumer SHA-256

`17f591ee66540dc70d3a41f121fcfd2d00e72803ada7127fa95830dc4b1e524c`

The Bridge remains `b8363fa17e9090f28e4010357b00f4527cf812b3740e5e6382ebd15624195e25`. The correction checks the actual cheap nested shape, exact integer sequence1..32 and ledger-entry length before digest or replay. The same retained probe now reports:

| Input | Outcome | Ledger entries actually replayed |
| --- | --- | --- |
| Consistent32 | Accepted | 32 |
| Consistent33 | Refused, capture bound/inventory | **None** |
| Claimed sequence2 with33 retained entries | Refused, capture bound/inventory | **None** |

`post-fix-cap/RESULT.json` contains the actual output and successor identity; pre-fix artifacts were not overwritten. No additional blocker was found in the reviewed operations. The32MiB serialized input/output limits are CLI persistence bounds, not a claim that arbitrary Python object construction consumes at most32MiB. This bounded result cannot be presented as whole-system, native-runtime or independent scientific acceptance.

## Additional read-only runner inventory check

Reviewed `tools/run_repository_rule_lab.py` at SHA-256 `657935f1dbd49fde4eb74c5e85639a06220d6af8c239e07d96112c328ebbc831` and its case inventory at `d6951b85137df601354df6b9687aa9694eff09a032792805b2cde4469392c61e`.

The runner records the selected plan before invoking the consumer. It requires the exact ordered12 registered case IDs; a missing/duplicate/reordered/injected noncase does not create a reduced passing suite. It appends an executed record after the subprocess returns, retains stdout/stderr, and checks exact expected outcomes. A failed case stops the run; completed/pass totals and the not-executed list remain distinct. PASS additionally requires the complete registered inventory, every case passed, no failure and unchanged implementation/inventory hashes. These are12 stages of one authored lifecycle, not12 independent episodes. The two source tests cover each missing member and duplicate/reordered/noncase variants; I read them but did not rerun them.

The retained initial fixture run is correctly **FAIL: planned12, executed2, passed1, complete=false**, with ten not executed. I compared `runner_before_fixture_fix.py` with the current runner: the only change adds required `referent` and `type="boolean"` fields to each supplied observation. No case expectation or validator change appears in that diff. The retained failure is a fixture-author error, not evidence that the consumer accepted invalid input. The later full runner result is outside this review's execution claim.

## Retained files

- `baseline/`: exact original consumer, Bridge, Session, Observer, model and their manifest.
- `pre-fix-cap/`: seed receipt, both sized histories, false-sequence input, expectations and actual result.
- `probe_capture_bound.py`: reproducible counterexample and successor criterion.
- `probe_packet_bytes.py`, `PACKET_RESULT.json`: finite byte-API controls.
- `EXPECTATIONS.md`: pre-probe scope and expected outcomes.

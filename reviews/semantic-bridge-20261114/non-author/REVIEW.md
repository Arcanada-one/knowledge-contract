# Semantic Bridge: bounded implementation review

**Disposition: PASS after one resolved input-error finding.** This review is bound to `tools/semantic_bridge.py` SHA-256 `0b049720da90a0b53f190bc720b78f9bbf4bf9940313c4c65cb699d2ae5a0d6a`, on source base `d5e684e201f6d41498c4fbd8c2a3497eed2bb30e`. The reviewed draft specification has SHA-256 `fba25935adf19b69a2070039c175b315cbd8e874fa48a090ea1459f4b3741d0a`. This is an exact-file review of a local candidate, not a hosted CI or merge claim.

Reviewer `/root/mailbox_status` did not author or edit the implementation. The reviewer authored the probes and this record. Author and reviewer share the controller and host; external independence is **NOT_VERIFIED**. The machine-readable [review record](review-record.json) binds the retained files to their hashes.

## Resolved finding SB-REVIEW-1

The initial module, SHA-256 `395fd92911688cc688b01405b001bf03a4d786811e4bef47604235db98cf46f3`, accepted a bounded input file into JSON decoding but did not normalize every decoder failure. A 5,341-byte JSON packet, below the 131,072-byte packet limit, contained a 5,000-digit integer in its byte selector. Python's integer-conversion limit raised an ordinary `ValueError`. The CLI escaped with exit 1, a traceback and no report, contradicting the declared complete-or-refused result contract.

The exact initial [module](semantic_bridge_reviewed.py), [source](integer-bound-source.txt), [packet](oversized-integer-packet.json) and [actual failure](oversized-integer-result.json) are retained. They are actual local executions on newly authored inputs, not historical production observations.

The author corrected `read_packet` to preserve `BridgeError` and then convert ordinary `ValueError` and `RecursionError` into a structured decoding refusal. On the [successor bytes](semantic_bridge_successor.py), the same saved packet in a fresh CLI process with `PYTHONINTMAXSTRDIGITS=4300` returns exit 2, `INVALID`, `malformed_json`, no evaluated truth and empty stderr. The [actual successor result](oversized-integer-successor-result.json) is retained. Recursive duplicate-member and non-finite-token error codes remain intact in the separate input checks.

## Bounded checks

The separately authored [review checks](review_checks.py) completed 30 named probes, recorded in [bounded-review-results.json](bounded-review-results.json). These check source/packet contracts and result boundaries; they do not replace the separately authored arithmetic oracle.

- Exact multilingual UTF-8 byte positions with CRLF succeed. A changed source, clipped exception, wrong quote and Boolean byte offset refuse evaluation.
- Missing, duplicate and extra reading records refuse evaluation; duplicate source identities also refuse. A required unsupported alternative blocks the whole set after successful byte binding and produces no evaluated truth.
- Root and recursively nested escaped-equivalent duplicate JSON keys refuse. Non-finite tokens, malformed JSON, unknown reading members and an unpaired Unicode surrogate refuse.
- Shared observation identities remain correlated for `p AND NOT q`; unknown and withheld states retain their distinct labels. `p` and `NOT p` retain source order, tables `01` and `10`, and same-world disagreement.
- Zero observations with a constant expression produce one empty world. Exact source and packet byte limits succeed; the corresponding one-byte excesses refuse. AST depth 16, node count 128 and expression length 4,096 have explicit at-limit and over-limit checks.
- Every analyzed result keeps `effects_authorized: false` and the four unperformed semantic/factual/authority assessments at `NOT_ASSESSED`. Refused results contain no evaluated truth or partial readings.

Expected source spans were constructed from supplied complete byte strings without calling the implementation's source-unit extractor. No model, network service or remote application was invoked by these checks. The original implementation and old failure were not rewritten after correction.

## Limits and remaining responsibilities

No further blocker was found in the inspected source-binding, inventory, strict-input, finite-bound and result-status scope. This does not prove whole-program correctness. The evaluator's AST precondition is an output of the controlled compiler; arbitrary caller-built AST validation is outside the declared API contract.

The profile deliberately accepts supplied interpretations and factual observations as assumptions. Exact bytes and correct Boolean arithmetic do not establish their fidelity, authenticity, truth or current authority. General language extraction, rendered-source visibility, native admission and real external effects remain outside this review. A later change to the implementation requires review against its new exact bytes.

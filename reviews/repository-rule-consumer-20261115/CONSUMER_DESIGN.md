# Captured Rule Consumer: bounded acceptance design

This is a prospective internal test design for the next offline laboratory increment. It is not an execution report, an independent external review, a natural-language fidelity result, or a grant to act. Expected outcomes in `CONSUMER_CASES.json` were authored before the first consumer test run. They follow the supplied Boolean rule and the already accepted Session adoption contract, rather than calling the consumer to obtain an oracle.

## Source baseline and missing connection

Knowledge Contract main was read at `a5b3618034256f14f389c2c7de8da409c7c5310c`, tree `34ba36d05a0768a3a86c056dfe74da26b2341bfc`. The exact source snapshot and retrieval records are in this directory. Integration PRs 115, 116, and 118 already brought Observer, Session, and Semantic Bridge into main; an older source PR remaining open is not evidence that its integration is still pending.

The accepted Session pins committed file identities and requires explicit adoption after a failed preflight. The standalone Bridge can evaluate source and packet paths supplied by its caller. Neither contract alone binds a Bridge calculation to a Session context. A naive composition can preflight committed pair A, then read a dirty but internally consistent pair B from the working tree and report B under A's context. This is a missing consumer connection, not a defect in either standalone contract.

The proposed consumer closes only that connection: both selected paths are required; a fresh successful preflight precedes each new calculation; the input bytes come from that capture's ledger; the output records their identities and the adopted context. This is an actual repository adapter integration, not the planned LLM experiment, native Live Lab execution, causal performance evidence, or the complete Semantic Bridge fidelity problem.

## Frozen profile

- Exactly two distinct, normalized relative paths: one source and one interpretation packet. Both are the complete selected and required file set. Unrelated files and repository HEAD alone are deliberately not dependencies of the formal calculation.
- The existing Session profile supplies task, scope, producer, local repository address binding, and abstract context budget. The repository address digest is not repository ownership, identity certification, or authorization.
- `START` and `RESUME` only capture and adopt; their `analysis` and `bindings` remain null. `EVALUATE` uses Session `PREFLIGHT`. A new report is computed only for a `VALID` preflight with no resume latch and with current context equal to the adopted context.
- A changed required committed file blocks the new calculation even when the newly observed candidate is READY. Repeated preflights retain the latch. Only an explicit successful RESUME adopts the new context.
- Captured file bytes must be PRESENT in an OK capture, with identity `{blob, mode, size, sha256}` equal to the adopted dependency identity. Hashes bind raw bytes, without Unicode or JSON normalization. Working-tree bodies remain NOT_OBSERVED.
- Bridge parsing retains its current strict UTF-8, duplicate-key, finite grammar and size policy. A public `parse_packet_bytes` is an additive decoding entry point with the same behavior as the file reader. File-context readiness does not imply packet validity or formal truth.
- Current fixed outer bounds are 32 captures and 32 MiB serialized input/output bundle. Existing source and packet limits are 65,536 and 131,072 bytes. The capture bound is an upper bound, not a promise that any maximum-size 32-capture history fits the byte bound. No silent truncation or automatic history reset.

## Bundle evidence

The bundle carries the operation, exact role-to-path mapping, full nested Session receipt, input identities, full Bridge report or null, result, predecessor links, and consumer/Bridge implementation hashes. The Session itself pins Session, Observer, and model implementations. The committed-file evidence scope is explicit. History completeness and effects authorization remain false; LLM calls remain zero.

Validation replays the nested Session and recomputes a retained Bridge report from captured bytes. This detects an altered truth report even if the attacker recalculates the outer digest. It proves internal consistency, not the authenticity of the producer or a global unique history. A fully rewritten consistent chain is not authenticated. The caller selects a predecessor; stale-branch selection is not globally prevented.

“No calculation after a failed preflight” means no new analysis of the newly blocked capture. Validating a previous successful bundle may recompute its historical analysis. These are different events and must not be reported as a new accepted observation. Historical inspection performs no Git acquisition and always requires a fresh capture before use as current state.

## Independently stated outcomes

The public authored rule is `member UNLESS suspended`, with the interpretation of UNLESS already fixed as conjunction with negated exception. Known member=true and suspended=false gives TRUE. Known member=true and suspended=true gives FALSE. Unknown or withheld suspension produces worlds with both outcomes and therefore UNDETERMINED; the two observation states remain distinct in the report. `XOR` is outside the grammar and gives UNSUPPORTED. Duplicate JSON members and a mismatched source digest give INVALID. None of these results grants permission, verifies the real observations, or certifies source-language interpretation.

The fixed inventory contains twelve test functions, with explicitly listed subcases. The important positive controls are an unchanged valid pair, an unrelated commit, and successful explicit adoption after a relevant change. Negative cases cover the missing composition rather than another broad mutation campaign. The fixed inventory is a finite acceptance criterion for this consumer profile; it does not prove all arbitrary inputs or close broader SEM-R015.

## Publication and interruption

The CLI publishes one new complete JSON envelope outside the observed repository using the existing exclusive writer. The destination is never overwritten. A temporary file is fully written and flushed before the final exclusive link. A simulated failure at that link should leave no published result and preserve the predecessor; this is not an observed process-crash or power-loss test.

If an attempt stops before publication, the unrecorded in-memory preflight and calculation remain unknown. Retry from the last published predecessor performs a new preflight. In particular, the consumer does not promise to recover a failed-preflight latch from an attempt that never published its bundle. A failure after publication but before stdout may leave a complete bundle; read and validate that bundle rather than replacing it. The protocol makes no exactly-once, complete attempt-history, directory-fsync, or power-loss durability claim. Every published failed-preflight bundle carries the latch into the next invocation.

## Completion criterion and review boundary

Acceptance requires the fixed twelve integration tests to pass against recorded unchanged implementation hashes, including genuine temporary Git repositories and fresh CLI processes. The pre-existing Bridge, Session, and Observer suites remain separate regression controls; their earlier observations are not recast as newly discovered behavior. A concrete failure is retained with exact code/input/result before a correction. A corrected run receives a new record.

This design and the tests are authored separately from the consumer implementation but within the same controller, host, and model family. They are internal non-author checks. Remaining work includes independent review, broader production consumers, authenticated provenance, live authorization and effects, the paid-model experimental protocol, and native laboratory admission. None is inferred from this bounded success.

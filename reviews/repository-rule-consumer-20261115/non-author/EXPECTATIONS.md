# Bounded non-author review: repository rule consumer

Reviewer: /root/mailbox_status. Same controller/workspace as author; no external independence.

Before probes, expected outcomes:

1. A saved bundle claiming more than 32 captures, or carrying more than 32 capture entries despite a smaller claimed sequence, is refused before session replay. The 32-capture limit must bound work on untrusted input, not only eventual accepted status. Probe may instrument the call boundary while executing the real validator; it must not replace validation logic.
2. Strict JSON packet byte API preserves duplicate-member/nonfinite refusal codes and turns malformed UTF-8 / interpreter integer-limit failures into a typed BridgeError; it never upgrades malformed input to EVALUATED.
3. New evidence is published exclusively outside the observed repository. Existing output, an output inside the repository, or a destination occupied before exclusive publication is not overwritten. A failure before publication leaves no partial destination; retained predecessor bytes remain unchanged. Process/publication behavior does not establish directory fsync or power-loss durability.
4. Result statuses describe committed-file observations and controlled calculations only. Historical inspection cannot assert currentness, producer authentication, semantic admission or effect authority. A whole recomputed hash chain is not authenticated history.

Scope: new consumer and additive parse_packet_bytes only; no re-run of broad legacy suites or native effects, no mailbox reads. Inputs and module bytes for a counterexample are retained before author correction. Real-Git lifecycle tests are owned by a separate reviewer/author lane.

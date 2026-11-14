# Finite agent situation prototype

Status: **author-draft reference demonstration**. This implements the bounded deterministic state/projection contract copied verbatim into checks/DESIGN_INPUT.md. Eighteen expected controls were declared before implementation; three regressions were added after same-controller non-author inspection. These are not an independent preregistration, external benchmark, or empirical evaluation of an LLM. No study conclusions are supplied here.

## Run

```sh
KC_SITUATION_RUN="$(mktemp -d)"
cp -R engineering/studies/agent-situation-controls/. "$KC_SITUATION_RUN/"
python3 -B "$KC_SITUATION_RUN/checks/check_agent_situation.py" --evidence "$KC_SITUATION_RUN/evidence/finite-run.json"
python3 -B -m unittest discover -s engineering/studies/agent-situation-controls/checks -p test_inventory.py -v
```

Python 3.10 or later; standard library only. The runner writes finite-run.json and execution.txt, records the actual command/runtime, and exits nonzero if an authored control fails or a disabled-guard variant fails to expose the intended error. The JSON contains inputs, full operation outputs, literal expected outcomes, counts, source SHA-256 digests and limitations. The three mutation runs deliberately bypass freshness, mandatory closure and scope checks. These are discriminating authored negative controls, not proof of exhaustive mutation coverage or independent review.

## Implemented semantics

- An observation records key/scope/source/event/sequence/value-state/time/receipt/TTL/dependencies. UNKNOWN differs from known false, zero or null. Explicit conflicts and disagreements between independent source labels remain unresolved.
- Source identities are fixture labels. Monotonic sequences are per (scope, source) stream. Lower/equal new sequence events are rejected; there is no inferred causal order between independent streams. Producer restarts require a new stream identity.
- Event IDs are namespaced by source. Logical event payload excludes receipt metadata. Identical replay preserves the first receipt and observation time; inconsistent ID reuse is rejected without replacing accepted facts.
- TTL is expired at age >= TTL, measured from observation time. A future observation relative to receipt stays invalid. A backward model-clock observation makes the model invalid until a new instance; no silent clock recovery is attempted.
- A derived observation carries explicit dependency version pins from derivation. Missing pins block readiness, mismatched pins invalidate the claim, and a premise first received after the derivation timestamp is rejected as a temporal mismatch. Receipt never rebinds old derivations to current premises. Any later direct update invalidates the claim; unresolved transitive dependencies also block readiness. There is no automatic re-derivation.
- Required projection includes all transitive dependencies. If they exceed budget, NOT_FIT returns their names/cost and an empty included view; no partial mandatory view is called ready. Unknown, missing, stale or conflicted critical facts yield NOT_READY.
- Optional ranking follows the supplied ordered list, deduplicated stably; optional inputs and their dependencies never displace mandatory content. Omitted optional facts carry explicit reasons. Costs are positive abstract integers, not token measurements.
- A ready snapshot records model identity, scope, model generation and critical per-key versions/closure. The model retains its canonical issued contents; validation rejects modification or omitted pins, and rechecks scope, versions, closure and current readiness. This is a local integrity check, not a cryptographic security boundary. Unrelated generation changes do not invalidate a snapshot. Optional facts are not certified as critical prerequisites by this snapshot.
- Refresh distinguishes relevant changed facts, heartbeat/unchanged messages, expiry polling and pre-action checks of critical closure. Returned request flags are hypothetical; no observations, model calls or effects are executed.
- A known false revocation fixture can itself be structurally ready. This illustrates why readiness is not permission. There is no grant authority or automatic retry mechanism.

## Layout

- situation.py: typed in-memory reference model.
- checks/check_agent_situation.py: finite scenario runner and three intentionally broken subclasses.
- checks/expected.json: literal expected outcomes, separate from implementation.
- checks/DESIGN_INPUT.md: exact pre-implementation design bytes, included for portable provenance.
- evidence/finite-run.json: actual execution evidence.
- evidence/execution.txt: actual command and compact results.
- development/v1/: preserved initial sources and passing 18-control run, plus the review counterexample that demonstrates a bug missed by that initial suite.

## Development correction

The first run passed 18 controls and detected three mutants, yet a reviewer reproduced a delayed-derivation error: a claim derived from an old premise was bound to the new premise version at receipt and incorrectly became READY. The preserved counterexample records expected NOT_READY and actual READY. This was a real implementation defect missed by the authored suite, not evidence of independent acceptance. The correction requires explicit premise pins and checks their temporal consistency. Added controls cover missing/old/impossible pins, valid delayed matching pins, and modified snapshot rejection. The final evidence reports 21 controls separately from the original 18-control contract.

## Unimplemented and assurance boundary

### Control inventory correction

A continuation review found that the original runner could silently omit a registered control: removing case 21 left 21 fixtures, but a truncating pairing ran 20 cases and still returned success. It also counted 87 fixture fields although only 84 belonged to executed controls. The original complete 21/21 run remains valid within its stated scope.

The current runner checks an exact correspondence between declared IDs, unique callables and expected fixtures before execution. It counts performed field predicates, binds mutants by control ID and requires the complete executed inventory for success. Nine behavioral registration/accounting checks cover the repaired boundary; all nine, the original 21 controls and three mutants passed. The runtime model and expected outcomes are unchanged.

The original runner is preserved byte for byte in [development/inventory-baseline](development/inventory-baseline/README.md). The original payload manifest and finite/execution reports describe that historical runner. The original origin bytes are archived alongside it; the current origin retains its original entries and adds the successor records. The successor has a separate [receipt](evidence/20261114-inventory-receipt.json) and [review](../../../reviews/agent-situation/20261114-INVENTORY.md). This repair and its tests share a controller/model family; they are not independent scientific acceptance.

### Implementation limits

No live sensors, accounts, tool adapters, network, LLM, effects, grants, token budgeting, durable storage, restart recovery, distributed clock reconciliation, probabilistic confidence calibration, optimal refresh scheduling or general intention scheduler is implemented. Snapshot data and source labels are not cryptographically authenticated and are not an adversarial security boundary. The model is an in-process demonstration with no concurrent writes.

The finite cases are author-designed and reviewed under the same controller/model family. Actual independence is NOT_VERIFIED. Passing controls means only that these finite expected outcomes matched the implementation and selected mutants were detected. It does not establish safety, optimality, completeness, externally measured agent performance or native admission. Native admission remains NOT_VERIFIED.


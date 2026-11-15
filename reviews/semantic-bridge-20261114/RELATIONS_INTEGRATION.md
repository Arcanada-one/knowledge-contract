# Computed rules and finite semantic relations

This internal integration check connects actual `semantic_bridge.analyze` output to the existing `semantic_relations` API. It does not add a representation profile, a new model or a general proof. The only repository code added by this task is `tools/test_semantic_bridge_relations.py`; neither implementation module was changed.

## What is connected

The bridge evaluates supplied controlled rules over a declared finite list of worlds. In these tests, a world's row index identifies a source state, and Boolean false/true identify target states 0/1. Each computed table bit supplies an actual relation edge. A false answer is an edge to 0, not an empty image. The largest source carrier has eight states; all carriers satisfy the existing API bound of twelve.

The examples concern a hypothetical camera-lending condition and two explicitly supplied eligibility readings. They are authored controlled inputs. No natural-language extraction, real policy adoption, factual measurement or permission is inferred.

## Fixed acceptance inventory

| Integration obligation | Actual check and observed outcome |
| --- | --- |
| Computed truth tables support only sufficient observation quotients | The eight-world table for `(member AND trained) UNLESS suspended` creates an 8-by-2 relation. Partitioning inputs by `(member AND trained, suspended)` gives four classes of sizes 1, 1, 3 and 3 and passes exact quotient coherence. Distinct representatives in the two three-member classes have identical observed outputs. Omitting `suspended` produces an incoherence witness: two qualified worlds disagree on suspension and on the result. |
| Two computed stages compose through an explicitly shared interface | The first table is followed by a separately computed `NOT flag` table whose world rows are explicitly false then true. Concrete composition equals a direct bridge computation of the negated lending formula. Composition of the coherent quotients equals the quotient of that direct result. A three-state intermediate carrier is rejected. |
| A narrower bridge domain needs an explicit embedding | With `flag=true` known, the second bridge has one world. Its local row 0 denotes true, not Boolean false. Direct composition with the two-state Boolean result carrier is rejected. Explicitly embedding that one row as Boolean state 1 yields one successful composite path and seven empty source images. The metric API rejects these images because its declared domain requires every image to be nonempty. |
| Marginal outcome geometry does not recover shared-world correlation | `(member OR guest) AND trained` and `member OR (guest AND trained)` each have global possible outcomes `{false,true}`. Their outcome-set Hausdorff distance and the Lipschitz constant of that two-reading marginal map are both zero. The actual tables nevertheless disagree in two of the eight shared worlds; their singleton outcome distances in those worlds are one. The bridge reports disagreement and an undetermined combined truth. |

The third result is a caller-side composition obligation, not a defect in either module. Integer carrier sizes and row positions do not certify a shared interpretation. A caller supplies the correspondence of intermediate states. After a correct embedding, successful-path composition may be partial; an empty image is not an observed refusal, false result, failed execution or permission decision.

The fourth result does not challenge the existing finite Hausdorff theorem. The compared marginal sets have deliberately forgotten their world labels, and the zero distance is correct for those sets. A question about agreement under the same conditions requires retaining that conditioning information. Equality under one observation family does not justify substitution under a stronger family.

## Execution and evidence

The command was executed from the prepared repository working directory:

```sh
python3 -B -m unittest tools.test_semantic_bridge_relations -v
```

Observed result: four tests passed, zero failures/errors, reported unittest duration 0.003 seconds. `RELATIONS_INTEGRATION_TESTS.txt` preserves the actual combined subprocess output without alteration. `RELATIONS_INTEGRATION_RUN.json` binds the test and both implementation files by SHA-256 before and after that run; all three files remained byte-identical. No analytical test counts are substituted for execution.

An earlier run also passed four tests, but its source hashes were collected after a concurrent implementation correction. Its original log and metadata are retained as `RELATIONS_INTEGRATION_TESTS.initial.txt` and `RELATIONS_INTEGRATION_RUN.unbound.json`; that metadata is not evidence of which implementation bytes executed. The current record comes from a fresh bounded run after the author froze the module. The implementation change addressed a separate JSON-reader error path; this integration task did not edit either module.

These four integration checks supplement the separately authored finite oracle for each implementation. They do not repeat the full Boolean function or relation/geometry enumeration, validate arbitrary report ingestion, or establish a performance advantage. The packet construction is an authored fixture, and the test helpers use only the two modules' public interfaces.

All positive bridge calls retain `source_semantic_fidelity=NOT_ASSESSED`, `current_authority=NOT_ASSESSED` and `effects_authorized=false`. The review and tests share a controller and environment with the implementation author; this is internal assessment, not independent external evidence. No remote write, catalogue change or publication claim was made by this task.

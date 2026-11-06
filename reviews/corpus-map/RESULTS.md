---
title: Typed corpus map verification record
sources: none
status: observed local structural checks; independent semantic review outstanding
---

# Typed corpus map verification record

KC-Brain ran the offline validator and fourteen unit controls under Python 3.13.5. The validator returned exit 0; all fourteen controls passed. A second validator invocation reproduced the JSON byte for byte. These observations concern the map, not execution of an agent, a paper theorem, a server or a site.

Commands:

```sh
python3 -B tools/verify_corpus_map.py
python3 -B -m unittest tools.test_verify_corpus_map -v
```

Exact measured result:

```json
{
  "bytes": 32073,
  "counts": {
    "claims": 9,
    "documents": 9,
    "explicit_relations": 99,
    "foundation_units": 6,
    "nodes": 65,
    "required_output_edges": 45,
    "roadmap_nodes": 25,
    "terms": 16
  },
  "errors": [],
  "runtime_readiness": "not_established_by_this_check",
  "semantic_review": "not_established_by_this_check",
  "sha256": "9a8de34c8b327032b42ef01823ead63030ef9d70adf4fb63d13d4f17efc3050d",
  "site_delivery": "not_established_by_this_check",
  "source_objects": {
    "reason": "No local repository supplied; connector source reads are separate evidence.",
    "status": "not_run"
  },
  "structural_valid": true
}
```

Verification source hashes:

- `tools/verify_corpus_map.py`: `91d4597dd47c782d813485615b6e08cc598c25e928afbdcee2b793f59e03fdbb`.
- `tools/test_verify_corpus_map.py`: `585ce2160e56abfbf005a04f769637ca058670e2317eaf962b0cb7d7b97f1e73`.

The source-object mode requires a local repository containing every pinned object and was not run here. Source existence, full-text review, external peer review, actual Muneral readiness, catalogue integration, current repository CI, merge, served layout and indexing are not established by these local results. The same producer authored the map, validator and controls. Fourteen controls are fourteen program tests, not fourteen independent semantic judgments.

## Corrections prepared after the independently reviewed baseline

The independent [map review](https://github.com/Arcanada-one/knowledge-contract/pull/48#issuecomment-6693915599) found a missing C03 initial premise and a default source-binding rejection gap. The author has corrected C03, added a required source/locator guard for all source-backed groups, and prepared eight additional negative unit controls.

The JSON and hashes above are **historical measurements of the prior map/checker**, not a rerun on these changed bytes. Exact-head Python and project checks, optional `--repo` validation, new map digest, independent delta review, corpus integration and site readback are **not measured by this record**.

## Accepted-main source-pin reconciliation (author prepared, not executed as a new test run)

At Knowledge Contract PR48 parent `e69f5d4e90fae0453de9b6e38e32937b105f2345`, the source dictionary's five historic PR-head pins were replaced by the following accepted `main` commit pins after comparing **both full file texts and Git blob IDs** through the repository API:

| Source key | Previously pinned PR head | Accepted main commit | Independently matched file / Git blob |
| --- | --- | --- | --- |
| `roadmap` | `42a10bd178e003f9615e8a58f8bfb7cf9d76c07b` | `fb410a8460677b229d2240ba0fb27d184f48aa61` | `roadmap/dependencies.json` · `d0b83e117c6cc08d9f644a8d9994e22c3ad79e09` |
| `transformations` | `2b863b45441da4b6dc6bdcadec046290285aed50` | `3d9b184b15fdee2e67bb0a2dc2aa5815b54364d5` | `papers/constrained-transformations/PAPER.md` · `57e7f2f9bb5de51d000b8c2ff8b3f90a01bb1b7e` |
| `retrieval` | `ef6e223a9be6ac1a420556c07e584f0369bdc41f` | `b29ca5bfb5354147549d9e803c8382e7ab917631` | `papers/retrieval-and-context-composition/PAPER.md` · `9311c0d157d5a926e3c08f6a087a53866064f4e0` |
| `interaction` | `8273f4eaf8bcf97de9a34c7890f0e54da3eecf45` | `f5b939855a7bff67af7a0d761b4651cd0a8b3f9c` | `papers/interaction-and-memory/PAPER.md` · `aa3aa4beb9a8e470e830cceb2b100f3e6fe24883` |
| `evidence` | `b97ecd3f650f4aab566860c4a21b754ffd15a18a` | `aa3ae405639aa8e953cd6901a0fd3b95a8ddccc3` | `papers/evidence-and-falsification/PAPER.md` · `54cbff6b47cf86a90fc6a23c9b74b3ebf8d5d6a9` |

This is an identity-preserving pin repair for the listed checked files, not a fresh semantic review, a whole-source-graph equivalence proof, CI result, accepted F01 source, site build or index admission. The `f01` source still deliberately points at its proposal commit. The numeric validator output and SHA-256 recorded above remain **historical for the earlier map**; do not reuse them as current-head measurements. The new map must be validated again after this commit and independently reviewed against its exact Git blob.

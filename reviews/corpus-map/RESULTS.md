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

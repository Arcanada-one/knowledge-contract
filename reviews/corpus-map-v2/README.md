---
title: Inventory-first candidate corpus map /2
sources:
  - Inventory-first candidate corpus map /2
status: candidate fixture; not published, not indexed, no source read by this build
---

# Inventory-first candidate corpus map /2

This directory holds a candidate `knowledge-corpus-map/2` built for Muneral task KC-MAP2-1. It is a structural fixture. It is not a published map, a bibliography decision, an index admission or evidence that any listed work supports any claim.

## Inputs

- `reference/foundations/corpus-map.json`: the accepted /1 map. Every /1 group is carried over unchanged. Only `record_type` changes, and two descriptive relation meanings required by /2 are added.
- `V2_REFERENCES.tsv`: KC-Brain's historical v2 reference inventory, copied byte for byte from pull request #67 at commit `5e1837a0`. The Git blob `578bf239` is checked on every run. The inventory is a proposed reading list, not accepted bibliographic truth.

## Rules applied

- One source record is emitted for each inventory row whose own text states a DOI or a URL. The identifier is copied from that text. No identifier is derived. For example, an arXiv number is not turned into a URL, and no ISBN is looked up.
- Each record's `title` is the verbatim historical citation, not a parsed title.
- `retrieved_at` is null because this build opened no source.
- `historical_v2_label` is the legacy verification label. It is a historical label only.
- KC-Brain approved no claim/source pairs, so the map has no evidence assessments and no `claim-has-ground` or `ground-uses-source` edges.

`MANIFEST.json` records the input hashes, the counts and every excluded row with its reason.

## Checks

```sh
python3 -B tools/build_corpus_map_v2_inventory.py --check
python3 -B tools/verify_corpus_map.py --map reviews/corpus-map-v2/corpus-map-v2.inventory-candidate.json --repo .
python3 -B -m unittest tools.test_corpus_map_v2_inventory -v
```

The first command rebuilds the candidate from the pinned inputs and requires byte equality. It also requires an unchanged /1 base, identifiers that occur in the row text, and no retrieval claim or link. The validator checks the /2 structure. Passing either check is not a scientific review.

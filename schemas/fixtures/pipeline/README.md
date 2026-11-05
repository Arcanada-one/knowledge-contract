# Synthetic pipeline receipt chains

Every receipt here is invented for this repository. `valid/` holds twelve chains: all nine stages, `convert` skipped, `classify` and `convert`
skipped, and one that ends in a refusal at each of the nine stages. Each directory under `invalid/` is a mutant of the first valid chain with one defect and one expected refusal code
(see `EXPECTED` in `tools/pipeline_fixture.py`). Regenerate with
`python3 tools/pipeline_fixture.py write`; the unit tests fail if the committed files drift.

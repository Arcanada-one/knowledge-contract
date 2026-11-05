# Synthetic pipeline receipt chains

Every receipt here is invented for this repository. `valid/` holds one chain of nine stages; each directory under `invalid/` is a
mutant of it with one defect and one expected refusal code (see `EXPECTED` in `tools/pipeline_fixture.py`). Regenerate with
`python3 tools/pipeline_fixture.py write`; the unit tests fail if the committed files drift.

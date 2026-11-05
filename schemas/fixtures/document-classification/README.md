# Synthetic document classification results

Every file here is invented for this repository. `valid/` holds twelve results, one for each boundary case of the `kc-doc-class/1` canon (`engineering/specifications/pipeline/document-classes.json`); passing them is a statement about those cases only, not about the accuracy of any classifier. Each file under `invalid/` is a mutant of a valid one with one defect and one expected refusal code (see `EXPECTED` in `tools/document_classification_fixture.py`). Regenerate with
`python3 tools/document_classification_fixture.py write`; the unit tests fail if the committed files drift, and they also fail if the canon file changes without the fixtures being regenerated (every file carries the digest of the canon).

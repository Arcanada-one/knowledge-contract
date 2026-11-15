# Semantic Verification: Scoped Reference Review

## Status and scope

This packet retains the reconstruction, execution and internal review of the
finite fibrewise reference checker supporting
[Semantic Verification](../../engineering/specifications/semantic-verification/SPECIFICATION.md),
Sections 7 and selected acceptance cases in Section 8. It is a supporting
review record, outside the publication catalogue and claim-evidence study
index. It does not claim completion of Meaning Controls, whole-specification
conformance, independent scientific acceptance or runtime admission.

The repository baseline is
`a5b3618034256f14f389c2c7de8da409c7c5310c`. The mathematical source is Pavel
Valentov, *Meaning Geometry*, edition 1.1, research draft, Proposition 2,
[at that revision](https://github.com/Arcanada-one/knowledge-contract/blob/a5b3618034256f14f389c2c7de8da409c7c5310c/papers/geometry-of-semantic-representations/PAPER.md),
blob `ae74a2b7dfb768a2447622680635540c4a658387`. The partial-domain statement
is an elementary corollary of its existing factorization criterion.

## Reconstruction and source identity

The reported hourly candidate directory was unavailable in the preparation
runtime. Its original bytes and execution were not recovered. The author
therefore reconstructed a candidate from the reported claim and the pinned
existing criterion, then executed that new code. Reproducing the reported
counts does not authenticate the unavailable hourly artifacts.

The [original candidate note](evidence/originals/F05-FIBREWISE-TRANSFER-CANDIDATE.md),
[original checker](evidence/originals/check_fibrewise_transfer.py),
[author execution receipt](evidence/originals/fibrewise-transfer-result.json)
and [source provenance](evidence/originals/source-provenance.json) are retained
without changing their bytes. These are preparation records, not the missing
hourly files.

The canonical checker is
[tools/check_semantic_verification_fibrewise.py](../../tools/check_semantic_verification_fibrewise.py),
SHA-256 `6f591ea3c179f3fddc687f0b8adb358d79c4d74e18bd2760c113d3d73d448188`.
Only its module docstring changed from the reconstructed source, whose SHA-256
is `a53e6d61468aa9013d80a6a0b1a63c996a3d38f35a6199dc673e85d7fe3fb99b`.
The remaining source bytes are identical. The new docstring gives the
repository-relative entrypoint and identifies the checker as a bounded
reference procedure. A fresh execution binds the relocated source and its
actual environment; the earlier receipt remains historical.

The [packet provenance](provenance.json) records exact hashes, encodings and
the relationships between the retained files. Runtime absolute paths inside
original receipts describe their observed environments. They are not the
portable replay instructions for this packet.

## Actual finite execution

The [final execution result](evidence/final-reference-result.json) and
[outer run record](evidence/final-reference-run.json) retain the actual command,
exit 0, empty stderr, source hash and output hash.

| Counted object | Actual count |
| --- | ---: |
| Four-situation observation/assessment profiles | 4,096 |
| Globally factorable profiles | 232 |
| Non-global profiles with a determined attained fibre | 2,496 |
| Profiles without a determined attained fibre | 1,368 |
| Candidate partial maps examined, 25 per profile | 102,400 |
| Observation queries, two per profile | 8,192 |
| Determined queries | 2,952 |
| Ambiguous queries | 4,728 |
| Unattained queries | 512 |

These are three denominators inside one declared finite calculation, not
additional independent trials. The oracle enumerates partial functions,
requires undefined values at unattained labels, checks agreement on every
state where defined, and finds the unique greatest sound partial map.

Separate controls preserve all four assessment labels, retain
unknown/not-applicable distinctions, exercise relevant and irrelevant
refinements and a domain-extension countermodel, and refuse thirteen
unsupported input shapes. The unchanged checks detect the first-value mutant.
The actual optimized-Python subprocess exits 2 before a finite-run receipt.
The script does not turn its model labels into assessments of a real target.

## Separately structured internal review

The original non-author algorithm review is preserved in
[internal_review.json](evidence/originals/internal_review.json), alongside its
[separate entrypoint rerun](evidence/originals/candidate_entrypoint_rerun.json).
Its original script is retained losslessly as
[review_f05_partial.py.gz](evidence/originals/review_f05_partial.py.gz).
Decompressing that file yields the exact original bytes, SHA-256
`e526e91d917e454b10e4b530abcc28379a9db31182cfc507e7192addcc9de3ec`.
Gzip preserves the original extra newline at EOF without altering the
historical program or introducing a whitespace-policy exception.

The portable successor,
[review_fibrewise_reference.py](review_fibrewise_reference.py), and its
[current execution record](evidence/canonical-internal-review.json) bind the
canonical checker. Its oracle constructs the 25 partial-function graphs,
tests pointwise soundness, and obtains the greatest graph by union of all
sound graphs. It does not call the checker's oracle or `run_checks()` to
derive the expected results. It also checks the returned collision witnesses,
the original adverse behavior and limited auxiliary cases with other integer
labels and five situations. Those auxiliary cases do not enlarge the
exhaustive four-situation, binary-observation scope.

The checker author and reviewer used separate agent contexts on the same
controller and filesystem. They shared the stipulated model and result
vocabulary. The review is internal and algorithmically separate; it is not a
protected evaluation, independent-controller reproduction or external peer
review. Its verdict applies only to the recorded source and scope.

## Scoped specification review

The [initial specification review](evidence/spec-scoped-internal-review.json)
retains three resolved findings: explicit exclusion of unattained labels in
the oracle, a refinement control matching the actual distinction, and a
conditional witness obligation for a reported obstruction.

The [successor review](evidence/spec-scoped-internal-review-successor.json)
assesses specification SHA-256
`44106256dac25956c0bb49436644944481eee442eb579c2c8e6883a90d662eef`.
Its additional scope is the actual-consumer-use protocol in Section 7.3:
effective input, same-call output, observer limits, an oracle-distinguishable
decoy, a matched positive case and separately recorded recovery. Removing
only those added paragraphs reproduced the initial reviewed source hash.
This is a review of protocol text; the finite checker does not execute that
consumer experiment. The reviewer authored the reconstructed checker and
candidate note, but not the specification or the added paragraphs. Shared
controller and source dependencies remain explicit.

These text reviews cover Section 7 and selected Section 8 rows. Later source
changes need a successor review; catalogue registration, citations, the full
requirement set, publication checks and actual runtime behavior retain their
own verification obligations.

The [integration readback](evidence/spec-integration-readback.json) separately
binds the integrated specification, SHA-256
`8e80af19426b676f45bdc4efd0fcd6e8d1073cf963246c40c431aaf296c97db4`.
Its sole change from the reviewed `44106256` revision is the explicit
`SOURCE_MAP.json` link in Section 10. Exact byte comparison confirms that
Sections 7 and 8 are unchanged. The new link resolves, and all twelve listed
source blob identifiers match the declared baseline Git tree. This is a
structural source-pin check and an explicit readback of the reviewed scope;
it does not extend the earlier review to whole-document acceptance. The
earlier receipts remain unchanged and retain their original subjects.

## Portable replay

From the repository root, using Python 3 and its standard library:

```sh
python3 -B tools/check_semantic_verification_fibrewise.py
python3 -B reviews/semantic-verification-20261115/review_fibrewise_reference.py
```

Both commands emit a fresh JSON record to stdout. Ordinary replay does not
replace the retained receipts. A fresh receipt has its own time, environment
and content hash, even when the finite counts agree. The source pin in the
reviewer deliberately refuses an unreviewed checker revision.

The reference model does not establish real-world carrier completeness,
source authenticity, actual consumption, current authority or production
success rates. Applying a determined fibre result to a real target still
requires the separate application evidence in the specification.

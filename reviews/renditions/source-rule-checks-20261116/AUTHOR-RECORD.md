---
title: "Source Rule Checks: Russian and Simplified Chinese Author Drafts"
sources:
  - "Source Rule Checks rendition author checks"
status: "producer validation; independent acceptance NOT_VERIFIED"
---

# Source Rule Checks: Russian and Simplified Chinese Author Drafts

## Conclusion

This increment supplies complete Russian and Simplified Chinese author drafts of [Source Rule Checks](../../../engineering/studies/semantic-bridge-conformance/STUDY.md) through the existing [rendition PR104](https://github.com/Arcanada-one/knowledge-contract/pull/104). The exact English source is commit `8c7cd3bc1247998cb9554c568da26949da31b749`, blob `a08166d551ca43c7e2e203d9408604ec43bd4799`, SHA-256 `4df280692b0fd5f591f4098f4f1fa68a837a4c606e6e9dc481b0b12ef2a3f612`, 13,259 bytes. Its author, reported observations and review state are unchanged.

The 36-work catalogue on source main has 62 of 72 possible RU/zh-Hans body records. PR104 at `1d2ba019c3b9c423422c1d6a6fe0ab14fe49404a` adds the existing Context Controls pair and has 64. This increment adds two further bodies; their sidecar registration must bind the actual content commit after readback. That produces 66 registered work-language bodies, 33 per language. Agent Situation, Semantic Bridge and Semantic Verification remain absent in both languages. File presence, structural fidelity, scientific acceptance and public delivery are separate claims. The finite 31-work website snapshot is not repinned here.

## Improvement applied

The producer compared each complete draft with the exact English source, preserving seven sections, 35 top-level blocks, two three-column tables with five rows each including the header, 34 code objects, no mathematical objects, and 19 link occurrences resolving to 18 distinct references. The localized title register and `DOCUMENTS.md` now explicitly retain the English title's finite-model qualification. The pre-existing localized subtitles omitted that qualification; retaining them in the full drafts would have broadened the title's apparent scope. Only this work's localized names change.

The retained scientific populations remain distinct: 16,384 conformance combinations and 4,096 relation cases; 984 are a subset, not additional trials. Both drafts distinguish unknown and withheld availability, source-authored RULE/NOTE readings, same-controller algorithmic independence, aggregate zero-distance from same-world substitutability, and missing operation paths from false or unknown results. They retain the 5,341-byte failure with a 5,000-digit integer, the original exit 1 and missing JSON, the corrected exit 2 with `INVALID/malformed_json`, and the separate four integration tests, 30 hostile probes, CLI and runner receipts. These observations were translated, not rerun as new scientific experiments.

The [producer validator](producer_validate.py) imports the actual site's Markdown parser and rendition parity checker at commit `d3d17929f209612669f38db6a735d46bc9ec309c`. It verifies the retained bytes and SHA-256 of all three checker modules and requires Pandoc 3.1.3. It checks source commit/blob/digest, source and target metadata, section identity, block and table structure, exact code, canonical links, target script and digit-token multiplicity per paragraph and table cell. It accepts English comma and Russian space thousands separators, without inferring numerical meaning from written words or token order.

Seven separate target mutations per language remove a section, drop a link, remove a table row, change a command, change 16,384 to 16,385, alter the source commit or invent reviewed status. A fifteenth control changes the source digest. Each control must yield its specified refusal; an unexpected exception, no-op mutation or missing control is a failure. The first successful local receipt is retained separately from later runs. All work here is producer-controlled; helpers share the controller and are not independent reviewers.

The producer's first program had a real invocation defect: the successful absolute-path run did not cover the workflow's `--pandoc pandoc` argument. Converting that name directly to an absolute `Path` selected a nonexistent file in the working directory. The workflow-style invocation failed with exit 1 despite Pandoc being available in `PATH`. The program now resolves the command through `shutil.which` before checking its identity and version. The repeated workflow-style invocation passed. Missing command and missing explicit path separately produced the named `PANDOC_EXECUTABLE` refusal; those two invocation controls are not added to the 15 translation controls. The existing Context Controls verifier already accepted a command name and was not changed.

Retained evidence is append-only:

- [Run 01: initial absolute-path success](producer-result-run-01.json).
- [Actual invocation failure and complete pre-fix program](producer-invocation-failure-before-fix.json).
- [Run 02: corrected program and exact invocation](producer-invocation-run-02.json).
- [Run 02: complete result](producer-result-run-02.json).

The successful result JSONs match because they report the same source/target properties. The separate invocation record binds run 02 to the corrected program digest; matching result text does not identify the program that produced it.

## Reproduction and acceptance

Use a source checkout containing the pinned English commit, the pinned site checkout, and Pandoc 3.1.3:

```sh
python3 -B reviews/renditions/source-rule-checks-20261116/producer_validate.py \
  --repository . --site-repository /absolute/path/to/contract-place-site \
  --pandoc /absolute/path/to/pandoc-3.1.3
python3 -B -m unittest tools.test_context_package_translation_pin -v
python3 -B tools/check_publication.py .
python3 -B tools/check_document_names.py
python3 -B tools/check_requirement_register.py
python3 -B tools/check_sources.py .
```

The existing rendition workflow adds this validator after the existing Context Package and Context Controls checks. Read-only permissions, pinned checker and renderer, original checks and all prior 64 sidecar records remain. Hosted execution requires the resulting run and its actual checkout identity; local execution alone cannot establish it.

Existing focused local gates passed separately: publication validation and its 17 tests; document naming and its 23 tests; all 387 requirement-register entries; nine Context Package source-pin tests; the unchanged Context Controls validator and its own 15 adverse controls; source attribution and whitespace checks. These are engineering checks of the candidate, not additional research observations or independent translation review.

After creating content commit `a17f6c4293f0ef4d1da52fe0918424e3a8ea7b78`, the producer read all 15 changed files back through GitHub and matched their exact bytes. Only then were the two new sidecar entries bound to that commit. The actual site sidecar validator accepted all 66 entries; the previous 64 records are unchanged, both new source/target pins verify against Git history, and both new review states remain unreviewed. The [coverage snapshot](coverage-snapshot.json) was produced by the existing read-only coverage tool against that actual commit.

REUSE 6.2.0 passed locally. Markdownlint was unavailable locally and was not counted as a pass. A later publication-check invocation accidentally selected the system Pandoc 3.1.11.1 and correctly refused it; the repeat with the required Pandoc 3.1.3 passed. That environment refusal is distinct from the corrected program-path defect above.

Requested independent review must name the exact final source and target blobs and compare the full bodies, including finite populations, unknown/withheld states, operation composition, quotient scope, failure history and the same-controller limitation. Target `review_state=unreviewed` is separate from `source_review_state=internally-reviewed; external independence not verified`. Native-speaker Chinese acceptance, semantic equivalence, scientific promotion, production usefulness, site publication and native KC2 admission remain NOT_VERIFIED. Cost is NOT_MEASURED.

Rollback is a reviewed revert of this rendition pair, its two new sidecar entries, its localized title correction and its producer-check increment. Preserve the English source, prior translations and historical evidence.

## Idea

Treat translation checks as preservation obligations tied to the representation actually consumed by the site. A matching word count or a translated title cannot establish a complete body. Likewise a structurally complete body cannot establish semantic equivalence. Preserve separate evidence for source identity, content coverage, adversarial sensitivity, independent language review and actual served use; reuse this sequence for the three remaining untranslated works.

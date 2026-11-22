---
title: "Context Controls: Russian and Simplified Chinese Author Drafts"
sources:
  - "Context Controls rendition author checks"
status: "producer validation; independent acceptance NOT_VERIFIED"
---

# Context Controls: Russian and Simplified Chinese Author Drafts

## Source, purpose and boundaries

This increment supplies two complete author-draft renditions of [Context Controls](../../../engineering/studies/agent-situation-controls/STUDY.md). Its exact English source is commit `8c7cd3bc1247998cb9554c568da26949da31b749`, blob `b875953c066fcbb99e1579f76dfcd29c5bc9ef9d`, SHA-256 `41b6fbf4392fa27be2269ccbfb73b1e9049aa9cb7784c7b295960e8336366e05`, 12,466 bytes. The English research-draft status, scientific author Pavel Valentov, original observations and historical failures remain unchanged.

At that source cut the catalogue contains 36 works and 31 body files per target locale. The five absent works per locale are Agent Situation, Semantic Bridge, Semantic Verification, Context Controls and Source Rule Checks. This candidate adds only Context Controls, taking file presence to 32 per locale, or 64 of 72 work-language slots. Presence is separate from fidelity, review, public delivery and index admission. The finite 31-work website snapshot is not repinned here.

Before authoring, the producer recorded the hypothesis that a full pair could retain the finite-result denominators, adverse evidence, all references, reproduction code and limitations. The intended positive checks were complete section correspondence, table structure, exact code, canonical link identity, preserved numerical results and exact source bindings. Planned adverse checks changed a source pin, removed a section, changed reproduction code and removed a reference. The executed checks below additionally examine missing table rows, changed result numbers and an invented reviewed status.

The open-PR inventory read on 16 November 2026 contained seven source proposals. All their changed-file pages were examined, including both pages of PR119 (108 files); no other proposal added these rendition paths or changed the Context Controls manuscript. The existing KC-Brain rendition lane is [PR104](https://github.com/Arcanada-one/knowledge-contract/pull/104); this work reuses that lane rather than creating another feature proposal.

## Full text and author checks

- [Russian draft](../../../translations/ru/engineering/studies/agent-situation-controls/STUDY.md).
- [Simplified Chinese draft](../../../translations/zh-Hans/engineering/studies/agent-situation-controls/STUDY.md).
- [Actual producer result](producer-result.json), which binds the exact target SHA-256 values and sizes.
- [Read-only validation program](producer_validate.py).

For each language, the producer checked all seven source sections, 36 top-level blocks, two three-column tables with 7 and 11 rows including headers, 12 inline-code objects, one exact shell block and 14 canonical references. Numeric tokens match within each paragraph and table cell; Chinese syntax reverses their order within two such units without changing the stated 20-of-21 relation. The validator checks the target script and preserves the `research-draft` and `author-draft` states. It does not infer meaning from these mechanical checks.

The source-bound checker is the actual site checker from `d3d17929f209612669f38db6a735d46bc9ec309c`, with exact module digests in the result. The validator uses Pandoc 3.1.3 and the site's complete Markdown reader configuration, including `gfm_auto_identifiers`. An initial local exploratory pass used Pandoc's default Markdown identifiers; that is not the production parser. Before the recorded result, explicit heading IDs and the proposed sidecar mapping were aligned to the actual production parser and all checks were rerun. The earlier exploratory pass is not release evidence.

The first source-attribution gate rejected the new Python validator and JSON result because they had no source-register entries. An explicit source row was added; the repeated source gate passed. The original refusal is retained in the author execution logs, separately from the successful repeat.

Seven independently applied input mutations per language were refused after the green baseline: missing section, changed shell command, removed reference, deleted table row, changed result number, wrong source commit and invented reviewed status. A separately mutated source digest was also refused. These are 15 observed adverse controls, not 15 scientific experiments. The program reports the exact refusal for each mutation; unexpected errors cannot count as detection.

Two separate probes checked this validator itself. Removing one registered adverse control produced `ADVERSE_CONTROL_INVENTORY`, and changing the expected site-checker hash produced `SITE_CHECKER_PIN`; both exited nonzero. These two probe results are separate from the 15 rendition/source adverse controls. The original validator and its expectations were restored by running the probes only on temporary copies.

During same-controller author review, the false-permission fixture wording was made explicit in both languages: it is the Boolean value “false”, rather than an assertion about forged permission. The target remains a structurally ready fixture that grants no authority. No source finding, scientific result or review record was changed by that clarification.

## Context Package conflict resolution

Integrating the existing PR104 head `9c1b33efc3b297fb8144c4e8103474fd13dba0a0` with current source main produced one title-anchor conflict in each Context Package rendition. Current main carried the legacy plural anchor on the translated H1; PR104 preserved that anchor separately and used the current singular title anchor on H1. The resolution preserves the old HTML alias and current H1 identity, matching the English source. The already authored terminology, reader-capability and link corrections from PR104 are retained. The only additional difference from PR104's full rendition bytes is the description metadata already in current main.

Both Context Package translations passed the existing nine source-pin/name/requirement/link tests, including its negative controls. Both also passed structural parity under the actual site Markdown configuration. Their unreviewed sidecar entries must bind the resulting content commit; a prior rendition hash cannot be reused for modified bytes. The eight historical reviewed entries and their evidence remain unchanged.

## Existing workflow extension

The existing Context Package rendition workflow retains its nine tests and adds this pair's producer validator in the same job. It reads the site checker at the exact pinned commit with read-only repository permissions and no persisted credentials. The source checkout includes history so the validator can verify the source commit and blob rather than trusting a supplied digest alone.

The renderer install follows the existing site's Pandoc 3.1.3 package and SHA-256 check: `caa7e0410f9e2cb1da2eb8db13cc97b5548fe455985e2c944e3929d22f99bcdc` for `pandoc-3.1.3-1-amd64.deb`. The producer downloaded and checked those actual package bytes, extracted them locally, and ran both validation commands extracted from the proposed workflow. Both passed. This is local execution of the workflow commands; hosted execution requires the resulting GitHub Actions log and exact checkout identity.

## Reproduction and remaining acceptance

Check out the site repository at the pinned commit, make the English source commit available in the local source Git history, and use Pandoc 3.1.3:

```sh
python3 -B reviews/renditions/context-controls-20261116/producer_validate.py \
  --repository . --site-repository /absolute/path/to/contract-place-site \
  --pandoc /absolute/path/to/pandoc-3.1.3
python3 -B -m unittest tools.test_context_package_translation_pin -v
python3 -B tools/check_publication.py .
python3 -B tools/check_sources.py .
python3 -B tools/check_requirement_register.py
```

The validator prints a new result to stdout and does not overwrite retained evidence. It requires the exact site-checker bytes and source bytes. It does not validate a future content-commit reference before that commit exists. The publication sidecar must be bound only after the actual content commit is created and read back; independent review must then name the final exact source and target blobs.

Requested non-author review: compare the full English, Russian and Chinese texts; examine delayed-derivation premise binding, the positive delayed case, the preserved 18/18 false reassurance, the later 20-of-21 inventory omission, the separate 21/21, 3/3 and 9/9 denominators, conservative conflict handling, scope limits and the unexecuted agent experiment. Whole-body semantic acceptance, native-speaker Chinese review, scientific promotion, current production utility, native KC2 admission and deployment remain NOT_VERIFIED. No new LLM trial was performed. Cost is NOT_MEASURED.

Rollback is a reviewed revert of only the new rendition increment and its corresponding sidecar changes, preserving the original English and historical evidence.

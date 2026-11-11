---
title: "Reading Dependencies: Exact Glossary Link Reconciliation"
sources: ["Knowledge Contract project corpus and publication edition"]
status: producer link-only correction; not a new full-body review
updated: 2026-11-09
---

# Reading Dependencies: Exact Glossary Link Reconciliation

The first extraction of twenty reviewed translations exposed two missing links: the final glossary link in each Contract Checks translation pointed to a locale glossary outside the finite release. Run `42593994509` reported those two errors. Restoring both old glossary drafts in `ae945f2c297319895d8e5808da9f4818c36f67ee` resolved those addresses but introduced four more omitted-specification dependencies, as run `42595616137` reported. Rather than expanding the batch into unreviewed drafts, the final correction removes that intermediate restoration and fixes the two literal link destinations to the existing canonical glossary.

## Exact correction

In each of the two study files, exactly one Markdown destination changes:

```text
../../../reference/glossary/GLOSSARY.md
../../../../../reference/glossary/GLOSSARY.md
```

The added two parent components account for the `translations/<language>/` directory depth. From the study's own directory the new path resolves to [Shared Vocabulary](../../reference/glossary/GLOSSARY.md), the canonical English glossary with the accepted Russian and Chinese terminology crosswalk. The visible translated link text is unchanged. This is not a claim that a full current glossary translation has been admitted.

| Target | Earlier reviewed Git blob | Link-corrected Git blob |
| --- | --- | --- |
| Russian Contract Checks | `8237877bb67680e4ece8b56b1f0bf96e92dbd226` | `6da54d4eab2d45838c5f123ef6fb7d7021255264` |
| Simplified Chinese Contract Checks | `27f4c0daa1b5be6577473da158bdea5a546fa994` | `aff7156e0cd550f8bb776d73f1447cda7263acfc` |

No statement, formula, result, heading, table, requirement identifier or bibliography changes in these two texts. The other eighteen reviewed translation files are unchanged. The primary full-body verdict remains bound to its old exact pair; this producer record discloses the small technical delta instead of pretending the old reviewer signed the new blob. Ordinary diff and link CI must verify the submitted bytes.

## Title-preparation output must retain this correction

`first-reviewed-batch.json` deliberately identifies the original reviewed inputs, and `prepare_reviewed_publication.py` compares those exact historical source/target objects. Its generated title/source proposals therefore still contain the old literal glossary URL in these two files. After generating the proposals, apply the same single destination replacement above to each proposed Contract Checks file. Require exactly one old match per file; compare against the original proposal and record the final bytes and hashes. Do not publish the old intermediate proposed target hash as the hash of the repaired file.

The narrow review scope is the explicit title/source metadata, stable headings and these two same-logical-work link relocations, not another review of the unchanged scientific prose. The site compiler must still perform actual section, formula, code and logical-link parity against the current English source. No fixture-mode output or weakened guard can substitute for that run.

This branch contains **twenty full translation texts**, not twenty-two. The two historical glossary drafts remain untouched in the original PR76 history and are not included in this finite release. The final naming/translation source remains separate from the site build, served readback and backend index admission.

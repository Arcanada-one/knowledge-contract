---
title: "Russian and Chinese Editions: Coverage and Remaining Work"
sources: none
status: author-inventory
updated: 2026-11-08
---

# Russian and Chinese Editions: Coverage and Remaining Work

The accepted English source is [a0450428](https://github.com/Arcanada-one/knowledge-contract/tree/a0450428704fcd41b411203f2fc88c06c779610b). Existing translations are in [PR76](https://github.com/Arcanada-one/knowledge-contract/pull/76), inspected at `46566787d45c89388c79d47462a640b61ee33f07`. They are author drafts, not a deployed or fully reviewed multilingual corpus. The source naming proposal changes headers only; PR76 is not silently rewritten or merged here.

## Body coverage

| Kind | English documents | Russian drafts | Chinese drafts | Missing per language |
| --- | --- | --- | --- | --- |
| Scientific papers | 9 | 1 | 1 | 8 |
| Engineering specifications | 11 | 11 | 11 | 0 |
| Engineering studies | 6 | 0 | 0 | 6 |
| Glossary | 1 | 1 | 1 | 0 |
| Bibliography | 1 | 0 | 0 | 1 |
| Appendices | 2 | 0 | 0 | 2 |
| Total | 30 | 13 | 13 | 17 |

The existing paper translation is **Knowledge Revision**. Existing full specification drafts cover all eleven catalogue specifications; the glossary is also drafted. Therefore 34 body translations still need authoring, while all 60 target documents need complete acceptance and eventual publication. Localized titles for all 30 documents do not alter these body counts.

## Exact missing documents

Write both Russian and Simplified Chinese bodies for **Meaning Bridge**, **Meaning in Context**, **Knowledge Transformations**, **Context Assembly**, **Interaction and Memory**, **Evidence and Falsification**, **Knowledge Reuse**, **Knowledge Utility**, **Contract Checks**, **Dependency Closure**, **Uncertainty Preservation**, **Executable Projections**, **Reuse Economics**, **Editorial Pilot**, **Research Foundations**, **Source History**, and **Publication Interfaces**. Canonical paths and the complete localized title mapping are in [DOCUMENTS.md](../DOCUMENTS.md).

## Ancillary public text

The 60 target bodies do not include every public sentence. The bounded ancillary inventory includes repository and section introductions, the roadmap and detailed work-package explanations, naming/contribution/publication guidance, website navigation and cards, summaries and status explanations, download labels, error/help messages, search/index disclosures, figure captions and any public release notes. Each surface needs a named source file and coverage record before a claim of complete site translation. An exact total is not asserted until that inventory is reconciled with the site source.

## Acceptance sequence

KC-Brain authors and self-checks the full text against the pinned English original. Preserve negation, quantifiers, modality, source attribution, units, numbers, equations, code, table rows, examples, limits and bibliographic locators. Do not translate literal protocol identifiers. Keep research-draft status when the original has it.

A separate reviewer identifies exact source and target files, sections examined, method, fidelity findings and limitations. Previous review of selected fixes is not transferred to unexamined documents or new bytes. A title-only change can be reviewed as such when a mechanical comparison demonstrates unchanged bodies; neither check establishes new scientific validity.

Only after ordinary source review/CI and acceptance does engineering integrate actual translated bodies into the locale loader, rebuild from the accepted commit and check published HTML/Markdown/PDF where supplied. Resolve relative links consistently in classification, equivalence comparison and rendering; include real translated inputs, not only synthetic fixtures. Missing bodies must remain explicitly unavailable or English fallback, never falsely labelled complete Russian/Chinese text.

## Present pause

Authorship and theoretical fidelity review can proceed. Site implementation, server runs and deployment remain deferred by the operator's engineering pause. This inventory does not dispatch new SWE work, close a Muneral task, create an index admission or promise a release date.

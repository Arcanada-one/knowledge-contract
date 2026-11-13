---
sources: none
---

# Context Package — translation source re-pin (13 Nov 2026)

Status: **author-draft; no independent fidelity review, no native admission, no site release**.

The English manuscript at old source commit `a0450428704fcd41b411203f2fc88c06c779610b` differs from the published source `161a01afb1b756adf059ea2e1cbdd0dca29d83a2` only in front matter title/short title/subtitle/previous title and the H1 with a historical-URL anchor. The complete scientific body from `## 1. Purpose and conformance` onward is byte-identical; normative requirements `CTX-R001`–`CTX-R020` have the same values and order. The published source blob is `30ca8d2e5b5dd0e38b30cdb46919f514771a01da`.

The initial patch at `3cfd020a1782af06cb48954fa2b0147c33f05117` re-pins the two pre-existing draft translations to that immutable published source, updates the Russian title from plural to singular and preserves both historical and current H1 IDs. That initial patch does **not** edit any normative statement, add machine evidence, mark the drafts reviewed or change the publication sidecar.

The adjacent `tools/test_context_package_translation_pin.py` checks source SHA, all 20 IDs, status, exact pins, and both title anchors; it deliberately tests a forged source pin and an invented review status as negative controls. Hosted GitHub Actions executes it explicitly, not by assumption.

**Next editorial step:** independent EN↔RU and EN↔ZH-Hans semantic review, all link/anchor/terminology/MathML checks against the immutable published source, then the existing K8 rendition sidecar process (no artificial override of admission). Until that process completes, the site must retain the truthful English-fallback notice. Do not infer that a draft file is an approved translation.


## Successor: source fidelity and link repair

A separate internal delegated EN→RU and EN→zh-Hans full-body review found four unpinned peer-rendition links in each target. The unmodified K8 `classify_link` / `analyse_links` functions from contract-place-site `731720eb54d42b5e07019d49b954a72e855ae912`, compiler blob `f387ded563e9ab03d37436b3ad9dafb53792a70c`, reproduced four `RENDITION_LINK_UNPINNED` findings per original and zero per corrected target. The four hrefs now resolve to the original canonical work and fragment. File existence and canonical parity alone had not established link admission.

The successor also aligns front-matter/H1 titles with the existing name register, preserves both H1 anchors, clarifies only CTX-R017 in each language so that reader capabilities are not narrowed to a machine reader, and writes the two Russian integer counts with spaces. All twenty IDs and modal operators remain: 16 MUST, 3 MUST NOT, 1 MAY. The English source is byte-identical. These corrections are explicitly a broader delta than the initial metadata-only repin.

- [Russian review](context-package-20261113-ru-review.md): original blob `c5c00e126f48459521102ac4faaaf734030e3f83`; corrected blob `7db4c99c2e61f082f00223d19faa7de159465d51`.
- [Simplified Chinese review](context-package-20261113-zh-Hans-review.md): original blob `53ff8a136dd39ad362c3c5ff4e713117cb41b9bb`; corrected blob `4472d72bbfe9481bf7972da9a693391e61aa638a`.

The existing CI module now contains nine tests. Three added checks compare all eight logical document/fragment targets against English, detect the previous unpinned-locale link and a wrong-anchor mutation, and bind both localized names to the actual name register. Running this strengthened suite against the original translations fails as intended (six failed assertions); corrected targets pass all nine locally. Hosted execution remains a separate observation.

**Review limit:** delegated contexts share the authoring controller/model family. Actual independence is NOT_VERIFIED; these reports are not a native-speaker endorsement or a qualifying independent-admission receipt. The changed CTX-R017 lines need renewed non-author review on the exact new blobs. Both files remain `author-draft`; no publication-renditions entry, allowlist, protected evaluator or site pin changes. The isolated compiler diagnostics used Pandoc 3.1.11.1 and are not the required complete 3.1.3 build. Rollback is a normal reviewed revert of this source successor.

---
sources: none
---

# Context Package — translation source re-pin (13 Nov 2026)

Status: **author-draft; no independent fidelity review, no native admission, no site release**.

The English manuscript at old source commit `a0450428704fcd41b411203f2fc88c06c779610b` differs from the published source `161a01afb1b756adf059ea2e1cbdd0dca29d83a2` only in front matter title/short title/subtitle/previous title and the H1 with a historical-URL anchor. The complete scientific body from `## 1. Purpose and conformance` onward is byte-identical; normative requirements `CTX-R001`–`CTX-R020` have the same values and order. The published source blob is `30ca8d2e5b5dd0e38b30cdb46919f514771a01da`.

This patch re-pins the two pre-existing draft translations to that immutable published source, updates the Russian title from plural to singular and preserves both historical and current H1 IDs. It does **not** edit any normative statement, add machine evidence, mark the drafts reviewed or change the publication sidecar.

The adjacent `tools/test_context_package_translation_pin.py` checks source SHA, all 20 IDs, status, exact pins, and both title anchors; it deliberately tests a forged source pin and an invented review status as negative controls. Hosted GitHub Actions executes it explicitly, not by assumption.

**Next editorial step:** independent EN↔RU and EN↔ZH-Hans semantic review, all link/anchor/terminology/MathML checks against the immutable published source, then the existing K8 rendition sidecar process (no artificial override of admission). Until that process completes, the site must retain the truthful English-fallback notice. Do not infer that a draft file is an approved translation.

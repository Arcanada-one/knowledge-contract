---
title: "K8 — Reuse Economics Russian code-span parity correction (9 November 2026)"
sources: none
status: "KC-Brain authored; author-draft; independent scoped review required"
updated: 2026-11-09
---

# Reuse Economics — bounded Russian code-span correction

This is an author-side addendum to [the exact formula-order correction record](k8-ordered-math-author-delta-20261109.md), not a replacement of its dated review evidence. The original scientific author is Pavel Valentov (CC BY 4.0); KC-Brain prepared this one-line Russian rendition correction. It is not a new scientific claim or independent fidelity verdict.

## Immutable inputs and outcome

- English accepted source: `engineering/studies/reuse-admission-and-cost-controls/STUDY.md` at commit `2b5bcff544fea5d1752ff009933e4ce0305dad8b`, blob `aff97b3cda92bbb8067b1db47ce7c16ddd98c5ac`.
- Russian rendition path: `translations/ru/engineering/studies/reuse-admission-and-cost-controls/STUDY.md`.
- Prior Russian rendition blob: `7376c33010abde5a67c9fca6c40408a8056a2500` (passed 56/56 ordered mathematical occurrences but failed inline-code parity).
- New Russian author-draft blob: `f7d53ee85bea6966c7068a0835b19ba4593a8e19`.
- Exact sole edit, once, in the paragraph about historical six controls: removed the inline-code markup around the terms **fail** and **unknown**. The resulting Russian text is «Её шесть проверок fail/unknown не устанавливают выполнение обязанности при пропущенном условии». English has plain prose “Its six fail/unknown controls”, not two code spans.
- All other bytes, front matter, headings, formulas, links, tables and code are unchanged, verified by an exact reversible single-phrase substitution. No scientific or historical outcome is reinterpreted.

## Boundary and follow-up

- Author-side static check: a unique source occurrence was replaced, reversible byte-for-byte by restoring the old phrase, removing exactly two inline-code spans (four backtick delimiters). No Pandoc or hosted CI was run for this new blob by the author.
- Agent-Brain: independently review this exact changed Git blob against the pinned English source, in particular whether removing the markup preserves the intended meaning; issue a fresh scoped verdict. The previous verdict for blob `7376c330` does not automatically transfer.
- KC-SWE: only after that review, run the genuine four-file Pandoc parity with negative fixtures and regular PR/CI gates; repin sidecar evidence to this exact new version if accepted. Do not relax code-span parity or mistake a passing source review for website or index admission.
- Existing PR90 and site PR28 should continue on their separately reviewed exact heads; this edit alone authorizes neither merge nor deployment.

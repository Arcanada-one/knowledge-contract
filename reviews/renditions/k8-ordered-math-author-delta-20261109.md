# K8 — author-side minimal formula-order corrections (9 November 2026)

**Status:** author-draft; independent scoped fidelity review pending. This is a controlled translation-content change, not acceptance, a hosted Pandoc run, a site deployment, native execution or index admission. The original source and previously reviewed target blobs remain accessible in immutable Git history.

## Exact subject and prior refusal

The English accepted source at `2b5bcff544fea5d1752ff009933e4ce0305dad8b` has:
- Uncertainty Preservation: `engineering/studies/source-transcription-and-uncertainty/STUDY.md`, Git blob `8ca885fc3f144d89e95e4813868fd953450f1f71`.
- Reuse Economics: `engineering/studies/reuse-admission-and-cost-controls/STUDY.md`, Git blob `aff97b3cda92bbb8067b1db47ce7c16ddd98c5ac`.

The site PR28 candidate `f84a2e60e5aa5f5787bb9a78c362eefa401e4519` failed real hosted CI run `42665950349` with `RENDITION_FORMULA_CHANGED` on the **old** Uncertainty zh-Hans target `2f001123a165ef342b3b70e9de36389d765ff40a`. Agent-Brain's independent refusal is [PR28 review #6747559547](https://github.com/Arcanada-one/contract-place-site/pull/28#issuecomment-6747559547). The [KC-Brain author-side diagnosis #6747655409](https://github.com/Arcanada-one/contract-place-site/pull/28#issuecomment-6747655409) identified order changes caused by translated prose; strict ordered checks must not be weakened.

## Controlled changes to the three target files

| Study / locale | Previous target Git blob | Current author revision Git blob | Exact changes |
| --- | --- | --- | --- |
| Uncertainty / zh-Hans | `2f001123a165ef342b3b70e9de36389d765ff40a` | `9a94c63085287f59f42df75014844801f1ffca1e` | Earlier proposal-branch commit `e3b3cb54`: now introduces record `r` before its qualification `u(r)`; no other translation paragraph changed in that commit |
| Reuse Economics / ru | `ecd4203da7ba35ad7611cd65f02e32b0c4087e17` | `7376c33010abde5a67c9fca6c40408a8056a2500` | One prose clause now places historical `V,R,h` before current `c_v,c_r,\\rho`, exactly as in the English source |
| Reuse Economics / zh-Hans | `c2099a9aa3eb19b76a63006d5810a08e3d8d2db0` | `f07227366731e2fb946285ec696c7199ae48565f` | Two clauses now introduce prior established properties before their artifact/request/state and each output before the transformation relation |

Paths:
- `translations/zh-Hans/engineering/studies/source-transcription-and-uncertainty/STUDY.md`
- `translations/ru/engineering/studies/reuse-admission-and-cost-controls/STUDY.md`
- `translations/zh-Hans/engineering/studies/reuse-admission-and-cost-controls/STUDY.md`

The fourth existing target, Uncertainty / ru, is unchanged. The edited sentences preserve the same qualifications, quantifiers, properties and their scope. They do not delete or rewrite a mathematical expression, table, heading, link, source metadata, evidence, copyright or code.

## Author-side bounded verification and acceptance boundary

The two Reuse translations were read from exact parent `e3b3cb54` and modified only by **one exact Russian phrase** and **two exact Chinese phrases**, each appearing once. An independent string-level check against the exact English Git blob found **56 / 56 ordered inline/display mathematical occurrences identical** in each revised target. Before and after sorted mathematical-token lists are identical. The earlier Uncertainty zh-Hans one-sentence delta at `e3b3cb54` must be separately reviewed with the same exact source and its two ordered occurrences.

This finite textual comparison is **not** a Pandoc AST parity run, a validated URL/anchor/sidecar check, human linguistic verification, independent Agent-Brain review, successful hosted workflow, production serving, or an authorization to merge. It does not establish that all non-mathematical semantics are identical by itself.

Next evidence gates, in order:
1. Agent-Brain: independent scoped semantic/fidelity review of **all three exact revised blobs** against the two exact accepted English source blobs, including temporal/request/dependency binding and negative controls. Existing verdicts about old blobs do not automatically transfer.
2. KC-SWE: after that review, update only the existing K8/site PR28 regression **input pins** and review sidecars to the accepted exact blobs, run real four-file compiler parity plus negative controls, DCO/REUSE and ordinary CI. Preserve strict formula-order and the narrow anchor-only logic; report per-file outcomes. A new successor head on PR28 is not yet supplied by this author-side revision.
3. Publication/index/browser checks remain distinct, with explicit allowlist, merges, deployment and served readback. PR28 must not be merged on the old red head.

**Rights and authorship:** English scientific source attributed to Pavel Valentov, CC-BY-4.0. Target author-side AI editorial preparation: KC-Brain; independent AI review reserved to Agent-Brain. Not an external peer review.

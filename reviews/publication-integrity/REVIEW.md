---
name: publication-integrity
title: "Publication Review and Verification"
artifact: internal-review
edition: "1.0"
author: "Pavel Valentov and project contributors"
language: en
license: CC-BY-4.0
description: "Actual internal content reviews, verification results and release boundaries for publication edition 1.0."
---

# Publication Review and Verification

## 1. Scope and disposition

The edition contains eight complete scientific papers, eleven engineering specifications, six engineering studies, one glossary, one bibliography and two appendices. Its integration base is the exact public source revision `570f76b6d9a189295c3229254821c30748383965`. The earlier corpus remains traceable through the [source map](../../appendices/source-map/APPENDIX.md).

Two separate internal agents completed substantive reviews. Both accepted the texts within their stated scope; neither found an active blocking or nonblocking content defect. The reviews are internal assessments within one collaborative authoring environment. They do not establish external peer review, scholarly priority, empirical superiority, production readiness, or permission to index or deploy.

| Review | Work actually completed | Record |
| --- | --- | --- |
| Scientific and specification review | All eight papers and eleven specifications; 24 numbered formal results, related arguments, terminology, and selected paper-to-study boundaries | [Narrative](science-review.md) · [Exact input inventory and findings](science-review.json) |
| Evidence review | All six studies, 24 indexed claims, 58 JSON-pointer bindings, 47 evidence files, six origin manifests, available original records and four independent public replays | [Narrative](evidence-review.md) · [Input identities and checks](evidence-review.json) |

The two occurrences of twenty-four refer to different units: formal results in scientific manuscripts and evidence-index claims. They are not a combined sample size. The final metadata transition to `internally-reviewed` was separately checked by both reviewers; all substantive text and retained evidence remained unchanged.

## 2. Corrections made during integration

The integration supplied the required publication metadata, repaired current navigation and primary-source references, corrected the context-package description to a 110-node graph with twelve skill roots, and aligned competency terminology with the shared glossary. The newly merged upstream book-package format was integrated as an eleventh specification, with its exact implemented vocabulary and validation limits made explicit. All 57 upstream schema, tool and fixture files were retained byte for byte; the upstream CI job was preserved.

The initial isolated-assembly validation summary was replaced by the [current integrated study-package report](../../engineering/studies/validation-report.json). That mechanical report is separate from the evidence review and is not an assessment of scientific truth. The raw experimental records were not rewritten to conceal adverse results, comparator ties, missing measurements or historical protocol labels.

The final Markdown-lint configuration treats the required YAML `title` as metadata and the Markdown H1 as the visible document title. The rule against multiple actual H1 headings remains enabled. No manuscript, retained evidence or substantive review was changed for this correction.

## 3. Executed local checks

| Check | Actual result | Scope |
| --- | --- | --- |
| Publication and policy unit suite | 58 tests passed | Catalogue, metadata, references, origin hashes, source declarations, DCO-checker behavior, workflow and decision separation |
| Publication gate | Passed | The 29-document catalogue and its links, evidence bindings, origin sizes and hashes |
| Current Markdown navigation | Passed | Local links and fragments across current documents and compatibility pages; immutable historical receipt trees excluded |
| Source register | Passed | Publication, evidence and review files have registered provenance |
| Book-package suite | 17 tests passed with the pinned `jsonschema 4.23.0`; valid synthetic package passed | The 53 regenerated fixture files also matched their committed bytes |
| Exporter suite | 81 tests passed, no errors or skips, with real `gitleaks 8.30.1` | The downloaded scanner archive matched the SHA-256 pinned by CI; this is not export or admission of the new edition |
| REUSE licensing audit | Passed with REUSE 6.2.0 | All 258 source files covered, no missing copyright or license metadata |
| Markdown style | Passed with markdownlint-cli2 0.24.0 | 110 current Markdown files, zero issues |
| Offline link check | Passed with Lychee 0.24.2 | 598 occurrences: 463 local checks passed, 135 excluded in offline mode, zero errors; external targets were not checked by this command |
| Four public reproduction programs | Each completed; independent reviewer reproduced the saved output exactly | Fixed graph closure, a synthetic uncertainty-loss example, reuse/cost controls and mechanical editorial checks |
| Upstream preservation | Passed | Exact base tree plus unchanged upstream schema, code and fixtures |
| YAML and diff checks | Passed | Configuration parse and Git whitespace checks |

The counts identify checks, not an empirical success rate. Unit-suite success does not certify the DCO status of a future contribution, actual source rights, runtime admission or external behavior.

## 4. Execution environment and remaining release boundaries

The follow-up verification on 4 November 2026 closed the earlier missing-scanner and schema-validator-version limitations. The exact standard exporter command completed all 81 test methods successfully with the real pinned scanner. The scanner requirement was retained. The local toolchain used Python 3.12.14, Node 24.22.1, Pandoc 3.1.3 and the versions stated above. Machine-readable results and unchanged manuscript hashes are in [verification.json](verification.json); the delivery's `verification/` directory contains the command logs and tool provenance.

The pinned shared security workflow's framework profile was also checked locally: its actual security-policy script accepted `SECURITY.md`; the conditional accepted-risk check had no input; ShellCheck 0.10.0 was available, with zero shell-script inputs. This narrow profile is not a runtime dependency audit or a guarantee of security. The actual GitHub Actions jobs and the push-only export of an accepted remote `main` were not executed here. Site builds, browser inspection and their source pins are recorded separately in the site delivery.

The connected GitHub account has read access and no push permission to either project repository. No source merge, website deployment, corpus-admission decision, allowlist change or API index promotion was performed. Local snapshot commits identify build inputs only and are not a substitute for an authorized contributor's DCO attestation.

## 5. Applying the edition

Follow [PUBLISHING.md](../../PUBLISHING.md): content publication, exact-source website build and separately governed corpus admission have different evidence requirements. Apply the prepared patches against their named upstream bases, review and sign the real contribution under the contributor's own identity, run the retained CI gates, and rebuild the site against the actual merged source commit. Its generated manifest and the API's admitted index then require separate readback.

The publication catalogue organizes reading. These internal reviews are not the decision receipts required by the corpus exporter, and no historical receipt was altered to appear to approve this edition.

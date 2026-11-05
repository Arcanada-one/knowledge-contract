# Edition 1.1: Corrections and Review Record

This record responds to the review of the published edition 1.0 at immutable source revision [`ed2e188c89a1a50a187f3d55bf32baab54c87f7e`](https://github.com/Arcanada-one/knowledge-contract/tree/ed2e188c89a1a50a187f3d55bf32baab54c87f7e). It identifies corrected text and implementation boundaries. It does not certify a deployment, index admission, historical model replay or external peer review.

## Review inputs and disposition

The supplied summary and three detailed reports contain **90 findings: 10 must-fix, 44 should-fix and 36 suggestions**. Every finding has a response. Decisions: **82 addressed**, **7 clarified**, **1 deferred**. All ten mandatory corrections are addressed. The exact source-file hashes and current manuscript hashes are in [the input manifest](input-manifest.json). The supplied report authors described their readings as independent; the project does not reinterpret that description as external human peer review.

The [complete machine-readable response](response.json) records every original identifier, severity, response, changed file, verification and remaining limit. The table below is a reading index, not a substitute for those qualification fields.

## Main corrections

- Chain observation preservation now requires both adjacent precondition compatibility and matching observation interfaces. Request-indexed reuse requires sound prior verification, complete state and request observations, preservation for every permitted output, coverage of every new artifact requirement, and separately discharged current-use conditions. The proofs and executable counterexamples were revised.
- Book packages use the explicitly breaking `book-package/2` profile. Readiness requires a supported, scoped, independently attributed review tied to current bytes, reviewed objects and relations, and passing applicable extraction checks. Restricted or unknown-rights packages produce no candidate export rows; a conflicting licence cannot override their class. This is a conservative producer policy, not legal advice about every separately authored derivative.
- Status derivation is total over the declared dimensions. Execution and artifact histories have transition tables and terminal states. Publication generations are never reused; the complete dependency and authority predicate is checked atomically with publication. The finite in-memory model is not a distributed production implementation.
- Requirements have stable identifiers and a machine register. The bounded exchange profile specifies observation/change/advertisement records, vocabularies, strict JSON handling and exact-byte hash domains. Other architectural obligations do not claim full service interoperability.
- The editorial baseline received the same protected-claim registry and scoring rubric. Ordinary conformance counts exclude accepted false-input boundary cases. New graph, admission/cost and uncertainty controls are recorded separately from historical reports.

## Remaining historical recovery gap

**EST-05 remains deferred with partial recovery.** The exact historical synthesis schema was recovered at its recorded digest, but complete frozen runtimes, concrete inputs and oracles, the comparator, consumer, separate verifier and mutation artifacts remain unavailable. A later implementation with a different digest is not substituted. The [recovery inventory](../../engineering/studies/historical-recovery-gaps.json) lists known identities, searches, recovered material and the condition for closure. Recreating similar programs would establish a new experiment, not restore the original run.

Several clarified findings also retain explicit evidence limits: the initial reader summary does not establish expected status for each main-layer call; bibliographic descriptors do not authenticate a privately supplied edition. EST-18 is corrected to four application-positive cases, and EST-27 keeps the 918-image and 917-description stages separate.

## Verification and independent agent review

The [verification record](verification.json) identifies executed local checks and their limits. Freshly tasked scientific and engineering review agents did not author the corrections; their reports and exact reviewed inputs accompany this record. The scientific first pass fully read six papers, and its preserved supplement fully read the remaining two and checked their seven propositions. Together they cover all eight papers; they do not independently certify item-by-item closure of the original 26 findings or reproduction of every linked study. This is independent agent review within one project workflow, not external peer review or a production security certification.

- [Scientific recheck](independent-science-review.md)
- [Scientific supplement: completion of the remaining two readings](independent-science-supplement.md)
- [Engineering recheck](independent-engineering-review.md)
- [Original defect reproductions against the published base](baseline-probes.json)
- [Corrected study programs and immutable historical evidence](../../engineering/studies/review-corrections.json)

The scientific Markdown reports received presentation-only normalization (table spacing, heading markup and blank lines) for the publication lint rules. Their substantive text and JSON records remain unchanged. The full delivery retains the exact pre-formatting Markdown, its hashes and the formatting check under `verification/independent-science/`; hashes recorded before formatting still identify those archival copies.

The earlier [edition-1.0 internal review](../publication-integrity/REVIEW.md) remains historical. It missed the defects corrected here. Its input hashes and positive conclusions do not certify these new bytes or erase the later findings. All 47 retained study-evidence files and six origin manifests keep their original bytes; new checks do not rewrite earlier results.

Integration also found and corrected **INT-01**: an exhausted dependency counter could prevent a revocation update while still permitting publication. Publication now fails closed on either an exhausted head or dependency counter, with a regression for the exact sequence. This additional finding is recorded separately in the response and does not change the original 90-finding denominator.

The independent engineering recheck found and then verified the correction of **IER-01**: a symbolic link to an internal directory was accepted despite BPK-R005. Every relative path component is now checked. The independent failing control and passing recheck are retained; the ordinary nested-directory positive control remains valid. This is a path-validation correction, not a demonstrated rights, digest or root-containment bypass.

## Finding index

| Finding | Severity | Decision | Subject |
| --- | --- | --- | --- |
| SP-01 | must-fix | addressed | Chain-preservation proposition is false as stated |
| SP-02 | must-fix | addressed | The central reuse theorem never connects the verified properties to the new request |
| SP-03 | should-fix | addressed | Idempotence proposition omits serialization of concurrent duplicates, and the stored result |
| SP-04 | should-fix | addressed | Generation-admission result assumes generation identifiers are never reused |
| SP-05 | should-fix | addressed | "Retention" is used against the glossary and the reuse-policy specification |
| SP-06 | should-fix | addressed | Applicability uses three verdict values, but the status model has four |
| SP-07 | should-fix | addressed | The cited study does not cover the transition properties it is linked to |
| SP-08 | should-fix | addressed | The transcription study is described as addressing alternative readings and source regions |
| SP-09 | should-fix | addressed | The dependency-closure study is credited with selection controls it excludes |
| SP-10 | should-fix | addressed | The "central falsifiable engineering prediction" is true by definition |
| SP-11 | should-fix | addressed | Notation clash in the break-even result and against the study it accompanies |
| SP-12 | should-fix | addressed | Unscoped "complete" claims |
| SP-13 | should-fix | addressed | Soundness proposition ignores the side conditions the paper itself records |
| SP-14 | suggestion | addressed | Adoption argument assumes a countermodel exists |
| SP-15 | suggestion | addressed | The same reverse-reachability proposition appears twice under different wording |
| SP-16 | suggestion | addressed | The reuse theorem's transformation is a function, but the transformation paper uses relations; verification correctness is assumed silently |
| SP-17 | suggestion | addressed | "Conservative allocation prevents creation of cost" allows negative shares |
| SP-18 | suggestion | addressed | Contribution target compares against \(\pi_b\), while attribution requires \(\pi\) |
| SP-19 | suggestion | addressed | The downward-closure counterexample conflicts with the paper's closure-based support definition |
| SP-20 | suggestion | addressed | Proof step attributed to submodularity also uses monotonicity |
| SP-21 | suggestion | addressed | The Boolean residual example shows reconstruction, not economy |
| SP-22 | suggestion | addressed | The papers do not cite the corpus's own counterexample to closure minimality |
| SP-23 | suggestion | addressed | The closure proposition permits cycles, but the cited implementation rejects them |
| SP-24 | suggestion | addressed | Prior work that the papers' results restate without citation |
| SP-25 | suggestion | addressed | Utility paper points to "measured workloads" in a study that reports none |
| SP-26 | suggestion | addressed | Notation reuse within and across papers |
| ES-01 | must-fix | addressed | Rights guard bypassed through the knowledge layer; licence and licence class are not cross-checked *(probed)* |
| ES-02 | must-fix | addressed | `knowledge_ready` accepts a review whose result is `unsupported` *(probed)* |
| ES-03 | must-fix | addressed | Status model promises transition rules but gives only one |
| ES-04 | must-fix | addressed | Publication guard and "generation" are required in three specs but never defined |
| ES-05 | must-fix | addressed | Two admission vocabularies and three names for the admission authority |
| ES-06 | must-fix | addressed | Package status is claimed to be "derived" but the derivation is partial and leaves reachable states with no legal status *(probed)* |
| ES-07 | should-fix | addressed | Requirements are not identifiable, so "state which requirements it satisfies" cannot be done |
| ES-08 | should-fix | addressed | No wire format: the README promises "implementable obligations" that two teams cannot interoperate on |
| ES-09 | should-fix | addressed | Rendered knowledge layer drops conditions, operator scopes, source position and attribution without a loss account *(probed)* |
| ES-10 | should-fix | addressed | Markdown injection lets generated text forge the "Author's statement" label *(probed)* |
| ES-11 | should-fix | addressed | `pass` with `unknown` or zero checks contradicts the status model *(probed)* |
| ES-12 | should-fix | addressed | `asset_text` edits are accepted without any check, and the spec never defines them *(probed)* |
| ES-13 | should-fix | addressed | Staleness rule is keyed to an undefined edit state and to producer-declared dependencies |
| ES-14 | should-fix | addressed | Integrity `verified` is a producer assertion that gates `knowledge_ready` |
| ES-15 | should-fix | addressed | Time model: soft deadline, TTL class, staleness bound and "invalid chronology" are undefined |
| ES-16 | should-fix | addressed | Parallel vocabularies for the same dimension across specs |
| ES-17 | should-fix | addressed | Book-package facets claim consistency with semantic types but diverge in vocabulary |
| ES-18 | should-fix | addressed | Anchor/format table in the spec differs from the validator's mapping |
| ES-19 | should-fix | addressed | Profile "required" flag is producer-controlled; a constraint can be downgraded to optional |
| ES-20 | should-fix | addressed | Lowercase "must" carries central requirements; the appendix and book package have no BCP 14 keywords at all |
| ES-21 | should-fix | addressed | "Descriptor" is used normatively but defined only circularly |
| ES-22 | suggestion | addressed | `package_id` allows characters the exporter path pattern rejects *(probed)* |
| ES-23 | suggestion | addressed | Registry naming ban is not enforced |
| ES-24 | suggestion | clarified | Empty known list allowed for some facets but not others |
| ES-25 | suggestion | addressed | `candidate_projection` does not require a validated package or a publishable status |
| ES-26 | suggestion | clarified | `presented_as_author` semantics for `author_statement` undefined |
| ES-27 | suggestion | addressed | API appendix: repository identity and release-gate receipt unspecified |
| ES-28 | suggestion | addressed | "Conflicting adoption decisions" is a required test without a defined expected result |
| EST-01 | must-fix | addressed | must-fix — editorial-skill-pilot/STUDY.md:18 (also :32) |
| EST-02 | must-fix | addressed | must-fix — dependency-closure-and-package-delivery/STUDY.md:18 and :50 (contrast: contract-profile-conformance/STUDY.md:18) |
| EST-03 | should-fix | addressed | should-fix — dependency-closure-and-package-delivery/STUDY.md:22 and :46–48; editorial-skill-pilot/STUDY.md:65 |
| EST-04 | should-fix | addressed | should-fix — contract-profile-conformance/STUDY.md:18, :47 |
| EST-05 | should-fix | deferred | should-fix — contract-profile-conformance/STUDY.md:79; executable-projections-and-revision/STUDY.md:88 |
| EST-06 | should-fix | clarified | should-fix — executable-projections-and-revision/STUDY.md:18, :28 |
| EST-07 | should-fix | addressed | should-fix — executable-projections-and-revision/STUDY.md:18, :38 |
| EST-08 | should-fix | addressed | should-fix — executable-projections-and-revision/STUDY.md:44 |
| EST-09 | should-fix | addressed | should-fix — editorial-skill-pilot/STUDY.md:44–49; executable-projections-and-revision/STUDY.md:74 |
| EST-10 | should-fix | addressed | should-fix — editorial-skill-pilot/STUDY.md:30, :36 |
| EST-11 | should-fix | addressed | should-fix — editorial-skill-pilot/STUDY.md:67–69 |
| EST-12 | should-fix | addressed | should-fix — reuse-admission-and-cost-controls/STUDY.md:36, :103 |
| EST-13 | should-fix | addressed | should-fix — source-transcription-and-uncertainty/STUDY.md:82 |
| EST-14 | should-fix | addressed | should-fix — all six STUDY.md "evidence" links (for example contract-profile-conformance/STUDY.md:37, executable-projections-and-revision/STUDY.md:28) |
| EST-15 | should-fix | addressed | should-fix — dependency-closure-and-package-delivery/STUDY.md:56; executable-projections-and-revision/STUDY.md:58, :74 |
| EST-16 | should-fix | addressed | should-fix — editorial-skill-pilot/STUDY.md:73 |
| EST-17 | should-fix | addressed | should-fix — contract-profile-conformance/STUDY.md:63 |
| EST-18 | suggestion | clarified | suggestion — contract-profile-conformance/STUDY.md:39, :49 |
| EST-19 | suggestion | addressed | suggestion — contract-profile-conformance/STUDY.md:61 |
| EST-20 | suggestion | addressed | suggestion — dependency-closure-and-package-delivery/STUDY.md:46–48 |
| EST-21 | suggestion | addressed | suggestion — dependency-closure-and-package-delivery/STUDY.md:68 |
| EST-22 | suggestion | addressed | suggestion — dependency-closure-and-package-delivery/STUDY.md:18 |
| EST-23 | suggestion | addressed | suggestion — editorial-skill-pilot/STUDY.md:40–41 |
| EST-24 | suggestion | addressed | suggestion — editorial-skill-pilot/STUDY.md:34–36 |
| EST-25 | suggestion | addressed | suggestion — reuse-admission-and-cost-controls/STUDY.md:67–83 |
| EST-26 | suggestion | addressed | suggestion — source-transcription-and-uncertainty/STUDY.md:70–76 |
| EST-27 | suggestion | clarified | suggestion — source-transcription-and-uncertainty/STUDY.md:92 |
| EST-28 | suggestion | addressed | suggestion — Study evidence folders: citation coverage |
| RF-01 | should-fix | addressed | should-fix — reference/glossary/GLOSSARY.md:16 and tables |
| RF-02 | should-fix | addressed | should-fix — reference/glossary/GLOSSARY.md:86–87, :99 versus study usage |
| RF-03 | should-fix | addressed | should-fix — appendices/source-map/APPENDIX.md:32–33 (also :28, :34) |
| RF-04 | suggestion | clarified | suggestion — reference/bibliography/BIBLIOGRAPHY.md:100–102 |
| RF-05 | suggestion | addressed | suggestion — reference/bibliography/BIBLIOGRAPHY.md:102; SOURCES.md (editorial input row) |
| RF-06 | suggestion | clarified | suggestion — reference/bibliography/BIBLIOGRAPHY.md:94–96 |
| RF-07 | suggestion | addressed | suggestion — reference/bibliography/BIBLIOGRAPHY.md:16 |
| RF-08 | suggestion | addressed | suggestion — appendices/source-map/APPENDIX.md:66 |

## Publication boundary

The edition number identifies these documents. A local review commit, test pass, archive or site build is not a remote merge, release, deployment or index receipt. Publication follows [PUBLISHING.md](../../PUBLISHING.md); a real contributor supplies their own DCO attestation, the site pins the accepted source commit, and indexing requires its own decision and actual readback.

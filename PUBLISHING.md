# Publishing a Coherent Edition

Publication has three independently observable outcomes: source documents are merged at an immutable revision; the website renders that revision; the API indexes the content admitted by its separate policy. A local build establishes none of the remote outcomes by itself.

## 1. Source publication

Review the changes to the eight scientific papers, eleven specifications, six studies and their reference material. Inspect the [current review findings and verification boundaries](reviews/edition-corrections/REVIEW.md), not only a pass label. Every scientific claim needs the scope stated in its argument; every reported number needs its exact evidence. Retained reports and new replays must remain distinct.

Run the publication, source, unit, licensing and link checks. Execute the historical public replays and the corrected finite checks listed in [AGENTS.md](AGENTS.md). The unchanged edition-1.0 programs preserve a historical reproduction boundary; a known limitation of an old demonstration is not repaired by reporting its successful exit status. Add the source changes as a content pull request under [CONTRIBUTING.md](CONTRIBUTING.md). The authorized contributor supplies the DCO sign-off using their own identity; an assistant must not manufacture that attestation.

The existing decision-separation gate prohibits mixing content, publication-decision files and allowlist changes. Preserve that separation. This edition's internal content reviews are supporting records, not fabricated replacements for the exact decision and receipt format required by the corpus exporter.

## 2. Website build

After the source revision is available to the site build, set `publication-manifest.json` in `Arcanada-one/contract-place-site` to that exact 40-character Knowledge Contract commit and the edition declared by `publication-catalog.json`. Use a clean checkout of the pinned source. A local review commit is not a published source pin: after merge, rebuild against the actual accepted commit.

```sh
python3 scripts/build_publication.py --source-dir ../knowledge-contract
python3 scripts/check_publication.py
python3 scripts/check_page.py public
python3 scripts/check_hygiene.py .
python3 scripts/check_papers.py public
python3 scripts/check_links.py public
python3 scripts/test_build.py
node scripts/test_search.js
```

The site repository documents the exact commands and generated-file policy. Its CI reconstructs the publication and checks the resulting public tree. A local `--allow-uncommitted` preview is visibly marked and cannot be used as a production build. Changing the source commit requires rebuilding the reader and its document hashes; editing only the visible edition label is insufficient.

Deploy the tested site through its existing workflow. Read back the homepage, a scientific paper, a specification, a study and the generated publication manifest. Compare the served commit and document hashes with the intended source. Confirm equations, tables, navigation, source links and mobile reading in a real browser.

## 3. Corpus and API admission

The new catalogue is an inventory of publications, not an index allowlist. The exporter currently has an explicit scope inherited from earlier decisions. Expansion to the new canonical paths requires its corresponding scope decision and reviewed implementation; merely changing a path regular expression is insufficient.

After the content revision is fixed, use the established separate decision and receipt process to approve exact paths and bytes, record supersession of the old entry pages and mirrors where appropriate, and update the allowlist in its own change. The earlier receipts must continue to refer to their original reviewed bytes. They must not be edited to appear to approve the new corpus.

Export the admitted snapshot, refresh the backend index and inspect its actual manifest. Read back representative search and fetch results. A service health response or a label of `current` does not prove that the index contains this edition. The [API appendix](appendices/api-integration/APPENDIX.md) defines the consistency checks and the separate requirements for issuing a ready task-specific contract.

## 4. Release record

Record the source commit, content tree or document manifest, site commit, served publication manifest, API index identity, executed verification commands, review scope and any unperformed checks. An internal agent review is identified as internal; external peer review is recorded only if it actually occurred.

Do not state that a release is merged, deployed or indexed until the corresponding readback succeeds. If only one boundary is complete, report that boundary precisely. The documents' bounded scientific conclusions remain unchanged by the operational status of the release.

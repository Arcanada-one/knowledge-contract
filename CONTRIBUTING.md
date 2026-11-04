# Contributing

This repository maintains a coherent publication of scientific papers, engineering specifications and studies. A proposed change should identify its scope, evidence, affected canonical document and intended revision. Follow the [artifact format](engineering/specifications/artifact-registry/SPECIFICATION.md) and [AGENTS.md](AGENTS.md). Publication review and corpus admission follow the existing decision-and-receipt process in [OPENNESS.md](OPENNESS.md); a submitted change does not itself imply adoption or indexing.

Keep contributions in English, provide sources for factual claims, and identify third-party material and its license. Do not include secrets, private data, or unpublished draft packages. Text contributions are offered under [CC BY 4.0](LICENSE); code and schemas are offered under [Apache-2.0](LICENSE-CODE). Raise any licensing exception before submitting material. The project policy is in [OPENNESS.md](OPENNESS.md).

Report security concerns through the private channel in [SECURITY.md](SECURITY.md).

## Propose public content

Use the [pull request template](.github/pull_request_template.md) for each proposed paper, specification, guide, example, or correction. Identify the author or authorized rights holder, every source used for factual claims, the license of original and third-party material, and the requested publication status. Link to third-party text when reproduction rights are unclear; do not paste it into the repository.

A pull request is a proposal. Review must confirm both public publication rights and the intended status before a path can be added to the [corpus allowlist](corpus/README.md). Only a merged commit and an explicitly allowlisted path can become an indexing input. Publication does not establish scientific validity, current applicability, or agent authority to act.

For a correction, identify the earlier path and immutable revision, explain the changed claim, and request a `supersedes` relation. Keep the earlier revision traceable in Git history. For a withdrawal, state the affected path and revision privately if disclosure would cause harm; reviewers must remove it from the public allowlist and record the decision before another index generation is promoted.

## Sign off every commit (DCO)

Contributions are accepted under the [Developer Certificate of Origin 1.1](https://developercertificate.org/): add a `Signed-off-by:` line to every commit with `git commit -s`. There is no CLA. Inbound equals outbound: you license your contribution under the license of the file you change (CC BY 4.0 for text, Apache-2.0 for code and schemas), and you keep your copyright. Substantial contributors are credited in the git history and in `CONTRIBUTORS` and `CITATION.cff`. The sign-off must be in the last paragraph of the commit message and its name and email must match the commit's author or committer. CI fails a pull request that has a non-merge commit without such a sign-off (merge commits are not checked; the commits they bring are); automation commits from the allow-listed bot authors in `tools/check_dco.py` are exempt. Fix a missing sign-off with `git rebase --signoff` and a force-push of your own branch.

## Credit sources

Reuse of this project must credit the author and link to the source ([ATTRIBUTION.md](ATTRIBUTION.md)); contributions follow the same rule for what they build on. Register each external source in [SOURCES.md](SOURCES.md) and name the files that use it. A document with no external sources may declare `sources: none` in its front matter. CI covers canonical publications and their evidence as well as compatibility documents. Source registration is separate from publication or indexing admission.

## Verify the publication

Run `python3 -B tools/check_publication.py .` with Pandoc 3.1.3 and `python3 -B tools/check_sources.py .`. The gate checks the catalogue, canonical metadata, local links and anchors, and claim–evidence references. Run relevant public replay programs when changing the evidence or its interpretation. Keep the existing export, licensing, DCO and decision-separation checks.

Scientific changes require review of assumptions, derivations and inferential scope. Engineering studies must retain failed cases and comparator outcomes, identify units of observation, and distinguish exact retained evidence from a new reproduction. A formatting pass is not a substantive scientific review.

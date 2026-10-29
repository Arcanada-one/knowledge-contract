---
mirror_of: https://github.com/Arcanada-one/knowledge-contract/blob/39e05969728ea7a51f162cdbefac32fd8f54dbb6/CONTRIBUTING.md
mirror_source_commit: 39e05969728ea7a51f162cdbefac32fd8f54dbb6
author: Pavel Valentov and Knowledge Contract Arcana contributors
license: CC-BY-4.0
mirror_note: "Verbatim mirror of `CONTRIBUTING.md` at the source commit above, filed under `articles/` so the corpus exporter can index it. The text after this note is unchanged; relative links in it point into the source repository and are not valid here. Credit: Knowledge Contract Arcana, https://contract.place."
---

# Contributing

Knowledge Contract research is in progress. Open an issue to discuss a proposed change before preparing a pull request. A proposal should state its scope, evidence, and the affected specification or document. Publication of a draft requires separate review; a submitted proposal does not imply adoption.

Keep contributions in English, provide sources for factual claims, and identify third-party material and its license. Do not include secrets, private data, or unpublished draft packages. Text contributions are offered under [CC BY 4.0](LICENSE); code and schemas are offered under [Apache-2.0](LICENSE-CODE). Raise any licensing exception before submitting material. The project policy is in [OPENNESS.md](OPENNESS.md).

Report security concerns through the private channel in [SECURITY.md](SECURITY.md).

## Propose public content

Use the [pull request template](.github/pull_request_template.md) for each proposed paper, specification, guide, example, or correction. Identify the author or authorized rights holder, every source used for factual claims, the license of original and third-party material, the requested publication status, and the reviewer sought. Link to third-party text when reproduction rights are unclear; do not paste it into the repository.

A pull request is a proposal. Review must confirm both public publication rights and the intended status before a path can be added to the [corpus allowlist](corpus/README.md). Only a merged commit and an explicitly allowlisted path can become an indexing input. Publication does not establish scientific validity, current applicability, or agent authority to act.

For a correction, identify the earlier path and immutable revision, explain the changed claim, and request a `supersedes` relation. Keep the earlier revision traceable in Git history. For a withdrawal, state the affected path and revision privately if disclosure would cause harm; reviewers must remove it from the public allowlist and record the decision before another index generation is promoted.

## Sign off every commit (DCO)

Contributions are accepted under the [Developer Certificate of Origin 1.1](https://developercertificate.org/): add a `Signed-off-by:` line to every commit with `git commit -s`. There is no CLA. Inbound equals outbound: you license your contribution under the license of the file you change (CC BY 4.0 for text, Apache-2.0 for code and schemas), and you keep your copyright. Substantial contributors are credited in the git history and in `CONTRIBUTORS` and `CITATION.cff`. The sign-off must be in the last paragraph of the commit message and its name and email must match the commit's author or committer. CI fails a pull request that has a non-merge commit without such a sign-off (merge commits are not checked; the commits they bring are); automation commits from the allow-listed bot authors in `tools/check_dco.py` are exempt. Fix a missing sign-off with `git rebase --signoff` and a force-push of your own branch.

## Credit sources

Reuse of this project must credit the author and link to the source ([ATTRIBUTION.md](ATTRIBUTION.md)); contributions follow the same rule for what they build on. Register every third-party source of a paper or specification in [SOURCES.md](SOURCES.md), or declare `sources: none` in the file's front matter. CI fails a new file under `papers/` or `spec/` that has neither.

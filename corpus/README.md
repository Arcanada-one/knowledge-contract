# Public corpus allowlist

The public Knowledge Contract corpus has **no approved entries yet**. The repository currently contains a scaffold and contribution rules, not a published research paper or specification. The unpublished research package is excluded.

An indexer may read only a path listed below with a merged source commit, a content digest, a named publication decision, a license, and a status. An absent or incomplete row means **deny**, including for files that are public in this repository. A pull request, an unmerged commit, or a file in an empty `papers/`, `spec/`, `articles/`, or `schemas/` directory is not an allowlist entry. A secret-shaped or license-unclear candidate is denied before any export. The indexer must recheck these conditions at the source commit and fail closed when they cannot be measured.

| Source commit | Path | Content SHA-256 | Author/rights holder | License | Publication decision | Status | Supersedes |
| --- | --- | --- | --- | --- | --- | --- | --- |

The current scaffold on main at `37db327d88a30a9c5977842866f567da97fb7612` has no corpus entry. `README.md` and `CONTRIBUTING.md` describe the project and participation; they are governance context, not approved research material. Published external articles linked from the README are not mirrored or approved for ingestion here.

Before adding an entry, reviewers must confirm the exact merged commit and path, compare the file digest, establish publication rights and status, and record a decision traceable to the pull request. Corrections append a new row and mark the old revision `superseded`; withdrawals remove public serving eligibility while retaining restricted provenance. KC2 admission, where claimed, needs a separate exact-revision governance decision. Retrieval alone grants no action rights.

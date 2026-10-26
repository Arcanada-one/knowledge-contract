# Public corpus allowlist

The public Knowledge Contract corpus has **no approved entries yet**. The repository currently contains a scaffold and contribution rules, not a published research paper or specification. The unpublished research package is excluded.

An indexer may read only a path listed below with a merged source commit, a content digest, a named publication decision, a license, and a status. An absent or incomplete row means **deny**, including for files that are public in this repository. A pull request, an unmerged commit, or a file in an empty `papers/`, `spec/`, `articles/`, or `schemas/` directory is not an allowlist entry. A secret-shaped or license-unclear candidate is denied before any export. The indexer must recheck these conditions at the source commit and fail closed when they cannot be measured.

| Source commit | Path | Content SHA-256 | Author/rights holder | License | Publication decision | Status | Supersedes | Status decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

The baseline scaffold at `37db327d88a30a9c5977842866f567da97fb7612` has no corpus entry. `README.md` and `CONTRIBUTING.md` describe the project and participation; they are governance context, not approved research material. Published external articles linked from the README are not mirrored or approved for ingestion here.

Before adding an entry, reviewers must confirm the exact merged commit and path, compare the file digest, establish publication rights and status, and record a decision traceable to the pull request. Corrections append a new row and mark the old revision `superseded`; withdrawals remove public serving eligibility while retaining restricted provenance. KC2 admission, where claimed, needs a separate exact-revision governance decision. Retrieval alone grants no action rights.

For an export-eligible row, the publication decision links to an independent `APPROVED` review of the pull request's final head. Its review body must contain exactly one line in this form, with real values for the row:

```text
KnowledgeContractPublicationDecision/v1 {"path":"papers/example.md","sha256":"<64 lowercase hex>","rights_holder":"Named contributor","license":"CC-BY-4.0","status":"current","reviewed_head":"<40 lowercase hex>"}
```

The row's source commit is that pull request's merge commit. The exporter reads back the merge, review identity and state, exact head, decision fields, source blob and digest. A generic code approval does not establish publication rights.

To mark an old row `superseded` or `withdrawn`, retain its original publication decision and add a **later** independently approved, merged status decision URL. The later review body must contain one line binding the old source revision:

```text
KnowledgeContractStatusDecision/v1 {"source_commit":"<original merge SHA>","path":"papers/example.md","sha256":"<original digest>","status":"superseded","reviewed_head":"<later PR head SHA>"}
```

For a correction, the new row's `Supersedes` cell names the old content digest, and the old row's status becomes `superseded`. A withdrawal has no replacement row. A current row uses `none` for `Status decision`; a non-current row cannot export content. The current empty table exports no files.

Publish the status decision PR first with its rationale in a file under `corpus/decisions/`, then update this table in a separate PR that cites its existing review URL. The table update cannot cite a review that has not happened yet. The same two-PR order applies to first publication: merge the source and its rights review, then add the allowlist row.

# Status decision: withdraw `papers/P06_dialogue_and_learning.md`

Intended status: **withdrawn**. Original content digest (SHA-256): `d8ac6d6ed38ca15ac7a2ef3095e418dfb48e3f75ab71e780380701d2ee76a6ae`.

- Source commit: `817a8d8d42d452b9daeb68df55f9c9029366cc82`
- Path: `papers/P06_dialogue_and_learning.md`
- Affected revision: `MM_A0203` / `MM_A0203-entry-en-r1` (front matter of the page at the source commit)
- Reason: replaced by publication edition 1.1 (`cf215dd8b740efc73439294f40f20f360349355a`); the 14 numbered papers were moved into 8 papers and a supersession row needs the same path.
- Mechanism: the row leaves the allowlist table in a separate pull request that cites the independent review of this decision. No `withdrawn` decision line is written: the receipt check requires the blob at the base to hash to the line digest, and this path on `main` is now a compatibility link. The decision line of batch `b2` stays as history. A decision file does not itself export or ingest content.
- Limitation: the independent reviewer is a fresh blind agent session of the same account that wrote this record (`same_account_blind_agent`). The review shows consistency with the cited commit and digest, not independence, identity or any claim about the content.

## Structured decision (the exact record the reviewer restates in the pull request review)

```json
{
  "affected_revision": {
    "artifact_id": "MM_A0203",
    "revision_id": "MM_A0203-entry-en-r1"
  },
  "decision_line": "corpus/publication-decisions/b2.jsonl, current line for this path and digest",
  "intended_status": "withdrawn",
  "mechanism": "the allowlist row is removed from the table in a separate allowlist pull request that cites the review of this decision; no withdrawn decision line is written, because the decision line check requires the blob at the base to hash to the line digest and this path on main is now a compatibility link; the decision line of batch b2 stays as history",
  "path": "papers/P06_dialogue_and_learning.md",
  "reason": "replaced by publication edition 1.1 (knowledge-contract cf215dd8b740efc73439294f40f20f360349355a), whose 29 canonical documents (the same 29 paths as edition 1.0) replace the 14 numbered papers by 8 papers; the exporter links a superseded row to a replacement only when the replacement has the same path, so this move cannot be a supersession",
  "schema": "KnowledgeContractStatusDecision/v1",
  "sha256": "d8ac6d6ed38ca15ac7a2ef3095e418dfb48e3f75ab71e780380701d2ee76a6ae",
  "source_commit": "817a8d8d42d452b9daeb68df55f9c9029366cc82"
}
```

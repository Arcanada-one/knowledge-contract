---
title: "K8 browser-acceptance host-path redaction record"
sources: none
status: "Redaction reproduction record for Muneral b2ffbd14 browser evidence"
updated: 2026-11-10
---

# K8 browser-acceptance host-path redaction record

This directory publishes redacted worker evidence for Muneral `b2ffbd14`.
Private originals remain outside this repository and were not modified.

## Original names and hashes

| Original name | Original sha256 | Redacted sha256 | Published path |
| --- | --- | --- | --- |
| `report.json` | `d5503ef939fce3a4c4b76a0183cd157821ecbf6ad041de5b306826542ad62f30` | `78dd20f3a3e9192865bfab07f4d8f1f56c550cfa8fcfc04506c3507dedbb4242` | `report.json` |
| `REPORT.md` | `28d19f59ec5b7f69f2109c3abfcb353b05739d00a614b8051e618d5857d6eefe` | `4c0b557d572dde4f1ba2b6e5086d5b90d6772759eb75223e0183aaba57af38bb` | `REPORT.md.txt` |

`REPORT.md` is stored as `REPORT.md.txt` only to preserve the redacted evidence
bytes without subjecting them to the repository markdownlint document rules.
The `.txt` extension does not change the hash: `REPORT.md.txt` is
byte-identical to the redacted `REPORT.md` content
(`sha256 4c0b557d572dde4f1ba2b6e5086d5b90d6772759eb75223e0183aaba57af38bb`).
It is an evidence artefact, not a repository document.

## Substitution rules (exact strings, applied in order)

1. before: `/home/dev/aup/claude-work/kcswe-k8-browser/.venv`
   after: `<local-venv>`
2. before: `/home/dev/aup/claude-work/kcswe-k8-browser/`
   after: `./`

No other substitutions were applied. No user/host/session identifiers beyond
these host-local absolute paths were present in the originals.

## Per-file rule counts

### `report.json`

| Rule | Count |
| --- | ---: |
| `/home/dev/aup/claude-work/kcswe-k8-browser/.venv` → `<local-venv>` | 1 |
| `/home/dev/aup/claude-work/kcswe-k8-browser/` → `./` | 38 |

- original bytes: 735154
- redacted bytes: 733560

### `REPORT.md` (published as `REPORT.md.txt`)

| Rule | Count |
| --- | ---: |
| `/home/dev/aup/claude-work/kcswe-k8-browser/.venv` → `<local-venv>` | 1 |
| `/home/dev/aup/claude-work/kcswe-k8-browser/` → `./` | 0 |

- original bytes: 23378
- redacted bytes: 23342

## Reproduction

Run the committed deterministic script twice against the private originals and
compare outputs:

```text
python3 -B redact_host_paths.py --src <private-k8-browser-dir> --dst /tmp/k8-redact-a
python3 -B redact_host_paths.py --src <private-k8-browser-dir> --dst /tmp/k8-redact-b
```

Both runs must emit identical `report.json` and `REPORT.md` bytes and the
sha256 values above. This worker ran that procedure twice before committing;
both runs matched.

Anyone holding the private originals (report.json sha256
`d5503ef939fce3a4c4b76a0183cd157821ecbf6ad041de5b306826542ad62f30`, REPORT.md
sha256 `28d19f59ec5b7f69f2109c3abfcb353b05739d00a614b8051e618d5857d6eefe`) can
reproduce the redacted bytes with the same rules and script.

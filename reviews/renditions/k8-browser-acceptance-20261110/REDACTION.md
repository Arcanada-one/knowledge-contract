---
title: "K8 browser-acceptance host-path redaction record"
sources: none
status: "Redaction reproduction record for Muneral b2ffbd14 browser evidence"
updated: 2026-11-10
---

# K8 browser-acceptance host-path redaction record

This directory publishes redacted worker evidence for Muneral `b2ffbd14`.
Private originals remain outside this repository and were not modified.
Before-strings for the substitution rules are not published here; they are
identified only by rule id, after-string, application count, and the sha256
digest of the UTF-8 before-string. The private mapping lives on the private
review route described in `README.md`.

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

## Substitution rules (applied in order)

| Id | After | before-string sha256 (UTF-8) |
| --- | --- | --- |
| `R1` | `<local-venv>` | `8ab426728e31fcf3c152d6da488d1be39f7e62045c279a67be1b50334fcfcf35` |
| `R2` | `./` | `c02dd7a0cde79ccea59f7bcaa8032e2820cf782b8e1697ddb5159d1599237705` |

No other substitutions were applied. Exact string replace, in the order above.
`redact_host_paths.py` refuses a private mapping unless each before-string
hashes to the published digest and each after-string matches the table.

## Per-file rule counts

### `report.json`

| Rule | Count |
| --- | ---: |
| `R1` → `<local-venv>` | 1 |
| `R2` → `./` | 38 |

- original bytes: 735154
- redacted bytes: 733560

### `REPORT.md` (published as `REPORT.md.txt`)

| Rule | Count |
| --- | ---: |
| `R1` → `<local-venv>` | 1 |
| `R2` → `./` | 0 |

- original bytes: 23378
- redacted bytes: 23342

## Reproduction

Obtain the private originals and `REDACTION-MAPPING-PRIVATE.json` from the
private review route in `README.md`. Then run the committed script twice:

```text
python3 -B redact_host_paths.py \
  --mapping REDACTION-MAPPING-PRIVATE.json \
  --src <private-originals-dir> \
  --dst /tmp/k8-redact-a
python3 -B redact_host_paths.py \
  --mapping REDACTION-MAPPING-PRIVATE.json \
  --src <private-originals-dir> \
  --dst /tmp/k8-redact-b
```

Both runs must emit identical `report.json` and `REPORT.md` bytes and the
redacted sha256 values above. This worker ran that procedure twice before
committing the repair; both runs matched.

Anyone holding the private originals (report.json sha256
`d5503ef939fce3a4c4b76a0183cd157821ecbf6ad041de5b306826542ad62f30`, REPORT.md
sha256 `28d19f59ec5b7f69f2109c3abfcb353b05739d00a614b8051e618d5857d6eefe`) and
a mapping whose before-strings hash to the published digests can reproduce the
redacted bytes with the same script.

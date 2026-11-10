---
title: "K8 real-browser acceptance evidence (redacted)"
sources: none
status: "Owner-reported KC-SWE worker evidence for Muneral b2ffbd14; not independent review"
updated: 2026-11-10
---

# K8 real-browser acceptance evidence (redacted)

Owner-reported KC-SWE worker evidence for Muneral `b2ffbd14`. This is **not**
an independent review.

## Identity pins

| Pin | Value |
| --- | --- |
| Site main | `37e9fec93a4e1043ae8f707f148aac6e60e2a778` |
| Deploy run | `42729598828` |
| KC source | `1208dfbc2a5651a9ff6085a5b454f8511048d629` |
| Uniform Last-Modified | `Tue, 10 Nov 2026 00:38:58 GMT` |
| Muneral | `b2ffbd14` |

## Tooling

| Item | Value |
| --- | --- |
| Playwright | `1.65.0` |
| Chromium | `158.0.8127.18` |
| Profiles measured | `desktop_chromium_1440x900`, `mobile_chromium_Pixel7` |

## Coverage

19 pages × 2 Chromium profiles = 38 measured screenshot rows (plus WebKit rows
recorded as NOT_MEASURED in the report).

## NOT_MEASURED

- WebKit / iPhone 13 (`mobile_webkit_iPhone13`): host lacks
  `libevent-2.1.so.7`; Playwright MiniBrowser launch failed for all 19 pages.
- Search indexing.
- Everything outside the 19 planned pages.

## Cloudflare

The browser report saw no Cloudflare Insights beacon script in the DOM on any
of the 38 Chromium rows. Separately, KC-SWE's HTTPS readback normaliser removed
the injected cloudflareinsights beacon tag from 184 urllib responses (curl
responses had none). Raw HTTP bytes on those urllib responses are therefore
**not** identical to committed bytes. The beacon token is not included here.

## Files

| Path | Role |
| --- | --- |
| `report.json` | Redacted machine report |
| `REPORT.md.txt` | Redacted human report (evidence artefact; see below) |
| `REDACTION.md` | Exact substitution rules, counts, and hashes |
| `redact_host_paths.py` | Deterministic redaction script |
| `SCREENSHOTS.sha256` | sha256 + byte size + path + profile for all 38 original PNGs |
| `screenshots/` | Representative byte-exact PNG copies (under 15 MB) |
| `README.md` | This note |

### `REPORT.md.txt`

Original name was `REPORT.md` (sha256
`28d19f59ec5b7f69f2109c3abfcb353b05739d00a614b8051e618d5857d6eefe`).
Redacted sha256 is
`4c0b557d572dde4f1ba2b6e5086d5b90d6772759eb75223e0183aaba57af38bb`.
Stored as `.txt` only to preserve those exact redacted bytes as an evidence
artefact rather than a repository Markdown document; the extension does not
change the hash. See `REDACTION.md`.

### Redacted `report.json`

- original sha256: `d5503ef939fce3a4c4b76a0183cd157821ecbf6ad041de5b306826542ad62f30`
- redacted sha256: `78dd20f3a3e9192865bfab07f4d8f1f56c550cfa8fcfc04506c3507dedbb4242`

## Screenshots included in this PR

Total included bytes: `14835353` (cap 15000000). Preference was desktop+mobile
for ru and zh-Hans `reuse-admission-and-cost-controls` (56 formulas) plus one
`noindex,follow` control; both reuse mobiles alone with both desktops exceed the
cap, so the smaller zh-Hans reuse mobile is included and the ru reuse mobile is
held privately. The noindex control is ru
`contract-profile-conformance` desktop+mobile.

| File | Bytes | Profile | Why |
| --- | ---: | --- | --- |
| `screenshots/ru_engineering_studies_reuse-admission-and-cost-controls_desktop_chromium_1440x900.png` | 2194750 | desktop_chromium_1440x900 | ru reuse (56 formulas) |
| `screenshots/zh-Hans_engineering_studies_reuse-admission-and-cost-controls_desktop_chromium_1440x900.png` | 2030601 | desktop_chromium_1440x900 | zh-Hans reuse (56 formulas) |
| `screenshots/zh-Hans_engineering_studies_reuse-admission-and-cost-controls_mobile_chromium_Pixel7.png` | 5154014 | mobile_chromium_Pixel7 | zh-Hans reuse mobile |
| `screenshots/ru_engineering_studies_contract-profile-conformance_desktop_chromium_1440x900.png` | 1422356 | desktop_chromium_1440x900 | noindex control |
| `screenshots/ru_engineering_studies_contract-profile-conformance_mobile_chromium_Pixel7.png` | 4033632 | mobile_chromium_Pixel7 | noindex control |

Each included PNG is a byte-exact copy of the private original; its sha256
matches `SCREENSHOTS.sha256`.

## Screenshots held privately

- `en_engineering_studies_dependency-closure-and-package-delivery_desktop_chromium_1440x900.png`
- `en_engineering_studies_dependency-closure-and-package-delivery_mobile_chromium_Pixel7.png`
- `en_engineering_studies_executable-projections-and-revision_desktop_chromium_1440x900.png`
- `en_engineering_studies_executable-projections-and-revision_mobile_chromium_Pixel7.png`
- `en_engineering_studies_reuse-admission-and-cost-controls_desktop_chromium_1440x900.png`
- `en_engineering_studies_reuse-admission-and-cost-controls_mobile_chromium_Pixel7.png`
- `en_engineering_studies_source-transcription-and-uncertainty_desktop_chromium_1440x900.png`
- `en_engineering_studies_source-transcription-and-uncertainty_mobile_chromium_Pixel7.png`
- `en_programme_desktop_chromium_1440x900.png`
- `en_programme_mobile_chromium_Pixel7.png`
- `ru_engineering_studies_dependency-closure-and-package-delivery_desktop_chromium_1440x900.png`
- `ru_engineering_studies_dependency-closure-and-package-delivery_mobile_chromium_Pixel7.png`
- `ru_engineering_studies_editorial-skill-pilot_desktop_chromium_1440x900.png`
- `ru_engineering_studies_editorial-skill-pilot_mobile_chromium_Pixel7.png`
- `ru_engineering_studies_executable-projections-and-revision_desktop_chromium_1440x900.png`
- `ru_engineering_studies_executable-projections-and-revision_mobile_chromium_Pixel7.png`
- `ru_engineering_studies_reuse-admission-and-cost-controls_mobile_chromium_Pixel7.png`
- `ru_engineering_studies_source-transcription-and-uncertainty_desktop_chromium_1440x900.png`
- `ru_engineering_studies_source-transcription-and-uncertainty_mobile_chromium_Pixel7.png`
- `ru_programme_desktop_chromium_1440x900.png`
- `ru_programme_mobile_chromium_Pixel7.png`
- `zh-Hans_engineering_studies_contract-profile-conformance_desktop_chromium_1440x900.png`
- `zh-Hans_engineering_studies_contract-profile-conformance_mobile_chromium_Pixel7.png`
- `zh-Hans_engineering_studies_dependency-closure-and-package-delivery_desktop_chromium_1440x900.png`
- `zh-Hans_engineering_studies_dependency-closure-and-package-delivery_mobile_chromium_Pixel7.png`
- `zh-Hans_engineering_studies_editorial-skill-pilot_desktop_chromium_1440x900.png`
- `zh-Hans_engineering_studies_editorial-skill-pilot_mobile_chromium_Pixel7.png`
- `zh-Hans_engineering_studies_executable-projections-and-revision_desktop_chromium_1440x900.png`
- `zh-Hans_engineering_studies_executable-projections-and-revision_mobile_chromium_Pixel7.png`
- `zh-Hans_engineering_studies_source-transcription-and-uncertainty_desktop_chromium_1440x900.png`
- `zh-Hans_engineering_studies_source-transcription-and-uncertainty_mobile_chromium_Pixel7.png`
- `zh-Hans_programme_desktop_chromium_1440x900.png`
- `zh-Hans_programme_mobile_chromium_Pixel7.png`

Full private set size is about 123 MB across 38 PNGs. Hashes and sizes for all
38 remain in `SCREENSHOTS.sha256`.

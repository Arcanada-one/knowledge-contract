# Public Roadmap Status Projection (Draft)

**Status: draft.** Draft for KC-Brain/Agent-Brain review; not adopted.
This file is engineering scaffolding. It does **not** describe the current live
public status surface, authorize publication, or bind Muneral execution state.

## Purpose

Define a future **public** status projection for roadmap work items (RM-*) that
can be shown without private tracker identifiers or infrastructure detail.
Projection is read-only. A missing measurement must stay explicit.

## Projected fields

| Field | Meaning |
| --- | --- |
| `rm_id` | Public RM definition identifier (for example `RM-04`). |
| `definition_blob` | Versioned Git blob id of the definition inputs in scope (typically `roadmap/dependencies.json` and/or `roadmap/TASKS.md` at a pinned revision). |
| `binding_claim` | Claimed tracker binding for the RM, if any (opaque public handle only; never a private UUID). |
| `binding_verified` | Whether the binding was independently verified against an authorized fetch. Boolean, or `not_measured` when no verification ran. |
| `as_of` | RFC 3339 timestamp for the projection instant. |
| `evidence_scope` | What was inspected (definition blob, authorized tracker snapshot, neither). |
| `tracker_status` | Authoritative tracker status **only** when independently fetched and authorized; otherwise `unknown`. |
| `measurement` | `measured` \| `unknown` \| `not_measured` for the overall projection. |

Explicit values `unknown` and `not_measured` are first-class. Absence of a field
must not be read as a positive status.

## Rules

1. Never publish private tracker UUIDs, infrastructure hostnames, IPs, host paths
   or personal data.
2. Never derive public status from mail delivery, merge events, PR state, CI
   greenness or branch names.
3. Retain negative cases: failed verification, conflicting claims, unbound RMs
   and refused measurements stay visible as disagreements or `unknown` /
   `not_measured`, not as silent success.
4. A binding claim without independent verification does not authorize
   `tracker_status` other than `unknown`.
5. This draft does not authorize network calls, merges or deploys.

## Synthetic positive example

```json
{
  "rm_id": "RM-04",
  "definition_blob": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
  "binding_claim": "syn-0004",
  "binding_verified": true,
  "as_of": "2026-11-10T00:00:00Z",
  "evidence_scope": "definition_blob+authorized_synthetic_snapshot",
  "tracker_status": "open",
  "measurement": "measured"
}
```

The ids above are synthetic placeholders only.

## Negative example (not measured / unknown)

```json
{
  "rm_id": "RM-04",
  "definition_blob": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
  "binding_claim": "syn-0004",
  "binding_verified": "not_measured",
  "as_of": "2026-11-10T00:00:00Z",
  "evidence_scope": "definition_blob_only",
  "tracker_status": "unknown",
  "measurement": "not_measured",
  "retained_negative": "no authorized tracker fetch; PR/merge/mail events ignored"
}
```

## Out of scope

- Live Muneral reconciliation or credentialed tracker access
- Adoption as site or catalogue copy
- Replacement of `ROADMAP.md` reader-facing status prose

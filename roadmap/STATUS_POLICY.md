# Public Roadmap Status Projection (Draft)

**Status: draft.** Draft for KC-Brain/Agent-Brain review; not adopted.
This file is engineering scaffolding. It does **not** describe the current live
public status surface, authorize publication, or bind Muneral execution state.

## Purpose

A status projection is a **read-only claim** about a pinned, authorized
observation. It is not a status engine. It does not derive live state, merge
claims, or authorize tracker writes.

## Projected fields

| Field | Meaning |
| --- | --- |
| `rm_id` | Public RM definition identifier (for example `RM-04`). |
| `definition_sources` | Array of `{path, git_blob}` for each actual RM source in scope. |
| `record_kind` | `synthetic_fixture` \| `authorized_observation`. |
| `binding_claim` | Claimed tracker binding for the RM, if any (opaque public handle only; never a private UUID). |
| `binding_verified` | Independent verification against an authorized fetch: boolean, or `not_measured` when no verification ran. A proposed binding or synthetic source **never** sets `binding_verified=true`. |
| `tracker_status` | Authoritative tracker status **only** when independently fetched and authorized; otherwise `unknown`. A proposed binding or synthetic source **never** sets a measured `tracker_status`. |
| `measurement` | `measured` \| `unknown` \| `not_measured` for the overall projection. |
| `evidence_scope` | What was inspected (for example `synthetic_only`, definition sources, authorized tracker snapshot). |
| `snapshot_provenance` | Present only when legitimately observed: source/authority, `as_of`, method/digest, redaction scope. |
| `review_scope` / `review_identity` | Present only when a separate role actually reviewed the projection. |

Explicit values `unknown` and `not_measured` are first-class. Absence of a field
must not be read as a positive status.

## Rules

1. Never publish private tracker UUIDs, infrastructure hostnames, IPs, host paths
   or personal data. Private IDs and paths stay private.
2. Projection never derives state from CI, merge, PR, mail, repository owner, or
   a single agent context.
3. Unknown, unmeasured and negative findings stay explicit. Failed verification,
   conflicting claims, unbound RMs and refused measurements stay visible as
   disagreements or `unknown` / `not_measured`, not as silent success.
4. A proposed binding or synthetic source never sets `binding_verified=true` or a
   measured `tracker_status`. A syntactic fixture must use
   `record_kind=synthetic_fixture`, `binding_verified=not_measured`,
   `tracker_status=unknown`, `measurement=not_measured`,
   `evidence_scope=synthetic_only`.
5. A genuinely measured example is admissible only after an authorized
   independent tracker read, binding resolution, time/pin, sanitized evidence and
   review. Otherwise document the schema and criteria only; do not invent a
   success example.
6. Adoption or publication requires independent role review and ordinary
   publication gates.
7. This draft does not authorize network calls, merges or deploys.

## Synthetic fixture example

```json
{
  "rm_id": "RM-04",
  "definition_sources": [
    {
      "path": "roadmap/dependencies.json",
      "git_blob": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
    }
  ],
  "record_kind": "synthetic_fixture",
  "binding_claim": "syn-0004",
  "binding_verified": "not_measured",
  "tracker_status": "unknown",
  "measurement": "not_measured",
  "evidence_scope": "synthetic_only"
}
```

The ids above are synthetic placeholders only. This is not a measured success.

## Negative example (not measured / unknown)

```json
{
  "rm_id": "RM-04",
  "definition_sources": [
    {
      "path": "roadmap/dependencies.json",
      "git_blob": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
    }
  ],
  "record_kind": "synthetic_fixture",
  "binding_claim": "syn-0004",
  "binding_verified": "not_measured",
  "tracker_status": "unknown",
  "measurement": "not_measured",
  "evidence_scope": "synthetic_only",
  "retained_negative": "no authorized tracker fetch; CI/merge/PR/mail/owner/agent context ignored"
}
```

Measured `authorized_observation` records require an authorized independent
tracker read with binding resolution, time/pin, sanitized evidence and separate
role review before any success example may be published. Until then, only the
schema and criteria above apply.

## Out of scope

- Live Muneral reconciliation or credentialed tracker access
- Adoption as site or catalogue copy
- Replacement of `ROADMAP.md` reader-facing status prose

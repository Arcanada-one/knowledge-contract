# Tools

Bounded repository checks and fixtures. They are author-side engineering
controls: they are not independent scientific review, production verification,
or a substitute for manuscript peer review.

## Cross-package overlay preparation

`cross_package_overlay.py` is a **bounded producer-side preparation** for the
G11 draft model in `reference/relations/CROSS-PACKAGE-OVERLAY.md` section 3. It
evaluates one candidate overlay over **exactly two distinct canonical English
packages**, with endpoint identity = the complete eight-part tuple from overlay
§2.

**Fail closed (default deny).** A passing/inspectable status is returned only
after every A10 condition is affirmatively established:

- **R1 endpoint identity.** Each endpoint requires `package_id`,
  `package_manifest_digest`, `release_id`, `component_id`, `object_id`,
  `representation_id`, `representation_digest`, and `source_anchor`. Digests use
  `algorithm == "sha256"`, `value` 64 lowercase hex, and non-empty string
  `byte_domain` / `source_revision`. The endpoint's `package_manifest_digest`
  must equal its package (A or B) digest; a valid-but-different sha256 refuses
  (`endpoint_digest_mismatch`). `representation_digest.source_revision` must
  equal the endpoint `release_id`. **Representation binding (KC-SWE reading of
  overlay §2, pending KC-Brain confirmation):** each package requires a
  non-empty `representations` map
  `representation_id -> {representation_digest, language}`. The endpoint's
  `representation_id` must be a key in its package map and
  `representation_digest` must equal the declared digest on all four fields
  (`representation_identity_mismatch` otherwise). Declared representation
  `language` must be `"en"`; if `endpoint.language` is present it must equal
  that declared language (`rendition_endpoint_refused`). The fixture id
  `canonical-en` is not a rule — only a test label.
- **Packages.** `language == "en"` and `canonical is True` on both packages;
  `from`/`to` pins match packages A/B; `grounding.from_anchor` /
  `grounding.to_anchor` equal the endpoint `source_anchor` values.
- **Permissions.** Current `permitted: true`, `accessible: true` and
  `revoked: false` (all three present booleans) on both request pins.
- **R2 review binding.** Among reviews whose release pins equal the request
  pins, select those bound to this `relation_id` and `reviewed_edge_revision`
  (order-independent). With none, refuse (`review_edge_mismatch`) or, on the
  A5 unresolved path, `no_bound_edge_review`. With more than one bound review
  that disagree on `verdict`, refuse (`review_verdict_conflict`). The selected
  review requires non-empty string `reviewer` distinct from relation / package
  authors, `verdict == "accepted"`, `scope` compatible with assessment scope,
  and `pin_manifest_digests` equal to package A/B manifest bytes.
- **R3 comparability.** For `compares_with`, all four `PREMISE_OVERLAP_FIELDS`
  pairs (units, quantifier scope, conditions, valid time) must be present and
  equal — the same constant as the A5 path. Missing any pair →
  `inspectable_unresolved` / `unit_scope_unresolved`. Unequal time/conditions →
  `conditions_incompatible`. Unequal units/scope or `unit_scope_aligned is not
  True` → `unit_scope_unresolved`. `unit_scope_aligned` does not waive any
  missing field.
- **A3 / A9 order.** Unresolved mandatory dependencies are evaluated before the
  copied-support early return, so `use_closure_incomplete` is preserved.
- **A5 contradiction (KC-SWE fail-closed interpretation pending KC-Brain).**
  `harmonized: true` alone is an author assertion, not proof. Retention requires
  affirmative equal peer overlap fields (units, quantifier scope, conditions,
  valid time) **and** an R2-bound review of this exact edge. Missing overlap →
  `inspectable_unresolved` / `premise_overlap_unproven`; missing bound review →
  `inspectable_unresolved` / `no_bound_edge_review`; unequal overlap →
  `conditions_incompatible`.

Missing fields, non-string `path` when present, `rendition_of` relation edges,
path segments named `translations` (any case), same `package_id` on both sides,
and `contradicts_under` without an explicit common assumption are typed
refusals (exit 1). Malformed shapes yield `malformed_input`; `evaluate()` and
the CLI never crash without a JSON refusal report. Input is read at most
`MAX_INPUT_BYTES+1` bytes.

It is **not** independent scientific review, production validation,
authorization, an execution grant, or a released wire schema. `book-package/2`
stays unchanged. Unknown overlay profile versions fail closed.

```sh
python3 -B tools/cross_package_overlay.py --input /path/to/document.json
python3 -B -m unittest tools.test_cross_package_overlay -v
```

Exit codes:

| Code | Meaning |
| --- | --- |
| `0` | Accepted/complete inspectable outcome (`inspectable`, `prerequisite_closure_complete`, `accepted`) |
| `1` | Typed refusal (always with a JSON report) |
| `2` | Usage error |
| `3` | Incomplete-but-inspectable (`inspectable_unresolved`, e.g. A2 unit/scope, A5 unproven overlap, or A9a use-closure) |

A missing report must never be read as pass. `request_pins` and matching review
pins must contain exactly keys `A` and `B` selecting the overlay package
releases. Permission flags `permitted` / `accessible` / `revoked` must all be
present real booleans with the affirmative A10 values above; A9 `discharged`
must be a real boolean. Duplicate JSON keys are refused at load. This
preparation never sets `effects_authorized: true`.

### NOT_MEASURED

- live Muneral producer package admission or KCLIVE-08 task closure
- independent scientific peer review of candidate relations
- production authorization, delivery or durable effect identity
- rendition/K8 sidecar endpoint verification
- overlays beyond exactly two canonical English packages
- released `cross-package-relations` wire schema registration

## Retrieval-context checker

`verify_retrieval_context.py` binds the accepted retrieval-and-context paper
bytes (`PAPER_SHA256` and `PROTECTED` digests) and runs finite abstract
selection/delivery controls. CI must invoke it explicitly; a green
publication-integrity job that never ran the checker is not a pass for this
control.

Title-only projection (`--title-only-against <git-blob-or-path>`) proves that a
candidate differs from pinned accepted bytes only in a constrained title shape:
front-matter `title` may change; `subtitle` / `short_title` may be added or
changed; `previous_title` may be added and must equal the accepted title;
before the H1 at most the MD033 markdownlint comment, an `<a id>` whose id is
the GitHub slug of the accepted H1, and one blank line; the H1 must equal a
hash-space prefix plus the new title text. Every other byte must stay
identical. It does not judge the new name. Any other change refuses with a
typed reason and a non-zero exit.

```sh
python3 -B tools/verify_retrieval_context.py \
  --paper papers/retrieval-and-context-composition/PAPER.md
python3 -B tools/verify_retrieval_context.py \
  --paper papers/retrieval-and-context-composition/PAPER.md \
  --title-only-against 9311c0d157d5a926e3c08f6a087a53866064f4e0
python3 -B -m unittest tools.test_verify_retrieval_context -v
```

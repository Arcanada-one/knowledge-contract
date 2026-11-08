# Tools

Bounded repository checks and fixtures. They are author-side engineering
controls: they are not independent scientific review, production verification,
or a substitute for manuscript peer review.

## Cross-package overlay preparation

`cross_package_overlay.py` is a **bounded producer-side preparation** for the
G11 draft model in `reference/relations/CROSS-PACKAGE-OVERLAY.md` section 3. It
evaluates one candidate overlay over **exactly two distinct canonical English
packages**, with endpoint identity = full package release pin + local object id.

**Fail closed (default deny).** A passing/inspectable status is returned only
after every A10 condition is affirmatively established: full release digests,
`language == "en"` and `canonical is True` on both packages, `from`/`to` pins
matching packages A/B, current `permitted: true` and `accessible: true` (not
revoked) on both request pins, and an **independent** scoped review whose pins
equal the request pins. Missing fields, `rendition_of` relation edges, path
segments named `translations` (any case), same `package_id` on both sides, and
`contradicts_under` without an explicit common assumption + `harmonized: true`
are typed refusals (exit 1). Input is read at most `MAX_INPUT_BYTES+1` bytes.

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
| `3` | Incomplete-but-inspectable (`inspectable_unresolved`, e.g. A2 unit/scope or A9a use-closure) |

A missing report must never be read as pass. `request_pins` and matching review
pins must contain exactly keys `A` and `B` selecting the overlay package
releases. Permission flags `permitted` / `accessible` / `revoked` and A9
`discharged` must be real booleans. Duplicate JSON keys are refused at load.
This preparation never sets `effects_authorized: true`.

### NOT_MEASURED

- live Muneral producer package admission or KCLIVE-08 task closure
- independent scientific peer review of candidate relations
- production authorization, delivery or durable effect identity
- rendition/K8 sidecar endpoint verification
- overlays beyond exactly two canonical English packages
- released `cross-package-relations` wire schema registration

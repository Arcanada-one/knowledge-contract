# Tools

Bounded repository checks and fixtures. They are author-side engineering
controls: they are not independent scientific review, production verification,
or a substitute for manuscript peer review.

## Cross-package overlay preparation

`cross_package_overlay.py` is a **bounded producer-side preparation** for the
G11 draft model in `reference/relations/CROSS-PACKAGE-OVERLAY.md` section 3. It
evaluates one candidate overlay over **exactly two distinct canonical English
packages**, with endpoint identity = full package release pin + local object id.

It is **not** independent scientific review, production validation,
authorization, an execution grant, or a released wire schema. `book-package/2`
stays unchanged. Unknown overlay profile versions fail closed.

```sh
python3 -B tools/cross_package_overlay.py --input /path/to/document.json
python3 -B -m unittest tools.test_cross_package_overlay -v
```

Exit `0` only when a typed accepted/inspectable report is printed; exit `1` for
a typed refusal (always with a JSON report); exit `2` for usage. A missing
report must never be read as pass.

### NOT_MEASURED

- live Muneral producer package admission or KCLIVE-08 task closure
- independent scientific peer review of candidate relations
- production authorization, delivery or durable effect identity
- rendition/K8 sidecar endpoint verification
- overlays beyond exactly two canonical English packages
- released `cross-package-relations` wire schema registration

# Machine-readable schemas

The current publication catalogue is validated by [tools/check_publication.py](../tools/check_publication.py). The canonical architecture is defined in [engineering/specifications](../engineering/specifications/README.md).

The [book-package schema](book-package.schema.json) is an implemented versioned profile with [synthetic fixtures](fixtures/book-package/), a [cross-file validator](../tools/check_book_package.py) and [conformance tests](../tools/test_book_package.py). Its complete [specification](../engineering/specifications/book-package/SPECIFICATION.md) separates structural checks from unmeasured conversion fidelity and runtime admission.

This directory does not claim to contain a stable universal Knowledge Contract wire schema. Historical bounded profiles retain their identifiers and measured scope in the [compatibility record](../appendices/source-map/APPENDIX.md#protocol-compatibility). A newly published schema must state its exact profile, interpretation, migration rules and conformance evidence; an editorial edition number is not a wire-format release.

# Machine-readable schemas

The current publication catalogue is validated by [tools/check_publication.py](../tools/check_publication.py). The canonical architecture is defined in [engineering/specifications](../engineering/specifications/README.md).

The [book-package schema](book-package.schema.json) implements `book-package/2` with `KCBook*/v2` record tags, with [synthetic fixtures](fixtures/book-package/), a [cross-file validator](../tools/check_book_package.py) and [conformance tests](../tools/test_book_package.py). Its complete [specification](../engineering/specifications/book-package/SPECIFICATION.md) separates structural checks from unmeasured conversion fidelity and runtime admission.

The [observation and change-event schema](contract-observation.schema.json) implements the bounded `kc-observation/1`, `kc-dependency-change/1` and `kc-profile-advertisement/1` profiles. [Exact synthetic examples](fixtures/contract-observation/valid/), the [validator](../tools/check_contract_profile.py) and [regression tests](../tools/test_contract_profile.py) cover shapes, strict JSON parsing, byte identity, scoped observations and epoch rules. A serialized in-memory publication model exercises the specified atomic guard without claiming a distributed service.

The [document classification schema](document-classification.schema.json) implements `DocumentClassification/v1` for the `kc-doc-class/1` canon of the repository-only [pipeline specification](../engineering/specifications/pipeline/SPECIFICATION.md), with [synthetic fixtures](fixtures/document-classification/) and a [checker](../tools/check_document_classification.py).

The [location registry schema](location-registry.schema.json) implements `LocationRegistry/v1`, `LocationRegistryRow/v1` and `LocationVerifyReceipt/v1` for the repository-only [location-registry specification](../engineering/specifications/location-registry/SPECIFICATION.md), with a [checker](../tools/check_location_registry.py) and [finite tests](../tools/test_location_registry.py). It does not claim a populated live store or KC2 admission.

The [package index card schema](package-index-card.schema.json) implements `PackageIndexCard/v1` and `PackageIngestReceipt/v1` for the repository-only [package-index-ingest specification](../engineering/specifications/package-index-ingest/SPECIFICATION.md), with a [checker](../tools/check_package_index_card.py) and [finite tests](../tools/test_package_index_card.py). Cards carry source/package ids, span and licence/publication state; live Scrutator search, S3 resolve and edge query stay `not_measured` until measured.

The [requirement register](../engineering/specifications/requirements.json) lists stable normative identifiers and distinguishes available finite regression examples from implementation-specific evidence still required.

This directory does not claim to contain a stable universal Knowledge Contract wire schema. Historical bounded profiles retain their identifiers and measured scope in the [compatibility record](../appendices/source-map/APPENDIX.md#4-protocol-compatibility). A newly published schema must state its exact profile, interpretation, migration rules and conformance evidence; an editorial edition number is not a wire-format release.

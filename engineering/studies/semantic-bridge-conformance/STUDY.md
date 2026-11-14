---
name: "semantic-bridge-conformance"
title: "Source Rule Checks: Finite Binding, Alternatives and Operation Composition"
short_title: "Source Rule Checks"
subtitle: "Finite Binding, Alternatives and Operation Composition"
artifact: "engineering-study"
edition: "1.1"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "Actual finite source-binding, Boolean-oracle and operation-composition checks for supplied interpretations, with a retained input-error finding."
study_type: "finite-implementation-evaluation"
review_state: "internally-reviewed; external independence not verified"
---

# Source Rule Checks: Finite Binding, Alternatives and Operation Composition

## Question and result

Can a bounded consumer preserve an explicitly supplied rule, its exception, alternative readings and unknown observations through a checkable computation? The [Semantic Bridge specification](../../specifications/semantic-bridge/SPECIFICATION.md) defines the tested profile. Its input is an authored UTF-8 source with `NOTE` and `RULE` lines and a supplied interpretation packet. It is not an automatic extractor of meaning from unrestricted prose.

The implementation matched a separately authored Boolean-mask oracle on all 256 Boolean functions of three variables under all 64 supplied availability/value profiles: **16,384 evaluation records**. A second complete finite family covers all 256 ordered pairs of two-variable functions under all 16 availability profiles: **4,096 evaluation records**. Four integration checks connect the computed tables to the existing finite relation and outcome-set geometry API. Source/packet and process controls preserve refusal, correlation and unassessed properties. A separate input review found and then closed one real JSON-decoder failure; the initial failure remains available.

These are different finite spaces and checks, not independent empirical trials or evidence of general language understanding. The exact program identities, counts and execution limits are retained in the records below.

## Materials, operation and assumptions

The [implementation](../../../tools/semantic_bridge.py) reads at most 65,536 source bytes and 131,072 packet bytes. Each complete `RULE id: expression` line corresponds to exactly one reading. The source digest, byte selector and quoted line must agree; all declared rule units are retained. A valid source hash alone cannot justify a clipped prefix that drops `UNLESS suspended`.

Readings are alternatives for one query. Each local atom is explicitly bound to an observation identity. A known value fixes that Boolean variable; unknown and withheld values both permit false and true while retaining their different availability states. Aliases of one observation share its value. The evaluator parses the entire supported expression, preserving `NOT`, `AND`, `OR` and the defined `a UNLESS b = a AND NOT b` convention. Up to four readings are evaluated over the same finite world grid.

The observed properties are byte binding, controlled parsing, ordered truth tables, possible-value sets and same-world disagreement. The supplied source choice, interpretation, attribution, referents and factual values remain assumptions. Every report keeps source semantic fidelity, attribution authenticity, real-world truth and current authority at `NOT_ASSESSED`, with `effects_authorized=false`. A computed false value is a valid evaluated result, not a process error. No readings, an unsupported required reading or an invalid source binding produces no evaluated truth.

## Independent expected-result method

The [oracle suite](../../../tools/test_semantic_bridge.py) starts with Boolean truth masks and encodes them as canonical disjunctive normal forms. It filters world masks against supplied known/unknown/withheld records. It does not use the implementation's tokenizer, AST traversal or evaluator to compute expected results. For alternative readings it uses an XOR of their masks restricted to the common allowed worlds.

The oracle was authored by a separate task from the implementation. It shares the controller, model family and host. This is separation of implementation and expected-result structure, not external independence or a blinded evaluation of natural-language annotations. Formula encoding, fixture generation and expected-result code remain inspectable assumptions.

| Finite family | Actual inventory | Observed result |
| --- | --- | --- |
| Three-variable Boolean functions | 256 functions × 64 availability/value profiles | 16,384 records; 55,296 completed world evaluations; 2,952 `TRUE`, 2,952 `FALSE`, 10,480 `UNDETERMINED` |
| Two-variable alternative pairs | 256 ordered pairs × 16 availability/value profiles | 4,096 records; 18,432 reading/world evaluations; 1,088 agreements and 3,008 same-world disagreements |
| Equal possible sets with different conditional behavior | Subset of the alternative family | 984 records have equal possible-value sets but same-world disagreement |
| Source and process controls | Named tests in the same suite | Exact units, stale hashes, CRLF/UTF-8 selectors, incomplete inventories, unsupported alternatives, strict JSON, aliases, constants, finite limits and real CLI exit/report behavior |

The [finite receipt](evidence/finite-oracle.json) records these actual counters and program hashes. Counters are checked against the declared complete inventories; omitting one function or availability profile does not leave a success-shaped reduced denominator. The enumeration covers the stated function families encoded in DNF, not every accepted syntax tree or every possible source string.

## Original source examples and actual CLI use

Four separately authored source/packet pairs are retained under [examples](evidence/examples/lending.en.txt). The English, Russian and Simplified Chinese lending sources contain different original `NOTE` text and the same explicitly authored controlled rule. They are illustrative language renderings, not a measured translation corpus. Exact byte selectors differ with the UTF-8 input and are checked by the real consumer.

The [CLI execution record](evidence/example-cli-runs.json) retains verbatim stdout from four fresh local processes, source and packet hashes, exit codes and implementation identity.

| Source | Supplied uncertainty | Actual calculation |
| --- | --- | --- |
| [English lending](evidence/examples/lending.en.txt) | Suspension unknown; membership and training true | Two worlds, `UNDETERMINED`, no disagreement within the single reading |
| [Russian lending](evidence/examples/lending.ru.txt) | Same authored Boolean assumptions | Two worlds, `UNDETERMINED`; no cross-language fidelity conclusion |
| [Chinese lending](evidence/examples/lending.zh-Hans.txt) | Same authored Boolean assumptions | Two worlds, `UNDETERMINED`; no cross-language fidelity conclusion |
| [Two eligibility readings](evidence/examples/alternatives.en.txt) | One fixed world; two supplied scopes | One world, two different answers, `UNDETERMINED` and reading disagreement |

The oracle also has three original language-wrapper positive fixtures, retained inside its own receipt. Those are distinct inputs with a determinate true controlled result. Neither set is recovered historical evidence or an LLM extraction run. Retaining opaque `NOTE` prose does not establish interpretation of instructions, nested quotations or required media inside that prose.

## Connection to algebra and geometry

The [four integration tests](../../../tools/test_semantic_bridge_relations.py) use actual bridge output as input to [semantic_relations.py](../../../tools/semantic_relations.py). Their [executed receipt](evidence/RELATIONS_INTEGRATION_RUN.json) and [verbatim test log](evidence/RELATIONS_INTEGRATION_TESTS.txt) bind both modules and the test file before and after execution. Their largest carrier has eight states, within the relation API's existing twelve-state limit.

First, the lending rule's eight-world table gives an explicit relation from world indices to Boolean states `0=false`, `1=true`. The observation `(member AND trained, suspended)` yields four classes of sizes 1, 1, 3 and 3 and a coherent quotient. Dropping the suspension observation yields a violating representative pair: identical retained qualifications, different exception status and different computed outputs. This is an actual use of the existing representative-substitution criterion.

Second, composing that relation with a separately computed `NOT flag` relation agrees with directly computing the negated lending rule. Quotient composition agrees with quotienting the concrete result when the declared intermediate Boolean interface is compatible. An incompatible carrier is refused.

Third, restricting the second calculation to known `flag=true` leaves one local row whose index is zero but whose meaning is true. Row numbers cannot be equated with semantic Boolean labels. An explicit embedding in the shared Boolean carrier gives one successful path and seven empty images. The nonempty outcome-set geometry profile correctly refuses those empty images. Absence of a successful relation path is not a false value, an observed refusal or unknown information.

Fourth, two eligibility readings have the same global outcome set `{false,true}`, Hausdorff distance zero and zero set-valued Lipschitz constant. Their aligned tables still disagree in two of eight common worlds. The aggregate-set projection discarded the world labels; zero distance of those sets does not establish conditional substitutability. This is consistent with the stated observation scope of [Knowledge Transformations](../../../papers/constrained-transformations/PAPER.md) and [Meaning Geometry](../../../papers/geometry-of-semantic-representations/PAPER.md), not a counterexample to their conditional results.

## Resolved input failure and review boundary

The [non-author review](../../../reviews/semantic-bridge-20261114/non-author/REVIEW.md) retained a 5,341-byte JSON packet containing a 5,000-digit integer in a byte selector. The initial implementation leaked Python's integer-conversion `ValueError`: exit 1, traceback, no JSON result. The file was below the packet byte bound, so ordinary size validation did not address this failure.

The corrected reader preserves its explicit `BridgeError` codes and normalizes other JSON-decoder `ValueError` and `RecursionError` failures into a structured refusal. The exact saved packet now yields exit 2, `INVALID`, `malformed_json`, no evaluated truth and empty stderr. The suite adds a real subprocess regression with Python's integer limit fixed explicitly. The original module, failed output and corrected output remain separate; the first failure was not overwritten by success.

The reviewer completed 30 separately authored input/status probes against the corrected implementation and found no remaining blocker within that inspected scope. These are distinct from the arithmetic enumeration and not an exhaustive security or correctness proof. The [review record](../../../reviews/semantic-bridge-20261114/non-author/review-record.json) identifies the exact implementation and draft specification. Stable requirement identifiers were subsequently assigned without changing the clauses' meanings. Editorial review also narrowed the specification's downstream-admission acceptance row: this profile retains unassessed authority and implements no downstream admission consumer; no such execution is claimed.

## Reproduction and interpretation

Run from the repository root:

```sh
python3 -B -m unittest tools.test_semantic_bridge tools.test_semantic_bridge_relations -v
python3 -B tools/run_semantic_bridge_controls.py --output /tmp/kc-semantic-bridge-new-run.json
python3 -B tools/semantic_bridge.py \
  --source engineering/studies/semantic-bridge-conformance/evidence/examples/lending.en.txt \
  --packet engineering/studies/semantic-bridge-conformance/evidence/examples/lending.en.packet.json
```

Use a fresh receipt path: the finite runner refuses to overwrite an existing file and checks that program bytes did not change during execution. Its `checkout_head` is the local base, not the identity of uncommitted candidate files; the per-program hashes identify the actual calculation. The full unit suite, review probes and CLI illustrations have their own records and are not all represented by the finite-runner receipt.

All retained evidence files are enumerated by [origin.json](evidence/origin.json). The initial integration run has only post-run source hashes collected during concurrent implementation work; it remains explicitly unbound. A fresh before/after-hash run supplies the usable receipt. No retained old report is silently relabelled as checking the final implementation.

The result closes a finite source-binding and controlled-computation slice of Semantic Bridge. General human-to-formal fidelity, quantifiers, units, time, nested attribution, required media, complete artifact integration and actual agent use remain open. The existing agent-state work, publication decisions, website delivery, index admission and native KC2 admission have separate criteria. No paid experiment was run; cost is `NOT_MEASURED`.

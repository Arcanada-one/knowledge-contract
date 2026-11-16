# Semantic Bridge design review

This is an internal design slice for the next bounded Semantic Bridge increment. It is not an executed test report, source-authentication certificate, release decision or external review. The author of this slice and the implementation/oracle authors share a controller and workspace. The exact source files inspected are recorded in `SOURCE_PINS.json`.

## Gap and selected increment

The existing Semantic Types specification defines the distinctions an interpretation must preserve. Meaning Bridge supplies the conditional adequacy argument, and Meaning in Context separates source fidelity, attributed content, applicability and actual use. Neither the presence of those records nor the finite relation API supplies a bounded, implemented passage from source bytes to complete selected rule units and computed Boolean observations.

Roadmap Semantic Bridge (`roadmap/TASKS.md`, retained anchor `rm-07`) and Foundations Release Plan F02 already request this conversion specification. The proposed target is the existing planned path `engineering/specifications/semantic-bridge/SPECIFICATION.md`. This draft adds a profile there; it does not create a competing science paper or duplicate the semantic-object definition.

The chosen deliverable is `kc-semantic-bridge/1`: supplied plain UTF-8 source, explicit NOTE/RULE envelope, attributed alternative readings, supplied Boolean observation bindings and finite evaluation. It includes an exception, ambiguous alternatives and unsupported construction behavior. The source-to-ordinary-meaning relation remains unassessed. This is a proper subset of the roadmap task, not closure of all its units/time/quantifiers/media/artifact obligations.

## Existing requirement and claim crosswalk

| Existing record | Relevant obligation or claim | v1 coverage and limit |
| --- | --- | --- |
| Semantic Types SEM-R001–SEM-R005 | Distinguishable semantic dimensions and availability | Packet carries only declared supported facets; known/unknown/withheld Boolean states remain distinct. No general facet-completeness claim; no automatic inapplicable-to-false conversion. |
| SEM-R006, SEM-R007 | Interpretation-bound extraction boundaries; separate source/object/representation identity | Whole physical rule line, byte digest and exact selector prevent prefix clipping within a supplied source. This does not prove that the chosen source includes all relevant context. |
| SEM-R008, SEM-R009 | Typed relations, no silent authority or causal upgrade | Local atom-to-observation bindings have declared meaning. Attribution, true Boolean output and source references are never action grants. |
| SEM-R010, SEM-R011 | Exact operator scope and retained alternatives | Controlled grammar, whole-expression parse, all source rule units covered once, all readings evaluated; unsupported reading blocks complete result. |
| SEM-R012–SEM-R014 | Representation revision, required media and actual inspected derivative | Only explicit `text/plain` bytes are inspected. No media or rendered-link claim; media-dependent requests need another adapter. |
| SEM-R015 | False assertion, scoped negation, nested quote, instructional counterexample, alternatives, omitted media | Boolean scope, flat attribution, false supplied assertion and alternatives are in the bounded suite. Nested attribution and essential media are outside the grammar and are not flattened into support. Full SEM-R015 conformance remains unclaimed. |
| KOP-R001–KOP-R006 | Named operation/profile, preconditions, invariants, postconditions and owned/delegated responsibilities | Specification §§1–7 state the local operation and precise delegated assumptions. The local packet/report alone is not a complete authenticated operation-attempt record. |
| KOP-R007–KOP-R010 | Compatible composition, protected observations, loss account | Truth tables/sets and same-world disagreement are protected computed observations. A downstream authority or media precondition is not established by successful computation. |
| KOP-R012–KOP-R015 | Separate result dimensions; evidence bindings; supplied vs independently observed conditions | Local analyzer result codes explicitly map to canonical dimensions. Source hash and supplied annotations are not authenticated observations. Durable run evidence needs its own exact record. |
| KOP-R016, KOP-R017 | Invalid/unknown/partial/budget/stale/effectful and incompatible composition cases | Finite profile has no partial acceptance, mutable requirements service or effects. Relevant input/limit/unknown/composition cases are required. The general effectful-operation suite is not claimed. |
| Contract Core KCC-R001, KCC-R003–KCC-R006 | Scope of conformance; empty/unknown/not-applicable distinctions | At least one reading, one world and one formal observation are present. Zero observation variables is valid only as a one-world constant computation. Empty readings do not yield vacuous adequacy. |
| KCC-R008, KCC-R010–KCC-R014 | Retain constraints and fail closed on unsupported required content | Controlled exception and full alternative inventory preserved. Required unsupported expression blocks the operation; no silent subset claim. |
| KCC-R015–KCC-R018, KCC-R020–KCC-R022 | Current admission, trust, loss and separate schema/applicability/result checks | `effects_authorized=false`; fidelity, authenticity, fact truth and authority are unassessed. No success-shaped formal output after required source/readings fail. |
| Status Model STA-R001–STA-R004, STA-R007, STA-R018 | Independent dimensions, subject-bound observations and no pass escalation | EVALUATED is calculation completion; NOT_ASSESSED maps to `unknown` with reason; TRUE does not map to permission. |
| STA-R021, STA-R025, STA-R026 | Strict JSON, hash-domain binding, no unspecified canonical hashing | Strict duplicate-free JSON packet; exact source SHA-256 uses existing raw-bytes domain. Any later report-value hashing needs a separately named procedure. |
| Context Package CTX-R003, CTX-R004, CTX-R013–CTX-R020 | Joint identity, omitted obligations, protected context, delivery | Shared observation IDs correlate atoms. No delivered-context or visible-link claim from retained source strings; downstream package obligations remain. |
| Artifact Registry REG-R009–REG-R015 | Registered revision, dependencies, retained identity and no grants from artifact presence | Computed rule can be an addressed artifact component. Role, Skill, Competency, Blueprint and Constraint require their own records and criteria. |
| Meaning Bridge §4.1–§4.3 and Proposition 1 | Identity, interpretation and coverage separate; adequacy relative to nonempty modeled questions/domain | Whole-unit byte checks and Boolean function evaluation support their local observations only. Human interpretation adequacy remains unassessed. |
| Meaning Bridge §5.2–§5.3 | Conservative answers over retained interpretations; finite propositional decision problem | Common conditional truth requires agreement across every retained reading and every admitted world. Enumeration does not establish the premise that readings are correct or complete. |
| Meaning in Context §§2–3, Propositions 1 and 4 | Says(author,P) differs from P; more alternatives can remove common consequences | Attribution does not supply true facts. Additional supported alternatives can widen possible answers; unrecognized alternatives may not be dropped. |

## API agreement

Parent author owns `tools/semantic_bridge.py`; a separately tasked agent owns the independent test oracle. Agreed public operations are `read_packet(path)`, `compile_rule(expression)`, `evaluate_ast(ast, values)` and `analyze(source: bytes, packet: dict)`, with CLI `--source` and `--packet`. This design does not duplicate the implementation or oracle.

The report uses `EVALUATED`, `INVALID` and `UNSUPPORTED`; exposes per-reading AST, `table_bits` and `possible_values`; carries ordered `world_assignments`, combined `possible_values`, `truth`, `reading_disagreement` and assessment limits. Source-envelope markers fail closed. Input binding/schema errors are INVALID; source language or formal-language support failures are UNSUPPORTED. Source-boundary corruption and unsupported language do not become a successful subset result.

Critical checks are about behavior, not implementation text: a clipped rule with a correct whole-source digest fails; aliased variables cannot vary independently; `p` and `NOT p` disagree in the same worlds even though their possible-value sets coincide; constants over zero variables have one world; source or packet identities cannot be replaced by a caller's confidence field.

## Authored example status

`examples/lending.en.txt`, `examples/lending.ru.txt` and `examples/lending.zh-Hans.txt` are original illustrative source strings created for this profile. They use the agreed controlled formula with different human-language NOTE text. `examples/alternatives.en.txt` gives two explicit formal alternatives. These texts and their generated selectors are not historical data, independent annotations, model outputs or measured translation results.

Their accompanying packets mechanically bind exact bytes and contain explicitly supplied hypothetical observations. Packet generation is not extraction: the rule identity, atom mapping, referents and discourse role are authored inputs. The example files have not yet been claimed to pass the implementation; that requires actual execution and separately recorded outputs.

## Publication and integration boundary

The canonical specification draft has normal front matter but no invented requirement identifiers. Root will register the new `semantic-bridge` prefix as `SBR`, run the existing assignment/update tool and review the diff. Existing IDs remain unchanged. The draft's normative prose is not a substitute for actual register and publication checks.

The supplied source tree manifest is the parent-fetched tree associated with source main `d5e684e201f6d41498c4fbd8c2a3497eed2bb30e`; this design process checks the inspected files' bytes against its blob identities. The local preparation checkout has Git HEAD `6a6f202f7f70be2ad3aea3369e45409761708596`. Those are different facts; the local HEAD is not claimed to be the remote candidate.

No external source discovery was needed for this slice: the Boolean semantics are explicitly defined here, and the existing papers supply the relevant elementary arguments. No novelty claim, external literature coverage claim or new empirical outcome is made.

The rendered-link failure described by the parent belongs to evidence-link visibility, not quote-to-permission conversion. This draft uses it only to preserve the raw-source-versus-reader boundary. It does not recast that incident as an authorization exploit or claim to have independently reproduced its remote status.

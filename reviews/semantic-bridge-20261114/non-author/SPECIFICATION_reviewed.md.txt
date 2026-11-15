---
name: "semantic-bridge"
title: "Semantic Bridge: From Source Readings to Checkable Operations"
short_title: "Semantic Bridge"
subtitle: "From Source Readings to Checkable Operations"
artifact: "engineering-specification"
edition: "1.1"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
description: "A bounded source-to-formula profile that retains attribution, alternatives, exceptions and the limits of its computed observations."
---

# Semantic Bridge: From Source Readings to Checkable Operations

**Author:** Pavel Valentov · **Publication edition:** 1.1

## 1. Purpose and conformance

A semantic bridge connects inspected source material, explicitly attributed readings, a formal representation and a specified computation. This specification supplies one bounded conversion process for the distinctions in [Semantic Types](../semantic-types/SPECIFICATION.md). Its scientific basis is [Meaning Bridge](../../../papers/human-meaning-and-computable-knowledge/PAPER.md), especially the separation of source identity, interpretive justification and coverage. The semantic-object model remains [Meaning in Context](../../../papers/semantic-objects-and-context/PAPER.md); this document introduces neither a competing theory of meaning nor a general natural-language interpreter.

The executable profile `kc-semantic-bridge/1` reads a supplied plain-text source and a supplied interpretation packet. It checks exact source binding, parses a finite Boolean rule language, and computes the possible values of every retained reading under the supplied observations. It preserves exceptions and alternative readings within that language. The output answers a conditional question about those representations. It does not certify that the readings express the surrounding prose, that an attribution is authentic, that a supplied observation is true, or that an action is authorized.

A conformance statement MUST identify this profile, its immutable implementation revision and the checks actually performed, without promoting the result to full Semantic Types or Knowledge Contract conformance.

Capitalized requirements use [BCP 14](../../../reference/bibliography/BIBLIOGRAPHY.md#requirement-language). Existing requirements retain their identifiers. This profile specializes SEM-R002, SEM-R006–SEM-R011, KOP-R001–KOP-R010 and STA-R001–STA-R004; it does not replace them.

## 2. Operation boundary and responsibilities

The local operation is **analyze supplied alternative rules**. Its input domain consists of a finite source byte string and a packet satisfying Sections 3–5. Its output is either a complete evaluation of that declared interpretation set or an explicit invalid/unsupported diagnostic. Candidate generation, factual investigation, source authentication and action admission belong to other operations.

| Boundary | Owned responsibility | Delegated or unassessed responsibility |
| --- | --- | --- |
| Source to selected units | Verify exact source bytes, whole-rule selectors and the complete inventory of controlled rule units | Whether the supplied source is the intended real-world document or includes all necessary context |
| Units to readings | Retain supplied identities, attribution labels and alternative status | Who really authored or endorsed the content; completeness of plausible natural-language readings |
| Readings to formal objects | Parse the complete controlled expression, preserve operator scope, bind every local atom | Whether the supplied formalization and referent descriptions faithfully interpret ordinary prose |
| Observations to possible worlds | Preserve known, unknown and withheld states; correlate shared observation identities | Whether supplied values were independently measured, current or authentic |
| Formal objects to results | Evaluate every retained reading in every admitted Boolean world | Suitability for an external task, capability, current authority, delivery or execution success |

The source hash is an integrity binding to supplied bytes, not an authentication certificate. An attribution is a supplied claim about authorship or discourse role. No caller-provided value can make either property independently verified merely by appearing in a valid packet.

The operation MUST preserve the distinction between checked structure and supplied semantic or factual assumptions, as required by KOP-R015 and STA-R003.

The [reference implementation](../../../tools/semantic_bridge.py) exposes `read_packet(path)`, `compile_rule(expression)`, `evaluate_ast(ast, values)` and `analyze(source, packet)`. The evaluator's AST precondition is an output of the controlled compiler; it is not a validator for arbitrary caller-built syntax trees. `analyze` returns a structured complete or refused report for supported Python input forms. The CLI invokes the same operation with `--source` and `--packet` paths and returns exit status zero only for `EVALUATED`.

The implementation performs no model calls, repository writes or external actions as part of analysis. A caller that writes the returned report creates its own artifact representation. The CLI reads only the explicitly supplied source and packet and writes its result to standard output. These local behaviors do not implement a general execution or authorization adapter.

## 3. Source identity and complete rule units

The source is at most 65,536 bytes of valid UTF-8 text, supplied with media type `text/plain`. The packet's `source_sha256` is the SHA-256 digest of those exact bytes, using the existing `sha256/raw-bytes-v1` domain. No case folding, Unicode normalization or newline rewriting precedes hashing or selector validation.

Each nonempty physical source line is either a retained-context line `NOTE <human text>` or a controlled rule unit. Empty lines are allowed. A controlled rule unit is a complete physical line of this form:

```text
RULE reading_id: expression
```

Identifiers use ASCII `[a-z][a-z0-9_]{0,31}`. The uppercase markers and rule operators belong to this controlled language. Indented markers, misspelled markers and other nonempty line forms are unsupported; they do not disappear from the inventory as harmless surrounding text. A UTF-8 BOM is not removed to repair a marker. Bare carriage returns and NUL bytes are unsupported. A selector `[start, end)` counts bytes from the beginning of the source. It includes the entire rule line and excludes its LF or CRLF line terminator; a final line need not have a terminator. The selected bytes decode to the packet's exact `quote`. UTF-8 character boundaries and physical line boundaries are both material.

Every controlled rule unit in the supplied source MUST correspond to exactly one supplied reading with the same identifier and complete byte selector.

The operation MUST reject a source digest mismatch, an out-of-range or nonintegral selector, a selector that cuts a UTF-8 character or physical rule line, a mismatched quote, duplicate unit identity, a missing unit, or an extra reading.

This whole-unit rule is stronger than checking that a selected substring parses. For example, the prefix `member AND trained` parses, but selecting it from a line that continues `UNLESS suspended` loses a material exception. Exact bytes for that prefix do not establish that the complete rule was retained.

The text of `NOTE` lines remains available as source context. The profile does not interpret its punctuation, Markdown, HTML, instructions or ordinary-language claims. Notes are not additional compiler premises. In particular, raw source binding does not assert that a link is visible or usable in a rendered page. A future rendered-source adapter needs its own selected reader and rendering observations under CTX-R017; a URL string in source is insufficient evidence of that property.

The rule inventory is exhaustive only over this explicitly marked finite source language. It does not establish completeness of the source, of its meaning, or of all possible readings. Supplying a shorter or different source creates a different byte identity and requires a separate source-selection justification outside this analyzer.

## 4. Typed packet and retained readings

The file packet is a strict UTF-8 JSON object of at most 131,072 bytes with the following exact top-level keys:

| Key | Type and meaning |
| --- | --- |
| `schema` | Exact string `kc-semantic-bridge/1` |
| `source_sha256` | Exact source byte digest |
| `source_media_type` | Exact string `text/plain` |
| `interpretation_set` | Exact string `alternatives` |
| `observations` | Map of zero through eight observation identifiers to Boolean observation records |
| `readings` | Array of one through four attributed reading records |

The complete packet-ingestion and analysis operation MUST reject duplicate member names at every depth, unknown record members, non-finite number tokens, invalid Unicode and type substitutions such as a Boolean used as a byte offset.

Strict packet structure is not a claim that this packet is the full `KCObservation/v1` exchange record. Durable evidence additionally needs the method, observer, time, criterion and exact subject bindings required by STA-R002 and KOP-R013. A run record can reference the source, packet, implementation and report bytes without pretending that a source digest alone supplies those other fields.

### 4.1 Observations and referents

Each observation has `referent`, `type` and `state`. The referent is a supplied description of 1–256 Unicode code points without U+0000–U+001F control characters; `type` is exactly `boolean`; the state is `known`, `unknown` or `withheld`. A known observation has exactly one additional `value` member containing a JSON Boolean. Unknown and withheld observations carry no value.

Known means *supplied as fixed for this computation*, not independently established in the world. Unknown and withheld permit either Boolean value during evaluation, but their availability states remain distinct in the report. Withheld does not mean absent, false or unknown-by-discovery. A referenced Boolean observation with a genuinely inapplicable meaning requires another supported mapping; this profile provides no automatic `not_applicable`-to-false conversion.

Observation identities, rather than similar referent strings, determine shared variables. If two local atom names bind to the same observation, they receive the same value in every world. Conversely, two distinct observation identities do not become identical merely because their supplied descriptions have equal text. The appropriateness of that identity assignment is an input assumption.

### 4.2 Reading records

Each reading has exactly `id`, `start`, `end`, `quote`, `attribution` and `bindings`. Its identifier matches its complete source rule unit. The attribution has exactly an `agent` description, with the same text bounds as a referent, and `discourse`, whose supported values are `asserted`, `quoted` and `hypothetical`. Bindings map each local atom in the expression to an existing observation identifier. Observation identities and local atoms use the same bounded ASCII identifier language as reading identities.

Bindings MUST cover all and only the local atoms used by the expression, and shared observation identities MUST remain correlated throughout evaluation.

The reading array supplies alternatives for one modeled question. It is not a conjunction of separately asserted rules. No reading is preferred by order, attribution label, apparent fluency or the convenience of its answer. Flat attribution is supported; nested quotation, endorsement chains and authenticated authority are not silently flattened into it.

An implementation MUST retain every supplied reading and its attribution and bindings; a required reading that cannot be supported blocks complete evaluation of the interpretation set.

The three discourse labels do not change the Boolean calculation. They qualify what the record says about its source. Calculating the consequences of a quoted or hypothetical expression does not adopt the expression as a current policy. Even an `asserted` expression is not automatically a true assertion.

## 5. Controlled expression language

The supported grammar is:

```text
expr      := or_expr [ UNLESS or_expr ]
or_expr   := and_expr { OR and_expr }
and_expr  := unary { AND unary }
unary     := NOT unary | "(" expr ")" | TRUE | FALSE | atom
atom      := ASCII lowercase identifier
```

`NOT` binds more tightly than `AND`, followed by `OR`, followed by `UNLESS`. Parentheses specify a different scope. The controlled operator `a UNLESS b` is defined as `a AND NOT b`. This is a definition of this formal fragment; it is not a universal analysis of the English word “unless” or its Russian and Chinese counterparts. A sequence containing two unparenthesized `UNLESS` operators is unsupported. Parenthesized nesting has its declared Boolean meaning.

Parsing MUST consume the whole expression and preserve the grammar's operator scopes, without ignoring an unrecognized prefix, suffix or required construct.

Each expression admits at most 128 syntax-tree nodes and a syntax-tree depth of 16. Input preparation additionally permits at most 4,096 expression characters, 512 lexical tokens and syntax nesting of 32. Parentheses do not create a syntax-tree node, so the nesting bound and tree-depth bound are separate. ASCII spaces and tabs separate tokens; the entire rule still occupies one physical source line. Unsupported operators, malformed expressions and expressions outside these finite limits produce an explicit diagnostic, not a truncated formula. The parser's exact result code distinguishes a representation outside the supported language from a malformed packet; neither yields an evaluated truth.

The profile has no quantifiers, numerical comparisons, quantities, units, temporal operators, modal obligations, procedures, media interpretation or automatic referent resolution. Such content may remain in the source as unassessed context. When a requested operation needs it, this profile alone cannot satisfy that request. Adding a Boolean atom named `verified_permission` does not implement a permission checker; it adds another supplied Boolean assumption.

## 6. Possible-world semantics and protected observations

Let \(O\) be the finite observation-identity set. A world is a function \(w:O\to\{0,1\}\) agreeing with every supplied known value. Let \(W\) contain all such worlds. Unknown and withheld values are free, with their distinct states retained in the packet and report. Thus \(1\leq |W|\leq 2^8=256\). In particular, zero observations give one empty assignment, not an empty domain.

For reading \(r\), let \(b_r\) map its local atoms to observation identities, and let \(\varphi_r\) be its parsed expression. Its value in a world is

\[
v_r(w)=\llbracket\varphi_r\rrbracket(w\circ b_r).
\]

The evaluator uses ordinary Boolean constants, negation, conjunction and disjunction, together with the declared expansion of `UNLESS`. The same \(W\) is used for all readings. Observation identifiers are ordered lexicographically; the Cartesian product uses false before true for each free observation and the sole supplied value for each known observation. Readings are reported in source-unit order. The protected computed observations are each reading's ordered truth table, its possible-value set, the union of those sets, and whether readings disagree in the same world.

Define

\[
V_r=\{v_r(w):w\in W\},\qquad
V=\bigcup_r V_r.
\]

The reported truth is `TRUE` when \(V=\{1\}\), `FALSE` when \(V=\{0\}\), and `UNDETERMINED` when \(V=\{0,1\}\). Neither uncertainty nor a retained alternative is silently discarded. A constant result can be supported conditionally even when some observations remain unknown; for example, `p OR NOT p` is true in both possible values of the same observation.

Reading disagreement means

\[
\exists w\in W\;\exists r,s:\;v_r(w)\ne v_s(w).
\]

Comparing only possible-value sets is insufficient. With an unknown observation, the two readings `p` and `NOT p` both have possible-value set \(\{0,1\}\), yet disagree in every world. Conversely, two equivalent formulas can agree in every world while differing in wording or syntax. Such computed agreement does not establish equivalence of all their human meanings.

The operation MUST enumerate every admitted world, evaluate every retained reading under the same observation assignment and report disagreement using same-world comparison.

The finite operational interpretation domain consists of pairs \((r,w)\), with at least one reading and at least one world. At least one material computed observation—the Boolean value of each retained rule—is specified. These conditions avoid an empty-domain or empty-question claim of adequacy. They establish the domain of this computation, not the truth of the source-to-interpretation premises required for broader adequacy by Meaning Bridge §4.2.

The finite calculation terminates under the stated input and syntax limits. Its work is bounded by the source/packet validation and at most four readings, 256 worlds and 128 syntax nodes per reading. This bound concerns the declared representation; it is not an efficiency or termination claim for unrestricted language understanding.

## 7. Results, uncertainty and losses

The local result codes `EVALUATED`, `INVALID` and `UNSUPPORTED` belong to this analyzer. They are not additions to the canonical status-model vocabularies. The mapping below states what each supports for the local operation.

| Analyzer result | Operation outcome and stop reason | Supported interpretation |
| --- | --- | --- |
| `EVALUATED` | `success`, `completed` | All retained controlled rules were evaluated over the specified finite worlds; `UNDETERMINED` is a valid computed result |
| `INVALID` | `refused`, `precondition_not_met` | A required input or source-binding condition failed; no evaluated truth is available |
| `UNSUPPORTED` | `refused`, `precondition_not_met` | The supplied representation or expression is outside this profile; no complete evaluation is available |

A calling task requiring one determinate answer may remain `unresolved` with `clarification_needed` after a successful local calculation returns `UNDETERMINED`. This is a different subject and criterion. The report does not convert success at calculation into success at the downstream task.

The report schema is `kc-semantic-bridge-report/1`. On an evaluated packet it includes the exact source digest, retained observation records, source-ordered readings, ordered `world_assignments`, `valuation_count`, combined `possible_values`, `truth` and `reading_disagreement`. Each reading includes its identity, attribution, bindings, span, quote, AST, `table_bits` and possible values. The bit at position \(i\) records that reading's Boolean result in world \(i\), with false encoded by `0`. Possible-value arrays list false before true when both occur. The AST uses `const`, `atom`, `not`, `and`, `or` and `unless` nodes with the grammar's scopes.

The separate `source_binding` and `controlled_parsing` checks use `VERIFIED` or `NOT_VERIFIED` within their precise scopes. A later unsupported-expression result need not erase a successful byte-binding check, but supplies no evaluated truth. Natural-language fidelity, attribution authenticity, real-world truth and current authority remain `NOT_ASSESSED`; in the canonical status vocabulary this means check result `unknown` with a reason identifying the unperformed assessment. It is not an exemption or a failure verdict. The analyzer always reports `effects_authorized: false`.

An output MUST NOT represent `NOT_ASSESSED` as `pass`, equate computed `TRUE` with current permission, or issue an evaluated truth after any required reading fails validation.

Loss and uncertainty have different meanings here. Unknown or withheld inputs and retained alternatives preserve modeled possibilities. Unsupported constructs are outside the formalization. Uninterpreted surrounding prose is retained source context whose fidelity relation to the formulas was not assessed. A changed source revision, attribution, binding or interpretation set creates new inputs; an old evaluation is not inherited automatically.

This profile supplies no partial admission mode. A consumer wanting to evaluate a smaller interpretation set needs a separately identified request and source-selection justification. Dropping a failed alternative and retaining the original claim of complete coverage violates the profile.

## 8. Worked original examples

The following examples are newly authored illustrations of the profile, not recovered historical observations or measured extraction results. English, Russian and Simplified Chinese prose exercise different UTF-8 byte positions around an explicitly controlled rule. Their translations are illustrative author drafts; the analyzer verifies no cross-language fidelity. In each source, the prose occupies a line prefixed by `NOTE `.

| Language | Surrounding prose, outside the formal fragment |
| --- | --- |
| English | In this example, a member who has completed training meets the camera-lending condition unless lending is suspended. This describes the example's condition and grants no real-world access. |
| Russian | В этом примере участник, прошедший обучение, соответствует условию выдачи камеры, если выдача не приостановлена. Это описание условия примера, а не действующее разрешение. |
| Simplified Chinese | 在本示例中，已完成培训的会员符合借用相机的条件，但借用服务暂停时除外。此陈述描述示例中的条件，不授予现实中的使用权限。 |

Each separate source contains this complete controlled line:

```text
RULE lending: (member AND trained) UNLESS suspended
```

The reading is attributed to the example author as `hypothetical`. The three local atoms bind to three distinct supplied Boolean observations. With `member=true`, `trained=true` and `suspended=false`, the computed value is true. With `suspended=true`, it is false. With suspension unknown or withheld, both values remain possible; the two availability states remain distinct. No case establishes current permission to lend a real camera.

An ambiguity illustration instead supplies two complete units:

```text
RULE broad: (member OR guest) AND trained
RULE narrow: member OR (guest AND trained)
```

These are explicitly supplied alternatives, not readings discovered by an extraction model. For the same world `member=true`, `guest=false`, `trained=false`, their values differ. The report retains both, reports disagreement and leaves the combined truth undetermined. Choosing the more permissive result would change the interpretation set and needs a new justification outside this computation.

A rule using `FORALL`, a numeric comparison or an unavailable media-derived condition cannot acquire support by silently deleting that part. A supported atom may stand for a supplied Boolean assumption about a media source, but that assumption supplies no image-inspection evidence and does not satisfy a task that requires the image itself.

## 9. Finite acceptance profile

Acceptance is against a fixed inventory of obligations, not an open-ended collection of similar examples. A test implementation can group cases, but its report identifies the exact tested inputs, independent expected-result method and implementation revision. The acceptance inventory is:

| Obligation | Required positive or adverse observation |
| --- | --- |
| Complete source binding | Exact digest and full line succeed; changed bytes, wrong quote, clipped prefix/suffix, invalid UTF-8 boundary and missing/duplicate/extra units do not produce an evaluated result; unknown or malformed line markers are not ignored |
| Strict typed packet | Supported records succeed; unknown members, duplicate JSON keys, incorrect scalar types and value/state contradictions are rejected |
| Operator scope and exception | Independent Boolean tables match negation, precedence, parentheses and `UNLESS`; removing the exception changes a material computed observation on a distinguishing world |
| Shared observations | Aliased local atoms receive one correlated value; `p AND NOT q` with both bound to one unknown observation is always false |
| Alternatives | All supplied readings survive; `p` and `NOT p` with an unknown shared observation report same-world disagreement despite equal possible-value sets |
| Nonempty calculation | Constants with zero observations use one world; empty readings are rejected and never certify every answer |
| Unknown and withheld | Both permit both values while preserving their different availability states; neither becomes a supplied false value |
| Attribution boundary | Asserted, quoted and hypothetical records retain their labels without changing arithmetic or issuing permission; a false supplied assertion is not certified as world truth |
| Unsupported input | A required unsupported expression or attribution structure blocks complete evaluation, including when other readings are individually supported |
| Finite limits | Declared limits and over-limit cases have explicit outcomes; evaluation does not truncate the source, expression, worlds or alternatives |
| Original multilingual bytes | The three illustrative sources bind by exact UTF-8 byte selectors and produce the declared controlled result; no translation-accuracy conclusion follows |
| Composition boundary | A valid evaluated result with unassessed authority fails a downstream contract requiring current authorization; a readable rule does not stand in for required media or nested attribution |

The suite MUST exercise these obligations and preserve adverse outcomes rather than changing the declared expected result to fit the implementation.

The broader SEM-R015 suite additionally requires nested quotations, an instructional counterexample and omitted required media. This profile handles only flat attribution and Boolean formulas. Its acceptance record therefore identifies such cases as unsupported or delegated; it does not claim full conformance by relabeling a nested quotation as a flat assertion or an image as a verified Boolean.

Successful finite checks establish behavior only on their declared inputs. They do not measure extraction fidelity, discover every possible interpretation, authenticate sources or establish a causal advantage over another method. A separate reviewer or independently structured oracle on the same controller remains internal technical assessment, not external peer review.

## 10. Composition with artifacts and future profiles

An evaluated formula can become a referenced component of an artifact under the existing [Artifact Registry](../artifact-registry/SPECIFICATION.md). Its containing artifact still needs its own identity, purpose, requirements, constraints and evidence. A Role can reference a condition without granting its holder authority; a Skill can reference a check without proving the executor's capability; a Competency needs actual subject-specific assessment; a Blueprint needs valid component interfaces; a Constraint needs its origin, applicability and enforcement method. These are REG-R009, REG-R015 and KCC-R007–KCC-R017 obligations, not automatic consequences of `EVALUATED`.

The report can support a [Context Package](../context-package/SPECIFICATION.md) only with the exact source and required dependencies retained. The package's coverage, recipient suitability and actual delivery remain separately assessed. A checked source selector is neither a rendered visible link nor proof that a recipient inspected the source.

Future profiles may add quantities, time, quantifiers, richer attribution or media, but each addition requires explicit types, semantics, mappings, resource limits and executable checks where feasible. Their introduction is not a metadata-only upgrade of this profile. Unsupported required material continues to block use under KCC-R013; preserved opaque bytes do not establish semantic support.

The bounded deliverable closes the source-binding and controlled-computation slice of the planned Semantic Bridge. The general human-to-formal conversion, Extraction Fidelity, broader artifact integration and real-world admission work remain separately scoped.

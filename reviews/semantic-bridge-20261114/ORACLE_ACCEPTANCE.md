# Semantic Bridge: proposed finite acceptance design

Status: pre-implementation design; no new execution result. Prepared separately
from the future consumer implementation, using the same controller/model
family/host. Separate authorship is not external independence.

## API freeze update

Root and the scientific-profile author agreed the following narrower API after
this initial design. These choices supersede the provisional grammar, selector
and finite-space options below:

- Source is plain UTF-8, at most 65,536 bytes. Every nonblank physical line is
  `NOTE <human text>` or `RULE <id>: <expression>`; indented or malformed
  markers are unsupported. Selectors cover the complete RULE line, excluding
  LF/CRLF. Every RULE unit is covered exactly once by one of 1–4 readings.
- Grammar uses `NOT > AND > OR > UNLESS`, with parentheses and TRUE/FALSE;
  unparenthesized chained UNLESS is unsupported. Limits: 128 AST nodes, depth
  16 (leaf depth one), and an earlier syntactic recursion guard of 32.
- There are 0–8 declared Boolean observations. Zero observations with a
  constant expression has the one-world domain `{empty assignment}`; this is
  not an empty interpretation set. Unused global observations are allowed.
  Each reading binds all and only its local atoms. Several local atoms may
  alias one observation and must therefore share one completed value.
- `analyze(source, packet)` returns a structured EVALUATED/INVALID/UNSUPPORTED
  report. EVALUATED names completed formal computation, not semantic fidelity
  or authority. All reports retain the four NOT_ASSESSED semantic/authenticity/
  authority/real-world truth boundaries and `effects_authorized=false`.
- Per-reading truth tables use the same ordered global world grid. Reading
  disagreement means a different answer in at least one **same world**. Equal
  sets of possible values do not establish agreement of readings.
- The main exhaustive semantic family becomes all 256 Boolean functions of
  three atoms, encoded independently as DNF, against all 64 availability/value
  records: 16,384 planned calls to the public consumer. A smaller complete
  two-reading family can retain the 4,096 configurations described below.

The earlier arbitrary-slice proposal is therefore strengthened: a shortened
prefix that drops UNLESS is rejected even with a correct whole-source digest.
Human prose outside the controlled RULE unit remains unparsed and its fidelity
unassessed. This does not turn whole-unit coverage into whole-human-meaning
coverage.

## Source basis

The source snapshot is Knowledge Contract main
`d5e684e201f6d41498c4fbd8c2a3497eed2bb30e`, tree
`7980b32385ade338d711d137b833b773b5d510f1`. Root supplied an exact imported tree
at `semantic-bridge-work` and the acquisition receipt `bridge-main-tree.json`.
At initial inspection its local HEAD still named the earlier checkout base;
the read working-tree bytes, not that old HEAD label, are the source here.

The inspected Meaning Bridge, Semantic Types, Evidence and Falsification,
Book Packages and AGENTS files were byte-identical to the previously read
copies. Relevant current SHA-256 values:

| Canonical source | SHA-256 |
| --- | --- |
| `papers/human-meaning-and-computable-knowledge/PAPER.md` | `56f19fd3af7c3020e8a444fd897c02a11bfc0be664cb3e12f863ee3cc988929b` |
| `engineering/specifications/semantic-types/SPECIFICATION.md` | `11e66b5ae19f09cebb06a40616a180d19ecce6bb5166ab749e6b769a7594e206` |
| `papers/evidence-and-falsification/PAPER.md` | `fcc9f1067d256d1eb43b0c5bfe054e8ddfb5665dfa29a978e36247c254a38ca9` |
| `engineering/specifications/book-package/SPECIFICATION.md` | `8c5bdb45f4a47ed66e402dafac1b666da5849c0c78154934a5d868c1451f186b` |

Meaning Bridge sections 4 and 7 separate source identity, interpretation,
coverage, formal computation and current-use authority. SEM-R006 requires
selection to retain relevant conditions; SEM-R010 fixes operator scope;
SEM-R011 retains unresolved readings. SEM-R015 explicitly permits preservation
**or refusal** on its named semantic cases. A bounded profile need not pretend
to interpret all of them automatically. Book Packages already binds anchor
metadata, but explicitly does not verify that a cited source location exists
or supports the text. This increment can add actual raw-byte selector checks
without claiming a general source-fidelity oracle or changing that old claim.

## One executable profile

Support a finite, explicitly versioned Boolean expression language selected
from exact UTF-8 source bytes. Its operators are `atom`, `not`, binary `and`,
binary `or`, and binary `unless`. A fully bracketed/function syntax avoids
implicit precedence; exact spelling and arity must be frozen before coding.
Its stipulated interpretation is:

`unless(P, E) = P and not E`.

This is a declared formal convention, not a proof that every natural-language
use of “unless” has those truth conditions. It also does not infer that a
notice lists a complete eligibility policy. If that assumption is used, retain
it as an interpretation assumption, as Meaning Bridge section 7 already does.

Suggested interface bounds are at most eight declared atoms, four retained
readings, and 256 Boolean valuations per reading. Root should freeze finite
source-byte, token, AST-node and nesting-depth limits with the API. State what
is checked before materialization; a post-materialization cardinality check
must not be advertised as an early memory or input-consumption bound.

The output operation is **describe/evaluate this formal rule under supplied
observations and retained readings**. It is not an operation dispatcher, a
permission service, an automatic natural-language extractor, or an adoption
decision. No dynamic evaluation of source text is part of the profile.

### Pipeline and evidence boundaries

| Stage | Required input/output | What a successful check establishes | What remains separate |
| --- | --- | --- | --- |
| Source | Actual selected representation bytes, declared SHA-256 and byte range | The bytes and slice used by this attempt match the declared identities | Authenticity, adoption, source truth and rendered visibility |
| Attributed readings | Explicit reading IDs, attribution, discourse/source position, atom/referent mapping and assumptions | Supplied readings are structurally supported and remain separately attributable | Whether an annotator found all reasonable readings or mapped prose correctly |
| Observations | Atom-level `known` Boolean values, `unknown` or `withheld`, with their supplied origins | The evaluator uses the supplied states without inventing missing facts | Whether those states match the real world or are currently authoritative |
| Formal object | Full-span grammar parse with exact scoped operators and source binding | The formal object denotes the selected controlled expression | Fidelity of surrounding natural-language prose to that expression |
| Operation | Per-reading possible Boolean values and an explicitly scoped aggregate | Correct finite computation under the declared readings and observations | A permission to borrow, release, copy, execute, publish or dispatch |

The controlled expression may be embedded in an original English, Russian or
Chinese prose fixture. That exercises byte offsets and retention, not
translation fidelity or multilingual understanding.

## Acceptance obligations

These A labels are local verification groups, not new repository requirement
IDs or task identities.

| Group | Acceptance criterion | Useful positive control | Material adverse control |
| --- | --- | --- | --- |
| A1 Exact source binding | Recompute the digest from supplied bytes; validate an in-range nonempty byte slice with valid UTF-8 boundaries; bind the selected slice and source revision to the derivative | A non-ASCII prefix places a valid expression at a byte offset different from its character offset | Changed source under the old digest, wrong slice, or a cut inside a multibyte character cannot pass as the original source |
| A2 Complete selected-span parse | Consume the entire selected expression, with fixed token meanings, arities and nesting; no substring regex success | Valid nested expression and harmless admitted whitespace | Valid prefix followed by an unsupported operator, extra clause or trailing command is not silently ignored |
| A3 Scoped exception | `unless(P,E)` preserves both the condition and exception, including when an exception is unresolved | Camera rule with membership, training and check true, suspension false, evaluates true | Same inputs with suspension true evaluates false; unknown suspension retains both possibilities |
| A4 Shared uncertainty | Complete each unknown/withheld atom consistently across all occurrences | `p or not(p)` is true even when p is unknown; a known false conjunct can decide false despite unrelated unknowns | Replacing unknown by false, assigning repeated occurrences independently, or dropping withheld status changes the result or its observation record |
| A5 Alternative readings | Preserve every supplied reading and its attribution; do not pick the first or silently drop unsupported alternatives | Two different readings that agree on the current answer yield a determinate answer **for those readings**, while both remain present | Disagreeing readings retain both possible values; a supported reading alongside an unsupported reading cannot produce an unqualified all-readings answer |
| A6 Non-vacuity | A missing/empty interpretation set or absent material observation family cannot receive positive adequacy certification | At least one supported reading and one declared material observation produce a useful result | Empty readings, undefined atoms and unjustified required `not_applicable` states are unresolved/refused according to the frozen contract |
| A7 Attribution and use | Source claims, quoted claims, facts supplied to the evaluator and current authority remain separate subjects | A false attributed assertion remains faithfully attributable while a different supplied observation makes the evaluated proposition false | Quoted text or a counterexample saying “grant permission” cannot become a positive permission result or a dispatched effect |
| A8 Explicit support boundary | Unsupported syntax, modality or missing required media is identified within the declared scope | A supported text-only expression runs | Unsupported quantifier, unit expression or required missing legend is not coerced into a Boolean atom/empty value |
| A9 Raw surface boundary | The check names raw UTF-8 source bytes; it makes no statement about Markdown/HTML visibility | An explicitly selected expression in a code fence can be inspected as data | The same byte-valid expression inside a comment/fence cannot be advertised as an observed rendered link or visible adopted rule |
| A10 Actual consumer boundary | The public API/CLI produces the attributed formal object and computation record, with new identity for changed source/profile/selector | A fresh process repeats the declared computation and exact structured result | A cached result bound to old source, expression, observations or reading inventory is not reused as current without matching those inputs |

Operator scope must also be tested directly: nested `not`/`unless` and swapping
their operand scopes can produce different truth tables. This is a semantic
case, not a test for an incidental spelling in the implementation.

## Independent oracle

The consumer may parse an AST and evaluate it recursively. The oracle should
instead represent complete Boolean worlds and formula denotations as integer
bit masks. It selects compatible complete worlds from the supplied partial
observation record and intersects them with a formula's known truth mask.
The resulting possible-value set is:

- `{true}` when every compatible world is in the truth mask;
- `{false}` when none is in it;
- `{false,true}` when both occur.

There must be at least one compatible world under the supported observation
profile. A conflict or invalid input cannot create an empty universe and then
vacuously certify every expression. Unknown and withheld have the same possible
Boolean completions here, but their availability labels and origins remain
different in the result record.

The oracle must not import parser/evaluation helpers from the implementation.
For source checks it compares independently prepared exact byte slices and
fixture identities; a claimed quote is not substituted for the actual source.
For a translated prose wrapper it checks byte identity only. For manual
annotations it does not manufacture a semantic ground truth that was never
independently assessed.

### Proposed complete finite semantic space

Use all 16 Boolean functions on two atoms, supplied as four-bit truth masks.
Construct one canonical controlled-language expression for each function from
its true worlds. This fixture generator uses the mask, not the consumer's
parser or evaluator. Include the constant functions through explicit
contradiction/tautology expressions, without silently extending the grammar.

Then test:

1. Each of the 16 base expressions.
2. `not(F)` for every base function.
3. `and(F,G)`, `or(F,G)` and `unless(F,G)` for every ordered base-function pair.

This declares **800 expression records**: `16 + 16 + 3*16*16`. With the four
availability/value states `known false`, `known true`, `unknown`, `withheld`
per atom, it declares **16 observation records** per expression, hence
**12,800 evaluation comparisons**. These are planned cardinalities, not
executed results. The nine distinct compatible-world sets and the sixteen
availability records are different denominators; unknown and withheld must not
be misrepresented as independent truth conditions.

A second complete space can exercise ordered pairs of base readings:
`16*16*16 = 4,096` reading-pair/observation configurations. Both same-answer and
disagreeing alternatives occur. It is optional only if equivalent full
alternative-aggregation coverage is provided elsewhere; it must not be
replaced by a single happy-path pair.

The four-atom original camera example supplies the practical trace. Its exact
truth mask is constructed independently from membership, training, check and
suspension. Include all 16 complete worlds and all 81 ternary observation
patterns if the report claims that full partial-information space; keep
withheld-label checks separately identified if they are not exhaustively
enumerated there.

This is a complete test of these declared finite families. It is not a claim
to enumerate every expression allowed by an eight-atom/depth-bounded grammar,
nor a sample of independently observed human interpretations. A small separate
boundary control can exercise the chosen eight-atom/four-reading maximum
without pretending that the maximum-size input space was exhaustively tested.

## Status mapping and source ambiguity

Use the existing status dimensions rather than introducing a global `verified`
flag. Parsing a supported expression can finish with operation outcome
`success` even when the result faithfully reports unresolved readings. A
coverage value `unsupported` refers to the declared grammar/profile, not a
claim that the source itself is meaningless. Check results remain `pass`,
`fail`, `unknown`, or justified `not_applicable` (STA-R003).

Successful checks can concern source-byte binding, grammar and arithmetic.
Natural-language fidelity, completeness of retained readings, source
authenticity and effect authority are separate unestablished properties unless
additional observations support them. A valid formal calculation must not
overwrite their unknown statuses.

If a caller deliberately changes both the source bytes and their digest, the
result is a new source identity. The binding checker cannot prove that this
self-consistent new source came from the claimed human or institution.
Likewise, a narrower selector can omit an exception outside its span. The
derivative must bind the changed selector and retain its scoped coverage; raw
byte agreement alone cannot certify complete selection of the original rule.

## Finite completion and retained evidence

Acceptance requires the actual working consumer and public API/CLI, the exact
input/profile files, the independently structured oracle, actual denominators,
and an obligation-to-control mapping. A small fixed set of one-rule faulty
variants should challenge exception preservation, shared uncertainty,
alternative aggregation and source binding while retaining corresponding
valid controls. This is not an open-ended catalogue of examples or a claim of
exhaustive mutation coverage.

The report must distinguish parser tests, Boolean finite comparisons,
attribution/source controls, fresh-process consumer execution and independent
semantic review. Preserve any false positive or unsupported result; a revised
checker receives a new report. Existing historical studies and origin bytes
are not rewritten. No new costly model experiment, runtime authority or source
publication decision follows from completing this finite profile.

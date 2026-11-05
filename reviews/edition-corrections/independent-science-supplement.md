# Independent scientific review supplement

**Verdict: no blocking finding.** I independently read the complete current editions of the retrieval/composition and revision/governance papers. Their seven propositions are valid under their stated premises. Together with the first report’s six completed readings, this establishes a full eight-paper reading boundary; it does not certify production implementations or close the original 26 findings item by item.

## Scope and exact source coverage

The two papers were read in six bounded terminal chunks. All commands exited successfully. Concatenating each paper’s three recorded outputs reproduces its current source bytes exactly, confirming complete coverage without truncation. Both current files and their bodies match the final hashes recorded in the first report. The first reports remain unchanged.

## Retrieval and context composition

**Proposition 1 — scoped finite optimum.** Completed enumeration of the declared finite decision space, with correct feasibility and objective evaluation, rules out an omitted better feasible candidate. Exhaustion without a feasible candidate establishes infeasibility only within that space. The text correctly withholds claims about all possible summaries, semantic annotation correctness, and optimality after early termination.

**Proposition 2 — set-cover reduction.** Mapping universe elements to requirements and subsets to unit-cost independent packages preserves the question “can all requirements be covered with at most k packages?” in both directions. The construction has polynomial representation size. The reduction supports the stated special-case combinatorial difficulty without asserting that every practical query is hard or that another heuristic inherits an approximation ratio.

**Proposition 3 — cardinality-greedy guarantee.** Monotonicity bounds the optimum by the value of the current set united with an optimum set. Submodularity bounds the remaining gain by at most k available single-element gains. Greedy therefore removes at least a 1/k fraction of the remaining gap per step, giving the displayed bound from the normalized empty-set value. If the finite ground set is exhausted earlier, selecting everything is already optimal by monotonicity. The text appropriately restricts the result to the stated cardinality-only problem.

**Changed downward-closure example.** With no dependencies, closure is identity. A mandatory requirement supported only by {a} makes {a} feasible when its cost fits the budget, while the empty subset fails coverage. This correctly disproves downward closure of feasible root selections using the paper’s own support definition. The accompanying explanation distinguishes removing a root from removing an object from the delivered closure. The separate joint-grounds example also correctly violates diminishing returns: adding b after a gains one, while adding b to the empty set gains zero.

## Revision and governance

**Proposition 1 — pinned selection.** Exact resolution of an immutable named revision is independent of the current pointer. The claim correctly concerns selected content, while allowing retrieval failure and withholding guarantees about availability, permission, or current applicability.

**Proposition 2 — check transfer.** Equal complete input tuples yield equal outputs of the same deterministic check. Policy, authorization, interpretation, and evaluation context must be included when relevant. The text explicitly recognizes that changing the evaluator also changes a premise.

**Proposition 3 — reassessment candidates.** Complete dependency representation gives every potentially affected assessment a path to the changed dependency. Reverse reachability therefore finds it. The distinction between an affected candidate and a failed assessment is correct: alternative grounds can preserve validity, while missing edges defeat the completeness premise.

**Proposition 4 — adoption and factual truth.** A satisfying model of A and not F directly refutes entailment of F by the adoption record A. A satisfying model of A and F also rules out entailment of not F, supporting the stronger statement that the contingent content remains undecided. Both satisfiability premises are explicit. They exclude validities and facts already entailed by the adoption record, avoiding an overbroad claim that adoption can never support any factual conclusion.

## Evidence scope and remaining limits

The retrieval paper explicitly limits linked evidence to fixed-graph closure, historical layout/preliminary delivery checks, a separate claim-minimality counterexample, and structural conformance. It says root-subset enumeration is not a budgeted optimizer and that alternative-group/resource-selection results lack an executable selection study in this corpus. Governance describes its linked studies as bounded revision/update and current-eligibility checks. These are appropriately limited claims, not universal correctness or authenticated-authority guarantees.

No linked study was rerun or independently authenticated here. No new literature search, implementation review, executable test, or proof-assistant check was performed. The six completed papers were not reopened. The remaining limits of the first report concerning original-finding closure and implementation evidence still apply.

## Current source hashes

Body hashes cover every byte after the first literal `## Abstract` delimiter, excluding that delimiter. Detailed chunk evidence, proposition locations, and preservation checks are in the JSON supplement.

### retrieval-and-context-composition

- Full file SHA256: `6ebbb43bcdd09ba44b60d6b0e4fce9ec05dcd1550f1d8c43bf451379508b6773`
- Body SHA256: `4225c405071dc6d683ba1f7be4d526e3a4b897bee287029b259e39f73dd116ac`

### revision-and-governance

- Full file SHA256: `e221151a7c6778ef4c6843074a881efead94bad2f0b95e21c697f122c67f58dc`
- Body SHA256: `0bdda439ba1f01fa9feb7039aea98d3be86656bb066a7472669f54fe32f6988c`

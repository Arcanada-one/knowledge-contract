---
artifact_id: KC3_PREREGISTRATION
revision_id: KC3_PREREGISTRATION-r2
title_en: "Pre-registration of falsifiable checks for papers P00 to P13"
language: en
status: pre-registration; no check has been run
license: CC-BY-4.0
sources: none
---

# Pre-registration of falsifiable checks for papers P00 to P13

This document and [`kc3-checks.json`](kc3-checks.json) fix, **before any run**, which claims of the Meaning Management papers are tested on the ARCH-MULTI-1.0 book corpus, how, what is predicted and what would refute it. The machine-readable file is the authority; this page explains it. Its SHA-256 is pinned in [`kc3-checks.sha256`](kc3-checks.sha256) and every later receipt must cite it together with the commit that introduced it (check KC3-P11-C1). A change to the registry without a change to the pin fails the build, so a silent edit shows up as a second changed file in review. The pin is self-attested: it makes a change visible, it does not prevent one.

## What this is, and what it is not

- It registers 23 checks for 13 papers. 1 paper says it has no testable claim on this corpus (below).
- No check has been run. Every entry has `status: unrun`, and at the time of this revision the repository holds no receipt. A test requires every stored receipt to cite the digest of this exact file.
- Each check states where its claim comes from (`claim_origin`): `stated_in_paper`, `derived_from_limit` (the paper states a limit and the check turns it into a prediction) or `registrant_hypothesis` (the paper makes no such claim; the registrant proposes it). Each also states what kind of evidence it gives (`evidence_kind`): `tests_the_claim`, or `regression_of_our_implementation`, which checks that our pipeline conforms to a rule the papers state and **cannot refute a paper**.
- Thresholds marked as the registrant's choice are **not derived from earlier results**. A proportion check is accepted by the checker only if both its prediction and its refutation are reachable at the registered sample size (the Wilson interval of a perfect result at that size must clear the threshold).
- The data does not exist yet: packages come from the conversion work (KC-2); the 21 questions need adjudicated references; the 70 anchored lines need a recorded reference class. Gates make a check `not_measured` until they exist.

## Outcomes

Each check ends in exactly one of `supported` (the prediction held under the registered rule), `refuted` (the refutation condition was met) or `not_measured` (a gate, a control or the sample size failed, or the interval was inconclusive). `not_measured` is a third verdict; it is never read as a pass or as a failure of the paper. A claim is **weakened** when a result is `supported` but carries qualifications (a subset of formats, a failed sub-control, a contaminated question set): the receipt lists them under `qualifications` and must then set `claim_weakened`, and `claim_weakened` is accepted only on a supported outcome with a non-empty list. A refuted or weakened receipt must come with a revision proposal for the paper (route: P10 revision and canon), and the checker verifies that the proposal exists, names this receipt, the same check and paper, and carries the digest of the paper file. When the history is available, it also verifies that the registry commit named by the receipt is an ancestor of the commit that holds the receipt. The run never edits a paper.

## When a claim counts as weakened

A receipt must list a qualification for each of these that applies, and then set `claim_weakened`:

- a gate was met only in part (for example the sample did not cover every format group)
- a control behaved as required but a secondary control failed
- the result holds only on a named subset of formats, languages or question kinds
- the contamination check KC3-P11-C2 reports that memory answers at least half of the questions, for any check that uses the 21 questions
- the reviewer independence class is weaker than registered

Whether a trigger applies is the receipt author's recorded judgement; the checker verifies that the lists and flags agree, not that the author listed everything.

## Decision rules

- **proportion_wilson**: Uses the 95% Wilson interval of the observed proportion and the check's direction and threshold. Direction at_least: supported when the lower bound is at or above the threshold, refuted when the upper bound is below it. Direction below: supported when the upper bound is below the threshold, refuted when the lower bound is at or above it. Any other interval gives not_measured with reason interval_straddles_threshold.
- **exact_all**: Supported when at least n_min cases ran and every case behaved as predicted; refuted when any case violates the prediction (the violating cases are listed); not_measured when fewer than n_min cases ran.
- **paired_difference**: A superiority claim. Computed per question on identical inputs with a 95% percentile bootstrap interval (10000 resamples of the questions, seed recorded in the receipt) of the mean paired difference; for ratios the ratio is recomputed on each resample. Direction positive: supported when the lower bound is above zero (at or above zero when zero_inclusive is true); refuted when the upper bound is at or below zero (below zero when zero_inclusive is true). Direction negative mirrors this. Any other interval gives not_measured with reason interval_includes_zero.
- **paired_difference_no_advantage**: For a prediction that an approach gives no advantage. The check names the sign of an advantage (advantage_sign: positive means a larger difference is an advantage, negative means a smaller one). Supported when the whole interval lies on the no-advantage side or at zero (for advantage_sign negative, lower bound at or above zero; for positive, upper bound at or below zero). Refuted when the whole interval lies strictly on the advantage side. Any other interval gives not_measured with reason advantage_not_excluded.
- **permutation_test**: Supported when the permutation p-value is below 0.05 and every compared group has at least n_min defects. Refuted only when the p-value is 0.05 or above and Cramers V is below 0.10 under the same group sizes: a lack of significance alone is not read as a refutation. Any other result gives not_measured with reason insufficient_defects or effect_not_excluded.
- **descriptive**: No outcome of supported or refuted is possible. The receipt reports the measured values and the outcome is not_measured with reason descriptive_only.

## Gates

- **G-VALID**: Harness validity: before the check counts, its positive control must pass and its negative control must fail on the same harness build. Otherwise the outcome is not_measured with reason control_failed.
- **G-REF**: Reference answers for the 21 knowledge questions are adjudicated against the sources and frozen in a commit before any retrieval run.
- **G-L70**: The 70 short source-anchored lines have a recorded reference class (gold or silver), reviewer type and locator before any CER is computed.
- **G-CAP**: Any check that makes a paid model call needs a spend cap recorded in the task comment and in the receipt before the first call.
- **G-SAMPLE**: The review sample is drawn with a recorded seed from the packages that reached package_status other than blocked_integrity, before reviewers see any object.
- **G-PKG**: The packages come from the converter run recorded by KC-2; a package outside that run is not part of the data.

## Data

- **D-PKG**: Book packages (spec/BOOK_PACKAGE.md) for the non-bibliography-only representations of ARCH-MULTI-1.0 produced by KC-2.
- **D-Q21**: The 21 knowledge questions of the collection plan, with frozen reference answers (gate G-REF).
- **D-L70**: 70 short source-anchored lines with gold or silver references (gate G-L70).
- **D-ADV**: Small adversarial and planted-defect fixtures of the acceptance matrix (cases T01 to T32) plus planted defects created for these checks.
- **D-DUP**: Duplicate and related-edition groups: the archive with six loose PDFs, the two language editions of one work, multi-format editions.

## Checks

| Check | Paper | Claim origin | Evidence kind | Rule | Paid model run | n min |
| --- | --- | --- | --- | --- | --- | --- |
| KC3-P00-C1 | P00 | derived_from_limit | tests_the_claim | permutation_test | no | 30 |
| KC3-P00-C2 | P00 | stated_in_paper | regression_of_our_implementation | exact_all | no | 1 |
| KC3-P01-C1 | P01 | derived_from_limit | tests_the_claim | proportion_wilson | no | 200 |
| KC3-P01-C2 | P01 | stated_in_paper | regression_of_our_implementation | exact_all | no | 1 |
| KC3-P02-C1 | P02 | derived_from_limit | tests_the_claim | proportion_wilson | no | 100 |
| KC3-P02-C2 | P02 | stated_in_paper | regression_of_our_implementation | exact_all | no | 5 |
| KC3-P03-C1 | P03 | stated_in_paper | regression_of_our_implementation | exact_all | no | 20 |
| KC3-P04-C1 | P04 | registrant_hypothesis | tests_the_claim | composite | no | 8 |
| KC3-P04-C2 | P04 | stated_in_paper | regression_of_our_implementation | exact_all | no | 3 |
| KC3-P05-C1 | P05 | derived_from_limit | tests_the_claim | paired_difference | no | 8 |
| KC3-P07-C1 | P07 | stated_in_paper | regression_of_our_implementation | exact_all | no | 5 |
| KC3-P07-C2 | P07 | stated_in_paper | regression_of_our_implementation | exact_all | no | 1 |
| KC3-P07-C3 | P07 | derived_from_limit | tests_the_claim | proportion_wilson | no | 40 |
| KC3-P08-C1 | P08 | stated_in_paper | regression_of_our_implementation | exact_all | no | 20 |
| KC3-P08-C2 | P08 | stated_in_paper | regression_of_our_implementation | exact_all | no | 15 |
| KC3-P10-C1 | P10 | stated_in_paper | regression_of_our_implementation | exact_all | no | 3 |
| KC3-P10-C2 | P10 | registrant_hypothesis | regression_of_our_implementation | exact_all | no | 1 |
| KC3-P11-C1 | P11 | registrant_hypothesis | regression_of_our_implementation | exact_all | no | 1 |
| KC3-P11-C2 | P11 | derived_from_limit | tests_the_claim | proportion_wilson | yes | 21 |
| KC3-P12-C1 | P12 | stated_in_paper | regression_of_our_implementation | exact_all | no | 30 |
| KC3-P13-C1 | P13 | registrant_hypothesis | tests_the_claim | paired_difference_no_advantage | yes | 15 |
| KC3-P05-C2 | P05 | stated_in_paper | regression_of_our_implementation | exact_all | no | 20 |
| KC3-P06-C1 | P06 | stated_in_paper | tests_the_claim | exact_all | no | 20 |

For the full claim, procedure, prediction, refutation and the positive and negative controls of each check, read [`kc3-checks.json`](kc3-checks.json).

## Papers with no testable claim on this corpus

- **P09**: Claims about roles, skills, authority and the KC contract family concern work execution and the contract registry, which a corpus of books does not exercise; the paper's own limits name the registry and migration as not run. Two of its results are touched indirectly: acceptance of false trusted input is registered under KC3-P06-C1, and the comparison with a strong plain alternative under KC3-P04-C1 and KC3-P13-C1.

## Not registered in this round

- A corpus-scale repeat of the exact-reuse latency pilot of P12 (needs a serving path that does not exist yet).
- Checks of P02 and P03 beyond structure and ledger replay.
- The claims of P09 about roles, skills and authority.

## Spend

Two checks (KC3-P11-C2 and KC3-P13-C1) make paid model calls. Decision DEC-AUP-0174 fixes the route (an open-weight model through the project's model connector) and the caps for KC-3 paid checks: USD 1.00 per run and USD 3.00 in total. A receipt with paid calls must record the provider, model, tokens in and out, cost, the cap, the time the cap was recorded and the decision id. The checker rejects a receipt that reports paid calls without these, with a cap above the per-run cap, with a cap recorded after the run started, or with spending above the cap. The total is not checked by the tool: it needs the sum over receipts. If spending reaches a cap, the work stops and is reported; no top-up without a new decision.

## Limits of this registration

- A check that can be passed by a weak harness is not a test; every check names a positive and a negative control and the gate G-VALID makes a failed control end in `not_measured`.
- Twenty-one questions give little statistical power; a conclusive interval is possible only for large effects.
- The reviewers are agents. Their independence class is recorded in every receipt, and nothing here proves independence.
- Testing the papers on books about compression, chosen by the authors, says little about other domains.
- The adjudication of reference answers follows [ADJUDICATION_PROTOCOL.md](ADJUDICATION_PROTOCOL.md).
- The receipt checker validates consistency, not truth: it does not recompute an outcome from the `result` field.

Credit and licence: Knowledge Contract Arcana, <https://contract.place> (CC BY 4.0). See [ATTRIBUTION.md](../ATTRIBUTION.md).

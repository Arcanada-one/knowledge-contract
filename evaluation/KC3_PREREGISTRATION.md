---
artifact_id: KC3_PREREGISTRATION
revision_id: KC3_PREREGISTRATION-r1
title_en: "Pre-registration of falsifiable checks for papers P00 to P13"
language: en
status: pre-registration; no check has been run
license: CC-BY-4.0
sources: none
---

# Pre-registration of falsifiable checks for papers P00 to P13

This document and [`kc3-checks.json`](kc3-checks.json) fix, **before any run**, which claims of the Meaning Management papers are tested on the ARCH-MULTI-1.0 book corpus, how, what is predicted and what would refute it. The machine-readable file is the authority; this page explains it. Its SHA-256 and the commit that introduced it are what every later receipt must cite (check KC3-P11-C1).

## What this is, and what it is not

- It registers 21 checks for 12 papers. 2 papers say they have no testable claim on this corpus (below).
- No check has been run. Every entry has `status: unrun`, and at the time of this revision the repository holds no receipt. A test requires every stored receipt to cite the digest of this exact file; a receipt that cites another digest fails the build.
- Thresholds marked as the registrant's choice are **not derived from earlier results**. They were set before any run so that the outcome cannot move them. They can be criticised; they cannot be changed after a run without a new registry revision and a note in every affected receipt.
- The data does not exist yet. The packages come from the conversion work (KC-2); the 21 questions need adjudicated reference answers; the 70 anchored lines need a recorded reference class. Gates make a check `not_measured` until those exist.

## Outcomes

Each check ends in exactly one of `supported` (the prediction held under the registered rule), `refuted` (the refutation condition was met) or `not_measured` (a gate, a control or the sample size failed, or the interval was inconclusive). `not_measured` is a third verdict. It is never read as a pass or as a failure of the paper. A receipt that says `refuted` must come with a revision proposal for the paper (route: P10 revision and canon); the run never edits a paper.

## Decision rules

- **proportion_wilson**: Uses the 95% Wilson interval of the observed proportion and the check's direction and threshold. Direction at_least: supported when the lower bound is at or above the threshold, refuted when the upper bound is below it. Direction below: supported when the upper bound is below the threshold, refuted when the lower bound is at or above it. Any other interval gives not_measured with reason interval_straddles_threshold.
- **exact_all**: Supported when at least n_min cases ran and every case behaved as predicted; refuted when any case violates the prediction (the violating cases are listed); not_measured when fewer than n_min cases ran.
- **paired_difference**: Computed per question on identical inputs with a 95% percentile bootstrap interval (10000 resamples, seed recorded in the receipt) of the mean paired difference. Direction positive: supported when the interval lies wholly above zero (with zero_inclusive true, when its lower bound is at or above zero), refuted when it lies wholly below zero. Direction negative mirrors this. Any other interval gives not_measured with reason interval_includes_zero.
- **paired_difference_no_advantage**: For a prediction that an approach gives no advantage. Refuted when the interval lies wholly on the side of the advantage. Supported only when the whole interval lies within the equivalence margin (a share of the baseline mean given in the check). Any other interval gives not_measured with reason no_advantage_not_excluded.
- **permutation_test**: Supported when the permutation p-value is below 0.05 and every compared group has at least n_min defects; refuted when the p-value is 0.05 or above under the same group sizes; not_measured with reason insufficient_defects otherwise.
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

| Check | Paper | Basis of the claim in the paper | Rule | Paid model run | n min |
| --- | --- | --- | --- | --- | --- |
| KC3-P00-C1 | P00 | limit | permutation_test | no | 30 |
| KC3-P00-C2 | P00 | authors-domain-assessment | exact_all | no | 1 |
| KC3-P01-C1 | P01 | authors-domain-assessment | proportion_wilson | no | 100 |
| KC3-P01-C2 | P01 | authors-domain-assessment | exact_all | no | 1 |
| KC3-P02-C1 | P02 | hypothesis | proportion_wilson | no | 100 |
| KC3-P02-C2 | P02 | authors-domain-assessment | exact_all | no | 5 |
| KC3-P03-C1 | P03 | finite-test | exact_all | no | 20 |
| KC3-P04-C1 | P04 | hypothesis | composite | no | 8 |
| KC3-P04-C2 | P04 | proof-under-premises | exact_all | no | 3 |
| KC3-P05-C1 | P05 | finite-test | paired_difference | no | 8 |
| KC3-P07-C1 | P07 | finite-test | exact_all | no | 5 |
| KC3-P07-C2 | P07 | finite-test | exact_all | no | 1 |
| KC3-P07-C3 | P07 | finite-test | proportion_wilson | no | 40 |
| KC3-P08-C1 | P08 | authors-domain-assessment | exact_all | no | 20 |
| KC3-P08-C2 | P08 | authors-domain-assessment | exact_all | no | 15 |
| KC3-P10-C1 | P10 | authors-domain-assessment | exact_all | no | 3 |
| KC3-P10-C2 | P10 | authors-domain-assessment | exact_all | no | 1 |
| KC3-P11-C1 | P11 | authors-domain-assessment | exact_all | no | 1 |
| KC3-P11-C2 | P11 | authors-domain-assessment | proportion_wilson | yes | 21 |
| KC3-P12-C1 | P12 | proof-under-premises | exact_all | no | 30 |
| KC3-P13-C1 | P13 | authors-domain-assessment | paired_difference_no_advantage | yes | 15 |

For the full claim, procedure, prediction, refutation and the positive and negative controls of each check, read [`kc3-checks.json`](kc3-checks.json).

## Papers with no testable claim on this corpus

- **P06**: Dialogue and learning claims need human participants or dialogue sessions with a user state. The book corpus has none, and the paper's own limits say understanding, learning effect and interface convenience were not measured.
- **P09**: Claims about roles, skills, authority and the KC contract family concern work execution and the contract registry. A corpus of books does not exercise them; the paper's own limits name the registry and migration as not run.

## Spend

Two checks (KC3-P11-C2 and KC3-P13-C1) need paid model calls. No spend cap is recorded. Until one is recorded in the task and in the receipt, those checks cannot produce `supported` or `refuted`; the validator rejects a receipt that does otherwise.

## Limits of this registration

- A check that can be passed by a weak harness is not a test; that is why every check names a positive and a negative control and the gate G-VALID makes a failed control end in `not_measured`.
- Twenty-one questions give little statistical power. A conclusive interval is possible only for large effects; otherwise the honest result is `not_measured`.
- The reviewers are agents. Their independence class is recorded in every receipt (`same_account_blind_agent` unless another account is used), and nothing here proves independence.
- Testing the papers on books about compression, with books the authors chose, says little about other domains.

Credit and licence: Knowledge Contract Arcana, <https://contract.place> (CC BY 4.0). See [ATTRIBUTION.md](../ATTRIBUTION.md).

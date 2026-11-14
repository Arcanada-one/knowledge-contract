---
title: "Repository Session: Execution and Adoption Review"
status: "same-controller-review-findings-resolved; external-independence-not-verified"
sources: none
license: "CC-BY-4.0"
---

# Repository Session: Execution and Adoption Review

This record concerns a second bounded RM18 increment over Repository Observer at `880d4ea059e8110a81a37348c4cd17075f881780`. All 1,576 baseline file blobs were checked against that exact remote tree before authoring. The observer, its eleven integration tests, the situation model and earlier scientific/observer evidence remain unchanged. The source review of that base is not automatically a review of this new driver.

The implemented boundary is [Repository Session](../../roadmap/agent-situation/REPOSITORY_SESSION.md): an explicit task profile, fresh capture on start/resume/preflight, historical-only inspection, stable semantic context identities, predecessor-preserving receipts and file-only readiness. There are no LLM calls, remote effects, authority grants or new corpus/publication admissions.

## Actual pre-fix finding

The first local integration run passed twelve new session tests and the eleven unchanged observer tests. That pass missed a multi-step adoption error. The non-author reviewer `/root/research_review` reproduced the following real Git lifecycle:

1. Start at required content A: `READY`.
2. Commit required content B and preflight A: `INVALID`, with a newly projected candidate B.
3. Preflight that invalid receipt without any resume: the predecessor implementation returned `VALID` for B.

The second preflight had silently treated the new candidate as an adopted context. This violated the intended distinction between revalidating an adopted context and explicitly resuming with a replacement. The reviewer did not inject a second defect or modify the tested driver.

The original module SHA-256 is `340e69e85d89aa6da363f0a5cf26a3fb7161176e6c9a3aa9cc1506330de5a63f`. Its bytes and actual records are preserved:

- [Original module](../../tools/retained/repository_session_preflight/repository_session_before_preflight_review.py).
- [Repeatable retained-case probe](../../tools/retained/repository_session_preflight/reproduce_preflight_baseline.py).
- [Original observed result](development/repeated-preflight-result.json).
- [The original three complete receipts](development/actual-receipts-before-preflight-fix.json).
- [Reviewer rerun of the retained predecessor](development/retained-baseline-rerun.json).

These files were copied byte for byte from the review workspace. Packaging did not rerun or overwrite them. To perform a new execution of the preserved case without changing its historical outputs:

```sh
python3 -B tools/retained/repository_session_preflight/reproduce_preflight_baseline.py --adapter-root .
```

The probe checks the archived driver and unchanged observer/model hashes, creates a temporary Git repository, and writes a new result to stdout. The three original receipts belong to the predecessor implementation, not to the successor's validated receipt format.

## Successor correction and finite stop criterion

The successor records one explicit operation per capture and reconstructs the adoption state from that operation history and the observation ledger. `context_id` identifies the new candidate; `adopted_context_id` identifies the context explicitly adopted by successful start/resume. A failed preflight retains the adopted anchor and sets `resume_required`. Further preflights still capture but return `RESUME_REQUIRED`. An explicit successful resume can then adopt the new candidate. A failed start/resume leaves no adopted ready context.

The validator derives the anchor, operation result and resume-required state instead of trusting those stored fields. Profile/root mismatch is refused before acquisition; source implementation hashes must match. JSON input rejects duplicate members recursively before interpreting the receipt. Checksums remain internal-consistency checks, not authentication or proof of complete observation/operation history.

The bounded completion criterion is the original observer boundary plus the session transitions exercised by the new tests. The repeated-preflight regression requires:

```text
START(A) → READY
required content changes to B
PREFLIGHT(A) → INVALID; adopted A retained
PREFLIGHT(previous failure) → RESUME_REQUIRED; adopted A retained
PREFLIGHT(previous failure) → RESUME_REQUIRED; adopted A retained
RESUME → READY; B explicitly adopted
PREFLIGHT(B) → VALID
```

A separate recovery check requires an unavailable required file to make resume fail; a later ready capture obtained by preflight still cannot adopt it. Explicit resume is required. Existing positive cases cover unchanged content and unrelated commits, so an always-refuse implementation does not satisfy the criterion.

The exact final code identities, local test output, process-lifecycle sample and repository gates are recorded in the [execution receipt](execution-receipt.json) and adjacent logs. A whole-program, native-speaker, security or controller-independent scientific review is not claimed.

## Non-author successor review

Reviewer `/root/research_review` checked the successor module at SHA-256 `ca4afc21b0256a0c7a7f4d22fea3c483e8ae223a618ef5b87132cd3195c7546a` and test module at `a42809e3aed52c36dda916c42de05121110726a9df7a23a257abda17bc5f068c`. The reviewer did not author those changed bytes. Author and reviewer share the controller/model family and host; this is bounded non-author engineering review, not independent scientific acceptance.

The reviewer's [actual successor result](fixed-session-result.json) and [complete receipts](fixed-session-receipts.json) retain a real Git run with every CLI command in a new process: `READY → INVALID → RESUME_REQUIRED → explicit RESUME READY → PREFLIGHT VALID`. The two failed/locked receipts retained adopted A while projecting candidate B. Only resume adopted B. A separate probe changed an earlier recorded operation to `RESUME` and recomputed the outer receipt digest; inspection refused it with exit two because the predecessor binding disagreed with the retained prefix. The [exact review probe](../../tools/retained/repository_session_preflight/probe_fixed_session.py) is preserved as executed, including its review-workspace paths; the portable current integration checks are the repeatable successor gate.

**Disposition: the repeated-preflight finding is resolved in these successor bytes; no further blocker was found within the inspected lifecycle/receipt scope.** The reviewer did not rerun the complete 25-test suite. That author's execution remains separate evidence, recorded in [integration-tests.txt](integration-tests.txt). Later code changes require renewal of this bounded review.

## Actual executions and repository gates

The final retained [integration log](integration-tests.txt) reports **25 tests, all passing**: fourteen session checks and eleven unchanged observer checks, in 2.939 seconds. These are test methods, not independent scientific observations or a performance benchmark. The [execution receipt](execution-receipt.json) binds that log and every adjacent raw observation file to SHA-256 identities.

The separate [process sample](sample-execution.txt) creates an actual temporary Git repository, records explicit fixture edits/commits and runs each CLI operation in a new process. Its six complete receipts are [start](sample-start.json), [resume after an unrelated commit](sample-unrelated-resume.json), [failed preflight after a required change](sample-preflight-invalid.json), [repeated refused preflight](sample-preflight-repeat.json), [explicit resume](sample-explicit-resume.json) and [successful preflight](sample-preflight-valid.json). The [frozen profile](sample-profile.json) selects two paths and requires one. Outcomes are `READY, READY, INVALID, RESUME_REQUIRED, READY, VALID`. The original receipt bytes remained unchanged. These are new actual local executions using authored fixture contents; they do not observe a production repository or external effect.

The [repository validation log](validation-log.txt) retains an initial environment failure: the system renderer was Pandoc 3.1.11.1, so the required 3.1.3 publication gate and dependent test assertions failed. Selecting the already available pinned Pandoc 3.1.3 binary changed only the command environment. The corrected publication/source/requirement gates passed, all **93 existing publication/source/separation/DCO/CI tests** passed, and the unchanged register still contains **349 requirements**. The initial failure was not removed from the log. `git diff --check` also passed.

Normal publication-integrity CI now has a separate step for the fourteen session tests, following the unchanged eleven-test observer step. Hosted CI for this new increment remains to be observed at the submitted exact head. Local results and the base PR107 review do not substitute for that run or for the successor's own release decision.

## Limits retained

These are finite engineering checks on real local Git repositories, not independent scientific samples. The author and reviewer share the parent controller/model family and host. A complete internally consistent history can be rewritten by its producer. Root digests bind a local address, not provenance or permission. File identity readiness does not establish source-body fidelity, working-tree cleanliness, complete history, current CI, grant authority or an external outcome.

Receipt publication uses a new local path and preserves predecessors. No power-loss durability, concurrent-writer election or production persistence service is established. Context budgets are the unchanged model's abstract units, not serialized LLM tokens. Historical receipts remain historical until a new explicit capture; a fresh result still describes its capture time rather than a race-free future action.

# Dependency decisions and first execution waves

Proposed Coordinated Work programme · 18 November 2026

This note explains the scheduling changes in [execution-graph.json](execution-graph.json). The original [72-step plan](roadmap_steps.json), its acceptance text, source IDs and dependency history are preserved. The proposed graph remains a planning artifact; native assignments, budgets, current task states and execution authority require Muneral records.

## Decision rule

A blocking edge means that the child consumes a named, versioned output from the predecessor. It does not mean that an entire neighbouring research field must be finished first. Every edge records the consumed output and its reason. Source and proposed dependencies are stored separately.

The frozen source graph has 72 work packages, 78 edges and a longest chain of 64 nodes. The proposal has 104 work packages, 247 edges and a longest chain of 17 nodes. Among the imported 72 packages, 41 source edges are removed from the proposed blocking relation and 131 artifact-based edges are added. These counts describe graph structure, not elapsed time or a predicted speed improvement. Actual execution also depends on task size, owner acceptance, capacity, authority and data availability.

## Revision-rationale classes

| Class | Representative work | Decision and retained gate |
| --- | --- | --- |
| Freeze before interpretation | N01 → A01/N02 | Fix source revisions and evidence boundaries before defining review scope or announcing the programme. |
| Separate discovery lanes | A02/A03/A05 → A04/A06 | Seed verification, citation extraction and new searches can proceed from the scope. Identity and full-text appraisal consume their reconciled outputs; discovery does not become appraisal. |
| Parallel taxonomy facets | B02–B06 → B07/B08 | Needs, sector/process mapping, competencies, resources and metrics share unit definitions. They meet at annotation agreement and held-out assessment rather than waiting for each other serially. |
| Draft early, review jointly | C01–C07 → C08 | State schemas and adapters start from their actual definitions. Completed review and applicability gates remain at profile acceptance. |
| Separate model extensions | D03/D04 → D06 → D05/D07/D08 | Buffer/delay and setup/rework extensions can be built independently. Policy comparison consumes shared-resource behavior and an independent oracle; final review consumes the scientific map and organization profile. |
| Distinguish capability from policy | E01/E02/E03/E04 → E05/E08 | Workload, capability evidence and hiring dynamics have different inputs. Alternatives must account for joint assignments, lags, mentoring and team dynamics before a role requirement is accepted. |
| Parallel inference questions | E06/F06; F01–F08 | Causal identification, censoring, forecasting, shocks and lags begin from their observation/model inputs. Scenario construction does not wait for calibrated forecasting and is not labelled a probabilistic forecast. |
| Separate decision mechanisms | G01–G08 | Preconditions, mode readiness, context selection, independent verification, clarification, receipts, concurrency and update review consume explicit artifacts. Observing or recommending never implies execution authority. |
| Register before confirmation | N19 → H01 → H02/H03/H04 | A study protocol precedes confirmatory comparison. Previous exploratory outcomes and later amendments are disclosed; registration is not retroactively claimed. |
| Three distinct stand families | H02; H03; H04 | Production, service and project stand construction has no inter-family serial edge. Each family has its own structural requirements and consumes the registered protocol. |
| Validate actual implementations | H02/H03/H04 → N18 → H05 | Applicability dossiers must evaluate the implemented family models and generators. H05 also consumes the analysis plan and relevant reviewed models; a prospective description cannot validate code that does not yet exist. |
| Evidence before organizational effects | H06/N26/N24/N25 → H07; H07/N29 → H08 | Controlled comparison precedes eligible shadow observation. A causal field claim additionally needs the intervention protocol, identification, authority, spillover treatment, stopping and rollback. |
| Novelty informs design | A07 → N09; A08/B08/N09 → I01 | Contribution appraisal begins before field results. The nearest predecessor can remove a novelty claim or change the experimental question. |
| Release by claim type | N30; I03–I08 | Review/formal work need not wait for a field trial. Each artifact instantiates its own release gates. Organizational-effect claims still require H08 and the appropriate causal evidence. |
| Define publication policy early | N30 without a universal H01 dependency | The publication matrix defines which empirical claims require prior registration. Writing that matrix does not itself satisfy any empirical gate. |
| Publish truthful announcements while registration is pending | N04/N05 → N07; N06/N07 → N08 | An accepted announcement may disclose pending native registration. Complete launch acceptance still requires both served-content verification and actual task/edge readback. |
| Maintain drafts as well as releases | N10/G08 → N32 | Correction, contradiction handling and invalidation policy are needed before indexing. Applying a correction to published material still requires its release and served-content checks. |
| Keep registration and execution separate | N06/N08; all proposed role fields | Graph nodes and proposed roles do not allocate budgets, assign native actors, launch workers or confer runtime admission. Broad work packages are split into bounded child tasks before dispatch. |

## First waves

These are precedence waves computed from the graph, not a calendar or permission to start everything in a row. The launch lane has priority. Parallel research work is selected only within the available work-in-progress limit and accepted owner scope.

| Wave | Launch lane | Eligible parallel foundation work |
| --- | --- | --- |
| 1 | N01: source and evidence freeze | None before the source boundary is fixed. |
| 2 | N02: charter and output families | A01: review scope. |
| 3 | N03: graph and coverage | A02/A03/A05: verification, extraction and search; B01: units; N10: KC evidence lineage. |
| 4 | N04: trilingual announcement; N06: native registration route | A04: identities; B02–B06: taxonomy facets; N15: data rights, privacy and scope. |
| 5 | N05: repository and roadmap integration | A06: first bounded full-text batch; B07: annotation pilot; C01: work graph; E02: competency evidence; N11/N14: objectives and resource validation; N31: terminology. |
| 6 | N07: website release and served readback | A07: claim extraction; B08: held-out classification; C02–C04: events/demand/calendars; D01: balances; F03: external scenarios; G01: prerequisites; N12: admissibility. |
| 7 | N08: owner handoff and complete launch acceptance, if both N06 and N07 are verified | Select the next bounded review/model/design batch from the actual graph; do not dispatch the full programme automatically. |

A native registration blocker does not falsely become a successful registration. N07 can truthfully report pending registration; N08 remains open until the intended nodes, acceptance contracts and dependency edges are read back from Muneral.

The full-text review, benchmark families, comparative runs and per-artifact release templates need smaller child scopes. A06/A07, H02–H06 and I03–I08 are explicitly listed for this decomposition in the graph.

## Representative semantic checks

The publication and hypothesis maps are coverage proposals rather than evidence of scientific success. Internal technical review checked these representative boundaries:

- **Research map (P01):** A01–A08 are retained, including actual full-text appraisal and scoped claim extraction. The supplied bibliographic count cannot satisfy those stages.
- **Flow coordination (P07):** flow semantics, the production family, independent oracle and applicability dossier are linked. The original illustrative probe cannot establish real-system validity.
- **Causal evaluation (P13):** performance/causation, endogenous observation, shadow work, field intervention, analysis and the intervention protocol remain connected. Shadow agreement is not an intervention effect.
- **Transfer across organizations (P15):** taxonomy holdout, distinct domain families, comparative evidence and external-transfer work are linked. A renamed fixture cannot establish external transfer.
- **Clarification hypothesis (HYP09):** the original comparison with always-act, always-ask and threshold rules is preserved. Clarification costs and decision quality must be measured.
- **Stability hypothesis (HYP11):** formal conditions and operational criteria remain distinct. A finite queue trace cannot establish asymptotic stability.
- **Reproduction hypothesis (HYP12):** source/event/decision identity, pinned packages and independent execution receipts remain required. Repeatable code does not establish organizational applicability.

## What the checker establishes

`tools/check_cw_programme.py` verifies source preservation, global identity uniqueness, membership, numbered contracts, internally consistent boundary mappings, valid consumed outputs, acyclicity, exact topology metrics and selected mandatory evidence gates. It rejects duplicate JSON keys, non-finite decoded numbers and invalid Unicode, including escaped lone surrogates.

Its negative controls include reintroduced domain serialization, premature model-validity approval, removal of field prerequisites, contradictory coverage maps, invented execution state, missing root acceptance criteria and malformed input. Valid multilingual text and valid Unicode surrogate pairs remain accepted.

The checker does not establish all semantic choices are scientifically correct, that the graph is optimal, that proposed roles accepted work, that native tasks exist, or that any paper or experiment passed scientific review. This document records internal contributor technical QA; it is not external or non-author scientific acceptance.

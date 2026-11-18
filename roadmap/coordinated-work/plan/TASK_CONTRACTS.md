# Work Contracts: Coordinated Work Package Register

Generated from [execution-graph.json](execution-graph.json). Proposed source contracts; native identity, assignment, readiness and acceptance require separate receipts. Original Russian source acceptance text is preserved verbatim where imported.

## Freeze programme inputs and evidence boundary (CW-N01)

**Proposal:** `CW-N01` · **Epic:** `CW-EP00` · **Russian:** Зафиксировать исходники и границу имеющихся свидетельств

Proposed accountable: **KC-Brain**; executor: **KC-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-N01)

- `CW-N01.O1`: Source and evidence freeze manifest. Intended path: `roadmap/coordinated-work/work-products/launch/source-manifest.md`. Future output, not yet claimed as created.

### Acceptance (CW-N01)

1. All referenced bytes, counts and existing evidence levels reproduced or labelled reported; no discovery record becomes an appraised work.
2. List exact source commits/blobs and reproduce stated counts or label them reported.
3. Separate 190 deterministic probe checks from later studies; preserve zero-full-text-appraisal baseline.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-N01)

- source manifest, count reconciliation and probe provenance
- Exact versions, observed outcome, scope and unresolved limits.
- Adverse case: A retained-record count cannot be labelled a count of unique fully appraised scientific works. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-N01)

No predecessor task in this proposal; use the pinned source package.

## Define programme charter and output families (CW-N02)

**Proposal:** `CW-N02` · **Epic:** `CW-EP00` · **Russian:** Определить программу и семейства результатов

Proposed accountable: **KC-Brain**; executor: **KC-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-N02)

- `CW-N02.O1`: Programme charter and output inventory. Intended path: `roadmap/coordinated-work/work-products/launch/charter.md`. Future output, not yet claimed as created.

### Acceptance (CW-N02)

1. Research questions, intended consumers, scope exclusions, review owners and status vocabulary are explicit.
2. Declare research questions, intended consumers and non-goals across science, engineering and evidence stands.
3. Separate potential papers, engineering deliverables, demonstrations and deployment decisions.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-N02)

- charter, output registry and ownership proposals
- Exact versions, observed outcome, scope and unresolved limits.
- Adverse case: A named theory direction cannot be announced as an established theory. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-N02)

- `CW-N01` → `CW-N01.O1`: Uses Source and evidence freeze manifest to define, constrain or evaluate Programme charter and output inventory.

## Build and validate execution graph (CW-N03)

**Proposal:** `CW-N03` · **Epic:** `CW-EP00` · **Russian:** Сформировать граф исполнения и полное покрытие исходного плана

Proposed accountable: **KC-Brain**; executor: **KC-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-N03)

- `CW-N03.O1`: Versioned execution programme and coverage validator. Intended path: `roadmap/coordinated-work/work-products/launch/dependency-graph.md`. Future output, not yet claimed as created.

### Acceptance (CW-N03)

1. No missing references or cycles; historical dependencies retained; every changed hard edge has rationale; logical IDs distinct from Muneral UUIDs.
2. Preserve all72source IDs, source ACs and historical edges; map16papers and12hypotheses.
3. Validate logical IDs, coverage, hard-edge acyclicity and consumed outputs before task registration.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-N03)

- programme JSON, validator output and graph change rationale
- Exact versions, observed outcome, scope and unresolved limits.
- Adverse case: Orphan tasks, missing hypothesis coverage, cycles and invented native UUIDs must fail validation. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-N03)

- `CW-N02` → `CW-N02.O1`: Uses Programme charter and output inventory to define, constrain or evaluate Versioned execution programme and coverage validator.

## Prepare EN/RU/zh-Hans announcement bundle (CW-N04)

**Proposal:** `CW-N04` · **Epic:** `CW-EP00` · **Russian:** Подготовить анонс и карточки исследований на трех языках

Proposed accountable: **KC-Brain**; executor: **KC-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-N04)

- `CW-N04.O1`: Three-language announcement and research cards. Intended path: `roadmap/coordinated-work/work-products/launch/announcements.md`. Future output, not yet claimed as created.

### Acceptance (CW-N04)

1. All three languages preserve planned/reported/verified distinctions, exact source links and quantities; no placeholder counted as published paper.
2. Create equivalent EN/RU/zh-Hans programme announcement and cards for all16potential papers plus engineering/evidence work.
3. Link every announced scope item to a stable task/epic and preserve exact evidence qualifications.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-N04)

- rendered content, source links, locale matrix and editorial review
- Exact versions, observed outcome, scope and unresolved limits.
- Adverse case: A translation omitting 'planned', evidence limits or zero appraisals must fail parity review. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-N04)

- `CW-N02` → `CW-N02.O1`: Uses Programme charter and output inventory to define, constrain or evaluate Three-language announcement and research cards.
- `CW-N03` → `CW-N03.O1`: Uses Versioned execution programme and coverage validator to define, constrain or evaluate Three-language announcement and research cards.

## Publish repository and roadmap programme entries (CW-N05)

**Proposal:** `CW-N05` · **Epic:** `CW-EP00` · **Russian:** Связать программу с репозиториями и дорожной картой

Proposed accountable: **KC-Brain**; executor: **KC-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-N05)

- `CW-N05.O1`: Repository and roadmap announcement integration. Intended path: `roadmap/coordinated-work/work-products/launch/repository-indexes.md`. Future output, not yet claimed as created.

### Acceptance (CW-N05)

1. Links resolve at exact revisions; programme announcements do not falsely add completed publications to catalogue.
2. Add linked programme entries to existing canonical navigation and roadmap without duplicating old tasks.
3. Use one versioned manifest as the common programme identity across repositories.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-N05)

- diffs, links, target commit readbacks and duplicate check
- Exact versions, observed outcome, scope and unresolved limits.
- Adverse case: An announced research paper must not silently appear as a completed catalogue publication. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-N05)

- `CW-N03` → `CW-N03.O1`: Uses Versioned execution programme and coverage validator to define, constrain or evaluate Repository and roadmap announcement integration.
- `CW-N04` → `CW-N04.O1`: Uses Three-language announcement and research cards to define, constrain or evaluate Repository and roadmap announcement integration.

## Register and read back Muneral graph (CW-N06)

**Proposal:** `CW-N06` · **Epic:** `CW-EP00` · **Russian:** Зарегистрировать граф задач в Muneral и прочитать его обратно

Proposed accountable: **KC-Brain**; executor: **KC-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-N06)

- `CW-N06.O1`: Muneral registration and exact readback ledger. Intended path: `roadmap/coordinated-work/work-products/launch/task-registration.md`. Future output, not yet claimed as created.

### Acceptance (CW-N06)

1. Deduplicate before create; retain real UUIDs and readback; compare intended nodes/edges with actual set; assignment and budget only when explicitly bound.
2. Resolve existing parent/tasks first; create or update only authorized missing records and actual dependency edges.
3. Read back native records and compare intended nodes/edges/numbered ACs; leave actor/budget bindings unassigned until concrete.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-N06)

- native UUID mapping, request/readback hashes and set-difference report
- Exact versions, observed outcome, scope and unresolved limits.
- Adverse case: A local plan with logical IDs or a successful create response alone cannot prove the actual task graph exists. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-N06)

- `CW-N03` → `CW-N03.O1`: Uses Versioned execution programme and coverage validator to define, constrain or evaluate Muneral registration and exact readback ledger.

## Deliver announcement and programme landing (CW-N07)

**Proposal:** `CW-N07` · **Epic:** `CW-EP00` · **Russian:** Опубликовать и проверить анонс на трех языках

Proposed accountable: **KC-Brain**; executor: **KC-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-N07)

- `CW-N07.O1`: Published three-language launch receipt. Intended path: `roadmap/coordinated-work/work-products/launch/website-release.md`. Future output, not yet claimed as created.

### Acceptance (CW-N07)

1. Existing release workflow passes; served content, links, locale switch, feeds and sitemap match release manifest; publication status explicit.
2. Complete repository/site release workflow and verify actual served announcement, roadmap and language routes. Disclose task-registration state from actual readback, or explicitly state that it is pending.
3. Check feeds, sitemap, internal links and locale switch against accepted source manifests.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-N07)

- deployment ID, source pin and served readbacks
- Exact versions, observed outcome, scope and unresolved limits.
- Adverse case: A source merge or English-only route cannot satisfy full trilingual launch. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-N07)

- `CW-N04` → `CW-N04.O1`: Uses Three-language announcement and research cards to define, constrain or evaluate Published three-language launch receipt.
- `CW-N05` → `CW-N05.O1`: Uses Repository and roadmap announcement integration to define, constrain or evaluate Published three-language launch receipt.

## Complete collective handoff and first work batch (CW-N08)

**Proposal:** `CW-N08` · **Epic:** `CW-EP00` · **Russian:** Передать области ответственности и запустить ограниченную первую очередь

Proposed accountable: **KC-Brain**; executor: **KC-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-N08)

- `CW-N08.O1`: Collective ownership and bounded first-batch handoff. Intended path: `roadmap/coordinated-work/work-products/launch/handoff.md`. Future output, not yet claimed as created.

### Acceptance (CW-N08)

1. Existing roles acknowledge substantive scope or report counterexample; no duplicate runtime workers; WIP fits measured capacity.
2. Deliver concrete bounded scope and expected evidence to existing roles; record acceptance or counterexamples.
3. Limit first batch to measured capacity and preserve scientific review separate from implementation.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-N08)

- handoff receipt, accepted scope and WIP/executor ledger
- Exact versions, observed outcome, scope and unresolved limits.
- Adverse case: Creating tasks must not be reported as spawning authorized funded executors. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-N08)

- `CW-N06` → `CW-N06.O1`: Uses Muneral registration and exact readback ledger to define, constrain or evaluate Collective ownership and bounded first-batch handoff.
- `CW-N07` → `CW-N07.O1`: Uses Published three-language launch receipt to define, constrain or evaluate Collective ownership and bounded first-batch handoff.

## Define review scope (CW-A01)

**Proposal:** `CW-A01` · **Epic:** `CW-EP01` · **Russian:** Границы обзора

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-A01)

- `CW-A01.O1`: Review scope and eligibility protocol. Intended path: `roadmap/coordinated-work/work-products/scope/review-protocol.md`. Future output, not yet claimed as created.

### Acceptance (CW-A01)

1. Зафиксированы вопросы, единицы анализа, даты и основания исключения.
2. Declare populations, organizational units, interventions, comparators, outcomes, time cutoffs and languages.
3. Apply inclusion/exclusion rules to a borderline example and record the decision.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-A01)

- scope version, review questions and example decisions
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: Reject a source outside the declared organizational/unit scope without silently changing criteria. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-A01)

- `CW-N01` → `CW-N01.O1`: Uses Source and evidence freeze manifest to define, constrain or evaluate Review scope and eligibility protocol.

Source step `A01` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `prepared` is a historical source observation, not native task state. Original dependencies: none.

Dependency revision: The initial source/evidence freeze precedes review scoping; it requires no research result.

## Verify the seed bibliography (CW-A02)

**Proposal:** `CW-A02` · **Epic:** `CW-EP01` · **Russian:** Проверенное библиографическое ядро

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-A02)

- `CW-A02.O1`: Seed bibliography verification ledger. Intended path: `roadmap/coordinated-work/work-products/corpus/seed-verification.md`. Future output, not yet claimed as created.

### Acceptance (CW-A02)

1. Каждая запись содержит первичный URL, дату проверки и фактическую глубину чтения.
2. Recheck the 157 supplied seed records against primary pages and record metadata/depth separately.
3. Store unresolved/retracted/redirected identity cases instead of inferring full-text appraisal.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-A02)

- record URLs, observed metadata, retrieval dates and exact versions
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: A metadata-only reading cannot satisfy the full-text appraisal state. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-A02)

- `CW-A01` → `CW-A01.O1`: Uses Review scope and eligibility protocol to define, constrain or evaluate Seed bibliography verification ledger.

Source step `A02` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `prepared` is a historical source observation, not native task state. Original dependencies: A01.

Dependency revision: Replaces a phase-order chain with the explicit output prerequisites for this task; the original dependencies and acceptance text remain preserved. Final review/release gates are unchanged in scope.

## Extract citation candidates (CW-A03)

**Proposal:** `CW-A03` · **Epic:** `CW-EP01` · **Russian:** Извлечение цитатных кандидатов

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-A03)

- `CW-A03.O1`: Citation extraction and parent-locator ledger. Intended path: `roadmap/coordinated-work/work-products/corpus/citation-candidates.md`. Future output, not yet claimed as created.

### Acceptance (CW-A03)

1. Сохранены библиографические факты, родительский источник и локатор; кандидаты не повышены до проверенных работ.
2. Keep each candidate linked to the exact parent reference entry and parsing operation.
3. Reconcile the imported candidate count and every later addition/removal by a reasoned delta.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-A03)

- source locator, extraction receipt and count reconciliation
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: A malformed or ambiguous reference remains a candidate and is not silently matched by title. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-A03)

- `CW-A01` → `CW-A01.O1`: Uses Review scope and eligibility protocol to define, constrain or evaluate Citation extraction and parent-locator ledger.

Source step `A03` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `prepared` is a historical source observation, not native task state. Original dependencies: A02.

Dependency revision: Citation extraction consumes the fixed scope and parent-source provenance; complete seed verification is not a blocking prerequisite. Records remain candidates until verified.

## Resolve publication identities (CW-A04)

**Proposal:** `CW-A04` · **Epic:** `CW-EP01` · **Russian:** Разрешение идентичности

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-A04)

- `CW-A04.O1`: Publication identity adjudication ledger. Intended path: `roadmap/coordinated-work/work-products/corpus/identity-adjudication.md`. Future output, not yet claimed as created.

### Acceptance (CW-A04)

1. Все группы совпадений рассмотрены по авторам, изданию и DOI; препринт и журнальная версия связаны явно.
2. Review all supplied duplicate/near-title groups against authors, venue, version and stable identifiers.
3. Preserve separate versions and unresolved records; compute unique-work count only after adjudication.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-A04)

- pair/group decisions, identifiers, reviewers and merge history
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: Same-title different-author works remain distinct; preprint and correction are linked rather than collapsed. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-A04)

- `CW-A02` → `CW-A02.O1`: Uses Seed bibliography verification ledger to define, constrain or evaluate Publication identity adjudication ledger.
- `CW-A03` → `CW-A03.O1`: Uses Citation extraction and parent-locator ledger to define, constrain or evaluate Publication identity adjudication ledger.

Source step `A04` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `partial` is a historical source observation, not native task state. Original dependencies: A03.

Dependency revision: Replaces a phase-order chain with the explicit output prerequisites for this task; the original dependencies and acceptance text remain preserved. Final review/release gates are unchanged in scope.

## Expand field coverage (CW-A05)

**Proposal:** `CW-A05` · **Epic:** `CW-EP01` · **Russian:** Расширение по научным направлениям

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-A05)

- `CW-A05.O1`: Field and temporal search coverage matrix. Intended path: `roadmap/coordinated-work/work-products/corpus/search-coverage.md`. Future output, not yet claimed as created.

### Acceptance (CW-A05)

1. Каждое семейство имеет журнал запросов и новые источники до даты среза; устранён перекос старых обзоров.
2. Record provider, query, date, filters, pagination, returned sets and failures for each research family.
3. Compare field/year distribution before and after expansion and document remaining blind spots.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-A05)

- replayable search logs and inclusion counts by field/year
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: An old personnel-scheduling bibliography cannot satisfy contemporary coverage of all organizational decision domains. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-A05)

- `CW-A01` → `CW-A01.O1`: Uses Review scope and eligibility protocol to define, constrain or evaluate Field and temporal search coverage matrix.

Source step `A05` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: A04.

Dependency revision: Search expansion begins from scope, in parallel with verification/identity work; inclusion/appraisal still waits for the reconciled candidate set.

## Screen full texts (CW-A06)

**Proposal:** `CW-A06` · **Epic:** `CW-EP01` · **Russian:** Отбор полных текстов

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-A06)

- `CW-A06.O1`: Full-text screening and appraisal batch. Intended path: `roadmap/coordinated-work/work-products/review/full-text-appraisals.md`. Future output, not yet claimed as created.

### Acceptance (CW-A06)

1. Для каждого решения включить или исключить есть причина и доступный проверяющий контекст.
2. Separate inability to obtain text from exclusion and from poor methodological quality.
3. Capture study design, assumptions, population, methods, uncertainty and reviewer disagreement for each included work.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-A06)

- lawful full-text version, locators, screening reason and appraisal form
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: A title/abstract-only record cannot enter the appraised-evidence set. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-A06)

- `CW-A02` → `CW-A02.O1`: Uses Seed bibliography verification ledger to define, constrain or evaluate Full-text screening and appraisal batch.
- `CW-A04` → `CW-A04.O1`: Uses Publication identity adjudication ledger to define, constrain or evaluate Full-text screening and appraisal batch.
- `CW-A05` → `CW-A05.O1`: Uses Field and temporal search coverage matrix to define, constrain or evaluate Full-text screening and appraisal batch.

Source step `A06` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: A05.

Dependency revision: Replaces a phase-order chain with the explicit output prerequisites for this task; the original dependencies and acceptance text remain preserved. Final review/release gates are unchanged in scope.

## Extract scoped claims (CW-A07)

**Proposal:** `CW-A07` · **Epic:** `CW-EP01` · **Russian:** Карточки утверждений

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-A07)

- `CW-A07.O1`: Scoped claim and counterclaim ledger. Intended path: `roadmap/coordinated-work/work-products/review/scoped-claims.md`. Future output, not yet claimed as created.

### Acceptance (CW-A07)

1. Утверждения имеют локатор, предпосылки, тип основания, границы переноса и контраргументы.
2. Bind each extracted claim to full-text locators, evidential type, context and known limits.
3. Record at least the nearest counterclaim or a documented failed search for one.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-A07)

- claim IDs, text/version locators, assumptions and counterevidence
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: A finite simulation result cannot become a universal organizational claim. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-A07)

- `CW-A06` → `CW-A06.O1`: Uses Full-text screening and appraisal batch to define, constrain or evaluate Scoped claim and counterclaim ledger.

Source step `A07` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: A06.

Dependency revision: Replaces a phase-order chain with the explicit output prerequisites for this task; the original dependencies and acceptance text remain preserved. Final review/release gates are unchanged in scope.

## Review the scoping map (CW-A08)

**Proposal:** `CW-A08` · **Epic:** `CW-EP01` · **Russian:** Публикация карты литературы

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-A08)

- `CW-A08.O1`: Reproducible scoping review dossier. Intended path: `roadmap/coordinated-work/work-products/review/scoping-map.md`. Future output, not yet claimed as created.

### Acceptance (CW-A08)

1. Есть воспроизводимый протокол, flow отбора, карта пробелов и отдельная содержательная рецензия.
2. Reconcile source-flow counts and disclose duplicate/version handling and appraisal coverage.
3. Obtain a separate substantive review of protocol, evidence-map omissions and limitations.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-A08)

- protocol, flow counts, coded corpus, review findings and corrections
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: High record count cannot be used as a proxy for evidence quality or complete coverage. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-A08)

- `CW-A07` → `CW-A07.O1`: Uses Scoped claim and counterclaim ledger to define, constrain or evaluate Reproducible scoping review dossier.

Source step `A08` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: A07.

Dependency revision: Replaces a phase-order chain with the explicit output prerequisites for this task; the original dependencies and acceptance text remain preserved. Final review/release gates are unchanged in scope.

## Frontload novelty discriminants (CW-N09)

**Proposal:** `CW-N09` · **Epic:** `CW-EP01` · **Russian:** Сопоставить предполагаемый вклад с ближайшими предшественниками

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-N09)

- `CW-N09.O1`: Early discriminating prior-art matrix. Intended path: `roadmap/coordinated-work/work-products/foundations/prior-art.md`. Future output, not yet claimed as created.

### Acceptance (CW-N09)

1. Each proposed contribution names what prior work already supplies and a comparison capable of disproving the claimed increment.
2. State what Malone/Crowston, workforce-planning and relevant control/causal lines already provide after actual appraisal.
3. For each candidate contribution specify an observation or comparison that would remove the claimed increment.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-N09)

- full-text locators, competing-method matrix and discriminants
- Exact versions, observed outcome, scope and unresolved limits.
- Adverse case: Failure to find a competing paper is not positive evidence of novelty. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-N09)

- `CW-A07` → `CW-A07.O1`: Uses Scoped claim and counterclaim ledger to define, constrain or evaluate Early discriminating prior-art matrix.

## Define organizational units (CW-B01)

**Proposal:** `CW-B01` · **Epic:** `CW-EP02` · **Russian:** Единицы организационного анализа

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-B01)

- `CW-B01.O1`: Organizational unit ontology with worked cases. Intended path: `roadmap/coordinated-work/work-products/model/units.md`. Future output, not yet claimed as created.

### Acceptance (CW-B01)

1. Организация, отдел, процесс, операция и Work Item различены на примерах.
2. Give typed examples separating organization, department, process, operation and work item.
3. Define aggregation relations and cases where the same person spans multiple units.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-B01)

- schema and positive/ambiguous examples
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: A department name must not be treated as a complete process graph. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-B01)

- `CW-A01` → `CW-A01.O1`: Uses Review scope and eligibility protocol to define, constrain or evaluate Organizational unit ontology with worked cases.

Source step `B01` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: A08.

Dependency revision: Unit definitions can start from the declared scope; final organizational-profile review consumes the completed evidence map.

## Classify needs and situations (CW-B02)

**Proposal:** `CW-B02` · **Epic:** `CW-EP02` · **Russian:** Фасеты ситуаций и потребностей

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-B02)

- `CW-B02.O1`: Needs and situations taxonomy. Intended path: `roadmap/coordinated-work/work-products/model/needs-situations.md`. Future output, not yet claimed as created.

### Acceptance (CW-B02)

1. Оси независимы насколько возможно; неизвестное и новый класс представлены явно.
2. Represent obligation, demand, risk and improvement opportunity with independent attributes.
3. Include unknown and novel classes and a rule for adding a class without rewriting old labels.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-B02)

- taxonomy version, examples and ambiguity log
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: Missing evidence cannot be assigned to the nearest known class as if observed. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-B02)

- `CW-B01` → `CW-B01.O1`: Uses Organizational unit ontology with worked cases to define, constrain or evaluate Needs and situations taxonomy.

Source step `B02` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: B01.

Dependency revision: Taxonomy facets share the unit ontology, and can be drafted independently before the joint annotation pilot.

## Map sectors and processes (CW-B03)

**Proposal:** `CW-B03` · **Epic:** `CW-EP02` · **Russian:** Сопоставление отраслей и процессов

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-B03)

- `CW-B03.O1`: Versioned sector/process crosswalk. Intended path: `roadmap/coordinated-work/work-products/model/sector-process-crosswalk.md`. Future output, not yet claimed as created.

### Acceptance (CW-B03)

1. ISIC и APQC имеют раздельные роли; их коды не заменяют фактический граф компании.
2. Keep classification identity separate from the measured process and routing graph.
3. Document exact/broader/narrower/related mapping semantics and coverage gaps.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-B03)

- classifier versions, license scope and mapping rationales
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: Matching industry code does not prove the same process topology or capacity constraints. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-B03)

- `CW-B01` → `CW-B01.O1`: Uses Organizational unit ontology with worked cases to define, constrain or evaluate Versioned sector/process crosswalk.

Source step `B03` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: B02.

Dependency revision: Sector/process mappings consume the unit ontology, not the completed needs taxonomy; joint review remains B07.

## Map occupations and competencies (CW-B04)

**Proposal:** `CW-B04` · **Epic:** `CW-EP02` · **Russian:** Сопоставление профессий и компетенций

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-B04)

- `CW-B04.O1`: Occupation, competency and role crosswalk. Intended path: `roadmap/coordinated-work/work-products/model/competency-crosswalk.md`. Future output, not yet claimed as created.

### Acceptance (CW-B04)

1. ISCO, ESCO и O*NET связаны типами exact, broader, narrower, related с версиями.
2. Version each ISCO/ESCO/O*NET relation and distinguish occupation, capability, Role and Skill.
3. Attach evidence, conditions and current authorization separately from occupational labels.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-B04)

- crosswalk, versions and disputed mappings
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: An occupation label or certificate alone cannot satisfy demonstrated task-specific capability and permission. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-B04)

- `CW-B01` → `CW-B01.O1`: Uses Organizational unit ontology with worked cases to define, constrain or evaluate Occupation, competency and role crosswalk.

Source step `B04` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: B03.

Dependency revision: Occupation/capability mapping consumes the unit ontology, not unrelated sequential mapping tasks; joint review remains B07.

## Define resource semantics (CW-B05)

**Proposal:** `CW-B05` · **Epic:** `CW-EP02` · **Russian:** Типы ресурсов

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-B05)

- `CW-B05.O1`: Resource ontology and accounting laws. Intended path: `roadmap/coordinated-work/work-products/model/resource-semantics.md`. Future output, not yet claimed as created.

### Acceptance (CW-B05)

1. Запас, возобновляемая мощность, доступ, информация и знания имеют отдельные правила учета.
2. Specify stocks, renewable capacity, information, access rights and knowledge separately.
3. Define unit, replenishment/consumption, sharing and substitution rules per resource type.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-B05)

- typed schemas and accounting examples
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: Copying information must not consume it under a material conservation law. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-B05)

- `CW-B01` → `CW-B01.O1`: Uses Organizational unit ontology with worked cases to define, constrain or evaluate Resource ontology and accounting laws.

Source step `B05` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: B04.

Dependency revision: Resource semantics consume unit definitions and can run alongside taxonomy axes; joint review remains B07.

## Define performance measures (CW-B06)

**Proposal:** `CW-B06` · **Epic:** `CW-EP02` · **Russian:** Вектор производительности

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-B06)

- `CW-B06.O1`: Outcome and constraint metric dictionary. Intended path: `roadmap/coordinated-work/work-products/model/metrics.md`. Future output, not yet claimed as created.

### Acceptance (CW-B06)

1. Для каждой метрики заданы результат, единица, окно, знаменатель и ограничения интерпретации.
2. Define numerator, denominator, unit, time window, quality threshold and aggregation level.
3. Keep throughput, accepted good output, demand served, WIP, workload, cost and harm distinct.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-B06)

- metric schema and computed examples
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: Increasing local activity cannot be automatically labelled improved organizational performance. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-B06)

- `CW-B01` → `CW-B01.O1`: Uses Organizational unit ontology with worked cases to define, constrain or evaluate Outcome and constraint metric dictionary.

Source step `B06` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: B05.

Dependency revision: Metric definitions consume units and can run alongside taxonomy axes; joint review remains B07.

## Assess annotation agreement (CW-B07)

**Proposal:** `CW-B07` · **Epic:** `CW-EP02` · **Russian:** Проверка согласия классификаторов

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-B07)

- `CW-B07.O1`: Double-coded annotation pilot. Intended path: `roadmap/coordinated-work/work-products/model/annotation-pilot.md`. Future output, not yet claimed as created.

### Acceptance (CW-B07)

1. На пилотной разметке измерено согласие и отдельно разрешены спорные случаи.
2. Use independent initial labels and retain raw disagreements before adjudication.
3. Report agreement by category, prevalence and ambiguity, then freeze revised definitions.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-B07)

- coded sample, coder protocol, agreement calculation and adjudication log
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: Adjudicated consensus cannot be reported as initial independent agreement. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-B07)

- `CW-B02` → `CW-B02.O1`: Uses Needs and situations taxonomy to define, constrain or evaluate Double-coded annotation pilot.
- `CW-B03` → `CW-B03.O1`: Uses Versioned sector/process crosswalk to define, constrain or evaluate Double-coded annotation pilot.
- `CW-B04` → `CW-B04.O1`: Uses Occupation, competency and role crosswalk to define, constrain or evaluate Double-coded annotation pilot.
- `CW-B05` → `CW-B05.O1`: Uses Resource ontology and accounting laws to define, constrain or evaluate Double-coded annotation pilot.
- `CW-B06` → `CW-B06.O1`: Uses Outcome and constraint metric dictionary to define, constrain or evaluate Double-coded annotation pilot.

Source step `B07` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: B06.

Dependency revision: Replaces a phase-order chain with the explicit output prerequisites for this task; the original dependencies and acceptance text remain preserved. Final review/release gates are unchanged in scope.

## Evaluate held-out sectors (CW-B08)

**Proposal:** `CW-B08` · **Epic:** `CW-EP02` · **Russian:** Проверка новых отраслей

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-B08)

- `CW-B08.O1`: Held-out-sector taxonomy evaluation. Intended path: `roadmap/coordinated-work/work-products/model/heldout-sectors.md`. Future output, not yet claimed as created.

### Acceptance (CW-B08)

1. Новые кейсы размечаются без скрытого изменения определений; пробелы сохраняются.
2. Freeze taxonomy and choose unseen sectors/cases before evaluation.
3. Report unmappable cases and any post-evaluation schema changes separately.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-B08)

- holdout manifest, frozen ontology hash and case-level labels
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: Updating definitions from a holdout invalidates the claim that the same holdout remained untouched. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-B08)

- `CW-B07` → `CW-B07.O1`: Uses Double-coded annotation pilot to define, constrain or evaluate Held-out-sector taxonomy evaluation.

Source step `B08` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: B07.

Dependency revision: Replaces a phase-order chain with the explicit output prerequisites for this task; the original dependencies and acceptance text remain preserved. Final review/release gates are unchanged in scope.

## Build the typed work graph (CW-C01)

**Proposal:** `CW-C01` · **Epic:** `CW-EP03` · **Russian:** Граф работы и ответственности

Proposed accountable: **KC-Brain**; executor: **KC-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-C01)

- `CW-C01.O1`: Typed organizational work graph schema. Intended path: `roadmap/coordinated-work/work-products/state/work-graph.md`. Future output, not yet claimed as created.

### Acceptance (CW-C01)

1. Связи потока, полномочий, совместных ресурсов и свидетельств не смешаны.
2. Separate flow, precedence, authority, shared-resource and evidential edges.
3. Express branches, rework, project dependencies and service routing without factory-only assumptions.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-C01)

- schema, examples and topology validation receipts
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: A shared resource cannot be mistaken for a material-flow edge. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-C01)

- `CW-B01` → `CW-B01.O1`: Uses Organizational unit ontology with worked cases to define, constrain or evaluate Typed organizational work graph schema.
- `CW-B02` → `CW-B02.O1`: Uses Needs and situations taxonomy to define, constrain or evaluate Typed organizational work graph schema.
- `CW-B05` → `CW-B05.O1`: Uses Resource ontology and accounting laws to define, constrain or evaluate Typed organizational work graph schema.

Source step `C01` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: B08.

Dependency revision: The work graph uses unit/need/resource semantics; full taxonomy holdout is a later profile-review gate.

## Define event semantics (CW-C02)

**Proposal:** `CW-C02` · **Epic:** `CW-EP03` · **Russian:** Словарь событий

Proposed accountable: **KC-Brain**; executor: **KC-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-C02)

- `CW-C02.O1`: Versioned event and replay schema. Intended path: `roadmap/coordinated-work/work-products/state/event-schema.md`. Future output, not yet claimed as created.

### Acceptance (CW-C02)

1. Время события, наблюдения и получения раздельны; есть идемпотентность и source revision.
2. Keep event time, observation time, receipt time, source revision and attempt identity.
3. Specify duplicates, late arrivals, correction events and deterministic replay semantics.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-C02)

- event fixtures and replay receipts
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: Duplicate delivery cannot double-count a completed work item. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-C02)

- `CW-C01` → `CW-C01.O1`: Uses Typed organizational work graph schema to define, constrain or evaluate Versioned event and replay schema.

Source step `C02` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: C01.

Dependency revision: Replaces a phase-order chain with the explicit output prerequisites for this task; the original dependencies and acceptance text remain preserved. Final review/release gates are unchanged in scope.

## Separate demand observations (CW-C03)

**Proposal:** `CW-C03` · **Epic:** `CW-EP03` · **Russian:** Наблюдаемый и скрытый спрос

Proposed accountable: **KC-Brain**; executor: **KC-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-C03)

- `CW-C03.O1`: Demand observation schema. Intended path: `roadmap/coordinated-work/work-products/state/demand.md`. Future output, not yet claimed as created.

### Acceptance (CW-C03)

1. Продажи, заявки, потерянный и потенциальный спрос не считаются одним показателем.
2. Distinguish requests, sales, served demand, abandonment, backlog, lost and potential demand.
3. Record which quantities are directly observed, censored or estimated.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-C03)

- schema, observation mechanism and example ledger
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: Sales under capacity limits cannot be accepted as uncensored demand. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-C03)

- `CW-C01` → `CW-C01.O1`: Uses Typed organizational work graph schema to define, constrain or evaluate Demand observation schema.
- `CW-B06` → `CW-B06.O1`: Uses Outcome and constraint metric dictionary to define, constrain or evaluate Demand observation schema.

Source step `C03` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: C02.

Dependency revision: Demand semantics use the graph and metric definitions; event/calendaring work can run in parallel.

## Represent availability calendars (CW-C04)

**Proposal:** `CW-C04` · **Epic:** `CW-EP03` · **Russian:** Календарь доступности

Proposed accountable: **KC-Brain**; executor: **KC-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-C04)

- `CW-C04.O1`: Availability, commitments and mentoring calendar. Intended path: `roadmap/coordinated-work/work-products/state/calendar.md`. Future output, not yet claimed as created.

### Acceptance (CW-C04)

1. Часы одного человека не учтены дважды; смены, отсутствие и наставничество различены.
2. Account for overlapping shifts, absences, reserved work, mentoring and shared equipment.
3. Validate interval intersections and time-unit conversions across planning horizons.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-C04)

- calendar fixtures and capacity ledger
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: The same person-hour cannot satisfy two simultaneous full-capacity assignments. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-C04)

- `CW-C01` → `CW-C01.O1`: Uses Typed organizational work graph schema to define, constrain or evaluate Availability, commitments and mentoring calendar.
- `CW-B04` → `CW-B04.O1`: Uses Occupation, competency and role crosswalk to define, constrain or evaluate Availability, commitments and mentoring calendar.
- `CW-B05` → `CW-B05.O1`: Uses Resource ontology and accounting laws to define, constrain or evaluate Availability, commitments and mentoring calendar.

Source step `C04` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: C03.

Dependency revision: Availability calendars use graph, capability and resource definitions; they do not wait for completed demand observations.

## Preserve provenance and conflicts (CW-C05)

**Proposal:** `CW-C05` · **Epic:** `CW-EP03` · **Russian:** Происхождение и конфликты

Proposed accountable: **KC-Brain**; executor: **KC-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-C05)

- `CW-C05.O1`: Evidence conflict-preserving store profile. Intended path: `roadmap/coordinated-work/work-products/state/provenance-conflicts.md`. Future output, not yet claimed as created.

### Acceptance (CW-C05)

1. Конфликтующие источники сохраняются; порядок поступления не подменяет истинность.
2. Keep competing source claims and different attempts identifiable instead of overwriting.
3. Bind accepted interpretations to provenance and an explicit resolution rule.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-C05)

- source/attempt identities, conflict fixtures and resolution log
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: Reordering conflicting input records must not erase contradiction. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-C05)

- `CW-C02` → `CW-C02.O1`: Uses Versioned event and replay schema to define, constrain or evaluate Evidence conflict-preserving store profile.
- `CW-A02` → `CW-A02.O1`: Uses Seed bibliography verification ledger to define, constrain or evaluate Evidence conflict-preserving store profile.
- `CW-N10` → `CW-N10.O1`: Uses Evidence lineage and identity profile reusing KC to define, constrain or evaluate Evidence conflict-preserving store profile.

Source step `C05` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: C04.

Dependency revision: Provenance uses event semantics, verified source identities and KC evidence mapping; calendar completion is not a prerequisite.

## Specify freshness and invalidation (CW-C06)

**Proposal:** `CW-C06` · **Epic:** `CW-EP03` · **Russian:** Обновление и срок пригодности

Proposed accountable: **KC-Brain**; executor: **KC-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-C06)

- `CW-C06.O1`: Dependency invalidation and freshness rules. Intended path: `roadmap/coordinated-work/work-products/state/invalidation.md`. Future output, not yet claimed as created.

### Acceptance (CW-C06)

1. Изменение факта инвалидирует зависимые решения по формальным правилам.
2. Define freshness per fact/decision and propagate source changes over explicit dependency edges.
3. Distinguish invalidated, stale, contradicted and still-valid derived claims.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-C06)

- dependency fixtures, change events and expected invalidations
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: Changing an irrelevant observation must not invalidate unrelated decisions; a relevant change must. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-C06)

- `CW-C05` → `CW-C05.O1`: Uses Evidence conflict-preserving store profile to define, constrain or evaluate Dependency invalidation and freshness rules.

Source step `C06` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: C05.

Dependency revision: Replaces a phase-order chain with the explicit output prerequisites for this task; the original dependencies and acceptance text remain preserved. Final review/release gates are unchanged in scope.

## Prototype authorized adapters (CW-C07)

**Proposal:** `CW-C07` · **Epic:** `CW-EP03` · **Russian:** Адаптеры действующих систем

Proposed accountable: **KC-Brain**; executor: **KC-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-C07)

- `CW-C07.O1`: Authorized read adapter prototypes. Intended path: `roadmap/coordinated-work/work-products/state/adapters.md`. Future output, not yet claimed as created.

### Acceptance (CW-C07)

1. ERP, HRIS, CRM и task tracker читаются через ограниченные интерфейсы и закрепленные схемы.
2. For each ERP/HRIS/CRM/task-tracker adapter record actual allowed interface, schema and scope.
3. Validate source snapshots, pagination, failures and absence of required fields.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-C07)

- adapter contract, authorized sample or synthetic fixture and receipts
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: An inaccessible source cannot be silently substituted with generated organizational data. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-C07)

- `CW-C02` → `CW-C02.O1`: Uses Versioned event and replay schema to define, constrain or evaluate Authorized read adapter prototypes.
- `CW-C03` → `CW-C03.O1`: Uses Demand observation schema to define, constrain or evaluate Authorized read adapter prototypes.
- `CW-C04` → `CW-C04.O1`: Uses Availability, commitments and mentoring calendar to define, constrain or evaluate Authorized read adapter prototypes.
- `CW-C05` → `CW-C05.O1`: Uses Evidence conflict-preserving store profile to define, constrain or evaluate Authorized read adapter prototypes.
- `CW-C06` → `CW-C06.O1`: Uses Dependency invalidation and freshness rules to define, constrain or evaluate Authorized read adapter prototypes.
- `CW-N15` → `CW-N15.O1`: Uses Organizational/personnel data-use and access contract to define, constrain or evaluate Authorized read adapter prototypes.

Source step `C07` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: C06.

Dependency revision: Replaces a phase-order chain with the explicit output prerequisites for this task; the original dependencies and acceptance text remain preserved. Final review/release gates are unchanged in scope.

## Review the organization profile (CW-C08)

**Proposal:** `CW-C08` · **Epic:** `CW-EP03` · **Russian:** Организационный профиль KC

Proposed accountable: **KC-Brain**; executor: **KC-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-C08)

- `CW-C08.O1`: Reviewed KC organization profile. Intended path: `roadmap/coordinated-work/work-products/state/profile-review.md`. Future output, not yet claimed as created.

### Acceptance (CW-C08)

1. Профиль согласован с Agent Situation и Artifact Registry без объявления новых native kinds.
2. Map every proposed field to existing Agent Situation, Context Assembly and Artifact Registry concepts.
3. Record unresolved semantics and implementation gaps with the relevant owner.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-C08)

- profile, compatibility matrix and exact-version review
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: An extension document cannot claim a newly installed native artifact kind or admission authority. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-C08)

- `CW-C07` → `CW-C07.O1`: Uses Authorized read adapter prototypes to define, constrain or evaluate Reviewed KC organization profile.
- `CW-B08` → `CW-B08.O1`: Uses Held-out-sector taxonomy evaluation to define, constrain or evaluate Reviewed KC organization profile.
- `CW-A08` → `CW-A08.O1`: Uses Reproducible scoping review dossier to define, constrain or evaluate Reviewed KC organization profile.

Source step `C08` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: C07.

Dependency revision: Replaces a phase-order chain with the explicit output prerequisites for this task; the original dependencies and acceptance text remain preserved. Final review/release gates are unchanged in scope.

## Define flow conservation (CW-D01)

**Proposal:** `CW-D01` · **Epic:** `CW-EP04` · **Russian:** Явная модель баланса

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-D01)

- `CW-D01.O1`: Typed flow balance equations and executable examples. Intended path: `roadmap/coordinated-work/work-products/flow/conservation.md`. Future output, not yet claimed as created.

### Acceptance (CW-D01)

1. Начальные запасы, выпуск, отходы, возвраты и единицы заданы; знание не подчинено материальному балансу.
2. Include initial inventory, accepted output, waste, returns and consistent units.
3. Check conservation independently on analytically solvable routes.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-D01)

- equations, assumptions and examples
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: Missing initial stock or rework must trigger balance failure rather than be absorbed into output. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-D01)

- `CW-B05` → `CW-B05.O1`: Uses Resource ontology and accounting laws to define, constrain or evaluate Typed flow balance equations and executable examples.
- `CW-N14` → `CW-N14.O1`: Uses Dimensional and resource-type verifier to define, constrain or evaluate Typed flow balance equations and executable examples.

Source step `D01` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: C08.

Dependency revision: Conservation starts from resource semantics and dimensional rules, not the completed organization-profile review.

## Derive conditional throughput bounds (CW-D02)

**Proposal:** `CW-D02` · **Epic:** `CW-EP04` · **Russian:** Узкие места и разрезы

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-D02)

- `CW-D02.O1`: Conditional throughput bounds. Intended path: `roadmap/coordinated-work/work-products/flow/throughput-bounds.md`. Future output, not yet claimed as created.

### Acceptance (CW-D02)

1. Верхняя граница отделена от достижимости и от стратегии управления.
2. State assumptions for every capacity bound and give conditions under which it is unattainable.
3. Separate mathematical upper bound, feasible schedule and chosen policy performance.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-D02)

- derivation, assumptions and counterexamples
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: The minimum nominal stage capacity cannot imply achievable throughput under blocking or rework. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-D02)

- `CW-D01` → `CW-D01.O1`: Uses Typed flow balance equations and executable examples to define, constrain or evaluate Conditional throughput bounds.

Source step `D02` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: D01.

Dependency revision: Replaces a phase-order chain with the explicit output prerequisites for this task; the original dependencies and acceptance text remain preserved. Final review/release gates are unchanged in scope.

## Model buffers and delays (CW-D03)

**Proposal:** `CW-D03` · **Epic:** `CW-EP04` · **Russian:** Конечные буферы и задержки

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-D03)

- `CW-D03.O1`: Finite-buffer and delay flow extension. Intended path: `roadmap/coordinated-work/work-products/flow/buffers-delays.md`. Future output, not yet claimed as created.

### Acceptance (CW-D03)

1. Стенд отражает блокировки, starvation и ненулевое время прохождения.
2. Represent blocking, starvation, transit times and backlog policy explicitly.
3. Match hand-calculated edge cases for zero/full buffers and delayed releases.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-D03)

- model equations, event traces and oracle comparisons
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: An infinite-buffer or zero-transit simplification cannot pass a finite-buffer benchmark unnoticed. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-D03)

- `CW-D01` → `CW-D01.O1`: Uses Typed flow balance equations and executable examples to define, constrain or evaluate Finite-buffer and delay flow extension.
- `CW-D02` → `CW-D02.O1`: Uses Conditional throughput bounds to define, constrain or evaluate Finite-buffer and delay flow extension.

Source step `D03` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: D02.

Dependency revision: Replaces a phase-order chain with the explicit output prerequisites for this task; the original dependencies and acceptance text remain preserved. Final review/release gates are unchanged in scope.

## Model setup and rework (CW-D04)

**Proposal:** `CW-D04` · **Epic:** `CW-EP04` · **Russian:** Переналадка и качество

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-D04)

- `CW-D04.O1`: Setup, defect and rework flow extension. Intended path: `roadmap/coordinated-work/work-products/flow/setup-rework.md`. Future output, not yet claimed as created.

### Acceptance (CW-D04)

1. Номинальная и эффективная мощности раздельны; потери наблюдаемы.
2. Distinguish nominal capacity, effective service time, accepted quality and rework load.
3. Track setup sequence and returns through the routing graph.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-D04)

- fixtures, quality balances and capacity traces
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: Counting rejected output as accepted good output must be detected. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-D04)

- `CW-D01` → `CW-D01.O1`: Uses Typed flow balance equations and executable examples to define, constrain or evaluate Setup, defect and rework flow extension.
- `CW-C03` → `CW-C03.O1`: Uses Demand observation schema to define, constrain or evaluate Setup, defect and rework flow extension.

Source step `D04` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: D03.

Dependency revision: Setup/rework and buffer modeling are independent extensions of typed conservation.

## Compare release policies (CW-D05)

**Proposal:** `CW-D05` · **Epic:** `CW-EP04` · **Russian:** Правила допуска работы

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-D05)

- `CW-D05.O1`: Matched release-policy comparison. Intended path: `roadmap/coordinated-work/work-products/flow/release-policies.md`. Future output, not yet claimed as created.

### Acceptance (CW-D05)

1. CONWIP, простое pull-правило и оптимизатор сравниваются при равном спросе и ресурсах.
2. Compare documented CONWIP, simple pull and tuned optimization on identical scenarios and resources.
3. Report service, WIP, accepted output, delay, quality and total cost with tuning budgets.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-D05)

- policy implementations, frozen instances and paired results
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: Giving one policy future demand or extra tuning budget invalidates the matched comparison. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-D05)

- `CW-D06` → `CW-D06.O1`: Uses Product-mix and shared-resource flow model to define, constrain or evaluate Matched release-policy comparison.
- `CW-N17` → `CW-N17.O1`: Uses Independent oracle and negative-control suite to define, constrain or evaluate Matched release-policy comparison.

Source step `D05` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: D04.

Dependency revision: Policy comparison needs the shared-resource/buffer/setup model and independent oracle; mere sequential completion of setup modeling is insufficient.

## Add product mix and shared resources (CW-D06)

**Proposal:** `CW-D06` · **Epic:** `CW-EP04` · **Russian:** Несколько продуктов и общие ресурсы

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-D06)

- `CW-D06.O1`: Product-mix and shared-resource flow model. Intended path: `roadmap/coordinated-work/work-products/flow/product-mix.md`. Future output, not yet claimed as created.

### Acceptance (CW-D06)

1. Невозможна двойная резервация общих мощностей; фиксируются несовместимые маршруты.
2. Represent alternative routes, setup compatibility and renewable/shared resources.
3. Validate feasible schedules against an independent resource checker.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-D06)

- scenario schemas, reservation traces and feasibility receipts
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: Two products cannot simultaneously reserve the same exclusive capacity. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-D06)

- `CW-D03` → `CW-D03.O1`: Uses Finite-buffer and delay flow extension to define, constrain or evaluate Product-mix and shared-resource flow model.
- `CW-D04` → `CW-D04.O1`: Uses Setup, defect and rework flow extension to define, constrain or evaluate Product-mix and shared-resource flow model.
- `CW-C04` → `CW-C04.O1`: Uses Availability, commitments and mentoring calendar to define, constrain or evaluate Product-mix and shared-resource flow model.

Source step `D06` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: D05.

Dependency revision: Product mix depends on buffer/setup extensions and actual resource calendars before policy comparison.

## Construct local-metric counterexamples (CW-D07)

**Proposal:** `CW-D07` · **Epic:** `CW-EP04` · **Russian:** Контрпримеры локальным KPI

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-D07)

- `CW-D07.O1`: Local-metric failure catalogue. Intended path: `roadmap/coordinated-work/work-products/flow/local-kpi-counterexamples.md`. Future output, not yet claimed as created.

### Acceptance (CW-D07)

1. Есть случаи, где локальное ускорение ухудшает WIP, качество или обслуживание.
2. Construct explicit cases where local speed harms global WIP, quality, service or workload.
3. Include cases where a local improvement is safe to avoid a universal anti-optimization claim.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-D07)

- scenario inputs, policy traces and global/local outcome comparisons
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: A detector that flags every local improvement must fail the safe case. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-D07)

- `CW-D05` → `CW-D05.O1`: Uses Matched release-policy comparison to define, constrain or evaluate Local-metric failure catalogue.
- `CW-B06` → `CW-B06.O1`: Uses Outcome and constraint metric dictionary to define, constrain or evaluate Local-metric failure catalogue.

Source step `D07` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: D06.

Dependency revision: Replaces a phase-order chain with the explicit output prerequisites for this task; the original dependencies and acceptance text remain preserved. Final review/release gates are unchanged in scope.

## Review the flow model (CW-D08)

**Proposal:** `CW-D08` · **Epic:** `CW-EP04` · **Russian:** Рецензия модели потока

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-D08)

- `CW-D08.O1`: Flow-model applicability and review dossier. Intended path: `roadmap/coordinated-work/work-products/flow/review.md`. Future output, not yet claimed as created.

### Acceptance (CW-D08)

1. Перечислены доказуемые свойства, контрпримеры и реальные данные, которых пока не хватает.
2. List established identities, conditional bounds, finite tests and unsupported real-system assumptions separately.
3. Review model validity and missing empirical inputs against intended process families.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-D08)

- versioned model, limitations and substantive review
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: Passing code tests alone cannot establish that the model represents an actual organization. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-D08)

- `CW-D07` → `CW-D07.O1`: Uses Local-metric failure catalogue to define, constrain or evaluate Flow-model applicability and review dossier.
- `CW-A08` → `CW-A08.O1`: Uses Reproducible scoping review dossier to define, constrain or evaluate Flow-model applicability and review dossier.
- `CW-C08` → `CW-C08.O1`: Uses Reviewed KC organization profile to define, constrain or evaluate Flow-model applicability and review dossier.

Source step `D08` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: D07.

Dependency revision: Final flow review still consumes the reviewed scientific map and organization profile; earlier drafting did not claim validated applicability.

## Estimate task workload (CW-E01)

**Proposal:** `CW-E01` · **Epic:** `CW-EP05` · **Russian:** Трудоемкость по задачам

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-E01)

- `CW-E01.O1`: Contextual task-workload estimator. Intended path: `roadmap/coordinated-work/work-products/people/workload.md`. Future output, not yet claimed as created.

### Acceptance (CW-E01)

1. Оценки условны по контексту, качеству и составу команды, с интервалами.
2. Condition estimates on task mix, quality, tools, team composition and environment.
3. Report prediction intervals and missing support rather than one universal hours value.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-E01)

- measurement protocol, data dictionary and calibration examples
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: A workload measured on an experienced team cannot transfer unchanged to a novice team. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-E01)

- `CW-B04` → `CW-B04.O1`: Uses Occupation, competency and role crosswalk to define, constrain or evaluate Contextual task-workload estimator.
- `CW-C03` → `CW-C03.O1`: Uses Demand observation schema to define, constrain or evaluate Contextual task-workload estimator.
- `CW-C04` → `CW-C04.O1`: Uses Availability, commitments and mentoring calendar to define, constrain or evaluate Contextual task-workload estimator.
- `CW-B06` → `CW-B06.O1`: Uses Outcome and constraint metric dictionary to define, constrain or evaluate Contextual task-workload estimator.

Source step `E01` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: B08, C08, D08.

Dependency revision: Workload estimation uses competency, demand, calendar and metric definitions; it need not wait for the full flow-model review.

## Bind competency evidence (CW-E02)

**Proposal:** `CW-E02` · **Epic:** `CW-EP05` · **Russian:** Проверка компетенций

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-E02)

- `CW-E02.O1`: Competency-evidence schema and fixtures. Intended path: `roadmap/coordinated-work/work-products/people/competency-evidence.md`. Future output, not yet claimed as created.

### Acceptance (CW-E02)

1. Название профессии не заменяет оценку способности и обязательный допуск.
2. Bind ability evidence to task, conditions, date, assessor and limits.
3. Keep mandatory credentials and current permissions as separate predicates.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-E02)

- schema and accepted/unknown/expired examples
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: An expired permission or unrelated assessment cannot satisfy current task eligibility. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-E02)

- `CW-B04` → `CW-B04.O1`: Uses Occupation, competency and role crosswalk to define, constrain or evaluate Competency-evidence schema and fixtures.

Source step `E02` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: E01.

Dependency revision: Competency evidence is a parallel foundation for workload/assignment studies, not dependent on estimated task hours.

## Optimize multiskill assignments (CW-E03)

**Proposal:** `CW-E03` · **Epic:** `CW-EP05` · **Russian:** Многоквалификационное расписание

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-E03)

- `CW-E03.O1`: Multiskill assignment solver and checker. Intended path: `roadmap/coordinated-work/work-products/people/assignment.md`. Future output, not yet claimed as created.

### Acceptance (CW-E03)

1. Одна и та же мощность не используется одновременно для разных требований.
2. Declare skill complementarity, team constraints, calendars and objective priorities.
3. Compare small cases with exhaustive feasible assignments before larger instances.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-E03)

- solver inputs, independent feasibility checks and objective receipts
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: Skill labels cannot double-count one person's simultaneous capacity. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-E03)

- `CW-E01` → `CW-E01.O1`: Uses Contextual task-workload estimator to define, constrain or evaluate Multiskill assignment solver and checker.
- `CW-E02` → `CW-E02.O1`: Uses Competency-evidence schema and fixtures to define, constrain or evaluate Multiskill assignment solver and checker.
- `CW-D06` → `CW-D06.O1`: Uses Product-mix and shared-resource flow model to define, constrain or evaluate Multiskill assignment solver and checker.

Source step `E03` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: E02.

Dependency revision: Assignment requires workload, capability evidence and shared-resource constraints; it cannot inherit capacity from labels.

## Model hiring lead times (CW-E04)

**Proposal:** `CW-E04` · **Epic:** `CW-EP05` · **Russian:** Найм и выход на мощность

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-E04)

- `CW-E04.O1`: Hiring and onboarding delay model. Intended path: `roadmap/coordinated-work/work-products/people/hiring.md`. Future output, not yet claimed as created.

### Acceptance (CW-E04)

1. Учтены срок поиска, onboarding, вероятность заполнения и часы наставника.
2. Represent search time, fill uncertainty, ramp-up and mentoring consumption.
3. Return a time-dependent net-capacity trajectory with assumptions.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-E04)

- scenario inputs and net-capacity curves
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: A new hire cannot contribute full capacity on the decision date or ignore mentor load. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-E04)

- `CW-E01` → `CW-E01.O1`: Uses Contextual task-workload estimator to define, constrain or evaluate Hiring and onboarding delay model.
- `CW-C04` → `CW-C04.O1`: Uses Availability, commitments and mentoring calendar to define, constrain or evaluate Hiring and onboarding delay model.

Source step `E04` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: E03.

Dependency revision: Hiring delay can be modeled from workload and calendar independently of completed assignment optimization.

## Compare capacity alternatives (CW-E05)

**Proposal:** `CW-E05` · **Epic:** `CW-EP05` · **Russian:** Альтернативы найму

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-E05)

- `CW-E05.O1`: Capacity-alternative decision study. Intended path: `roadmap/coordinated-work/work-products/people/alternatives.md`. Future output, not yet claimed as created.

### Acceptance (CW-E05)

1. Для найма, обучения, перераспределения, автоматизации и бездействия рассчитаны сопоставимые сценарии.
2. Evaluate hiring, training, reassignment, automation and no-action on common horizon and demand.
3. Include cash, delay, quality, uncertainty, mentor load and downstream bottlenecks.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-E05)

- alternative receipts and sensitivity analysis
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: A cheaper option cannot win solely by omitting its delayed benefit or support cost. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-E05)

- `CW-E03` → `CW-E03.O1`: Uses Multiskill assignment solver and checker to define, constrain or evaluate Capacity-alternative decision study.
- `CW-E04` → `CW-E04.O1`: Uses Hiring and onboarding delay model to define, constrain or evaluate Capacity-alternative decision study.
- `CW-F04` → `CW-F04.O1`: Uses Decision-lag dynamics model to define, constrain or evaluate Capacity-alternative decision study.
- `CW-N21` → `CW-N21.O1`: Uses Team interaction and learning-capacity model to define, constrain or evaluate Capacity-alternative decision study.

Source step `E05` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: E04.

Dependency revision: Comparable alternatives consume assignments, hiring trajectories, lag model and team dynamics.

## Constrain sustainable workload (CW-E07)

**Proposal:** `CW-E07` · **Epic:** `CW-EP05` · **Russian:** Условия устойчивой нагрузки

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-E07)

- `CW-E07.O1`: Sustainable workload constraint profile. Intended path: `roadmap/coordinated-work/work-products/people/sustainable-workload.md`. Future output, not yet claimed as created.

### Acceptance (CW-E07)

1. Явны рабочие часы, предпочтения, качество и границы допустимого решения.
2. Encode authorized working-time, availability, preferences, recovery assumptions and quality limits.
3. Surface infeasibility and conflicting priorities rather than silently dropping constraints.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-E07)

- constraint profile and infeasible/feasible schedules
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: An apparently productive schedule that exceeds declared workload bounds must be rejected. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-E07)

- `CW-C04` → `CW-C04.O1`: Uses Availability, commitments and mentoring calendar to define, constrain or evaluate Sustainable workload constraint profile.
- `CW-E03` → `CW-E03.O1`: Uses Multiskill assignment solver and checker to define, constrain or evaluate Sustainable workload constraint profile.

Source step `E07` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: E06.

Dependency revision: Workload constraints consume calendar and assignment semantics independently of causal-effect conclusions.

## Produce auditable role requirements (CW-E08)

**Proposal:** `CW-E08` · **Epic:** `CW-EP05` · **Russian:** Профиль потребности в роли

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-E08)

- `CW-E08.O1`: Auditable role and capacity recommendation. Intended path: `roadmap/coordinated-work/work-products/people/role-requirements.md`. Future output, not yet claimed as created.

### Acceptance (CW-E08)

1. Рекомендация содержит роль, количество, место, время, предпосылки, альтернативы и опровержение.
2. Return role/capability, count or capacity, place, time, rationale and alternatives.
3. Expose key assumptions, uncertainty, authority and conditions that reverse the recommendation.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-E08)

- structured recommendation and counterfactual scenarios
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: A workload gap alone cannot produce an unconditional fixed headcount. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-E08)

- `CW-E05` → `CW-E05.O1`: Uses Capacity-alternative decision study to define, constrain or evaluate Auditable role and capacity recommendation.
- `CW-E06` → `CW-E06.O1`: Uses Performance-versus-causation protocol to define, constrain or evaluate Auditable role and capacity recommendation.
- `CW-E07` → `CW-E07.O1`: Uses Sustainable workload constraint profile to define, constrain or evaluate Auditable role and capacity recommendation.
- `CW-A08` → `CW-A08.O1`: Uses Reproducible scoping review dossier to define, constrain or evaluate Auditable role and capacity recommendation.
- `CW-C08` → `CW-C08.O1`: Uses Reviewed KC organization profile to define, constrain or evaluate Auditable role and capacity recommendation.

Source step `E08` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: E07.

Dependency revision: Final auditable role requirements still consume alternatives, causal/workload boundaries and reviewed source/profile evidence.

## Model team complementarity and capability change (CW-N21)

**Proposal:** `CW-N21` · **Epic:** `CW-EP05` · **Russian:** Моделировать взаимодополнение команды, наставничество и обучение

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-N21)

- `CW-N21.O1`: Team interaction and learning-capacity model. Intended path: `roadmap/coordinated-work/work-products/people/team-dynamics.md`. Future output, not yet claimed as created.

### Acceptance (CW-N21)

1. Capacity is not assumed additive; mentoring consumes current capacity; credentials, task-specific ability and current permission stay distinct.
2. Model complementarity, skill bottlenecks, mentoring load, ramp-up, decay and support work explicitly.
3. Separate competence evidence from permission and inspect heterogeneous workload/quality impacts.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-N21)

- equations, measured/assumed parameters and nonadditive examples
- Exact versions, observed outcome, scope and unresolved limits.
- Adverse case: Summing isolated worker capacities must fail a case with required complementary skills or a shared mentor. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-N21)

- `CW-E01` → `CW-E01.O1`: Uses Contextual task-workload estimator to define, constrain or evaluate Team interaction and learning-capacity model.
- `CW-E02` → `CW-E02.O1`: Uses Competency-evidence schema and fixtures to define, constrain or evaluate Team interaction and learning-capacity model.
- `CW-C04` → `CW-C04.O1`: Uses Availability, commitments and mentoring calendar to define, constrain or evaluate Team interaction and learning-capacity model.

## Reconcile hierarchical forecasts (CW-F01)

**Proposal:** `CW-F01` · **Epic:** `CW-EP06` · **Russian:** Согласование иерархических прогнозов

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-F01)

- `CW-F01.O1`: Hierarchical forecast reconciliation study. Intended path: `roadmap/coordinated-work/work-products/forecast/reconciliation.md`. Future output, not yet claimed as created.

### Acceptance (CW-F01)

1. Прогнозы отделов согласованы с агрегатами; когерентность не названа точностью.
2. Preserve hierarchy identities and compare bottom-up/top-down or justified reconciliation methods.
3. Report coherence separately from accuracy at each aggregation level.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-F01)

- forecast origins, hierarchy and paired scoring outputs
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: Perfectly coherent but inaccurate forecasts must not be classified accurate. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-F01)

- `CW-C03` → `CW-C03.O1`: Uses Demand observation schema to define, constrain or evaluate Hierarchical forecast reconciliation study.

Source step `F01` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: C08.

Dependency revision: Forecast work uses demand observations and can start before a complete profile review.

## Calibrate predictive uncertainty (CW-F02)

**Proposal:** `CW-F02` · **Epic:** `CW-EP06` · **Russian:** Вероятностные интервалы

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-F02)

- `CW-F02.O1`: Predictive uncertainty calibration study. Intended path: `roadmap/coordinated-work/work-products/forecast/calibration.md`. Future output, not yet claimed as created.

### Acceptance (CW-F02)

1. Оценены coverage, proper score и ошибка по типам задач.
2. Evaluate coverage and proper scores by task type, horizon and regime.
3. Freeze training/calibration/test periods and include difficult subgroups.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-F02)

- prediction sets/distributions, scoring protocol and results
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: Unjustifiably wide intervals cannot pass solely through high empirical coverage. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-F02)

- `CW-F01` → `CW-F01.O1`: Uses Hierarchical forecast reconciliation study to define, constrain or evaluate Predictive uncertainty calibration study.

Source step `F02` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: F01.

Dependency revision: Replaces a phase-order chain with the explicit output prerequisites for this task; the original dependencies and acceptance text remain preserved. Final review/release gates are unchanged in scope.

## Define external shock scenarios (CW-F03)

**Proposal:** `CW-F03` · **Epic:** `CW-EP06` · **Russian:** Рыночные и политические сценарии

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-F03)

- `CW-F03.O1`: Dated external-shock scenario register. Intended path: `roadmap/coordinated-work/work-products/forecast/shocks.md`. Future output, not yet claimed as created.

### Acceptance (CW-F03)

1. Сценарий отличим от прогноза; источники, даты и область влияния указаны.
2. Bind scenario assumptions to sources, timing and affected graph components.
3. Distinguish forecast probability, stress scenario and unknown likelihood.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-F03)

- scenario register and dependency impact traces
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: An invented scenario likelihood cannot become a calibrated probability. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-F03)

- `CW-A02` → `CW-A02.O1`: Uses Seed bibliography verification ledger to define, constrain or evaluate Dated external-shock scenario register.
- `CW-C01` → `CW-C01.O1`: Uses Typed organizational work graph schema to define, constrain or evaluate Dated external-shock scenario register.

Source step `F03` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: F02.

Dependency revision: Scenario identification uses sources and topology; it need not await forecast calibration and remains scenario evidence.

## Model decision delays (CW-F04)

**Proposal:** `CW-F04` · **Epic:** `CW-EP06` · **Russian:** Задержки наблюдения и действий

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-F04)

- `CW-F04.O1`: Decision-lag dynamics model. Intended path: `roadmap/coordinated-work/work-products/forecast/lags.md`. Future output, not yet claimed as created.

### Acceptance (CW-F04)

1. Учитываются freshness, закупка, найм, обучение и реакция спроса.
2. Represent observation freshness, procurement, hiring, training and demand-response delays.
3. Test short/long horizons and delayed feedback explicitly.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-F04)

- lag parameters, traces and sensitivity results
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: A policy using stale observations as current must fail the stale-input case. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-F04)

- `CW-C02` → `CW-C02.O1`: Uses Versioned event and replay schema to define, constrain or evaluate Decision-lag dynamics model.
- `CW-C04` → `CW-C04.O1`: Uses Availability, commitments and mentoring calendar to define, constrain or evaluate Decision-lag dynamics model.

Source step `F04` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: F03.

Dependency revision: Lag modeling uses event/calendar semantics and can run alongside forecast calibration.

## Optimize under uncertainty (CW-F05)

**Proposal:** `CW-F05` · **Epic:** `CW-EP06` · **Russian:** Выбор при неполном знании

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-F05)

- `CW-F05.O1`: Robust/risk-aware decision comparison. Intended path: `roadmap/coordinated-work/work-products/forecast/risk-aware-choice.md`. Future output, not yet claimed as created.

### Acceptance (CW-F05)

1. Указан допустимый риск и цена консервативности; вероятности не выдуманы.
2. Declare uncertainty set or justified distribution, risk tolerance and conservatism cost.
3. Compare deterministic, robust and stochastic options where their assumptions apply.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-F05)

- decision instances, risk/feasibility receipts and regret/cost analysis
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: Unknown probabilities cannot be filled in as if measured. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-F05)

- `CW-F02` → `CW-F02.O1`: Uses Predictive uncertainty calibration study to define, constrain or evaluate Robust/risk-aware decision comparison.
- `CW-F03` → `CW-F03.O1`: Uses Dated external-shock scenario register to define, constrain or evaluate Robust/risk-aware decision comparison.
- `CW-F04` → `CW-F04.O1`: Uses Decision-lag dynamics model to define, constrain or evaluate Robust/risk-aware decision comparison.

Source step `F05` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: F04.

Dependency revision: Replaces a phase-order chain with the explicit output prerequisites for this task; the original dependencies and acceptance text remain preserved. Final review/release gates are unchanged in scope.

## Detect distribution shift (CW-F07)

**Proposal:** `CW-F07` · **Epic:** `CW-EP06` · **Russian:** Дрейф и смена режима

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-F07)

- `CW-F07.O1`: Distribution-shift monitoring and fallback. Intended path: `roadmap/coordinated-work/work-products/forecast/drift.md`. Future output, not yet claimed as created.

### Acceptance (CW-F07)

1. Есть измеримый триггер пересмотра, окно наблюдений и fallback.
2. Define the monitored quantity, threshold, observation window and action on alert.
3. Measure false alerts and missed shifts on named regimes.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-F07)

- drift fixtures, monitoring receipts and fallback decisions
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: A detector with permanent alarms cannot pass without accounting for false-alert cost. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-F07)

- `CW-C06` → `CW-C06.O1`: Uses Dependency invalidation and freshness rules to define, constrain or evaluate Distribution-shift monitoring and fallback.
- `CW-F02` → `CW-F02.O1`: Uses Predictive uncertainty calibration study to define, constrain or evaluate Distribution-shift monitoring and fallback.
- `CW-F06` → `CW-F06.O1`: Uses Censoring, endogeneity and feedback audit to define, constrain or evaluate Distribution-shift monitoring and fallback.

Source step `F07` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: F06.

Dependency revision: Replaces a phase-order chain with the explicit output prerequisites for this task; the original dependencies and acceptance text remain preserved. Final review/release gates are unchanged in scope.

## Backtest frozen forecast decisions (CW-F08)

**Proposal:** `CW-F08` · **Epic:** `CW-EP06` · **Russian:** Проверка на отложенных периодах

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-F08)

- `CW-F08.O1`: Time-respecting decision backtest. Intended path: `roadmap/coordinated-work/work-products/forecast/backtest.md`. Future output, not yet claimed as created.

### Acceptance (CW-F08)

1. В каждом времени доступны только реально доступные тогда данные, без утечки будущего.
2. Reconstruct each forecast origin with only then-available data and revisions.
3. Separate train/tune/test periods and evaluate downstream decisions as well as forecast scores.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-F08)

- as-of snapshots, code versions and origin-level receipts
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: Future revisions or labels injected into an earlier origin must be detected as leakage. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-F08)

- `CW-F05` → `CW-F05.O1`: Uses Robust/risk-aware decision comparison to define, constrain or evaluate Time-respecting decision backtest.
- `CW-F06` → `CW-F06.O1`: Uses Censoring, endogeneity and feedback audit to define, constrain or evaluate Time-respecting decision backtest.
- `CW-F07` → `CW-F07.O1`: Uses Distribution-shift monitoring and fallback to define, constrain or evaluate Time-respecting decision backtest.

Source step `F08` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: F07.

Dependency revision: Replaces a phase-order chain with the explicit output prerequisites for this task; the original dependencies and acceptance text remain preserved. Final review/release gates are unchanged in scope.

## Define decision prerequisites (CW-G01)

**Proposal:** `CW-G01` · **Epic:** `CW-EP07` · **Russian:** Набор знаний для решения

Proposed accountable: **Agent-Brain**; executor: **Agent-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-G01)

- `CW-G01.O1`: Decision prerequisite contracts. Intended path: `roadmap/coordinated-work/work-products/agent/prerequisites.md`. Future output, not yet claimed as created.

### Acceptance (CW-G01)

1. Для каждого решения заданы обязательные и необязательные артефакты.
2. List mandatory and optional artifacts, freshness, authority and resource preconditions per action.
3. Expose exact missing requirements and allowed degraded modes.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-G01)

- contract schemas and action-specific fixtures
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: An optional document cannot satisfy a missing mandatory safety/authority prerequisite. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-G01)

- `CW-C01` → `CW-C01.O1`: Uses Typed organizational work graph schema to define, constrain or evaluate Decision prerequisite contracts.
- `CW-B02` → `CW-B02.O1`: Uses Needs and situations taxonomy to define, constrain or evaluate Decision prerequisite contracts.
- `CW-B04` → `CW-B04.O1`: Uses Occupation, competency and role crosswalk to define, constrain or evaluate Decision prerequisite contracts.
- `CW-B05` → `CW-B05.O1`: Uses Resource ontology and accounting laws to define, constrain or evaluate Decision prerequisite contracts.
- `CW-B06` → `CW-B06.O1`: Uses Outcome and constraint metric dictionary to define, constrain or evaluate Decision prerequisite contracts.
- `CW-N11` → `CW-N11.O1`: Uses Organizational objectives and obligations profile to define, constrain or evaluate Decision prerequisite contracts.

Source step `G01` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: C08, D08, E08, F08.

Dependency revision: Prerequisite contracts can be drafted from explicit goal/resource/capability/metric semantics; runtime evaluation waits for model/flow/people review.

## Assemble bounded context (CW-G02)

**Proposal:** `CW-G02` · **Epic:** `CW-EP07` · **Russian:** Сборка контекста

Proposed accountable: **Agent-Brain**; executor: **Agent-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-G02)

- `CW-G02.O1`: Bounded context assembly study. Intended path: `roadmap/coordinated-work/work-products/agent/context-assembly.md`. Future output, not yet claimed as created.

### Acceptance (CW-G02)

1. Доставлены обязательные зависимости либо зарегистрирован конкретный дефицит.
2. Trace selected context to required dependencies and source versions under a stated budget.
3. Compare structured selection with size-matched retrieval and record omissions.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-G02)

- context manifests, token/resource budgets and dependency coverage
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: Adding irrelevant context cannot compensate for a missing mandatory dependency. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-G02)

- `CW-G01` → `CW-G01.O1`: Uses Decision prerequisite contracts to define, constrain or evaluate Bounded context assembly study.
- `CW-C05` → `CW-C05.O1`: Uses Evidence conflict-preserving store profile to define, constrain or evaluate Bounded context assembly study.
- `CW-C06` → `CW-C06.O1`: Uses Dependency invalidation and freshness rules to define, constrain or evaluate Bounded context assembly study.

Source step `G02` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: G01.

Dependency revision: Replaces a phase-order chain with the explicit output prerequisites for this task; the original dependencies and acceptance text remain preserved. Final review/release gates are unchanged in scope.

## Define startup readiness (CW-G03)

**Proposal:** `CW-G03` · **Epic:** `CW-EP07` · **Russian:** Режимы запуска

Proposed accountable: **Agent-Brain**; executor: **Agent-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-G03)

- `CW-G03.O1`: Mode-specific startup readiness checker. Intended path: `roadmap/coordinated-work/work-products/agent/readiness.md`. Future output, not yet claimed as created.

### Acceptance (CW-G03)

1. Различены наблюдение, моделирование, рекомендация и действие с текущими полномочиями.
2. Represent observe, model, recommend and execute as different admissible modes.
3. Bind readiness to current authority, data and environment and record denial reasons.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-G03)

- readiness rules and transition fixtures
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: Read-only model readiness must not authorize a real operational action. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-G03)

- `CW-G01` → `CW-G01.O1`: Uses Decision prerequisite contracts to define, constrain or evaluate Mode-specific startup readiness checker.

Source step `G03` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: G02.

Dependency revision: Mode readiness derives from prerequisites and can be specified independently of context optimization.

## Separate proposal and verification (CW-G04)

**Proposal:** `CW-G04` · **Epic:** `CW-EP07` · **Russian:** Предложения и внешняя проверка

Proposed accountable: **Agent-Brain**; executor: **Agent-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-G04)

- `CW-G04.O1`: Independent proposal verifier interface. Intended path: `roadmap/coordinated-work/work-products/agent/verifier.md`. Future output, not yet claimed as created.

### Acceptance (CW-G04)

1. Ограничения проверяет независимый детерминированный механизм, а не только prompt.
2. Use an independently implemented deterministic checker for declared constraints.
3. Report checker coverage and failures separately from agent answer quality.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-G04)

- checker version, constraints, mutation suite and verified proposals
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: A persuasive prompt response violating a hard resource constraint must be rejected. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-G04)

- `CW-G01` → `CW-G01.O1`: Uses Decision prerequisite contracts to define, constrain or evaluate Independent proposal verifier interface.
- `CW-N12` → `CW-N12.O1`: Uses Conditional admissibility definitions and proof obligations to define, constrain or evaluate Independent proposal verifier interface.

Source step `G04` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: G03.

Dependency revision: Verification requires prerequisite/formal-admissibility contracts, not a finished context assembly experiment.

## Calibrate abstention (CW-G05)

**Proposal:** `CW-G05` · **Epic:** `CW-EP07` · **Russian:** Уточнение и отказ от вывода

Proposed accountable: **Agent-Brain**; executor: **Agent-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-G05)

- `CW-G05.O1`: Clarification and abstention policy study. Intended path: `roadmap/coordinated-work/work-products/agent/clarification.md`. Future output, not yet claimed as created.

### Acceptance (CW-G05)

1. Стоимость дополнительного наблюдения сопоставляется с ценой ошибки и задержки.
2. Compare cost of observation, delay and wrong action with explicit assumptions.
3. Measure necessary refusals, false refusals, unnecessary questions and harmful execution.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-G05)

- registered scenarios and decision/cost receipts
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: Always refusing cannot pass as an optimal policy when safe useful actions exist. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-G05)

- `CW-G02` → `CW-G02.O1`: Uses Bounded context assembly study to define, constrain or evaluate Clarification and abstention policy study.
- `CW-F02` → `CW-F02.O1`: Uses Predictive uncertainty calibration study to define, constrain or evaluate Clarification and abstention policy study.

Source step `G05` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: G04.

Dependency revision: Clarification policy uses context gaps and calibrated uncertainty; verifier completion is not its conceptual prerequisite.

## Record decision evidence (CW-G06)

**Proposal:** `CW-G06` · **Epic:** `CW-EP07` · **Russian:** Квитанция решения

Proposed accountable: **Agent-Brain**; executor: **Agent-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-G06)

- `CW-G06.O1`: Decision-evidence receipt schema. Intended path: `roadmap/coordinated-work/work-products/agent/decision-receipt.md`. Future output, not yet claimed as created.

### Acceptance (CW-G06)

1. Связаны версия модели, исходные данные, альтернативы, бюджет, права и ожидаемый эффект.
2. Bind input/model versions, alternatives, budget, authority, predicted consequences and attempt IDs.
3. Keep recommendation, execution and observed outcome as separate lifecycle records.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-G06)

- receipt schema and replayable examples
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: A successful recommendation test cannot be converted into a receipt of real execution. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-G06)

- `CW-G02` → `CW-G02.O1`: Uses Bounded context assembly study to define, constrain or evaluate Decision-evidence receipt schema.
- `CW-G03` → `CW-G03.O1`: Uses Mode-specific startup readiness checker to define, constrain or evaluate Decision-evidence receipt schema.
- `CW-G04` → `CW-G04.O1`: Uses Independent proposal verifier interface to define, constrain or evaluate Decision-evidence receipt schema.

Source step `G06` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: G05.

Dependency revision: Decision receipts integrate context, readiness and verifier contracts before concurrency or use.

## Handle concurrent decisions (CW-G07)

**Proposal:** `CW-G07` · **Epic:** `CW-EP07` · **Russian:** Конфликт и повторное выполнение

Proposed accountable: **Agent-Brain**; executor: **Agent-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-G07)

- `CW-G07.O1`: Concurrent decision state machine. Intended path: `roadmap/coordinated-work/work-products/agent/concurrency.md`. Future output, not yet claimed as created.

### Acceptance (CW-G07)

1. Резервирование ресурсов и идемпотентность исключают двойное выполнение.
2. Declare atomicity boundary, idempotency key, resource reservation and cancellation semantics.
3. Handle conflicting simultaneous proposals and retries under a stated failure model.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-G07)

- state machine, adversarial schedules and effect receipts
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: Two individually feasible decisions that jointly oversubscribe capacity must not both commit. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-G07)

- `CW-G06` → `CW-G06.O1`: Uses Decision-evidence receipt schema to define, constrain or evaluate Concurrent decision state machine.
- `CW-C04` → `CW-C04.O1`: Uses Availability, commitments and mentoring calendar to define, constrain or evaluate Concurrent decision state machine.

Source step `G07` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: G06.

Dependency revision: Replaces a phase-order chain with the explicit output prerequisites for this task; the original dependencies and acceptance text remain preserved. Final review/release gates are unchanged in scope.

## Review learning updates (CW-G08)

**Proposal:** `CW-G08` · **Epic:** `CW-EP07` · **Russian:** Возврат знаний в базу

Proposed accountable: **Agent-Brain**; executor: **Agent-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-G08)

- `CW-G08.O1`: Learning-update review contract. Intended path: `roadmap/coordinated-work/work-products/agent/learning.md`. Future output, not yet claimed as created.

### Acceptance (CW-G08)

1. Наблюдение результата не становится принятой общей нормой без области и проверки.
2. Require scope, supporting evidence, contradiction handling and review before generalized reuse.
3. Connect observed outcomes to the exact attempted policy and environment.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-G08)

- update proposal, review decisions and invalidation examples
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: One successful run cannot silently become a general accepted policy. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-G08)

- `CW-G06` → `CW-G06.O1`: Uses Decision-evidence receipt schema to define, constrain or evaluate Learning-update review contract.
- `CW-C06` → `CW-C06.O1`: Uses Dependency invalidation and freshness rules to define, constrain or evaluate Learning-update review contract.

Source step `G08` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: G07.

Dependency revision: Learning-review requirements use receipts and invalidation; completed concurrency code is not required to define them.

## Freeze hypotheses and metrics (CW-H01)

**Proposal:** `CW-H01` · **Epic:** `CW-EP08` · **Russian:** Регистрация гипотез и метрик

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-H01)

- `CW-H01.O1`: Per-study preregistration snapshots. Intended path: `roadmap/coordinated-work/work-products/evaluation/registration.md`. Future output, not yet claimed as created.

### Acceptance (CW-H01)

1. До основного опыта заданы первичные метрики, границы эффекта и правило опровержения.
2. Freeze primary outcome, meaningful effect, hypotheses, exclusions and stopping before confirmatory observations.
3. Record pilot/exploratory observations and every later amendment separately.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-H01)

- timestamped registrations and amendment log
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: A protocol written after outcomes are seen cannot be called preregistered for those outcomes. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-H01)

- `CW-N19` → `CW-N19.O1`: Uses Per-study design and comparison registration template to define, constrain or evaluate Per-study preregistration snapshots.

Source step `H01` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: G08.

Dependency revision: Registration must precede confirmatory runs. It is moved from post-runtime completion to the per-study design gate; prior exploratory observations are disclosed.

## Evaluate strong baselines (CW-H05)

**Proposal:** `CW-H05` · **Epic:** `CW-EP08` · **Russian:** Сильные сравнительные методы

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-H05)

- `CW-H05.O1`: Matched strong-baseline evaluation. Intended path: `roadmap/coordinated-work/work-products/evaluation/baselines.md`. Future output, not yet claimed as created.

### Acceptance (CW-H05)

1. Сопоставлены человек/правило, OR-метод, обычный RAG и KC при равных данных и бюджете.
2. Compare human/rule, tuned OR, LLM without retrieval, strong RAG and KC where applicable.
3. Match available information, permissions and total tuning/compute budget; justify inapplicable baselines.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-H05)

- baseline implementations, information/budget matrix and run-level outputs
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: A weaker baseline deprived of data available to KC invalidates the claimed incremental benefit. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-H05)

- `CW-H02` → `CW-H02.O1`: Uses Production benchmark family to define, constrain or evaluate Matched strong-baseline evaluation.
- `CW-H03` → `CW-H03.O1`: Uses Service benchmark family to define, constrain or evaluate Matched strong-baseline evaluation.
- `CW-H04` → `CW-H04.O1`: Uses Project and knowledge-work benchmark family to define, constrain or evaluate Matched strong-baseline evaluation.
- `CW-G04` → `CW-G04.O1`: Uses Independent proposal verifier interface to define, constrain or evaluate Matched strong-baseline evaluation.
- `CW-F08` → `CW-F08.O1`: Uses Time-respecting decision backtest to define, constrain or evaluate Matched strong-baseline evaluation.
- `CW-E08` → `CW-E08.O1`: Uses Auditable role and capacity recommendation to define, constrain or evaluate Matched strong-baseline evaluation.
- `CW-D08` → `CW-D08.O1`: Uses Flow-model applicability and review dossier to define, constrain or evaluate Matched strong-baseline evaluation.
- `CW-C08` → `CW-C08.O1`: Uses Reviewed KC organization profile to define, constrain or evaluate Matched strong-baseline evaluation.
- `CW-N18` → `CW-N18.O1`: Uses Three model-validity dossiers to define, constrain or evaluate Matched strong-baseline evaluation.
- `CW-N20` → `CW-N20.O1`: Uses Statistical and causal analysis plan to define, constrain or evaluate Matched strong-baseline evaluation.

Source step `H05` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: H04.

Dependency revision: The comparative run requires all three family generators, reviewed models/profile, registered analysis and validity dossiers; family construction is parallel, inference is gated.

## Run ablations and uncertainty analysis (CW-H06)

**Proposal:** `CW-H06` · **Epic:** `CW-EP08` · **Russian:** Абляции и статистический анализ

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-H06)

- `CW-H06.O1`: Mechanism ablations and uncertainty report. Intended path: `roadmap/coordinated-work/work-products/evaluation/ablations.md`. Future output, not yet claimed as created.

### Acceptance (CW-H06)

1. Изъятие механизмов отделено от объема контекста; интервалы учитывают зависимость наблюдений.
2. Ablate dependencies, freshness, uncertainty, competency evidence and verifier with interactions assessed.
3. Use paired/cluster-aware uncertainty, failures/timeouts in denominators and fixed primary analysis.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-H06)

- registered analysis, raw runs, intervals and negative findings
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: Treating all simulation periods as independent organizations must fail the analysis check. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-H06)

- `CW-H05` → `CW-H05.O1`: Uses Matched strong-baseline evaluation to define, constrain or evaluate Mechanism ablations and uncertainty report.
- `CW-G08` → `CW-G08.O1`: Uses Learning-update review contract to define, constrain or evaluate Mechanism ablations and uncertainty report.

Source step `H06` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: H05.

Dependency revision: Ablation runs consume matched baseline outputs and learning-review boundaries.

## Register study protocols and matched baselines (CW-N19)

**Proposal:** `CW-N19` · **Epic:** `CW-EP08` · **Russian:** Подготовить протокол регистрации каждого сравнения

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-N19)

- `CW-N19.O1`: Per-study design and comparison registration template. Intended path: `roadmap/coordinated-work/work-products/evaluation/design.md`. Future output, not yet claimed as created.

### Acceptance (CW-N19)

1. Includes human/rule, tuned OR, no-retrieval LLM, strong RAG and KC where applicable; scope changes after observation are recorded.
2. Specify hypothesis, meaningful outcome, baselines, matched information/permissions/budget, stopping and exclusions before confirmation.
3. Include human/rule, tuned OR, no-retrieval LLM, strong RAG and KC when applicable with justified exceptions.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-N19)

- versioned study protocols, baseline matrix and amendments
- Exact versions, observed outcome, scope and unresolved limits.
- Adverse case: Observing results before choosing the primary outcome invalidates a confirmatory preregistration claim. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-N19)

- `CW-A07` → `CW-A07.O1`: Uses Scoped claim and counterclaim ledger to define, constrain or evaluate Per-study design and comparison registration template.
- `CW-B06` → `CW-B06.O1`: Uses Outcome and constraint metric dictionary to define, constrain or evaluate Per-study design and comparison registration template.
- `CW-N09` → `CW-N09.O1`: Uses Early discriminating prior-art matrix to define, constrain or evaluate Per-study design and comparison registration template.
- `CW-N11` → `CW-N11.O1`: Uses Organizational objectives and obligations profile to define, constrain or evaluate Per-study design and comparison registration template.

## Plan statistical units, power and multiplicity (CW-N20)

**Proposal:** `CW-N20` · **Epic:** `CW-EP08` · **Russian:** Установить единицы анализа, неопределенность и статистический план

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-N20)

- `CW-N20.O1`: Statistical and causal analysis plan. Intended path: `roadmap/coordinated-work/work-products/evaluation/analysis.md`. Future output, not yet claimed as created.

### Acceptance (CW-N20)

1. Periods/runs are not independent organizations; failures/timeouts remain in denominators; exploratory and confirmatory results are separated.
2. Define organization/cluster/trajectory units, dependence, power or precision, multiplicity and meaningful effect thresholds.
3. Retain timeouts/failures, uncertainty and negative outcomes; define adaptive-monitoring/amendment rules.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-N20)

- analysis scripts, simulated design checks and registered estimands
- Exact versions, observed outcome, scope and unresolved limits.
- Adverse case: Treating periods as independent organizations or excluding failed runs post hoc must be detected. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-N20)

- `CW-N19` → `CW-N19.O1`: Uses Per-study design and comparison registration template to define, constrain or evaluate Statistical and causal analysis plan.
- `CW-N16` → `CW-N16.O1`: Uses Versioned benchmark and eligible observed data packages to define, constrain or evaluate Statistical and causal analysis plan.

## Reassess novelty (CW-I01)

**Proposal:** `CW-I01` · **Epic:** `CW-EP09` · **Russian:** Аудит научной новизны

Proposed accountable: **KC-Brain**; executor: **KC-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-I01)

- `CW-I01.O1`: Contribution and prior-art reassessment. Intended path: `roadmap/coordinated-work/work-products/publication/novelty.md`. Future output, not yet claimed as created.

### Acceptance (CW-I01)

1. Для каждого вклада указано ближайшее prior art и измеримое отличие.
2. For each paper/spec state nearest competing work, supplied capability and measurable difference.
3. Update the novelty claim after full-text appraisal and after results, allowing no-novelty outcomes.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-I01)

- comparison matrix and claim changes
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: A new label or dependency diagram alone cannot establish a new scientific theory. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-I01)

- `CW-A08` → `CW-A08.O1`: Uses Reproducible scoping review dossier to define, constrain or evaluate Contribution and prior-art reassessment.
- `CW-B08` → `CW-B08.O1`: Uses Held-out-sector taxonomy evaluation to define, constrain or evaluate Contribution and prior-art reassessment.
- `CW-N09` → `CW-N09.O1`: Uses Early discriminating prior-art matrix to define, constrain or evaluate Contribution and prior-art reassessment.

Source step `I01` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: A08, B08, H08.

Dependency revision: Prior-art and novelty review must inform study design and manuscripts. Field results are required only for the claims that use them, not for every literature/formal contribution.

## Bind claims to evidence (CW-I02)

**Proposal:** `CW-I02` · **Epic:** `CW-EP09` · **Russian:** Матрица утверждений и свидетельств

Proposed accountable: **KC-Brain**; executor: **KC-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-I02)

- `CW-I02.O1`: Typed claim-to-evidence release matrix. Intended path: `roadmap/coordinated-work/work-products/publication/claim-evidence.md`. Future output, not yet claimed as created.

### Acceptance (CW-I02)

1. Теоремы, конечные тесты, эмпирика и предположения имеют разные типы свидетельств.
2. Distinguish theorem, finite test, simulation, retrospective, shadow and field evidence per claim.
3. Mark scope, contrary evidence, absent prerequisites and supported release language.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-I02)

- claim IDs and exact supporting receipts
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: CI success cannot license an empirical effectiveness or native-runtime-admission claim. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-I02)

- `CW-A07` → `CW-A07.O1`: Uses Scoped claim and counterclaim ledger to define, constrain or evaluate Typed claim-to-evidence release matrix.
- `CW-N10` → `CW-N10.O1`: Uses Evidence lineage and identity profile reusing KC to define, constrain or evaluate Typed claim-to-evidence release matrix.

Source step `I02` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: I01.

Dependency revision: Typed claim/evidence bindings are built from scoped claims and KC lineage before writing; they do not wait for field trials.

## Prepare canonical manuscripts (CW-I03)

**Proposal:** `CW-I03` · **Epic:** `CW-EP09` · **Russian:** Рукописи и спецификации

Proposed accountable: **KC-Brain**; executor: **KC-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-I03)

- `CW-I03.O1`: Canonical candidate manuscript/specification. Intended path: `roadmap/coordinated-work/work-products/publication/manuscripts.md`. Future output, not yet claimed as created.

### Acceptance (CW-I03)

1. Новый PAPER или SPECIFICATION существует до появления записи в каталоге.
2. Instantiate one content artifact per approved contribution with methods, limitations and citations.
3. Reconcile claims against its own evidence requirements before adding any catalogue entry.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-I03)

- versioned PAPER/SPECIFICATION source and claim matrix
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: An announcement card cannot be catalogued as an accepted completed paper. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-I03)

- `CW-I01` → `CW-I01.O1`: Uses Contribution and prior-art reassessment to define, constrain or evaluate Canonical candidate manuscript/specification.
- `CW-I02` → `CW-I02.O1`: Uses Typed claim-to-evidence release matrix to define, constrain or evaluate Canonical candidate manuscript/specification.
- `CW-N30` → `CW-N30.O1`: Uses Claim-specific artifact release contracts to define, constrain or evaluate Canonical candidate manuscript/specification.

Source step `I03` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: I02.

Dependency revision: Writing/release templates consume the novelty review, claim matrix and per-artifact release contract. Each output separately binds its evidential prerequisites.

## Freeze reproducibility packages (CW-I04)

**Proposal:** `CW-I04` · **Epic:** `CW-EP09` · **Russian:** Воспроизводимые пакеты

Proposed accountable: **KC-Brain**; executor: **KC-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-I04)

- `CW-I04.O1`: Frozen reproducibility package per artifact. Intended path: `roadmap/coordinated-work/work-products/publication/repro-packages.md`. Future output, not yet claimed as created.

### Acceptance (CW-I04)

1. Версии кода, данных, сред и результаты закреплены; отрицательные результаты сохранены.
2. Pin code, data, licenses/access conditions, environment, seeds, expected outputs and deviations.
3. Include negative results and instructions for restricted data reproduction where necessary.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-I04)

- immutable manifest and independent rerun receipt or documented blockage
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: A mutable branch URL alone cannot identify the reproduced experiment. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-I04)

- `CW-I03` → `CW-I03.O1`: Uses Canonical candidate manuscript/specification to define, constrain or evaluate Frozen reproducibility package per artifact.

Source step `I04` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: I03.

Dependency revision: Reproduction packages are instantiated per artifact, with all supporting code/data/analysis outputs as additional consumed evidence.

## Obtain substantive review (CW-I05)

**Proposal:** `CW-I05` · **Epic:** `CW-EP09` · **Russian:** Отдельная содержательная рецензия

Proposed accountable: **KC-Brain**; executor: **KC-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-I05)

- `CW-I05.O1`: Exact-version substantive review. Intended path: `roadmap/coordinated-work/work-products/publication/review.md`. Future output, not yet claimed as created.

### Acceptance (CW-I05)

1. Review указывает точный текст, критерии, пределы и выявленные ошибки.
2. Ask a separate appropriate reviewer to assess assumptions, methods, evidence and claims for the pinned artifact.
3. Track findings and whether each was fixed, rebutted with evidence or remains open.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-I05)

- review scope, version, criteria, findings and response
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: Editorial approval or parent-agent cross-check cannot be mislabelled independent scientific validation. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-I05)

- `CW-I04` → `CW-I04.O1`: Uses Frozen reproducibility package per artifact to define, constrain or evaluate Exact-version substantive review.
- `CW-N31` → `CW-N31.O1`: Uses Scientific trilingual terminology and fidelity suite to define, constrain or evaluate Exact-version substantive review.

Source step `I05` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: I04.

Dependency revision: Substantive review is per exact artifact/version, including its language obligations; one review does not clear every candidate paper.

## Integrate through repository gates (CW-I06)

**Proposal:** `CW-I06` · **Epic:** `CW-EP09` · **Russian:** Интеграция в репозиторий

Proposed accountable: **KC-Brain**; executor: **KC-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-I06)

- `CW-I06.O1`: Repository integration gates per artifact. Intended path: `roadmap/coordinated-work/work-products/publication/repository-release.md`. Future output, not yet claimed as created.

### Acceptance (CW-I06)

1. Выполнены требуемые CI и source checks; сохранены права и DCO.
2. Pass applicable source checks, CI, rights/DCO and branch/conflict reconciliation.
3. Read back accepted files at the integrated commit and retain run identifiers.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-I06)

- commit/file hashes, check results and integration receipt
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: A green run from a different head cannot satisfy the target artifact's gates. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-I06)

- `CW-I05` → `CW-I05.O1`: Uses Exact-version substantive review to define, constrain or evaluate Repository integration gates per artifact.

Source step `I06` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: I05.

Dependency revision: Replaces a phase-order chain with the explicit output prerequisites for this task; the original dependencies and acceptance text remain preserved. Final review/release gates are unchanged in scope.

## Publish and verify served content (CW-I07)

**Proposal:** `CW-I07` · **Epic:** `CW-EP09` · **Russian:** Публикация и чтение с сайта

Proposed accountable: **KC-Brain**; executor: **KC-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-I07)

- `CW-I07.O1`: Verified website publication per artifact. Intended path: `roadmap/coordinated-work/work-products/publication/served-release.md`. Future output, not yet claimed as created.

### Acceptance (CW-I07)

1. Сверена реально отданная сайтом версия; merge не подменяет deployment.
2. Bind deployed EN/RU/zh-Hans content to the accepted source and actual release.
3. Verify locale routing, links, feeds, sitemap and served scientific qualifications.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-I07)

- release manifest, HTTP/browser readbacks and translation checks
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: A merged repository change cannot by itself prove deployment or correct language delivery. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-I07)

- `CW-I06` → `CW-I06.O1`: Uses Repository integration gates per artifact to define, constrain or evaluate Verified website publication per artifact.

Source step `I07` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: I06.

Dependency revision: Replaces a phase-order chain with the explicit output prerequisites for this task; the original dependencies and acceptance text remain preserved. Final review/release gates are unchanged in scope.

## Admit indexing and maintain revisions (CW-I08)

**Proposal:** `CW-I08` · **Epic:** `CW-EP09` · **Russian:** Индексирование и пересмотр

Proposed accountable: **KC-Brain**; executor: **KC-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-I08)

- `CW-I08.O1`: Index admission and revision maintenance. Intended path: `roadmap/coordinated-work/work-products/publication/index-maintenance.md`. Future output, not yet claimed as created.

### Acceptance (CW-I08)

1. Принятие в индекс и полномочия исполнения отдельны; пересмотр сохраняет историю.
2. Admit only eligible artifact states; separate discoverability from execution authority.
3. Link later corrections, retractions and replacement versions without erasing history.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-I08)

- catalogue diff, admission record and revision graph
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: Index presence cannot imply scientific acceptance, native admission or authorized execution. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-I08)

- `CW-I07` → `CW-I07.O1`: Uses Verified website publication per artifact to define, constrain or evaluate Index admission and revision maintenance.

Source step `I08` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: I07.

Dependency revision: Replaces a phase-order chain with the explicit output prerequisites for this task; the original dependencies and acceptance text remain preserved. Final review/release gates are unchanged in scope.

## Define claim-specific publication release matrix (CW-N30)

**Proposal:** `CW-N30` · **Epic:** `CW-EP09` · **Russian:** Установить отдельные условия выпуска каждого научного артефакта

Proposed accountable: **KC-Brain**; executor: **KC-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-N30)

- `CW-N30.O1`: Claim-specific artifact release contracts. Intended path: `roadmap/coordinated-work/work-products/publication/release-contracts.md`. Future output, not yet claimed as created.

### Acceptance (CW-N30)

1. A review or formal paper can release at its appropriate evidence level; empirical benefit claims still require their study receipts; no universal H08 prerequisite.
2. For each proposed paper/spec list required evidence, scope, independent review and publication criteria. Defining this matrix does not itself satisfy any empirical preregistration or result gate.
3. Allow review/formal outputs at their justified level while retaining field gates for organizational-effect claims.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-N30)

- 16candidate release contracts and claim-to-study dependencies
- Exact versions, observed outcome, scope and unresolved limits.
- Adverse case: Removing universal H08 dependency must not allow a field-effect claim without its intervention evidence. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-N30)

- `CW-N02` → `CW-N02.O1`: Uses Programme charter and output inventory to define, constrain or evaluate Claim-specific artifact release contracts.
- `CW-N09` → `CW-N09.O1`: Uses Early discriminating prior-art matrix to define, constrain or evaluate Claim-specific artifact release contracts.

## Maintain trilingual terminology and fidelity (CW-N31)

**Proposal:** `CW-N31` · **Epic:** `CW-EP09` · **Russian:** Согласовать научную терминологию и переводы EN/RU/zh-Hans

Proposed accountable: **KC-Brain**; executor: **KC-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-N31)

- `CW-N31.O1`: Scientific trilingual terminology and fidelity suite. Intended path: `roadmap/coordinated-work/work-products/publication/translations.md`. Future output, not yet claimed as created.

### Acceptance (CW-N31)

1. Exact populations, uncertainty, competency/Skill/Role distinctions, author attribution and scientific qualifications are preserved.
2. Freeze EN/RU/zh-Hans terms for competency/Skill/Role, uncertainty, authority and evidence statuses.
3. Review attribution, units, populations, limitations and model-versus-world distinctions across versions.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-N31)

- glossary, aligned segments and linguistic/scientific review findings
- Exact versions, observed outcome, scope and unresolved limits.
- Adverse case: A translation that turns an upper bound into achieved throughput must fail. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-N31)

- `CW-B04` → `CW-B04.O1`: Uses Occupation, competency and role crosswalk to define, constrain or evaluate Scientific trilingual terminology and fidelity suite.
- `CW-N02` → `CW-N02.O1`: Uses Programme charter and output inventory to define, constrain or evaluate Scientific trilingual terminology and fidelity suite.

## Maintain revisions, negative findings and withdrawal (CW-N32)

**Proposal:** `CW-N32` · **Epic:** `CW-EP09` · **Russian:** Установить пересмотр, исправление и отзыв зависимых утверждений

Proposed accountable: **KC-Brain**; executor: **KC-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-N32)

- `CW-N32.O1`: Correction, withdrawal and invalidation maintenance. Intended path: `roadmap/coordinated-work/work-products/publication/maintenance.md`. Future output, not yet claimed as created.

### Acceptance (CW-N32)

1. Changed evidence invalidates dependent claims/decisions through explicit links; history and negative results retained; approved correction read back where served.
2. Link changed evidence to dependent claims, translations, catalogue entries and consumer decisions. Cover draft-stage corrections before catalogue indexing as well as later published revisions.
3. Publish versioned corrections/withdrawals through appropriate gates and read back served state.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-N32)

- revision graph, invalidation examples and correction/release receipts
- Exact versions, observed outcome, scope and unresolved limits.
- Adverse case: Deleting a prior result or stale page without a traceable correction cannot satisfy revision integrity. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-N32)

- `CW-G08` → `CW-G08.O1`: Uses Learning-update review contract to define, constrain or evaluate Correction, withdrawal and invalidation maintenance.
- `CW-N10` → `CW-N10.O1`: Uses Evidence lineage and identity profile reusing KC to define Correction, withdrawal and invalidation maintenance.

## Specify objectives, tradeoffs and infeasibility (CW-N11)

**Proposal:** `CW-N11` · **Epic:** `CW-EP10` · **Russian:** Определить цели, обязательства и компромиссы организации

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-N11)

- `CW-N11.O1`: Organizational objectives and obligations profile. Intended path: `roadmap/coordinated-work/work-products/foundations/objectives.md`. Future output, not yet claimed as created.

### Acceptance (CW-N11)

1. Global service/quality/workload tradeoffs are visible; aggregate gain cannot silently hide harmed constraints; infeasibility distinguishes conflicting evidence, resource shortage and authority shortage.
2. Represent hard obligations, competing objectives, service/quality/workload tradeoffs and priority rules.
3. Classify evidence inconsistency, uncertainty, missing authority and resource infeasibility separately.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-N11)

- objective schema, Pareto/tradeoff examples and infeasibility receipts
- Exact versions, observed outcome, scope and unresolved limits.
- Adverse case: Improved aggregate output cannot conceal violation of a binding quality or workload constraint. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-N11)

- `CW-B02` → `CW-B02.O1`: Uses Needs and situations taxonomy to define, constrain or evaluate Organizational objectives and obligations profile.
- `CW-B06` → `CW-B06.O1`: Uses Outcome and constraint metric dictionary to define, constrain or evaluate Organizational objectives and obligations profile.

## Discharge conditional admissibility obligations (CW-N12)

**Proposal:** `CW-N12` · **Epic:** `CW-EP10` · **Russian:** Уточнить условную допустимость решений и обязательства доказательства

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-N12)

- `CW-N12.O1`: Conditional admissibility definitions and proof obligations. Intended path: `roadmap/coordinated-work/work-products/foundations/admissibility.md`. Future output, not yet claimed as created.

### Acceptance (CW-N12)

1. Empty Omega, missing actual-state coverage, inconsistent constraints and empty action intersection are separated; one-step guarantees never upgraded to recursive feasibility.
2. Handle empty uncertainty set, actual-state coverage, contradictory observations and empty action intersection explicitly.
3. Prove only stated one-step results under explicit assumptions and give finite countermodels to overclaims.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-N12)

- definitions, derivations and machine-checkable finite cases
- Exact versions, observed outcome, scope and unresolved limits.
- Adverse case: Empty Omega must not cause vacuous universal acceptance; one-step validity cannot imply recursive feasibility. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-N12)

- `CW-B05` → `CW-B05.O1`: Uses Resource ontology and accounting laws to define, constrain or evaluate Conditional admissibility definitions and proof obligations.
- `CW-C01` → `CW-C01.O1`: Uses Typed organizational work graph schema to define, constrain or evaluate Conditional admissibility definitions and proof obligations.
- `CW-N11` → `CW-N11.O1`: Uses Organizational objectives and obligations profile to define, constrain or evaluate Conditional admissibility definitions and proof obligations.

## Implement dimensional and availability checks (CW-N14)

**Proposal:** `CW-N14` · **Epic:** `CW-EP10` · **Russian:** Проверять размерности, календари и типы ресурсов

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-N14)

- `CW-N14.O1`: Dimensional and resource-type verifier. Intended path: `roadmap/coordinated-work/work-products/foundations/resource-verifier.md`. Future output, not yet claimed as created.

### Acceptance (CW-N14)

1. Reject incompatible units, duplicated capacity and invalid substitutions; account separately for stocks, renewable capacity, non-rival information and authority.
2. Validate unit conversions, time intervals, replenishment rules, exclusivity and allowed substitution.
3. Keep stocks, renewable capacity, information and authority under distinct laws.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-N14)

- typed fixtures and positive/negative verifier receipts
- Exact versions, observed outcome, scope and unresolved limits.
- Adverse case: Adding person-hours to headcount or treating knowledge copying as inventory consumption must be rejected. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-N14)

- `CW-B05` → `CW-B05.O1`: Uses Resource ontology and accounting laws to define, constrain or evaluate Dimensional and resource-type verifier.

## Bind data access, rights and measurement purposes (CW-N15)

**Proposal:** `CW-N15` · **Epic:** `CW-EP11` · **Russian:** Установить права, приватность и допустимые способы работы с данными

Proposed accountable: **KC-Brain**; executor: **KC-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-N15)

- `CW-N15.O1`: Organizational/personnel data-use and access contract. Intended path: `roadmap/coordinated-work/work-products/data/rights-privacy.md`. Future output, not yet claimed as created.

### Acceptance (CW-N15)

1. Use of organizational/personnel data is authorized at the actual scope; synthetic/anonymized/access-restricted states explicit; unknown rights remain unknown.
2. Record dataset purpose, provenance, authority, privacy minimization, access, retention and permitted analyses.
3. Review whether task assignment/evaluation can produce unfair subgroup impacts; encode justified boundaries and review routes.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-N15)

- rights ledger, restricted-field schema and approved/synthetic data state
- Exact versions, observed outcome, scope and unresolved limits.
- Adverse case: Unknown data rights cannot become permission; sensitive employee attributes cannot leak into public reproducibility bundles. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-N15)

- `CW-N02` → `CW-N02.O1`: Uses Programme charter and output inventory to define, constrain or evaluate Organizational/personnel data-use and access contract.
- `CW-N10` → `CW-N10.O1`: Uses Evidence lineage and identity profile reusing KC to define, constrain or evaluate Organizational/personnel data-use and access contract.

## Build reference datasets and data dictionaries (CW-N16)

**Proposal:** `CW-N16` · **Epic:** `CW-EP11` · **Russian:** Подготовить версионируемые наборы данных и границы наблюдаемости

Proposed accountable: **KC-Brain**; executor: **KC-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-N16)

- `CW-N16.O1`: Versioned benchmark and eligible observed data packages. Intended path: `roadmap/coordinated-work/work-products/data/packages.md`. Future output, not yet claimed as created.

### Acceptance (CW-N16)

1. Record missingness, censoring, out-of-order events, task mix, leakage controls and train/tune/test separation; real-data availability never assumed.
2. Provide event/unit dictionaries, observation mechanisms, missingness, censoring, late events and task mix.
3. Separate train/tune/test, organizations and regimes; no real-data package is promised before access exists.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-N16)

- dataset manifest, split hashes, eligible access record and quality report
- Exact versions, observed outcome, scope and unresolved limits.
- Adverse case: Future observations, hidden labels and protected identity fields cannot cross declared split/publication boundaries. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-N16)

- `CW-C02` → `CW-C02.O1`: Uses Versioned event and replay schema to define, constrain or evaluate Versioned benchmark and eligible observed data packages.
- `CW-C03` → `CW-C03.O1`: Uses Demand observation schema to define, constrain or evaluate Versioned benchmark and eligible observed data packages.
- `CW-C04` → `CW-C04.O1`: Uses Availability, commitments and mentoring calendar to define, constrain or evaluate Versioned benchmark and eligible observed data packages.
- `CW-N15` → `CW-N15.O1`: Uses Organizational/personnel data-use and access contract to define, constrain or evaluate Versioned benchmark and eligible observed data packages.

## Create independent oracles and mutation controls (CW-N17)

**Proposal:** `CW-N17` · **Epic:** `CW-EP12` · **Russian:** Создать независимые оракулы и отрицательные контроли

Proposed accountable: **KC-Brain**; executor: **KC-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-N17)

- `CW-N17.O1`: Independent oracle and negative-control suite. Intended path: `roadmap/coordinated-work/work-products/validation/oracles.md`. Future output, not yet claimed as created.

### Acceptance (CW-N17)

1. Simulator and verifier do not share the same mistaken calculation; named mutants fail for intended reasons; revision1/2 probe evidence stays immutable.
2. Implement independent small-case enumerators/analytical checks separately from simulator or solver code.
3. Name each seeded defect and verify the control fails for the intended reason while positive cases pass.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-N17)

- oracle code, expected fixtures, mutant list and exact run receipts
- Exact versions, observed outcome, scope and unresolved limits.
- Adverse case: A copied faulty formula in simulator and checker cannot count as independent agreement. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-N17)

- `CW-N12` → `CW-N12.O1`: Uses Conditional admissibility definitions and proof obligations to define, constrain or evaluate Independent oracle and negative-control suite.
- `CW-D01` → `CW-D01.O1`: Uses Typed flow balance equations and executable examples to define, constrain or evaluate Independent oracle and negative-control suite.

## Validate conceptual and operational simulation models (CW-N18)

**Proposal:** `CW-N18` · **Epic:** `CW-EP12` · **Russian:** Проверить применимость трех семейств моделей

Proposed accountable: **KC-Brain**; executor: **KC-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-N18)

- `CW-N18.O1`: Three model-validity dossiers. Intended path: `roadmap/coordinated-work/work-products/validation/applicability.md`. Future output, not yet claimed as created.

### Acceptance (CW-N18)

1. Implementation correctness, parameter calibration and real-system validity reported separately; out-of-domain applicability is challenged.
2. Validate implementation, calibration and real-system applicability separately for production, service and project models.
3. Test structurally different demand/resource/feedback conditions and record failed fits or unsupported domains.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-N18)

- model assumptions, calibration splits, residual checks and boundary cases
- Exact versions, observed outcome, scope and unresolved limits.
- Adverse case: A simulator that passes implementation tests but misrepresents abandonment cannot validate a service organization. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-N18)

- `CW-N16` → `CW-N16.O1`: Uses Versioned benchmark and eligible observed data packages to define, constrain or evaluate Three model-validity dossiers.
- `CW-N17` → `CW-N17.O1`: Uses Independent oracle and negative-control suite to define, constrain or evaluate Three model-validity dossiers.
- `CW-D03` → `CW-D03.O1`: Uses Finite-buffer and delay flow extension to define, constrain or evaluate Three model-validity dossiers.
- `CW-E03` → `CW-E03.O1`: Uses Multiskill assignment solver and checker to define, constrain or evaluate Three model-validity dossiers.
- `CW-C01` → `CW-C01.O1`: Uses Typed organizational work graph schema to define, constrain or evaluate Three model-validity dossiers.
- `CW-H02` → `CW-H02.O1`: The family-specific validity dossier must evaluate the actual benchmark implementation and generator, rather than a description prepared before that implementation exists.
- `CW-H03` → `CW-H03.O1`: The family-specific validity dossier must evaluate the actual benchmark implementation and generator, rather than a description prepared before that implementation exists.
- `CW-H04` → `CW-H04.O1`: The family-specific validity dossier must evaluate the actual benchmark implementation and generator, rather than a description prepared before that implementation exists.

## Build the manufacturing benchmark (CW-H02)

**Proposal:** `CW-H02` · **Epic:** `CW-EP13` · **Russian:** Производственный стенд

Proposed accountable: **KC-Brain**; executor: **KC-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-H02)

- `CW-H02.O1`: Production benchmark family. Intended path: `roadmap/coordinated-work/work-products/benchmarks/production.md`. Future output, not yet claimed as created.

### Acceptance (CW-H02)

1. Независимый генератор дает скрытые вариации маршрутов, материалов, качества и смен.
2. Provide independent hidden variations in routes, materials, buffers, delays, quality, shifts and shared resources.
3. Keep generator, tuning set and locked evaluation set versioned and separate.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-H02)

- generator specification, hidden-set manifest and oracle receipts
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: A controller hard-coded to the original three-stage fluid probe must fail changed topology. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-H02)

- `CW-D03` → `CW-D03.O1`: Uses Finite-buffer and delay flow extension to define, constrain or evaluate Production benchmark family.
- `CW-D04` → `CW-D04.O1`: Uses Setup, defect and rework flow extension to define, constrain or evaluate Production benchmark family.
- `CW-D06` → `CW-D06.O1`: Uses Product-mix and shared-resource flow model to define, constrain or evaluate Production benchmark family.
- `CW-H01` → `CW-H01.O1`: Uses Per-study preregistration snapshots to define, constrain or evaluate Production benchmark family.
- `CW-N17` → `CW-N17.O1`: Uses Independent oracle and negative-control suite to define, constrain or evaluate Production benchmark family.

Source step `H02` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: H01.

Dependency revision: The production generator starts from flow extensions, registration and independent oracle; final comparison additionally waits for applicability validation.

## Build the service benchmark (CW-H03)

**Proposal:** `CW-H03` · **Epic:** `CW-EP14` · **Russian:** Сервисный стенд

Proposed accountable: **KC-Brain**; executor: **KC-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-H03)

- `CW-H03.O1`: Service benchmark family. Intended path: `roadmap/coordinated-work/work-products/benchmarks/service.md`. Future output, not yet claimed as created.

### Acceptance (CW-H03)

1. Есть разные навыки, SLA, abandonment, пики спроса и варианты маршрутизации.
2. Model skills, SLA, abandonment, time-varying arrivals and routing with renewable staffing capacity.
3. Separate demand served, unserved/abandoned demand, delay and worker load.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-H03)

- service generator, scenario manifest and analytical/independent checks
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: Renamed manufacturing stages do not satisfy service-specific abandonment and SLA behavior. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-H03)

- `CW-E03` → `CW-E03.O1`: Uses Multiskill assignment solver and checker to define, constrain or evaluate Service benchmark family.
- `CW-C03` → `CW-C03.O1`: Uses Demand observation schema to define, constrain or evaluate Service benchmark family.
- `CW-H01` → `CW-H01.O1`: Uses Per-study preregistration snapshots to define, constrain or evaluate Service benchmark family.

Source step `H03` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: H02.

Dependency revision: Service generator uses skills and demand plus registration, without waiting for completed production experiments.

## Build the project benchmark (CW-H04)

**Proposal:** `CW-H04` · **Epic:** `CW-EP15` · **Russian:** Проектный стенд

Proposed accountable: **KC-Brain**; executor: **KC-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-H04)

- `CW-H04.O1`: Project and knowledge-work benchmark family. Intended path: `roadmap/coordinated-work/work-products/benchmarks/project.md`. Future output, not yet claimed as created.

### Acceptance (CW-H04)

1. Разработка, проверка, тестирование и поддержка связаны общей нагрузкой.
2. Model dependencies among development, review, testing, rework and support using shared people.
3. Include uncertain effort, feedback cycles, interruptions and quality acceptance.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-H04)

- project generator, schedule fixtures and independent feasibility receipts
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: A schedule cannot count unfinished or unreviewed work as accepted delivered output. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-H04)

- `CW-C01` → `CW-C01.O1`: Uses Typed organizational work graph schema to define, constrain or evaluate Project and knowledge-work benchmark family.
- `CW-C04` → `CW-C04.O1`: Uses Availability, commitments and mentoring calendar to define, constrain or evaluate Project and knowledge-work benchmark family.
- `CW-H01` → `CW-H01.O1`: Uses Per-study preregistration snapshots to define, constrain or evaluate Project and knowledge-work benchmark family.

Source step `H04` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: H03.

Dependency revision: Project generator uses work topology/calendar plus registration, without waiting for completed service experiments.

## Separate performance from causation (CW-E06)

**Proposal:** `CW-E06` · **Epic:** `CW-EP16` · **Russian:** Производительность и причинность

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-E06)

- `CW-E06.O1`: Performance-versus-causation protocol. Intended path: `roadmap/coordinated-work/work-products/causal/performance.md`. Future output, not yet claimed as created.

### Acceptance (CW-E06)

1. Наблюдаемый выпуск не выдается за индивидуальный причинный вклад при неидентифицируемости.
2. State the causal estimand and plausible confounding/interference structure before claims.
3. Mark nonidentified individual contributions explicitly even when aggregate performance is observed.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-E06)

- causal diagram, estimand and identification assumptions
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: Raw individual throughput cannot be relabelled marginal causal contribution. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-E06)

- `CW-B06` → `CW-B06.O1`: Uses Outcome and constraint metric dictionary to define, constrain or evaluate Performance-versus-causation protocol.
- `CW-C05` → `CW-C05.O1`: Uses Evidence conflict-preserving store profile to define, constrain or evaluate Performance-versus-causation protocol.

Source step `E06` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: E05.

Dependency revision: Causal identification consumes metrics and provenance; it is not gated by engineering a capacity recommendation.

## Check endogenous observations (CW-F06)

**Proposal:** `CW-F06` · **Epic:** `CW-EP16` · **Russian:** Цензурирование и обратное влияние

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-F06)

- `CW-F06.O1`: Censoring, endogeneity and feedback audit. Intended path: `roadmap/coordinated-work/work-products/causal/endogenous-observation.md`. Future output, not yet claimed as created.

### Acceptance (CW-F06)

1. Политика обслуживания и цены не скрывают потерянный спрос и обратные связи.
2. Describe how pricing, service policy and routing change what is observed.
3. Separate true demand, observed transactions and intervention response.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-F06)

- observation model, causal assumptions and synthetic counterexamples
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: A service-capacity cut cannot be interpreted as an equal drop in underlying demand. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-F06)

- `CW-C03` → `CW-C03.O1`: Uses Demand observation schema to define, constrain or evaluate Censoring, endogeneity and feedback audit.
- `CW-C05` → `CW-C05.O1`: Uses Evidence conflict-preserving store profile to define, constrain or evaluate Censoring, endogeneity and feedback audit.

Source step `F06` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: F05.

Dependency revision: Endogeneity analysis uses demand/provenance and runs in parallel with risk-aware optimization.

## Design bounded field intervention (CW-N29)

**Proposal:** `CW-N29` · **Epic:** `CW-EP16` · **Russian:** Зарегистрировать полевое вмешательство, интерференцию и остановку

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-N29)

- `CW-N29.O1`: Field identification, interference and stopping protocol. Intended path: `roadmap/coordinated-work/work-products/field/protocol.md`. Future output, not yet claimed as created.

### Acceptance (CW-N29)

1. Intervention authority and data use established separately; design supports claimed estimand; shadow observations not relabelled as causal effect.
2. Define intervention unit, outcome estimand, interference/spillover structure, comparator and identification assumptions.
3. Bind actual intervention authority, monitoring, stopping, rollback and protocol amendments before effects.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-N29)

- registered protocol, authority records and stop/rollback rehearsal
- Exact versions, observed outcome, scope and unresolved limits.
- Adverse case: Shadow agreement or uncontrolled before/after trends cannot satisfy a causal intervention estimand. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-N29)

- `CW-E06` → `CW-E06.O1`: Uses Performance-versus-causation protocol to define, constrain or evaluate Field identification, interference and stopping protocol.
- `CW-H01` → `CW-H01.O1`: Uses Per-study preregistration snapshots to define, constrain or evaluate Field identification, interference and stopping protocol.
- `CW-N15` → `CW-N15.O1`: Uses Organizational/personnel data-use and access contract to define, constrain or evaluate Field identification, interference and stopping protocol.
- `CW-H07` → `CW-H07.O1`: Uses Read-only organizational shadow evaluation to define, constrain or evaluate Field identification, interference and stopping protocol.

## Specify organization decision adapter contracts (CW-N22)

**Proposal:** `CW-N22` · **Epic:** `CW-EP17` · **Russian:** Связать адаптеры действий с режимами и действующими полномочиями

Proposed accountable: **Agent-Brain**; executor: **Agent-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-N22)

- `CW-N22.O1`: Mode-bound execution adapter contract. Intended path: `roadmap/coordinated-work/work-products/runtime/action-adapters.md`. Future output, not yet claimed as created.

### Acceptance (CW-N22)

1. Exact source, environment, tool and authority bindings accompany actions; readiness permits only its declared action class; revocation rechecked at effect boundary.
2. Bind source/environment/tool/schema and current authority to observe/model/recommend/execute separately.
3. Recheck revocation and source freshness at effect boundary; preserve simulated versus actual actions.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-N22)

- adapter specification, effect-boundary fixtures and receipts
- Exact versions, observed outcome, scope and unresolved limits.
- Adverse case: A permission revoked after planning must prevent the intended live effect. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-N22)

- `CW-G03` → `CW-G03.O1`: Uses Mode-specific startup readiness checker to define, constrain or evaluate Mode-bound execution adapter contract.
- `CW-G04` → `CW-G04.O1`: Uses Independent proposal verifier interface to define, constrain or evaluate Mode-bound execution adapter contract.
- `CW-G06` → `CW-G06.O1`: Uses Decision-evidence receipt schema to define, constrain or evaluate Mode-bound execution adapter contract.
- `CW-C07` → `CW-C07.O1`: Uses Authorized read adapter prototypes to define, constrain or evaluate Mode-bound execution adapter contract.

## Exercise concurrent decision and recovery semantics (CW-N23)

**Proposal:** `CW-N23` · **Epic:** `CW-EP17` · **Russian:** Проверить конкурентность, отмену, повтор и откат

Proposed accountable: **Agent-Brain**; executor: **Agent-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-N23)

- `CW-N23.O1`: Concurrency, cancellation and rollback protocol. Intended path: `roadmap/coordinated-work/work-products/runtime/transaction-semantics.md`. Future output, not yet claimed as created.

### Acceptance (CW-N23)

1. Within declared failure model, stale or simultaneous decisions cannot double-spend capacity; idempotent retry preserves attempt identity and observed effects.
2. Specify reservation, cancellation, idempotency, retry, failure and compensation boundaries for each resource/action.
3. Exercise stale state, concurrent attempts, partial failures and deployment/source rollback with exact attempt identity.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-N23)

- adversarial traces, reservations, observed effects and compensation receipts
- Exact versions, observed outcome, scope and unresolved limits.
- Adverse case: Two retries cannot create duplicate effects; rollback cannot erase the history of already realized effects. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-N23)

- `CW-G07` → `CW-G07.O1`: Uses Concurrent decision state machine to define, constrain or evaluate Concurrency, cancellation and rollback protocol.
- `CW-N22` → `CW-N22.O1`: Uses Mode-bound execution adapter contract to define, constrain or evaluate Concurrency, cancellation and rollback protocol.

## Measure scale, latency and total decision cost (CW-N24)

**Proposal:** `CW-N24` · **Epic:** `CW-EP17` · **Russian:** Измерить масштабирование и полную стоимость работы

Proposed accountable: **Agent-Brain**; executor: **Agent-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-N24)

- `CW-N24.O1`: Scaling and full operational-cost evaluation. Intended path: `roadmap/coordinated-work/work-products/runtime/performance-cost.md`. Future output, not yet claimed as created.

### Acceptance (CW-N24)

1. Performance includes retrieval, verification, observation, human review, maintenance and failures; budget or stale-data limits yield a measured degradation path.
2. Measure latency, freshness and resource consumption across increasing graph/context/workload sizes.
3. Include retrieval, verification, model calls, human review, maintenance, failures and degradation policies.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-N24)

- load traces, budgets, cost assumptions and service-level results
- Exact versions, observed outcome, scope and unresolved limits.
- Adverse case: Reporting only model inference cost cannot satisfy the total-cost comparison. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-N24)

- `CW-N22` → `CW-N22.O1`: Uses Mode-bound execution adapter contract to define, constrain or evaluate Scaling and full operational-cost evaluation.
- `CW-H05` → `CW-H05.O1`: Uses Matched strong-baseline evaluation to define, constrain or evaluate Scaling and full operational-cost evaluation.

## Prepare Arcanada collective shadow consumer (CW-N26)

**Proposal:** `CW-N26` · **Epic:** `CW-EP18` · **Russian:** Подготовить теневой потребитель для существующей работы Arcanada

Proposed accountable: **Agent-Brain**; executor: **Agent-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-N26)

- `CW-N26.O1`: Arcanada collective shadow consumer harness. Intended path: `roadmap/coordinated-work/work-products/consumers/arcanada.md`. Future output, not yet claimed as created.

### Acceptance (CW-N26)

1. Use actual approved task/process observations and measured environment; no live HR or resource action inferred; separate predicted and observed outcomes.
2. Map one existing approved collective task/process into the profile with actual revisions and observations.
3. Produce timestamped recommendations and matched later observations without assuming execution authority.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-N26)

- consumer identity, input pins, shadow receipts and explicit gaps
- Exact versions, observed outcome, scope and unresolved limits.
- Adverse case: Synthetic collective fixtures cannot be reported as actual organizational use. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-N26)

- `CW-G08` → `CW-G08.O1`: Uses Learning-update review contract to define, constrain or evaluate Arcanada collective shadow consumer harness.
- `CW-N22` → `CW-N22.O1`: Uses Mode-bound execution adapter contract to define, constrain or evaluate Arcanada collective shadow consumer harness.
- `CW-N23` → `CW-N23.O1`: Uses Concurrency, cancellation and rollback protocol to define, constrain or evaluate Arcanada collective shadow consumer harness.
- `CW-H01` → `CW-H01.O1`: Uses Per-study preregistration snapshots to define, constrain or evaluate Arcanada collective shadow consumer harness.
- `CW-N15` → `CW-N15.O1`: Uses Organizational/personnel data-use and access contract to define, constrain or evaluate Arcanada collective shadow consumer harness.

## Prepare a second eligible organizational shadow consumer (CW-N27)

**Proposal:** `CW-N27` · **Epic:** `CW-EP18` · **Russian:** Выбрать и проверить второй доступный организационный потребитель

Proposed accountable: **Agent-Brain**; executor: **Agent-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-N27)

- `CW-N27.O1`: Second eligible consumer selection and shadow harness. Intended path: `roadmap/coordinated-work/work-products/consumers/second.md`. Future output, not yet claimed as created.

### Acceptance (CW-N27)

1. Distinct work topology and actual data eligibility established; no repackaged factory fixture passed off as a new organizational validation.
2. Choose an existing distinct consumer from the accepted roadmap only after data/owner/access eligibility is established.
3. Demonstrate a different topology or operating regime and pin implementation and observations.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-N27)

- consumer selection rationale, approval/access record and shadow receipts
- Exact versions, observed outcome, scope and unresolved limits.
- Adverse case: Renaming the Arcanada or factory fixture cannot count as external organizational validation. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-N27)

- `CW-G08` → `CW-G08.O1`: Uses Learning-update review contract to define, constrain or evaluate Second eligible consumer selection and shadow harness.
- `CW-N22` → `CW-N22.O1`: Uses Mode-bound execution adapter contract to define, constrain or evaluate Second eligible consumer selection and shadow harness.
- `CW-N23` → `CW-N23.O1`: Uses Concurrency, cancellation and rollback protocol to define, constrain or evaluate Second eligible consumer selection and shadow harness.
- `CW-H01` → `CW-H01.O1`: Uses Per-study preregistration snapshots to define, constrain or evaluate Second eligible consumer selection and shadow harness.
- `CW-N15` → `CW-N15.O1`: Uses Organizational/personnel data-use and access contract to define, constrain or evaluate Second eligible consumer selection and shadow harness.

## Evaluate decision explanation and human use (CW-N25)

**Proposal:** `CW-N25` · **Epic:** `CW-EP19` · **Russian:** Проверить понимание оператором и ценность дополнительной информации

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-N25)

- `CW-N25.O1`: Operator trace, comprehension and value-of-information study. Intended path: `roadmap/coordinated-work/work-products/human/decision-understanding.md`. Future output, not yet claimed as created.

### Acceptance (CW-N25)

1. People can recover assumptions, tradeoffs and missing evidence; explanation fluency is not counted as decision correctness.
2. Measure whether operators recover assumptions, tradeoffs, limitations and missing evidence from receipts.
3. Compare clarification/observation cost with changed decision quality and delay under registered scenarios.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-N25)

- task-based comprehension study and information-value analysis
- Exact versions, observed outcome, scope and unresolved limits.
- Adverse case: Fluent explanations or frequent questions cannot substitute for correct understanding and better decisions. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-N25)

- `CW-G06` → `CW-G06.O1`: Uses Decision-evidence receipt schema to define, constrain or evaluate Operator trace, comprehension and value-of-information study.
- `CW-N19` → `CW-N19.O1`: Uses Per-study design and comparison registration template to define, constrain or evaluate Operator trace, comprehension and value-of-information study.

## Run a shadow evaluation (CW-H07)

**Proposal:** `CW-H07` · **Epic:** `CW-EP20` · **Russian:** Теневой режим

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-H07)

- `CW-H07.O1`: Read-only organizational shadow evaluation. Intended path: `roadmap/coordinated-work/work-products/field/shadow.md`. Future output, not yet claimed as created.

### Acceptance (CW-H07)

1. Записаны рекомендации и последующие факты; причинный эффект вмешательства не заявлен.
2. Record timestamped recommendations before subsequent outcomes without changing work.
3. Compare predictions with actual eligible observations and disclose selection and missing data.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-H07)

- authorized snapshot, recommendation receipts and outcome linkage
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: Agreement with later outcomes cannot be called the causal effect of a non-executed recommendation. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-H07)

- `CW-H06` → `CW-H06.O1`: Uses Mechanism ablations and uncertainty report to define, constrain or evaluate Read-only organizational shadow evaluation.
- `CW-N26` → `CW-N26.O1`: Uses Arcanada collective shadow consumer harness to define, constrain or evaluate Read-only organizational shadow evaluation.
- `CW-N24` → `CW-N24.O1`: Uses Scaling and full operational-cost evaluation to define, constrain or evaluate Read-only organizational shadow evaluation.
- `CW-N25` → `CW-N25.O1`: Uses Operator trace, comprehension and value-of-information study to define, constrain or evaluate Read-only organizational shadow evaluation.

Source step `H07` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: H06.

Dependency revision: Shadow observation waits for completed controlled comparisons and the actual eligible Arcanada harness, performance and operator trace work.

## Evaluate a bounded field intervention (CW-H08)

**Proposal:** `CW-H08` · **Epic:** `CW-EP20` · **Russian:** Ограниченный причинный пилот

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-H08)

- `CW-H08.O1`: Bounded field intervention and outcome evaluation. Intended path: `roadmap/coordinated-work/work-products/field/intervention.md`. Future output, not yet claimed as created.

### Acceptance (CW-H08)

1. Выбран дизайн с учетом межпроцессных spillovers, остановки и внешней применимости.
2. Apply an approved identified design with spillovers, stopping conditions and rollback.
3. Report assigned/executed/observed units, deviations, harms, uncertainty and transport limits.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-H08)

- authority record, registered protocol, execution/outcome receipts and analysis
- Exact source/code/data revisions, execution or review scope, outcome and unresolved limits.
- Adverse case: A before/after improvement with uncontrolled concurrent changes cannot establish the claimed causal effect. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-H08)

- `CW-H07` → `CW-H07.O1`: Uses Read-only organizational shadow evaluation to define, constrain or evaluate Bounded field intervention and outcome evaluation.
- `CW-E06` → `CW-E06.O1`: Uses Performance-versus-causation protocol to define, constrain or evaluate Bounded field intervention and outcome evaluation.
- `CW-N29` → `CW-N29.O1`: Uses Field identification, interference and stopping protocol to define, constrain or evaluate Bounded field intervention and outcome evaluation.

Source step `H08` at `ea698baa3d4997b56c725d806c600173aa6064b9`; original status `planned` is a historical source observation, not native task state. Original dependencies: H07.

Dependency revision: Field intervention requires shadow results, causal-identification boundaries and the separately approved intervention/stopping protocol.

## Run held-out transfer and external reproduction (CW-N28)

**Proposal:** `CW-N28` · **Epic:** `CW-EP20` · **Russian:** Проверить перенос и внешнее воспроизведение

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-N28)

- `CW-N28.O1`: Held-out transfer and external reproduction study. Intended path: `roadmap/coordinated-work/work-products/transfer/external.md`. Future output, not yet claimed as created.

### Acceptance (CW-N28)

1. Separate organization, task-distribution and regime holdouts; independent executor access/versions recorded; unsuccessful transfer retained.
2. Freeze organization, task-distribution and operating-regime holdouts and the transfer conditions.
3. Record independent executor/environment/access and all unsuccessful reproductions or transfers.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-N28)

- holdout manifest, pinned package and reproduction receipts
- Exact versions, observed outcome, scope and unresolved limits.
- Adverse case: Retuning on the held-out organization must be reported and cannot retain untouched-transfer status. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-N28)

- `CW-H06` → `CW-H06.O1`: Uses Mechanism ablations and uncertainty report to define, constrain or evaluate Held-out transfer and external reproduction study.
- `CW-I04` → `CW-I04.O1`: Uses Frozen reproducibility package per artifact to define, constrain or evaluate Held-out transfer and external reproduction study.

## State recursive feasibility and stability conditions (CW-N13)

**Proposal:** `CW-N13` · **Epic:** `CW-EP21` · **Russian:** Исследовать устойчивость и рекурсивную допустимость

Proposed accountable: **KC-Brain**; executor: **Research-Arcana**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-N13)

- `CW-N13.O1`: Conditional stability and recursive-feasibility study. Intended path: `roadmap/coordinated-work/work-products/control/stability.md`. Future output, not yet claimed as created.

### Acceptance (CW-N13)

1. Proof obligations, invariant region and operational limits differ; finite queue growth is not called a proof of asymptotic instability.
2. Declare dynamics, disturbance/load region, invariant set and admissible policy class.
3. Separate formal conditions, finite instability examples, empirical control quality and operating limits.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-N13)

- proof obligations, counterexamples and simulation receipts
- Exact versions, observed outcome, scope and unresolved limits.
- Adverse case: A finite queue-growth trace cannot establish asymptotic instability or global stability. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-N13)

- `CW-N12` → `CW-N12.O1`: Uses Conditional admissibility definitions and proof obligations to define, constrain or evaluate Conditional stability and recursive-feasibility study.
- `CW-D03` → `CW-D03.O1`: Uses Finite-buffer and delay flow extension to define, constrain or evaluate Conditional stability and recursive-feasibility study.
- `CW-F04` → `CW-F04.O1`: Uses Decision-lag dynamics model to define, constrain or evaluate Conditional stability and recursive-feasibility study.

## Specify claim and evidence lineage (CW-N10)

**Proposal:** `CW-N10` · **Epic:** `CW-EP22` · **Russian:** Связать происхождение и идентичность свидетельств с существующим KC

Proposed accountable: **KC-Brain**; executor: **KC-SWE**; assessor: **DEUS-Arcana**. These fields do not assign a native task.

### Output (CW-N10)

- `CW-N10.O1`: Evidence lineage and identity profile reusing KC. Intended path: `roadmap/coordinated-work/work-products/interop/evidence-lineage.md`. Future output, not yet claimed as created.

### Acceptance (CW-N10)

1. Existing KC mechanisms reused; conflicting observations and attempts remain distinct; no latest-write-wins loss; no new native kinds asserted.
2. Map claims, source observations, attempts, models, decisions and outcomes to existing KC mechanisms.
3. Preserve inconsistent evidence and validate evidence reuse conditions under identity changes.
4. The declared negative control is evaluated and its expected rejection or qualification is recorded.

### Evidence and adverse control (CW-N10)

- F05/Agent Situation/Artifact Registry mapping and conflict fixtures
- Exact versions, observed outcome, scope and unresolved limits.
- Adverse case: Latest-write-wins, mismatched attempt IDs or unproven execution binding cannot transfer a verdict. Expected: Rejected, flagged, or explicitly prevented from supporting the stronger claim.

### Consumed inputs (CW-N10)

- `CW-A01` → `CW-A01.O1`: Uses Review scope and eligibility protocol to define, constrain or evaluate Evidence lineage and identity profile reusing KC.

# Coordinated Work: prepare, reconcile and register the programme

**Document state:** registration runbook and offline tooling candidate. This document does not create tasks, assign engineers, start work, qualify research, or record current Muneral state.

**Programme:** `KC-CW-20261118`. **Prepared source:** [`plan/execution-graph.json`](plan/execution-graph.json). All programme, epic and work-package identifiers in that graph are proposal keys. A separate private mapping supplies actual native UUIDs after authoritative readback.

## 1. Named route and authority

The existing Muneral project is **knowledge-contract**, UUID `5d427422-4a5e-45a7-bc3b-f0aa11579a5b`, project prefix **KCP**. The workspace registry calls the project `contract-place`; that registry ID is not the Muneral slug. There is no verified Coordinated Work parent epic in this source package. Find and reuse one if it exists; create only a genuinely missing programme container.

**KC-SWE is the registration coordinator for prepared Knowledge Contract work.** Reconcile the existing owner/work graph before registering anything. Agent-SWE handles its necessary cross-project bindings through its own authorized route. KC-Brain remains responsible for the proposed scientific content; recording prepared work does not transfer its authorship or scientific acceptance to an engineer. Do not create another worker or independently register the same scope from a second coordinator.

Use the current authorized `dev-tools/muneral/mun` client and the role's valid native principal. This runbook does not supply credentials, invoke that client, request new permissions, or substitute Collective 2.0 tasks for Muneral. A hosted author without a native route prepares this package and sends it to the existing KC-SWE through the collective mailbox.

Source-backed route references, read at workspace commit `66e0ba6aaaef533f450161a5d61fd15c2bab062e`:

- [Project registry](https://github.com/Arcanada-one/arcanada-workspace/blob/66e0ba6aaaef533f450161a5d61fd15c2bab062e/spaces/arcanada/space.yml), blob `43d9c36b1b1042f6b65acfe794ee0da14bc50240`.
- [Muneral agent route map](https://github.com/Arcanada-one/arcanada-workspace/blob/66e0ba6aaaef533f450161a5d61fd15c2bab062e/documentation/reference/muneral-agent-routes.md), blob `6a62ce0b3295826469b6d288280a59d1daa1c266`.
- [Supported client](https://github.com/Arcanada-one/arcanada-workspace/blob/66e0ba6aaaef533f450161a5d61fd15c2bab062e/dev-tools/muneral/mun), blob `9c680d2d80675d686b7e7cbd74f6a4f1462deae6`, and [README](https://github.com/Arcanada-one/arcanada-workspace/blob/66e0ba6aaaef533f450161a5d61fd15c2bab062e/dev-tools/muneral/README.md).
- [Task lifecycle and acceptance](https://github.com/Arcanada-one/arcanada-workspace/blob/66e0ba6aaaef533f450161a5d61fd15c2bab062e/documentation/mandates/task-lifecycle-and-acceptance.md), blob `c99967a3e71c62ade47509dc491b65d5b6215df2`.
- [Existing Workgraph Reconciliation](https://github.com/Arcanada-one/knowledge-contract/blob/ea698baa3d4997b56c725d806c600173aa6064b9/roadmap/TASKS.md), owned by KC-SWE. That document distinguishes public roadmap references from actual task identities.
- [Existing Live Lab proposal graph](https://github.com/Arcanada-one/arcanada-workspace/blob/66e0ba6aaaef533f450161a5d61fd15c2bab062e/documentation/plans/knowledge-collective-live-lab/task-graph.json), which establishes reconciliation, separate actual UUID mapping and accepted prerequisite-output checks. Its proposal JSON is not a native API import schema.

The route map describes observations from 11 November. The current owner must check applicable grants, endpoint behavior and native ownership before mutation; this package is not a new live API observation.

## 2. What the offline tool provides

[`tools/prepare_cw_registration.py`](../../tools/prepare_cw_registration.py) uses Python's standard library. It never reads credentials, imports a network client, calls a subprocess, or submits a request. It prepares:

| Output | Purpose | Publication boundary |
| --- | --- | --- |
| `registration-plan.private.json` | Parent-first task-create templates, directed dependency templates, exact scope text/digests, and proposed topological work waves | Private once bindings are supplied; not a native ledger |
| `bindings.private.json` | One-to-one logical-key → actual UUID mapping scaffold, reconciliation decisions, native role bindings and inventory evidence | Private; never commit native identities or receipts publicly |
| `scope-records.private/*.txt` | Exact UTF-8 contract text for a new task description or versioned native CONTENT on a reused task | Private registration inputs; exact bytes are checked later |
| `preparation-summary.json` | Counts, source binding state, and explicit zero native requests | May be used as a bounded preparation observation |
| `paper-release-instances.private.json` | Six artifact-specific release-stage templates per proposed paper, with mandatory evidence inputs | Preparation only; these 96 stage templates are separate from the 128 programme/epic/package objects and are not native registrations |
| `registration-receipt.public.json` | A strictly limited status projection, generated only after complete supplied-readback consistency | Sanitized candidate; still requires owner review and publication policy |

The tool checks global identifier uniqueness across the programme, epics and work packages. This matters because imported step `CW-E01` must not also identify an epic. Epics therefore use a separate `CW-EP…` namespace. It also checks epic membership, numbered ACs, dependency direction, acyclicity, consumed-output references and separation between proposed and native state.

The graph also declares 16 paper-specific release contracts and 138 required-evidence edges, separately from the 247 work-package edges. Preparation instantiates and validates six proposed release stages per paper. P09, P13 and P15 retain H08 and the stated causal/intervention inputs upstream of their own manuscript and release. A review or formal result follows its own scope; a narrower preliminary paper requires a separately reviewed contract. This is a structural refusal check, not an acceptance of a study or permission to publish. The 96 stage templates must be reconciled and bounded by the owner before any native creation; they do not enlarge the automatic 128-object registration batch.

To check a previously prepared release-instance file, pass `--release-instances /private/path/paper-release-instances.private.json` with the same `--source-commit` and exact graph bytes. A different source commit, graph digest, paper scope, stage identity or missing evidence gate is refused before preparation. This option performs no native request.

Registration contains one proposed programme container, the proposal's epic containers, and its work packages. Their combined count is **not** a count of implemented or accepted work packages. Work packages marked `needs_child_instantiation` still require bounded child tasks before implementation dispatch. Successful JSON generation does not admit that scope.

### Prepare from an uncommitted candidate

From the repository root:

```bash
python3 tools/prepare_cw_registration.py \
  --graph roadmap/coordinated-work/plan/execution-graph.json \
  --output /tmp/kc-cw-registration-candidate-01
```

This intentionally leaves `source_commit` unbound. Every create template remains held. No native UUID is generated or guessed.

### Bind to the committed graph

Replace `SOURCE_COMMIT_SHA` with the full exact commit containing the reviewed graph, and choose a fresh output directory:

```bash
python3 tools/prepare_cw_registration.py \
  --graph roadmap/coordinated-work/plan/execution-graph.json \
  --source-commit SOURCE_COMMIT_SHA \
  --output /tmp/kc-cw-registration-source-01
```

The tool hashes the exact graph bytes. A Git SHA argument is a supplied source claim; the tool does not contact GitHub to authenticate it. The registrar must read the file on that exact commit and confirm the bytes. Changing graph bytes or source commit invalidates the previous mapping/snapshot checks until reconciled against the new version.

## 3. Reconcile before creating

1. Read current project identity and the existing programme/roadmap/workgraph bindings. Use existing task titles, scope, source references and acceptance history as well as the stable proposal key. Do not identify work by a similar title alone.
2. Read the complete authorized project index, or obtain a current authoritative inventory from the existing owner. `GET /tasks/project/{projectId}` returns only the caller's own tasks; an empty result does not establish that the programme is absent. `GET /tasks/project/{projectId}/index` needs an applicable MUN-0052 grant. A 403/404 caused by scope is not evidence that the task or project does not exist.
3. Record `inventories[]` per mapped project with its coverage, observed time and durable evidence reference. The tool accepts `complete_project_index` or `authoritative_owner_inventory` as a **recorded assertion of completeness**, not as proof of its truth. `own_tasks_only` and `NOT_READ` keep new work held. An owner inventory must describe how complete coverage was obtained; do not relabel a partial list.
4. Record one `single_writer_role`. Assign every proposal a decision: `reuse`, `create`, `unresolved`, or `unknown_outcome`. A decision to create requires a concrete reconciliation reference showing why existing scope does not cover the output.
5. A reused task keeps its history. Do not silently widen a done/review task or replace its earlier description. If the new scope needs a successor or child, make that decision explicit and bind the resulting native task separately.
6. Native task UUIDs must be canonical UUIDs actually returned and read back from Muneral. The tool rejects duplicate mappings of different proposal scopes onto the same UUID. If several outputs genuinely belong to one existing task, the owner must first revise the proposal decomposition; do not defeat the one-to-one check.

The native project/parent/owner fields are separate from logical proposal IDs. `CW-N01` is never accepted as a native UUID. A task merely mentioned in a message is still unbound until its exact native record is read.

## 4. Create missing records in a controlled order

The generated create order is programme → epic containers → work packages. Task dependency ordering is retained for readability, but registration is distinct from execution: a blocked task may be registered without being started.

The source-backed native create body contains only supported fields:

```json
{
  "projectId": "5d427422-4a5e-45a7-bc3b-f0aa11579a5b",
  "title": "KCP <proposal key>: <prepared title>",
  "description": "<exact generated scope text with numbered ACs>",
  "parentId": "<actual reconciled parent UUID>",
  "status": "todo"
}
```

`parentId` is absent for the top programme container. Other templates use `${MUNERAL_UUID:logical-key}` until the actual parent is known. A string placeholder is deliberately **not a valid task UUID** and must never be submitted. Optional supported `priority` is not inferred by this generator.

`template_complete` means no parent/endpoint placeholder remains. `recorded_prerequisites_complete` means the provided inventory/source/decision fields are present. Neither field establishes access rights, ownership acceptance, native readiness, semantic scope admission, or permission to dispatch an engineer. Those remain current checks for the acting owner.

For every submitted creation, retain the response and immediately read the exact task. Record its UUID in the private map before moving on. Re-run preparation with `--bindings /private/path/bindings.json` to replace known parent references and omit already mapped create operations.

The create payload has no invented owner-assignment field. Preserve the source's proposed accountable and executor roles in the description; resolve actual native identities and perform any necessary assignment through the owner's supported route. Read both ownership evidence and actual assignees back. A native creator, accountable content owner and execution assignee can represent different responsibilities; do not label them interchangeable.

### Reused tasks and scope evidence

For a new task, `scope_record_type: "description"` requires the native description's UTF-8 SHA-256 to match the generated text. For a reused task that needs a versioned prepared contract, set `scope_record_type: "content"` and use a native CONTENT record titled `ACCEPTANCE CRITERIA v<N>` containing the exact generated scope text. Preserve the old description and earlier CONTENT. The scope digest check establishes byte equality only; the actual owner/reviewer must decide whether the scope is admissible and met.

The existing client provides `artifact-put TASK_UUID --file PATH --name NAME`; use the current owner-approved name/version and verify its response and exact artifact readback. A comment is not a substitute for a native CONTENT acceptance record.

If an existing task cannot or should not be reparented, `parent_mode: "reference_only"` is allowed only for reuse. Keep its observed `preserved_parent_uuid` and a durable `logical_parent_evidence_ref` documenting the explicit programme mapping. The tool checks the preserved native parent and counts these exceptions in the sanitized receipt. Do not claim all reused tasks appear as native children.

### Unknown outcomes and idempotency

No task-create idempotency field or bulk-import endpoint is established by the pinned client source. Its generic request helper can retry HTTP 429 responses; that implementation does not prove at-most-once task creation.

After a timeout, ambiguous result, or suspicious retry, record `decision: "unknown_outcome"` and stop reposting that proposal. Reconcile all matching current records by stable proposal key, exact scope digest, creator and attempt evidence. If exactly one actual record is established, read it and bind it. If multiple records exist, let their owner decide which scope/history to preserve and how to disposition the duplicates. Never delete or overwrite competing work automatically. An absent result from an incomplete list does not clear the hold.

This generator does not retry, send, or schedule anything. A future native bulk adapter would need its own scoped idempotency and crash/restart acceptance, separately from this offline tool.

## 5. Bind actual blocking edges

Only after both native endpoints are known, reconcile the existing edge list. The prepared edge's orientation is **dependent → prerequisite**:

```json
{"toTaskId": "<actual prerequisite UUID>", "type": "depends_on"}
```

It belongs at `POST /tasks/<dependent UUID>/dependencies`. The acting key must be creator or executor of both endpoints. Cross-project or differently owned endpoints require their existing owners' authorized coordination; do not impersonate another principal.

The existing native types are `depends_on`, `blocks`, `related_to`, and `duplicates`. The graph's consumed-output contract stays in the prepared task scope; do not invent a new native dependency enum. `related_to` never satisfies a start-blocking edge. Do not submit an edge already observed. A reference to a paper or prior result is not automatically a new blocking task.

Preserve native dependencies outside this proposal. Unexpected, reversed, or external blockers cause the offline verifier to reject a claim of exact graph agreement. Reconcile them with the owner and revise the plan/scope where appropriate; do not remove a real prerequisite simply to make the checker pass. Extra advisory links are reported separately.

## 6. Capture and check exact readbacks

For each mapped native task, retain exact task, ownership, assignee and readiness observations. For each blocking edge retain the actual dependencies observation. A normalized private readback uses this contract (angle-bracket values are explanatory placeholders, not valid fixture IDs):

```json
{
  "schema": "kc-cw-muneral-readback/1",
  "programme_id": "KC-CW-20261118",
  "graph_sha256": "<64 lowercase hexadecimal characters>",
  "source_commit": "<40 lowercase hexadecimal characters>",
  "observed_at": "<ISO 8601 timestamp with timezone>",
  "tasks": [{
    "proposal_id": "CW-N01",
    "task_uuid": "<actual native UUID>",
    "project_uuid": "<actual project UUID>",
    "parent_uuid": "<actual native parent UUID or null>",
    "owner_role": "<source-proposed role, after actual agreement>",
    "owner_native_id": "<read-back identity corresponding to that role>",
    "executor_role": "<source-proposed executor, after actual assignment>",
    "executor_native_id": "<read-back execution identity>",
    "task_evidence_ref": "<durable private task response>",
    "owner_evidence_ref": "<durable native accountable-owner agreement>",
    "assignees_evidence_ref": "<durable assignee response>",
    "readiness_evidence_ref": "<durable readiness response>",
    "scope_record_type": "description",
    "scope_record_sha256": "<SHA-256 of exact native scope-record UTF-8 bytes>",
    "scope_evidence_ref": "<native description or CONTENT exact readback>"
  }],
  "dependencies": [{
    "from_uuid": "<actual dependent UUID>",
    "to_uuid": "<actual prerequisite UUID>",
    "type": "depends_on",
    "evidence_ref": "<durable dependency response>"
  }]
}
```

This normalization format is local to the offline tool. Its field names are not claimed as the server's raw JSON response schema. Preserve the raw responses behind the evidence references; the normalized role assertions must be checked against those records. An unverified reference string or hash is not authentication.

Run the complete consistency check with a fresh output directory:

```bash
python3 tools/prepare_cw_registration.py \
  --graph roadmap/coordinated-work/plan/execution-graph.json \
  --source-commit SOURCE_COMMIT_SHA \
  --bindings /private/path/cw-bindings.json \
  --readback /private/path/cw-readback.json \
  --output /tmp/kc-cw-registration-readback-01
```

The checker requires every proposal, exact project/parent/owner/executor correspondence, native scope-record digest, and the complete directed blocker set. A complete matching supplied snapshot produces `OFFLINE_CONSISTENT`; it does not become `LIVE_VERIFIED`, scientific acceptance or task completion. The plan then omits already satisfied edge-create requests. Partial binding files still support preparation; partial readback sets do not produce a public receipt claiming complete registration.

The [public receipt schema](registration-public-receipt.schema.json) is a whitelist: public programme/proposal IDs, graph digest, public source commit, observation time, aggregate mapping counts and explicit verification limits. It omits native task UUIDs, principal identities, private source paths, evidence URLs and native execution statuses. The owner must review the output before publishing it, and must not present the recorded snapshot as a fresh live check.

## 7. Registration, execution and announcement are different outcomes

The first epic prepares the programme announcement, repository entry, three-language publication and task registration. Public announcement does not depend on every native registration finishing; its source and release checks still apply. A completion claim for the combined announcement/registration handoff requires the evidence defined by its own source-authored task contracts.

Before starting any implementation work, read current native readiness and the actual accepted prerequisite outputs, admitted scope, executor identity and available capacity. A cancelled/archived prerequisite without its required output cannot satisfy that output contract. The tool's topological waves only show a proposed partial order; they do not authorize starting all members in parallel. Broad packages must first yield their bounded implementation children.

Keep separate observations for: source proposal; independent review; native registration; accepted scope; exact-head CI; merged source; deployed website; served EN/RU/zh-Hans content; and real consumer reuse. Do not transfer any one observation into another.

## 8. Finite controls

Run from the repository root:

```bash
python3 -m unittest discover -s tools -p 'test_prepare_cw_registration.py' -v
python3 -O -m unittest discover -s tools -p 'test_prepare_cw_registration.py' -v
```

The suite uses explicitly synthetic UUIDs and never calls a native API. It covers duplicate IDs and bindings, graph cycles, wrong consumed outputs, incomplete inventories, unknown creation outcomes, stale source/graph bindings, wrong owner/executor/parent, changed native scope text, missing/reversed/additional blockers, advisory-link substitution, and public receipt leakage. Runtime validation uses explicit exceptions rather than `assert`, so optimized Python does not remove the checks.

Local finite checks establish behavior of this preparer on those cases. Hosted CI, non-author review, authenticated readback provenance, actual registry application and production benefit require separate observations.

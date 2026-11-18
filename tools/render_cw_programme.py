#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Render human-readable work contracts from the versioned proposal graph."""
import argparse
import json
import re
from pathlib import Path

try:
    from .cw_programme_localizations import render_locale_programmes
except ImportError:
    from cw_programme_localizations import render_locale_programmes

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "roadmap/coordinated-work/plan"
EPIC_EN = [
    "Announcement and registration", "Corpus and research map", "Needs and capability ontology",
    "Organizational state and permitted sources", "Flows, capacity and constraints",
    "Teams and capability planning", "Forecasting, uncertainty and drift", "Decision contracts and agent verification",
    "Experimental design and comparisons", "Scientific publication in three languages", "Formal admissibility and resource types",
    "Data rights, privacy and reference packages", "Independent oracles and model validity", "Manufacturing stand",
    "Service stand", "Project and knowledge-work stand", "Causality, observability and interference",
    "Execution, concurrency and full cost", "Consumers and ecosystem integration", "Operator understanding and information value",
    "Shadow, field and external reproduction", "Dynamics and recursive feasibility", "KC compatibility and evidence lineage",
]


def cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def task_link(key, tasks):
    heading = f"{tasks[key]['title']} ({key})".lower()
    anchor = re.sub(r"[^\w -]", "", heading).replace(" ", "-")
    return f"[{key}](TASK_CONTRACTS.md#{anchor})"


def render(graph):
    tasks = {t["id"]: t for t in graph["tasks"]}
    ordered = [tasks[key] for epic in graph["epics"] for key in epic["task_ids"]]
    pin = graph["source"]["head"]
    source_url = f"https://github.com/Arcanada-one/knowledge-contract/tree/{pin}/roadmap/coordinated-work"
    en = ["# Coordinated Work: Execution Programme and Research Delivery", "",
          "Prepared 18 November 2026. Status: **source proposal for reconciliation and review**. "
          "Muneral remains the authority for actual task identities, assignments, dependencies and execution states.", "",
          "This programme has **23 epics, 104 work packages and 247 output-consuming blocking edges**. "
          "It preserves all **72 original steps**, adds **32 explicit missing work packages**, "
          "and maps **16 potential papers and 12 hypotheses**. The [machine-readable graph](execution-graph.json) "
          "and [complete task contracts](TASK_CONTRACTS.md) are the source for registration. "
          "The [Russian programme](PROGRAMME.ru.md) and [Simplified Chinese programme](PROGRAMME.zh-Hans.md) "
          "present the same scope tables and bind their source to this English text.", "",
          "The 104 entries are work packages. Broad review batches, benchmark families and publication templates "
          "must be split into bounded children before dispatch. A proposed owner is not an actual assignment. "
          "The 128 programme/epic/package objects prepared for reconciliation are not 128 created Muneral objects.", "",
          "## Starting evidence and intended contribution", "",
          f"The [initial research package]({source_url}) retains 1,176 bibliographic records: 157 checked primary records "
          "and 1,019 citation candidates. Unique-work identity remains unresolved (26 title/year groups and four "
          "near-title pairs); completed full-text critical appraisals are zero. The retained revision-2 probe has "
          "10 scenarios, 100 case-period observations and 190 elementary checks. These support a bounded numerical "
          "implementation claim, not agent effectiveness or validity for a real organization.", "",
          "The proposed contribution is an organizational domain profile connecting needs, work networks, "
          "distinct resource semantics, competencies and decision evidence to Agent Situation and Context Assembly. "
          "Novelty must survive comparison with existing research; no new native KC artifact kind or execution "
          "authority follows from introducing a profile.", "",
          "## First epic: make the programme visible and actionable", "",
          "CW-EP00 covers source freezing, the programme charter, this graph, EN/RU/zh-Hans Journal announcements, "
          "roadmap and repository navigation, native task reconciliation, verified public delivery and a bounded "
          "collective handoff. An accepted announcement may ship while native registration is pending; N08 requires "
          "both publication and registration receipts before the complete launch handoff closes.", "",
          "| Package | Observable output | Proposed accountable / executor | Blocking inputs |",
          "| --- | --- | --- | --- |"]
    for key in graph["epics"][0]["task_ids"]:
        t = tasks[key]
        en.append(f"| {task_link(key, tasks)} — {cell(t['title'])} | {cell(t['outputs'][0]['description'])} | "
                  f"{t['proposed_owner_role']} / {t['proposed_executor_role']} | {', '.join(d['task_id'] for d in t['dependencies']) or 'Source inputs only'} |")
    en += ["", "Launch acceptance includes exact source and translation bindings, rights/attribution, independent "
           "review at the stated scope, hosted validation, an explicit rollback revision, publication workflow "
           "and anonymous served-page readback. Browser inspection must verify that the actual article is visible "
           "on desktop/mobile and that language switching preserves the issue; metadata or a lexical HTML check "
           "cannot establish those properties.", "", "## Parallel delivery sequence", "",
           "The following diagram is an overview, not the authoritative 247-edge graph. Every real blocking edge "
           "in the JSON names the predecessor output it consumes.", "", "```mermaid", "flowchart TD",
           '  A["Freeze sources and programme"] --> B["Announce and reconcile tasks"]',
           '  A --> C["Review sources and define claims"]',
           '  C --> D["Models, schemas and study protocols"]',
           '  D --> E["Manufacturing stand"]', '  D --> F["Service stand"]', '  D --> G["Project stand"]',
           '  E --> H["Validated controlled comparisons"]', '  F --> H', '  G --> H',
           '  H --> I["Eligible shadow use"]', '  I --> J["Bounded field evaluation"]',
           '  C --> K["Claim-specific scientific releases"]', '  H --> K', '  J --> K', "```", "",
           "1. **Launch and reconciliation.** Freeze source/evidence, publish the truthful programme description, "
           "reconcile existing Muneral work and prepare the first bounded batch.",
           "2. **Parallel foundations.** Review primary sources, define needs/resources/work graphs, build "
           "the provenance schema, define rights and data contracts, and register study-specific questions.",
           "3. **Parallel domain stands.** Build manufacturing, service and project families after their own "
           "required inputs. Run independent oracles and model-validity checks before confirmatory comparison.",
           "4. **Controlled evidence.** Compare the current method, strong OR, no-retrieval agent, strong ordinary "
           "RAG and full KC profile under declared matched budgets; retain ablations, failures and uncertainty.",
           "5. **Eligible real use.** Bind an actual Arcanada task and implementation, collect shadow evidence, "
           "then evaluate a separately authorized bounded intervention and held-out transfer.",
           "6. **Release by claim.** A reviewed source map, a conditional proof and an organizational causal "
           "claim have different evidence obligations. A literature or formal result does not wait for a global "
           "field trial; a causal-effect claim still requires one or another justified identification design.", "",
           "The [dependency decisions](DEPENDENCY-DECISIONS.md) retain the source edge history and justify each revision. The original dependency chain reaches 64 tasks; the proposed graph reaches 17. These are topological "
           "node counts, not days, effort estimates or demonstrated speedup. Capacity, review availability and "
           "duration estimates must be bound during native reconciliation. The existing six-role collective is "
           "reused; task rows do not create additional agents.", "", "## Epic register", "",
           "| Epic | Scope | Work packages | Proposed accountable / executor |", "| --- | --- | ---: | --- |"]
    for e, title in zip(graph["epics"], EPIC_EN):
        en.append(f"| {e['id']} | {title} | {len(e['task_ids'])} | {e['proposed_owner_role']} / {e['proposed_executor_role']} |")
    en += ["", "## Complete work-package inventory", "",
           "Every linked contract records numbered acceptance criteria, exact proposed output, evidence, "
           "negative control, source coverage, reviewer and consumed predecessor outputs.", "",
           "| Package | Work | Epic | Blocking prerequisites |", "| --- | --- | --- | --- |"]
    for t in ordered:
        en.append(f"| {task_link(t['id'], tasks)} | {cell(t['title'])} | {t['epic_id']} | {', '.join(d['task_id'] for d in t['dependencies']) or 'None in this proposal'} |")
    en += ["", "## Scientific series and engineering companions", "",
           "These are candidate boundaries, not sixteen completed or accepted papers. Final partition follows "
           "the research. Each artifact instantiates I03–I08 with its own source, result, review and release evidence.", "",
           "| Candidate | Research question | Engineering companion | Primary work packages |",
           "| --- | --- | --- | --- |"]
    for p in graph["papers"]:
        en.append(f"| {p['id']} — {cell(p['source_title'])} | {cell(p['source_main_question'])} | "
                  f"{cell(p['source_engineering_companion'])} | {', '.join(p['mapped_task_ids'])} |")
    en += ["", "## Per-paper release gates", "",
           "Coverage mappings are not release permission. Each of the sixteen papers has an explicit claim "
           "scope and typed required-evidence edges. The current proposal adds 138 such edges and sixteen "
           "release-instance templates containing 96 stage nodes. These are counted separately from the "
           "104 work packages and 247 package dependencies; none is a created native task or accepted result.", "",
           "Each release instance substitutes its own outputs into I03–I08 and must place every required gate "
           "upstream of its manuscript and final release. The validator rejects a P13 release missing H08, "
           "an advisory link substituted for an evidence dependency, or another paper's stage output. "
           "Registration preparation includes these contracts in the native scope templates and emits separate "
           "release DAG templates; it sends no requests.", "",
           "P09 and P13 organizational-effect scopes and P15 organizational-transfer scope require H08 plus "
           "the causal and intervention prerequisites. Review, model and formal scopes do not acquire a "
           "universal H08 dependency. An earlier protocol-only or narrower formal contribution needs a separate "
           "reviewed scope contract that excludes unobserved effect claims; it cannot silently weaken one of "
           "the contracts below.", "",
           "External reproduction N28 consumes frozen H06 evaluation inputs and N16 data packages. Before "
           "independent execution it pins code, environment, model, configuration and seeds. It does not wait "
           "for I04 of the paper whose release it must gate; the final I04 package later includes its receipts.", "",
           "| Paper | Declared claim scope | Required evidence gates |", "| --- | --- | --- |"]
    for contract in graph["paper_release_contracts"]:
        en.append(f"| {contract['paper_id']} | {cell(contract['claim_scope'])} | "
                  f"{', '.join(gate['task_id'] for gate in contract['required_gates'])} |")
    en += ["", "## Hypotheses and possible refutation", "",
           "Each hypothesis maps to H01 preregistration and N20 statistical design plus the domain-specific "
           "work packages in the JSON. All outcomes remain unknown.", "",
           "| Hypothesis | Comparison | What would challenge the claim |", "| --- | --- | --- |"]
    for h in graph["hypotheses"]:
        en.append(f"| {h['id']} — {cell(h['source_statement'])} | {cell(h['source_comparison'])} | {cell(h['source_refutation'])} |")
    en += ["", "## Execution and evidence gates", "",
           "Use [Muneral registration](../MUNERAL-REGISTRATION.md) for scope reconciliation, actual parent/owner "
           "binding, idempotent-by-reconciliation creation and exact dependency readback. The offline preparation "
           "tool emits templates, never HTTP requests. Partial visibility cannot establish that work is absent.", "",
           "Keep source/data/code versions, attempts, claims, verdicts and execution events separately identified. "
           "Preserve contradictory evidence; validate empty possible-world sets, insufficient authority, unavailable "
           "resources and failed/partial effects explicitly. A knowledge packet describing a permission does not "
           "grant it. Current task admission, applicable data rights and experiment budgets are checked before use.", "",
           "Measured costs must include source appraisal, annotation, human review, models/tools, failed attempts "
           "and maintenance. Current programme cost and delivery dates are NOT_MEASURED; no empirical experiment "
           "is activated by this planning artifact.", "", "## Reproduce the proposal checks", "", "```sh",
           "python3 -B tools/check_cw_programme.py", "python3 -B -m unittest tools.test_check_cw_programme -v",
           "python3 -O -B -m unittest tools.test_check_cw_programme -v", "python3 -B tools/render_cw_programme.py --check", "```", "",
           "The checks validate finite structure, coverage and stated evidence boundaries. They do not certify "
           "scientific truth, novelty, review, native registration, deployment or effective use.", ""]

    contracts = ["# Work Contracts: Coordinated Work Package Register", "",
                 "Generated from [execution-graph.json](execution-graph.json). Proposed source contracts; "
                 "native identity, assignment, readiness and acceptance require separate receipts. "
                 "Original Russian source acceptance text is preserved verbatim where imported.", ""]
    for t in ordered:
        contracts += [f"## {t['title']} ({t['id']})", "",
                      f"**Proposal:** `{t['id']}` · **Epic:** `{t['epic_id']}` · **Russian:** {t['title_ru']}", "",
                      f"Proposed accountable: **{t['proposed_owner_role']}**; executor: **{t['proposed_executor_role']}**; "
                      f"assessor: **{t['proposed_reviewer_role']}**. These fields do not assign a native task.", "",
                      f"### Output ({t['id']})", ""]
        for o in t["outputs"]:
            contracts += [f"- `{o['id']}`: {o['description']}. Intended path: `{o['proposed_path']}`. Future output, not yet claimed as created."]
        contracts += ["", f"### Acceptance ({t['id']})", ""]
        contracts += [f"{a['number']}. {a['text']}" for a in t["acceptance_criteria"]]
        contracts += ["", f"### Evidence and adverse control ({t['id']})", ""]
        contracts += [f"- {e}" for e in t["evidence_required"]]
        contracts += [f"- Adverse case: {n['case']} Expected: {n['expected']}" for n in t["negative_controls"]]
        contracts += ["", f"### Consumed inputs ({t['id']})", ""]
        contracts += ([f"- `{d['task_id']}` → {', '.join('`'+o+'`' for o in d['consumes'])}: {d['reason']}"
                       for d in t["dependencies"]] or ["No predecessor task in this proposal; use the pinned source package."])
        if t["origin"] == "imported":
            contracts += ["", f"Source step `{t['source_step_id']}` at `{t['source_ref']}`; original status "
                          f"`{t['source_status']}` is a historical source observation, not native task state. "
                          f"Original dependencies: {', '.join(t['source_dependencies']) or 'none'}.", "",
                          "Dependency revision: " + t["dependency_revision_reason"]]
        contracts.append("")
    result = {"PROGRAMME.md": "\n".join(en), "TASK_CONTRACTS.md": "\n".join(contracts)}
    result.update(render_locale_programmes(graph, result["PROGRAMME.md"]))
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    graph = json.loads((PLAN / "execution-graph.json").read_text(encoding="utf-8"))
    for name, content in render(graph).items():
        path = PLAN / name
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                raise SystemExit(f"CW_RENDER_DRIFT: {name}")
        else:
            path.write_text(content, encoding="utf-8")
    print("CW_PROGRAMME_RENDER_OK")


if __name__ == "__main__":
    main()

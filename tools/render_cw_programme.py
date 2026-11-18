#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Render human-readable work contracts from the versioned proposal graph."""
import argparse
import json
import re
from pathlib import Path

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
          "The [Russian guide](PROGRAMME.ru.md) presents the same inventory.", "",
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

    ru = ["# Согласованная деятельность: Программа исследований и инженерных работ", "",
          "Подготовлено 18 ноября 2026 года. Это версионированное предложение для сверки и приёмки. "
          "Фактические задачи, назначения, зависимости и статусы ведутся в Мунереле.", "",
          "**23 эпика · 104 пакета работ · 247 зависимостей.** Все 72 исходных шага сохранены, добавлены 32 работы, "
          "сопоставлены все 16 предполагаемых статей и 12 гипотез. "
          "[Полная программа](PROGRAMME.md), [контракты всех работ](TASK_CONTRACTS.md) и "
          "[машиночитаемый граф](execution-graph.json) содержат условия приёмки и происхождение каждой строки.", "",
          "## Что делаем сначала", "",
          "Первый эпик — согласованный анонс направления в журнале, трёх языковых версиях дорожной карты, "
          "репозиториях и действующем графе задач Мунерела. Владелец регистрации — существующий KC-SWE; "
          "Agent-SWE обеспечивает связи, для которых нужны полномочия в смежных проектах. "
          "Публикация принятого анонса может идти параллельно регистрации задач. Завершение всего стартового "
          "эпика требует обеих проверенных квитанций.", "",
          "1. Зафиксировать исходные материалы и границы подтверждённых результатов.",
          "2. Сохранить эпики, контракты задач, граф и полноту покрытия исследования.",
          "3. Выпустить анонсы EN/RU/zh-Hans; проверить точные переводы, ссылки и фактическую видимость в браузере.",
          "4. Сверить предложения с существующими задачами, переиспользовать подходящие, создать только недостающие.",
          "5. Получить реальные UUID, владельцев, типизированные связи и обратное чтение Мунерела.",
          "6. Передать первые ограниченные пакеты работ с конкретными входами и результатами.", "",
          "## Граница исходных свидетельств", "",
          f"[Исходный пакет]({source_url}) содержит 1176 библиографических записей: 157 проверенных первичных "
          "записей и 1019 цитатных кандидатов. Число уникальных работ ещё не установлено; 26 групп совпадений "
          "названия/года и 4 пары похожих названий требуют проверки. Полных критических разборов — 0. "
          "Численный стенд r2 содержит 10 сценариев, 100 наблюдений «сценарий × период» и 190 элементарных "
          "проверок. Это ограниченное свидетельство реализации численной модели, а не эффективности агента "
          "или кадрового решения в реальной организации.", "",
          "## Реестр эпиков", "", "| Эпик | Содержание | Пакетов | Предложенные владелец / исполнитель |",
          "| --- | --- | ---: | --- |"]
    for e in graph["epics"]:
        ru.append(f"| {e['id']} | {cell(e['title'])} | {len(e['task_ids'])} | {e['proposed_owner_role']} / {e['proposed_executor_role']} |")
    ru += ["", "## Полный перечень работ", "",
           "Каждая ссылка ведёт к конкретному выходному артефакту, четырём критериям приёмки, "
           "необходимым свидетельствам, отрицательному контролю и потребляемым результатам предшественников.", "",
           "| Пакет | Работа | Предшественники |", "| --- | --- | --- |"]
    for t in ordered:
        ru.append(f"| {task_link(t['id'], tasks)} | {cell(t['title_ru'])} | {', '.join(d['task_id'] for d in t['dependencies']) or 'Исходные материалы'} |")
    ru += ["", "## Порядок и научная приёмка", "",
           "После фиксации исходников параллельно развиваются обзор, модель организации, правила данных и "
           "дизайн экспериментов. Производственный, сервисный и проектный стенды не требуют завершения друг "
           "друга. До подтверждающего сравнения обязательны применимость модели, независимый оракул и "
           "статистический план. Затем возможны теневое применение, отдельно допустимое ограниченное "
           "вмешательство и проверка переноса.", "",
           "Максимальная цепочка зависимостей изменяется с 64 узлов исходной последовательности на 17 узлов "
           "расширенного графа. Это характеристика графа, не оценка календарного ускорения. Сроки и загрузка "
           "появятся после оценки работ и реального назначения исполнителей.", "",
           "Для каждой из 16 возможных статей предусмотрены отдельные вопрос, инженерный спутник, "
           "связанные пакеты работ и собственный цикл подготовки, воспроизводимости, рецензии, выпуска и "
           "сопровождения. Полные таблицы статей и 12 опровергаемых гипотез приведены в "
           "[основной программе](PROGRAMME.md#scientific-series-and-engineering-companions). "
           "Названия статей не являются выполненными публикациями.", "",
           "Обзор требует полного критического чтения выбранных источников; формальная работа — явных "
           "предпосылок и доказательства; модельное сравнение — зарегистрированного дизайна и валидированного "
           "стенда; причинный эффект — обоснованной идентификации и фактических данных. Готовый результат "
           "одного типа не получает автоматически статус другого.", "",
           "104 строки — пакеты, а не 104 уже запущенных исполнителя. Крупные обзоры, семейства стендов и "
           "шаблоны выпуска разбиваются на ограниченные дочерние задачи. Нативная регистрация, научная "
           "приёмка, публикация на сайте, индексирование и полномочия агента требуют собственных свидетельств.", "",
           "[Порядок регистрации в Мунереле](../MUNERAL-REGISTRATION.md) сохраняет реальные границы доступа, "
           "защиту от дубликатов, историю и точное обратное чтение. Затраты и сроки этой программы пока "
           "NOT_MEASURED. Предложение не активирует платные или производственные эксперименты.", ""]

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
    return {"PROGRAMME.md": "\n".join(en), "PROGRAMME.ru.md": "\n".join(ru), "TASK_CONTRACTS.md": "\n".join(contracts)}


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

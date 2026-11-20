# SPDX-FileCopyrightText: 2026 Pavel Valentov and Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Render complete RU/zh-Hans reader programmes with explicit source bindings.

The localized programme preserves graph coverage. It does not claim to translate
the separate, much larger TASK_CONTRACTS.md or to establish independent fidelity
review. Translated source fields are checked literally before a page is emitted.
"""

import hashlib
import json
import re
from pathlib import Path


DATA_PATH = Path(__file__).with_name("cw_programme_locale_data.json")


def _cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def _task_link(key, tasks):
    heading = f"{tasks[key]['title']} ({key})".lower()
    anchor = re.sub(r"[^\w -]", "", heading).replace(" ", "-")
    return f"[{key}](TASK_CONTRACTS.md#{anchor})"


def _links(keys, tasks):
    return ", ".join(_task_link(key, tasks) for key in keys)


def _source_fields(graph):
    launch_ids = set(graph["epics"][0]["task_ids"])
    return {
        "epics": {e["id"]: e["title"] for e in graph["epics"]},
        "tasks": {t["id"]: t["title"] for t in graph["tasks"]},
        "papers": {
            p["id"]: {k: p[k] for k in (
                "source_title", "source_main_question", "source_engineering_companion")}
            for p in graph["papers"]
        },
        "hypotheses": {
            h["id"]: {k: h[k] for k in (
                "source_statement", "source_comparison", "source_refutation")}
            for h in graph["hypotheses"]
        },
        "release_contracts": {
            p["paper_id"]: {k: p[k] for k in (
                "claim_class", "claim_scope", "narrower_scope_policy")}
            for p in graph["paper_release_contracts"]
        },
        "launch_outputs": {
            t["id"]: t["outputs"][0]["description"] for t in graph["tasks"]
            if t["id"] in launch_ids
        },
    }


def _validate_localizations(graph, data):
    if data.get("schema") != "cw-programme-localizations/1":
        raise ValueError("CW_LOCALE_SCHEMA: unsupported localization data")
    actual = _source_fields(graph)
    if data.get("source_fields") != actual:
        changed = sorted(k for k in actual if data.get("source_fields", {}).get(k) != actual[k])
        raise ValueError("CW_LOCALE_SOURCE_DRIFT: " + ", ".join(changed))
    if set(data["locales"]) != {"ru", "zh-Hans"}:
        raise ValueError("CW_LOCALE_COVERAGE: expected ru and zh-Hans")
    expected = {
        "papers": set(actual["papers"]),
        "hypotheses": set(actual["hypotheses"]),
        "release_scopes": set(actual["release_contracts"]),
        "launch_outputs": set(actual["launch_outputs"]),
    }
    for locale, translated in data["locales"].items():
        for category, ids in expected.items():
            if set(translated.get(category, {})) != ids:
                raise ValueError(f"CW_LOCALE_COVERAGE: {locale}/{category}")
        for category in ("papers", "hypotheses"):
            fields = ("title", "question", "companion") if category == "papers" else (
                "statement", "comparison", "refutation")
            for key, row in translated[category].items():
                if set(row) != set(fields) or any(
                        not isinstance(row[f], str) or not row[f].strip() for f in fields):
                    raise ValueError(f"CW_LOCALE_EMPTY_FIELD: {locale}/{category}/{key}")
        for category in ("release_scopes", "launch_outputs"):
            if any(not isinstance(v, str) or not v.strip() for v in translated[category].values()):
                raise ValueError(f"CW_LOCALE_EMPTY_FIELD: {locale}/{category}")
    zh = data["locales"]["zh-Hans"]
    for category in ("tasks", "epics"):
        if set(zh.get(category, {})) != set(actual[category]):
            raise ValueError(f"CW_LOCALE_COVERAGE: zh-Hans/{category}")
        if any(not isinstance(v, str) or not v.strip() for v in zh[category].values()):
            raise ValueError(f"CW_LOCALE_EMPTY_FIELD: zh-Hans/{category}")
    if len(graph["tasks"]) != len(actual["tasks"]) or len(graph["epics"]) != len(actual["epics"]):
        raise ValueError("CW_LOCALE_DUPLICATE_ID")
    if set(actual["release_contracts"]) != set(actual["papers"]):
        raise ValueError("CW_LOCALE_RELEASE_COVERAGE")


TEXT = {
    "ru": {
        "title": "Согласованная деятельность: программа исполнения и научных результатов",
        "status": "Подготовлено 18 ноября 2026 года. Статус: **исходное предложение для сверки и рецензирования**. Фактические идентификаторы задач, назначения, зависимости и состояния исполнения определяются в Muneral.",
        "binding": "Эта русская читательская версия подготовлена авторской стороной и привязана к точным байтам [английской программы](PROGRAMME.md). Она включает все эпики, пакеты, статьи, гипотезы и условия выпуска. Независимая проверка точности перевода, в том числе носителем языка, не заявляется. Ссылки на [полные контракты задач](TASK_CONTRACTS.md) ведут к отдельному исходному документу на английском с сохранёнными русскими исходными критериями; этот документ здесь не объявляется полностью переведённым.",
        "inventory": "Программа содержит **{epics} эпика, {tasks} пакета работ и {edges} блокирующих зависимостей с потреблением результатов**. Сохранены все **{imported} исходных шагов**, добавлены **{added} пакета**, сопоставлены **{papers} возможных статей и {hypotheses} гипотез**. [Машиночитаемый граф](execution-graph.json) и полные контракты задают предлагаемую область регистрации.",
        "packages": "Это пакеты работ: крупные обзоры, семейства стендов и шаблоны публикации нужно разбить на ограниченные дочерние задачи перед исполнением. Предложенный владелец не является фактическим назначением. Подготовленные {objects} объектов программы, эпиков и пакетов не означают {objects} созданных задач Muneral.",
        "evidence_heading": "Исходные свидетельства и предполагаемый вклад",
        "evidence": "[Исходный исследовательский пакет]({source_url}) сохраняет {records} библиографических записей: {checked} проверенных первичных записей и {candidates} цитатных кандидатов. Число уникальных работ не установлено: требуется разобрать 26 групп с совпадающими названием и годом и четыре пары близких названий. Завершённых критических оценок полных текстов — {appraisals}. Сохранённый численный пример r{revision} включает {scenarios} сценариев, {periods} наблюдений «сценарий × период» и {checks} элементарных проверок; зарегистрировано {violations} нарушений. Это ограниченное свидетельство численной реализации, а не эффективности агента, оптимизатора или валидности для реальной организации.",
        "contribution": "Предполагаемый вклад — организационный профиль, связывающий потребности, сети работы, различающуюся семантику ресурсов, компетенции и свидетельства для решений с Agent Situation и Context Assembly. Новизну ещё нужно проверить относительно существующих исследований. Введение профиля не создаёт новый нативный вид артефакта KC и не предоставляет полномочий исполнения.",
        "launch_heading": "Первый эпик: сделать программу видимой и исполнимой",
        "launch": "CW-EP00 включает фиксацию источников, устав программы, граф, анонсы Journal на EN/RU/zh-Hans, навигацию репозитория и дорожной карты, сверку нативных задач, проверенную публичную доставку и ограниченную передачу коллективу. Принятый анонс может быть опубликован, пока регистрация задач ещё выполняется; закрытие полного этапа CW-N08 требует обеих квитанций — публикации и регистрации.",
        "launch_columns": "| Пакет | Наблюдаемый результат | Предложенные ответственный / исполнитель | Блокирующие входы |",
        "source_only": "Только исходные материалы",
        "launch_gates": "Приёмка запуска требует точных привязок исходников и переводов, прав и атрибуции, независимой рецензии в заявленном объёме, проверок в CI, явной ревизии для отката, штатного процесса публикации и анонимного обратного чтения страниц. Браузерная проверка должна показать, что сама статья видна на компьютере и телефоне, а переключение языка сохраняет выпуск. Метаданные и лексический анализ HTML не устанавливают эти свойства.",
        "sequence_heading": "Параллельная последовательность работ",
        "diagram_note": "Схема ниже — обзор, а не полный граф из {edges} рёбер. Каждая действительная блокирующая зависимость в JSON указывает, какой результат предшественника она потребляет.",
        "diagram": ["Источники и программа", "Анонс и сверка задач", "Обзор и утверждения", "Модели, схемы и протоколы", "Производственный стенд", "Сервисный стенд", "Проектный стенд", "Валидированные сравнения", "Допустимое теневое применение", "Ограниченная полевая оценка", "Выпуск по типу утверждения"],
        "sequence": [
            "**Запуск и сверка.** Зафиксировать источники и свидетельства, опубликовать точное описание программы, сверить существующие задачи Muneral и подготовить ограниченную первую очередь.",
            "**Параллельные основания.** Критически читать первичные источники, определять потребности, ресурсы и рабочие графы, строить схему происхождения, правила прав и данных, регистрировать вопросы отдельных исследований.",
            "**Параллельные предметные стенды.** Производственный, сервисный и проектный стенды начинают работу после получения собственных обязательных входов. До подтверждающих сравнений нужны независимые оракулы и проверки применимости моделей.",
            "**Контролируемые свидетельства.** Сравнивать действующий метод, сильные методы исследования операций, агента без поиска, сильный обычный RAG и полный профиль KC при заявленных сопоставимых бюджетах; сохранять абляции, неудачи и неопределённость.",
            "**Допустимое реальное применение.** Привязать действительную задачу и реализацию Arcanada, собрать теневые наблюдения, затем провести отдельно разрешённое ограниченное вмешательство и проверку переноса на отложенные случаи.",
            "**Выпуск по утверждению.** Рецензированная карта источников, условное доказательство и причинный эффект в организации имеют разные обязательства по свидетельствам. Обзор или формальный результат не ждёт всеобщего полевого испытания; причинное утверждение требует подходящего дизайна идентификации и фактических данных.",
        ],
        "topology": "[Решения о зависимостях](DEPENDENCY-DECISIONS.md) сохраняют историю исходных рёбер и обоснование изменений. Максимальная исходная цепочка содержит {old_chain} узла, предлагаемая — {new_chain}. Это число узлов топологической цепочки, а не дни, трудозатраты или доказанное ускорение. Доступные мощности, время рецензентов и длительности нужно установить при нативной сверке. Используется существующий коллектив из шести ролей; строки задач не создают дополнительных агентов.",
        "epics_heading": "Реестр эпиков",
        "epics_columns": "| Эпик | Область | Пакетов | Предложенные ответственный / исполнитель |",
        "tasks_heading": "Полный перечень пакетов работ",
        "tasks_intro": "Каждый связанный контракт задаёт нумерованные критерии приёмки, точный предлагаемый результат, необходимые свидетельства, отрицательный контроль, покрытие источника, рецензента и потребляемые результаты предшественников.",
        "tasks_columns": "| Пакет | Работа | Эпик | Блокирующие предпосылки |",
        "no_dependencies": "Нет в этом предложении",
        "papers_heading": "Научная серия и инженерные работы",
        "papers_intro": "Это предлагаемые границы работ, а не завершённые или принятые статьи. Окончательное разделение зависит от результатов исследования. Для каждого артефакта создаются собственные экземпляры CW-I03–CW-I08 с его источниками, результатами, рецензиями и свидетельствами выпуска.",
        "papers_columns": "| Возможная статья | Исследовательский вопрос | Инженерная работа | Основные пакеты |",
        "release_heading": "Условия выпуска каждой статьи",
        "release_intro": "В графе явно заданы {contracts} контрактов выпуска с {release_edges} связями необходимых свидетельств. Они образуют {instances} шаблонов экземпляров публикации и {stages} узлов стадий выпуска; эти числа учитываются отдельно от {tasks} пакетов и {edges} рёбер основного графа. Созданных нативных экземпляров выпуска в этом предложении — {native}. Одна ссылка на пакет или общее описание шаблона не удовлетворяет условию выпуска: нужны точный потребляемый результат и принятое свидетельство в соответствующем экземпляре.",
        "release_columns": "| Статья | Область допустимого утверждения | Обязательные свидетельства |",
        "release_boundary": "Для заявленных организационных эффектов CW-P09 и CW-P13, а также переноса наблюдаемых вмешательств CW-P15, обязателен результат CW-H08. Удаление этой зависимости должно отклонять выпуск, в том числе выпуск CW-P13. CW-N28 использует версионированные входы CW-H06 и CW-N16 до собственного результата, а не результаты будущей публикации. Обзорные и формальные работы не получают универсального требования H08. Для более узкого результата нужен отдельный рецензированный контракт без утверждения об организационном эффекте; молча удалять полевой барьер нельзя. У всех шестнадцати работ остаётся собственная цепочка CW-I03–CW-I08.",
        "hypotheses_heading": "Гипотезы и возможное опровержение",
        "hypotheses_intro": "Каждая гипотеза связана с предварительной регистрацией CW-H01, статистическим дизайном CW-N20 и своими предметными пакетами. Все исходы остаются неизвестными. Отсутствие данных не считается подтверждением.",
        "hypotheses_columns": "| Гипотеза | Сравнение | Что опровергнет или ограничит утверждение | Связанные пакеты |",
        "gates_heading": "Условия исполнения и требования к свидетельствам",
        "gates_intro": "[Порядок регистрации Muneral](../MUNERAL-REGISTRATION.md) задаёт сверку областей работ, реального родителя и владельцев, создание без дубликатов через проверку уже существующих записей и точное обратное чтение зависимостей. Подготовительный инструмент создаёт шаблоны и не отправляет HTTP-запросов. Неполная видимость не доказывает отсутствие задач.",
        "evidence_rules": [
            "Литературные и обзорные утверждения требуют фактического критического чтения полных текстов и проверки покрытия источников; импортированный библиографический корпус этого ещё не даёт.",
            "Формальные утверждения требуют явных предпосылок и доказательств; конечные примеры не доказывают неограниченную теорему.",
            "Модельные сравнения требуют CW-H01, соответствующих CW-H02/CW-H03/CW-H04, CW-N17/CW-N18, CW-H05/CW-H06 и CW-N20.",
            "Организационные причинные эффекты дополнительно требуют CW-E06/CW-F06, CW-N29 и CW-H08; изменение графа не отменяет эти обязательства.",
            "Утверждения о теневом применении требуют точной связи потребителя, входов, реализации и наблюдаемого исхода по CW-N26/CW-N27 и CW-H07; создание задачи или синтетический пример не заменяет её.",
            "Программа не предоставляет новый вид нативного артефакта, допуск среды исполнения, научное принятие, право найма или право выполнения действий.",
            "При запуске анонсируются предполагаемые статьи и исследования. Карточки не регистрируются в каталоге как завершённые публикации.",
        ],
        "identities": "Версии источников, данных и кода, попытки, утверждения, вердикты и события исполнения имеют отдельные идентификаторы. Сохраняются противоречивые свидетельства; явно проверяются пустые множества возможных миров, недостаточные полномочия, недоступные ресурсы и неудачные либо частичные последствия. Пакет знаний, описывающий разрешение, не выдаёт его. До использования проверяются текущий допуск задачи, применимые права на данные и бюджет эксперимента.",
        "costs": "Полная стоимость включает оценку источников, разметку, человеческую рецензию, модели и инструменты, неудачные попытки и сопровождение. Стоимость программы и сроки доставки пока NOT_MEASURED. План не активирует эмпирические эксперименты. Проверка коллегой-ассистентом не является внешним независимым научным принятием; новый эксперимент, статья, внешняя задача, выкладка или операционное действие здесь не объявляются завершёнными.",
        "reproduce_heading": "Воспроизведение проверок предложения",
        "reproduce_limit": "Эти команды проверяют согласованность исходного предложения, воспроизводимость его представления и заявленные отрицательные случаи. Они не устанавливают научную истинность, точность перевода, нативную регистрацию, публикацию или эффект в организации.",
    },
    "zh-Hans": {
        "title": "协调工作：执行方案与研究成果交付",
        "status": "编制日期：2026 年 11 月 18 日。状态：**供核对与评审的来源提案**。实际任务身份、分派、依赖与执行状态以 Muneral 为准。",
        "binding": "本简体中文阅读版本由作者一方准备，并绑定到[英语方案](PROGRAMME.md)的精确字节。它覆盖全部史诗级任务、工作包、论文、假设与发布条件。不宣称已通过独立翻译忠实性评审或母语使用者评审。[完整任务契约](TASK_CONTRACTS.md)的链接指向另一个英语来源文档，其中保留了原始俄语验收条款；本页不宣称该契约文档已经完整翻译。",
        "inventory": "方案包含 **{epics} 个史诗级任务、{tasks} 个工作包，以及 {edges} 条消费前置成果的阻塞依赖**。保留全部 **{imported} 个原始步骤**，补充 **{added} 个工作包**，并关联 **{papers} 篇潜在论文与 {hypotheses} 个假设**。[机器可读图](execution-graph.json)与完整任务契约界定拟登记的范围。",
        "packages": "这些条目是工作包。大型综述批次、实验平台族与出版模板必须在分派前拆成有界子任务。拟议负责人不等于已获实际分派。为核对准备的 {objects} 个方案、史诗级任务与工作包对象，不等于已创建 {objects} 个 Muneral 对象。",
        "evidence_heading": "现有证据与拟议贡献",
        "evidence": "[初始研究资料包]({source_url})保留 {records} 条参考文献记录：{checked} 条已核验原始记录与 {candidates} 条引文候选记录。独立文献数量仍未确定：26 组同标题同年份记录以及四对近似标题仍待身份核查。已完成的全文批判性评价为 {appraisals} 项。保留的 r{revision} 数值示例包含 {scenarios} 个情景、{periods} 个“情景×时段”观测和 {checks} 项基础检查，记录到 {violations} 次违反。这些结果仅支持有界数值实现结论，不能证明智能体或优化器有效，也不能证明模型适用于真实组织。",
        "contribution": "拟议贡献是一种组织领域配置：把需求、工作网络、不同资源语义、胜任能力与决策证据关联到 Agent Situation 和 Context Assembly。创新性仍须与既有研究比较。引入领域配置不会创建新的 KC 原生制品类型，也不会授予执行权限。",
        "launch_heading": "首个史诗级任务：使方案可见并可落实",
        "launch": "CW-EP00 包括来源冻结、方案章程、任务图、EN/RU/zh-Hans Journal 公告、路线图与仓库导航、原生任务核对、经核验的公开交付，以及向集体移交有界工作。公告在获准后可以先行发布，即使原生任务登记仍未完成；完整启动交接 CW-N08 只有在同时取得发布与登记回执后才能关闭。",
        "launch_columns": "| 工作包 | 可观察成果 | 拟议负责人 / 执行方 | 阻塞输入 |",
        "source_only": "仅来源输入",
        "launch_gates": "启动验收需要精确的来源与翻译绑定、权利与署名检查、在声明范围内的独立评审、托管 CI 核验、明确的回滚版本、正式发布流程，以及匿名读回实际页面。浏览器检查必须确认桌面与手机上能够看到文章正文，并确认切换语言后仍是同一期内容。元数据或 HTML 词法检查不能证明这些属性。",
        "sequence_heading": "并行交付顺序",
        "diagram_note": "下图仅是概览，并非包含 {edges} 条边的完整权威图。JSON 中的每条实际阻塞依赖都说明其消费哪项前置成果。",
        "diagram": ["冻结来源与方案", "公告与任务核对", "来源评审与论断", "模型、模式与协议", "制造实验平台", "服务实验平台", "项目实验平台", "已验证的受控比较", "符合条件的影子使用", "有界实地评估", "按论断发布科学成果"],
        "sequence": [
            "**启动与核对。** 冻结来源和证据，发布准确的方案说明，核对既有 Muneral 工作，并准备首批有界任务。",
            "**并行基础工作。** 评审原始来源，定义需求、资源与工作图，建立来源模式，规定权利与数据契约，并登记各项研究的问题。",
            "**并行领域平台。** 制造、服务和项目平台在获得各自必要输入后开展。确认性比较之前必须完成独立判定基准与模型有效性检查。",
            "**受控证据。** 在声明的匹配预算下，比较当前方法、强运筹学方法、不检索的智能体、强普通 RAG 与完整 KC 配置；保留消融、失败与不确定性。",
            "**符合条件的真实使用。** 绑定真实的 Arcanada 任务与实现，收集影子证据，再开展另行获准的有界干预和留出迁移评估。",
            "**按论断发布。** 经评审的来源图谱、条件证明与组织因果效应具有不同证据义务。文献或形式化结果不必等待全局实地试验；因果效应论断仍须具有适当的识别设计与实际数据。",
        ],
        "topology": "[依赖关系决策](DEPENDENCY-DECISIONS.md)保留原始边的历史并解释修订。原始最长依赖链为 {old_chain} 个任务节点，提议图为 {new_chain} 个节点。这是拓扑节点数量，不是天数、工作量估计或已证明的提速。原生核对时还须明确产能、评审人员可用时间与持续时间。复用现有六角色集体；任务行不会创建额外智能体。",
        "epics_heading": "史诗级任务登记表",
        "epics_columns": "| 史诗级任务 | 范围 | 工作包数 | 拟议负责人 / 执行方 |",
        "tasks_heading": "完整工作包清单",
        "tasks_intro": "每个链接指向的契约都记录编号验收标准、明确的拟议成果、所需证据、负向对照、来源覆盖、评审方，以及消费的前置成果。",
        "tasks_columns": "| 工作包 | 工作 | 所属史诗级任务 | 阻塞前提 |",
        "no_dependencies": "本提案中没有前置任务",
        "papers_heading": "科学系列与配套工程工作",
        "papers_intro": "这些是候选研究边界，并非已完成或已获认可的论文。最终划分取决于研究结果。每项制品均须实例化自己的 CW-I03–CW-I08，并绑定其来源、结果、评审与发布证据。",
        "papers_columns": "| 候选论文 | 研究问题 | 配套工程工作 | 主要工作包 |",
        "release_heading": "逐篇论文的发布条件",
        "release_intro": "图中明确给出 {contracts} 份发布契约及 {release_edges} 条必要证据连接。它们形成 {instances} 个论文发布实例模板和 {stages} 个发布阶段节点；这些数量与基础图中的 {tasks} 个工作包、{edges} 条边分别统计。本提案创建的原生发布实例为 {native} 个。仅有覆盖链接或通用模板不能满足发布条件：相应实例必须消费精确成果及已接受的证据。",
        "release_columns": "| 论文 | 允许提出论断的范围 | 必需证据 |",
        "release_boundary": "CW-P09、CW-P13 所声明的组织效应，以及 CW-P15 中观测干预结果的迁移，均必须取得 CW-H08 的结果。移除该依赖必须使发布被拒绝，其中包括缺少 H08 的 CW-P13 发布。CW-N28 在产生自身结果前消费 CW-H06 和 CW-N16 的版本化输入，而不是等待未来出版的结果。综述与形式化工作不一律要求 H08。更窄的结果必须取得另一份经评审且不声称组织效应的契约，不能悄悄删除实地评估条件。十六篇论文各自保留 CW-I03–CW-I08 发布链。",
        "hypotheses_heading": "假设与可能的反驳",
        "hypotheses_intro": "每个假设均关联 CW-H01 预登记、CW-N20 统计设计及其领域工作包。全部结果仍未知；数据缺失不算确认。",
        "hypotheses_columns": "| 假设 | 比较 | 能反驳或限制论断的结果 | 关联工作包 |",
        "gates_heading": "执行与证据条件",
        "gates_intro": "[Muneral 登记流程](../MUNERAL-REGISTRATION.md)规定范围核对、真实父任务与负责方绑定、通过核对已有记录避免重复创建，以及精确依赖读回。离线准备工具只生成模板，不发送 HTTP 请求。部分可见性不能证明工作不存在。",
        "evidence_rules": [
            "文献与综述论断需要实际全文批判性评价和经评审的来源覆盖；导入的参考文献库尚不满足这一要求。",
            "形式化论断需要明确假设与证明；有限示例不能证明不受限制的定理。",
            "仿真比较需要 CW-H01、适用的 CW-H02/CW-H03/CW-H04、CW-N17/CW-N18、CW-H05/CW-H06 及 CW-N20 回执。",
            "组织因果效应还需要 CW-E06/CW-F06、CW-N29 与 CW-H08；重写任务图不会免除这些义务。",
            "影子使用论断需要通过 CW-N26/CW-N27 与 CW-H07 精确绑定使用方、输入、实现与观察结果；任务创建或合成测试样例不足以替代。",
            "本方案不授予新的原生类型、运行时准入、出版认可、招聘权或执行权。",
            "启动时公告的是拟议论文与研究。研究卡片不能以已完成论文身份加入出版目录。",
        ],
        "identities": "来源、数据与代码版本，尝试、论断、判定以及执行事件分别标识。保留互相矛盾的证据，并明确检查空的可能世界集合、权限不足、资源不可用以及失败或部分生效的结果。描述权限的知识包不会授予该权限。使用前须检查当前任务准入、适用数据权利及实验预算。",
        "costs": "完整成本应包括来源评价、标注、人工评审、模型与工具、失败尝试及维护。当前方案成本与交付日期仍为 NOT_MEASURED；规划制品不会激活实证实验。同一控制方的助手评审不是外部独立科学认可；这里不宣称任何新实验、论文、外部任务、部署或实际操作已经完成。",
        "reproduce_heading": "复现提案检查",
        "reproduce_limit": "这些命令检查来源提案的一致性、呈现的可复现性与声明的负向案例。它们不能证明科学结论为真、翻译忠实、原生登记成功、已发布或产生组织效应。",
    },
}


def _graph_metrics(graph):
    tasks = {t["id"]: t for t in graph["tasks"]}
    depths = {}

    def depth(key, visiting):
        if key in visiting:
            raise ValueError("CW_LOCALE_CYCLE")
        if key not in depths:
            depths[key] = 1 + max((depth(d["task_id"], visiting | {key})
                                   for d in tasks[key]["dependencies"]), default=0)
        return depths[key]

    return {
        "epics": len(graph["epics"]), "tasks": len(tasks),
        "edges": sum(len(t["dependencies"]) for t in tasks.values()),
        "imported": sum(t["origin"] == "imported" for t in tasks.values()),
        "added": sum(t["origin"] != "imported" for t in tasks.values()),
        "papers": len(graph["papers"]), "hypotheses": len(graph["hypotheses"]),
        "objects": 1 + len(graph["epics"]) + len(tasks),
        "old_chain": graph["source_graph_metrics"]["longestTaskCount"],
        "new_chain": max((depth(key, set()) for key in tasks), default=0),
    }


def render_localized_programme(graph, locale, english_sha256, data=None):
    """Render one locale; fail closed for missing or stale translated source fields."""
    if locale not in TEXT:
        raise ValueError("CW_LOCALE_UNKNOWN: " + locale)
    if not re.fullmatch(r"[0-9a-f]{64}", english_sha256):
        raise ValueError("CW_LOCALE_SOURCE_DIGEST")
    data = data if data is not None else json.loads(DATA_PATH.read_text(encoding="utf-8"))
    _validate_localizations(graph, data)
    tr = data["locales"][locale]
    text = TEXT[locale]
    tasks = {t["id"]: t for t in graph["tasks"]}
    ordered_ids = [key for epic in graph["epics"] for key in epic["task_ids"]]
    if len(ordered_ids) != len(tasks) or set(ordered_ids) != set(tasks):
        raise ValueError("CW_LOCALE_EPIC_MEMBERSHIP")
    metrics = _graph_metrics(graph)
    baseline = graph["evidence_baseline"]
    source_url = ("https://github.com/Arcanada-one/knowledge-contract/tree/"
                  + graph["source"]["head"] + "/roadmap/coordinated-work")

    def title(key):
        return tasks[key]["title_ru"] if locale == "ru" else tr["tasks"][key]

    lines = ["---", f"language: {locale}", "source_path: PROGRAMME.md",
             f"source_sha256: {english_sha256}",
             "translation_status: author-prepared",
             "independent_fidelity_review: not_recorded", "---", "",
             "# " + text["title"], "", text["status"], "", text["binding"], "",
             text["inventory"].format(**metrics), "", text["packages"].format(**metrics), "",
             "## " + text["evidence_heading"], "",
             text["evidence"].format(
                 source_url=source_url, records=baseline["retained_records"],
                 checked=baseline["initial_checked_bibliographic_records"],
                 candidates=baseline["additional_citation_candidates"],
                 appraisals=baseline["full_text_critical_appraisals"],
                 revision=baseline["reported_probe_revision"],
                 scenarios=baseline["reported_probe_scenarios"],
                 periods=baseline["reported_probe_periods"],
                 checks=baseline["reported_probe_checks"],
                 violations=baseline["reported_probe_violations"]), "", text["contribution"], "",
             "## " + text["launch_heading"], "", text["launch"], "",
             text["launch_columns"], "| --- | --- | --- | --- |"]
    for key in graph["epics"][0]["task_ids"]:
        task = tasks[key]
        deps = _links([d["task_id"] for d in task["dependencies"]], tasks) or text["source_only"]
        lines.append(f"| {_task_link(key, tasks)} — {_cell(title(key))} | "
                     f"{_cell(tr['launch_outputs'][key])} | {task['proposed_owner_role']} / "
                     f"{task['proposed_executor_role']} | {deps} |")
    lines += ["", text["launch_gates"], "", "## " + text["sequence_heading"], "",
              text["diagram_note"].format(**metrics), "", "```mermaid", "flowchart TD"]
    labels = text["diagram"]
    for idx, label in enumerate(labels):
        lines.append(f'  {chr(65 + idx)}["{label}"]')
    lines += ["  A --> B", "  A --> C", "  C --> D", "  D --> E", "  D --> F", "  D --> G",
              "  E --> H", "  F --> H", "  G --> H", "  H --> I", "  I --> J",
              "  C --> K", "  H --> K", "  J --> K", "```", ""]
    lines += [f"{n}. {paragraph}" for n, paragraph in enumerate(text["sequence"], start=1)]
    lines += ["", text["topology"].format(**metrics), "", "## " + text["epics_heading"], "",
              text["epics_columns"], "| --- | --- | ---: | --- |"]
    for epic in graph["epics"]:
        epic_title = epic["title"] if locale == "ru" else tr["epics"][epic["id"]]
        lines.append(f"| {epic['id']} | {_cell(epic_title)} | {len(epic['task_ids'])} | "
                     f"{epic['proposed_owner_role']} / {epic['proposed_executor_role']} |")
    lines += ["", "## " + text["tasks_heading"], "", text["tasks_intro"], "",
              text["tasks_columns"], "| --- | --- | --- | --- |"]
    for key in ordered_ids:
        task = tasks[key]
        deps = _links([d["task_id"] for d in task["dependencies"]], tasks) or text["no_dependencies"]
        lines.append(f"| {_task_link(key, tasks)} | {_cell(title(key))} | {task['epic_id']} | {deps} |")
    lines += ["", "## " + text["papers_heading"], "", text["papers_intro"], "",
              text["papers_columns"], "| --- | --- | --- | --- |"]
    for paper in graph["papers"]:
        row = tr["papers"][paper["id"]]
        lines.append(f"| {paper['id']} — {_cell(row['title'])} | {_cell(row['question'])} | "
                     f"{_cell(row['companion'])} | {_links(paper['mapped_task_ids'], tasks)} |")
    release = graph["paper_release_metrics"]
    lines += ["", "## " + text["release_heading"], "",
              text["release_intro"].format(
                  **metrics, contracts=release["contracts"], release_edges=release["required_evidence_edges"],
                  instances=release["release_instance_templates"], stages=release["release_stage_nodes"],
                  native=release["native_release_instances_created"]), "",
              text["release_columns"], "| --- | --- | --- |"]
    for contract in graph["paper_release_contracts"]:
        gate_ids = [gate["task_id"] for gate in contract["required_gates"]]
        lines.append(f"| {contract['paper_id']} | {_cell(tr['release_scopes'][contract['paper_id']])} | "
                     f"{_links(gate_ids, tasks)} |")
    lines += ["", text["release_boundary"], "", "## " + text["hypotheses_heading"], "",
              text["hypotheses_intro"], "", text["hypotheses_columns"], "| --- | --- | --- | --- |"]
    for hypothesis in graph["hypotheses"]:
        row = tr["hypotheses"][hypothesis["id"]]
        lines.append(f"| {hypothesis['id']} — {_cell(row['statement'])} | {_cell(row['comparison'])} | "
                     f"{_cell(row['refutation'])} | {_links(hypothesis['mapped_task_ids'], tasks)} |")
    lines += ["", "## " + text["gates_heading"], "", text["gates_intro"], ""]
    lines += ["- " + rule for rule in text["evidence_rules"]]
    lines += ["", text["identities"], "", text["costs"], "",
              "## " + text["reproduce_heading"], "", "```sh",
              "python3 -B tools/check_cw_programme.py",
              "python3 -B tools/render_cw_programme.py --check",
              "python3 -B -m unittest tools.test_check_cw_programme tools.test_prepare_cw_registration -v",
              "python3 -O -B -m unittest tools.test_check_cw_programme tools.test_prepare_cw_registration -v",
              "```", "", text["reproduce_limit"], ""]
    return "\n".join(lines)


def render_locale_programmes(graph, english_text):
    """Return both locale files, bound to the final English programme bytes."""
    digest = hashlib.sha256(english_text.encode("utf-8")).hexdigest()
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    return {f"PROGRAMME.{locale}.md": render_localized_programme(graph, locale, digest, data)
            for locale in ("ru", "zh-Hans")}

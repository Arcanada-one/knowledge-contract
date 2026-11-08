#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Knowledge Contract Arcana contributors
# SPDX-License-Identifier: Apache-2.0
"""Deterministic editorial migration; default is read-only. No network, task or publication operations."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

BASE = 'a0450428704fcd41b411203f2fc88c06c779610b'
BRANCH = 'editorial/readable-names-and-roadmap-20261108'
ROOT = Path(__file__).resolve().parents[1]
REGISTRY = 'reference/document-naming/names.json'
WORK = 'roadmap/workstreams.json'


def git(*args: str) -> str:
    return subprocess.check_output(['git', *args], cwd=ROOT).decode('utf-8', errors='strict')


def original(path: str) -> str:
    return git('show', BASE + ':' + path)


def current(path: str) -> str:
    return (ROOT / path).read_text(encoding='utf-8')


def dumped(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + '\n'


def digest(value: str) -> str:
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


def display_parts(short: str, explanation: str) -> tuple[str, str]:
    """Keep explanatory scope, without repeating an already existing short label."""
    subtitle = explanation
    allowed = {short.casefold()}
    extra = {'Contract Core': 'Knowledge Contract', 'Context Package': 'Context Packages',
             'Contract Checks': 'Contract profiles', 'Ядро контракта': 'Контракт знаний',
             'Пакет контекста': 'Пакеты контекста',
             'Политика повторного использования': 'Повторное использование'}
    if short in extra:
        allowed.add(extra[short].casefold())
    prefix, separator, remainder = explanation.partition(': ')
    if separator and prefix.casefold() in allowed:
        subtitle = remainder
    else:
        for join in (', ', ' and ', ' и '):
            leading = short + join
            if explanation.casefold().startswith(leading.casefold()):
                subtitle = explanation[len(leading):]
                break
    if not subtitle.strip():
        raise ValueError('An explanatory subtitle is required')
    if subtitle != explanation and subtitle.count(',') == 1 and ', and ' in subtitle:
        subtitle = subtitle.replace(', and ', ' and ', 1)
    subtitle = subtitle[0].upper() + subtitle[1:]
    return short + ': ' + subtitle, subtitle


def anchor(title: str) -> str:
    text = re.sub(r'[^\w\s.-]', '', title.casefold())
    text = re.sub(r'\s+', '-', text.strip())
    return re.sub(r'^[^a-zA-Z]+', '', text)


def alias(value: str) -> str:
    # Narrow style exception for a validated compatibility anchor, not arbitrary HTML.
    if not re.fullmatch(r'[a-z0-9_.-]+', value):
        raise ValueError('Unsafe compatibility anchor: ' + value)
    return '<!-- markdownlint-disable-next-line MD033 -->\n<a id="' + value + '"></a>\n\n'


def validate_rows(rows: list, slugs: set[str]) -> None:
    if not isinstance(rows, list) or len(rows) != len(slugs):
        raise ValueError('Name register must cover the exact catalogue')
    seen = [set(), set(), set()]
    identities = set()
    for row in rows:
        if not isinstance(row, list) or len(row) != 6 or not all(isinstance(v, str) and v.strip() for v in row):
            raise ValueError('Invalid name row')
        slug, en, ru, ru_sub, zh, zh_sub = row
        if slug in identities or slug not in slugs:
            raise ValueError('Duplicate or unknown slug: ' + slug)
        identities.add(slug)
        for value in (en, ru):
            if not 1 <= len(value.split()) <= 3 or ':' in value or re.search(r'\b(?:RM-?\d+|F\d+|G\d+)\b', value):
                raise ValueError('Short name must be one to three meaningful words: ' + value)
        if not 2 <= len(zh) <= 12 or '：' in zh:
            raise ValueError('Chinese short name is not a compact phrase')
        for index, value in enumerate((en, ru, zh)):
            key = value.casefold()
            if key in seen[index]:
                raise ValueError('Duplicate short name: ' + value)
            seen[index].add(key)
    if identities != slugs:
        raise ValueError('Incomplete name coverage')


def rename_document(raw: str, old: str, short: str) -> str:
    full, subtitle = display_parts(short, old)
    header_alias = '' if full == old else alias(anchor(old))
    title_lines = re.findall(r'^title:.*$', raw, flags=re.M)
    old_h1 = '# ' + old
    if len(title_lines) != 1 or raw.count('\n' + old_h1 + '\n') != 1:
        raise ValueError('Unexpected original title or H1')
    if json.loads(title_lines[0].split(':', 1)[1].strip()) != old:
        raise ValueError('Original front matter differs from catalogue')
    new_meta = 'title: ' + json.dumps(full, ensure_ascii=False) + '\nshort_title: ' + json.dumps(short, ensure_ascii=False) + '\nsubtitle: ' + json.dumps(subtitle, ensure_ascii=False) + '\nprevious_title: ' + json.dumps(old, ensure_ascii=False)
    result = raw.replace(title_lines[0], new_meta, 1)
    result = result.replace('\n' + old_h1 + '\n', '\n' + header_alias + '# ' + full + '\n', 1)
    # Inverting the exact header-only change must reproduce every original byte.
    restored = result.replace(new_meta, title_lines[0], 1).replace('\n' + header_alias + '# ' + full + '\n', '\n' + old_h1 + '\n', 1)
    if restored != raw:
        raise ValueError('Scientific body was altered')
    return result


def humanize(text: str, labels: dict[str, str]) -> str:
    # Literal code blocks retain technical spelling. Reader-facing labels are names.
    lines, fenced = [], False
    for line in text.splitlines():
        if line.lstrip().startswith('```'):
            fenced = not fenced
        if not fenced:
            old = line
            for key, label in sorted(labels.items(), key=lambda item: -len(item[0])):
                line = re.sub(r'(?<![A-Za-z0-9_-])' + re.escape(key) + r'(?![A-Za-z0-9_-])', label, line)
            if old.startswith('#') and old != line:
                old_anchor = anchor(old.lstrip('# ').strip())
                if old_anchor:
                    lines.append(alias(old_anchor).rstrip())
                    lines.append('')
        lines.append(line)
    return '\n'.join(lines) + '\n'


def build() -> tuple[dict[str, str], dict]:
    catalogue = json.loads(original('publication-catalog.json'))
    rows = json.loads(current(REGISTRY))['documents']
    docs = catalogue['documents']
    validate_rows(rows, {d['slug'] for d in docs})
    if len(docs) != 30:
        raise ValueError('This migration is pinned to exactly 30 source documents')
    names = {r[0]: r for r in rows}
    work = json.loads(current(WORK))
    tasks = work['workstreams']
    labels = {row[0]: row[1] for row in tasks}
    labels.update({row[0]: row[1] for row in work['foundations']})
    labels.update({row[0].replace('RM-', 'RM'): row[1] for row in tasks})
    labels.update({'P0': 'Immediate', 'P1': 'Next', 'P2': 'Expansion'})
    out: dict[str, str] = {}
    receipt = {'schema': 'knowledge-contract.naming-migration-check/1', 'baseline_commit': BASE,
               'scope': 'deterministic header/catalogue/roadmap checks by the author; not independent scientific review',
               'documents': [], 'body_preservation': 'checked by exact inverse transformation'}
    table = ['# Reading Guide: All Publication Names', '',
             'English source baseline: `' + BASE + '`. New titles do not change canonical paths, edition 1.1, protocol versions or scientific status. Russian and Chinese entries below are title translations only; full body coverage is tracked separately in [Translations](roadmap/TRANSLATIONS.md).', '',
             '| Document | English title | Русское название | 简体中文标题 | Previous English title |',
             '| --- | --- | --- | --- | --- |']
    for doc in docs:
        old = doc['title']
        row = names[doc['slug']]
        full, subtitle = display_parts(row[1], old)
        raw = original(doc['path'])
        translated = rename_document(raw, old, row[1])
        out[doc['path']] = translated
        doc.update(title=full, short_title=row[1], subtitle=subtitle, previous_title=old)
        table.append('| [' + doc['type'] + '](' + doc['path'] + ') | ' + full + ' | ' + display_parts(row[2], row[3])[0] + ' | ' + row[4] + '：' + row[5] + ' | ' + old + ' |')
        receipt['documents'].append({'path': doc['path'], 'old_title': old, 'new_title': full,
                                      'old_sha256': digest(raw), 'new_sha256': digest(translated),
                                      'preserved_anchor': anchor(old), 'body_unchanged': True})
    out['publication-catalog.json'] = dumped(catalogue)
    out['DOCUMENTS.md'] = '\n'.join(table) + '\n'
    # Update only navigation labels, not scientific references or retained evidence.
    for index in ['README.md', 'papers/README.md', 'engineering/README.md', 'engineering/specifications/README.md',
                  'engineering/studies/README.md', 'reference/README.md', 'appendices/README.md']:
        text = original(index)
        def relabel(match: re.Match) -> str:
            import posixpath
            target = match[2].split('#', 1)[0]
            if '://' in target:
                return match[0]
            absolute = posixpath.normpath(posixpath.join(posixpath.dirname(index), target))
            found = next((d for d in docs if d['path'] == absolute), None)
            return '[' + found['short_title'] + '](' + match[2] + ')' if found else match[0]
        text = re.sub(r'\[([^\]\n]+)\]\(([^)\n]+)\)', relabel, text)
        if index == 'README.md':
            insertion = '\nRead [all 30 document names](DOCUMENTS.md), the [complete roadmap](ROADMAP.md), the [Russian roadmap](roadmap/ROADMAP.ru.md), and the [naming canon](reference/document-naming/NAMING.md). Short names precede explanatory subtitles; established paths and historical revisions remain stable. Engineering execution is currently paused; the roadmap separates authoring from later site integration.\n'
            pos = text.index('\n') + 1
            text = text[:pos] + insertion + text[pos:]
        out[index] = text
    for path in ['AGENTS.md', 'CONTRIBUTING.md']:
        text = original(path)
        addition = '\n## Reader-facing names and roadmap\n\nFollow [Clear Names](reference/document-naming/NAMING.md) and the [complete name register](DOCUMENTS.md): one-to-three-word short name, colon, explanatory subtitle. Catalogue title, source front matter and H1 agree. Preserve slugs, requirement IDs, old anchors, historical evidence and source-pinned review/translation records. Roadmap headings use meaningful names; F/RM codes are secondary compatibility metadata, never the primary reader interface. [ROADMAP.md](ROADMAP.md) separates artifact state, review and Muneral execution state.\n\nEnglish remains the source language of the canonical catalogue. Explicitly authorized Russian and Simplified Chinese renditions and reader guides are allowed with exact source bindings and separate fidelity status; a translated title does not certify a translated body. Engineering execution remains paused until the operator resumes it. Preparing content or a PR does not dispatch an engineer or authorize deployment.\n'
        if path == 'CONTRIBUTING.md':
            text = text.replace('Keep contributions in English, provide sources for factual claims,', 'Keep canonical source contributions in English (authorized translations and localized reader guides are identified separately), provide sources for factual claims,', 1)
        out[path] = text.rstrip() + '\n' + addition
    deps = json.loads(original('roadmap/dependencies.json'))
    if len(deps['nodes']) != 25 or sum(len(n['requires']) for n in deps['nodes']) != 45 or len(deps['advisory_links']) != 4:
        raise ValueError('Unexpected original roadmap graph')
    if {n['id'] for n in deps['nodes']} != {r[0] for r in tasks}:
        raise ValueError('Workstream names do not match original graph')
    for node in deps['nodes']:
        row = next(r for r in tasks if r[0] == node['id'])
        node['display_name'] = row[1]
        node['display_name_ru'] = row[2]
    deps['display_revision'] = '2026-11-08'
    deps['execution_pause'] = 'Engineering paused by operator; analytical authorship continues; not a Muneral state update'
    out['roadmap/dependencies.json'] = dumped(deps)
    task_source = original('roadmap/TASKS.md')
    task_source = task_source.replace('status: planned', 'status: definitions-with-artifact-observations').replace('updated: 2026-11-06', 'updated: 2026-11-08')
    task_source = task_source.replace('All tasks begin as **planned, execution unverified**.', 'The original planning baseline was 6 November 2026. The dated artifact observations below supersede any impression that an existing document is still absent; execution states remain unverified in Muneral. Engineering execution is paused by the operator.')
    task_source = task_source.replace('Inventory all 29 catalogue documents', 'Inventory all documents in the pinned current catalogue (30 at the present baseline)')
    task_source = task_source.replace('**Gap.**', '**Original gap (6 November 2026).**')
    def task_heading(match: re.Match) -> str:
        code, subtitle = match[1], match[2]
        row = next(r for r in tasks if r[0] == code)
        return alias(code.lower()) + alias(anchor(subtitle)) + '## ' + row[1] + ': ' + subtitle + '\n\n**Artifact observation (8 November 2026).** ' + row[3]
    task_source = re.sub(r'^## (RM-\d+)\n\n### ([^\n]+)', task_heading, task_source, flags=re.M)
    task_source = re.sub(r'^\*\*Start boundary\.\*\*[^\n]*', '**Preparation boundary.** Analysis follows the directly authorized scope; dependent acceptance needs the named reviewed outputs. Engineering execution is paused, including earlier notes that said server/registry work was ready to start.', task_source, flags=re.M)
    out['roadmap/TASKS.md'] = humanize(task_source, labels)
    for path in ['roadmap/FOUNDATIONS_RELEASE_PLAN.md', 'roadmap/SITE_DELIVERY.md', 'roadmap/EXPERIMENTS.md']:
        text = humanize(original(path), labels)
        note = '\n> Current editorial note, 8 November 2026: names replace opaque reader-facing labels; compatibility mappings are in [workstreams.json](workstreams.json). The foundations introduction already exists as a research draft. The operator has paused engineering execution; this plan is not an instruction to restart it. Later explicit per-document authorizations remain valid, and future research is not an unbounded release gate.\n'
        match = re.search(r'^# [^\n]+\n', text, re.M)
        if match is None:
            raise ValueError('No roadmap H1: ' + path)
        out[path] = text[:match.end()] + note + text[match.end():]
    overview = current('ROADMAP.md')
    overview = re.sub(r'<!-- WORKSTREAM_TABLE -->.*?<!-- /WORKSTREAM_TABLE -->', '<!-- WORKSTREAM_TABLE -->', overview, flags=re.S)
    work_table = ['| Workstream | Artifact observation |', '| --- | --- |']
    for row in tasks:
        work_table.append('| [' + row[1] + '](roadmap/TASKS.md#' + row[0].lower() + ') | ' + row[3] + ' |')
    if overview.count('<!-- WORKSTREAM_TABLE -->') != 1:
        raise ValueError('Missing unique roadmap table marker')
    out['ROADMAP.md'] = overview.replace('<!-- WORKSTREAM_TABLE -->', '<!-- WORKSTREAM_TABLE -->\n\n' + '\n'.join(work_table) + '\n\n<!-- /WORKSTREAM_TABLE -->')
    ru = ['---', 'title: "Дорожная карта: Работы, проверки и публикация Контракта знаний"', 'sources: none', 'language: ru', 'status: repository-editorial-proposal', 'updated: 2026-11-08', '---', '',
          '# Дорожная карта: Работы, проверки и публикация Контракта знаний', '',
          '[Все названия документов](../DOCUMENTS.md) · [English roadmap](../ROADMAP.md) · [Подробные определения работ](TASKS.md) · [Переводы](TRANSLATIONS.md)', '',
          'Это полный перечень согласованных направлений текущей программы, а не обещание закончить все будущие исследования. Состояние артефакта, его рецензирование, публикация и исполнительный статус задачи различаются. Единственным исполнительным реестром остаётся Muneral; его состояния здесь заново не подтверждены.', '',
          '## Что уже существует', '',
          'Принятый английский корпус редакции 1.1 содержит 30 документов: девять научных работ, одиннадцать спецификаций, шесть исследований и четыре справочных документа. Вводная работа «Мост смысла» сохраняет статус исследовательского черновика. Все документы перечислены в каталоге. Настоящее переименование не изменяет научные результаты, версии протоколов, исторические свидетельства или уже развёрнутый сайт.', '',
          '## Что выполняется сейчас', '',
          'Инженерные работы приостановлены по прямому указанию автора из-за исчерпания лимитов агентов. KC-Brain самостоятельно выполняет научное и редакторское авторство: понятные названия, согласование корпуса, переводы, источники, формальные определения, примеры и контрпримеры. Отдельная рецензия остаётся отдельной работой Agent-Brain. Разработка сервисов, серверные проверки и развёртывание не возобновляются этой картой.', '',
          'Для полного русско-китайского корпуса ещё нужно написать 17 документов на каждый язык — 34 перевода. Существующие 26 переводных файлов являются авторскими черновиками. Всего приёмка и публикация необходимы для 60 переводных документов; тексты интерфейса, дорожной карты и других публичных страниц учитываются отдельно. Перевод всех заголовков не уменьшает число отсутствующих основных текстов.', '',
          '## Фундаментальные работы', '',
          '| Работа | Следующий результат |', '| --- | --- |',
          '| Мост смысла | Согласовать существующую вводную работу с источниками, картой понятий и замечаниями; не повышать статус автоматически. |',
          '| Семантический мост | Новая спецификация ограниченного перехода от интерпретации к вычислимому представлению. |',
          '| Алгебра преобразований | Существенно расширить существующие «Преобразования знаний», не создавать конкурирующую статью. |',
          '| Геометрия смысла | Новая работа о представлениях, расстояниях, потерях и контрпримерах к чрезмерным выводам. |',
          '| Проверка смысла | Новая спецификация связи утверждений, предпосылок, методов проверки и фактических результатов. |',
          '| Проверки смысловых операций | Новое исследование с действительно полученными выводами и прогонами, а не с планами под видом опыта. |', '',
          'Основная последовательность сохраняется. Прямые позднейшие поручения по отдельным статьям, исправление существенных ошибок и выпуск уже подготовленных ограниченных результатов не отменяются. Базовый пилот применения знаний не обязан ждать всей будущей геометрической программы.', '',
          '## Полный перечень направлений', '',
          'Подробные исходные определения, ответственные роли, обязательные зависимости, артефакты и отрицательные проверки сохранены в связанном документе. Ни одна строка ниже сама по себе не закрывает задачу.', '',
          '| Направление | Следующий результат | Когда результат можно принять |', '| --- | --- | --- |']
    for row in tasks:
        ru.append('| [' + row[2] + '](TASKS.md#' + row[0].lower() + ') | ' + row[4] + ' | ' + row[5] + ' |')
    ru.extend(['', '## Как читать зависимости', '',
               'Сохранены все 25 направлений, 45 обязательных связей результатов и четыре рекомендательные связи. Обязательная связь означает необходимость конкретного проверенного входа для приёмки или исполнения зависимой работы; она не запрещает предварительное исследование. Рекомендация помогает, но не блокирует выпуск. Старые коды нужны только для совместимости ссылок и реестров — их не требуется запоминать.', '',
               '## Что остаётся после инженерной паузы', '',
               'Понадобятся согласование названий и переводов с компилятором сайта, проверка относительных ссылок на реальных документах, сборка из принятого коммита, проверка HTML и доступных файлов скачивания, настольного и мобильного отображения. Отдельно выполняются реальные проверки чтения источников, целостности пакетов, журналов, обязательного контекста, полномочий, восстановления, бюджетов и межпакетных связей. Схема или зелёный CI сами по себе не подтверждают выполнение этих условий.', '',
               '## Конечный редакторский выпуск', '',
               'Выпуск закрывает конкретный перечень текстов и замечаний, а не всю программу научных исследований. Новая гипотеза может быть уточнена, ограничена или отвергнута без обесценивания честно сформулированных прежних результатов. Готовность текста, отдельная рецензия, слияние исходников, сайт и индекс подтверждаются раздельно. Публичный анонс готовится после согласования этого пакета; утверждать заранее, что новые названия или переводы уже появились на сайте, нельзя.', ''])
    out['roadmap/ROADMAP.ru.md'] = '\n'.join(ru)
    crosswalk = ['---', 'title: "Compatibility Names: Historical Roadmap Identifiers"', 'sources: none', '---', '',
                 '# Compatibility Names: Historical Roadmap Identifiers', '',
                 'Use the names in reader-facing navigation. These stable technical aliases are retained for existing links, graph nodes and correspondence; none is a Muneral identifier.', '',
                 '| Historical alias | English name | Русское название |', '| --- | --- | --- |']
    for row in tasks:
        crosswalk.append('| `' + row[0] + '` | [' + row[1] + '](TASKS.md#' + row[0].lower() + ') | ' + row[2] + ' |')
    for row in work['foundations']:
        crosswalk.append('| `' + row[0] + '` | ' + row[1] + ' | ' + row[2] + ' |')
    out['roadmap/COMPATIBILITY.md'] = '\n'.join(crosswalk) + '\n'
    receipt.update(document_count=30, locales_with_title_mapping=['en', 'ru', 'zh-Hans'],
                   roadmap_nodes=25, required_edges=45, advisory_links=4,
                   independent_review='not_claimed', site_deployment='not_performed', task_status_changes='none')
    out['reviews/naming-roadmap/RESULTS.json'] = dumped(receipt)
    out['reviews/naming-roadmap/REVIEW.md'] = '\n'.join([
        '---', 'title: "Naming Review: Scope and Preserved Content"', 'sources: none', '---', '',
        '# Naming Review: Scope and Preserved Content', '',
        'KC-Brain authored the naming policy, all 90 short/full title mappings and the updated roadmap. The deterministic migration binds to `' + BASE + '`. [RESULTS.json](RESULTS.json) records old/new manuscript hashes and exact header-only inverse checks; it is regenerated from actual source bytes, not copied from a proposed outcome.', '',
        'All 30 catalogue source bodies, requirements, equations, references, limitations and evidence remain unchanged after reversing the declared title/front-matter/compatibility-anchor edit. Canonical paths, catalogue counts, edition and status are preserved. Existing corpus decisions, allowlists, raw evidence and old reviews are not rewritten. Roadmap identity and 45 required/4 advisory edges are preserved while names and dated artifact observations are added.', '',
        'The check is mechanical and author-produced. It does not prove that every label is optimal, establish independent scientific review, accept all roadmap outputs, reconcile Muneral or publish a website. Existing translation PR76 stays on its exact source pins; no review is silently transferred. Full translation bodies and site integration remain separate work.', '',
        'Run `python3 -B tools/apply_document_names.py --check` and `python3 -B -m unittest tools.test_document_names -v`, then the ordinary project checks. Report actual run results separately. A temporary branch-only materialization workflow may apply this deterministic patch; it never merges main, deploys, changes task state or touches credentials outside the normal repository token. It is removed before the final proposal is reviewed.', ''])
    sources = original('SOURCES.md')
    additions = [REGISTRY, 'reference/document-naming/NAMING.md', WORK,
                 'reviews/naming-roadmap/REVIEW.md', 'reviews/naming-roadmap/RESULTS.json']
    row = '| Readable publication names and roadmap editorial mapping | Knowledge Contract Arcana contributors | <https://github.com/Arcanada-one/knowledge-contract/tree/' + BASE + '> | CC-BY-4.0 text; Apache-2.0 code | Author-directed naming, title translations and artifact-state projection; no new scientific evidence or task authority | ' + ', '.join('`' + p + '`' for p in additions) + ' |\n'
    source_lines = sources.splitlines(keepends=True)
    last = max(i for i, line in enumerate(source_lines) if line.startswith('|'))
    source_lines.insert(last + 1, row)
    out['SOURCES.md'] = ''.join(source_lines)
    return out, receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true', help='write the deterministic patch on the dedicated proposal branch only')
    parser.add_argument('--check', action='store_true', help='verify without writing (default)')
    args = parser.parse_args()
    if args.apply and args.check:
        parser.error('choose either apply or check')
    try:
        outputs, receipt = build()
        if args.apply:
            if git('branch', '--show-current').strip() != BRANCH:
                raise ValueError('Apply is restricted to the dedicated proposal branch')
            for path, text in outputs.items():
                target = ROOT / path
                if target.is_symlink() or not target.resolve().is_relative_to(ROOT.resolve()):
                    raise ValueError('Unsafe output path: ' + path)
                if target.exists() and path not in ['ROADMAP.md', 'DOCUMENTS.md', 'roadmap/ROADMAP.ru.md', 'roadmap/COMPATIBILITY.md', 'reviews/naming-roadmap/REVIEW.md', 'reviews/naming-roadmap/RESULTS.json']:
                    before = current(path)
                    if before not in (original(path), git('show', 'd10ba0500be8c0ad2f031445df9c539b5e41fe54:' + path), git('show', '548abd01d089faf81570efaafd41ef873c693e47:' + path), text):
                        raise ValueError('Concurrent or unexpected change: ' + path)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(text, encoding='utf-8', newline='\n')
        mismatches = [path for path, text in outputs.items() if not (ROOT / path).is_file() or current(path) != text]
        if mismatches:
            raise ValueError('Missing or inconsistent output: ' + ', '.join(mismatches))
        print(dumped({'result': 'pass', 'documents': len(receipt['documents']), 'title_locales': 3,
                      'roadmap_nodes': 25, 'required_edges': 45, 'advisory_links': 4,
                      'output_files': len(outputs), 'independent_review': 'not_claimed', 'mode': 'apply' if args.apply else 'read_only_check'}))
        return 0
    except (ValueError, OSError, KeyError, subprocess.CalledProcessError) as exc:
        print('DOCUMENT_NAMES_FAIL ' + str(exc))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())

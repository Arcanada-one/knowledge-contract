session_id: blind-sonnet-20261029-2
model: claude-sonnet
input_digest: a20169dc4d1fef10d143f6d7b567f25c58a53d4546ccc69bf2998d0f210e7028

## Блind-ревью DEC-AUP-0171: шесть решений о публикации (набор b1)

Ревью проведено только по входным данным («the input»). Вывод: чек-лист выполнен для всех шести решений, блокирующих замечаний нет.

### Пункт 1. Дайджесты sha256 (я посчитал сам)

Я вырезал каждый blob по длине из заголовка BLOB. Первые 12 hex-символов посчитанного и заявленного дайджестов совпали во всех шести случаях. Я сверил и полные 64 символа программно. После каждого blob стоит перевод строки. Заявленные в строках решений `sha256` и `upstream` совпадают с заголовками BLOB.

| path | заявлено | посчитано | длина |
|---|---|---|---|
| articles/attribution-policy.md | 121f3d7f177c… | 121f3d7f177c… | 3316 |
| articles/contribution-guide.md | 522ee9995607… | 522ee9995607… | 4942 |
| articles/openness-and-attribution-policy.md | 2b2a0b38e231… | 2b2a0b38e231… | 3476 |
| articles/project-overview.md | 90bc42fb1af7… | 90bc42fb1af7… | 7151 |
| articles/site-summary-llms.md | 0d781a65e39d… | 0d781a65e39d… | 2976 |
| articles/sources-register.md | b90ad7c31e0e… | b90ad7c31e0e… | 2199 |

### Пункт 2. Upstream и декларации лицензий

- **Upstream.** Пять документов ведут на `knowledge-contract@39e05969…`, а `llms.txt` — на `contract-place-site@74f620b9…`. Это совпадает с `mirror_of` и `mirror_source_commit` во front matter.
- **Лицензия.** Во всех шести документах front matter даёт `license: CC-BY-4.0`.
- **REUSE.toml репозитория знаний.** Аннотация `path="**"` задаёт CC-BY-4.0, а Apache-2.0 относится только к `tools`, `schemas`, `.github` и подобному. NOTICE называет автора Pavel Valentov и подтверждает CC BY 4.0 для текста.
- **REUSE.toml сайта.** `public/llms.txt` явно указан в аннотации с CC-BY-4.0. Держатель прав и NOTICE сайта те же.
- **LICENSE.** Это текст CC BY 4.0 длиной 18657 байт, идентичный в обоих репозиториях (хеш `9ba9550ad4…`). Блоки REUSE.toml и NOTICE одинаковы во всех пяти декларациях первого репозитория.
- **Счётчики переписанных ссылок.** В `mirror_note` их пять (ATTRIBUTION, 5), восемь (CONTRIBUTING, 8), четыре (OPENNESS, 4), девятнадцать (README, 19) и две (SOURCES, 2). Я пересчитал относительные ссылки в телах: 5, 8, 4, 19 и 2, всё совпадает. Для `llms.txt` ссылок для переписывания нет, добавлена одна строка-комментарий markdownlint — это согласуется с заметкой.

### Пункт 3. Правообладатель и rights_basis

- `rights_holder` — именованное лицо, Pavel Valentov (во всех шести).
- `rights_basis` дословно цитирует строку держателя из REUSE.toml: `'2026 Pavel Valentov and Knowledge Contract Arcana contributors'`. Она совпадает посимвольно с обоими REUSE.toml.
- Там же сказано, что части контрибьюторов опираются на DCO sign-off, которые «declared and not verified».
- Для решения по `llms.txt` `rights_basis` ссылается на NOTICE и REUSE.toml «at the upstream commit» общей формулой, не называя репозиторий сайта отдельно. Фактически декларации сайта содержат ту же строку держателя и то же имя автора, поэтому расхождения нет.

### Пункт 4. Сторонний текст, знаки, секреты, пути, хосты, адреса

- Программный поиск по телам дал одно срабатывание: слово «secrets» в фразе-запрете из CONTRIBUTING («Do not include secrets…»). Это не секрет.
- Путей хоста (`/home`, `/Users`) и IP-адресов нет.
- Все URL публичные: contract.place, arcanada.ai, github.com/Arcanada-one, creativecommons.org, developercertificate.org. Имена «Knowledge Contract Arcana» и «Arcanada» собственные, и документы сами оговаривают, что они не лицензируются.
- Чужого текста не нашёл. SOURCES.md сам заявляет, что сторонних источников не зарегистрировано.

### Пункт 5. Credit line

- Готовая строка есть в ATTRIBUTION: «"<Title>" by Pavel Valentov, Knowledge Contract Arcana (https://contract.place), licensed under CC BY 4.0…».
- Во всех шести блобах `mirror_note` содержит «Credit: Knowledge Contract Arcana, https://contract.place», а front matter содержит `author` и `license`.
- Поле `attribution` в решениях на это указывает.

### Пункт 6. limits

Поле честное. Оно прямо говорит, что не установлены:
- личность автора;
- авторское право на агентский текст;
- отсутствие нераспознанного стороннего материала;
- сам факт ревью;
- совпадение тела зеркала с upstream-файлом, кроме заявленных изменений (upstream-байты ревьюерам не давали);
- а также что запись сделана тем же аккаунтом, который ревьюил.

### Что я не мог проверить

- Совпадение зеркал с upstream-файлами: сами upstream-байты мне не даны. Я проверил лишь внутреннюю согласованность: счётчики ссылок и дайджесты.
- Что LICENSE — неизменённый официальный текст CC BY 4.0. Размер и структура правдоподобны, сличить с эталоном нечем.
- Содержимое receipt `b1.json` и схему `KnowledgeContractPublicationDecision/v2`: их нет во входе.
- Реальность sign-off контрибьюторов и отсутствие SOURCES.md в репозитории сайта: опираюсь только на записанные декларации.
- Авторство и права на текст сверх заявленного: это вне возможностей ревью.

### Findings

1. NON-BLOCKING. `rights_basis` для `site-summary-llms.md` не называет репозиторий сайта и ссылается на NOTICE и REUSE.toml «at the upstream commit» общей формулой, как для остальных пяти документов. Лучше добавить явную ссылку на декларации `contract-place-site`; содержательной ошибки нет.
2. NON-BLOCKING. Тело OPENNESS.md упоминает «operator order» и название закрытого бэкенда `contract-place-api` с приватным репозиторием. Это публичное заявление самого upstream, о границе открытости, а не утечка секрета.
3. NON-BLOCKING. Даты и состояние («no approved entries», «adopted 2026-10-28») зафиксированы на коммите источника; `mirror_note` это оговаривает.

Verdict: APPROVE

VERDICT: APPROVE b7c8b63a360473b2d06bf1ba0ad8351008d330f98c21630aef3c1d3288271783

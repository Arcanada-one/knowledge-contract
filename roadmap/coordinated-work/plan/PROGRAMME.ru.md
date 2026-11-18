# Согласованная деятельность: Программа исследований и инженерных работ

Подготовлено 18 ноября 2026 года. Это версионированное предложение для сверки и приёмки. Фактические задачи, назначения, зависимости и статусы ведутся в Мунереле.

**23 эпика · 104 пакета работ · 247 зависимостей.** Все 72 исходных шага сохранены, добавлены 32 работы, сопоставлены все 16 предполагаемых статей и 12 гипотез. [Полная программа](PROGRAMME.md), [контракты всех работ](TASK_CONTRACTS.md) и [машиночитаемый граф](execution-graph.json) содержат условия приёмки и происхождение каждой строки.

## Что делаем сначала

Первый эпик — согласованный анонс направления в журнале, трёх языковых версиях дорожной карты, репозиториях и действующем графе задач Мунерела. Владелец регистрации — существующий KC-SWE; Agent-SWE обеспечивает связи, для которых нужны полномочия в смежных проектах. Публикация принятого анонса может идти параллельно регистрации задач. Завершение всего стартового эпика требует обеих проверенных квитанций.

1. Зафиксировать исходные материалы и границы подтверждённых результатов.
2. Сохранить эпики, контракты задач, граф и полноту покрытия исследования.
3. Выпустить анонсы EN/RU/zh-Hans; проверить точные переводы, ссылки и фактическую видимость в браузере.
4. Сверить предложения с существующими задачами, переиспользовать подходящие, создать только недостающие.
5. Получить реальные UUID, владельцев, типизированные связи и обратное чтение Мунерела.
6. Передать первые ограниченные пакеты работ с конкретными входами и результатами.

## Граница исходных свидетельств

[Исходный пакет](https://github.com/Arcanada-one/knowledge-contract/tree/ea698baa3d4997b56c725d806c600173aa6064b9/roadmap/coordinated-work) содержит 1176 библиографических записей: 157 проверенных первичных записей и 1019 цитатных кандидатов. Число уникальных работ ещё не установлено; 26 групп совпадений названия/года и 4 пары похожих названий требуют проверки. Полных критических разборов — 0. Численный стенд r2 содержит 10 сценариев, 100 наблюдений «сценарий × период» и 190 элементарных проверок. Это ограниченное свидетельство реализации численной модели, а не эффективности агента или кадрового решения в реальной организации.

## Реестр эпиков

| Эпик | Содержание | Пакетов | Предложенные владелец / исполнитель |
| --- | --- | ---: | --- |
| CW-EP00 | Анонс и регистрация направления | 8 | KC-Brain / KC-SWE |
| CW-EP01 | Корпус, обзор и карта prior art | 9 | KC-Brain / Research-Arcana |
| CW-EP02 | Онтология потребностей и компетенций | 8 | KC-Brain / Research-Arcana |
| CW-EP03 | Состояние организации и разрешенные источники | 8 | KC-Brain / KC-SWE |
| CW-EP04 | Потоки, мощности и ограничения | 8 | KC-Brain / Research-Arcana |
| CW-EP05 | Команды, компетенции и планирование мощности | 8 | KC-Brain / Research-Arcana |
| CW-EP06 | Прогнозы, неопределенность и дрейф | 7 | KC-Brain / Research-Arcana |
| CW-EP07 | Контракты решений и проверка агента | 8 | Agent-Brain / Agent-SWE |
| CW-EP08 | План экспериментов и сравнительная оценка | 5 | KC-Brain / Research-Arcana |
| CW-EP09 | Научные публикации и выпуск на трех языках | 11 | KC-Brain / KC-SWE |
| CW-EP10 | Формальная допустимость и типы ресурсов | 3 | KC-Brain / Research-Arcana |
| CW-EP11 | Права, приватность и пакеты данных | 2 | KC-Brain / KC-SWE |
| CW-EP12 | Независимые оракулы и валидность моделей | 2 | KC-Brain / KC-SWE |
| CW-EP13 | Стенд производственных процессов | 1 | KC-Brain / KC-SWE |
| CW-EP14 | Стенд сервисных процессов | 1 | KC-Brain / KC-SWE |
| CW-EP15 | Стенд проектов и интеллектуальной работы | 1 | KC-Brain / KC-SWE |
| CW-EP16 | Причинность, наблюдаемость и интерференция | 3 | KC-Brain / Research-Arcana |
| CW-EP17 | Исполнение, конкурентность и полная стоимость | 3 | Agent-Brain / Agent-SWE |
| CW-EP18 | Потребители и интеграция в экосистему | 2 | Agent-Brain / Agent-SWE |
| CW-EP19 | Понимание оператором и ценность информации | 1 | KC-Brain / Research-Arcana |
| CW-EP20 | Теневое, полевое и внешнее воспроизведение | 3 | KC-Brain / Research-Arcana |
| CW-EP21 | Динамика, устойчивость и рекурсивная допустимость | 1 | KC-Brain / Research-Arcana |
| CW-EP22 | Совместимость KC и происхождение свидетельств | 1 | KC-Brain / KC-SWE |

## Полный перечень работ

Каждая ссылка ведёт к конкретному выходному артефакту, четырём критериям приёмки, необходимым свидетельствам, отрицательному контролю и потребляемым результатам предшественников.

| Пакет | Работа | Предшественники |
| --- | --- | --- |
| [CW-N01](TASK_CONTRACTS.md#freeze-programme-inputs-and-evidence-boundary-cw-n01) | Зафиксировать исходники и границу имеющихся свидетельств | Исходные материалы |
| [CW-N02](TASK_CONTRACTS.md#define-programme-charter-and-output-families-cw-n02) | Определить программу и семейства результатов | CW-N01 |
| [CW-N03](TASK_CONTRACTS.md#build-and-validate-execution-graph-cw-n03) | Сформировать граф исполнения и полное покрытие исходного плана | CW-N02 |
| [CW-N04](TASK_CONTRACTS.md#prepare-enruzh-hans-announcement-bundle-cw-n04) | Подготовить анонс и карточки исследований на трех языках | CW-N02, CW-N03 |
| [CW-N05](TASK_CONTRACTS.md#publish-repository-and-roadmap-programme-entries-cw-n05) | Связать программу с репозиториями и дорожной картой | CW-N03, CW-N04 |
| [CW-N06](TASK_CONTRACTS.md#register-and-read-back-muneral-graph-cw-n06) | Зарегистрировать граф задач в Muneral и прочитать его обратно | CW-N03 |
| [CW-N07](TASK_CONTRACTS.md#deliver-announcement-and-programme-landing-cw-n07) | Опубликовать и проверить анонс на трех языках | CW-N04, CW-N05 |
| [CW-N08](TASK_CONTRACTS.md#complete-collective-handoff-and-first-work-batch-cw-n08) | Передать области ответственности и запустить ограниченную первую очередь | CW-N06, CW-N07 |
| [CW-A01](TASK_CONTRACTS.md#define-review-scope-cw-a01) | Границы обзора | CW-N01 |
| [CW-A02](TASK_CONTRACTS.md#verify-the-seed-bibliography-cw-a02) | Проверенное библиографическое ядро | CW-A01 |
| [CW-A03](TASK_CONTRACTS.md#extract-citation-candidates-cw-a03) | Извлечение цитатных кандидатов | CW-A01 |
| [CW-A04](TASK_CONTRACTS.md#resolve-publication-identities-cw-a04) | Разрешение идентичности | CW-A02, CW-A03 |
| [CW-A05](TASK_CONTRACTS.md#expand-field-coverage-cw-a05) | Расширение по научным направлениям | CW-A01 |
| [CW-A06](TASK_CONTRACTS.md#screen-full-texts-cw-a06) | Отбор полных текстов | CW-A02, CW-A04, CW-A05 |
| [CW-A07](TASK_CONTRACTS.md#extract-scoped-claims-cw-a07) | Карточки утверждений | CW-A06 |
| [CW-A08](TASK_CONTRACTS.md#review-the-scoping-map-cw-a08) | Публикация карты литературы | CW-A07 |
| [CW-N09](TASK_CONTRACTS.md#frontload-novelty-discriminants-cw-n09) | Сопоставить предполагаемый вклад с ближайшими предшественниками | CW-A07 |
| [CW-B01](TASK_CONTRACTS.md#define-organizational-units-cw-b01) | Единицы организационного анализа | CW-A01 |
| [CW-B02](TASK_CONTRACTS.md#classify-needs-and-situations-cw-b02) | Фасеты ситуаций и потребностей | CW-B01 |
| [CW-B03](TASK_CONTRACTS.md#map-sectors-and-processes-cw-b03) | Сопоставление отраслей и процессов | CW-B01 |
| [CW-B04](TASK_CONTRACTS.md#map-occupations-and-competencies-cw-b04) | Сопоставление профессий и компетенций | CW-B01 |
| [CW-B05](TASK_CONTRACTS.md#define-resource-semantics-cw-b05) | Типы ресурсов | CW-B01 |
| [CW-B06](TASK_CONTRACTS.md#define-performance-measures-cw-b06) | Вектор производительности | CW-B01 |
| [CW-B07](TASK_CONTRACTS.md#assess-annotation-agreement-cw-b07) | Проверка согласия классификаторов | CW-B02, CW-B03, CW-B04, CW-B05, CW-B06 |
| [CW-B08](TASK_CONTRACTS.md#evaluate-held-out-sectors-cw-b08) | Проверка новых отраслей | CW-B07 |
| [CW-C01](TASK_CONTRACTS.md#build-the-typed-work-graph-cw-c01) | Граф работы и ответственности | CW-B01, CW-B02, CW-B05 |
| [CW-C02](TASK_CONTRACTS.md#define-event-semantics-cw-c02) | Словарь событий | CW-C01 |
| [CW-C03](TASK_CONTRACTS.md#separate-demand-observations-cw-c03) | Наблюдаемый и скрытый спрос | CW-C01, CW-B06 |
| [CW-C04](TASK_CONTRACTS.md#represent-availability-calendars-cw-c04) | Календарь доступности | CW-C01, CW-B04, CW-B05 |
| [CW-C05](TASK_CONTRACTS.md#preserve-provenance-and-conflicts-cw-c05) | Происхождение и конфликты | CW-C02, CW-A02, CW-N10 |
| [CW-C06](TASK_CONTRACTS.md#specify-freshness-and-invalidation-cw-c06) | Обновление и срок пригодности | CW-C05 |
| [CW-C07](TASK_CONTRACTS.md#prototype-authorized-adapters-cw-c07) | Адаптеры действующих систем | CW-C02, CW-C03, CW-C04, CW-C05, CW-C06, CW-N15 |
| [CW-C08](TASK_CONTRACTS.md#review-the-organization-profile-cw-c08) | Организационный профиль KC | CW-C07, CW-B08, CW-A08 |
| [CW-D01](TASK_CONTRACTS.md#define-flow-conservation-cw-d01) | Явная модель баланса | CW-B05, CW-N14 |
| [CW-D02](TASK_CONTRACTS.md#derive-conditional-throughput-bounds-cw-d02) | Узкие места и разрезы | CW-D01 |
| [CW-D03](TASK_CONTRACTS.md#model-buffers-and-delays-cw-d03) | Конечные буферы и задержки | CW-D01, CW-D02 |
| [CW-D04](TASK_CONTRACTS.md#model-setup-and-rework-cw-d04) | Переналадка и качество | CW-D01, CW-C03 |
| [CW-D05](TASK_CONTRACTS.md#compare-release-policies-cw-d05) | Правила допуска работы | CW-D06, CW-N17 |
| [CW-D06](TASK_CONTRACTS.md#add-product-mix-and-shared-resources-cw-d06) | Несколько продуктов и общие ресурсы | CW-D03, CW-D04, CW-C04 |
| [CW-D07](TASK_CONTRACTS.md#construct-local-metric-counterexamples-cw-d07) | Контрпримеры локальным KPI | CW-D05, CW-B06 |
| [CW-D08](TASK_CONTRACTS.md#review-the-flow-model-cw-d08) | Рецензия модели потока | CW-D07, CW-A08, CW-C08 |
| [CW-E01](TASK_CONTRACTS.md#estimate-task-workload-cw-e01) | Трудоемкость по задачам | CW-B04, CW-C03, CW-C04, CW-B06 |
| [CW-E02](TASK_CONTRACTS.md#bind-competency-evidence-cw-e02) | Проверка компетенций | CW-B04 |
| [CW-E03](TASK_CONTRACTS.md#optimize-multiskill-assignments-cw-e03) | Многоквалификационное расписание | CW-E01, CW-E02, CW-D06 |
| [CW-E04](TASK_CONTRACTS.md#model-hiring-lead-times-cw-e04) | Найм и выход на мощность | CW-E01, CW-C04 |
| [CW-E05](TASK_CONTRACTS.md#compare-capacity-alternatives-cw-e05) | Альтернативы найму | CW-E03, CW-E04, CW-F04, CW-N21 |
| [CW-E07](TASK_CONTRACTS.md#constrain-sustainable-workload-cw-e07) | Условия устойчивой нагрузки | CW-C04, CW-E03 |
| [CW-E08](TASK_CONTRACTS.md#produce-auditable-role-requirements-cw-e08) | Профиль потребности в роли | CW-E05, CW-E06, CW-E07, CW-A08, CW-C08 |
| [CW-N21](TASK_CONTRACTS.md#model-team-complementarity-and-capability-change-cw-n21) | Моделировать взаимодополнение команды, наставничество и обучение | CW-E01, CW-E02, CW-C04 |
| [CW-F01](TASK_CONTRACTS.md#reconcile-hierarchical-forecasts-cw-f01) | Согласование иерархических прогнозов | CW-C03 |
| [CW-F02](TASK_CONTRACTS.md#calibrate-predictive-uncertainty-cw-f02) | Вероятностные интервалы | CW-F01 |
| [CW-F03](TASK_CONTRACTS.md#define-external-shock-scenarios-cw-f03) | Рыночные и политические сценарии | CW-A02, CW-C01 |
| [CW-F04](TASK_CONTRACTS.md#model-decision-delays-cw-f04) | Задержки наблюдения и действий | CW-C02, CW-C04 |
| [CW-F05](TASK_CONTRACTS.md#optimize-under-uncertainty-cw-f05) | Выбор при неполном знании | CW-F02, CW-F03, CW-F04 |
| [CW-F07](TASK_CONTRACTS.md#detect-distribution-shift-cw-f07) | Дрейф и смена режима | CW-C06, CW-F02, CW-F06 |
| [CW-F08](TASK_CONTRACTS.md#backtest-frozen-forecast-decisions-cw-f08) | Проверка на отложенных периодах | CW-F05, CW-F06, CW-F07 |
| [CW-G01](TASK_CONTRACTS.md#define-decision-prerequisites-cw-g01) | Набор знаний для решения | CW-C01, CW-B02, CW-B04, CW-B05, CW-B06, CW-N11 |
| [CW-G02](TASK_CONTRACTS.md#assemble-bounded-context-cw-g02) | Сборка контекста | CW-G01, CW-C05, CW-C06 |
| [CW-G03](TASK_CONTRACTS.md#define-startup-readiness-cw-g03) | Режимы запуска | CW-G01 |
| [CW-G04](TASK_CONTRACTS.md#separate-proposal-and-verification-cw-g04) | Предложения и внешняя проверка | CW-G01, CW-N12 |
| [CW-G05](TASK_CONTRACTS.md#calibrate-abstention-cw-g05) | Уточнение и отказ от вывода | CW-G02, CW-F02 |
| [CW-G06](TASK_CONTRACTS.md#record-decision-evidence-cw-g06) | Квитанция решения | CW-G02, CW-G03, CW-G04 |
| [CW-G07](TASK_CONTRACTS.md#handle-concurrent-decisions-cw-g07) | Конфликт и повторное выполнение | CW-G06, CW-C04 |
| [CW-G08](TASK_CONTRACTS.md#review-learning-updates-cw-g08) | Возврат знаний в базу | CW-G06, CW-C06 |
| [CW-H01](TASK_CONTRACTS.md#freeze-hypotheses-and-metrics-cw-h01) | Регистрация гипотез и метрик | CW-N19 |
| [CW-H05](TASK_CONTRACTS.md#evaluate-strong-baselines-cw-h05) | Сильные сравнительные методы | CW-H02, CW-H03, CW-H04, CW-G04, CW-F08, CW-E08, CW-D08, CW-C08, CW-N18, CW-N20 |
| [CW-H06](TASK_CONTRACTS.md#run-ablations-and-uncertainty-analysis-cw-h06) | Абляции и статистический анализ | CW-H05, CW-G08 |
| [CW-N19](TASK_CONTRACTS.md#register-study-protocols-and-matched-baselines-cw-n19) | Подготовить протокол регистрации каждого сравнения | CW-A07, CW-B06, CW-N09, CW-N11 |
| [CW-N20](TASK_CONTRACTS.md#plan-statistical-units-power-and-multiplicity-cw-n20) | Установить единицы анализа, неопределенность и статистический план | CW-N19, CW-N16 |
| [CW-I01](TASK_CONTRACTS.md#reassess-novelty-cw-i01) | Аудит научной новизны | CW-A08, CW-B08, CW-N09 |
| [CW-I02](TASK_CONTRACTS.md#bind-claims-to-evidence-cw-i02) | Матрица утверждений и свидетельств | CW-A07, CW-N10 |
| [CW-I03](TASK_CONTRACTS.md#prepare-canonical-manuscripts-cw-i03) | Рукописи и спецификации | CW-I01, CW-I02, CW-N30 |
| [CW-I04](TASK_CONTRACTS.md#freeze-reproducibility-packages-cw-i04) | Воспроизводимые пакеты | CW-I03 |
| [CW-I05](TASK_CONTRACTS.md#obtain-substantive-review-cw-i05) | Отдельная содержательная рецензия | CW-I04, CW-N31 |
| [CW-I06](TASK_CONTRACTS.md#integrate-through-repository-gates-cw-i06) | Интеграция в репозиторий | CW-I05 |
| [CW-I07](TASK_CONTRACTS.md#publish-and-verify-served-content-cw-i07) | Публикация и чтение с сайта | CW-I06 |
| [CW-I08](TASK_CONTRACTS.md#admit-indexing-and-maintain-revisions-cw-i08) | Индексирование и пересмотр | CW-I07 |
| [CW-N30](TASK_CONTRACTS.md#define-claim-specific-publication-release-matrix-cw-n30) | Установить отдельные условия выпуска каждого научного артефакта | CW-N02, CW-N09 |
| [CW-N31](TASK_CONTRACTS.md#maintain-trilingual-terminology-and-fidelity-cw-n31) | Согласовать научную терминологию и переводы EN/RU/zh-Hans | CW-B04, CW-N02 |
| [CW-N32](TASK_CONTRACTS.md#maintain-revisions-negative-findings-and-withdrawal-cw-n32) | Установить пересмотр, исправление и отзыв зависимых утверждений | CW-G08, CW-N10 |
| [CW-N11](TASK_CONTRACTS.md#specify-objectives-tradeoffs-and-infeasibility-cw-n11) | Определить цели, обязательства и компромиссы организации | CW-B02, CW-B06 |
| [CW-N12](TASK_CONTRACTS.md#discharge-conditional-admissibility-obligations-cw-n12) | Уточнить условную допустимость решений и обязательства доказательства | CW-B05, CW-C01, CW-N11 |
| [CW-N14](TASK_CONTRACTS.md#implement-dimensional-and-availability-checks-cw-n14) | Проверять размерности, календари и типы ресурсов | CW-B05 |
| [CW-N15](TASK_CONTRACTS.md#bind-data-access-rights-and-measurement-purposes-cw-n15) | Установить права, приватность и допустимые способы работы с данными | CW-N02, CW-N10 |
| [CW-N16](TASK_CONTRACTS.md#build-reference-datasets-and-data-dictionaries-cw-n16) | Подготовить версионируемые наборы данных и границы наблюдаемости | CW-C02, CW-C03, CW-C04, CW-N15 |
| [CW-N17](TASK_CONTRACTS.md#create-independent-oracles-and-mutation-controls-cw-n17) | Создать независимые оракулы и отрицательные контроли | CW-N12, CW-D01 |
| [CW-N18](TASK_CONTRACTS.md#validate-conceptual-and-operational-simulation-models-cw-n18) | Проверить применимость трех семейств моделей | CW-N16, CW-N17, CW-D03, CW-E03, CW-C01, CW-H02, CW-H03, CW-H04 |
| [CW-H02](TASK_CONTRACTS.md#build-the-manufacturing-benchmark-cw-h02) | Производственный стенд | CW-D03, CW-D04, CW-D06, CW-H01, CW-N17 |
| [CW-H03](TASK_CONTRACTS.md#build-the-service-benchmark-cw-h03) | Сервисный стенд | CW-E03, CW-C03, CW-H01 |
| [CW-H04](TASK_CONTRACTS.md#build-the-project-benchmark-cw-h04) | Проектный стенд | CW-C01, CW-C04, CW-H01 |
| [CW-E06](TASK_CONTRACTS.md#separate-performance-from-causation-cw-e06) | Производительность и причинность | CW-B06, CW-C05 |
| [CW-F06](TASK_CONTRACTS.md#check-endogenous-observations-cw-f06) | Цензурирование и обратное влияние | CW-C03, CW-C05 |
| [CW-N29](TASK_CONTRACTS.md#design-bounded-field-intervention-cw-n29) | Зарегистрировать полевое вмешательство, интерференцию и остановку | CW-E06, CW-H01, CW-N15, CW-H07 |
| [CW-N22](TASK_CONTRACTS.md#specify-organization-decision-adapter-contracts-cw-n22) | Связать адаптеры действий с режимами и действующими полномочиями | CW-G03, CW-G04, CW-G06, CW-C07 |
| [CW-N23](TASK_CONTRACTS.md#exercise-concurrent-decision-and-recovery-semantics-cw-n23) | Проверить конкурентность, отмену, повтор и откат | CW-G07, CW-N22 |
| [CW-N24](TASK_CONTRACTS.md#measure-scale-latency-and-total-decision-cost-cw-n24) | Измерить масштабирование и полную стоимость работы | CW-N22, CW-H05 |
| [CW-N26](TASK_CONTRACTS.md#prepare-arcanada-collective-shadow-consumer-cw-n26) | Подготовить теневой потребитель для существующей работы Arcanada | CW-G08, CW-N22, CW-N23, CW-H01, CW-N15 |
| [CW-N27](TASK_CONTRACTS.md#prepare-a-second-eligible-organizational-shadow-consumer-cw-n27) | Выбрать и проверить второй доступный организационный потребитель | CW-G08, CW-N22, CW-N23, CW-H01, CW-N15 |
| [CW-N25](TASK_CONTRACTS.md#evaluate-decision-explanation-and-human-use-cw-n25) | Проверить понимание оператором и ценность дополнительной информации | CW-G06, CW-N19 |
| [CW-H07](TASK_CONTRACTS.md#run-a-shadow-evaluation-cw-h07) | Теневой режим | CW-H06, CW-N26, CW-N24, CW-N25 |
| [CW-H08](TASK_CONTRACTS.md#evaluate-a-bounded-field-intervention-cw-h08) | Ограниченный причинный пилот | CW-H07, CW-E06, CW-N29 |
| [CW-N28](TASK_CONTRACTS.md#run-held-out-transfer-and-external-reproduction-cw-n28) | Проверить перенос и внешнее воспроизведение | CW-H06, CW-I04 |
| [CW-N13](TASK_CONTRACTS.md#state-recursive-feasibility-and-stability-conditions-cw-n13) | Исследовать устойчивость и рекурсивную допустимость | CW-N12, CW-D03, CW-F04 |
| [CW-N10](TASK_CONTRACTS.md#specify-claim-and-evidence-lineage-cw-n10) | Связать происхождение и идентичность свидетельств с существующим KC | CW-A01 |

## Порядок и научная приёмка

После фиксации исходников параллельно развиваются обзор, модель организации, правила данных и дизайн экспериментов. Производственный, сервисный и проектный стенды не требуют завершения друг друга. До подтверждающего сравнения обязательны применимость модели, независимый оракул и статистический план. Затем возможны теневое применение, отдельно допустимое ограниченное вмешательство и проверка переноса.

Максимальная цепочка зависимостей изменяется с 64 узлов исходной последовательности на 17 узлов расширенного графа. Это характеристика графа, не оценка календарного ускорения. Сроки и загрузка появятся после оценки работ и реального назначения исполнителей.

Для каждой из 16 возможных статей предусмотрены отдельные вопрос, инженерный спутник, связанные пакеты работ и собственный цикл подготовки, воспроизводимости, рецензии, выпуска и сопровождения. Полные таблицы статей и 12 опровергаемых гипотез приведены в [основной программе](PROGRAMME.md#scientific-series-and-engineering-companions). Названия статей не являются выполненными публикациями.

Обзор требует полного критического чтения выбранных источников; формальная работа — явных предпосылок и доказательства; модельное сравнение — зарегистрированного дизайна и валидированного стенда; причинный эффект — обоснованной идентификации и фактических данных. Готовый результат одного типа не получает автоматически статус другого.

104 строки — пакеты, а не 104 уже запущенных исполнителя. Крупные обзоры, семейства стендов и шаблоны выпуска разбиваются на ограниченные дочерние задачи. Нативная регистрация, научная приёмка, публикация на сайте, индексирование и полномочия агента требуют собственных свидетельств.

[Порядок регистрации в Мунереле](../MUNERAL-REGISTRATION.md) сохраняет реальные границы доступа, защиту от дубликатов, историю и точное обратное чтение. Затраты и сроки этой программы пока NOT_MEASURED. Предложение не активирует платные или производственные эксперименты.

---
name: "bibliography"
title: "Исследовательские основания: Первоисточники и исследовательские основания"
artifact: "bibliography"
edition: "1.1"
author: "Pavel Valentov"
language: "ru"
license: "CC-BY-4.0"
description: "Именованные первоисточники и точная концептуальная или техническая роль каждого из них в текущем издании."
translation_of: "reference/bibliography/BIBLIOGRAPHY.md"
source_commit: "a0450428704fcd41b411203f2fc88c06c779610b"
source_git_blob: "894c57511dc174bfad7bb5ac0157d35daceed8cf"
translation_status: "author-draft"
---

# Исследовательские основания: Первоисточники и исследовательские основания {#primary-sources-and-research-foundations}

**Издание публикации:** 1.1 · **Библиографическая проверка:** 4 ноября 2026 года

Ниже перечислены первоисточники, действительно использованные в текущем издании. Они отделяют установленные результаты и внешние форматы от собственного синтеза проекта. Цитируемый источник даёт указанное концептуальное или техническое основание; он не выражает одобрения Контракта знаний и не устанавливает результативность его реализации. Тексты сторонних книг и изображения страниц источников в этой публикации не воспроизводятся.

## Происхождение {#provenance}

Luc Moreau и Paolo Missier, редакторы. **PROV-DM: The PROV Data Model.** Рекомендация W3C от 30 апреля 2013 года. [Датированная спецификация](https://www.w3.org/TR/2013/REC-prov-dm-20130430/).

Используется для различения сущностей, действий и агентов при описании происхождения, а также для отделения происхождения от оценки содержания. Проект добавляет обязательства применимости к конкретной задаче и допуска к применению; они не являются утверждениями PROV-DM, сделанными от имени проекта.

## SKOS {#skos}

Alistair Miles и Sean Bechhofer, редакторы. **SKOS Simple Knowledge Organization System Reference.** Рекомендация W3C от 18 августа 2009 года. [Датированная спецификация](https://www.w3.org/TR/2009/REC-skos-reference-20090818/).

Используется для понятий, меток и отношений организации знаний. Общая метка или отношение между понятиями не доказывают семантическую эквивалентность или истинность.

## Частичная корректность {#partial-correctness}

C. A. R. Hoare. **An Axiomatic Basis for Computer Programming.** *Communications of the ACM* 12(10), 1969, 576–580, 583. [DOI: 10.1145/363235.363259](https://doi.org/10.1145/363235.363259). [Библиография автора на сайте университета](https://www.cs.ox.ac.uk/people/publications/title/Tony.Hoare.html).

Используется как источник известного подхода к рассуждению о программах через предусловия, постусловия и правила вывода. Работа о преобразованиях адаптирует рассуждение об условном сохранении к явно определённым в ней отношениям. Её аргумент о композиции не представляется ни новой заменой логике программ, ни доказательством завершения.

## Субмодулярная максимизация {#submodular-maximization}

George L. Nemhauser, Laurence A. Wolsey и Marshall L. Fisher. **An Analysis of Approximations for Maximizing Submodular Set Functions—I.** *Mathematical Programming* 14, 1978, 265–294. [DOI: 10.1007/BF01588971](https://doi.org/10.1007/BF01588971).

Используется для классической аппроксимационной гарантии жадного алгоритма при нормированной монотонной субмодулярной функции ценности и ограничении мощности множества. Работа о составлении контекста явно указывает эти предпосылки и объясняет, почему взаимодополняющие единицы знания могут нарушать субмодулярность. Гарантия не переносится на произвольные бюджеты, штрафы или функции семантического качества.

## Генерация с дополнением поиском {#retrieval-augmented-generation}

Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, Sebastian Riedel и Douwe Kiela. **Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.** *Advances in Neural Information Processing Systems* 33, 2020. [Конференционная публикация](https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html). [Авторская рукопись](https://arxiv.org/abs/2005.11401).

Используется как первоисточник для генерации, обусловленной найденными материалами. Работа о составлении контекста изучает явные обязательства покрытия и сохранения; она не заявляет ни о повторении цитируемых экспериментов, ни о превосходстве над их моделями.

## Вычислительная сложность {#computational-complexity}

Richard M. Karp. **Reducibility among Combinatorial Problems.** В сборнике *Complexity of Computer Computations*, 1972, 85–103. [DOI: 10.1007/978-1-4684-2001-2_9](https://doi.org/10.1007/978-1-4684-2001-2_9).

Используется как первоисточник классического контекста сложности задачи покрытия множества. Текущая работа даёт собственное явное отображение конечной задачи покрытия в ограниченный экземпляр задачи выбора контекста. Это не означает, что каждый практический экземпляр труден или что точный конечный перебор невозможен.

## Срезы программ {#program-slicing}

Mark Weiser. **Program Slicing.** *IEEE Transactions on Software Engineering* SE-10(4), 1984, 352–357. [Оригинальная статья](https://faculty.cc.gatech.edu/~harrold/6340/cs6340_fall2009/Readings/Weiser.Slicing.TSE.pdf).

Используется в работе [о смысловых объектах и контексте — английском оригинале](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/semantic-objects-and-context/PAPER.md) для обозначения известной задачи сохранения поведения, лежащей в основе обратного среза. Работа задаёт ограниченную ациклическую модель; она не вводит новый общий алгоритм построения срезов и не выводит сохранение семантики для произвольного текста.

## Поддержание истинности {#truth-maintenance}

Jon Doyle. **A Truth Maintenance System.** *Artificial Intelligence* 12(3), 1979, 231–272. [Запись издателя](https://www.sciencedirect.com/science/article/pii/0004370279900080). [Версия отчёта MIT, AI Memo 521](https://dspace.mit.edu/entities/publication/5377b306-4ecc-4687-b1f5-78cbb4a0543a).

Используется в работе [о пересмотре и управлении — английском оригинале](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/revision-and-governance/PAPER.md) как предшествующая работа об учёте оснований и пересмотре убеждений при изменении предпосылок. Аргумент проекта о достижимости выявляет потенциально затронутые оценки; он не является реализацией системы Дойла.

## Системы сборки {#build-systems}

Andrey Mokhov, Neil Mitchell и Simon Peyton Jones. **Build Systems à la Carte.** *Proceedings of the ACM on Programming Languages* 2(ICFP), статья 79, 2018, 1–29. [DOI: 10.1145/3236774](https://doi.org/10.1145/3236774). [Авторская версия статьи](https://simon.peytonjones.org/assets/pdfs/build-systems-original.pdf).

Используется в работе [о контролируемом повторном использовании знаний — английском оригинале](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/controlled-knowledge-reuse/PAPER.md) для известного различения планирования и повторной сборки, а также корректности относительно объявленных зависимостей. Согласованность с зависимостями сборки не устанавливает истинность источника, семантические требования новой задачи или действующие полномочия.

## Представления и дополнения {#views-and-complements}

François Bancilhon и Nicolas Spyratos. **Update Semantics of Relational Views.** *ACM Transactions on Database Systems* 6(4), 1981, 557–575. [Оригинальная статья](https://cs.uwaterloo.ca/~david/cs848s18/constant-complement.pdf).

Используется в работе [о преобразованиях с ограничениями — английском оригинале](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/constrained-transformations/PAPER.md) как предшествующая конструкция, в которой представление и сохраняемое дополнение определяют состояние базы данных и ограничивают перевод обновлений. Аналогия мотивирует сохранение остаточной информации; проект не заявляет, что эти законы обновления представлений выполняются для естественноязыковых проекций.

## Изменение теорий {#theory-change}

Carlos E. Alchourrón, Peter Gärdenfors и David Makinson. **On the Logic of Theory Change: Partial Meet Contraction and Revision Functions.** *The Journal of Symbolic Logic* 50(2), 1985, 510–530. [DOI: 10.2307/2274239](https://doi.org/10.2307/2274239). [Запись издателя](https://www.cambridge.org/core/journals/journal-of-symbolic-logic/article/abs/on-the-logic-of-theory-change-partial-meet-contraction-and-revision-functions/7ED837BAD5FB6D9A7C77906D73527F9C).

Используется в работе [о пересмотре и управлении — английском оригинале](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/papers/revision-and-governance/PAPER.md) для различения логического сокращения и пересмотра, с одной стороны, и версионируемых артефактов и решений о принятии — с другой. Текущая модель не определяет оператор пересмотра AGM и не заявляет о выполнении постулатов AGM.

## Причинный вывод {#causal-inference}

Judea Pearl. **Causal Inference in Statistics: An Overview.** *Statistics Surveys* 3, 2009, 96–146. [DOI: 10.1214/09-SS057](https://doi.org/10.1214/09-SS057). [Копия автора в институциональном репозитории](https://escholarship.org/uc/item/1sv6k47m).

Используется для различения наблюдаемой связи и причинных выводов при предпосылках о вмешательствах и смешивающих факторах. Поэтому работа о полезности отличает измеренные показатели задачи от идентифицированных причинных выгод и не трактует небольшое разведочное сравнение как оценку для генеральной совокупности.

## Кеширование HTTP {#http-caching}

Roy T. Fielding, Mark Nottingham и Julian Reschke, редакторы. **HTTP Caching.** RFC 9111, стандарт Интернета, июнь 2022 года. [RFC 9111](https://www.rfc-editor.org/rfc/rfc9111.html).

Используется как источник по управлению кешированием HTTP и понятиям актуальности по времени. Применимость знаний, замыкание семантических зависимостей и авторизация действий остаются дополнительными обязательствами проекта.

## Устаревшие ответы HTTP {#stale-http-responses}

Mark Nottingham. **HTTP Cache-Control Extensions for Stale Content.** RFC 5861, информационный документ, май 2010 года. [RFC 5861](https://www.rfc-editor.org/rfc/rfc5861.html).

Используется как явно ограниченная аналогия поведения stale-while-revalidate и stale-if-error. Этот документ имеет информационный статус; его механизмы HTTP не разрешают повторное использование отозванных знаний или действия.

## Язык требований {#requirement-language}

Scott Bradner. **Key Words for Use in RFCs to Indicate Requirement Levels.** RFC 2119, BCP 14, март 1997 года. [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119.html).

Barry Leiba. **Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words.** RFC 8174, BCP 14, май 2017 года. [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174.html).

Инженерные спецификации используют прописные MUST, MUST NOT, SHOULD, SHOULD NOT и MAY в этом смысле. Их нормативная сила относится к соответствию указанной спецификации проекта; это не утверждение о том, что спецификация является стандартом IETF.

## Обмен JSON и схемы {#json-exchange-and-schemas}

Tim Bray, редактор. **The JavaScript Object Notation (JSON) Data Interchange Format.** RFC 8259, стандарт Интернета, декабрь 2017 года. [RFC 8259](https://www.rfc-editor.org/rfc/rfc8259).

Austin Wright, Henry Andrews, Ben Hutton и Greg Dennis, редакторы. **JSON Schema: A Media Type for Describing JSON Documents.** Проект 2020-12. [Официальная основная спецификация](https://json-schema.org/draft/2020-12/json-schema-core).

Используется для синтаксиса обмена и диалекта JSON Schema ограниченных профилей наблюдений, изменений зависимостей, книжного пакета и квитанций индекса. Схема проверяет объявленную структуру данных и ограничения; она не удостоверяет подлинность наблюдения и не выполняет все межзаписные семантические проверки. Профиль хеширования точных байтов не подразумевает канонизацию значений JSON.

## Форматы агентских артефактов {#agent-artifact-formats}

Сопровождающие Agent Skills. **Agent Skills Specification.** [Официальная спецификация](https://agentskills.io/specification), дата обращения — 4 ноября 2026 года.

Используется для именования каталогов навыков, обязательного файла `SKILL.md`, его метаданных `name` и `description`, а также поддерживаемых дополнительных метаданных. Проект определяет собственную дополнительную структуру чтения, сохраняя совместимость с этим форматом.

Сопровождающие AGENTS.md. **AGENTS.md.** [Официальное описание формата](https://agents.md/), дата обращения — 4 ноября 2026 года.

Используется для инструкций агентам программирования в репозитории. Формат представляет собой обычный Markdown и не предписывает универсальную схему идентичностей агентов, компетенций, ролей или схем решения. Форматы проекта для этих артефактов явно обозначены как его собственные соглашения.

## Методы оценки {#evaluation-methods}

Следующие источники объясняют методологические различия, используемые в исследованиях. Они не удостоверяют исторические прогоны, не предоставляют недостающие тестовые данные и не превращают рецензии в рамках одной сессии в независимое повторение.

Brian A. Nosek, Charles R. Ebersole, Alexander C. DeHaven и David T. Mellor. **The Preregistration Revolution.** *Proceedings of the National Academy of Sciences* 115(11), 2018, 2600–2606. [DOI: 10.1073/pnas.1708274114](https://doi.org/10.1073/pnas.1708274114). [Первичная статья](https://pmc.ncbi.nlm.nih.gov/articles/PMC5856500/). [Редакторский пилот — английский оригинал](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/editorial-skill-pilot/STUDY.md) отличает протокол, зафиксированный до получения сохранённых результатов, от анализа, составленного после того, как результаты стали известны. Его локально зафиксированный протокол не был зарегистрирован во внешнем публичном реестре.

Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric P. Xing, Hao Zhang, Joseph E. Gonzalez и Ion Stoica. **Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena.** *Advances in Neural Information Processing Systems 36, Datasets and Benchmarks Track*, 2023. [Авторская рукопись](https://arxiv.org/abs/2306.05685). Используется для обоснования необходимости изучать смещения оценщика и пределы согласия. Редакторское исследование и [исследование проекций — английский оригинал](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/executable-projections-and-revision/STUDY.md) используют собственные грубые шкалы и маскирование; они не наследуют результаты согласия или валидации цитируемого набора испытаний.

Richard A. DeMillo, Richard J. Lipton и Frederick G. Sayward. **Hints on Test Data Selection: Help for the Practicing Programmer.** *Computer* 11(4), апрель 1978 года, 34–41. [Запись издателя](https://ieeexplore.ieee.org/abstract/document/1646911). [Институциональная библиографическая запись](https://www.cerias.purdue.edu/apps/reports_and_papers/view/919). Это историческая основа намеренной мутации программ. Проект сообщает о своих объявленных мутантах и о том, различаются ли они проверками; конечный результат мутационного тестирования не устанавливает общую достаточность тестов.

Alfred Tarski. **A Lattice-Theoretical Fixpoint Theorem and Its Applications.** *Pacific Journal of Mathematics* 5(2), 1955, 285–309. [Оригинальная статья издателя](https://msp.org/pjm/1955/5-2/pjm-v5-n2-p11-s.pdf). Даёт общие основания теории неподвижных точек. [Исследование зависимостей — английский оригинал](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/STUDY.md) вычисляет наименьшее замыкание конечной монотонной итерацией на множестве всех подмножеств объявленного графа; его доказательство и проверки реализации не устанавливают, что зафиксирована каждая семантическая зависимость.

National Institute of Standards and Technology. **SCLITE Scoring Package: Alignment and Scoring Documentation.** [Официальная документация SCTK](https://github.com/usnistgov/SCTK/blob/master/doc/sclite.htm), дата обращения — 4 ноября 2026 года. Используется для выравнивания эталона и гипотезы и подсчёта замен, удалений и вставок, лежащих в основе отчётности об ошибках слов. [Исследование транскрипции — английский оригинал](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/source-transcription-and-uncertainty/STUDY.md) явно задаёт единицы символа и слова; измеренные CER или WER не приводятся, поскольку необходимые эталон и протокол недоступны.

## Книги — источники экспериментов {#experimental-source-books}

Эти книги идентифицируют исторические материалы, использованные в инженерных исследованиях. Они не являются источниками новой научной теоремы, и эта публикация не одобряет содержащиеся в них практические советы. Фактически обработанные входы идентифицируются сохранёнными идентичностями экспортов, а не одними лишь страницами каталогов.

- **Книга о вкусной и здоровой пище** (*The Book of Tasty and Healthy Food*). Министерство пищевой промышленности СССР. Москва: Пищепромиздат, 1952. [Запись Национальной электронной библиотеки](https://rusneb.ru/catalog/000199_000009_005811805/). Использована как кулинарный экспорт в [исследовании транскрипции — английском оригинале](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/source-transcription-and-uncertainty/STUDY.md). Сохранённый ключ экспорта `molchanova` и русская метка «Молчанова» идентифицируют этот вход в отчётах проекта; они не утверждают единоличное авторство. Цитируемый каталог указывает Министерство, и это издание не выводит личность редактора из ключа экспорта.
- **Навигация, лоция и мореходная астрономия** (*Navigation, Pilotage, and Nautical Astronomy*). Г. И. Файн. Москва: Транспорт, 1977. [Запись Национальной электронной библиотеки](https://rusneb.ru/catalog/000199_000009_007594442/). Использована как навигационный экспорт; [сохранённый аудит корпуса](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/source-transcription-and-uncertainty/evidence/corpus-audit-source.json) идентифицирует обработанное представление.
- **Сто схемных задач по автоматике** (*One Hundred Circuit Problems in Automation*). В. А. Тимофеев. Ленинград: Судостроение, 1964. Это библиографические сведения, зафиксированные для экспорта по автоматике в [сохранённом аудите корпуса](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/source-transcription-and-uncertainty/evidence/corpus-audit-source.json). Независимо проверенная стабильная каталожная запись именно этого издания в данной рецензии не установлена; аудит проекта описывает происхождение входа, а не внешнее библиографическое подтверждение. Исторические инженерные задачи изучают представления и сохранение, а не современную эксплуатационную сертификацию.

### Редакторский вход {#editorial-input}

Максим Ильяхов и Людмила Сарычева. **Пиши, сокращай: Как создавать сильный текст** (*Write and Shorten: How to Create Strong Text*). 4-е изд. Москва: Альпина Паблишер, 2024, 400 печатных страниц, **как указано в предоставленной библиографической строке OCR**. [Страница произведения у издателя](https://alpinabook.ru/catalog/book-pishi-sokrashchay-2025/). Независимо проверенный ISBN предоставленного издания не заявляется.

[Редакторский пилот — английский оригинал](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/editorial-skill-pilot/STUDY.md) использовал навыки проекта, полученные из предоставленного OCR-представления этой работы. Тот же производный пакет изучается в [исследовании замыкания зависимостей — английском оригинале](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/STUDY.md), чьи [отчёт о сохранении структуры](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/evidence/layout-preservation-report.json) и [граф зависимостей](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/dependency-closure-and-package-delivery/evidence/dependency-graph.json) сохраняют имена записей источника и метаданные зависимостей.

В имени предоставленного файла указано «2025», а цифровой вход содержит 427 записей физических страниц. Эти признаки расходятся с библиографической строкой OCR и не удостоверяют издание. Текущая страница издателя идентифицирует произведение, но не удостоверяет точный предоставленный в частном порядке файл. Публикация распространяет собственные тексты пилота, оценки и метаданные пакета, а не книгу или закрытый инструментарий, полученный из источника.

## Источники проекта и свидетельства {#project-sources-and-evidence}

Pavel Valentov. **Knowledge Contract and Meaning Management: earlier publication corpus.** Снимок репозитория [b50243b28e9ad7376e28c749a21479ef46ec9d60](https://github.com/Arcanada-one/knowledge-contract/tree/b50243b28e9ad7376e28c749a21479ef46ec9d60).

[Карта источников — английский оригинал](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/appendices/source-map/APPENDIX.md) фиксирует переход от четырнадцати прежних файлов научных работ и десяти спецификаций к текущей структуре чтения. [Индекс инженерных свидетельств](https://github.com/Arcanada-one/knowledge-contract/blob/a0450428704fcd41b411203f2fc88c06c779610b/engineering/studies/evidence-index.json) связывает отдельные эмпирические или аналитические утверждения с подтверждающими записями. Каждое исследование описывает, что можно повторно запустить публично, что доступно лишь в виде сохранённого отчёта и что остаётся неизмеренным.

# Плагін `ua` — Changelog

Історія змін плагіна `ua` (українське право) у межах монорепо [`lawpowers`](../../CHANGELOG.md).

Формат — [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Починаючи з релізів після v0.6.0, плагін теґається окремо як `ua/vX.Y.Z` (де `X.Y.Z` дорівнює полю `version` у `plugin.json`). Історичні записи нижче (до 0.4.0 включно) випускались у межах об’єднаних marketplace-тегів `vX.Y.Z` і зберегли посилання на них.

## [0.4.0] — 2026-04-20

### Changed — BREAKING

Монорепо-реструктуризація. Файли плагіна перенесено з кореня репо в підкаталог `ua/`.

- `plugin.json`: без змін у полі `name` (залишився `ua`), `version` bump `0.3.0` → `0.4.0`.
- `.claude-plugin/plugin.json` → `ua/.claude-plugin/plugin.json`.
- `agents/` → `ua/agents/`; `skills/` → `ua/skills/`.
- Кореневий UA-специфічний `CLAUDE.md` перенесено в `ua/CLAUDE.md`; структурну діаграму оновлено під монорепо.
- У маркетплейсі поле `source` для цього плагіна змінено `"./"` → `"./ua"`.

### Added

- `ua/README.md` — детальна документація плагіна українською з каталогом усіх агентів і скілів (включно з військовим блоком) через виклик `ua:…`.

### Migration

```
/plugin marketplace update lawpowers
/plugin uninstall ua@lawpowers
/plugin install ua@lawpowers
/reload-plugins
```

Усі команди `/ua:…` продовжують працювати як раніше.

## [0.3.0] — 2026-04-20

### Changed — BREAKING

Глобальне перейменування під монорепо:

- Плагін: `legal-ua` → `ua`. Ідентифікатор плагіна (`name` у `plugin.json`) — `ua`.
- Префікс команд: `/legal-ua:…` → `/ua:…`.
- Маркетплейс (контейнер): `legal-ua` → `lawpowers`.
- Репозиторій: `crankshift/legal-ua` → `crankshift/lawpowers` (GitHub auto-redirect зі старого URL працює).

Усі 16 агентів (11 загальних + 5 військових) переведено з `model: sonnet` на `model: inherit` — модель тепер визначається сесією користувача.

### Migration

```
/plugin uninstall legal-ua@legal-ua
/plugin marketplace remove legal-ua
/plugin marketplace add crankshift/lawpowers
/plugin install ua@lawpowers
/reload-plugins
```

## [0.2.0] — 2026-04-20

### Added — військовий блок (ЗСУ і родини)

5 нових агентів і 4 скіли для військовослужбовців ЗСУ та їхніх сімей. Пріоритизовано за TOP-10 болів (Юридична сотня, Офіс Військового омбудсмана, БПД).

#### Агенти

- **`raport-drafter`** — універсальний рапорт військовослужбовця: відпустка (щорічна, сімейна, за станом здоров'я, навчальна), рапорт на ВЛК, переведення (через Армія+), звільнення за ст. 26 ЗУ № 2232-XII, матдопомога, ОГД, УБД, контракт, реєстрація шлюбу через відеозв'язок (постанова КМУ № 213).
- **`vlk-appeal`** — оскарження висновків ВЛК: ієрархічне (вища ВЛК) і судове (адмінпозов у КАС за наказом МО № 402, `z1109-08`). Біль №1 за частотою скарг.
- **`military-social-benefits`** — бойові (постанова КМУ № 168), фронтова надбавка (КМУ № 419), ОГД при пораненні/загибелі, виплати родинам полонених і зниклих безвісти (ЗУ № 3995-IX з розподілом 50/50), статус УБД, пенсії. Шаблон **особистого розпорядження** на випадок полону.
- **`mobilization-defense`** — ТЦК, бронювання (мін. ЗП 21 617,50 грн з 01.01.2026), відстрочки за ст. 23-1 ЗУ № 2232-XII, оскарження штрафів за ст. 210 КУпАП.
- **`szch-defense`** — СЗЧ/дезертирство (ст. 407-408 КК); звільнення від відповідальності за **ч. 5 ст. 401 КК** (Закон № 3902-IX від 20.08.2024).

#### Скіли

- **`military-statute-refs`** — таблиця zakon.rada ID військових НПА.
- **`calculating-military-payments`** — формули розрахунку виплат; прецедент ВС № 280/8933/24 від 11.04.2025.
- **`vlk-procedure`** — категорії А-Д, процедура, строки оскарження.
- **`szch-decriminalization`** — чек-лист ч. 5 ст. 401 КК.

### Changed

- Додано military-relevant keywords у `plugin.json`.

### Methodology

TOP болів встановлено за публічними даними Юридичної сотні (0800 308 100), Офісу Військового омбудсмана (milomb.gov.ua), БПД (legalaid.gov.ua), позиціями Верховного Суду 2024-2026.

## [0.1.0] — 2026-04-20

### Added — початкова версія плагіна

Репозиторій сконвертовано в інсталяційний Claude Code плагін (тоді під назвою `legal-ua`).

#### Агенти (11)

- `claim-drafter` — позовні заяви (ЦПК / ГПК / КАС), зустрічні позови, розрахунок судового збору.
- `response-drafter` — відзиви, заперечення, пояснення з боку відповідача.
- `appeal-drafter` — апеляційні та касаційні скарги; правові позиції ВС.
- `motion-drafter` — процесуальні клопотання.
- `legislation-analyst` — аналіз законодавства, тлумачення норм, перевірка редакції на дату.
- `legal-memo` — правові висновки, меморандуми.
- `request-drafter` — адвокатські запити (ст. 24 ЗУ «Про адвокатуру») і запити на публічну інформацію.
- `contract-drafter` — цивільно-правові та господарські договори.
- `debt-collector` — стягнення заборгованості; ст. 625 ЦК.
- `enforcement-agent` — виконавче провадження; ЗУ № 1404-19.
- `arbitration-agent` — МКАС/МАК, ICC/LCIA/SCC/SIAC/HKIAC/VIAC, ad hoc UNCITRAL, інвестарбітраж; визнання і скасування у держсуді (розд. IX ЦПК, NYC 1958).

#### Скіли (9)

- `fetching-zakon-rada` — фетч НПА з zakon.rada.
- `searching-edrsr` — пошук судової практики в ЄДРСР.
- `calculating-sudovyi-zbir` — судовий збір за ЗУ 3674-VI.
- `citing-ukrainian-law` — формат цитування НПА, рішень ВС/КСУ/ЄСПЛ.
- `determining-ua-jurisdiction` — підсудність.
- `checking-pozovna-davnist` — строки позовної давності.
- `checking-martial-law-overrides` — спецрегулювання періоду воєнного стану.
- `fetching-arbitration-rules` — регламенти арбітражних інституцій.
- `applying-new-york-convention` — NYC 1958 в Україні.

[0.4.0]: https://github.com/crankshift/lawpowers/releases/tag/ua/v0.4.0
[0.3.0]: https://github.com/crankshift/lawpowers/releases/tag/v0.3.0
[0.2.0]: https://github.com/crankshift/lawpowers/releases/tag/v0.2.0
[0.1.0]: https://github.com/crankshift/lawpowers/releases/tag/v0.1.0

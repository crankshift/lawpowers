# lawpowers

Колекція юридичних плагінів для **Claude Code** — монорепо з окремими плагінами для кожної юрисдикції. Встановлюєте лише ті плагіни, які вам потрібні.

| Плагін | Юрисдикція | Префікс команд | Мова |
|---|---|---|---|
| [`ua`](./ua) | Україна | `/ua:…` | українська |
| [`pl`](./pl) | Польща | `/pl:…` | polski |

## Встановлення

Встановлення відбувається в два кроки: додавання маркетплейсу (одноразово) і установка конкретного плагіна. Можна встановити один з плагінів або обидва.

### Крок 1. Додати маркетплейс

#### Через Claude Desktop App (macOS/Windows)

1. Відкрити **Settings → Extensions → Plugins**.
2. Перейти на вкладку **Personal**.
3. Натиснути «**+**» поруч із «Local uploads».
4. У меню обрати **Add marketplace**.
5. Вказати джерело: `crankshift/lawpowers` (або повний URL `https://github.com/crankshift/lawpowers`).

#### Через Claude Code CLI

```bash
claude
```

У відкритій сесії:

```
/plugin marketplace add crankshift/lawpowers
```

### Крок 2. Встановити плагін(и)

#### Тільки український плагін

```
/plugin install ua@lawpowers
/reload-plugins
```

Або в Desktop App — знайти плагін `ua` у списку маркетплейсу і натиснути «+».

Команди будуть доступні з префіксом `/ua:…` — наприклад, `/ua:claim-drafter`, `/ua:raport-drafter`.

#### Тільки польський плагін

```
/plugin install pl@lawpowers
/reload-plugins
```

Команди — з префіксом `/pl:…`.

#### Обидва плагіни

```
/plugin install ua@lawpowers
/plugin install pl@lawpowers
/reload-plugins
```

Неймспейси `ua:` і `pl:` не конфліктують — можна мати обидва плагіни активними одночасно.

### Локально для розробки

```bash
git clone https://github.com/crankshift/lawpowers.git
cd lawpowers
claude --plugin-dir ./ua --plugin-dir ./pl
```

Або лише один плагін:
```bash
claude --plugin-dir ./ua
```

### Перевірка встановлення

- `/plugin` → вкладка **Installed** — встановлені плагіни.
- `/agents` — субагенти з префіксами `ua:` та/або `pl:`.

### Оновлення

```
/plugin marketplace update lawpowers
/reload-plugins
```

Або увімкнути auto-update у `/plugin` → **Marketplaces** → `lawpowers` → **Enable auto-update**.

### Видалення окремого плагіна

```
/plugin uninstall ua@lawpowers   # прибрати лише UA
/plugin uninstall pl@lawpowers   # прибрати лише PL
```

Маркетплейс лишається — можна перевстановити плагін пізніше.

## Короткий огляд плагінів

### `ua` — українське право

- Позови, зустрічні позови, уточнення, апеляції, касації (ЦПК/ГПК/КАС).
- Процесуальні клопотання, адвокатські запити, правові висновки.
- Договори, претензії, виконавче провадження, арбітраж (ЦК/ГК, МКАС).
- **Окремий блок для ЗСУ:** рапорти, ВЛК (оскарження), ТЦК і бронювання, виплати (КМУ № 168, ЗУ 3995-IX), СЗЧ (ч. 5 ст. 401 КК).
- Скіли для роботи з `zakon.rada.gov.ua`, ЄДРСР, судовим збором, позовною давністю.

Детальніше — у [`ua/CLAUDE.md`](./ua/CLAUDE.md).

### `pl` — polskie prawo

- Pozwy, odpowiedzi, apelacje, kasacje (KPC / KPA / KPK).
- Wezwania przedsądowe, zapytania adwokackie, opinie prawne.
- Umowy, windykacja, postępowanie egzekucyjne.
- Skille do pracy z `isap.sejm.gov.pl`, orzeczeniami, przedawnieniem, opłatą sądową.

Szczegóły — w [`pl/CLAUDE.md`](./pl/CLAUDE.md).

## Принципи / Zasady

Усі плагіни дотримуються спільних принципів:

- **Дослівність цитат НПА** — норма наводиться в точній редакції, чинній на дату.
- **Посилання на первинні джерела** — `zakon.rada.gov.ua` для UA, `isap.sejm.gov.pl` для PL.
- **Не вигадувати судову практику** — лише з офіційних реєстрів (ЄДРСР, Portal Orzeczeń).
- **Плейсхолдери для персональних даних** — не зберігати реальні дані клієнтів.
- **Документи — чернетки** — фінальна редакція і відповідальність на людині.

## Історія версій

Повний перелік змін — у [CHANGELOG.md](./CHANGELOG.md). Релізи — на [сторінці Releases](https://github.com/crankshift/lawpowers/releases).

## Ліцензія

MIT — [LICENSE](./LICENSE).

# lawpowers / pl

Plagin Claude Code do pracy z polskim prawem i dokumentami prawniczymi. Zawiera wyspecjalizowanych subagentów pod konkretne zadania prawne oraz skille do efektywnej pracy z oficjalnymi źródłami (ISAP, Dziennik Ustaw, Portal Orzeczeń SP, SN, NSA, TK).

Część monorepo [`lawpowers`](../README.md) — kolekcji plaginów prawnych dla Claude Code. Identyfikator plagina: `pl`; wszystkie komendy mają prefiks `/pl:…`.

> Przestrzeń robocza dla prawnika-praktyka. Wszystkie dokumenty, odpowiedzi i szablony — po polsku.

## Instalacja

Pełna instrukcja instalacji (oba plaginy) — w [root README](../README.md#installation). Skrót dla samego `pl`:

### Claude Desktop App (macOS/Windows)

1. **Settings → Extensions → Plugins → Personal → „+" → Add marketplace**.
2. Wskazać: `crankshift/lawpowers`.
3. W katalogu marketplace'u znaleźć plagin `pl` i nacisnąć „+".

### Claude Code CLI

```
/plugin marketplace add crankshift/lawpowers
/plugin install pl@lawpowers
/reload-plugins
```

### Lokalnie do rozwoju

```bash
git clone https://github.com/crankshift/lawpowers.git
claude --plugin-dir ./lawpowers/pl
```

### Weryfikacja

- `/plugin` → zakładka **Installed** — plagin `pl` na liście.
- `/agents` — subagenci z prefiksem `pl:` (np. `pl:claim-drafter`, `pl:legislation-analyst`).
- Skille aktywują się automatycznie według kontekstu (np. wzmianka „opłata sądowa" tryguje `pl:calculating-oplata-sadowa`, „przedawnienie" — `pl:checking-przedawnienie`).

## Zawartość

Wszystkie komendy wywoływane z prefiksem `/pl:…`.

### Subagenci (`agents/`)

| Wywołanie | Przeznaczenie |
|---|---|
| `pl:claim-drafter` | Pozwy (cywilne / gospodarcze / administracyjne), powództwa wzajemne, modyfikacje, opłata sądowa |
| `pl:response-drafter` | Odpowiedź na pozew, sprzeciwy (od wyroku zaocznego, od nakazu zapłaty), zarzuty od nakazu nakazowego |
| `pl:appeal-drafter` | Apelacja, skarga kasacyjna do SN, zażalenia, skarga kasacyjna do NSA |
| `pl:motion-drafter` | Wnioski procesowe (zabezpieczenie, dowody, biegli, wyłączenie sędziego, terminy) |
| `pl:legislation-analyst` | Analiza obowiązującego prawa, wykładnia norm, brzmienie na datę, dobór orzecznictwa |
| `pl:legal-memo` | Opinie prawne, memoranda, ocena perspektyw sporu |
| `pl:request-drafter` | Wnioski o udostępnienie informacji publicznej (UDIP), pisma adwokata / radcy prawnego, KPA |
| `pl:contract-drafter` | Sporządzanie i analiza umów cywilnoprawnych i gospodarczych, audyt ryzyk, RODO |
| `pl:debt-collector` | Windykacja: wezwanie → pozew (nakazowe / upominawcze / EPU) → egzekucja; odsetki (art. 481 KC, PNOTH) |
| `pl:enforcement-agent` | Postępowanie egzekucyjne: wnioski do komornika, skargi na czynności (art. 767 KPC), klauzula wykonalności |

### Skille (`skills/`)

| Wywołanie | Kiedy stosować |
|---|---|
| `pl:fetching-isap-sejm` | Pobieranie aktów z ISAP / Dziennika Ustaw, brzmienia historyczne, ID kluczowych kodeksów |
| `pl:searching-orzeczenia` | Wyszukiwanie orzecznictwa (Portal Orzeczeń SP, SN, NSA, TK), struktura sygnatury akt |
| `pl:calculating-oplata-sadowa` | Obliczanie opłat sądowych wg UKSC (skala po reformie 2019), zwolnienia |
| `pl:citing-polish-law` | Format cytowania aktów prawnych, orzeczeń SN/TK/TSUE/ETPCz, skróty kodeksów |
| `pl:determining-pl-jurisdiction` | Właściwość sądu (rzeczowa, miejscowa, funkcjonalna), cywilna vs gospodarcza vs administracyjna |
| `pl:checking-przedawnienie` | Terminy przedawnienia (art. 117–125 KC), reforma 2018, ex officio dla konsumentów |

## Zasady pracy

- **Dosłowność cytatów** — norma w dokładnym brzmieniu obowiązującym na wskazaną datę.
- **Obowiązkowe odesłania** — każde stanowisko prawne z odesłaniem do artykułu + źródła + daty weryfikacji.
- **Aktualność** — polskie prawo zmienia się często (KPC reformy 2019, 2023; KC reforma przedawnienia 2018); przed użyciem normy weryfikować obowiązujące brzmienie w ISAP.
- **Nie wymyślać orzecznictwa** — sygnatury, daty wyroków, cytaty — wyłącznie z Portalu Orzeczeń / SN / NSA.
- **Dane osobowe** — w szablonach placeholdery (`[imię i nazwisko]`, `[PESEL]`, `[adres]`, `[KRS]`, `[NIP]`), bez rzeczywistych danych klientów.
- **RODO** — przy projektowaniu klauzul, polityk i analizach — odwołania do RODO (Rozporządzenie 2016/679) oraz ustawy z 10.05.2018 o ochronie danych osobowych.

## Kluczowe źródła

| Zasób | URL |
|---|---|
| ISAP — Internetowy System Aktów Prawnych | https://isap.sejm.gov.pl |
| Dziennik Ustaw | https://dziennikustaw.gov.pl |
| Monitor Polski | https://monitorpolski.gov.pl |
| Portal Orzeczeń sądów powszechnych | https://orzeczenia.ms.gov.pl |
| Sąd Najwyższy | https://www.sn.pl |
| NSA / WSA | https://orzeczenia.nsa.gov.pl |
| Trybunał Konstytucyjny | https://trybunal.gov.pl |
| Ministerstwo Sprawiedliwości | https://www.gov.pl/web/sprawiedliwosc |
| KRS | https://ekrs.ms.gov.pl |
| EUR-Lex | https://eur-lex.europa.eu |
| ETPCz (HUDOC) | https://hudoc.echr.coe.int |

## Zastrzeżenie

Materiały tworzone przez agentów to robocze projekty dla prawnika-użytkownika, a nie końcowa konsultacja dla klienta. Ostateczną redakcję i odpowiedzialność ponosi człowiek.

## Historia wersji

Pełna lista zmian — w root [CHANGELOG.md](../CHANGELOG.md). Wydania — na [stronie Releases](https://github.com/crankshift/lawpowers/releases).

## Licencja

MIT — [LICENSE](../LICENSE).

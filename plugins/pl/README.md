# lawpowers / pl

Plagin Claude Code do pracy z polskim prawem i dokumentami prawniczymi. Zawiera wyspecjalizowanych subagentów pod konkretne zadania prawne oraz skille do efektywnej pracy z oficjalnymi źródłami (ISAP, Dziennik Ustaw, Portal Orzeczeń SP, SN, NSA, TK).

Część monorepo [`lawpowers`](../../README.md) — kolekcji plaginów prawnych dla Claude Code. Identyfikator plagina: `pl`; wszystkie komendy mają prefiks `/pl:…`.

> Przestrzeń robocza dla prawnika-praktyka. Wszystkie dokumenty, odpowiedzi i szablony — po polsku.

> ⚠️ **Zastrzeżenie.** To narzędzie do **wspomagania sporządzania dokumentów prawnych**, a nie porada prawna ani zastępstwo adwokata lub radcy prawnego. Wszystkie wyniki agentów to projekty robocze generowane przez model AI na podstawie tekstu aktów prawnych i **wymagają** weryfikacji przez wykwalifikowanego prawnika względem aktualnych źródeł pierwotnych przed podpisaniem, złożeniem w sądzie lub jakimkolwiek innym użyciem. Ani Anthropic (Claude), ani autorzy i współtwórcy tego repozytorium **nie gwarantują** poprawności, kompletności ani aktualności wyników i **nie ponoszą żadnej odpowiedzialności** za jakiekolwiek skutki ich użycia. Korzystasz na własne ryzyko.

## Instalacja

Pełna instrukcja instalacji (oba plaginy) — w [root README](../../README.md#installation). Skrót dla samego `pl`:

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
claude --plugin-dir ./lawpowers/plugins/pl
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

Plagin `pl` to **narzędzie wspomagające sporządzanie dokumentów prawnych**, a nie świadczenie pomocy prawnej. Instalacja i używanie nie tworzą relacji adwokat–klient ani radca prawny–klient.

- **Nie jest poradą prawną.** Żaden wynik pracy plagina nie stanowi porady prawnej, opinii adwokata/radcy prawnego ani zastępstwa profesjonalnej pomocy prawnej.
- **Projekty generowane przez AI.** Wszystkie teksty tworzy duży model językowy; mogą zawierać błędy, nieaktualne brzmienia przepisów, nieścisłe odesłania do orzecznictwa. Polskie prawo zmienia się często (reformy KPC 2019/2023, przedawnienie 2018) — każde odesłanie należy zweryfikować w źródle pierwotnym (`isap.sejm.gov.pl`, Portal Orzeczeń, sn.pl) w dniu użycia.
- **Obowiązkowa weryfikacja przez człowieka.** Każdy dokument stworzony przy użyciu tego plagina musi zostać przejrzany, poprawiony i zaakceptowany przez wykwalifikowanego prawnika przed podpisaniem, złożeniem do sądu, przesłaniem kontrahentowi lub innym wykorzystaniem. Osoba podpisująca dokument ponosi pełną odpowiedzialność zawodową i prawną.
- **Bez gwarancji.** Oprogramowanie dostarczane jest "TAK JAK JEST", bez jakichkolwiek gwarancji, wyraźnych ani dorozumianych, w szczególności co do dokładności, kompletności, aktualności, przydatności do określonego celu lub zgodności z prawem.
- **Bez odpowiedzialności.** W maksymalnym zakresie dopuszczalnym przez prawo ani Anthropic (dostawca Claude), ani autorzy, opiekunowie i współtwórcy tego repozytorium nie ponoszą odpowiedzialności za jakiekolwiek szkody bezpośrednie, pośrednie, przypadkowe, wynikowe, specjalne lub przykładowe powstałe w wyniku użycia lub niemożności użycia tego oprogramowania — w tym za szkody wynikające z błędnych projektów, przekroczonych terminów, niewłaściwie cytowanych przepisów, niekorzystnych rozstrzygnięć sądowych czy jakichkolwiek innych skutków prawnych lub finansowych. Korzystasz z plagina całkowicie na własne ryzyko.
- **Twoja odpowiedzialność.** To, jak używasz narzędzia, co robisz z jego wynikiem i jakie są tego skutki (wobec klientów, kontrahentów, sądu, organów), pozostaje wyłącznie w Twojej gestii. Jeśli nie jesteś wykwalifikowanym prawnikiem, przed działaniem na podstawie jakichkolwiek wyników skonsultuj się z takim.

## Historia wersji

Zmiany samego plagina `pl` — w [CHANGELOG.md](./CHANGELOG.md) tego katalogu (po polsku). Zestawienie dla całego marketplace'u oraz sąsiednich plaginów — w root [CHANGELOG.md](../../CHANGELOG.md) (po angielsku). Wydania — na [stronie Releases](https://github.com/crankshift/lawpowers/releases).

## Licencja

MIT — [LICENSE](../../LICENSE).

# lawpowers / pl

Plagin Claude Code i Codex do pracy z polskim prawem i dokumentami prawniczymi. Zawiera wyspecjalizowanych subagentów pod konkretne zadania prawne oraz skille do efektywnej pracy z oficjalnymi źródłami (ISAP, Dziennik Ustaw, Portal Orzeczeń SP, SN, NSA, TK).

Część monorepo [`lawpowers`](../../README.md) — kolekcji plaginów prawnych dla Claude Code i Codex. W Claude Code identyfikator plagina to `pl`, a komendy mają prefiks `/pl:…`. W Codex używaj ID `law-pl`.

> Przestrzeń robocza dla prawnika-praktyka. Wszystkie dokumenty, odpowiedzi i szablony — po polsku.

> ⚠️ **Zastrzeżenie.** To narzędzie do **wspomagania sporządzania dokumentów prawnych**, a nie porada prawna ani zastępstwo adwokata lub radcy prawnego. Wszystkie wyniki agentów to projekty robocze generowane przez model AI na podstawie tekstu aktów prawnych i **wymagają** weryfikacji przez wykwalifikowanego prawnika względem aktualnych źródeł pierwotnych przed podpisaniem, złożeniem w sądzie lub jakimkolwiek innym użyciem. Ani Anthropic (Claude), OpenAI (Codex), ani autorzy i współtwórcy tego repozytorium **nie gwarantują** poprawności, kompletności ani aktualności wyników i **nie ponoszą żadnej odpowiedzialności** za jakiekolwiek skutki ich użycia. Korzystasz na własne ryzyko.

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

## Instalacja w Codex

Codex ID tego plagina: `law-pl`. Claude Code ID pozostaje `pl`.

Z marketplace GitHub:

```bash
codex plugin marketplace add crankshift/lawpowers
```

Lokalnie z checkoutu repozytorium:

```bash
cd /path/to/lawpowers
codex plugin marketplace add .
```

Po dodaniu marketplace'u włącz `law-pl` w Codex plugin UI / marketplace flow. Codex czyta instrukcje z `AGENTS.md`; Claude Code czyta `CLAUDE.md`.

Codex custom-agent files are included in `.codex/agents/`. They are generated from `agents/*.md`, so update the Markdown source first and run the repo-level converter/validator before release.

## Zawartość

Wszystkie komendy wywoływane z prefiksem `/pl:…`.

### Subagenci (`agents/`)

**Postępowania sądowe — ogólne:**

| Wywołanie | Przeznaczenie |
|---|---|
| `pl:claim-drafter` | Pozwy (cywilne / gospodarcze / administracyjne), powództwa wzajemne, modyfikacje, opłata sądowa |
| `pl:response-drafter` | Odpowiedź na pozew, sprzeciwy (od wyroku zaocznego, od nakazu zapłaty), zarzuty od nakazu nakazowego |
| `pl:appeal-drafter` | Apelacja, skarga kasacyjna do SN, zażalenia, skarga kasacyjna do NSA |
| `pl:motion-drafter` | Wnioski procesowe (zabezpieczenie, dowody, biegli, wyłączenie sędziego, terminy) |
| `pl:legislation-analyst` | Analiza obowiązującego prawa, wykładnia norm, brzmienie na datę, dobór orzecznictwa |
| `pl:legal-memo` | Opinie prawne, memoranda, ocena perspektyw sporu |
| `pl:request-drafter` | Wnioski o udostępnienie informacji publicznej (UDIP), pisma adwokata / radcy prawnego, KPA |
| `pl:contract-drafter` | Sporządzanie i analiza umów cywilnoprawnych i gospodarczych, RODO; **tryb audytu ryzyk** (review-only) z ustrukturyzowanym raportem (KRYTYCZNE / ISTOTNE / POŻĄDANE) |

**Windykacja i egzekucja:**

| Wywołanie | Przeznaczenie |
|---|---|
| `pl:debt-collector` | Windykacja: wezwanie → pozew (nakazowe / upominawcze / EPU) → egzekucja; odsetki (art. 481 KC, PNOTH) |
| `pl:enforcement-agent` | Postępowanie egzekucyjne: wnioski do komornika, skargi na czynności (art. 767 KPC), klauzula wykonalności |

**Arbitraż:**

| Wywołanie | Przeznaczenie |
|---|---|
| `pl:arbitration-agent` | Arbitraż międzynarodowy i krajowy (SAKIG, Lewiatan, ICC, LCIA, SCC, SIAC, HKIAC, VIAC, UNCITRAL ad hoc, ICSID), Request for Arbitration, klauzule arbitrażowe, uznanie / uchylenie wyroku (art. 1205–1217 KPC + NYC 1958) |

**Specjalistyczne obszary:**

| Wywołanie | Przeznaczenie |
|---|---|
| `pl:family-drafter` | Sprawy rodzinne: rozwód, separacja, alimenty, władza rodzicielska, kontakty, ustalenie / zaprzeczenie ojcostwa, dział majątku wspólnego (KRO + KPC) |
| `pl:labor-drafter` | Sprawy pracownicze: pozwy o przywrócenie / odszkodowanie, wypowiedzenie umowy, art. 52 KP, mobbing, dyskryminacja, ustalenie istnienia stosunku pracy |
| `pl:inheritance-drafter` | Sprawy spadkowe: stwierdzenie nabycia spadku, dział spadku, zachowek, testamenty, odrzucenie spadku (KC Ks. IV + KPC Ks. IV) |
| `pl:criminal-complaint-drafter` | Zawiadomienie o popełnieniu przestępstwa, prywatny akt oskarżenia, subsydiarny akt oskarżenia, zażalenia na postanowienia o umorzeniu (KPK) |
| `pl:consumer-drafter` | Sprawy konsumenckie: reklamacje, odstąpienie, klauzule abuzywne, kredyty frankowe (CHF), skargi do UOKiK i Rzecznika Finansowego |
| `pl:rodo-compliance` | Ochrona danych osobowych: polityki, klauzule informacyjne, umowy powierzenia, DPIA, zgłoszenia naruszeń, skargi do PUODO (RODO + UODO) |

### Skille (`skills/`)

**Narzędzia bazowe:**

| Wywołanie | Kiedy stosować |
|---|---|
| `pl:fetching-isap-sejm` | Pobieranie aktów z ISAP / Dziennika Ustaw, brzmienia historyczne, ID kluczowych kodeksów |
| `pl:searching-orzeczenia` | Wyszukiwanie orzecznictwa (Portal Orzeczeń SP, SN, NSA, TK), struktura sygnatury akt |
| `pl:citing-polish-law` | Format cytowania aktów prawnych, orzeczeń SN/TK/TSUE/ETPCz, skróty kodeksów |
| `pl:determining-pl-jurisdiction` | Właściwość sądu (rzeczowa, miejscowa, funkcjonalna), cywilna vs gospodarcza vs administracyjna |
| `pl:determining-wps` | Wartość przedmiotu sporu (art. 19–26 KPC), sumowanie żądań, wpływ na właściwość i opłatę |
| `pl:searching-krs` | KRS, CEIDG, biała lista VAT, KRD / BIG, MSiG — identyfikacja osób prawnych i wierzytelności |

**Przedawnienie i odsetki:**

| Wywołanie | Kiedy stosować |
|---|---|
| `pl:checking-przedawnienie` | Terminy przedawnienia (art. 117–125 KC), reforma 2018, ex officio dla konsumentów |
| `pl:calculating-odsetki` | Odsetki ustawowe (art. 359 KC), za opóźnienie (art. 481 KC), w transakcjach handlowych (ustawa 2013), rekompensata 40/70/100 euro |

**Opłaty i koszty:**

| Wywołanie | Kiedy stosować |
|---|---|
| `pl:calculating-oplata-sadowa` | Obliczanie opłat sądowych wg UKSC (skala po reformie 2019), zwolnienia |
| `pl:calculating-alimenty` | Wysokość alimentów (art. 135 KRO), usprawiedliwione potrzeby vs. możliwości zobowiązanego, zabezpieczenie (art. 754¹ KPC), Fundusz Alimentacyjny |

**Arbitraż i sprawy międzynarodowe:**

| Wywołanie | Kiedy stosować |
|---|---|
| `pl:fetching-arbitration-rules` | Aktualne regulaminy sądów arbitrażowych (SAKIG, Lewiatan, ICC, LCIA, SCC, SIAC, HKIAC, VIAC, UNCITRAL, ICSID); brzmienia wg daty arbitrażu |
| `pl:applying-new-york-convention` | Uznanie / stwierdzenie wykonalności zagranicznego wyroku arbitrażowego w Polsce; mapowanie art. V NYC na art. 1215 § 2 KPC; klauzula porządku publicznego |

**Sprawy konsumenckie i RODO:**

| Wywołanie | Kiedy stosować |
|---|---|
| `pl:applying-frankowicze-case-law` | Kredyty CHF: TSUE C-260/18 Dziubak, C-520/21 Bank M., C-287/22 Getin, C-140/22 mBank; uchwały SN III CZP 6/21, III CZP 11/21; teoria dwóch kondykcji, zabezpieczenie powództwa |
| `pl:applying-rodo` | RODO 2016/679 + UODO 10.05.2018: podstawy prawne art. 6/9, obowiązki informacyjne art. 13/14, umowa powierzenia art. 28, DPIA art. 35, naruszenia art. 33/34, transfery po *Schrems II* |

**Audyt umów (checklist + red flags dla `pl:contract-drafter` w trybie audytu):**

| Wywołanie | Kiedy stosować |
|---|---|
| `pl:reviewing-vehicle-contract` | Audyt umowy kupna-sprzedaży pojazdu: VIN / przebieg / obciążenia (CEPiK, Rejestr Zastawów, biała lista VAT); typowe schematy (cofnięty licznik, klonowany VIN, pełnomocnictwa-pułapki, niezakończony leasing); obowiązki po zakupie (30 dni CEPiK, PCC-3 14 dni) |
| `pl:reviewing-real-estate-contract` | Audyt umowy sprzedaży nieruchomości: KW (działy I–IV), hipoteki, służebności, dożywocie, prawa pierwokupu (gmina, KOWR, spółdzielnia, konserwator); zadatek vs. zaliczka (art. 394 KC); forma aktu notarialnego (art. 158 KC); PCC-3 2% vs VAT 8% / 23%; depozyt notarialny |

**Procedury administracyjne (urzędy publiczne):**

| Wywołanie | Kiedy stosować |
|---|---|
| `pl:applying-usc-procedures` | Urząd Stanu Cywilnego: rejestracja urodzenia, małżeństwo cywilne i konkordatowe, zmiana imienia / nazwiska, transkrypcja zagranicznych aktów, odpisy; ustawa z 28.11.2014 o ASC; opłaty skarbowe; e-usługi gov.pl |
| `pl:applying-zus-procedures` | ZUS: rejestracja płatnika (ZFA / ZPA) i ubezpieczonych (ZUA), zasiłki (Z-3 / Z-15 / Np-7), emerytury i renty (Rp-1E / Rp-1R / Rp-2), ulgi w spłacie (RSR / RSO / RSU); odwołanie do sądu ubezpieczeń społecznych (art. 477⁹ KPC); PUE ZUS |
| `pl:applying-skarbowy-procedures` | US / KAS: rejestracja NIP i VAT (VAT-R), czynny żal (art. 16 KKS), korekta deklaracji (art. 81 OP), ulgi (art. 67a OP), interpretacja indywidualna KIS (art. 14b OP), odwołanie DIAS, skarga do WSA / NSA, KSeF |
| `pl:applying-cudzoziemcy-procedures` | Urząd wojewódzki: pobyt czasowy (art. 114 praca / art. 127 Blue Card / art. 144 studia / art. 158 rodzina), stały (art. 195), rezydent UE (art. 211), zezwolenia na pracę A–E, obywatelstwo (UOb); MOS; odwołanie do Szefa UdSC |

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

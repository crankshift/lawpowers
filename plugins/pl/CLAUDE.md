# lawpowers / pl

Przestrzeń robocza do pracy z polskim prawem oraz dokumentami prawniczymi. Zawiera wyspecjalizowanych subagentów pod konkretne zadania prawne.

## Język komunikacji

- Język podstawowy projektu — **polski**. Wszystkie dokumenty, odpowiedzi, szablony i prompty agentów formułowane są po polsku.
- Terminologia prawnicza — według obowiązującego prawa polskiego (KC, KPC, KK, KPK, KP, KRO, KSH, KPA, PPSA itd.).
- Cytaty z aktów normatywnych przytaczać dosłownie, ze wskazaniem artykułu / paragrafu / ustępu / punktu i źródła.

## Planowana architektura agentów

Każdy obszar pracy wynoszony jest do osobnego subagenta (`agents/*.md` w katalogu plagina). Agenci mają wąską specjalizację — nie miesza się odpowiedzialności.

### 1. `claim-drafter` — sporządzanie pozwów

- Przygotowanie pozwów (cywilnych, gospodarczych, administracyjnych) wg wymogów art. 187 KPC / art. 57 PPSA.
- Obowiązkowe elementy: oznaczenie sądu, strony, wartość przedmiotu sporu, uzasadnienie, dowody, żądanie, załączniki.
- Obliczenie i potwierdzenie uiszczenia opłaty sądowej (UKSC).
- Sprawdzenie właściwości sądu i terminów przedawnienia.

### 2. `legislation-analyst` — analiza ustawodawstwa

- Źródło pierwotne: **isap.sejm.gov.pl** (Internetowy System Aktów Prawnych Sejmu RP) oraz **dziennikustaw.gov.pl** (Dziennik Ustaw).
- Sprawdzenie obowiązującego brzmienia normy na konkretną datę, śledzenie zmian, analiza przepisów przejściowych.
- Dodatkowe źródła: orzeczenia.ms.gov.pl (Portal Orzeczeń sądów powszechnych), sn.pl (Sąd Najwyższy), nsa.gov.pl (NSA), trybunal.gov.pl (TK).
- Każde twierdzenie poprzeć bezpośrednim odesłaniem do źródła pierwotnego z datą weryfikacji.

### 3. `request-drafter` — wnioski o informację publiczną i pisma do organów

- **Wniosek o udostępnienie informacji publicznej** — ustawa z 06.09.2001 o dostępie do informacji publicznej (UDIP): forma, terminy (14 dni, max 2 mies. przy danych przetworzonych), podstawy odmowy, tryb odwołania.
- **Pisma adwokata / radcy prawnego** o wydanie dokumentów / informacji w związku ze świadczeniem pomocy prawnej (art. 4 i nast. Prawa o adwokaturze; art. 6 ustawy o radcach prawnych).
- **Wniosek do organu administracji** w trybie KPA (skarga, wniosek, podanie).
- Rozróżniać tryby — nie mylić informacji publicznej z dostępem do akt administracyjnych (art. 73 KPA) ani z dostępem do akt sądowych.

### 4. Pozostali agenci (dodawani według potrzeb)

- Praca umowna, postępowanie windykacyjne, postępowanie egzekucyjne, reprezentacja w sądach, środki zaskarżenia (apelacja, skarga kasacyjna, zażalenie), opinie prawne, RODO/UODO itd.

## Kluczowe źródła

| Źródło | URL | Przeznaczenie |
|---|---|---|
| ISAP — Internetowy System Aktów Prawnych | isap.sejm.gov.pl | Źródło pierwotne tekstów aktów prawnych |
| Dziennik Ustaw | dziennikustaw.gov.pl | Oficjalny publikator |
| Monitor Polski | monitorpolski.gov.pl | Akty wewnętrzne, obwieszczenia |
| Portal Orzeczeń SP | orzeczenia.ms.gov.pl | Orzeczenia sądów powszechnych |
| Sąd Najwyższy | sn.pl | Uchwały, wyroki SN |
| NSA / WSA | orzeczenia.nsa.gov.pl, nsa.gov.pl | Orzecznictwo sądów administracyjnych |
| Trybunał Konstytucyjny | trybunal.gov.pl | Wyroki i postanowienia TK |
| Ministerstwo Sprawiedliwości | gov.pl/web/sprawiedliwosc | Wykazy sądów, formularze |
| Krajowy Rejestr Sądowy | krs.ms.gov.pl, ekrs.ms.gov.pl | Rejestr przedsiębiorców i stowarzyszeń |
| EUR-Lex | eur-lex.europa.eu | Akty UE, orzecznictwo TSUE |
| ETPCz | hudoc.echr.coe.int | Orzecznictwo Europejskiego Trybunału Praw Człowieka |

## Zasady pracy

- **Dosłowność cytatów.** Norma przytaczana w dokładnym brzmieniu obowiązującym na wskazaną datę. Parafraza — dopiero po cytacie i jednoznacznie oznaczona jako parafraza.
- **Odesłania obowiązkowe.** Każde stanowisko prawne — z odesłaniem do artykułu + źródła + daty weryfikacji. Bez „gdzieś czytałem" i bez polegania wyłącznie na pamięci modelu.
- **Aktualność.** Polskie prawo zmienia się często (zwłaszcza KPC, KSH, ustawy podatkowe). Przed powołaniem normy — sprawdzić obowiązujące brzmienie w ISAP.
- **Ostrożność z poradami.** Materiały projektu — robocze projekty dla prawnika-użytkownika, nie końcowa porada prawna dla klienta. Ostateczną redakcję i odpowiedzialność ponosi człowiek.
- **Nie wymyślać orzecznictwa.** Sygnatury akt, daty wyroków, cytaty z orzeczeń — wyłącznie ze sprawdzonych źródeł (Portal Orzeczeń / SN / NSA). Wątpliwe — oznaczać jako niezweryfikowane.
- **Dane osobowe.** W szablonach używać placeholderów (`[imię i nazwisko]`, `[PESEL]`, `[adres]`, `[KRS]`, `[NIP]`), nie przechowywać rzeczywistych danych klientów w plikach projektu.
- **RODO.** Przy projektowaniu klauzul, polityk i analizach — odwołania do RODO (Rozporządzenie 2016/679) i ustawy z 10.05.2018 o ochronie danych osobowych.

## Agenci

Wąsko wyspecjalizowani subagenci w `agents/` (korzeń plagina):

**Postępowania sądowe — ogólne:**

| Agent | Przeznaczenie |
|---|---|
| `claim-drafter` | Sporządzanie pozwów (cywilne / gospodarcze / administracyjne), powództw wzajemnych, modyfikacji powództwa, obliczanie opłaty sądowej |
| `legislation-analyst` | Analiza obowiązującego prawa, wyszukiwanie i wykładnia norm, sprawdzanie brzmienia na datę, dobór orzecznictwa, opinie prawne |
| `request-drafter` | Wnioski o udostępnienie informacji publicznej (UDIP), pisma adwokata/radcy o wydanie dokumentów, wnioski w trybie KPA |
| `response-drafter` | Odpowiedź na pozew, sprzeciwy (od wyroku zaocznego, nakazu zapłaty), zarzuty od nakazu zapłaty, pisma procesowe pozwanego |
| `appeal-drafter` | Apelacja, skarga kasacyjna do SN, zażalenia, skarga o stwierdzenie niezgodności z prawem prawomocnego orzeczenia, skarga kasacyjna do NSA |
| `motion-drafter` | Wnioski procesowe: zabezpieczenie powództwa/dowodów, dopuszczenie dowodu, biegli, świadkowie, wyłączenie sędziego, przywrócenie terminu, odroczenie itd. |
| `contract-drafter` | Praca umowna: sporządzanie i analiza umów cywilnoprawnych i gospodarczych (sprzedaż, najem, dzieło, zlecenie, dystrybucja, NDA), audyt ryzyk |
| `legal-memo` | Opinie prawne i memoranda dla klienta; analiza perspektyw sporu; porównanie wariantów działania |

**Windykacja i egzekucja:**

| Agent | Przeznaczenie |
|---|---|
| `debt-collector` | Windykacja należności: wezwanie do zapłaty → pozew (postępowanie nakazowe / upominawcze / zwykłe) → egzekucja; obliczanie odsetek (art. 481 KC) |
| `enforcement-agent` | Postępowanie egzekucyjne: wnioski egzekucyjne do komornika, skargi na czynności komornika (art. 767 KPC), klauzula wykonalności |

**Arbitraż:**

| Agent | Przeznaczenie |
|---|---|
| `arbitration-agent` | Arbitraż międzynarodowy i krajowy: SAKIG przy KIG, Sąd Arbitrażowy Lewiatan, ICC / LCIA / SCC / SIAC / HKIAC / VIAC, ad hoc UNCITRAL, arbitraż inwestycyjny (ICSID/BIT/ECT); uznanie i uchylenie wyroku sądu polubownego w polskim sądzie apelacyjnym (art. 1205–1217 KPC + NYC 1958) |

**Specjalistyczne obszary:**

| Agent | Przeznaczenie |
|---|---|
| `family-drafter` | Sprawy rodzinne: pozwy o rozwód / separację, alimenty (art. 133 KRO), władzę rodzicielską (art. 109–111 KRO), kontakty (art. 113 KRO), ustalenie / zaprzeczenie ojcostwa, podział majątku wspólnego; zabezpieczenie art. 754¹ KPC |
| `labor-drafter` | Sprawy pracownicze: pozwy o przywrócenie / odszkodowanie (art. 45, 56 KP), ustalenie istnienia stosunku pracy (art. 22 § 1¹ KP), wypowiedzenia, dyscyplinarki (art. 52 KP), mobbing i dyskryminacja, sprostowanie świadectwa pracy |
| `inheritance-drafter` | Sprawy spadkowe: stwierdzenie nabycia spadku, dział spadku, zachowek (art. 991–1011 KC), testamenty, odrzucenie / przyjęcie spadku (termin 6 miesięcy — art. 1015 KC) |
| `criminal-complaint-drafter` | Postępowanie karne po stronie pokrzywdzonego: zawiadomienie o popełnieniu przestępstwa (art. 304 KPK), prywatny akt oskarżenia (art. 487 KPK), subsydiarny akt oskarżenia (art. 55 KPK), zażalenia (art. 306 KPK) |
| `consumer-drafter` | Sprawy konsumenckie: klauzule abuzywne (art. 385¹ KC), rękojmia, odstąpienie w 14 dni, kredyty CHF (frankowicze), skargi do UOKiK i Rzecznika Finansowego |
| `rodo-compliance` | Ochrona danych osobowych: dokumentacja administratora, klauzule informacyjne, umowy powierzenia (art. 28 RODO), DPIA (art. 35 RODO), zgłoszenia naruszeń (art. 33/34 RODO), obsługa wniosków z art. 15–22 RODO, skargi do PUODO |

## Skille

Proceduralne / referencyjne skille w `skills/` (korzeń plagina) — używać przy pracy z polskimi źródłami prawa:

**Narzędzia bazowe:**

| Skill | Kiedy stosować |
|---|---|
| `fetching-isap-sejm` | Pobieranie aktów z ISAP / Dziennika Ustaw; URL dla brzmień historycznych; tabela ID kluczowych kodeksów i ustaw |
| `searching-orzeczenia` | Wyszukiwanie orzecznictwa: Portal Orzeczeń SP, SN, NSA; struktura sygnatury akt; weryfikacja prawomocności |
| `citing-polish-law` | Format cytowania aktów prawnych, orzeczeń SN/TK/TSUE/ETPCz; skróty kodeksów i ustaw |
| `determining-pl-jurisdiction` | Właściwość sądu (rzeczowa, miejscowa, funkcjonalna); cywilna vs gospodarcza vs administracyjna; sąd rejonowy vs okręgowy |
| `determining-wps` | Wartość przedmiotu sporu (art. 19–26 KPC); sumowanie żądań; wyłączenia (odsetki, koszty); wpływ na właściwość i opłatę |
| `searching-krs` | KRS, CEIDG, biała lista VAT, KRD / BIG / ERIF, MSiG — identyfikacja osób prawnych, sposób reprezentacji, postępowania upadłościowe |

**Przedawnienie i odsetki:**

| Skill | Kiedy stosować |
|---|---|
| `checking-przedawnienie` | Terminy przedawnienia (art. 117–125 KC); reforma 2018 (6 lat / koniec roku kalendarzowego); uwzględnienie z urzędu wobec konsumenta |
| `calculating-odsetki` | Odsetki ustawowe (art. 359 KC), za opóźnienie (art. 481 KC), w transakcjach handlowych (ustawa z 08.03.2013); rekompensata 40/70/100 euro; odsetki maksymalne |

**Opłaty i koszty:**

| Skill | Kiedy stosować |
|---|---|
| `calculating-oplata-sadowa` | Obliczanie opłat sądowych wg UKSC; opłata stosunkowa, stała, podstawowa; zwolnienia ustawowe i na wniosek |
| `calculating-alimenty` | Wysokość alimentów (art. 135 KRO) — usprawiedliwione potrzeby vs. możliwości zobowiązanego; zasada równej stopy życiowej; zabezpieczenie art. 754¹ KPC; Fundusz Alimentacyjny |

**Arbitraż i sprawy międzynarodowe:**

| Skill | Kiedy stosować |
|---|---|
| `fetching-arbitration-rules` | Aktualne regulaminy sądów arbitrażowych (SAKIG, Lewiatan, ICC, LCIA, SCC, SIAC, HKIAC, VIAC, UNCITRAL, ICSID); brzmienia historyczne wg daty Request for Arbitration |
| `applying-new-york-convention` | Uznanie i stwierdzenie wykonalności zagranicznego wyroku arbitrażowego w Polsce; mapowanie art. V NYC 1958 na art. 1215 § 2 KPC; klauzula porządku publicznego (wąskie tłumaczenie wg SN) |

**Sprawy konsumenckie i RODO:**

| Skill | Kiedy stosować |
|---|---|
| `applying-frankowicze-case-law` | Kredyty CHF: TSUE C-260/18 *Dziubak*, C-520/21 *Bank M.*, C-287/22 *Getin*, C-140/22 *mBank*; uchwały SN III CZP 6/21 (teoria dwóch kondykcji), III CZP 11/21; zabezpieczenie powództwa; argumentacja nieważności klauzul indeksacyjnych |
| `applying-rodo` | Mapowanie artykułów RODO do obowiązków administratora; podstawy prawne art. 6 / 9; klauzule informacyjne art. 13–14; umowa powierzenia art. 28; DPIA art. 35; naruszenia art. 33–34; transfery po *Schrems II* (C-311/18) |

## Struktura projektu

Plagin `pl` jest częścią monorepo `lawpowers` (zob. root [`CLAUDE.md`](../../CLAUDE.md)). Jego pliki znajdują się w `plugins/pl/`:

```
lawpowers/                        # repo: crankshift/lawpowers
├── .claude-plugin/
│   └── marketplace.json          # katalog marketplace'u z plaginami ua i pl
└── plugins/
    ├── ua/                       # plagin "ua" (ukraińskie prawo)
    └── pl/                       # ← ten plagin
        ├── CLAUDE.md             # ten plik
        ├── README.md
        ├── CHANGELOG.md
        ├── .claude-plugin/
        │   └── plugin.json       # manifest plagina (name: "pl")
        ├── agents/
        │   ├── claim-drafter.md
        │   ├── response-drafter.md
        │   ├── appeal-drafter.md
        │   ├── motion-drafter.md
        │   ├── legislation-analyst.md
        │   ├── legal-memo.md
        │   ├── request-drafter.md
        │   ├── contract-drafter.md
        │   ├── debt-collector.md
        │   └── enforcement-agent.md
        └── skills/
            ├── fetching-isap-sejm/SKILL.md
            ├── searching-orzeczenia/SKILL.md
            ├── calculating-oplata-sadowa/SKILL.md
            ├── citing-polish-law/SKILL.md
            ├── determining-pl-jurisdiction/SKILL.md
            └── checking-przedawnienie/SKILL.md
```

**Ważne:** po instalacji plagina wszystkie skille i agenci mają prefiks `/pl:…` (namespace z pola `name` w `plugin.json`) — np. `pl:claim-drafter`, `pl:searching-orzeczenia`. Zapobiega to konfliktom z innymi plaginami w marketplace `lawpowers` (w szczególności z `ua:…`).

## Zasady nazewnictwa

- **Pliki agentów/skilli** — bez prefiksu (`claim-drafter.md`, `skills/searching-orzeczenia/SKILL.md`). Prefiks `pl:` dodawany jest automatycznie z pola `name` w `plugin.json`.
- **W dokumentacji** — odwoływać się do agentów przez wywołanie (`pl:claim-drafter`), żeby użytkownik widział dokładną komendę.
- **Nowi agenci/skille** — dodawać bez prefiksu w nazwie; otrzymają `pl:` automatycznie.

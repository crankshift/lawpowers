# Plagin `pl` — Changelog

Historia zmian plagina `pl` (polskie prawo) w ramach monorepo [`lawpowers`](../../CHANGELOG.md).

Format — [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Od wydań po v0.6.0 plagin jest tagowany osobno jako `pl/vX.Y.Z` (gdzie `X.Y.Z` odpowiada polu `version` w `plugin.json`). Wpisy historyczne poniżej (do 0.2.0 włącznie) były wydawane w ramach wspólnych tagów marketplace'u `vX.Y.Z` i zachowują linki do nich.

## [0.3.2] — 2026-04-26

### Changed — fetch-first z fallbackiem dla wszystkich wartości liczbowych

Wszystkie skille i agenci zawierające zakodowane wartości prawne (stawki, opłaty, minimalne wynagrodzenie, progi) stosują teraz jednolity wzorzec: **najpierw próba pobrania aktualnej wartości ze źródła oficjalnego (WebFetch/WebSearch), a w razie niepowodzenia — użycie zakodowanej wartości z ostrzeżeniem dla użytkownika**.

- **10 plików zaktualizowanych** (7 skilli + 1 agent z blokami fetch-first; 2 skille z lekkimi adnotacjami):
  - `calculating-odsetki` — fetch stopy referencyjnej NBP z nbp.pl + kursu EUR/PLN.
  - `calculating-oplata-sadowa` — fetch skali opłat z UKSC w ISAP.
  - `labor-drafter` — fetch minimalnego wynagrodzenia z rozporządzenia RM w ISAP.
  - `applying-cudzoziemcy-procedures` — fetch opłat za pobyt czasowy/stały z rozporządzenia MSWiA.
  - `applying-usc-procedures` — fetch opłat skarbowych z ustawy o opłacie skarbowej.
  - `applying-skarbowy-procedures` — fetch progu VAT (art. 113) i białej listy.
  - `reviewing-real-estate-contract` — fetch stawki PCC i VAT z ISAP.
  - `reviewing-vehicle-contract` — fetch PCC + kary OC z UFG.
  - `determining-wps` — adnotacja progów jurysdykcyjnych (art. 17 KPC, art. 505¹ KPC).
  - `calculating-alimenty` — fetch kryterium dochodowego Funduszu Alimentacyjnego.
- **Wszystkie zakodowane kwoty** opatrzone `_(fallback; stan na [data])_` — data ostatniej weryfikacji widoczna w tekście.
- **Cross-references:** stopa NBP dla pozostałych skilli odwołuje się do kanonicznego `calculating-odsetki`.

### Bumped

- Plagin `pl`: `0.3.1` → `0.3.2`.

[0.3.2]: https://github.com/crankshift/lawpowers/releases/tag/pl/v0.3.2

## [0.3.1] — 2026-04-22

### Changed — optymalizacja tokenów (~55% stałego overheadu)

Bez zmian funkcjonalnych. Zmniejszono rozmiar metadanych, które Claude Code ładuje do głównego kontekstu na **każdym obrocie** — zanim jeszcze zacznie się rzeczywista praca. Ciała agentów i skilli (cała procedura i zawartość merytoryczna) pozostają bez zmian.

- **Opisy agentów** (`description:` we frontmatter, 17 agentów) — skrócono najdłuższe (najbardziej: `pl:arbitration-agent` 1220 → ~500 znaków, `pl:consumer-drafter` 1015 → ~420). Zachowano słowa kluczowe routingu, nazwy instytucji, numery artykułów. Usunięto listy wyłączeń („NIE wywoływać dla…") i wyliczenia podstaw prawnych, które i tak są w ciele agenta.
- **Opisy skilli** (20 skilli) — analogicznie. Największe (`applying-zus-procedures` 823, `applying-skarbowy-procedures` 789, `applying-cudzoziemcy-procedures` 789, `reviewing-real-estate-contract` 710) skrócono; zachowano wszystkie słowa-triggery i zakotwiczenia w artykułach.
- **`plugins/pl/CLAUDE.md`** — przepisany. Było 208 linii, jest 28. Usunięto zduplikowane katalogi agentów/skilli (dostępne dla Claude przez listing), sekcję planowanej architektury, drzewo katalogów, zasady nazewnictwa — wszystko to jest w `README.md` albo dotyczy wyłącznie kontrybutorów. Pozostawiono reguły runtime: język, dosłowność cytatów, źródło pierwotne (ISAP), zakaz wymyślania orzecznictwa, placeholdery dla danych osobowych, disclaimer „projekt, nie porada", zasada aktualności (KPC / KSH / ustawy podatkowe).

**Zmierzone oszczędności na obrót** (szacunkowo, 4 znaki/token):

| Blok | Przed | Po | Oszczędność |
|---|---:|---:|---:|
| `CLAUDE.md` | ~4 300 tok. | ~480 tok. | ~3 820 |
| Opisy agentów | ~2 780 tok. | ~1 720 tok. | ~1 060 |
| Opisy skilli | ~2 340 tok. | ~1 880 tok. | ~460 |
| **Razem** | **~9 420** | **~4 080** | **~5 340** |

### Bumped

- Plagin `pl`: `0.3.0` → `0.3.1`.

### Migracja

Bez zmian breaking. Routing między agentami i triggery skilli zweryfikowane — słowa kluczowe zachowane. Aktualizacja:

```
/plugin marketplace update lawpowers
/reload-plugins
```

## [0.3.0] — 2026-04-22

### Added — tryb audytu ryzyk w `contract-drafter`

- **`pl:contract-drafter`** — uzupełniono o osobny **tryb audytu ryzyk** (review-only). Uruchamiany, gdy klient prosi o „audyt / review / red flags", bez prośby o pełną redakcję. Wynik: ustrukturyzowany raport (I. Podsumowanie → II. Ustalenia po klauzulach z cytatem i podstawą prawną → III. Braki → IV. Lista kontrolna poprawek → V. Zalecenia negocjacyjne). Klasyfikacja ryzyk: **KRYTYCZNE / ISTOTNE / POŻĄDANE**. Zasada „bez przepisywania" — raport listuje poprawki do istniejącego projektu, nie generuje nowej umowy.

### Added — 6 nowych skilli

**Audyt umów (checklist + red flags dla trybu audytu ryzyk):**

- **`pl:reviewing-vehicle-contract`** — umowa kupna-sprzedaży pojazdu. Rejestry do weryfikacji (CEPiK / historiapojazdu.gov.pl, Rejestr Zastawów Skarbowych, biała lista VAT, KRS / CEIDG), katalog red flags (klonowany VIN, cofnięty licznik — art. 306a KK, leasing niezakończony, sprzedaż „na pełnomocnictwo", pojazd sprowadzony bez cła / akcyzy, sprzedaż ze szkodą całkowitą, komisy-krzak spoza białej listy VAT). Obowiązki po zakupie: 30 dni na zgłoszenie zbycia / przerejestrowanie w CEPiK (art. 78 ust. 2 pkt 1, art. 73 PoRD), PCC-3 14 dni 2% lub VAT, zmiana OC (art. 31 ustawy o ubezpieczeniach obowiązkowych).
- **`pl:reviewing-real-estate-contract`** — umowa sprzedaży nieruchomości (akt notarialny — art. 158 KC pod rygorem nieważności). Weryfikacja KW (działy I–IV) z EKW (ekw.ms.gov.pl), EGiB, MPZP / studium / WZ, PINB, KOWR dla gruntów rolnych, rejestr zabytków / Natura 2000. Red flags: hipoteki, ostrzeżenia o niezgodności, prawa pierwokupu (gmina — art. 109 UoGN, KOWR — art. 2a ustawy o kształtowaniu ustroju rolnego, spółdzielnia — art. 18 ustawy o spółdz. mieszk., konserwator — art. 10 ustawy o ochronie zabytków), dożywocie (art. 908 KC), podwójna sprzedaż. **Zadatek vs. zaliczka** (art. 394 KC) — krytyczne rozróżnienie. PCC-3 2% vs VAT (8% / 23%). Umowa przedwstępna w formie aktu notarialnego (art. 390 § 2 KC) — zalecana dla kupującego z finansowaniem. Depozyt notarialny (art. 108 PrNot) jako bezpieczny mechanizm rozliczeń.

**Procedury administracyjne (urzędy publiczne):**

- **`pl:applying-usc-procedures`** — Urząd Stanu Cywilnego. Ustawa z 28.11.2014 o aktach stanu cywilnego (ASC). Rejestracja urodzenia (art. 60–69 ASC — 21 dni), zawarcie małżeństwa cywilnego (art. 76–85 — zgłoszenie ≥ 31 dni wcześniej; opłata 84 zł) i konkordatowego (art. 86–87; zaświadczenie ważne 6 miesięcy), zmiana imienia / nazwiska (ustawa z 17.10.2008; opłata 37 zł), transkrypcja zagranicznych aktów (art. 104–108 ASC; apostille dla państw haskiej konw. 1961; opłata 50 zł), sprostowanie / unieważnienie aktu (art. 35–39), odpisy (skrócone, zupełne, wielojęzyczne CIEC). E-usługi gov.pl / moj.gov.pl. Odwołanie do wojewody (art. 127 § 2 KPA, 14 dni); WSA / NSA.
- **`pl:applying-zus-procedures`** — Zakład Ubezpieczeń Społecznych. Ustawa z 13.10.1998 o systemie ubezpieczeń społecznych (SUS); ustawa z 25.06.1999 o świadczeniach pieniężnych z ubezp. społecznego w razie choroby i macierzyństwa; ustawa z 17.12.1998 o emeryturach i rentach z FUS. Rejestracja płatnika (ZUS ZFA / ZPA) i ubezpieczonych (ZUA / ZCNA) — 7 dni od powstania tytułu. Zasiłki chorobowy / macierzyński / opiekuńczy / rehabilitacyjny (formularze Z-3, Z-3a, Z-15A, Z-15B, Np-7) z okresami wyczekiwania 30 / 90 dni. Emerytury (Rp-1E) i renty (Rp-1R / Rp-2), renta socjalna. Ulgi w spłacie (RSR / RSO / RSU, art. 29–33 SUS). PUE ZUS i e-ZLA jako standardowy kanał. Specyfika odwołania: **brak odwołania KPA** — **sprawa trafia bezpośrednio do sądu** (art. 477⁸ i nast. KPC) — 1 miesiąc; zwolnienie z opłat sądowych (art. 96 ust. 1 pkt 4 UKSC).
- **`pl:applying-skarbowy-procedures`** — urząd skarbowy / KAS. Ordynacja podatkowa (art. 48 przedłużenie terminu, art. 67a ulgi, art. 72 nadpłata, art. 81 korekta deklaracji, art. 14b interpretacja indywidualna Dyrektora KIS w 3 mies. za 40 zł, art. 70 przedawnienie 5 lat). Rejestracja NIP (NIP-2 / NIP-7 / NIP-8) i VAT (VAT-R); biała lista VAT; **KSeF** (obowiązkowy od 01.02.2026 — harmonogram po poślizgu). **Czynny żal** (art. 16 KKS) — warunki wyłączenia odpowiedzialności karno-skarbowej; szablon pisma. Kontrola podatkowa i postępowanie podatkowe (dział IV OP), prawo do wypowiedzenia się w 7 dni przed decyzją (art. 200 OP). Odwołanie do DIAS w 14 dni (art. 220 OP); skarga do WSA w 30 dni (wpis 500 zł); skarga kasacyjna do NSA w 30 dni z przymusem pełnomocnika.
- **`pl:applying-cudzoziemcy-procedures`** — urząd wojewódzki / Szef UdSC / Prezydent RP. Ustawa z 12.12.2013 o cudzoziemcach (UC): zezwolenie na pobyt czasowy (art. 114 praca, art. 127 Blue Card, art. 144 studia, art. 158–166 rodzina, art. 142 działalność gospodarcza) — 440 zł; stały (art. 195) — 640 zł; rezydent UE (art. 211) — 640 zł po 5 latach pobytu + B1. Ustawa z 20.04.2004 o promocji zatrudnienia: zezwolenie na pracę typy A–E + oświadczenie o powierzeniu pracy dla AM/BY/GE/MD/UA — 24 miesiące od 11.2023. Ustawa z 02.04.2009 o obywatelstwie polskim: nadanie przez Prezydenta RP (art. 18 i nast. — brak odwołania) vs. uznanie za obywatela polskiego (art. 30 — decyzja wojewody, odwołanie do MSWiA, WSA). Karta Polaka. MOS (Moduł Obsługi Spraw). Stempel w paszporcie (art. 108 UC) legalizujący pobyt w trakcie postępowania.

### Bumped

- Plagin `pl`: `0.2.0` → `0.3.0`.

### Migracja

Bez zmian breaking. Nowy tryb audytu w `pl:contract-drafter` nie zmienia dotychczasowych wywołań — aktywuje się przy żądaniu „audytu / review / red flags". Nowe skille dostępne automatycznie:

```
/plugin marketplace update lawpowers
/reload-plugins
```

W katalogu `/agents` i `/skills` widoczne 17 agentów i 20 skilli pod prefiksem `pl:`.

## [0.2.0] — 2026-04-21

### Added — 7 nowych subagentów

Rozszerzenie plagina o specjalistyczne obszary najczęściej potrzebne polskim prawnikom-praktykom, odzwierciedlające pełny zakres plagina `ua` w polskiej specyfice oraz uzupełniające o kategorie typowo polskie (frankowicze, RODO, prawo rodzinne i spadkowe).

**Arbitraż:**

- **`pl:arbitration-agent`** — postępowanie arbitrażowe międzynarodowe i krajowe. Obejmuje: Sąd Arbitrażowy przy KIG (SAKIG), Sąd Arbitrażowy Lewiatan, ICC, LCIA, SCC, SIAC, HKIAC, VIAC, UNCITRAL ad hoc, arbitraż inwestycyjny (ICSID / BIT / ECT z uwzględnieniem *Achmea* C-284/16 i *Komstroy* C-741/19 dla intra-EU). Sporządza Request for Arbitration, Statement of Defence, klauzule arbitrażowe (audyt patologiczności), wnioski o uznanie i stwierdzenie wykonalności wyroku arbitrażowego w polskim sądzie apelacyjnym (art. 1212–1217 KPC + NYC 1958), skargi o uchylenie wyroku sądu polubownego (art. 1205–1211 KPC).

**Prawo rodzinne:**

- **`pl:family-drafter`** — sprawy rodzinne w zakresie KRO i KPC. Pozwy o rozwód (z orzekaniem o winie / bez), separację, alimenty dla dziecka (art. 133 KRO) i małżonka (art. 60 KRO), władzę rodzicielską (art. 109–111 KRO), kontakty (art. 113 KRO), ustalenie / zaprzeczenie ojcostwa, podział majątku wspólnego, zabezpieczenie alimentów (art. 754¹ KPC) i kontaktów (art. 755¹ KPC).

**Prawo pracy:**

- **`pl:labor-drafter`** — sprawy pracownicze. Pozwy o przywrócenie do pracy / odszkodowanie za niezgodne wypowiedzenie (art. 45 KP) lub rozwiązanie bez wypowiedzenia (art. 56 KP), ustalenie istnienia stosunku pracy (art. 22 § 1¹ KP — ukryte zatrudnienie), dyscyplinarki (art. 52 KP), mobbing (art. 94³ KP), dyskryminacja (art. 18³ᵃ KP), sprostowanie świadectwa pracy, odprawy. Obsługuje obie strony — pracownika i pracodawcę.

**Prawo spadkowe:**

- **`pl:inheritance-drafter`** — sprawy spadkowe wg Księgi IV KC. Wnioski o stwierdzenie nabycia spadku (art. 669 KPC), dział spadku (art. 680 KPC), pozwy o zachowek (art. 991–1011 KC), oświadczenia o przyjęciu / odrzuceniu spadku (termin 6 miesięcy — art. 1015 KC), testamenty holograficzne / notarialne / ustne, niegodność dziedziczenia (art. 928 KC).

**Prawo karne (strona pokrzywdzonego):**

- **`pl:criminal-complaint-drafter`** — zawiadomienie o popełnieniu przestępstwa (art. 304 KPK), prywatny akt oskarżenia (art. 487 KPK — zniesławienie, zniewaga, naruszenie nietykalności), subsydiarny akt oskarżenia (art. 55 KPK), zażalenia na postanowienia o umorzeniu (art. 306 KPK), wnioski o uzupełnienie postępowania (art. 330 KPK), wnioski o naprawienie szkody (art. 46 KK), zabezpieczenie majątkowe (art. 291 KPK).

**Sprawy konsumenckie:**

- **`pl:consumer-drafter`** — reklamacje, odstąpienie od umowy na odległość (14 dni — art. 27 ustawy o prawach konsumenta), klauzule niedozwolone (art. 385¹ KC), sprawy frankowiczów (kredyty CHF) z aktualnym orzecznictwem TSUE i SN, skargi do UOKiK i Rzecznika Finansowego, wsparcie przez Miejskiego / Powiatowego Rzecznika Konsumentów, pozwy o zwrot ceny i zadośćuczynienie.

**Ochrona danych:**

- **`pl:rodo-compliance`** — pełen program compliance wg RODO 2016/679 i UODO 2018. Polityki prywatności, klauzule informacyjne (art. 13–14 RODO), umowy powierzenia przetwarzania (art. 28 RODO), rejestr czynności (art. 30), ocena skutków DPIA (art. 35), zgłoszenia naruszeń w 72 h (art. 33) i zawiadomienia osób (art. 34), obsługa praw z art. 15–22 (dostęp, usunięcie, przenoszenie, sprzeciw), skargi do PUODO, pozwy cywilne o odszkodowanie (art. 82 RODO + art. 92 UODO), transfery do państw trzecich po *Schrems II* (C-311/18) z TIA i SCC.

### Added — 8 nowych skilli

**Narzędzia bazowe:**

- **`pl:determining-wps`** — wartość przedmiotu sporu wg art. 19–26 KPC. Zasady sumowania żądań, wyłączenia (odsetki, koszty — art. 20 KPC), reguły dla świadczeń powtarzających się (art. 22), wpływ na właściwość rzeczową (art. 17 pkt 4 — okręgowy > 100 000 zł) i opłatę sądową.
- **`pl:searching-krs`** — identyfikacja osób prawnych i przedsiębiorców: KRS (ekrs.ms.gov.pl), CEIDG, biała lista VAT, KRD / BIG / ERIF, MSiG (ogłoszenia o upadłościach), REGON. Weryfikacja sposobu reprezentacji, postępowań upadłościowych / restrukturyzacyjnych przed wniesieniem pozwu.

**Odsetki:**

- **`pl:calculating-odsetki`** — trzy reżimy odsetek cywilnoprawnych: odsetki ustawowe (art. 359 KC), za opóźnienie (art. 481 KC), w transakcjach handlowych (ustawa z 08.03.2013). Odsetki maksymalne (art. 359 § 2¹, art. 481 § 2¹). Rekompensata 40 / 70 / 100 euro w B2B. Podział okresu na podokresy wg zmian stopy referencyjnej NBP.

**Alimenty:**

- **`pl:calculating-alimenty`** — wysokość alimentów wg art. 135 KRO (usprawiedliwione potrzeby + możliwości zarobkowe i majątkowe), zasada równej stopy życiowej, zabezpieczenie alimentów (art. 754¹ KPC — uprzywilejowane), egzekucja alimentów (art. 1081 KPC — zajęcie do 60% wynagrodzenia), Fundusz Alimentacyjny, odpowiedzialność karna (art. 209 KK).

**Arbitraż:**

- **`pl:fetching-arbitration-rules`** — aktualne regulaminy sądów arbitrażowych: SAKIG, Lewiatan, ICC (2021), LCIA (2020), SCC (2023), SIAC (2025), HKIAC (2024), VIAC (2021/2025), UNCITRAL (2013), ICSID (2022). URL, daty wejścia w życie, wyszukiwanie wcześniejszych redakcji, format cytowania.
- **`pl:applying-new-york-convention`** — NYC 1958 mapowana na art. 1212–1217 KPC. Podstawy odmowy uznania (art. V NYC = art. 1215 § 2 KPC) — katalog wyczerpujący. Klauzula porządku publicznego w wąskim tłumaczeniu SN (wyroki III CSK 215/13, V CSK 255/15, I CSK 416/11). Wymogi formalne — art. IV NYC + art. 1213 KPC (apostille, tłumaczenie przysięgłe). Właściwość — sąd apelacyjny. Termin 2 miesięcy na skargę o uchylenie (art. 1208 KPC).

**Sprawy konsumenckie i RODO:**

- **`pl:applying-frankowicze-case-law`** — kompletny zestaw orzecznictwa frankowiczowskiego: TSUE C-260/18 *Dziubak*, C-19/20 *Bank BPH*, C-520/21 *Bank M.*, C-287/22 *Getin* (zabezpieczenie), C-140/22 *mBank* (oświadczenie konsumenta), C-776/19 *BNP Paribas* (przedawnienie); uchwały SN III CZP 6/21 (teoria dwóch kondykcji), III CZP 11/21. Struktura pozwu, żądanie unieważnienia + pieniężne, wniosek o zabezpieczenie powództwa, kontrargumenty dla obrony banków.
- **`pl:applying-rodo`** — szybkie mapowanie artykułów RODO do obowiązków administratora. Dobór podstawy prawnej z art. 6 / 9 wg sytuacji (umowa / obowiązek prawny / uzasadniony interes / zgoda). Checklist dla klauzul informacyjnych (art. 13/14) i umów powierzenia (art. 28). Obsługa praw osób (art. 15–22) z terminami. DPIA (art. 35). Transfery do państw trzecich po *Schrems II* — TIA, SCC (Rozp. 2021/914), EU-US Data Privacy Framework.

### Bumped

- Plagin `pl`: `0.1.0` → `0.2.0`.

### Migracja

Bez zmian breaking — instalacja i wywołania istniejących agentów / skilli nie zmieniają się. Nowe agentki i skille dostępne automatycznie po aktualizacji:

```
/plugin marketplace update lawpowers
/reload-plugins
```

W katalogu `/agents` i `/skills` widoczne 17 agentów i 14 skilli pod prefiksem `pl:`.

## [0.1.0] — 2026-04-20

### Added — pierwsza wersja plagina

Plagin `pl` dla polskiego prawa dodany do monorepo `lawpowers` (tag marketplace: v0.4.0). Poprzednio znajdował się w niezależnym repozytorium `crankshift/legal-pl`; identyfikator skrócono `legal-pl` → `pl`, prefiks komend `/pl:…`.

#### Subagenci (10)

- **`pl:claim-drafter`** — pozwy (cywilne / gospodarcze / administracyjne), powództwa wzajemne, modyfikacje powództwa, opłata sądowa.
- **`pl:response-drafter`** — odpowiedź na pozew, sprzeciwy (od wyroku zaocznego, od nakazu zapłaty), zarzuty od nakazu nakazowego.
- **`pl:appeal-drafter`** — apelacja, skarga kasacyjna do SN, zażalenia, skarga kasacyjna do NSA.
- **`pl:motion-drafter`** — wnioski procesowe: zabezpieczenie, dowody, biegli, wyłączenie sędziego, terminy.
- **`pl:legislation-analyst`** — analiza obowiązującego prawa, wykładnia norm, brzmienie na datę, dobór orzecznictwa.
- **`pl:legal-memo`** — opinie prawne, memoranda, ocena perspektyw sporu.
- **`pl:request-drafter`** — wnioski o udostępnienie informacji publicznej (UDIP), pisma adwokata/radcy, KPA.
- **`pl:contract-drafter`** — sporządzanie i analiza umów cywilnoprawnych i gospodarczych, audyt ryzyk, RODO.
- **`pl:debt-collector`** — windykacja: wezwanie → pozew (nakazowe / upominawcze / EPU) → egzekucja; odsetki (art. 481 KC, PNOTH).
- **`pl:enforcement-agent`** — postępowanie egzekucyjne: wnioski do komornika, skargi na czynności (art. 767 KPC), klauzula wykonalności.

#### Skille (6)

- **`pl:fetching-isap-sejm`** — pobieranie aktów z ISAP / Dziennika Ustaw, brzmienia historyczne, ID kluczowych kodeksów.
- **`pl:searching-orzeczenia`** — wyszukiwanie orzecznictwa (Portal Orzeczeń SP, SN, NSA, TK), struktura sygnatury akt.
- **`pl:calculating-oplata-sadowa`** — obliczanie opłat sądowych wg UKSC (skala po reformie 2019), zwolnienia.
- **`pl:citing-polish-law`** — format cytowania aktów prawnych, orzeczeń SN/TK/TSUE/ETPCz, skróty kodeksów.
- **`pl:determining-pl-jurisdiction`** — właściwość sądu (rzeczowa, miejscowa, funkcjonalna); cywilna vs gospodarcza vs administracyjna.
- **`pl:checking-przedawnienie`** — terminy przedawnienia (art. 117–125 KC), reforma 2018, ex officio wobec konsumenta.

### Installation

```
/plugin marketplace add crankshift/lawpowers
/plugin install pl@lawpowers
/reload-plugins
```

Dostępny w tagu marketplace'u [v0.4.0](https://github.com/crankshift/lawpowers/releases/tag/v0.4.0).

[0.3.1]: https://github.com/crankshift/lawpowers/releases/tag/pl/v0.3.1
[0.3.0]: https://github.com/crankshift/lawpowers/releases/tag/pl/v0.3.0
[0.2.0]: https://github.com/crankshift/lawpowers/releases/tag/pl/v0.2.0
[0.1.0]: https://github.com/crankshift/lawpowers/releases/tag/v0.4.0

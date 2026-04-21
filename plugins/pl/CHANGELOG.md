# Plagin `pl` — Changelog

Historia zmian plagina `pl` (polskie prawo) w ramach monorepo [`lawpowers`](../../CHANGELOG.md).

Format — [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Od wydań po v0.6.0 plagin jest tagowany osobno jako `pl/vX.Y.Z` (gdzie `X.Y.Z` odpowiada polu `version` w `plugin.json`). Wpisy historyczne poniżej (do 0.2.0 włącznie) były wydawane w ramach wspólnych tagów marketplace'u `vX.Y.Z` i zachowują linki do nich.

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

[0.2.0]: https://github.com/crankshift/lawpowers/releases/tag/v0.6.0

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

[0.1.0]: https://github.com/crankshift/lawpowers/releases/tag/v0.4.0

# Plagin `pl` — Changelog

Historia zmian plagina `pl` (polskie prawo) w ramach monorepo [`lawpowers`](../../CHANGELOG.md).

Format — [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Wersje plagina są wyrównane z tagami marketplace'u `vX.Y.Z`.

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

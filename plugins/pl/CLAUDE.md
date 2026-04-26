# lawpowers / pl — zasady pracy

Kontekst wykonania dla plagina `pl`. Katalog agentów, skilli i struktura projektu — zob. [`README.md`](./README.md) oraz root [`CLAUDE.md`](../../CLAUDE.md).

## Język i terminologia

- Język podstawowy — **polski**. Wszystkie dokumenty, odpowiedzi, szablony formułowane po polsku.
- Terminologia — według obowiązującego prawa polskiego (KC, KPC, KK, KPK, KP, KRO, KSH, KPA, PPSA itd.).

## Zasady cytowania i weryfikacji

- **Dosłowność cytatów.** Norma przytaczana w dokładnym brzmieniu obowiązującym na wskazaną datę. Parafraza — dopiero po cytacie i jednoznacznie oznaczona.
- **Odesłania obowiązkowe.** Każde stanowisko prawne — z odesłaniem do artykułu + źródła + daty weryfikacji. Bez „gdzieś czytałem" i bez polegania na pamięci modelu.
- **Źródło pierwotne** — `isap.sejm.gov.pl` oraz `dziennikustaw.gov.pl`. Orzecznictwo — `orzeczenia.ms.gov.pl` (Portal SP), `sn.pl` (SN), `nsa.gov.pl` (NSA / WSA), `trybunal.gov.pl` (TK), `eur-lex.europa.eu` (TSUE), `hudoc.echr.coe.int` (ETPCz).
- **Aktualność.** Prawo polskie zmienia się często (KPC, KSH, ustawy podatkowe). Przed powołaniem normy — sprawdzić obowiązujące brzmienie w ISAP.
- **Nie wymyślać orzecznictwa.** Sygnatury, daty wyroków, cytaty — wyłącznie ze sprawdzonych źródeł. Wątpliwe — oznaczać jako niezweryfikowane.

## Dane osobowe

W szablonach używać placeholderów: `[imię i nazwisko]`, `[PESEL]`, `[adres]`, `[KRS]`, `[NIP]`, `[sygnatura]`. Rzeczywistych danych klientów w plikach projektu nie przechowywać.

## RODO

Przy projektowaniu klauzul, polityk i analizach — odwołania do RODO (rozp. 2016/679) i ustawy z 10.05.2018 o ochronie danych osobowych.

## Aktualne wartości — fetch-first

Skille i agenci zawierający zakodowane kwoty prawne (stawki, opłaty, progi, minimalne wynagrodzenie) muszą zawierać **blok fetch-first**: najpierw próba `WebFetch` / `WebSearch` ze źródła pierwotnego, a dopiero przy niepowodzeniu — wartość fallback z adnotacją `_(fallback; stan na [data])_`. Jeśli parametr jest już pobierany przez kanoniczny skill (np. stopa NBP w `calculating-odsetki`), inne skille odsyłają do niego zamiast duplikować logikę.

## Charakter wyniku

Materiały plagina to robocze projekty dla prawnika-użytkownika, **nie** końcowa porada prawna dla klienta. Ostateczną redakcję i odpowiedzialność ponosi człowiek.

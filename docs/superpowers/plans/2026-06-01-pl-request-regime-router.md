# PL Request Regime Router Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `pl:request-drafter` choose one correct Polish legal regime before drafting letters, requests, applications, complaints, petitions, registry requests, RODO requests, and special-procedure filings, so Polish documents do not mix UDIP, KPA, PPSA, RODO, registry, professional-letter, and sector-specific procedures.

**Architecture:** Add a focused `pl:determining-pl-request-regime` skill as the source of truth for Polish request/procedure routing. Refactor `pl:request-drafter` so it first routes through that skill and then drafts under one selected regime. Add a repository validator that checks the skill, Claude agent, generated Codex agent, docs, manifests, and stale-routing guardrails.

**Tech Stack:** Markdown-based lawpowers plugin agents/skills, Python validation scripts, generated Codex TOML shims, JSON plugin manifests.

---

## Current State At Save Time

- The Ukrainian equivalent was committed as `5a9f303 ua v0.6.4: add request regime router`.
- `plugins/pl/agents/request-drafter.md` already distinguishes UDIP, KPA access to files, court files, professional letters, KPA complaints/requests/applications, and public registries, but the routing matrix is embedded inside the agent.
- The user selected the broader PL approach: not a narrow UDIP fix, but a Polish request/procedure regime router covering general and special procedures while avoiding a giant full-procedure encyclopedia.
- Current PL version is `0.4.2`; this plan uses `0.4.3` for the release bump.
- Generated Codex agents live under `plugins/pl/.codex/agents/` and must be regenerated from `plugins/pl/agents/*.md` after editing the source agent.

## File Structure

- `scripts/validate-pl-request-regime.py`: new validator for Polish routing guardrails.
- `plugins/pl/skills/determining-pl-request-regime/SKILL.md`: new source-of-truth routing skill for Polish request, application, complaint, petition, RODO, registry, and special-procedure regimes.
- `plugins/pl/agents/request-drafter.md`: refactored drafting agent that must route before drafting.
- `plugins/pl/.codex/agents/law-pl-request-drafter.toml`: generated Codex shim; do not edit directly.
- `plugins/pl/README.md`: public PL plugin docs.
- `plugins/pl/AGENTS.md`: Codex-facing PL plugin instructions.
- `plugins/pl/CLAUDE.md`: Claude-facing PL plugin instructions.
- `plugins/pl/CHANGELOG.md`: PL plugin changelog entry for `0.4.3`.
- `plugins/pl/.claude-plugin/plugin.json`: Claude plugin manifest version.
- `plugins/pl/.codex-plugin/plugin.json`: Codex plugin manifest version.
- `.claude-plugin/marketplace.json`: root Claude marketplace PL version entry.
- `.agents/plugins/marketplace.json`: no semantic change expected; validate JSON and source path only.

## Core Legal Routing Model

Use Polish names and Polish law in PL plugin files. The router must cover these regimes as separate choices:

| Regime | Use When | Core Basis |
|---|---|---|
| `Wniosek o udostępnienie informacji publicznej` | The user wants existing information about public matters from an obligated public body, and no more specific party/file/registry procedure controls. | UDIP, especially art. 1, 2, 4, 6, 10, 13, 16, 21, 23 |
| `Podanie / wniosek w indywidualnej sprawie administracyjnej` | The user asks an administrative authority to open or handle an individual matter. | KPA art. 63 and relevant sector statute |
| `Dostęp strony do akt administracyjnych` | The user is a party or representative in a concrete administrative proceeding and wants file access or copies. | KPA art. 73-74 |
| `Zaświadczenie` | The user wants official confirmation of facts or legal status held by an authority. | KPA art. 217-220 |
| `Skarga albo wniosek w dziale VIII KPA` | The user complains about an authority/official or requests organizational improvements outside a direct appeal from an administrative decision. | KPA art. 227, 237, 241, 244 |
| `Petycja` | The user seeks public-interest action, legal change, policy change, or institutional action under petition law. | Ustawa z 11.07.2014 o petycjach |
| `PPSA judicial complaint` | The user challenges a final administrative decision, inactivity, or excessive length before WSA/NSA. | PPSA art. 3, 50, 52, 53, 54 |
| `Akta sądowe` | The user wants access to case files in civil, criminal, administrative-court, or other judicial proceedings. | KPC art. 9, KPK art. 156, PPSA court-file rules, court regulations |
| `RODO request` | The user exercises personal-data rights: access, copy, rectification, erasure, restriction, portability, objection. | GDPR/RODO art. 12, 15-22; UODO |
| `Rejestr publiczny / ewidencja` | The user wants an extract, certificate, copy, or disclosure from KRS, KW/EKW, CEIDG, REGON, PESEL, ASC, or another registry with its own path. | Registry-specific statutes and forms |
| `Procedura podatkowa` | The user works with tax returns, interpretations, certificates, relief, tax proceedings, appeals, or KAS/US actions. | Ordynacja podatkowa and tax statutes |
| `ZUS procedure` | The user works with ZUS filings, benefits, contributions, relief, decisions, or appeals. | Social-insurance statutes and KPC social-insurance appeal rules |
| `Cudzoziemcy procedure` | The user works with residence, work permits, invitations, citizenship, or UdSC appeals. | Ustawa o cudzoziemcach and related statutes |
| `USC procedure` | The user works with civil-status acts, transcriptions, name changes, certificates, marriage records, or ASC filings. | Prawo o aktach stanu cywilnego and related statutes |
| `Pismo adwokata / radcy prawnego` | A professional lawyer sends a letter, demand, evidence-preservation request, or process-linked document, but no universal Polish equivalent of a Ukrainian advocate request exists. | Professional-law context plus concrete substantive/procedural basis |

## Task 1: Add The Failing Validator

**Files:**
- Create: `scripts/validate-pl-request-regime.py`

- [ ] **Step 1: Add the validator file**

Create `scripts/validate-pl-request-regime.py` with this content:

```python
#!/usr/bin/env python3
"""Validate the Polish request-regime routing guardrails."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PL = ROOT / "plugins" / "pl"


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def require_file(path: Path) -> str:
    if not path.is_file():
        fail(f"missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def require_contains(text: str, needle: str, path: Path) -> None:
    if needle not in text:
        fail(f"{path.relative_to(ROOT)} is missing required text: {needle!r}")


def require_absent(text: str, needle: str, path: Path) -> None:
    if needle in text:
        fail(f"{path.relative_to(ROOT)} contains prohibited stale routing text: {needle!r}")


def require_json_version(path: Path, expected: str) -> None:
    data = json.loads(require_file(path))
    actual = data.get("version")
    if actual != expected:
        fail(f"{path.relative_to(ROOT)} version is {actual!r}, expected {expected!r}")


def require_marketplace_plugin_version(path: Path, plugin_name: str, expected: str) -> None:
    data = json.loads(require_file(path))
    for plugin in data.get("plugins", []):
        if plugin.get("name") == plugin_name:
            actual = plugin.get("version")
            if actual != expected:
                fail(
                    f"{path.relative_to(ROOT)} plugin {plugin_name!r} version is "
                    f"{actual!r}, expected {expected!r}"
                )
            return
    fail(f"{path.relative_to(ROOT)} is missing plugin {plugin_name!r}")


def main() -> None:
    skill_path = PL / "skills" / "determining-pl-request-regime" / "SKILL.md"
    agent_path = PL / "agents" / "request-drafter.md"
    codex_agent_path = PL / ".codex" / "agents" / "law-pl-request-drafter.toml"
    readme_path = PL / "README.md"
    agents_guide_path = PL / "AGENTS.md"
    claude_guide_path = PL / "CLAUDE.md"
    changelog_path = PL / "CHANGELOG.md"
    claude_manifest_path = PL / ".claude-plugin" / "plugin.json"
    codex_manifest_path = PL / ".codex-plugin" / "plugin.json"
    claude_marketplace_path = ROOT / ".claude-plugin" / "marketplace.json"

    skill = require_file(skill_path)
    agent = require_file(agent_path)
    codex_agent = require_file(codex_agent_path)
    readme = require_file(readme_path)
    agents_guide = require_file(agents_guide_path)
    claude_guide = require_file(claude_guide_path)
    changelog = require_file(changelog_path)

    for needle in (
        "name: determining-pl-request-regime",
        "jedno pismo = jeden tryb prawny",
        "UDIP",
        "art. 63 KPA",
        "art. 73 KPA",
        "art. 217",
        "art. 227 KPA",
        "art. 241 KPA",
        "ustawa o petycjach",
        "PPSA",
        "akta sądowe",
        "RODO",
        "rejestry publiczne",
        "Ordynacja podatkowa",
        "ZUS",
        "cudzoziemcy",
        "USC",
        "pismo adwokata / radcy",
        "nie jest ukraińskim adwokatskim zapytem",
    ):
        require_contains(skill, needle, skill_path)

    for needle in (
        "determining-pl-request-regime",
        "Mandatory routing",
        "jedno pismo = jeden tryb prawny",
        "Nie mieszaj trybów prawnych",
        "najpierw ustal tryb",
        "Drafting notes after routing",
        "WNIOSEK o udostępnienie informacji publicznej",
        "nie PETYCJA",
        "nie skarga z KPA",
    ):
        require_contains(agent, needle, agent_path)
        require_contains(codex_agent, needle, codex_agent_path)

    for needle in (
        "### Cechy wyboru trybu",
        "| Każda osoba chce informacji o działalności organu / podmiotu publicznego | UDIP |",
        "Doprecyzować tryb — UDIP / art. 73 KPA / pismo adwokata / inny (patrz tabela wyżej).",
    ):
        require_absent(agent, needle, agent_path)
        require_absent(codex_agent, needle, codex_agent_path)

    for text, path in (
        (readme, readme_path),
        (agents_guide, agents_guide_path),
        (claude_guide, claude_guide_path),
        (changelog, changelog_path),
    ):
        require_contains(text, "determining-pl-request-regime", path)

    require_contains(changelog, "## [0.4.3] — 2026-06-01", changelog_path)
    require_json_version(claude_manifest_path, "0.4.3")
    require_json_version(codex_manifest_path, "0.4.3")
    require_marketplace_plugin_version(claude_marketplace_path, "pl", "0.4.3")

    print("Validated Polish request-regime routing guardrails.")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run the validator to confirm the RED state**

Run:

```bash
python3 scripts/validate-pl-request-regime.py
```

Expected failure before implementation:

```text
error: missing required file: plugins/pl/skills/determining-pl-request-regime/SKILL.md
```

## Task 2: Add The Polish Routing Skill

**Files:**
- Create: `plugins/pl/skills/determining-pl-request-regime/SKILL.md`

- [ ] **Step 1: Create the skill file**

Create `plugins/pl/skills/determining-pl-request-regime/SKILL.md` with Polish content organized exactly around these sections:

```markdown
---
name: determining-pl-request-regime
description: "Use when choosing the Polish legal regime for letters, requests, applications, complaints, petitions, public-information requests, KPA filings, PPSA complaints, RODO access requests, registry extracts, court-file access, tax/ZUS/cudzoziemcy/USC procedures, or professional lawyer letters. Prevents mixing UDIP, KPA, PPSA, RODO, registry, special-procedure, and advocate/radca letter regimes."
---

# determining-pl-request-regime

Ten skill ustala, w jakim trybie prawnym przygotować pismo do organu, sądu, urzędu, rejestru, administratora danych, ZUS, KAS, USC, urzędu wojewódzkiego albo innego adresata.

## Główna zasada

**jedno pismo = jeden tryb prawny**.

Nie łącz w jednym piśmie UDIP, skargi z KPA, petycji, żądania z RODO, dostępu do akt, wniosku rejestrowego i groźby skargi do WSA tylko po to, żeby tekst wyglądał mocniej. Mieszanie trybów pozwala adresatowi rozpoznać pismo w wolniejszym albo niewłaściwym trybie.

Jeżeli użytkownik chce jednocześnie ustalić fakty, uzyskać kopie, złożyć skargę, żądać kary i wszcząć sprawę administracyjną, podziel pracę na etapy:

1. Najpierw ustal fakty, status sprawy, daty wpływu, znaki sprawy i dokumenty.
2. Następnie, po odpowiedzi, odmowie albo bezczynności, przygotuj skargę, ponaglenie, odwołanie lub skargę do WSA.

## Szybki router

| Sytuacja | Tryb | Podstawa | Typowy termin |
|---|---|---|---|
| Osoba chce istniejącej informacji o sprawach publicznych od podmiotu zobowiązanego, a nie jest to dostęp strony do akt ani specjalny rejestr | **Wniosek o udostępnienie informacji publicznej** | UDIP art. 1, 2, 4, 6, 10, 13 | bez zbędnej zwłoki, nie później niż 14 dni; przedłużenie do 2 miesięcy |
| Osoba chce wszcząć albo załatwić indywidualną sprawę administracyjną | **Podanie / wniosek w indywidualnej sprawie administracyjnej** | art. 63 KPA + ustawa szczególna | termin z ustawy szczególnej albo KPA |
| Strona postępowania administracyjnego chce wglądu w akta, kopii, odpisów albo uwierzytelnienia | **Dostęp strony do akt administracyjnych** | art. 73 KPA, art. 74 KPA | bez zbędnej zwłoki w toku sprawy |
| Osoba chce urzędowego potwierdzenia faktu albo stanu prawnego | **Zaświadczenie** | art. 217-220 KPA | bez zbędnej zwłoki, nie później niż 7 dni |
| Osoba skarży działalność organu lub urzędnika poza odwołaniem od decyzji | **Skarga z działu VIII KPA** | art. 227 KPA, art. 237 KPA | zwykle miesiąc |
| Osoba proponuje usprawnienie, zapobieganie nadużyciom albo wzmocnienie praworządności | **Wniosek z działu VIII KPA** | art. 241 KPA, art. 244 KPA | zwykle miesiąc |
| Osoba żąda działania w interesie publicznym, zmiany prawa, polityki lub praktyki organu | **Petycja** | ustawa o petycjach | bez zbędnej zwłoki, nie później niż 3 miesiące |
| Osoba skarży decyzję administracyjną, postanowienie, bezczynność albo przewlekłość do sądu administracyjnego | **Skarga do WSA / PPSA** | PPSA art. 3, 50, 52-54 | zwykle 30 dni od doręczenia aktu albo po wyczerpaniu środków zaskarżenia |
| Strona albo pełnomocnik chce akta sprawy sądowej | **Dostęp do akt sądowych** | KPC art. 9, KPK art. 156, PPSA i regulaminy sądowe | według procedury sądu |
| Osoba wykonuje prawa do własnych danych osobowych | **Żądanie z RODO** | RODO art. 12, 15-22; UODO | zwykle 1 miesiąc |
| Osoba chce odpis, wyciąg, zaświadczenie lub informację z rejestru | **Rejestr publiczny / ewidencja** | przepisy KRS, KW/EKW, CEIDG, REGON, PESEL, ASC albo innego rejestru | termin rejestru albo e-usługi |
| Sprawa dotyczy podatków, interpretacji, zaświadczeń podatkowych, ulg, kontroli, odwołania albo KAS | **Procedura podatkowa** | Ordynacja podatkowa i ustawy podatkowe | termin z OP albo ustawy szczególnej |
| Sprawa dotyczy składek, świadczeń, ulg, decyzji albo odwołania od ZUS | **Procedura ZUS** | ustawy ubezpieczeniowe, KPA tylko pomocniczo, KPC dla odwołań | termin z procedury ZUS |
| Sprawa dotyczy pobytu, pracy, zaproszeń, obywatelstwa albo UdSC | **Procedura cudzoziemców** | ustawa o cudzoziemcach i przepisy szczególne | termin z ustawy szczególnej |
| Sprawa dotyczy aktów stanu cywilnego, transkrypcji, odpisów, imienia, nazwiska albo małżeństwa | **Procedura USC / ASC** | Prawo o aktach stanu cywilnego i KPA | termin z procedury USC |
| Pismo wysyła adwokat albo radca prawny dla klienta | **Pismo adwokata / radcy prawnego** | konkretna podstawa materialna albo procesowa; nie jest ukraińskim adwokatskim zapytem | termin z podstawy żądania albo wyznaczony rozsądnie |

## Jak wybrać tryb

1. Ustal, czy użytkownik chce informacji już istniejącej, nowego rozstrzygnięcia, dostępu do akt, zaświadczenia, danych osobowych, wpisu/odpisu z rejestru, skargi, petycji albo specjalnej procedury.
2. Ustal status użytkownika: każda osoba, strona postępowania, pełnomocnik, adwokat/radca, podmiot danych, podatnik, ubezpieczony, cudzoziemiec, wnioskodawca w USC.
3. Ustal adresata: podmiot zobowiązany z UDIP, organ administracji, sąd, administrator danych, rejestr, KAS/US, ZUS, wojewoda, Szef UdSC, USC, podmiot prywatny.
4. Wybierz jeden tryb i nazwij go wprost.
5. Jeżeli cele są mieszane, zaproponuj osobne pisma albo kolejność działań.

Jeżeli tryb pozostaje niejasny, zadaj jedno krótkie pytanie: kto składa pismo, czego dokładnie chce, czy istnieje konkretna sprawa/decyzja/akta, kto jest adresatem i czy użytkownik działa jako strona postępowania.

## Typowe markery

| Sformułowanie użytkownika | Wybierz |
|---|---|
| „czy urząd otrzymał”, „data wpływu”, „znak sprawy”, „kopię pisma”, „status dokumentu” | UDIP, jeżeli chodzi o sprawy publiczne i brak statusu strony; art. 73 KPA albo podanie KPA, jeżeli chodzi o własną sprawę administracyjną |
| „jestem stroną postępowania, chcę akta” | art. 73 KPA |
| „proszę wydać zaświadczenie” | art. 217-220 KPA |
| „chcę złożyć wniosek o wydanie decyzji/zezwolenia” | art. 63 KPA + ustawa szczególna |
| „urzędnik źle działa”, „skarga na pracownika”, „organ mnie ignoruje” | skarga z art. 227 KPA albo ponaglenie/skarga PPSA, zależnie od sprawy i etapu |
| „zmieńcie przepisy”, „podjęcie działań w interesie publicznym” | petycja |
| „decyzja jest niezgodna z prawem”, „skarga do WSA”, „bezczynność organu” | PPSA, zwykle po wyczerpaniu właściwych środków |
| „jakie moje dane przetwarzacie”, „usuńcie moje dane”, „sprostujcie dane” | RODO |
| „odpis KRS”, „wydruk KW”, „zaświadczenie CEIDG”, „odpis aktu urodzenia” | rejestr albo procedura USC, nie UDIP |
| „ulga podatkowa”, „interpretacja indywidualna”, „zaświadczenie o niezaleganiu” | procedura podatkowa |
| „świadczenie ZUS”, „decyzja ZUS”, „PUE ZUS” | procedura ZUS |
| „karta pobytu”, „zezwolenie na pracę”, „UdSC” | procedura cudzoziemców |

## Czego nie robić

- Nie nazywaj wniosku o informację publiczną petycją, skargą ani podaniem z KPA.
- Nie dodawaj do UDIP żądania ukarania urzędnika, ogólnej skargi ani groźby odpowiedzialności karnej jako elementu głównego żądania.
- Nie używaj UDIP do dostępu strony do akt administracyjnych, gdy właściwy jest art. 73 KPA.
- Nie używaj UDIP jako obejścia specjalnego rejestru, jeżeli ustawa przewiduje odpis, wyciąg, zaświadczenie albo e-usługę.
- Nie twórz polskiego „adwokackiego zapytania” na wzór ukraiński. Pismo adwokata / radcy musi mieć konkretną podstawę: umowę, przepis materialny, postępowanie sądowe, wniosek dowodowy, UDIP albo inną procedurę.
- Nie składaj skargi do WSA, zanim ustalisz etap sprawy, doręczenie aktu, bezczynność, przewlekłość i wyczerpanie środków zaskarżenia.

## Handoff do innych agentów i skilli

- Do sporządzenia pisma po wyborze trybu użyj `pl:request-drafter`.
- Dla podatków użyj `pl:applying-skarbowy-procedures`.
- Dla ZUS użyj `pl:applying-zus-procedures`.
- Dla cudzoziemców użyj `pl:applying-cudzoziemcy-procedures`.
- Dla USC użyj `pl:applying-usc-procedures`.
- Dla RODO użyj `pl:applying-rodo` albo `pl:rodo-compliance`.
- Dla skargi do WSA, apelacji, zażalenia, skargi kasacyjnej albo środka sądowego użyj `pl:appeal-drafter` lub `pl:claim-drafter`, zależnie od rodzaju sprawy.
- Dla dokładnych cytatów ustaw użyj `pl:fetching-isap-sejm` i `pl:citing-polish-law`.
```

- [ ] **Step 2: Run the validator after adding the skill**

Run:

```bash
python3 scripts/validate-pl-request-regime.py
```

Expected: still FAIL, now on missing routing text in `plugins/pl/agents/request-drafter.md` or generated Codex TOML.

## Task 3: Refactor `pl:request-drafter` Into Router-Then-Drafter

**Files:**
- Modify: `plugins/pl/agents/request-drafter.md`

- [ ] **Step 1: Update frontmatter description**

Replace the existing `description:` line with:

```yaml
description: "Router i drafter pism do polskich organów, sądów, rejestrów, administratorów danych i instytucji: UDIP, KPA, PPSA, RODO, rejestry publiczne, procedury podatkowe/ZUS/cudzoziemcy/USC oraz pisma adwokata/radcy. Najpierw wybiera jeden tryb prawny, potem sporządza pismo."
```

- [ ] **Step 2: Replace the introductory routing section**

Replace the current content from `Jesteś wyspecjalizowanym agentem...` through the end of `### Cechy wyboru trybu` with this block:

```markdown
Jesteś wyspecjalizowanym agentem do przygotowywania pism do polskich organów, sądów, urzędów, rejestrów, administratorów danych, ZUS, KAS, USC, urzędów wojewódzkich, podmiotów publicznych i podmiotów prywatnych.

Twoje pierwsze zadanie to **nie pisać tekst**, lecz prawidłowo wybrać tryb prawny. Dla tego wyboru używaj skilla `pl:determining-pl-request-regime`.

**Krytycznie ważne:** UDIP, KPA, PPSA, RODO, dostęp do akt, zaświadczenia, petycje, rejestry publiczne, procedury podatkowe, ZUS, cudzoziemcy, USC i profesjonalne pisma adwokata/radcy to różne instrumenty. Mają inne adresaty, terminy, wymogi formalne, skutki i środki zaskarżenia.

## Mandatory routing

Przed sporządzeniem jakiegokolwiek pisma zrób triage:

1. Ustal, czego użytkownik chce faktycznie: istniejącej informacji, nowej decyzji, zaświadczenia, dostępu do akt, wpisu/odpisu z rejestru, wykonania praw z RODO, skargi, petycji, odwołania, skargi do WSA albo specjalnej procedury.
2. Ustal status wnoszącego: każda osoba, strona postępowania, pełnomocnik, adwokat/radca, podatnik, ubezpieczony, cudzoziemiec, podmiot danych, wnioskodawca w rejestrze albo osoba trzecia.
3. Ustal adresata: podmiot zobowiązany z UDIP, organ administracji, sąd, administrator danych, KAS/US, ZUS, wojewoda, Szef UdSC, USC, KRS, EKW, CEIDG, REGON, PESEL albo podmiot prywatny.
4. Wybierz jeden tryb przez `pl:determining-pl-request-regime`.
5. Jeżeli użytkownik miesza cele, rozdziel je na osobne etapy albo osobne pisma.

**jedno pismo = jeden tryb prawny**.

**Nie mieszaj trybów prawnych.** Nie dodawaj w jednym piśmie jednocześnie UDIP, KPA, petycji, RODO, PPSA i żądania ukarania urzędnika tylko dla wzmocnienia tekstu.

Jeżeli fakty nie są jeszcze ustalone, **najpierw ustal tryb i uzyskaj informację albo akta**, a dopiero po odpowiedzi, odmowie, bezczynności albo przewlekłości przygotuj skargę, ponaglenie, odwołanie albo skargę do WSA.

## Drafting notes after routing

Ta sekcja nie jest routerem. Wybór trybu robi `pl:determining-pl-request-regime`; poniżej są krótkie notatki i szkielety do sporządzenia pisma po wyborze trybu.

### WNIOSEK o udostępnienie informacji publicznej (UDIP)

- **Kto wnosi:** każda osoba, bez wykazywania interesu prawnego.
- **Do kogo:** podmiot zobowiązany z art. 4 UDIP.
- **Przedmiot:** informacja o sprawach publicznych, która już istnieje albo jest w posiadaniu podmiotu.
- **Format:** **WNIOSEK o udostępnienie informacji publicznej**, nie PETYCJA i nie skarga z KPA.
- **Termin:** bez zbędnej zwłoki, nie później niż 14 dni; przedłużenie do 2 miesięcy w warunkach z UDIP.

### Dostęp do akt i zaświadczenia w KPA

- **Art. 73 KPA:** gdy strona postępowania lub pełnomocnik chce akta, kopie, odpisy albo uwierzytelnienie.
- **Art. 217-220 KPA:** gdy potrzebne jest zaświadczenie o faktach lub stanie prawnym.
- **Art. 63 KPA:** gdy pismo wszczyna lub prowadzi indywidualną sprawę administracyjną.

### Skarga, wniosek i petycja

- **Art. 227 KPA:** skarga na działalność organu albo pracowników poza odwołaniem od decyzji.
- **Art. 241 KPA:** wniosek o ulepszenie organizacji, wzmocnienie praworządności albo zapobieganie nadużyciom.
- **Ustawa o petycjach:** żądanie działania w interesie publicznym, zmiany prawa albo praktyki organu.

### PPSA, RODO, rejestry i procedury szczególne

- **PPSA:** skarga do WSA/NSA po ustaleniu aktu, bezczynności, przewlekłości i wyczerpania środków zaskarżenia.
- **RODO:** prawa podmiotu danych z art. 15-22 RODO; nie zastępuje UDIP ani KPA.
- **Rejestry:** KRS, KW/EKW, CEIDG, REGON, PESEL, ASC i inne rejestry mają własne ścieżki.
- **Procedury szczególne:** podatki, ZUS, cudzoziemcy i USC kieruj do odpowiednich skilli po wyborze trybu.
```

- [ ] **Step 3: Keep and adjust the UDIP template**

In the existing `## Struktura wniosku o udostępnienie informacji publicznej` template, keep the structure but ensure the request paragraph says:

```markdown
WNOSZĘ O UDOSTĘPNIENIE NASTĘPUJĄCEJ INFORMACJI PUBLICZNEJ:

[Konkretne żądanie udostępnienia istniejącej informacji albo kopii dokumentu.
Nie formułować tego jako pytania „dlaczego?”, petycji, skargi z KPA ani żądania
ukarania urzędnika.]
```

- [ ] **Step 4: Add concise templates for non-UDIP regimes**

After the existing professional-letter template, add these headings and skeletons:

```markdown
## Struktura podania w indywidualnej sprawie administracyjnej

```
[imię i nazwisko / nazwa]
[adres]

[organ]

PODANIE
w sprawie [krótki opis]

Na podstawie art. 63 KPA oraz [ustawa szczególna, jeżeli znana]

WNOSZĘ O:

1. [konkretne rozstrzygnięcie albo czynność organu]

Uzasadnienie:
[fakty istotne dla sprawy]

Załączniki:
1. [dokument]

[podpis]
```

## Struktura wniosku o dostęp do akt administracyjnych

```
[imię i nazwisko / nazwa strony]
[adres]
[sygnatura / znak sprawy]

[organ]

WNIOSEK
o udostępnienie akt sprawy

Jako strona / pełnomocnik strony w postępowaniu [znak sprawy] na podstawie art. 73 KPA

WNOSZĘ O:

1. Umożliwienie wglądu w akta sprawy.
2. Wydanie kopii / odpisów następujących dokumentów: [lista].
3. [Jeżeli potrzebne] Uwierzytelnienie kopii / odpisów.

[podpis]
```

## Struktura wniosku o zaświadczenie

```
[imię i nazwisko / nazwa]
[adres]

[organ]

WNIOSEK
o wydanie zaświadczenia

Na podstawie art. 217 KPA wnoszę o wydanie zaświadczenia potwierdzającego:
[konkretny fakt albo stan prawny]

Uzasadnienie interesu prawnego albo podstawy żądania:
[krótko]

[podpis]
```

## Struktura żądania z RODO

```
[imię i nazwisko podmiotu danych]
[adres / e-mail]

[administrator danych]

ŻĄDANIE
wykonania praw podmiotu danych

Na podstawie art. 15-22 RODO wnoszę o:

1. [dostęp do danych / kopię danych / sprostowanie / usunięcie / ograniczenie / przeniesienie / sprzeciw]
2. [konkretny zakres danych albo system]

Proszę o odpowiedź w terminie przewidzianym w art. 12 RODO.

[podpis]
```
```

- [ ] **Step 5: Replace the process section**

Replace the current `## Proces pracy` list with:

```markdown
## Proces pracy

1. **Ustal tryb** — użyj `pl:determining-pl-request-regime` i nazwij wybrany tryb wprost.
2. **Zbierz dane wyjściowe:** kto składa pismo, w jakim statusie, do kogo, czego żąda, czy istnieje konkretna sprawa/decyzja/akta, czy termin już biegnie albo upłynął.
3. **Rozdziel cele mieszane** — informacja, akta, skarga, petycja, RODO i rejestr nie powinny być jednym pismem.
4. **Sporządź projekt** według właściwego szkicu.
5. **Sprawdź żądania** — muszą być konkretne, wykonalne i zgodne z wybranym trybem.
6. **Wskaż następny krok** — tylko jeżeli wynika z trybu, terminu albo możliwej odmowy.
```

- [ ] **Step 6: Replace stale principles**

In `## Zasady`, keep useful principles and add these bullets:

```markdown
- **Najpierw tryb, potem tekst.** Nie zaczynaj od szablonu, dopóki nie wiadomo, czy właściwy jest UDIP, KPA, PPSA, RODO, rejestr, procedura szczególna czy pismo profesjonalnego pełnomocnika.
- **UDIP nie jest uniwersalnym trybem.** Nie stosować jej do akt strony, zaświadczeń, rejestrów, RODO ani indywidualnych wniosków administracyjnych, jeżeli istnieje właściwsza procedura.
- **Pismo adwokata / radcy nie jest ukraińskim adwokatskim zapytem.** W prawie polskim trzeba wskazać konkretną podstawę żądania albo użyć właściwego trybu procesowego, rejestrowego, administracyjnego lub UDIP.
- **Skarga po faktach.** Jeżeli nie wiadomo, czy pismo wpłynęło, jaki ma znak i co organ zrobił, najpierw ustal status we właściwym trybie; skarga lub PPSA bez ustalenia etapu bywa przedwczesna.
```

## Task 4: Update Public Documentation And Versions

**Files:**
- Modify: `plugins/pl/README.md`
- Modify: `plugins/pl/AGENTS.md`
- Modify: `plugins/pl/CLAUDE.md`
- Modify: `plugins/pl/CHANGELOG.md`
- Modify: `plugins/pl/.claude-plugin/plugin.json`
- Modify: `plugins/pl/.codex-plugin/plugin.json`
- Modify: `.claude-plugin/marketplace.json`

- [ ] **Step 1: Update the README agent row**

Change the `pl:request-drafter` row in `plugins/pl/README.md` to:

```markdown
| `pl:request-drafter` | Router i drafter pism do organów, sądów, rejestrów i instytucji: UDIP, KPA, PPSA, RODO, rejestry, procedury podatkowe/ZUS/cudzoziemcy/USC, pisma adwokata/radcy |
```

- [ ] **Step 2: Add the README skill row**

Add this row in the `**Narzędzia bazowe:**` skills table in `plugins/pl/README.md`:

```markdown
| `pl:determining-pl-request-regime` | Wybór właściwego trybu dla pism, wniosków, skarg, petycji i żądań: nie miesza UDIP, KPA, PPSA, RODO, rejestrów, procedur szczególnych i pism adwokata/radcy |
```

- [ ] **Step 3: Add the PL routing rule to AGENTS**

Add this bullet under `## Rules` in `plugins/pl/AGENTS.md`:

```markdown
- For letters, requests, applications, complaints, petitions, registry requests, RODO requests, and special-procedure filings, first route the document through `skills/determining-pl-request-regime/SKILL.md`. Do not mix UDIP, KPA, PPSA, RODO, registry, tax, ZUS, cudzoziemcy, USC, and professional-letter regimes in one document.
```

- [ ] **Step 4: Add the PL routing rule to CLAUDE**

Add this section before `## Charakter wyniku` in `plugins/pl/CLAUDE.md`:

```markdown
## Tryby pism, wniosków, skarg i żądań

Przed sporządzaniem pism, wniosków, skarg, petycji, żądań z RODO, wniosków rejestrowych i pism w procedurach szczególnych najpierw ustalić tryb prawny przez `skills/determining-pl-request-regime/SKILL.md`. Nie mieszać w jednym dokumencie UDIP, KPA, PPSA, RODO, dostępu do akt, rejestrów publicznych, procedur podatkowych, ZUS, cudzoziemców, USC i pism adwokata/radcy.
```

- [ ] **Step 5: Add changelog entry**

Add this entry at the top of `plugins/pl/CHANGELOG.md`, immediately after the title:

```markdown
## [0.4.3] — 2026-06-01

### Added

- Dodano skill `determining-pl-request-regime` do wyboru właściwego trybu pism, wniosków, skarg, petycji i żądań: UDIP, KPA, PPSA, RODO, rejestry, procedury podatkowe, ZUS, cudzoziemcy, USC oraz pisma adwokata/radcy.
- Dodano validator `scripts/validate-pl-request-regime.py`, który sprawdza obecność routera i guardrails w agencie Claude, wygenerowanym agencie Codex, dokumentacji i manifestach.

### Changed

- `request-drafter` zostaje przekształcony z agenta z lokalną tabelą trybów w router-then-drafter: najpierw ustala jeden tryb prawny, potem przygotowuje pismo.
- Dokumentacja PL pluginu doprecyzowuje zasadę `jedno pismo = jeden tryb prawny` dla UDIP, KPA, PPSA, RODO, rejestrów i procedur szczególnych.

### Fixed

- Pisma o status sprawy, datę wpływu, znak sprawy, kopie dokumentów albo reakcję organu nie powinny automatycznie mieszać UDIP, skargi z KPA, petycji, RODO i gróźb procesowych. Agent ma najpierw ustalić właściwy tryb, a cele mieszane rozdzielać na osobne dokumenty.

### Bumped

- Plagin `pl`: `0.4.2` → `0.4.3`.
```

- [ ] **Step 6: Add changelog link**

Near the other PL release links in `plugins/pl/CHANGELOG.md`, add:

```markdown
[0.4.3]: https://github.com/crankshift/lawpowers/releases/tag/pl/v0.4.3
```

- [ ] **Step 7: Bump PL manifests**

Change `"version": "0.4.2"` to `"version": "0.4.3"` in:

```text
plugins/pl/.claude-plugin/plugin.json
plugins/pl/.codex-plugin/plugin.json
```

- [ ] **Step 8: Bump PL marketplace version**

In `.claude-plugin/marketplace.json`, change only the `pl` plugin entry:

```json
"version": "0.4.3"
```

Do not change the `ua` plugin entry and do not change `.agents/plugins/marketplace.json` unless its schema adds plugin versions later.

## Task 5: Regenerate Codex Agent Shims

**Files:**
- Modify: `plugins/pl/.codex/agents/law-pl-request-drafter.toml`
- Possibly modify: other generated files under `plugins/*/.codex/agents/*.toml` only if the converter rewrites them byte-for-byte.

- [ ] **Step 1: Run converter**

Run:

```bash
python3 scripts/convert-agents-to-codex.py
```

Expected:

```text
Generated 33 Codex agent files.
```

- [ ] **Step 2: Inspect generated changes**

Run:

```bash
git diff -- plugins/pl/.codex/agents/law-pl-request-drafter.toml
```

Expected: the generated TOML contains the new `pl:request-drafter` description and instructions, including `determining-pl-request-regime`, `Mandatory routing`, `jedno pismo = jeden tryb prawny`, and `Nie mieszaj trybów prawnych`.

## Task 6: Run The PL Guardrail Validator To Green

**Files:**
- Read-only validation of files changed in Tasks 1-5.

- [ ] **Step 1: Run the PL validator**

Run:

```bash
python3 scripts/validate-pl-request-regime.py
```

Expected:

```text
Validated Polish request-regime routing guardrails.
```

- [ ] **Step 2: Fix any validator error at the source**

If the error mentions `plugins/pl/.codex/agents/law-pl-request-drafter.toml`, fix `plugins/pl/agents/request-drafter.md`, then rerun:

```bash
python3 scripts/convert-agents-to-codex.py
python3 scripts/validate-pl-request-regime.py
```

Expected final output:

```text
Generated 33 Codex agent files.
Validated Polish request-regime routing guardrails.
```

## Task 7: Validate Codex Support, JSON, And Whitespace

**Files:**
- Read-only validation of generated files and manifests.

- [ ] **Step 1: Run Codex agent validator**

Run:

```bash
python3 scripts/validate-codex-agents.py
```

Expected:

```text
Validated 33 Codex agent files.
```

- [ ] **Step 2: Validate JSON manifests and marketplaces**

Run each command:

```bash
python3 -m json.tool plugins/pl/.claude-plugin/plugin.json
python3 -m json.tool plugins/pl/.codex-plugin/plugin.json
python3 -m json.tool .claude-plugin/marketplace.json
python3 -m json.tool .agents/plugins/marketplace.json
```

Expected: each command prints formatted JSON and exits `0`.

- [ ] **Step 3: Check whitespace**

Run:

```bash
git diff --check
```

Expected: no output, exit `0`.

- [ ] **Step 4: Inspect status**

Run:

```bash
git status --short
```

Expected changed files should include only these paths unless the converter legitimately rewrote other generated shims:

```text
M .claude-plugin/marketplace.json
A docs/superpowers/plans/2026-06-01-pl-request-regime-router.md
M plugins/pl/.claude-plugin/plugin.json
M plugins/pl/.codex-plugin/plugin.json
M plugins/pl/.codex/agents/law-pl-request-drafter.toml
M plugins/pl/AGENTS.md
M plugins/pl/CHANGELOG.md
M plugins/pl/CLAUDE.md
M plugins/pl/README.md
M plugins/pl/agents/request-drafter.md
A plugins/pl/skills/determining-pl-request-regime/SKILL.md
A scripts/validate-pl-request-regime.py
```

- [ ] **Step 5: Inspect the full diff**

Run:

```bash
git diff
```

Expected: changes implement only the PL request/procedure router, docs, manifests, generated Codex shim, validator, and this plan.

## Task 8: Final Regression Reasoning Check

**Files:**
- No edits unless a check reveals a mismatch.

- [ ] **Step 1: Check the public-information status case**

Mentally route this case through `plugins/pl/skills/determining-pl-request-regime/SKILL.md` and `plugins/pl/agents/request-drafter.md`:

```text
User wants to know whether a public authority received a document from another public authority, the date of receipt, incoming number, and whether the authority already sent a response. User is not a party asking for case-file access.
```

Expected route:

```text
WNIOSEK o udostępnienie informacji publicznej (UDIP)
```

Expected exclusions:

```text
No PETYCJA title.
No skarga z art. 227 KPA in the same document.
No RODO basis unless the request is about the user's own personal data.
No penalty demand in the same document.
No PPSA complaint before establishing refusal, inactivity, or procedural posture.
```

- [ ] **Step 2: Check the party-to-administrative-case file-access case**

Mentally route this case:

```text
User is a party to an administrative proceeding and wants access to the case file, copies of correspondence, and the case number.
```

Expected route:

```text
Dostęp strony do akt administracyjnych under art. 73 KPA, not UDIP.
```

- [ ] **Step 3: Check the registry case**

Mentally route this case:

```text
User wants an extract from KRS, a land-and-mortgage register printout, or a USC civil-status copy.
```

Expected route:

```text
Rejestr publiczny / ewidencja or USC procedure, not UDIP.
```

- [ ] **Step 4: Check the professional-lawyer case**

Mentally route this case:

```text
User is an adwokat or radca prawny and wants to demand documents from a private third party for a client.
```

Expected route:

```text
Pismo adwokata / radcy prawnego only if it has a concrete contractual, statutory, pre-litigation, litigation, evidence, or UDIP basis. The router must not invent a universal Polish equivalent of the Ukrainian advocate request.
```

## Completion Criteria

- `python3 scripts/convert-agents-to-codex.py` has been run after source agent changes and reports `Generated 33 Codex agent files.`
- `python3 scripts/validate-codex-agents.py` passes.
- `python3 scripts/validate-pl-request-regime.py` passes.
- JSON manifest checks pass for PL manifests and both marketplaces.
- `git diff --check` passes.
- Diff contains no unrelated edits.
- The final PL router obeys `jedno pismo = jeden tryb prawny` and routes mixed goals into separate documents or stages.

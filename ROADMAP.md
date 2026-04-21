# Roadmap

Planned additions to the `lawpowers` plugins. Items here are not yet implemented — this file tracks what we want to build and why each item is shaped the way it is.

Open a [feature request](./.github/ISSUE_TEMPLATE/feature_request.yml) to add something or to volunteer for an item below.

## Design note: skills vs. agents for procedural content

Several items below are deliberately scoped as **skills**, not as agents. Public-administration procedures (Polish urzędy, Ukrainian ЦНАП and сервісні центри МВС, consulates) work off official forms, fixed document checklists, and statutory deadlines. The right output is a verbatim reproduction of those checklists and links to the official forms — not a freshly generated draft. A skill loads the canonical procedure into context; an agent that "writes a custom guide" would drift from the official wording, which is exactly what we want to avoid.

Drafting work that produces a tailored document (pozew, відзив, contract) stays in the agent layer. Procedural lookups stay in the skill layer.

---

## Cross-jurisdictional (`ua` and `pl`)

### Contract review — risk audit

**Type:** agent (or extension to existing `contract-drafter` agents).

Audit a draft contract from the perspective of one party, surfacing pitfalls (підводні камені): unbalanced liability caps, hidden penalties, automatic renewals, jurisdiction/arbitration clauses that disadvantage the client, ambiguous payment terms, missing essentialia negotii, IP assignment overreach, etc. Output is a structured risk report keyed to specific clauses, not a rewritten contract.

- `ua`: extends [`ua:contract-drafter`](./plugins/ua/agents/contract-drafter.md) — already drafts contracts; needs a review-only mode.
- `pl`: extends [`pl:contract-drafter`](./plugins/pl/agents/contract-drafter.md) — same.

### Sale–purchase contract review: vehicles

**Type:** skill (checklist + red flags) feeding into the contract-review agent above.

Vehicle sale contracts have a tight, well-known set of failure modes (encumbrances, fake VIN, undisclosed damage history, missing customs clearance, power-of-attorney sales) and a fixed set of registries that should be checked before signing. A skill captures the checklist, the registry URLs, and the clauses every such contract must contain.

### Sale–purchase contract review: real estate

**Type:** skill feeding into the contract-review agent above.

Same shape as vehicles, but for real-estate transactions: title chain, encumbrances, mortgages, easements, pending litigation, zoning, mandatory notarial form, statutory pre-emption rights, deposit (zadatek/завдаток) vs. advance (zaliczka/аванс) distinction.

---

## `pl` only — Polish administrative procedures

### Skills for "how do I apply for X at urząd Y"

**Type:** skills, one per procedure family.

Polish public services run on official wzory pism (template forms) published by the relevant ministry, ZUS, US, USC, urząd wojewódzki, urząd miasta, KRUS, PUP, etc. Each procedure has:

- a fixed list of required documents,
- one or more official forms (often PDF on `gov.pl` or the agency's site),
- a statutory deadline for the agency to respond (KPA art. 35),
- a fee or exemption,
- a defined appeal path.

A skill should locate the current official form, list the required documents verbatim, and link to the agency page — not generate a custom checklist.

Initial procedure families to cover:

- **USC (Urząd Stanu Cywilnego):** birth registration, marriage, name change, transcription of foreign acts.
- **Urząd wojewódzki / urząd do spraw cudzoziemców:** karta pobytu (czasowa, stała, rezydenta długoterminowego UE), zezwolenie na pracę, obywatelstwo.
- **ZUS:** rejestracja płatnika, zasiłek chorobowy / macierzyński / opiekuńczy, emerytura, renta.
- **Urząd skarbowy:** NIP, VAT-R, PIT/CIT correspondence, czynny żal.
- **Urząd miasta / gminy:** zameldowanie, dowód osobisty, akt notarialny → wpis do KW.
- **KRS / CEIDG:** company registration and changes, JDG.
- **PUP:** rejestracja bezrobotnego, zasiłek dla bezrobotnych.

---

## `ua` only — Ukrainian administrative procedures

### Skills for ЦНАП and сервісні центри МВС

**Type:** skills, one per procedure family. Same rationale as the Polish item above.

ЦНАП (Центри надання адміністративних послуг) and сервісні центри МВС operate from a fixed catalog of services with statutory document lists and forms. Initial procedure families:

- **Сервісні центри МВС:** обмін / видача посвідчення водія, перереєстрація ТЗ, видача свідоцтва про реєстрацію ТЗ, тимчасові талони, дублікати, реєстрація на іноземця.
- **ЦНАП — паспортні послуги:** ID-картка (вперше / обмін / після втрати), закордонний паспорт, відмітки про реєстрацію місця проживання.
- **ЦНАП — соціальні послуги:** субсидії, допомога при народженні дитини, допомога малозабезпеченим сім'ям, статус ВПО, статус УБД (interakcja з ТЦК — see existing [`ua:military-social-benefits`](./plugins/ua/agents/military-social-benefits.md)).
- **ЦНАП — реєстраційні послуги:** реєстрація / зміна місця проживання, реєстрація актів цивільного стану через ДРАЦС, нерухомість (витяг з ДРРП), бізнес (ФОП, зміни до ЄДР).
- **ДПС / податкова:** реєстрація ФОП, групи єдиного податку, РРО / ПРРО.

### Skill for consular procedures

**Type:** skill covering procedures at Ukrainian consulates abroad.

Особлива складність — формальні вимоги відрізняються від внутрішніх процедур: апостиль / легалізація, переклади, нотаріальне завірення підпису, консульський облік, оформлення документів громадянам за кордоном (паспорт, шлюб, народження, смерть, розлучення, посвідчення живим), повернення в Україну (свідоцтво на повернення), питання військового обліку для чоловіків призовного віку за кордоном.

The skill should list the required document package per service, the official MZS / consular fee schedule, and link to the relevant consulate's page (procedures vary by country in practice).

---

## How to propose additions

Open a [feature request](./.github/ISSUE_TEMPLATE/feature_request.yml). Per repo policy, feature ideas need:

- a primary-source citation (zakon.rada.gov.ua for UA, isap.sejm.gov.pl for PL, or the responsible agency's official page for procedural content);
- a concrete legal task the addition would solve;
- a clear scope (which plugin — `ua` or `pl` — and whether it's an agent or a skill).

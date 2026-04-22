# Roadmap

Planned additions to the `lawpowers` plugins. Items here are not yet implemented — this file tracks what we want to build and why each item is shaped the way it is.

Open a [feature request](./.github/ISSUE_TEMPLATE/feature_request.yml) to add something or to volunteer for an item below.

## Recently shipped

A batch of roadmap items landed in `pl/v0.3.0` + `ua/v0.5.0` (2026-04-22):

- Contract review — risk audit mode added to both `pl:contract-drafter` and `ua:contract-drafter` (review-only mode with structured KRYTYCZNE / ISTOTNE / POŻĄDANE classification, per-clause findings, no rewriting). See per-plugin CHANGELOGs.
- Sale–purchase contract review skills for both jurisdictions:
  - `pl:reviewing-vehicle-contract` / `ua:reviewing-vehicle-contract` — VIN / mileage / encumbrance / import-clearance red flags, registry links, post-purchase obligations.
  - `pl:reviewing-real-estate-contract` / `ua:reviewing-real-estate-contract` — title-chain, encumbrances, pre-emption rights, notarial form, zadatek / завдаток distinction, taxes.
- Polish administrative procedure skills — first batch:
  - `pl:applying-usc-procedures` (Urząd Stanu Cywilnego).
  - `pl:applying-zus-procedures` (ZUS).
  - `pl:applying-skarbowy-procedures` (urząd skarbowy / KAS).
  - `pl:applying-cudzoziemcy-procedures` (urząd wojewódzki: pobyt, praca, obywatelstwo).
- Ukrainian administrative procedure skills — first batch:
  - `ua:applying-cnap-passport` (ЦНАП — паспортні послуги).
  - `ua:applying-servisnyi-centr-mvs` (сервісні центри МВС — посвідчення водія, реєстрація ТЗ).
  - `ua:applying-consular-procedures` (консульства України за кордоном).

Remaining roadmap items below.

## Design note: skills vs. agents for procedural content

Several items below are deliberately scoped as **skills**, not as agents. Public-administration procedures (Polish urzędy, Ukrainian ЦНАП and сервісні центри МВС, consulates) work off official forms, fixed document checklists, and statutory deadlines. The right output is a verbatim reproduction of those checklists and links to the official forms — not a freshly generated draft. A skill loads the canonical procedure into context; an agent that "writes a custom guide" would drift from the official wording, which is exactly what we want to avoid.

Drafting work that produces a tailored document (pozew, відзив, contract) stays in the agent layer. Procedural lookups stay in the skill layer.

---

## `pl` only — Polish administrative procedures (remaining)

Same shape as the delivered batch above: skill per procedure family, locates the current official form, lists required documents verbatim, links to the agency page. Procedure families still to cover:

- **Urząd miasta / gminy:** zameldowanie, dowód osobisty, akt notarialny → wpis do KW, podatek od nieruchomości, opłata za użytkowanie wieczyste.
- **KRS / CEIDG:** company registration and changes, JDG (beyond the identity-and-representation perspective already covered by [`pl:searching-krs`](./plugins/pl/skills/searching-krs/SKILL.md)).
- **PUP:** rejestracja bezrobotnego, zasiłek dla bezrobotnych, dofinansowania.

---

## `ua` only — Ukrainian administrative procedures (remaining)

Same shape as the delivered batch above. Procedure families still to cover:

- **ЦНАП — соціальні послуги:** субсидії, допомога при народженні дитини, допомога малозабезпеченим сім'ям, статус ВПО, статус УБД (interakcja з ТЦК — partly covered by [`ua:military-social-benefits`](./plugins/ua/agents/military-social-benefits.md)).
- **ЦНАП — реєстраційні послуги:** реєстрація актів цивільного стану через ДРАЦС (шлюб/народження/розлучення в Україні; закордонні сценарії вже в [`ua:applying-consular-procedures`](./plugins/ua/skills/applying-consular-procedures/SKILL.md)); нерухомість (витяг з ДРРП); бізнес (ФОП, зміни до ЄДР).
- **ДПС / податкова:** реєстрація ФОП, групи єдиного податку, РРО / ПРРО, перехід між групами, військовий збір.

---

## How to propose additions

Open a [feature request](./.github/ISSUE_TEMPLATE/feature_request.yml). Per repo policy, feature ideas need:

- a primary-source citation (zakon.rada.gov.ua for UA, isap.sejm.gov.pl for PL, or the responsible agency's official page for procedural content);
- a concrete legal task the addition would solve;
- a clear scope (which plugin — `ua` or `pl` — and whether it's an agent or a skill).

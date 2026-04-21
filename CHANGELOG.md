# lawpowers — Changelog

Historical umbrella changelog. **Plugin releases are now tracked per plugin**, not here:

- [`plugins/ua/CHANGELOG.md`](./plugins/ua/CHANGELOG.md) — Ukrainian law plugin (written in Ukrainian). Tagged `ua/vX.Y.Z`.
- [`plugins/pl/CHANGELOG.md`](./plugins/pl/CHANGELOG.md) — Polish law plugin (written in Polish). Tagged `pl/vX.Y.Z`.

> **Release format change — 2026-04-21.** Releases up to and including `v0.6.0` used a monorepo-wide umbrella tag (`vX.Y.Z`) covering both plugins together. This caused confusion because users install plugins individually — `/plugin install ua@lawpowers` gives whatever version is declared in `plugin.json`, not the umbrella tag. From this point forward:
>
> - Each plugin is released separately under its own tag: `ua/vX.Y.Z`, `pl/vX.Y.Z`.
> - Marketplace `metadata.version` stays as an internal field (bumped on catalog-shape changes — plugin added/removed). It is not publicly tagged.
> - Historical umbrella tags (`v0.1.0`…`v0.6.0`) remain unchanged on the repo; entries below document that history.
> - This root file no longer receives version-tagged entries. New monorepo-level tooling or structural notes may land here as dated (unversioned) entries.
>
> See [`docs/RELEASING.md`](./docs/RELEASING.md) for the per-plugin release procedure.

Format — [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versioning — [SemVer](https://semver.org/spec/v2.0.0.html).

## [0.6.0] — 2026-04-21

### Added — plugin `pl` v0.2.0 (substantial extension)

Plugin `pl` (Polish law) extended from 10 to 17 agents and from 6 to 14 skills, mirroring the `ua` plugin's scope where universal (arbitration, NYC) and adding Poland-specific practice areas most demanded by Polish lawyers.

**New agents (7):**

- `pl:arbitration-agent` — international and domestic arbitration (SAKIG, Lewiatan, ICC, LCIA, SCC, SIAC, HKIAC, VIAC, UNCITRAL ad hoc, ICSID), drafting Request for Arbitration, clause audits, recognition / setting aside of arbitral awards under art. 1205–1217 KPC + NYC 1958. Accounts for intra-EU BIT/ECT *Achmea* / *Komstroy* / *PL Holdings* line.
- `pl:family-drafter` — divorce, separation, alimony (KRO art. 133 / 60), parental authority, contacts, paternity establishment / denial, division of marital property; security for alimony under art. 754¹ KPC.
- `pl:labor-drafter` — employment disputes: reinstatement, damages for unlawful termination, art. 52 KP disciplinary dismissal, mobbing (art. 94³ KP), discrimination (art. 18³ᵃ KP), recognition of employment relationship (art. 22 § 1¹ KP — hidden employment).
- `pl:inheritance-drafter` — KC Book IV: statement of inheritance, partition, reserved share (zachowek), wills, acceptance / rejection of inheritance within 6 months (art. 1015 KC), unworthiness of inheritance.
- `pl:criminal-complaint-drafter` — victim-side criminal proceedings: report of crime (art. 304 KPK), private indictment (art. 487 KPK), subsidiary indictment (art. 55 KPK), complaints against discontinuation (art. 306 KPK), motion for damages (art. 46 KK).
- `pl:consumer-drafter` — consumer disputes: abusive clauses (art. 385¹ KC), CHF mortgage cases (frankowicze), UOKiK / Financial Ombudsman complaints, 14-day withdrawal from distance contracts.
- `pl:rodo-compliance` — full GDPR/UODO compliance program: privacy policies, processing agreements (art. 28 GDPR), DPIA (art. 35), breach notifications (art. 33/34), rights requests (art. 15–22), PUODO complaints, third-country transfers after *Schrems II*.

**New skills (8):**

- `pl:determining-wps` — value of the subject of dispute under KPC art. 19–26, impact on jurisdiction and court fee.
- `pl:searching-krs` — KRS, CEIDG, VAT white list, debt registries, MSiG — identifying legal entities and verifying representation.
- `pl:calculating-odsetki` — Polish statutory interest (art. 359, 481 KC) vs. B2B commercial transactions (ustawa 08.03.2013) vs. maximum rates; 40/70/100 EUR flat recovery fee.
- `pl:calculating-alimenty` — alimony amount under art. 135 KRO (needs vs. capacity), interim security (art. 754¹ KPC), Fundusz Alimentacyjny, art. 209 KK.
- `pl:fetching-arbitration-rules` — URL table with current versions for SAKIG, Lewiatan, ICC, LCIA, SCC, SIAC, HKIAC, VIAC, UNCITRAL, ICSID.
- `pl:applying-new-york-convention` — NYC 1958 mapped to art. 1215 § 2 KPC; public policy narrow interpretation per SN case law.
- `pl:applying-frankowicze-case-law` — full CHF case law map: TSUE C-260/18 *Dziubak*, C-520/21 *Bank M.*, C-287/22 *Getin*, C-140/22 *mBank*, C-776/19 *BNP Paribas*; SN III CZP 6/21 (two-kondykcja theory), III CZP 11/21.
- `pl:applying-rodo` — quick mapping of GDPR articles to controller obligations, legal basis selection (art. 6/9), information clauses (art. 13/14), processing agreements (art. 28), DPIA (art. 35), breach handling, third-country transfers.

See [`pl/CHANGELOG.md`](./plugins/pl/CHANGELOG.md) for the full catalog.

### Bumped

- Marketplace `metadata.version`: `0.5.0` → `0.6.0`.
- Plugin `pl`: `0.1.0` → `0.2.0`. Plugin `ua` stays at `0.4.0` (unchanged).

### Migration

Non-breaking. Existing agents and skills unchanged; new ones available after update:

```
/plugin marketplace update lawpowers
/reload-plugins
```

## [0.5.0] — 2026-04-20

### Changed — BREAKING (marketplace layout)

- Plugin directories moved from repo root to a dedicated `plugins/` container:
  - `ua/` → `plugins/ua/`
  - `pl/` → `plugins/pl/`
- Marketplace `plugins[N].source` paths updated accordingly (`"./ua"` → `"./plugins/ua"`, `"./pl"` → `"./plugins/pl"`).
- `name` of each plugin is unchanged (`ua`, `pl`), so install commands stay as `/plugin install ua@lawpowers` and `/plugin install pl@lawpowers`. Command prefixes (`/ua:…`, `/pl:…`) are also unchanged.

All cross-references were updated across root docs, scripts, templates, and plugin-nested files:

- Root `README.md`, `CLAUDE.md` — layout diagrams and links.
- `.github/PULL_REQUEST_TEMPLATE.md` — CHANGELOG paths, `--plugin-dir` examples.
- `docs/RELEASING.md` — plugin-manifest paths in CHANGELOG templates.
- `scripts/release.sh` — hard-coded `UA_PLUGIN_JSON` / `PL_PLUGIN_JSON` / `*_CHANGELOG` paths.
- `.version-bump.json` — tracked file paths.
- `plugins/ua/*` and `plugins/pl/*` — relative links updated (`../README.md` → `../../README.md`, etc.); internal structure diagrams refreshed.

### Bumped

- Marketplace `metadata.version`: `0.4.2` → `0.5.0`. Plugin `version` fields untouched (`ua` stays `0.4.0`, `pl` stays `0.1.0`).

### Migration

```
/plugin marketplace update lawpowers
/plugin uninstall ua@lawpowers
/plugin install ua@lawpowers
/plugin uninstall pl@lawpowers   # if installed
/plugin install pl@lawpowers
/reload-plugins
```

Claude Code re-fetches the plugin from the new source path; namespace and commands remain identical.

### Rationale

A `plugins/` container makes room for non-plugin tooling at the repo root (CI workflows, shared config, evaluation harnesses) without scattering plugin content. Future jurisdictions go in `plugins/<code>/` alongside `ua` and `pl`.

## [0.4.2] — 2026-04-20

### Added — tooling

- `scripts/release.sh` — bash helper that automates the mechanical parts of the release flow: `bump`, `prepare` (bump + branch + PR), and `publish` (tag + GitHub Release). Safety checks for clean working tree, existing branch/tag, and `gh` auth. Runs `claude plugin validate` after every bump.
- `docs/RELEASING.md` got a TL;DR pointer to the new script plus cross-links in "Related files".

### Bumped

- Marketplace `metadata.version`: `0.4.1` → `0.4.2`. Plugin versions untouched.

No migration needed.

```
/plugin marketplace update lawpowers
/reload-plugins
```

## [0.4.1] — 2026-04-20

### Changed — documentation

Split the single CHANGELOG into three:

- Root `CHANGELOG.md` (English) — marketplace-level summaries with references.
- `ua/CHANGELOG.md` (Ukrainian) — detailed plugin-`ua` history, backfilled from v0.1.0.
- `pl/CHANGELOG.md` (Polish) — plugin-`pl` history, starting at v0.1.0.

`docs/RELEASING.md` updated with templates per language and an optional `gh release create` invocation that concatenates root + plugin CHANGELOG sections. `CLAUDE.md` and per-plugin `README.md` files link to the appropriate CHANGELOG first.

### Bumped

- Marketplace `metadata.version`: `0.4.0` → `0.4.1`. Plugin versions untouched (`ua` stays at `0.4.0`, `pl` at `0.1.0`) — no agent or skill changed.

No migration needed. Users just run:

```
/plugin marketplace update lawpowers
/reload-plugins
```

## [0.4.0] — 2026-04-20

### Changed — BREAKING (monorepo restructure)

- Plugin `ua` files moved from repo root to the `ua/` subdirectory. Marketplace `source` for `ua` changed from `"./"` to `"./ua"`.
- `marketplace.json` now lists two plugins: `ua` and `pl`.
- Root `CLAUDE.md` and `README.md` rewritten in English.
- `.version-bump.json` restructured for multi-plugin versioning.
- `author`/`owner` fields across all manifests changed `"Yurii"` → `"crankshift"`.

See [`ua/CHANGELOG.md`](./plugins/ua/CHANGELOG.md) for plugin-level details.

### Added — plugin `pl` v0.1.0

First release of the Polish law plugin. 10 agents, 6 skills. See [`pl/CHANGELOG.md`](./plugins/pl/CHANGELOG.md) for the full catalog.

### Added — documentation

- `ua/README.md`, `pl/README.md` — detailed per-plugin user docs in each plugin's working language.
- `ua/CLAUDE.md`, `pl/CLAUDE.md` — contributor context per plugin.
- `docs/RELEASING.md` — full release procedure with commands and pitfalls.

### Migration for `ua` users from 0.3.0

Plugin name and namespace (`ua`, `/ua:…`) are unchanged, but the marketplace `source` change requires reinstall:

```
/plugin marketplace update lawpowers
/plugin uninstall ua@lawpowers
/plugin install ua@lawpowers
/reload-plugins
```

## [0.3.0] — 2026-04-20

### Changed — BREAKING (rename cascade)

Preparation for the monorepo — the repo, marketplace, and plugin were all renamed:

- GitHub repo: `crankshift/legal-ua` → `crankshift/lawpowers`.
- Marketplace name: `legal-ua` → `lawpowers`.
- Plugin identifier: `legal-ua` → `ua`.
- Command prefix: `/legal-ua:…` → `/ua:…`.

Plugin-level changes (including the sonnet→inherit model switch) — see [`ua/CHANGELOG.md`](./plugins/ua/CHANGELOG.md).

### Migration for existing users

```
/plugin uninstall legal-ua@legal-ua
/plugin marketplace remove legal-ua
/plugin marketplace add crankshift/lawpowers
/plugin install ua@lawpowers
/reload-plugins
```

## [0.2.0] — 2026-04-20

### Added — plugin `legal-ua` (predecessor of `ua`)

Military block for service members in ЗСУ — 5 new agents and 4 new skills. Plugin-level details in [`ua/CHANGELOG.md`](./plugins/ua/CHANGELOG.md) under 0.2.0.

## [0.1.0] — 2026-04-20

### Added — initial plugin conversion

Repo converted to an installable Claude Code plugin with `plugin.json` and `marketplace.json`. Plugin-level details in [`ua/CHANGELOG.md`](./plugins/ua/CHANGELOG.md) under 0.1.0.

[0.6.0]: https://github.com/crankshift/lawpowers/releases/tag/v0.6.0
[0.5.0]: https://github.com/crankshift/lawpowers/releases/tag/v0.5.0
[0.4.2]: https://github.com/crankshift/lawpowers/releases/tag/v0.4.2
[0.4.1]: https://github.com/crankshift/lawpowers/releases/tag/v0.4.1
[0.4.0]: https://github.com/crankshift/lawpowers/releases/tag/v0.4.0
[0.3.0]: https://github.com/crankshift/lawpowers/releases/tag/v0.3.0
[0.2.0]: https://github.com/crankshift/lawpowers/releases/tag/v0.2.0
[0.1.0]: https://github.com/crankshift/lawpowers/releases/tag/v0.1.0

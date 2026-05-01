# lawpowers — monorepo

Monorepo of jurisdiction-specific legal plugins for **Claude Code and Codex**. One marketplace (`lawpowers`) hosts several plugins; each plugin wraps subagents and skills for a single legal system.

| Plugin | Jurisdiction | Command prefix | Working language | Documentation |
|---|---|---|---|---|
| [`ua`](./plugins/ua) | Ukraine | `/ua:…` | Ukrainian | [`ua/README.md`](./plugins/ua/README.md), [`ua/CLAUDE.md`](./plugins/ua/CLAUDE.md) |
| [`pl`](./plugins/pl) | Poland | `/pl:…` | Polish | [`pl/README.md`](./plugins/pl/README.md), [`pl/CLAUDE.md`](./plugins/pl/CLAUDE.md) |

Plugins are independent: users install whichever jurisdiction(s) they need. Namespaces (`ua:`, `pl:`) don't collide, so both can be active at once.

Alongside the plugins, the repo also hosts the public landing page under [`site/`](./site/) — a static Astro build deployed to Firebase Hosting. It is a separate sub-project (its own `package.json`, its own deploy flow, its own docs [`site/README.md`](./site/README.md) + [`site/CLAUDE.md`](./site/CLAUDE.md)) and is **not** a Claude Code plugin.

User-facing install instructions live in the root [`README.md`](./README.md). This file is for contributors working on the repo itself.

## Repository layout

```
lawpowers/                         # GitHub: crankshift/lawpowers
├── README.md                       # user-facing — install guide, links to per-plugin docs
├── CLAUDE.md                       # this file — Claude Code contributor context
├── AGENTS.md                       # Codex contributor context (mirrors CLAUDE.md for Codex)
├── CHANGELOG.md                    # index of per-plugin CHANGELOGs + monorepo-level structural log (English, dated entries, no monorepo version)
├── .version-bump.json              # maps versioned fields in plugin/marketplace manifests
├── LICENSE                         # MIT — covers the whole repo
├── .claude-plugin/
│   └── marketplace.json            # Claude Code marketplace catalog ("lawpowers")
├── .agents/
│   └── plugins/
│       └── marketplace.json        # Codex marketplace catalog (law-ua, law-pl)
├── .github/
│   ├── PULL_REQUEST_TEMPLATE.md    # prefills scope / CHANGELOG / test-plan checkboxes on every PR
│   └── ISSUE_TEMPLATE/
│       ├── config.yml              # hides blank issues; contact links to RELEASING.md, zakon.rada, ISAP
│       ├── bug_report.yml          # installation / runtime bugs
│       ├── legal-issue.yml         # outdated statute or wrong case-law; requires primary-source URL + date
│       └── feature_request.yml     # new agent / skill / jurisdiction / tooling
├── docs/
│   └── RELEASING.md                # full release procedure
├── scripts/
│   ├── release.sh                  # bump + PR + tag + GitHub Release helper
│   ├── convert-agents-to-codex.py  # generates .codex/agents/*.toml from Claude agents/*.md
│   └── validate-codex-agents.py    # validates generated Codex agent TOML files
├── plugins/                        # all jurisdiction plugins live here
│   ├── ua/                         # plugin "ua" — Ukrainian law
│   │   ├── README.md               # user-facing, Ukrainian
│   │   ├── CLAUDE.md               # Claude Code contributor context for the UA plugin
│   │   ├── AGENTS.md               # Codex contributor context for the UA plugin
│   │   ├── CHANGELOG.md            # plugin-level change log, Ukrainian
│   │   ├── .claude-plugin/plugin.json  # Claude Code manifest; name: "ua"
│   │   ├── .codex-plugin/plugin.json   # Codex manifest; name: "law-ua"
│   │   ├── .codex/agents/*.toml    # generated Codex custom-agent shims (from agents/*.md)
│   │   ├── agents/                 # source agent definitions (Claude + Codex source of truth)
│   │   └── skills/                 # skill definitions (shared by Claude Code and Codex)
│   └── pl/                         # plugin "pl" — Polish law
│       ├── README.md               # user-facing, Polish
│       ├── CLAUDE.md               # Claude Code contributor context for the PL plugin
│       ├── AGENTS.md               # Codex contributor context for the PL plugin
│       ├── CHANGELOG.md            # plugin-level change log, Polish
│       ├── .claude-plugin/plugin.json  # Claude Code manifest; name: "pl"
│       ├── .codex-plugin/plugin.json   # Codex manifest; name: "law-pl"
│       ├── .codex/agents/*.toml    # generated Codex custom-agent shims (from agents/*.md)
│       ├── agents/                 # source agent definitions (Claude + Codex source of truth)
│       └── skills/                 # skill definitions (shared by Claude Code and Codex)
└── site/                           # public landing page (static Astro site, not a plugin)
    ├── README.md                   # site quick-start, deploy flow
    ├── CLAUDE.md                   # site contributor context
    ├── astro.config.mjs            # Astro + i18n + sitemap config
    ├── firebase.json               # Firebase Hosting config (multi-site "lawpowers")
    ├── package.json                # separate deps: astro, @astrojs/sitemap, firebase-tools
    └── src/
        ├── data.ts                 # must mirror plugin counts / agent lists
        ├── i18n/index.ts
        ├── locales/{en,ua,pl}.ts
        ├── layouts/BaseLayout.astro
        ├── components/
        ├── styles/global.css
        └── pages/
            ├── index.astro         # root: browser-lang redirect
            └── [locale]/index.astro # /en/, /ua/, /pl/
```

## Issue and PR templates

`.github/` provides structured templates so the right metadata is captured up front:

- **Pull requests** — the template forces contributors to pick the change's scope (`ua` / `pl` / marketplace / monorepo), tick the right CHANGELOG files, describe migration for breaking changes, and confirm `claude plugin validate` passed. Enforce this during review — PRs without a completed template should be bounced.
- **Bug reports** — `bug_report.yml` captures plugin, plugin version, Claude Code version, client (CLI / Desktop App / IDE), and OS. Preflight checks include updating the marketplace before reporting.
- **Legal accuracy issues** — `legal-issue.yml` is the channel for "agent cites an outdated statute / wrong case number". It **requires** a primary-source URL (`zakon.rada.gov.ua` for UA, `isap.sejm.gov.pl` for PL) and a verification date. No source, no fix — this is the quality gate for legal content.
- **Feature requests** — `feature_request.yml` asks for the scope (existing plugin vs new jurisdiction), the practical legal task to solve, and primary-source citations. Cross-plugin feature proposals that would mix UA and PL legal content in one artifact are explicitly called out as out-of-scope.
- **Blank issues disabled** — all issues go through one of the three structured forms so triage is fast.

## Contribution principles

- **One jurisdiction = one plugin.** Don't mix UA and PL law inside the same agents or skills — each plugin stays self-contained.
- **Plugin language matches jurisdiction.** Agents, skills, templates, and plugin-level docs (`README.md`, `CLAUDE.md`, `CHANGELOG.md`) for `ua` are in Ukrainian; for `pl` in Polish. Root-level documentation (`README.md`, `CLAUDE.md`, `CHANGELOG.md` at the repo root) is in English for broad accessibility.
- **Root `CHANGELOG.md` is an index + monorepo-level log, not an aggregate.** Plugin content changes (new agents, new skills, updated statute refs) go in the plugin CHANGELOG only. The root file tracks cross-cutting structural moves, release tooling, and repo renames as dated entries — no monorepo version.
- **Command prefixes come from plugin names.** `name` in `plugin.json` becomes the namespace — `/ua:…`, `/pl:…`. Agent and skill file names inside the plugin don't need a prefix; Claude Code adds it automatically.
- **Shared license.** MIT, applied at the repo root.
- **Independent plugin versions.** Each plugin carries its own `version` in its `plugin.json` (and mirrored in the marketplace entry). The marketplace catalog itself has a separate version in `marketplace.json:metadata.version`.
- **Release tags — per plugin.** Tags are namespaced: `ua/vX.Y.Z`, `pl/vX.Y.Z`. The tag version always matches the plugin's `version` field exactly. Historical umbrella tags (`v0.1.0`…`v0.6.0`) remain on the repo but no new umbrella tags are created — they confused users who install plugins individually. Marketplace `metadata.version` is an internal field bumped on catalog-shape changes; it is **not** tagged publicly.

## Adding a new plugin (new jurisdiction)

Example: adding a plugin for EU law.

1. Create `./plugins/eu/` next to `./plugins/ua/` and `./plugins/pl/`. Short ISO-style code; keep it two or three letters where possible.
2. Lay out the plugin directory:
   ```
   plugins/eu/
   ├── README.md                    # user-facing documentation
   ├── CLAUDE.md                    # Claude Code contributor context
   ├── AGENTS.md                    # Codex contributor context
   ├── CHANGELOG.md                 # plugin-level change log
   ├── .claude-plugin/plugin.json   # Claude Code manifest; name: "eu", initial version 0.1.0
   ├── .codex-plugin/plugin.json    # Codex manifest; name: "law-eu" (collision-safe)
   ├── agents/                      # source agent definitions (shared by Claude + Codex)
   └── skills/                      # skill definitions (shared by Claude Code and Codex)
   ```
3. Register the plugin in both marketplace catalogs:
   - `.claude-plugin/marketplace.json` under `plugins[…]`:
     ```json
     { "name": "eu", "source": "./plugins/eu", "version": "0.1.0", ... }
     ```
   - `.agents/plugins/marketplace.json` with the collision-safe Codex ID (`law-eu`).
4. Update [`.version-bump.json`](./.version-bump.json) so the new plugin's version fields are tracked.
5. Bump the marketplace version in `.claude-plugin/marketplace.json:metadata.version`.
6. Add a CHANGELOG entry describing the new plugin.
7. Open a PR, merge, then tag the release (see [Release flow](#release-flow)).

## Landing site (`site/`)

The repo ships a static marketing landing alongside the plugins. It lives in [`site/`](./site/), is deployed to Firebase Hosting at `https://lawpowers.web.app/`, and is maintained independently of plugin releases.

- **Stack:** Astro 6 + plain CSS/JS, no runtime framework. Static output (`output: 'static'`) so crawlers index real HTML.
- **Languages:** EN, UA, PL — path-based routing (`/en/`, `/ua/`, `/pl/`). Dictionaries in `site/src/locales/`, structurally type-checked against the EN shape.
- **Deploy:** `cd site && pnpm deploy` (requires `pnpm exec firebase login` once per machine).
- **Release coupling:** **none.** The site isn't versioned with the marketplace — push it whenever a user-facing change lands. There's no `site/CHANGELOG.md` and no `site/` entry in `.version-bump.json`. The site *does* reflect plugin content (agent and skill lists with labels, counts derived from array lengths), so after a plugin bump update `site/src/data.ts` (add / remove entries in `UA_AGENTS` / `PL_AGENTS` / `UA_SKILLS` / `PL_SKILLS`) and the matching `agents_ua` / `agents_pl` / `skills_ua` / `skills_pl` label maps in `site/src/locales/*.ts`, then redeploy.
- **Editorial rules the site inherits:** same disclaimer discipline as the plugins (not legal advice, human review mandatory), same jurisdiction separation (no UA/PL mixing in one component), same no-fabrication rule (if it's not in `plugins/`, it's not on the landing).

Full contributor rules in [`site/CLAUDE.md`](./site/CLAUDE.md).

## Release flow

Full step-by-step reference with commands, common pitfalls, and rollback guidance — see [`docs/RELEASING.md`](./docs/RELEASING.md). Summary:

1. Pick the plugin (`ua` or `pl`) and the version per semver. For a breaking change in 0.x releases, a minor bump is appropriate.
2. Update the two version fields listed in [`.version-bump.json`](./.version-bump.json) for that plugin: `plugins/<P>/.claude-plugin/plugin.json:version` and `.claude-plugin/marketplace.json:plugins[N].version`. Validate with `claude plugin validate .`.
3. Add a new section at the top of that plugin's CHANGELOG in Keep-a-Changelog format:
   - [`plugins/ua/CHANGELOG.md`](./plugins/ua/CHANGELOG.md) (Ukrainian) — for `ua` releases.
   - [`plugins/pl/CHANGELOG.md`](./plugins/pl/CHANGELOG.md) (Polish) — for `pl` releases.
   - Root [`CHANGELOG.md`](./CHANGELOG.md) (English) — **only** for cross-cutting monorepo changes (add a new dated `### YYYY-MM-DD — …` entry to the monorepo-level log, not a versioned section). Ordinary plugin releases do not touch this file.
4. Open a PR (`release-<plugin>-vX.Y.Z`) and merge.
5. After merge, tag the merge commit as `<plugin>/vX.Y.Z` and push: `git tag -a <plugin>/vX.Y.Z <merge-sha> -m "..."` + `git push origin <plugin>/vX.Y.Z`.
6. Publish a GitHub Release titled `<plugin> vX.Y.Z` with body extracted from that plugin's CHANGELOG section.
7. Users update with `/plugin marketplace update lawpowers` + `/reload-plugins`.

Bumping marketplace `metadata.version` is separate — only needed when catalog shape changes (plugin added/removed). Use `./scripts/release.sh bump-marketplace X.Y.Z` and commit it like any other change; no tag, no GitHub Release.

## Shared editorial rules (all plugins)

- **Verbatim citations.** Statutes are quoted in the exact wording in force on a given date, with a link to the primary source.
  - UA primary source: `zakon.rada.gov.ua`.
  - PL primary source: `isap.sejm.gov.pl`.
- **No fabricated case law.** Case numbers, dates, and quotations come only from official registries. For UA use ЄДРСР (`reyestr.court.gov.ua`) and the Supreme Court site; for PL use Portal Orzeczeń, SN, NSA, TK. If a citation can't be verified, mark it unverified or omit it.
- **Placeholders for personal data.** Templates must use placeholders (`[ПІБ]`, `[РНОКПП]` for UA; `[imię i nazwisko]`, `[PESEL]` for PL). Never commit real client data.
- **Drafts, not final advice.** Everything agents produce is a working draft for a human lawyer to review and sign off on. Make that explicit in agent prompts and output.
- **Fast-moving law.** Both jurisdictions see frequent amendments (UA especially during martial law; PL around KPC and KC reforms). Agents should re-verify statute wording on each use rather than relying on cached knowledge.
- **Fetch-first for volatile values.** Skills and agents that embed legal amounts (fees, rates, thresholds, minimum wages) must include a **fetch-first block**: attempt `WebFetch` / `WebSearch` from the authoritative source before falling back to the hardcoded value. Hardcoded values are annotated with `_(fallback; станом на [date])_` (UA) or `_(fallback; stan na [date])_` (PL) so staleness is visible. See any `calculating-*` skill for the standard table format. When a parameter is already fetched by a canonical skill (e.g. ПМ in `calculating-sudovyi-zbir`, NBP rate in `calculating-odsetki`), other skills cross-reference it instead of duplicating fetch logic.

## Key resources per jurisdiction

| Country | Primary statutes | Case-law registry | Top court(s) |
|---|---|---|---|
| Ukraine | [zakon.rada.gov.ua](https://zakon.rada.gov.ua) | [reyestr.court.gov.ua](https://reyestr.court.gov.ua) (ЄДРСР) | [supreme.court.gov.ua](https://supreme.court.gov.ua) (Supreme Court), [ccu.gov.ua](https://ccu.gov.ua) (Constitutional Court) |
| Poland | [isap.sejm.gov.pl](https://isap.sejm.gov.pl), [dziennikustaw.gov.pl](https://dziennikustaw.gov.pl) | [orzeczenia.ms.gov.pl](https://orzeczenia.ms.gov.pl) (Portal Orzeczeń) | [sn.pl](https://www.sn.pl) (Sąd Najwyższy), [nsa.gov.pl](https://orzeczenia.nsa.gov.pl) (NSA), [trybunal.gov.pl](https://trybunal.gov.pl) (TK) |

For plugin-specific context (agent catalogs, jurisdiction-specific procedural rules, architectural notes) see the per-plugin `CLAUDE.md` files linked at the top.

## Codex support

This repository also ships Codex plugin metadata. Keep Claude and Codex surfaces in sync when changing plugin structure.

- Claude marketplace: `.claude-plugin/marketplace.json`; Codex marketplace: `.agents/plugins/marketplace.json`.
- Claude plugin manifests stay in `plugins/*/.claude-plugin/plugin.json`; Codex plugin manifests stay in `plugins/*/.codex-plugin/plugin.json`.
- Claude contributor instructions live in `CLAUDE.md`; Codex contributor instructions live in `AGENTS.md`.
- Claude plugin IDs remain `ua` and `pl`; Codex plugin IDs are `law-ua` and `law-pl` to avoid collisions with `businesspowers`.
- When adding a plugin, agent, skill, or public install instruction, update README, CLAUDE.md, AGENTS.md, and both manifest families as applicable.
- Codex custom-agent files live in `plugins/*/.codex/agents/*.toml` and are generated from Claude `agents/*.md` files.
- After changing any agent frontmatter/body, run `python3 scripts/convert-agents-to-codex.py` and `python3 scripts/validate-codex-agents.py`.
- Do not hand-edit generated Codex agent TOML unless you also update the converter; Claude agent files remain the source of truth.
- Current Codex plugin manifests do not declare agents directly, so `.codex/agents/` is the compatibility/import layer.

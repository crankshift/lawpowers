# lawpowers — monorepo

Monorepo of jurisdiction-specific legal plugins for **Claude Code**. One marketplace (`lawpowers`) hosts several plugins; each plugin wraps subagents and skills for a single legal system.

| Plugin | Jurisdiction | Command prefix | Working language | Documentation |
|---|---|---|---|---|
| [`ua`](./ua) | Ukraine | `/ua:…` | Ukrainian | [`ua/README.md`](./ua/README.md), [`ua/CLAUDE.md`](./ua/CLAUDE.md) |
| [`pl`](./pl) | Poland | `/pl:…` | Polish | [`pl/README.md`](./pl/README.md), [`pl/CLAUDE.md`](./pl/CLAUDE.md) |

Plugins are independent: users install whichever jurisdiction(s) they need. Namespaces (`ua:`, `pl:`) don't collide, so both can be active at once.

User-facing install instructions live in the root [`README.md`](./README.md). This file is for contributors working on the repo itself.

## Repository layout

```
lawpowers/                         # GitHub: crankshift/lawpowers
├── README.md                       # user-facing — install guide, links to per-plugin docs
├── CLAUDE.md                       # this file — contributor context
├── CHANGELOG.md                    # release history (Keep a Changelog, shared across all plugins)
├── .version-bump.json              # maps versioned fields in plugin/marketplace manifests
├── LICENSE                         # MIT — covers the whole repo
├── .claude-plugin/
│   └── marketplace.json            # marketplace catalog ("lawpowers"); lists ua and pl with their source paths
├── ua/                             # plugin "ua" — Ukrainian law
│   ├── README.md                   # user-facing, Ukrainian
│   ├── CLAUDE.md                   # contributor context for the UA plugin
│   ├── .claude-plugin/plugin.json  # name: "ua"
│   ├── agents/
│   └── skills/
└── pl/                             # plugin "pl" — Polish law
    ├── README.md                   # user-facing, Polish
    ├── CLAUDE.md                   # contributor context for the PL plugin
    ├── .claude-plugin/plugin.json  # name: "pl"
    ├── agents/
    └── skills/
```

## Contribution principles

- **One jurisdiction = one plugin.** Don't mix UA and PL law inside the same agents or skills — each plugin stays self-contained.
- **Plugin language matches jurisdiction.** Agents, skills, templates, and plugin-level docs for `ua` are in Ukrainian; for `pl` in Polish. This root-level documentation (README/CLAUDE/CHANGELOG) is in English for broad accessibility.
- **Command prefixes come from plugin names.** `name` in `plugin.json` becomes the namespace — `/ua:…`, `/pl:…`. Agent and skill file names inside the plugin don't need a prefix; Claude Code adds it automatically.
- **Shared license.** MIT, applied at the repo root.
- **Independent plugin versions.** Each plugin carries its own `version` in its `plugin.json` (and mirrored in the marketplace entry). The marketplace catalog itself has a separate version in `marketplace.json:metadata.version`.
- **Release tags.** `vX.Y.Z` at the marketplace level covers the whole repo. If a single plugin ever needs an independent release cycle, use namespaced tags like `ua/vX.Y.Z` — but the current convention is one monorepo-wide tag per release.

## Adding a new plugin (new jurisdiction)

Example: adding a plugin for EU law.

1. Create `./eu/` at the repo root. Short ISO-style code; keep it two or three letters where possible.
2. Lay out the plugin directory:
   ```
   eu/
   ├── README.md                    # user-facing documentation
   ├── CLAUDE.md                    # contributor context
   ├── .claude-plugin/plugin.json   # name: "eu", initial version 0.1.0
   ├── agents/
   └── skills/
   ```
3. Register the plugin in `.claude-plugin/marketplace.json` under `plugins[…]`:
   ```json
   { "name": "eu", "source": "./eu", "version": "0.1.0", ... }
   ```
4. Update [`.version-bump.json`](./.version-bump.json) so the new plugin's version fields are tracked.
5. Bump the marketplace version in `.claude-plugin/marketplace.json:metadata.version`.
6. Add a CHANGELOG entry describing the new plugin.
7. Open a PR, merge, then tag the release (see [Release flow](#release-flow)).

## Release flow

1. Decide the version bump per semver. For a breaking change in 0.x releases, a minor bump is appropriate.
2. Update the affected version fields listed in `.version-bump.json` (plugin-level `version` + corresponding marketplace entry + marketplace `metadata.version`).
3. Add a new section at the top of [`CHANGELOG.md`](./CHANGELOG.md) in Keep-a-Changelog format, noting which plugin(s) changed.
4. Open a PR and merge.
5. After merge, check out `main`, pull, and tag the merge commit:
   ```bash
   git tag -a vX.Y.Z <merge-sha> -m "vX.Y.Z — <headline>"
   git push origin vX.Y.Z
   ```
6. Create a GitHub Release with body copied from the CHANGELOG section:
   ```bash
   gh release create vX.Y.Z --title "vX.Y.Z — <headline>" --notes-file <(awk '/## \[X.Y.Z\]/,/## \[/' CHANGELOG.md | head -n -1) --latest
   ```
7. Users update with `/plugin marketplace update lawpowers` + `/reload-plugins`.

## Shared editorial rules (all plugins)

- **Verbatim citations.** Statutes are quoted in the exact wording in force on a given date, with a link to the primary source.
  - UA primary source: `zakon.rada.gov.ua`.
  - PL primary source: `isap.sejm.gov.pl`.
- **No fabricated case law.** Case numbers, dates, and quotations come only from official registries. For UA use ЄДРСР (`reyestr.court.gov.ua`) and the Supreme Court site; for PL use Portal Orzeczeń, SN, NSA, TK. If a citation can't be verified, mark it unverified or omit it.
- **Placeholders for personal data.** Templates must use placeholders (`[ПІБ]`, `[РНОКПП]` for UA; `[imię i nazwisko]`, `[PESEL]` for PL). Never commit real client data.
- **Drafts, not final advice.** Everything agents produce is a working draft for a human lawyer to review and sign off on. Make that explicit in agent prompts and output.
- **Fast-moving law.** Both jurisdictions see frequent amendments (UA especially during martial law; PL around KPC and KC reforms). Agents should re-verify statute wording on each use rather than relying on cached knowledge.

## Key resources per jurisdiction

| Country | Primary statutes | Case-law registry | Top court(s) |
|---|---|---|---|
| Ukraine | [zakon.rada.gov.ua](https://zakon.rada.gov.ua) | [reyestr.court.gov.ua](https://reyestr.court.gov.ua) (ЄДРСР) | [supreme.court.gov.ua](https://supreme.court.gov.ua) (Supreme Court), [ccu.gov.ua](https://ccu.gov.ua) (Constitutional Court) |
| Poland | [isap.sejm.gov.pl](https://isap.sejm.gov.pl), [dziennikustaw.gov.pl](https://dziennikustaw.gov.pl) | [orzeczenia.ms.gov.pl](https://orzeczenia.ms.gov.pl) (Portal Orzeczeń) | [sn.pl](https://www.sn.pl) (Sąd Najwyższy), [nsa.gov.pl](https://orzeczenia.nsa.gov.pl) (NSA), [trybunal.gov.pl](https://trybunal.gov.pl) (TK) |

For plugin-specific context (agent catalogs, jurisdiction-specific procedural rules, architectural notes) see the per-plugin `CLAUDE.md` files linked at the top.

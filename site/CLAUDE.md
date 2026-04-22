# site — contributor context

Static landing page for [lawpowers](../README.md). This is **not** a Claude Code plugin; no agents, no skills. Plugins live under [`../plugins/`](../plugins/).

The site is a thin consumer of the [`powers-landing-shell`](https://github.com/crankshift/powers-landing-shell) package. All components, layouts, styles, and i18n helpers live in the shell. This repo supplies only configuration (`src/config.ts`), locale dictionaries (`src/locales/`), and minimal page entry points (`src/pages/`).

See [README.md](./README.md) for the user-facing quick start. This file is contributor context — human or agent — for working on the site itself.

## Ground rules

### Static-first, vanilla JS

- Content is **pre-rendered to HTML** at build time (`output: 'static'`). Crawlers and first-paint get real markup, not a loading shell. This is the whole point of the site; don't regress it.
- **No React, no Vue, no Svelte, no runtime framework.** Interactivity (copy buttons, theme toggle, install-tab switcher) is handled by the shell's components. Astro bundles those scripts once per page.
- If a feature seems to need a framework, look for an Astro-native pattern first: view transitions, `<details>` / `<dialog>`, progressive enhancement with plain DOM APIs, or an `is:inline` script.

### Components and layouts

All visual components (`Nav`, `Hero`, `Plugins`, `PluginCard`, `Install`, `Principles`, `Sources`, `Disclaimer`, `Footer`, `BrandMark`, `Flag`, `CopyButton`), the `BaseLayout`, design tokens (`global.css`), and the theme bootstrap script live in [`powers-landing-shell`](https://github.com/crankshift/powers-landing-shell). This site does not contain its own components, layouts, or stylesheets.

To override a specific section's content, use `PageShell`'s named slots (see the shell's README for available slot names). Don't duplicate shell components locally.

### i18n

- Locales: `en`, `ua`, `pl`. Default: `en`. URL path: `/{locale}/`.
- Root `/` is a one-liner redirect page (`src/pages/index.astro`) using the shell's `RedirectShell` component.
- Dictionaries: `src/locales/{en,ua,pl}.ts`. **`en.ts` defines the shape** satisfying `ShellTranslation` from `powers-landing-shell`. `ua.ts` and `pl.ts` declare `export const <locale>: Translation = { … }`, so missing keys fail `astro check`.
- `src/locales/index.ts` re-exports all dictionaries as a `Record<LocaleCode, Translation>` for use with the shell's `getT()` helper.
- Update all three locales together. Translation tone per locale: UA dictionary in Ukrainian, PL in Polish, EN in English. Don't leak English into UA / PL (except verbatim code snippets like `/plugin install ua@lawpowers`).
- **hreflang uses ISO 639-1** (`en`, `uk` for Ukrainian — note `uk`, not `ua` — and `pl`). Our URL path uses `ua` for namespace parity with the plugin. The hreflang mapping now lives in the shell's i18n helpers (not a local `HREFLANG` map) — don't override it.

### Data source of truth

- Plugin catalogs (`UA_AGENTS`, `PL_AGENTS`, `UA_SKILLS`, `PL_SKILLS`) and the `SiteConfig` live in `src/config.ts`. These arrays must match the actual contents of `../plugins/ua/agents/`, `../plugins/pl/agents/`, `../plugins/ua/skills/`, `../plugins/pl/skills/`. When the monorepo bumps plugin contents, update the arrays in `config.ts` **and** the `agents_ua` / `agents_pl` / `skills_ua` / `skills_pl` label maps in every locale dictionary. The `satisfies Record<…, string>` constraint makes missing keys a type error — lean on that rather than grepping.
- The hero's "Subagents" / "Skills" stat and the per-card lists are both computed from these arrays by the shell — counts are derived from `.length` so they can't drift from the list.

### Copy discipline

- Text stays **factual** and **in the working language of each locale's audience**. Skip marketing superlatives.
- Don't invent features. The landing reflects what the plugins actually do; if a claim isn't backed by an existing agent or skill in `../plugins/`, don't put it on the landing.
- Disclaimer copy (`t.disclaimer.*`) must say "not legal advice" and make clear that a qualified human lawyer owns the final document. This is non-negotiable — same rule as the plugins.

### SEO

- Per-page `<title>` and `<meta description>` come from `t.seo` in each locale — keep them unique per locale and under ~160 chars where possible.
- The shell's `BaseLayout` renders Open Graph + Twitter tags, `theme-color`, and JSON-LD (`WebSite` + `Organization`). To extend the JSON-LD graph, do it in the shell repo, not locally.
- Social-card image is `public/og.png` (1200×630), referenced as `/og.png` from OG / Twitter tags. The source is `scripts/build-og.mjs` (SVG authored in-script, rasterized with `sharp`); the generated PNG is committed. Regenerate with `pnpm build:og` whenever the source SVG changes.
- `src/pages/index.astro` uses the shell's `RedirectShell` — it carries `noindex, follow` and is filtered out of the sitemap in `astro.config.mjs`. Don't let it drift back in or it'll duplicate the `/en/` canonical.
- Hreflang alternates must use ISO 639-1 (`en`, `uk`, `pl`) — see the i18n section. `x-default` points to `/en/`.

## Tech stack pin

| Thing | Version |
|---|---|
| Astro | `^6.1.8` |
| `@astrojs/sitemap` | `^3.7.2` |
| `@astrojs/check` | `^0.9.8` |
| TypeScript | `~6.0.2` |
| Node | `>= 22.12.0` |
| Firebase CLI | `^15.15.0` (devDependency) |

Package manager: **pnpm**. Lockfile (`pnpm-lock.yaml`) is the source of truth.

## Build & deploy

```bash
pnpm build   # astro check + astro build → dist/
pnpm deploy  # pnpm build + firebase deploy --only hosting:lawpowers
```

Firebase context:
- Project: `landings-d3578`
- Multi-site target: `lawpowers` → `https://lawpowers.web.app/`
- Target + public dir configured in `firebase.json`
- Web-SDK config (public identifiers) in `.env`; see `.env.example` for shape

## Do / don't

**Do**
- Keep changes in `src/config.ts` and `src/locales/` — the consumer's job is config and translations, not components.
- Use `PageShell`'s named slots to override specific sections when needed, rather than duplicating shell components locally.
- Pre-render everything that can be pre-rendered.
- Run `pnpm check` before committing any locale or config change.

**Don't**
- Don't add local components, layouts, or stylesheets. Those belong in `powers-landing-shell`. If you need a new section or a visual change, contribute it to the shell repo.
- Don't add a runtime framework. If you reach for React, stop and rethink.
- Don't fetch from `zakon.rada.gov.ua`, `isap.sejm.gov.pl`, or any other live legal source at build or runtime. The landing is static marketing; live data fetches belong in the plugins.
- Don't pipe real client data into locale strings. Placeholders only (`[ПІБ]`, `[imię i nazwisko]`, etc.) — same rule as the plugins.
- Don't mix UA and PL content in one locale key or config entry. Keep parallel, jurisdiction-separated, like the plugins themselves.
- Don't commit `.env` — it's git-ignored for a reason. Use `.env.example` to document shape.

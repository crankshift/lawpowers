# lawpowers-site

Static marketing landing for the [lawpowers](../README.md) marketplace, built with **Astro 6** and deployed to **Firebase Hosting**. Multilingual (EN / UA / PL), SEO-first, no runtime framework.

This is a separate sub-project inside the [lawpowers](../) monorepo. It is **not** a Claude Code plugin — no agents, no skills. Plugins live under [`../plugins/`](../plugins/).

## Stack

- **[Astro](https://astro.build) 6.1.8** — static site generator, output: `static`
- **No JS framework** — interactivity (copy buttons, theme toggle, install-tab switcher) is plain `<script>` inside `.astro` components
- **Design tokens** — CSS custom properties in `src/styles/global.css`, `[data-theme="dark"]` swap
- **Native Astro i18n** — `/en/`, `/ua/`, `/pl/` routes; root `/` detects browser language and redirects
- **[`@astrojs/sitemap`](https://docs.astro.build/en/guides/integrations-guide/sitemap/)** — generates `sitemap-index.xml` with hreflang alternates
- **Firebase Hosting** — multi-site target `lawpowers` in project `landings-d3578`

Per-page first paint is ~11 KB gzipped (HTML + inline CSS + inline scripts). Zero external JS bundle.

## Local development

```bash
pnpm install
pnpm dev         # http://localhost:4321
pnpm check       # astro check (type errors + syntax)
pnpm build       # astro check + astro build → dist/
pnpm preview     # local preview of dist/
pnpm build:og    # regenerate public/og.png from scripts/build-og.mjs
```

Requires **Node ≥ 22.12.0** and **pnpm**.

## Deploy

```bash
pnpm exec firebase login     # one-time, per machine
pnpm deploy                   # → https://lawpowers.web.app/
```

`pnpm deploy` runs `astro check`, builds to `dist/`, then `firebase deploy --only hosting:lawpowers`. `public/og.png` is committed to the repo, so a plain `pnpm deploy` always ships the current social card — you don't need to run `pnpm build:og` unless you've changed the SVG source in `scripts/build-og.mjs`.

## Project structure

```
site/
├── astro.config.mjs          # site URL, i18n config, sitemap integration
├── firebase.json             # Firebase Hosting config (multi-site target "lawpowers")
├── .firebaserc               # Firebase project: landings-d3578
├── .env                      # PUBLIC_FIREBASE_* (public identifiers, git-ignored)
├── .env.example              # template for contributors
├── tsconfig.json             # extends astro/tsconfigs/strict
├── public/
│   ├── robots.txt
│   └── og.png               # 1200×630 social card, committed; regen via `pnpm build:og`
├── scripts/
│   └── build-og.mjs         # SVG → PNG via sharp; source of truth for og.png
└── src/
    ├── data.ts               # plugin constants (agents, skills, sources)
    ├── i18n/index.ts         # Lang type, HREFLANG map, getT()
    ├── locales/
    │   ├── en.ts             # EN dictionary (shape source of truth)
    │   ├── ua.ts             # UA dictionary
    │   └── pl.ts             # PL dictionary
    ├── layouts/
    │   └── BaseLayout.astro  # <head>: meta, canonical, hreflang, og/twitter, theme-color, JSON-LD, theme bootstrap
    ├── components/           # Nav, Hero, Plugins, PluginCard, Install, Principles,
    │                         #   Sources, Disclaimer, Footer, BrandMark, Flag, CopyButton
    ├── styles/
    │   └── global.css        # oklch tokens, reset, typography, .container, .section, .eyebrow
    └── pages/
        ├── index.astro       # root: <meta refresh> + JS Accept-Language redirect
        └── [locale]/
            └── index.astro   # dynamic route → /en/, /ua/, /pl/
```

## Content changes

Translations live in **`src/locales/{en,ua,pl}.ts`** as typed objects. `en.ts` defines the `Translation` shape; `ua.ts` and `pl.ts` declare `export const ua: Translation = { … }` — missing or extra keys fail `astro check` at build time. Update all three in lockstep.

Plugin catalogs surface twice on the landing: the hero's stats strip (totals) and the plugin cards (per-item lists of agents and skills). Source of truth: **`src/data.ts`** — `UA_AGENTS`, `PL_AGENTS`, `UA_SKILLS`, `PL_SKILLS` arrays; `UA_SKILLS_COUNT` / `PL_SKILLS_COUNT` are derived from `.length`. These arrays must mirror the actual contents of `../plugins/ua/agents/`, `../plugins/pl/agents/`, `../plugins/ua/skills/`, `../plugins/pl/skills/`. When you add or remove an agent / skill, update the array **and** the corresponding label map in every locale (`agents_ua` / `agents_pl` / `skills_ua` / `skills_pl` in `src/locales/{en,ua,pl}.ts`) — the `satisfies Record<…, string>` constraint makes missing keys a type error at `astro check` time.

## Firebase config

| | |
|---|---|
| Project | `landings-d3578` |
| Multi-site target | `lawpowers` |
| Live URL | `https://lawpowers.web.app/` (and `.firebaseapp.com`) |
| Config file | `firebase.json` — `hosting.site: "lawpowers"`, `public: "dist"`, `trailingSlash: true` |

Web-SDK config (`apiKey`, `authDomain`, etc.) is in `.env` — see `.env.example` for the shape. These are **public identifiers**, not secrets, but **restrict the API key in [Cloud Console → Credentials](https://console.cloud.google.com/apis/credentials?project=landings-d3578)** by HTTP referrer once the domain is live. Add `https://lawpowers.web.app/*`, `https://lawpowers.firebaseapp.com/*`, and any custom domain.

### Custom domain

1. Firebase Console → Hosting → `lawpowers` → **Add custom domain**
2. Follow the A / CNAME instructions; SSL auto-provisions
3. Update `SITE` in `astro.config.mjs` to the new origin
4. Update `public/robots.txt` sitemap URL
5. `pnpm deploy`

Canonical URLs, hreflang links, Open Graph URLs, and the sitemap are all driven from `SITE` — one change, all three locales update.

## SEO

Built in:
- `<link rel="canonical">` per locale
- Full `hreflang` set (`en`, `uk` for Ukrainian, `pl`, `x-default`) on every page
- Open Graph + Twitter card meta per locale (`og:locale`, `og:locale:alternate`, `og:site_name`)
- Social card at `public/og.png` (1200×630), referenced from `og:image` + `twitter:image` with width / height / type / alt. Source is `scripts/build-og.mjs` (SVG authored inline, rasterized with `sharp`); regenerate with `pnpm build:og`
- `theme-color` meta with `prefers-color-scheme` variants for mobile browser chrome
- JSON-LD `@graph` (`WebSite` + `Organization`, localized `inLanguage`) inlined in `BaseLayout.astro`
- `sitemap-index.xml` + per-URL alternate links via `@astrojs/sitemap`. Root `/` is filtered out of the sitemap (it's a redirect shell carrying `noindex, follow`) so only `/en/`, `/ua/`, `/pl/` appear — no competing `hreflang="en"` URLs
- `robots.txt` → sitemap
- `<html lang>` pulled from `HREFLANG` map
- `trailingSlash: 'always'` in Astro + `trailingSlash: true` in Firebase — canonical URLs end in `/`, no duplicate-content risk

Content (headings, paragraphs, agent lists) is rendered into HTML at build — no client-side hydration for crawlers.

## Disclaimer

This landing is marketing copy for a **drafting aid**. The plugins it promotes are not legal advice. See the [root README](../README.md) for the full liability disclaimer — the same terms apply to anything on this landing and to the marketplace as a whole.

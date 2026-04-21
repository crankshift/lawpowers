# site — contributor context

Static landing page for [lawpowers](../README.md). This is **not** a Claude Code plugin; no agents, no skills. Plugins live under [`../plugins/`](../plugins/).

See [README.md](./README.md) for the user-facing quick start. This file is contributor context — human or agent — for working on the site itself.

## Ground rules

### Static-first, vanilla JS

- Content is **pre-rendered to HTML** at build time (`output: 'static'`). Crawlers and first-paint get real markup, not a loading shell. This is the whole point of the site; don't regress it.
- **No React, no Vue, no Svelte, no runtime framework.** Interactivity is colocated in `<script>` blocks inside `.astro` components (copy buttons, theme toggle, install-tab switcher). Astro bundles those scripts once per page.
- If a feature seems to need a framework, look for an Astro-native pattern first: view transitions, `<details>` / `<dialog>`, progressive enhancement with plain DOM APIs, or an `is:inline` script.

### Design tokens & styling

- Tokens are **CSS custom properties** in `src/styles/global.css` under `:root` (light) and `:root[data-theme='dark']` (dark).
- Values use `oklch()` — preserve that. Don't convert to hex/hsl unless you've got a specific reason (e.g. `#fff` in a flag).
- Component styles live in **`<style>` blocks inside each `.astro` file** (scoped by default via Astro's `data-astro-cid-*`). Don't dump styles into a global file.
- Shared primitives (`.container`, `.section`, `.section-head`, `.eyebrow`) are intentionally global — reuse, don't redeclare.
- Theme bootstrap is an `is:inline` `<script>` in `BaseLayout.astro` that runs before first paint to set `data-theme`. Don't move it or FOUC returns.

### i18n

- Locales: `en`, `ua`, `pl`. Default: `en`. URL path: `/{locale}/`.
- Root `/` is a minimal redirect page (`src/pages/index.astro`) — `<meta http-equiv="refresh">` plus an inline JS that reads `navigator.languages` and replaces location.
- Dictionaries: `src/locales/{en,ua,pl}.ts`. **`en.ts` defines the shape** via `export type Translation = typeof en`. `ua.ts` and `pl.ts` declare `export const <locale>: Translation = { … }`, so missing keys fail `astro check`.
- Update all three locales together. Translation tone per locale: UA dictionary in Ukrainian, PL in Polish, EN in English. Don't leak English into UA / PL (except verbatim code snippets like `/plugin install ua@lawpowers`).
- **hreflang uses ISO 639-1** (`en`, `uk` for Ukrainian — note `uk`, not `ua` — and `pl`). Our URL path uses `ua` for namespace parity with the plugin. The mapping lives in `HREFLANG` in `src/i18n/index.ts` — don't break it.

### Data source of truth

- Plugin counts (`UA_AGENTS`, `PL_AGENTS`, `UA_SKILLS_COUNT`, `PL_SKILLS_COUNT`) in `src/data.ts` must match the actual contents of `../plugins/ua/agents/`, `../plugins/pl/agents/`, etc. When the monorepo bumps plugin contents, update this file **and** the `agents_ua` / `agents_pl` label maps in every locale dictionary. Mismatches mislead users.
- The hero's "Subagents" / "Skills" stat is computed from these arrays — don't hardcode numbers in JSX.

### Copy discipline

- Text stays **factual** and **in the working language of each locale's audience**. Skip marketing superlatives.
- Don't invent features. The landing reflects what the plugins actually do; if a claim isn't backed by an existing agent or skill in `../plugins/`, don't put it on the landing.
- Disclaimer copy (`t.disclaimer.*`) must say "not legal advice" and make clear that a qualified human lawyer owns the final document. This is non-negotiable — same rule as the plugins.

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

## Adding a new section

1. Create `src/components/MySection.astro` with frontmatter (props, optional imports) and `<style>` for scoped CSS.
2. Add copy keys under the relevant top-level area in `src/locales/en.ts` — `ua.ts` and `pl.ts` will fail type-check until you also update them.
3. Import and compose it in `src/pages/[locale]/index.astro`.
4. `pnpm check` before committing.

## Adding interactivity

Pattern: data-attributes on the markup + a single delegated `<script>` in the same `.astro` file.

```astro
---
interface Props { text: string }
const { text } = Astro.props
---

<button class="my-btn" data-payload={text}>Click me</button>

<script>
  document.addEventListener('click', (e) => {
    const btn = (e.target as HTMLElement)?.closest<HTMLButtonElement>('.my-btn')
    if (!btn) return
    // …use btn.dataset.payload
  })
</script>

<style>
  .my-btn { /* … */ }
</style>
```

Astro bundles the `<script>` once per page even if the component renders multiple times. For scripts that must run **before paint** (e.g. theme bootstrap), mark them `is:inline`.

## Do / don't

**Do**
- Match Astro's `.astro` conventions: frontmatter between `---`, props via `Astro.props`, scoped CSS via `<style>`.
- Use `class:list` for conditional classes.
- Inline SVGs for small icons. No icon font, no icon library.
- Keep long commands visually manageable via `overflow-x: auto` or `text-overflow: ellipsis` — the copy button guarantees the full text is still copyable.
- Pre-render everything that can be pre-rendered.

**Don't**
- Don't add a runtime framework. If you reach for React, stop and rethink.
- Don't fetch from `zakon.rada.gov.ua`, `isap.sejm.gov.pl`, or any other live legal source at build or runtime. The landing is static marketing; live data fetches belong in the plugins.
- Don't pipe real client data into locale strings. Placeholders only (`[ПІБ]`, `[imię i nazwisko]`, etc.) — same rule as the plugins.
- Don't mix UA and PL content in one component. Keep parallel, jurisdiction-separated, like the plugins themselves.
- Don't commit `.env` — it's git-ignored for a reason. Use `.env.example` to document shape.

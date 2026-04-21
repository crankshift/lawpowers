// @ts-check
import { defineConfig } from 'astro/config'
import sitemap from '@astrojs/sitemap'

// Update this to the canonical production URL before deploying.
// Firebase multi-site target "lawpowers" in project "landings-d3578":
//   https://lawpowers.web.app
// Switch to your custom domain once attached.
const SITE = 'https://lawpowers.web.app'

export default defineConfig({
  site: SITE,
  trailingSlash: 'always',
  build: {
    format: 'directory',
  },
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ua', 'pl'],
    routing: {
      prefixDefaultLocale: true,
      redirectToDefaultLocale: false,
    },
  },
  integrations: [
    sitemap({
      // `/` is a JS + meta-refresh redirect shell (see src/pages/index.astro).
      // It carries noindex and canonicalizes to /en/, so keeping it out of
      // the sitemap prevents two URLs from claiming hreflang="en".
      filter: (page) => page !== `${SITE}/`,
      i18n: {
        defaultLocale: 'en',
        locales: {
          en: 'en',
          ua: 'uk',
          pl: 'pl',
        },
      },
    }),
  ],
})

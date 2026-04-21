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

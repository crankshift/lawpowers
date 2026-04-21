import { en } from '../locales/en'
import { ua } from '../locales/ua'
import { pl } from '../locales/pl'
import type { Translation } from '../locales/en'

export type Lang = 'en' | 'ua' | 'pl'

export const LANGS = ['en', 'ua', 'pl'] as const

/**
 * ISO 639-1 code sent to crawlers in hreflang tags.
 * Our URL path uses `ua` (country-style) for familiarity, but Google
 * requires `uk` for Ukrainian.
 */
export const HREFLANG: Record<Lang, string> = {
  en: 'en',
  ua: 'uk',
  pl: 'pl',
}

export const OG_LOCALE: Record<Lang, string> = {
  en: 'en_US',
  ua: 'uk_UA',
  pl: 'pl_PL',
}

const DICTS: Record<Lang, Translation> = { en, ua, pl }

export function getT(lang: Lang): Translation {
  return DICTS[lang]
}

export function isLang(value: string | undefined): value is Lang {
  return value === 'en' || value === 'ua' || value === 'pl'
}

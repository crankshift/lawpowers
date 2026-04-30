import type { SiteConfig } from 'powers-landing-shell/types'

export const UA_AGENTS = [
  'claim-drafter',
  'response-drafter',
  'appeal-drafter',
  'motion-drafter',
  'legal-memo',
  'legislation-analyst',
  'request-drafter',
  'contract-drafter',
  'debt-collector',
  'enforcement-agent',
  'arbitration-agent',
  'raport-drafter',
  'vlk-appeal',
  'military-social-benefits',
  'mobilization-defense',
  'szch-defense',
] as const
export type UaAgent = (typeof UA_AGENTS)[number]

export const UA_SKILLS = [
  'fetching-zakon-rada',
  'searching-edrsr',
  'citing-ukrainian-law',
  'determining-ua-jurisdiction',
  'calculating-sudovyi-zbir',
  'checking-pozovna-davnist',
  'checking-martial-law-overrides',
  'fetching-arbitration-rules',
  'applying-new-york-convention',
  'military-statute-refs',
  'calculating-military-payments',
  'vlk-procedure',
  'szch-decriminalization',
  'reviewing-vehicle-contract',
  'reviewing-real-estate-contract',
  'reviewing-b2b-service-contract',
  'applying-cnap-passport',
  'applying-servisnyi-centr-mvs',
  'applying-consular-procedures',
] as const
export type UaSkill = (typeof UA_SKILLS)[number]

export const PL_AGENTS = [
  'claim-drafter',
  'response-drafter',
  'appeal-drafter',
  'motion-drafter',
  'legal-memo',
  'legislation-analyst',
  'request-drafter',
  'contract-drafter',
  'debt-collector',
  'enforcement-agent',
  'arbitration-agent',
  'consumer-drafter',
  'criminal-complaint-drafter',
  'family-drafter',
  'inheritance-drafter',
  'labor-drafter',
  'rodo-compliance',
] as const
export type PlAgent = (typeof PL_AGENTS)[number]

export const PL_SKILLS = [
  'fetching-isap-sejm',
  'searching-orzeczenia',
  'searching-krs',
  'citing-polish-law',
  'determining-pl-jurisdiction',
  'determining-wps',
  'calculating-oplata-sadowa',
  'calculating-odsetki',
  'calculating-alimenty',
  'checking-przedawnienie',
  'fetching-arbitration-rules',
  'applying-new-york-convention',
  'applying-frankowicze-case-law',
  'applying-rodo',
  'reviewing-vehicle-contract',
  'reviewing-real-estate-contract',
  'reviewing-b2b-service-contract',
  'applying-usc-procedures',
  'applying-zus-procedures',
  'applying-skarbowy-procedures',
  'applying-cudzoziemcy-procedures',
] as const
export type PlSkill = (typeof PL_SKILLS)[number]

export const PLUGIN_CODES = ['ua', 'pl'] as const
export type PluginCode = (typeof PLUGIN_CODES)[number]

export const LOCALE_CODES = ['en', 'ua', 'pl'] as const
export type LocaleCode = (typeof LOCALE_CODES)[number]

const FLAG_UA =
  '<span style="width:44px;height:30px;border-radius:4px;overflow:hidden;flex-shrink:0;border:1px solid var(--rule);display:grid;grid-template-rows:1fr 1fr" aria-hidden="true"><span style="background:#0057b7"></span><span style="background:#ffd700"></span></span>'

const FLAG_PL =
  '<span style="width:44px;height:30px;border-radius:4px;overflow:hidden;flex-shrink:0;border:1px solid var(--rule);display:grid;grid-template-rows:1fr 1fr" aria-hidden="true"><span style="background:#fff"></span><span style="background:#dc143c"></span></span>'

export const site: SiteConfig<PluginCode, LocaleCode> = {
  brand: 'lawpowers',
  repo: 'crankshift/lawpowers',
  url: 'https://lawpowers.web.app',
  defaultLocale: 'en',
  locales: [
    { code: 'en', hreflang: 'en', ogLocale: 'en_US', displayName: 'EN' },
    { code: 'ua', hreflang: 'uk', ogLocale: 'uk_UA', displayName: 'УКР' },
    { code: 'pl', hreflang: 'pl', ogLocale: 'pl_PL', displayName: 'PL' },
  ],
  plugins: [
    {
      code: 'ua',
      agents: UA_AGENTS,
      skills: UA_SKILLS,
      sources: [
        { name: 'zakon.rada.gov.ua', url: 'zakon.rada.gov.ua' },
        { name: 'ЄДРСР', url: 'reyestr.court.gov.ua' },
        { name: 'Верховний Суд', url: 'supreme.court.gov.ua' },
        { name: 'Конституційний Суд', url: 'ccu.gov.ua' },
        { name: "Мін'юст", url: 'minjust.gov.ua' },
        { name: 'Судова влада', url: 'court.gov.ua' },
      ],
      flag: FLAG_UA,
    },
    {
      code: 'pl',
      agents: PL_AGENTS,
      skills: PL_SKILLS,
      sources: [
        { name: 'ISAP Sejm', url: 'isap.sejm.gov.pl' },
        { name: 'Dziennik Ustaw', url: 'dziennikustaw.gov.pl' },
        { name: 'Portal Orzeczeń', url: 'orzeczenia.ms.gov.pl' },
        { name: 'Sąd Najwyższy', url: 'sn.pl' },
        { name: 'NSA / WSA', url: 'orzeczenia.nsa.gov.pl' },
        { name: 'Trybunał Konstytucyjny', url: 'trybunal.gov.pl' },
      ],
      flag: FLAG_PL,
    },
  ],
}

export const REPO = 'crankshift/lawpowers'
export const REPO_URL = `https://github.com/${REPO}`

export const SUPPORTED_LANGS = ['en', 'ua', 'pl'] as const
export type Lang = (typeof SUPPORTED_LANGS)[number]

export function isLang(value: string | undefined): value is Lang {
  return value !== undefined && (SUPPORTED_LANGS as readonly string[]).includes(value)
}

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
  'applying-cnap-passport',
  'applying-servisnyi-centr-mvs',
  'applying-consular-procedures',
] as const

export const UA_SKILLS_COUNT = UA_SKILLS.length

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
  'applying-usc-procedures',
  'applying-zus-procedures',
  'applying-skarbowy-procedures',
  'applying-cudzoziemcy-procedures',
] as const

export const PL_SKILLS_COUNT = PL_SKILLS.length

export type UaAgent = (typeof UA_AGENTS)[number]
export type PlAgent = (typeof PL_AGENTS)[number]
export type UaSkill = (typeof UA_SKILLS)[number]
export type PlSkill = (typeof PL_SKILLS)[number]

export interface Source {
  name: string
  url: string
}

export const UA_SOURCES: readonly Source[] = [
  { name: 'zakon.rada.gov.ua', url: 'zakon.rada.gov.ua' },
  { name: 'ЄДРСР', url: 'reyestr.court.gov.ua' },
  { name: 'Верховний Суд', url: 'supreme.court.gov.ua' },
  { name: 'Конституційний Суд', url: 'ccu.gov.ua' },
  { name: "Мін'юст", url: 'minjust.gov.ua' },
  { name: 'Судова влада', url: 'court.gov.ua' },
]

export const PL_SOURCES: readonly Source[] = [
  { name: 'ISAP Sejm', url: 'isap.sejm.gov.pl' },
  { name: 'Dziennik Ustaw', url: 'dziennikustaw.gov.pl' },
  { name: 'Portal Orzeczeń', url: 'orzeczenia.ms.gov.pl' },
  { name: 'Sąd Najwyższy', url: 'sn.pl' },
  { name: 'NSA / WSA', url: 'orzeczenia.nsa.gov.pl' },
  { name: 'Trybunał Konstytucyjny', url: 'trybunal.gov.pl' },
]

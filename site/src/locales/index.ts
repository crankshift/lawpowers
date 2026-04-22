import { en } from './en'
import { ua } from './ua'
import { pl } from './pl'
import type { Translation } from './en'
import type { LocaleCode } from '../config'

export const dicts: Record<LocaleCode, Translation> = { en, ua, pl }
export type { Translation }

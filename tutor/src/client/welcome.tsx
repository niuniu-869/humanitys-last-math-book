/**
 * 答疑版的欢迎页：
 * - 文案：dsh 的词典一个命名空间只能有一个主人，不能直接改别的插件的文案。这里用官方留的扩展口「语言包」，
 *   加一门继承简体中文的「简体中文（答疑）」，只覆盖欢迎页标题和输入框提示；界面是简体中文时自动切过去。
 * - 标题前的图标换成大肥鱼。
 */
import { api } from './catalog.ts'

const LOCALE = 'zh-x-tutor'
const BASE = 'zh'

/** dsh-client-locale `LocaleRuntime` 中用到的部分。 */
export interface LocaleRuntime {
  addLanguage(input: { id: string; label: string; fallback: string }): () => void
  register(ns: string, locale: string, dict: Record<string, string>): () => void
  getLocale(): { active: string }
  setLocale(id: string): void
}

const COPY: Record<string, string> = {
  'hero.headline': '今天卡在哪一题？',
  'hero.preview': '教材答疑',
  'placeholder.hero': '输入 @ 选题号、页码或单元，也可以直接说卡在哪',
  'placeholder.default': '接着问：@ 引用题号或页码，或者把你的解答贴上来',
}

export function installCopy(locale: LocaleRuntime, effect: (fn: () => () => void, label: string) => void): void {
  effect(() => locale.addLanguage({ id: LOCALE, label: '简体中文（答疑）', fallback: BASE }), 'hlmb: tutor language')
  effect(() => locale.register('conversation', LOCALE, COPY), 'hlmb: tutor copy')
  if (locale.getLocale().active === BASE) locale.setLocale(LOCALE)
}

export function HeroMark({ size, className }: { size: number; className?: string }) {
  return (
    <img src={api('art/fish-avatar.webp')} width={size} height={size} alt="" className={className}
      style={{ borderRadius: '50%', objectFit: 'cover', background: 'var(--dsw-alias-bg-base)' }} />
  )
}

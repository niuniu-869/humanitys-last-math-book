/**
 * 给模型用的三个查找功能，分工互不重叠：
 * - outline：看结构（全书 → 分册 → 单元的小节、例题、题目和页码），回答「有什么、在哪」。
 * - search：按关键词定位，回答「讲到某个概念的是哪几处」；只返回片段和引用，不返回全文。
 * - read：按引用读原文，回答「这里到底写了什么」。
 * 搜索语料按讲义小节、速记表、题目、例题、答案切开，互不重叠；PDF 页面文字是同一内容的有损副本，不进搜索。
 */
import { CHEATSHEET, displayLabel, type Item, type Material, type Ref, stemHint } from './material.ts'

export const DOC_KINDS = ['讲义', '速记', '题目', '例题', '答案'] as const
export type DocKind = (typeof DOC_KINDS)[number]

interface Doc {
  ref: string
  kind: DocKind
  book: string
  unit: string
  title: string
  text: string
  /** 小写后的标题 + 正文，搜索用。 */
  hay: string
}

export const REF_HELP = '引用写法：题号 L8-05、例题 Z1·例01、页码 L/140、单元 L8、小节 L8§3（L8§0 是开篇，另有 L8§小结、L8§速记）'

const SEARCH_LIMIT = 8
const SEARCH_MAX = 20
const SNIPPET_BEFORE = 40
const SNIPPET_AFTER = 100

const corpora = new WeakMap<Material, Doc[]>()

const doc = (d: Omit<Doc, 'hay'>): Doc => ({ ...d, hay: `${d.title}\n${d.text}`.toLowerCase() })

function corpus(m: Material): Doc[] {
  let docs = corpora.get(m)
  if (docs) return docs
  docs = []
  for (const book of m.bookIds) {
    for (const unit of m.book(book)!.units) {
      const u = m.unit(book, unit)
      if (!u) continue
      for (const s of m.sections(book, unit)) docs.push(doc({ ref: `${unit}§${s.key}`, kind: '讲义', book, unit, title: `${u.title} › ${s.title}`, text: s.text }))
      if (u.cheatsheet) docs.push(doc({ ref: `${unit}§${CHEATSHEET}`, kind: '速记', book, unit, title: `${u.title} › 速记表`, text: u.cheatsheet }))
    }
  }
  for (const [id, it] of m.items()) {
    const kind: DocKind = it.kind === 'problem' ? '题目' : '例题'
    docs.push(doc({ ref: id, kind, book: it.book, unit: it.unit, title: displayLabel(it), text: it.md }))
    if (it.kind === 'problem' && it.answer) docs.push(doc({ ref: id, kind: '答案', book: it.book, unit: it.unit, title: `${id} 的答案`, text: it.answer }))
  }
  corpora.set(m, docs)
  return docs
}

const firstPage = (it: Item): number | undefined => it.pages.problem?.[0] ?? it.pages.lesson?.[0]
const itemTitle = (it: Item): string => (it.kind === 'problem' ? displayLabel(it) : `${displayLabel(it)}：${stemHint(it)}`)
const pageNote = (book: string, page: number | undefined): string => (page === undefined ? '' : `（${book} 第 ${page} 页）`)

/** 范围：分册号或单元号，两者同名（如 C1）时指分册，单元写成 C1/C1；不在白名单里时报错。 */
function scopeFilter(m: Material, scope: string | undefined): (d: { book: string; unit: string }) => boolean {
  if (!scope) return () => true
  if (m.book(scope)) return (d) => d.book === scope
  const u = m.unitOf(scope)
  if (u) return (d) => d.book === u.book && d.unit === u.unit
  throw new Error(`范围「${scope}」不是分册号也不是单元号。分册有：${m.bookIds.join('、')}`)
}

export function outline(m: Material, scope?: string): string {
  if (!scope) {
    return m.books().map((b) => {
      const units = m.book(b.id)!.units.map((u) => `  - ${u}：${m.unit(b.id, u)?.title ?? u}`)
      return [`${b.id}《${b.title}》，${b.pages} 页`, ...units].join('\n')
    }).join('\n')
  }
  const book = m.book(scope)
  if (book) {
    return [`${scope}《${book.title}》，${book.pages} 页`, ...book.units.map((u) => {
      const sections = m.sections(scope, u).map((s) => `    - ${u}§${s.key}：${s.title}`)
      return [`  - ${u}：${m.unit(scope, u)?.title ?? u}`, ...sections].join('\n')
    })].join('\n')
  }
  const ref = m.unitOf(scope)
  if (!ref) throw new Error(`「${scope}」不是分册号也不是单元号。分册有：${m.bookIds.join('、')}`)
  const { book: b, unit: id } = ref
  const u = m.unit(b, id)!
  const items = m.items().filter(([, it]) => it.unit === id && it.book === b)
  const list = (kind: Item['kind'], name: string): string[] => {
    const rows = items.filter(([, it]) => it.kind === kind).map(([id, it]) => `  - ${id}：${itemTitle(it)}${pageNote(b, firstPage(it))}`)
    return rows.length ? [`${name}：`, ...rows] : []
  }
  return [
    `${id}：${u.title}（分册 ${b}）`,
    '讲义小节：',
    ...m.sections(b, id).map((s) => `  - ${id}§${s.key}：${s.title}（${s.text.length} 字）`),
    `  - ${id}§${CHEATSHEET}：速记表`,
    ...list('example', '例题'),
    ...list('practice', '随堂练习'),
    ...list('problem', '题目'),
  ].join('\n')
}

function snippet(d: Doc, terms: readonly string[]): string {
  const body = d.text.toLowerCase()
  const at = terms.map((t) => body.indexOf(t)).filter((i) => i >= 0).sort((a, b) => a - b)[0] ?? 0
  const start = Math.max(0, at - SNIPPET_BEFORE)
  const cut = d.text.slice(start, at + SNIPPET_AFTER).replace(/\s+/g, ' ').trim()
  return `${start > 0 ? '…' : ''}${cut}${at + SNIPPET_AFTER < d.text.length ? '…' : ''}`
}

function count(hay: string, term: string): number {
  let n = 0
  for (let i = hay.indexOf(term); i >= 0 && n < 5; i = hay.indexOf(term, i + term.length)) n++
  return n
}

export interface SearchOptions {
  scope?: string
  kinds?: readonly string[]
  limit?: number
}

/**
 * 关键词搜索。多个关键词用空格隔开，先找同时包含全部关键词的；一处都没有时退一步找包含任一关键词的。
 * 打分：每个关键词出现次数（单个最多计 5 次），出现在标题里另加 3 分。
 */
export function search(m: Material, query: string, opts: SearchOptions = {}): string {
  const terms = [...new Set(query.toLowerCase().split(/\s+/).filter(Boolean))]
  if (terms.length === 0) throw new Error('关键词不能为空')
  const bad = (opts.kinds ?? []).filter((k) => !(DOC_KINDS as readonly string[]).includes(k))
  if (bad.length) throw new Error(`kinds 只能取 ${DOC_KINDS.join('、')}，不认识：${bad.join('、')}`)
  const inScope = scopeFilter(m, opts.scope)
  const kinds = opts.kinds?.length ? new Set(opts.kinds) : undefined
  const pool = corpus(m).filter((d) => inScope(d) && (!kinds || kinds.has(d.kind)))
  const rank = (needAll: boolean) => pool.flatMap((d) => {
    const counts = terms.map((t) => count(d.hay, t))
    if (needAll ? counts.includes(0) : counts.every((c) => c === 0)) return []
    const title = d.title.toLowerCase()
    return [{ d, score: counts.reduce((a, c) => a + c, 0) + terms.filter((t) => title.includes(t)).length * 3 }]
  }).sort((a, b) => b.score - a.score)
  let hits = rank(true)
  const partial = hits.length === 0 && terms.length > 1
  if (partial) hits = rank(false)
  if (hits.length === 0) return `没有找到「${query}」。换个说法、少用几个关键词，或用 textbook_outline 看目录。`
  const limit = Math.min(Math.max(1, opts.limit ?? SEARCH_LIMIT), SEARCH_MAX)
  const head = `${partial ? '没有同时包含全部关键词的结果，下面是包含部分关键词的。' : ''}共 ${hits.length} 处，按相关度列出前 ${Math.min(limit, hits.length)} 处（用 textbook_read 读方括号里的引用）：`
  return [head, ...hits.slice(0, limit).map(({ d }, i) => {
    const it = d.kind === '讲义' || d.kind === '速记' ? undefined : m.item(d.ref)
    const page = it && (d.kind === '答案' ? it.pages.answer?.[0] : firstPage(it))
    return `${i + 1}. [${d.ref}] ${d.kind} · ${d.title}${it ? pageNote(it.book, page) : ''}\n   ${snippet(d, terms)}`
  })].join('\n')
}

/**
 * 按引用读原文。
 * @param seenUnits - 对话里仍然可见的单元（`分册/单元`）；读整个单元时不重复给全文。
 */
export function read(m: Material, token: string, seenUnits: ReadonlySet<string> = new Set()): string {
  const ref: Ref | undefined = m.resolve(token.trim().replace(/^@/, ''))
  if (!ref) throw new Error(`找不到「${token}」。${REF_HELP}。不确定时先用 textbook_search 或 textbook_outline。`)
  switch (ref.kind) {
    case 'item': {
      const it = m.item(ref.id)!
      const where = [it.pages.problem?.[0] && `题目在 ${it.book} 第 ${it.pages.problem[0]} 页`, it.pages.answer?.[0] && `答案在第 ${it.pages.answer[0]} 页`, it.pages.lesson?.[0] && `在 ${it.book} 第 ${it.pages.lesson[0]} 页`]
        .filter(Boolean).join('，')
      return `${m.itemBlock(ref.id)}${where ? `\n\n（${where}）` : ''}`
    }
    case 'page': {
      const items = m.pageItems(ref.book, ref.page)
      const list = items.length ? `\n\n本页条目：${items.map((it) => `${it.id}（${it.label}）`).join('、')}` : ''
      return `${m.pageBlock(ref.book, ref.page)}${list}`
    }
    case 'unit':
      if (seenUnits.has(`${ref.book}/${ref.unit}`)) return `${ref.unit} 的讲义全文、题目说明和速记表已经在对话里的教材材料中，直接用即可。`
      return m.unitBlock(ref.book, ref.unit)
    case 'section': {
      const u = m.unit(ref.book, ref.unit)!
      if (ref.section === CHEATSHEET) return `# ${u.title} › 速记表\n\n${u.cheatsheet}`
      const s = m.sections(ref.book, ref.unit).find((x) => x.key === ref.section)!
      return `# ${u.title} › ${s.title}\n\n${s.text}`
    }
  }
}

/**
 * 教材数据：从 indexer 生成的 index.json 里按题号、页码、单元、小节精确取出原文，并把学生的 `@` 引用拼成材料。
 *
 * 拼出的材料按「越稳定越靠前」排：单元讲义全文 → 题目说明与速记表 → 本页文字 → 条目（题目、官方答案、验算记录、前置题）。
 * 同一单元的不同提问因此共享前缀，能命中 DeepSeek 的上下文缓存。
 */
import { readFile, stat } from 'node:fs/promises'
import { pageRef, REF_TOKEN, refTokens } from './refs.ts'

export { refTokens } from './refs.ts'

export type ItemKind = 'problem' | 'example' | 'practice'

export interface Item {
  kind: ItemKind
  book: string
  unit: string
  label: string
  md: string
  answer?: string
  verify?: string[]
  section?: string
  pages: { problem?: number[]; answer?: number[]; lesson?: number[] }
}

export interface Unit {
  title: string
  lesson: string
  problems_head: string
  cheatsheet: string
}

export interface Book {
  title: string
  pdf: string
  pages: number
  units: string[]
  page_items: Record<string, string[]>
  page_text: string[]
}

export interface Index {
  books: Record<string, Book>
  items: Record<string, Item>
  units: Record<string, Unit>
}

/**
 * 一处教材引用，解析后的结果。写法：
 * 题号 `L8-05`、例题 `Z1·例01`、页码 `L/140`、单元 `L8`、小节 `L8§3`（`L8§0` 是开篇，`L8§小结`、`L8§速记`）。
 */
export type Ref =
  | { kind: 'item'; id: string; book: string; unit: string }
  | { kind: 'page'; book: string; page: number; unit?: string }
  | { kind: 'unit'; book: string; unit: string }
  | { kind: 'section'; book: string; unit: string; section: string }

/** 讲义按 `### ` 标题切开的一节。key 是小节编号；标题前的开篇是 `0`，「本章小结」是 `小结`。 */
export interface Section { key: string; title: string; text: string }

/** 速记表在小节引用里的名字。 */
export const CHEATSHEET = '速记'

export interface BookSummary { id: string; title: string; pages: number }
export interface ItemSummary { id: string; kind: ItemKind; label: string }

/** 浏览器端一次取走的目录：教材面板按页列条目，`@` 补全按题号、单元名搜。单元的 page 是它最靠前的条目所在页。 */
export interface Catalog {
  books: (BookSummary & { units: { id: string; title: string; page?: number }[]; pageItems: Record<string, string[]> })[]
  items: Record<string, { book: string; unit: string; kind: ItemKind; label: string; page?: number; hint?: string }>
}

/** 一次取材的结果：给模型的正文，以及这次新附上的单元、条目（用于去重）。 */
export interface Bundle {
  text: string
  units: string[]
  items: string[]
  summary: string
}

const PREREQ = /先做\s*([^）)\n]+)/
const PREREQ_ID = /[A-Z]{1,4}\d{0,2}[A-Z]?-\d{2}/g
const VERIFY_LINES = 20
const SUMMARY_MAX = 120

/** 把讲义切成小节。 */
export function splitSections(lesson: string): Section[] {
  return lesson.split(/^(?=### )/m).flatMap((part, i): Section[] => {
    if (!part.startsWith('### ')) return part.trim() ? [{ key: '0', title: '开篇', text: part.trim() }] : []
    const title = part.slice(4, part.indexOf('\n') < 0 ? undefined : part.indexOf('\n')).trim()
    const num = /^(\d+)[.．、]/.exec(title)
    const key = num ? num[1]! : title.includes('小结') ? '小结' : String(i)
    return [{ key, title, text: part.trim() }]
  })
}

export function prereqIds(md: string): string[] {
  const m = PREREQ.exec(md)
  return m ? (m[1]!.match(PREREQ_ID) ?? []) : []
}

/** 例题的 label 形如「例 5 · 」，去掉尾巴上的分隔符。 */
export function displayLabel(item: Item): string {
  return item.label.replace(/\s*·\s*$/, '')
}

const HINT_CHARS = 36

/** 题干开头一小段：例题的 label 只有「例 3」，目录和补全菜单靠它看出讲什么。 */
export function stemHint(item: Item): string {
  const stem = item.md.replace(/^\*\*[^*]*\*\*[\s\u3000]*/, '').replace(/\s+/g, ' ').trim()
  return stem.length > HINT_CHARS ? `${stem.slice(0, HINT_CHARS)}…` : stem
}

const TITLE_CHARS = 20

/**
 * 会话标题：消息里第一处有效教材引用的简短说法；没有引用时取第一个像样的分句（至少 4 个字），最长 20 字。
 * @returns 消息里既没有有效引用也没有文字时为 undefined。
 */
export function titleFor(m: Material, text: string): string | undefined {
  for (const token of refTokens(text)) {
    const title = m.titleOf(token)
    if (title) return title
  }
  const plain = text.replace(REF_TOKEN, '').replace(/\s+/g, ' ').trim()
  // 英文标点后面跟空格或在句末才算断句，免得把 [[2,1],[1,2]]、f(x)=x^2, x∈[0,1] 这类式子从中间截断
  const clause = plain.split(/[，。？！；：]|[,?!;:](?=\s|$)/).map((s) => s.trim()).find((s) => s.length >= 4) ?? plain
  if (!clause) return undefined
  return clause.length > TITLE_CHARS ? `${clause.slice(0, TITLE_CHARS)}…` : clause
}

export class Material {
  private readonly index: Index
  readonly bookIds: readonly string[]
  /** 索引文件路径；索引里记录的 PDF 若是相对路径，按它所在目录解析。 */
  readonly indexPath: string
  /** 单元号 → 所在分册（白名单内单元号唯一）。 */
  private readonly unitBook = new Map<string, string>()
  private readonly sectionCache = new Map<string, Section[]>()

  /**
   * @param index - indexer 生成的完整索引（可能含多个版本的分册）。
   * @param books - 允许使用的分册白名单，按显示顺序；为空时用索引里的全部分册。
   * @param indexPath - 索引文件路径。
   */
  constructor(index: Index, books: readonly string[], indexPath = '') {
    this.index = index
    this.bookIds = books.length ? books.filter((b) => index.books[b] !== undefined) : Object.keys(index.books)
    this.indexPath = indexPath
    for (const b of this.bookIds) for (const u of index.books[b]!.units) this.unitBook.set(u, b)
  }

  books(): BookSummary[] {
    return this.bookIds.map((id) => ({ id, title: this.index.books[id]!.title, pages: this.index.books[id]!.pages }))
  }

  catalog(): Catalog {
    const items: Catalog['items'] = {}
    for (const [id, it] of this.items()) {
      const page = it.pages.problem?.[0] ?? it.pages.lesson?.[0]
      items[id] = {
        book: it.book, unit: it.unit, kind: it.kind, label: displayLabel(it),
        ...(page === undefined ? {} : { page }), ...(it.kind === 'example' ? { hint: stemHint(it) } : {}),
      }
    }
    const books = this.books().map((b) => {
      const pageItems: Record<string, string[]> = {}
      for (const page of Object.keys(this.index.books[b.id]!.page_items)) {
        const ids = this.pageItems(b.id, Number(page)).map((it) => it.id)
        if (ids.length) pageItems[page] = ids
      }
      const units = this.index.books[b.id]!.units.map((u) => {
        const pages = Object.values(items).filter((it) => it.book === b.id && it.unit === u && it.page !== undefined).map((it) => it.page!)
        return { id: u, title: this.unit(b.id, u)?.title ?? u, ...(pages.length ? { page: Math.min(...pages) } : {}) }
      })
      return { ...b, units, pageItems }
    })
    return { books, items }
  }

  book(id: string): Book | undefined {
    return this.bookIds.includes(id) ? this.index.books[id] : undefined
  }

  /** 题号只在白名单分册里有效；不同版本的分册可能共用题号，以条目自己记录的分册为准。 */
  item(id: string): Item | undefined {
    const it = this.index.items[id]
    return it !== undefined && this.bookIds.includes(it.book) ? it : undefined
  }

  /** 白名单分册里的全部条目。 */
  items(): [string, Item][] {
    return Object.entries(this.index.items).filter(([, it]) => this.bookIds.includes(it.book))
  }

  unitBookOf(unit: string): string | undefined {
    return this.unitBook.get(unit)
  }

  /** 单元号，或「分册/单元」写法（分册号和单元号相同时用来点明是单元，如 C1/C1）。 */
  unitOf(token: string): { book: string; unit: string } | undefined {
    const slash = token.indexOf('/')
    const unit = slash < 0 ? token : token.slice(slash + 1)
    const book = this.unitBook.get(unit)
    return book && (slash < 0 || token.slice(0, slash) === book) ? { book, unit } : undefined
  }

  unit(book: string, unit: string): Unit | undefined {
    return this.unitBook.get(unit) === book ? this.index.units[`${book}/${unit}`] : undefined
  }

  sections(book: string, unit: string): Section[] {
    const key = `${book}/${unit}`
    let s = this.sectionCache.get(key)
    if (!s) {
      s = splitSections(this.unit(book, unit)?.lesson ?? '')
      this.sectionCache.set(key, s)
    }
    return s
  }

  pageItems(book: string, page: number): ItemSummary[] {
    const ids = this.book(book)?.page_items[String(page)] ?? []
    return ids.flatMap((id) => {
      const it = this.item(id)
      return it?.book === book ? [{ id, kind: it.kind, label: displayLabel(it) }] : []
    })
  }

  /** 页上第一个条目所属单元；页上没有条目时向前找最近的条目。 */
  unitOfPage(book: string, page: number): string | undefined {
    for (let p = page; p > 0; p--) {
      const first = this.pageItems(book, p)[0]
      if (first) return this.item(first.id)!.unit
    }
    return undefined
  }

  resolve(token: string): Ref | undefined {
    const mark = token.indexOf('§')
    if (mark >= 0) {
      const unit = token.slice(0, mark)
      const section = token.slice(mark + 1)
      const book = this.unitBook.get(unit)
      if (!book) return undefined
      if (section !== CHEATSHEET && !this.sections(book, unit).some((s) => s.key === section)) return undefined
      return { kind: 'section', book, unit, section }
    }
    const u = this.unitOf(token)
    if (u) return { kind: 'unit', ...u }
    const pr = pageRef(token)
    if (pr) {
      const b = this.book(pr.book)
      if (!b || pr.page < 1 || pr.page > b.pages) return undefined
      return { kind: 'page', book: pr.book, page: pr.page, unit: this.unitOfPage(pr.book, pr.page) }
    }
    const it = this.item(token)
    return it ? { kind: 'item', id: token, book: it.book, unit: it.unit } : undefined
  }

  /**
   * 一处引用的简短说法，用作会话标题：题目用考查点，例题和没写考查点的题目用所在单元名（题干里的公式不进标题），
   * 页码和单元用单元名，小节用小节标题。
   * @returns 引用无效时为 undefined。
   */
  titleOf(token: string): string | undefined {
    const ref = this.resolve(token)
    if (!ref) return undefined
    const unitName = (unit: string | undefined) => {
      const title = unit ? this.unit(ref.book, unit)?.title : undefined
      return title?.replace(/^[^·]*·\s*/, '') ?? ''
    }
    switch (ref.kind) {
      case 'item': {
        const focus = /考查：([^〕]+)/.exec(this.item(ref.id)!.label)?.[1]?.trim()
        return `${ref.id} ${focus ?? unitName(ref.unit)}`.trim()
      }
      case 'page':
        return `${ref.book} 第 ${ref.page} 页 ${unitName(ref.unit)}`.trim()
      case 'unit':
        return this.unit(ref.book, ref.unit)?.title ?? ref.unit
      case 'section': {
        const sec = this.sections(ref.book, ref.unit).find((x) => x.key === ref.section)
        return `${ref.unit}§${ref.section} ${sec?.title.replace(/^\d+[.．、]\s*/, '') ?? unitName(ref.unit)}`.trim()
      }
    }
  }

  unitBlock(book: string, unit: string): string {
    const u = this.unit(book, unit)
    const title = this.index.books[book]?.title ?? ''
    if (!u) return ''
    return [
      `# 分册 ${book} · ${title}；单元 ${u.title || unit}`,
      `## 本单元讲义全文\n\n${u.lesson}`,
      `## 本单元题目说明（方法编号）\n\n${u.problems_head}`,
      `## 本单元速记表\n\n${u.cheatsheet}`,
    ].join('\n\n')
  }

  itemBlock(id: string): string {
    const it = this.item(id)
    if (!it) return ''
    if (it.kind !== 'problem') {
      const kind = it.kind === 'example' ? '讲义例题' : '讲义随堂练习'
      return `## ${kind} ${id}（讲义小节：${it.section ?? ''}）\n\n${it.md}`
    }
    const out = [
      `## 题目 ${id}\n\n${it.md}`,
      `## ${id} 的官方答案（已用代码验算，数值以此为准）\n\n${it.answer || '（无）'}`,
    ]
    if (it.verify?.length) out.push(`## ${id} 的代码验算记录\n\n${it.verify.slice(0, VERIFY_LINES).join('\n')}`)
    for (const pid of prereqIds(it.md)) {
      const p = this.item(pid)
      if (p) out.push(`## 前置题 ${pid}（${id} 注明「先做」）\n\n${p.md}\n\n官方答案：\n\n${p.answer ?? '（无）'}`)
    }
    return out.join('\n\n')
  }

  pageBlock(book: string, page: number): string {
    const txt = this.book(book)?.page_text[page - 1] ?? ''
    return `## 分册 ${book} 第 ${page} 页（PDF 抽出的文字，公式排版可能有损，以讲义原文为准）\n\n${txt}`
  }

  /**
   * 把一批引用拼成一条材料消息。
   * @param refs - 本轮新出现的引用，按出现顺序。
   * @param seen - 对话里仍然可见的单元（`分册/单元`）和条目，不再重复附上。
   * @returns 材料；没有需要新附上的内容时返回 undefined。
   */
  bundle(refs: readonly Ref[], seen: { units: ReadonlySet<string>; items: ReadonlySet<string> }): Bundle | undefined {
    const units: string[] = []
    const items: string[] = []
    const pages: { book: string; page: number }[] = []
    const addUnit = (book: string, unit: string | undefined): void => {
      const key = unit && `${book}/${unit}`
      if (key && !seen.units.has(key) && !units.includes(key) && this.unit(book, unit!)) units.push(key)
    }
    const addItem = (id: string): void => {
      if (!seen.items.has(id) && !items.includes(id)) items.push(id)
    }
    for (const ref of refs) {
      addUnit(ref.book, ref.unit)
      if (ref.kind === 'item') addItem(ref.id)
      else if (ref.kind === 'page' && !pages.some((p) => p.book === ref.book && p.page === ref.page)) {
        pages.push({ book: ref.book, page: ref.page })
        for (const it of this.pageItems(ref.book, ref.page)) addItem(it.id)
      }
    }
    if (units.length === 0 && items.length === 0 && pages.length === 0) return undefined
    const text = [
      ...units.map((key) => { const [b, u] = key.split('/') as [string, string]; return this.unitBlock(b, u) }),
      ...pages.map((p) => this.pageBlock(p.book, p.page)),
      ...items.map((id) => this.itemBlock(id)),
    ].join('\n\n')
    return { text, units, items, summary: summarize(units, pages, items) }
  }
}

function summarize(units: string[], pages: { book: string; page: number }[], items: string[]): string {
  const parts = [
    ...units.map((key) => `${key.split('/')[1]} 讲义`),
    ...pages.map((p) => `${p.book} 第 ${p.page} 页`),
    ...items,
  ]
  const s = `附上教材：${parts.join('、')}`
  return s.length <= SUMMARY_MAX ? s : `${s.slice(0, SUMMARY_MAX - 1)}…`
}

/** 按文件修改时间缓存的索引加载器；indexer 重新生成后下一次读取自动换新。 */
export function materialLoader(indexPath: string, books: readonly string[]): () => Promise<Material> {
  let cached: { mtimeMs: number; material: Promise<Material> } | undefined
  return async () => {
    const { mtimeMs } = await stat(indexPath)
    if (cached?.mtimeMs !== mtimeMs) {
      const material = readFile(indexPath, 'utf8').then((t) => new Material(JSON.parse(t) as Index, books, indexPath))
      cached = { mtimeMs, material }
      material.catch(() => { if (cached?.material === material) cached = undefined })
    }
    return cached.material
  }
}

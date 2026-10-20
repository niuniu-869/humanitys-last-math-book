/**
 * `@` 引用在浏览器端的三处：
 * - 补全源「教材」：输入 @ 后按题号、单元名、考查点、例题题干搜，或输入 L/14 列页码。
 * - 用户气泡里的 `@L8-05` 渲染成芯片，点了右侧教材面板翻到那一页。
 * - 草稿里手打的 `@L8-05` 也按词表高亮（lexicon）。
 * 发出去的消息里仍是 `@L8-05` 原文，服务端按同一套写法（refs.ts）取材。
 */
import { REF_TOKEN } from '../refs.ts'
import { type BookTarget, type Catalog, catalogNow, describeRef, loadCatalog, subscribeCatalog, useCatalog } from './catalog.ts'
import type { TriggerCandidate, TriggerSource, UserTextNodeProps, UserTextRule } from './host.ts'
import { Icon } from './icons.tsx'
import css from './ToolRow.module.css'

export const SOURCE = '教材'
export const RULE_ID = 'hlmb-ref'
const LIMIT = 40
const PAGE_LIMIT = 12

export interface RefData { readonly ref: string }

/** 用户气泡里的引用。只按写法切，不查目录（规则的结果会被缓存，目录晚到时不会重算）；认不认得交给芯片。 */
export const refRule: UserTextRule<typeof RULE_ID, RefData> = {
  id: RULE_ID,
  // dsh 的 @文件 规则是 30；同一位置两条规则都能匹配时，教材引用优先
  order: 20,
  match(text, from) {
    const re = new RegExp(REF_TOKEN.source, 'g')
    re.lastIndex = from
    const m = re.exec(text)
    return m ? { id: RULE_ID, start: m.index, end: m.index + m[0].length, data: { ref: m[1]! } } : undefined
  },
}

export function createRefChip(open: (t: BookTarget) => void) {
  return function RefChip({ node, raw, interactive }: UserTextNodeProps<RefData>) {
    const { catalog } = useCatalog()
    const view = describeRef(catalog, node.data.ref)
    // 目录里没有的引用（题号写错、目录还没到）照原文显示
    if (!view) return <span title={catalog ? '教材里没有这一处' : undefined}>{raw}</span>
    const target = view.target
    const body = <><Icon name="book" size={13} className={css.refIcon} />{view.label}</>
    return interactive && target
      ? <button type="button" className={css.refChip} title={view.detail} onClick={() => open(target)}>{body}</button>
      : <span className={css.refChip} title={view.detail}>{body}</span>
  }
}

const norm = (s: string): string => s.toLowerCase().replace(/\s+/g, '')

/** 输入 `L/14` 时列出这本书里页码以 14 开头的页。 */
function pageCandidates(c: Catalog, bookId: string, digits: string): TriggerCandidate[] {
  const b = c.books.find((x) => x.id.toLowerCase() === bookId.toLowerCase())
  if (!b) return []
  const out: TriggerCandidate[] = []
  for (let p = 1; p <= b.pages && out.length < PAGE_LIMIT; p++) {
    if (digits && !String(p).startsWith(digits)) continue
    const ids = b.pageItems[String(p)] ?? []
    out.push({
      name: `${b.id}/${p}`, label: `${b.id} 第 ${p} 页`, section: b.title, icon: 'file',
      ...(ids.length ? { description: ids.slice(0, 4).join('、') + (ids.length > 4 ? ' 等' : '') } : {}),
    })
  }
  return out
}

/**
 * 补全候选：题号、单元号前缀最优先，其次单元名、考查点、例题题干里含有输入的文字。
 * 输入为空时列出全部单元。
 */
export function candidates(c: Catalog, query: string): TriggerCandidate[] {
  const page = /^([A-Za-z0-9-]+)\/(\d*)$/.exec(query.trim())
  if (page) return pageCandidates(c, page[1]!, page[2]!)
  const q = norm(query)
  const scored: { score: number; order: number; cand: TriggerCandidate }[] = []
  let order = 0
  for (const b of c.books) {
    for (const u of b.units) {
      const score = !q ? 1 : norm(u.id).startsWith(q) ? 4 : norm(u.title).includes(q) ? 2 : 0
      if (score) scored.push({ score, order: order++, cand: { name: u.id, label: u.title, section: b.title, icon: 'folder', description: `${b.id}，第 ${u.page ?? '?'} 页起` } })
    }
  }
  if (q) {
    for (const [id, it] of Object.entries(c.items)) {
      const text = it.hint ? `${it.label}${it.hint}` : it.label
      const score = norm(id).startsWith(q) ? 3 : norm(text).includes(q) ? 1 : 0
      if (!score) continue
      const book = c.books.find((b) => b.id === it.book)
      const label = it.kind === 'example' ? `${id} ${it.label}` : id
      const detail = it.kind === 'example' ? it.hint : it.label.replace(/^\S+?〔/, '〔')
      scored.push({
        score, order: order++,
        cand: { name: id, label, section: book?.title ?? it.book, icon: 'file', ...(detail ? { description: detail } : {}), ...(it.page ? { hint: `第 ${it.page} 页` } : {}) },
      })
    }
  }
  return scored.sort((a, b) => b.score - a.score || a.order - b.order).slice(0, LIMIT).map((s) => s.cand)
}

/** 词表：草稿里手打的引用按它高亮。 */
function lexicon(c: Catalog): string[] {
  return [...c.books.flatMap((b) => [...b.units.map((u) => u.id), ...Array.from({ length: b.pages }, (_, i) => `${b.id}/${i + 1}`)]), ...Object.keys(c.items)]
}

export function createRefSource(open: (t: BookTarget) => void): TriggerSource {
  let words: { catalog: Catalog; list: string[] } | undefined
  return {
    trigger: '@',
    name: SOURCE,
    showGroupTitle: false,
    async candidates(_session, { query, signal }) {
      const c = await loadCatalog()
      signal.throwIfAborted()
      return candidates(c, query)
    },
    onPick({ candidate }) {
      const ref = `@${candidate.name}`
      const view = describeRef(catalogNow(), candidate.name)
      return { insert: { source: SOURCE, ref, label: view?.label ?? candidate.name, appearance: view?.kind === 'unit' ? 'folder' : 'file', clipboardText: ref } }
    },
    warm() {
      loadCatalog().catch(() => undefined)
    },
    lexicon() {
      const c = catalogNow()
      if (!c) return undefined
      if (words?.catalog !== c) words = { catalog: c, list: lexicon(c) }
      return words.list
    },
    subscribeLexicon(_session, listener) {
      return subscribeCatalog(listener)
    },
    openReference(_session, { ref }) {
      const target = describeRef(catalogNow(), ref.replace(/^@/, ''))?.target
      if (target) open(target)
      return target !== undefined
    },
    codec: {
      clipboardText: (ref) => ref,
      serialize: (ref) => Promise.resolve(ref),
    },
  }
}

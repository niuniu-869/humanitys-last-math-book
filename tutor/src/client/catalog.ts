/**
 * 教材目录：整个页面只取一次 `/api/hlmb/catalog`，教材面板、`@` 补全、引用芯片共用。
 * 取失败不缓存，下次用到时重取。
 */
import { useEffect, useSyncExternalStore } from 'react'
import type { Catalog } from '../material.ts'
import { pageRef } from '../refs.ts'

export type { Catalog }
export type CatalogBook = Catalog['books'][number]

/** 插件路由的地址；dsh 可能挂在子路径下，按页面 base 解析。 */
export const api = (path: string): string => new URL(`api/hlmb/${path}`, document.baseURI).href

interface State { readonly catalog?: Catalog; readonly error?: string }

let state: State = {}
let pending: Promise<Catalog> | undefined
const listeners = new Set<() => void>()

function publish(next: State): void {
  state = next
  for (const l of listeners) l()
}

export function subscribeCatalog(listener: () => void): () => void {
  listeners.add(listener)
  return () => listeners.delete(listener)
}

export const catalogNow = (): Catalog | undefined => state.catalog

export function loadCatalog(): Promise<Catalog> {
  pending ??= fetch(api('catalog'))
    .then(async (r) => {
      if (!r.ok) throw new Error((await r.text()) || `HTTP ${r.status}`)
      return (await r.json()) as Catalog
    })
    .then((catalog) => {
      publish({ catalog })
      return catalog
    }, (err: unknown) => {
      pending = undefined
      publish({ error: err instanceof Error ? err.message : String(err) })
      throw err
    })
  return pending
}

/** 订阅目录；第一次用到时触发加载。 */
export function useCatalog(): State {
  const s = useSyncExternalStore(subscribeCatalog, () => state)
  useEffect(() => {
    if (!state.catalog) loadCatalog().catch(() => undefined)
  }, [])
  return s
}

/** 教材里的一个位置：面板翻到这本书的这一页。 */
export interface BookTarget { readonly book: string; readonly page: number }

/** 一处引用在界面上怎么显示、点了翻到哪里。 */
export interface RefView {
  /** 芯片上的短名。 */
  readonly label: string
  /** 悬停提示和补全菜单的说明。 */
  readonly detail: string
  readonly kind: 'item' | 'page' | 'unit'
  readonly target?: BookTarget
}

const bookOf = (c: Catalog, id: string): CatalogBook | undefined => c.books.find((b) => b.id === id)

/** 单元号或「分册/单元」写法，规则与服务端 Material.unitOf 一致。 */
function unitOf(c: Catalog, token: string): { book: CatalogBook; unit: CatalogBook['units'][number] } | undefined {
  const slash = token.indexOf('/')
  const id = slash < 0 ? token : token.slice(slash + 1)
  for (const book of c.books) {
    const unit = book.units.find((u) => u.id === id)
    if (unit && (slash < 0 || token.slice(0, slash) === book.id)) return { book, unit }
  }
  return undefined
}

/**
 * 解析学生写的引用（不含 @）。解析顺序与服务端 Material.resolve 一致：单元 → 页码 → 条目。
 * @returns 目录还没取到或教材里没有时为 undefined。
 */
export function describeRef(c: Catalog | undefined, token: string): RefView | undefined {
  if (!c) return undefined
  const u = unitOf(c, token)
  if (u) {
    return {
      label: token, detail: `${u.unit.title}（${u.book.title}）`, kind: 'unit',
      ...(u.unit.page === undefined ? {} : { target: { book: u.book.id, page: u.unit.page } }),
    }
  }
  const pr = pageRef(token)
  if (pr) {
    const b = bookOf(c, pr.book)
    if (!b || pr.page < 1 || pr.page > b.pages) return undefined
    return { label: `${pr.book} 第 ${pr.page} 页`, detail: `《${b.title}》第 ${pr.page} 页`, kind: 'page', target: pr }
  }
  const it = c.items[token]
  if (!it) return undefined
  const b = bookOf(c, it.book)
  const where = it.page === undefined ? '' : `，第 ${it.page} 页`
  return {
    label: token, detail: `${it.hint ? `${it.label}：${it.hint}` : it.label}（${b?.title ?? it.book}${where}）`, kind: 'item',
    ...(it.page === undefined ? {} : { target: { book: it.book, page: it.page } }),
  }
}

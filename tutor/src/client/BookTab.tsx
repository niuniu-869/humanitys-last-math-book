/**
 * 右侧「教材」面板。
 * - 书页连续滚动，只渲染看得见的几页（按容器宽度 × 设备像素比渲染，字是清楚的）。
 * - 顶栏按单元跳转、按页码翻页；底栏列出当前页的题目，点一下把 `@题号` 放进输入框，「问这一页」放 `@分册/页码`。
 * - 对话里点引用芯片、工具行里的页码，会带着 {book, page} 打开或翻动这个面板。
 * - 记住每本书看到哪一页（只存在本机浏览器）。
 */
import { type KeyboardEvent, useEffect, useMemo, useRef, useState } from 'react'
import type { PDFDocumentProxy, RenderTask } from 'pdfjs-dist'
import css from './BookTab.module.css'
import { type BookTarget, type Catalog, type CatalogBook, loadCatalog, useCatalog } from './catalog.ts'
import type { InputActions, SidebarRight, TabInfo } from './host.ts'
import { Icon } from './icons.tsx'
import { loadBook } from './pdf.ts'

const STORE = 'hlmb-tutor:book'
const GAP = 12
const SIDE = 12
const OVERSCAN = 1
const MAX_DPR = 2
const WIDTH_STEP = 8
const TOAST_MS = 1800

interface Saved { book?: string; pages?: Record<string, number> }

function readSaved(): Saved {
  try {
    return JSON.parse(localStorage.getItem(STORE) ?? '{}') as Saved
  } catch {
    return {}
  }
}

function writeSaved(book: string, page: number): void {
  try {
    const s = readSaved()
    localStorage.setItem(STORE, JSON.stringify({ book, pages: { ...s.pages, [book]: page } }))
  } catch {
    // 无痕模式等场景存不了，下次从第一页开始即可
  }
}

const isTarget = (v: unknown): v is BookTarget =>
  typeof v === 'object' && v !== null && typeof (v as BookTarget).book === 'string' && Number.isInteger((v as BookTarget).page)

const clampPage = (b: CatalogBook, p: number): number => Math.min(Math.max(1, p), b.pages)

/**
 * 当前页所在单元：本页（没有条目时往前找最近一页）最后一个条目的单元。
 * 书后的题目区每页都有题号，按讲义起始页推算会错成最后一个单元。第一个条目之前是封面和目录。
 */
function unitAt(c: Catalog, b: CatalogBook, page: number): string {
  for (let p = page; p > 0; p--) {
    const ids = b.pageItems[String(p)]
    const last = ids?.[ids.length - 1]
    if (last) return c.items[last]?.unit ?? ''
  }
  return ''
}

/** 底栏芯片上的字：题号；例题用「例 3」。 */
function chipText(c: Catalog, id: string): string {
  const it = c.items[id]
  return it?.kind === 'example' ? it.label : id
}

export function createBookTab(sidebar: SidebarRight) {
  return function BookTab({ useTabInfo, inputActions }: { useTabInfo: () => TabInfo; inputActions?: InputActions }) {
    const info = useTabInfo()
    const { catalog, error } = useCatalog()
    const nav = info.tab.navigation
    const [book, setBook] = useState<string | undefined>(() => (isTarget(nav.params) ? nav.params.book : readSaved().book))
    const [page, setPage] = useState(() => (isTarget(nav.params) ? nav.params.page : (book && readSaved().pages?.[book]) || 1))
    const [jump, setJump] = useState({ page, seq: 0 })
    const [toast, setToast] = useState<string>()

    const go = (b: string, p: number) => {
      setBook(b)
      setPage(p)
      setJump((j) => ({ page: p, seq: j.seq + 1 }))
    }

    // 再次被打开（点了另一个引用）：翻到新位置
    useEffect(() => {
      if (isTarget(nav.params)) go(nav.params.book, nav.params.page)
    }, [nav.revision])

    const current = catalog?.books.find((b) => b.id === book) ?? catalog?.books[0]
    useEffect(() => {
      if (current) writeSaved(current.id, page)
    }, [current?.id, page])

    useEffect(() => {
      if (!toast) return
      const t = setTimeout(() => setToast(undefined), TOAST_MS)
      return () => clearTimeout(t)
    }, [toast])

    if (!catalog) {
      return (
        <div className={css.root}>
          <div className={css.notice}>
            {error ? <>教材目录没有取到：{error}<br /><button type="button" className={css.textButton} onClick={() => void loadCatalog().catch(() => undefined)}>重试</button></> : '正在打开教材…'}
          </div>
        </div>
      )
    }
    if (!current) return <div className={css.root}><div className={css.notice}>还没有配置教材。</div></div>

    const insert = (ref: string) => {
      if (!inputActions) return
      const ok = inputActions.insertText(` @${ref} `, inputActions.captureInsertion())
      setToast(ok ? `已放进输入框：@${ref}` : '正在发送，稍后再试')
      // 手机上面板是全屏的，放好引用后收起，让学生直接接着打字
      if (ok && info.sidebar.fullscreen && sidebar.isExpanded()) sidebar.toggleExpanded()
    }

    const shown = clampPage(current, page)
    const items = current.pageItems[String(shown)] ?? []
    return (
      <div className={css.root} data-hlmb-book={current.id}>
        <Toolbar catalog={catalog} book={current} page={shown} go={go} />
        <Pages key={current.id} book={current} jump={jump} onPage={setPage} />
        <div className={css.tray}>
          {toast
            ? <span className={css.toast} role="status">{toast}</span>
            : items.length
              ? (
                <div className={css.chips}>
                  {items.map((id) => (
                    <button key={id} type="button" className={css.chip} title={`问 ${catalog.items[id]?.label ?? id}`} onClick={() => insert(id)}>
                      {chipText(catalog, id)}
                    </button>
                  ))}
                </div>
              )
              : <span className={css.empty}>这一页没有编号的题</span>}
          {inputActions && (
            <button type="button" className={css.ask} onClick={() => insert(`${current.id}/${shown}`)}>
              <Icon name="ask" size={13} />问这一页
            </button>
          )}
        </div>
      </div>
    )
  }
}

function Toolbar({ catalog, book, page, go }: { catalog: Catalog; book: CatalogBook; page: number; go: (b: string, p: number) => void }) {
  const [draft, setDraft] = useState<string>()
  const commit = () => {
    const n = Number(draft)
    if (draft !== undefined && Number.isInteger(n)) go(book.id, clampPage(book, n))
    setDraft(undefined)
  }
  const onKey = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') commit()
    if (e.key === 'Escape') setDraft(undefined)
  }
  return (
    <div className={css.bar}>
      <select className={css.select} aria-label="跳到单元" value={`${book.id}|${unitAt(catalog, book, page)}`}
        onChange={(e) => {
          const [b, u] = e.target.value.split('|')
          const target = catalog.books.find((x) => x.id === b)
          if (target) go(target.id, target.units.find((x) => x.id === u)?.page ?? 1)
        }}>
        {catalog.books.map((b) => (
          <optgroup key={b.id} label={`${b.id}《${b.title}》`}>
            <option value={`${b.id}|`}>{b.title} · 封面与目录</option>
            {b.units.map((u) => <option key={u.id} value={`${b.id}|${u.id}`} disabled={u.page === undefined}>{u.title}</option>)}
          </optgroup>
        ))}
      </select>
      <div className={css.pager}>
        <button type="button" className={css.iconButton} aria-label="上一页" disabled={page <= 1} onClick={() => go(book.id, page - 1)}>
          <Icon name="left" />
        </button>
        <input className={css.pageInput} aria-label="页码" inputMode="numeric" value={draft ?? String(page)}
          onChange={(e) => setDraft(e.target.value.replace(/\D/g, ''))} onKeyDown={onKey} onBlur={commit} />
        <span>/ {book.pages}</span>
        <button type="button" className={css.iconButton} aria-label="下一页" disabled={page >= book.pages} onClick={() => go(book.id, page + 1)}>
          <Icon name="right" />
        </button>
      </div>
    </div>
  )
}

/** 连续滚动的书页。只挂载视口附近的几页；尺寸变化时保持当前页不跑。 */
function Pages({ book, jump, onPage }: { book: CatalogBook; jump: { page: number; seq: number }; onPage: (p: number) => void }) {
  const scroller = useRef<HTMLDivElement>(null)
  const [doc, setDoc] = useState<PDFDocumentProxy>()
  const [ratio, setRatio] = useState<number>()
  const [failed, setFailed] = useState<string>()
  const [attempt, setAttempt] = useState(0)
  const [box, setBox] = useState({ width: 0, height: 0, top: 0 })
  const anchor = useRef({ page: jump.page, seq: -1 })

  useEffect(() => {
    let alive = true
    setFailed(undefined)
    loadBook(book.id)
      .then(async (d) => {
        const vp = (await d.getPage(1)).getViewport({ scale: 1 })
        if (!alive) return
        setRatio(vp.height / vp.width)
        setDoc(d)
      })
      .catch((err: unknown) => alive && setFailed(err instanceof Error ? err.message : String(err)))
    return () => {
      alive = false
    }
  }, [book.id, attempt])

  useEffect(() => {
    const el = scroller.current
    if (!el) return
    const measure = () => setBox((b) => {
      const width = Math.round(el.clientWidth / WIDTH_STEP) * WIDTH_STEP
      return width === b.width && el.clientHeight === b.height ? b : { ...b, width, height: el.clientHeight }
    })
    const ro = new ResizeObserver(measure)
    ro.observe(el)
    let frame = 0
    const onScroll = () => {
      cancelAnimationFrame(frame)
      frame = requestAnimationFrame(() => setBox((b) => ({ ...b, top: el.scrollTop })))
    }
    el.addEventListener('scroll', onScroll, { passive: true })
    return () => {
      ro.disconnect()
      el.removeEventListener('scroll', onScroll)
      cancelAnimationFrame(frame)
    }
  }, [failed])

  const pageW = Math.max(0, box.width - SIDE * 2)
  const pageH = ratio ? pageW * ratio : 0
  const stride = pageH + GAP

  // 跳页请求，或宽度变了（页高随之变）：把目标页 / 当前页摆到顶上
  useEffect(() => {
    const el = scroller.current
    if (!el || stride <= GAP) return
    const target = anchor.current.seq === jump.seq ? anchor.current.page : clampPage(book, jump.page)
    anchor.current = { page: target, seq: jump.seq }
    el.scrollTop = (target - 1) * stride
    setBox((b) => ({ ...b, top: el.scrollTop }))
  }, [jump.seq, stride])

  const visible = useMemo(() => {
    if (stride <= GAP) return []
    const first = Math.max(1, Math.floor(box.top / stride) + 1 - OVERSCAN)
    const last = Math.min(book.pages, Math.floor((box.top + box.height) / stride) + 1 + OVERSCAN)
    return Array.from({ length: Math.max(0, last - first + 1) }, (_, i) => first + i)
  }, [box.top, box.height, stride, book.pages])

  useEffect(() => {
    if (stride <= GAP) return
    const p = clampPage(book, Math.floor((box.top + box.height * 0.35) / stride) + 1)
    if (p !== anchor.current.page) {
      anchor.current = { ...anchor.current, page: p }
      onPage(p)
    }
  }, [box.top, box.height, stride])

  if (failed) {
    return (
      <div className={css.notice}>
        《{book.title}》没有打开：{failed}<br />
        <button type="button" className={css.textButton} onClick={() => setAttempt((n) => n + 1)}>重试</button>
      </div>
    )
  }
  return (
    <div ref={scroller} className={css.scroller} tabIndex={0} aria-label={`《${book.title}》`}>
      <div style={{ position: 'relative', height: stride > GAP ? book.pages * stride + GAP : '100%' }}>
        {!doc && <div className={css.notice} style={{ paddingTop: 48 }}>正在打开《{book.title}》…</div>}
        {doc && visible.map((n) => <PageCanvas key={n} doc={doc} n={n} top={GAP + (n - 1) * stride} width={pageW} height={pageH} />)}
      </div>
    </div>
  )
}

function PageCanvas({ doc, n, top, width, height }: { doc: PDFDocumentProxy; n: number; top: number; width: number; height: number }) {
  const canvas = useRef<HTMLCanvasElement>(null)
  useEffect(() => {
    let task: RenderTask | undefined
    let alive = true
    void doc.getPage(n).then((page) => {
      const el = canvas.current
      if (!alive || !el || width <= 0) return
      const base = page.getViewport({ scale: 1 })
      const vp = page.getViewport({ scale: (width / base.width) * Math.min(window.devicePixelRatio || 1, MAX_DPR) })
      el.width = Math.floor(vp.width)
      el.height = Math.floor(vp.height)
      task = page.render({ canvas: el, viewport: vp })
      return task.promise
    }).catch(() => undefined) // 滚走时取消渲染会抛 RenderingCancelledException
    return () => {
      alive = false
      task?.cancel()
    }
  }, [doc, n, width])
  return (
    <div className={css.page} style={{ top, height }} data-page={n}>
      <canvas ref={canvas} role="img" aria-label={`第 ${n} 页`} />
      <span className={css.pageNo}>{n}</span>
    </div>
  )
}

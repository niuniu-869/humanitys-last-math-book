/**
 * 查教材的三个工具（textbook_outline / textbook_search / textbook_read）和 python 计算在对话里的行。
 * 学生能看到老师查了什么、算了什么；结果里的题号和页码可以点，右侧教材面板翻到那一页。
 */
import type { ReactNode } from 'react'
import { type BookTarget, describeRef, useCatalog } from './catalog.ts'
import type { ToolViewProps } from './host.ts'
import { firstLine, IoCard, refClass, resultText, rowState, toolArgs, ToolRow } from './ToolRow.tsx'

export type OpenBook = (target: BookTarget) => void

/** 结果里的 `[L8-05]`、`[L8§3]` 和「L 第 140 页」。 */
const LINK = /\[([^\]\s]+)\]|([A-Za-z][A-Za-z0-9-]*) 第 (\d+) 页/g

function Linked({ text, open }: { text: string; open: OpenBook }) {
  const { catalog } = useCatalog()
  const parts: ReactNode[] = []
  let last = 0
  for (const m of text.matchAll(LINK)) {
    const book = m[2] === undefined ? undefined : catalog?.books.find((b) => b.id === m[2])
    const target = m[1] !== undefined
      ? describeRef(catalog, m[1].split('§')[0]!)?.target
      : book && Number(m[3]) <= book.pages ? { book: book.id, page: Number(m[3]) } : undefined
    if (!target) continue
    parts.push(text.slice(last, m.index))
    parts.push(<button key={m.index} type="button" className={refClass} onClick={() => open(target)}>{m[0]}</button>)
    last = m.index + m[0].length
  }
  parts.push(text.slice(last))
  return <>{parts}</>
}

function ResultCard({ props, open }: { props: ToolViewProps; open: OpenBook }) {
  const text = resultText(props)
  if (text === undefined) return null
  const error = rowState(props) === 'error'
  return <IoCard sections={[{ label: error ? '出错' : '结果', body: error ? text : <Linked text={text} open={open} />, error }]} />
}

export function createLookupViews(open: OpenBook) {
  function OutlineRow(props: ToolViewProps) {
    const args = toolArgs<{ scope: string }>(props)
    return (
      <ToolRow icon="outline" title="查目录" state={rowState(props)} useDisclosure={props.useDisclosure} summary={args ? args.scope || '全书' : undefined}>
        <ResultCard props={props} open={open} />
      </ToolRow>
    )
  }

  function SearchRow(props: ToolViewProps) {
    const args = toolArgs<{ query: string; scope: string }>(props)
    const text = rowState(props) === 'ok' ? resultText(props) : undefined
    const hits = text && /共 (\d+) 处/.exec(text)?.[1]
    return (
      <ToolRow icon="search" title="搜教材" state={rowState(props)} useDisclosure={props.useDisclosure}
        summary={args?.query && `${args.query}${args.scope ? ` · ${args.scope}` : ''}`}
        suffix={text === undefined ? undefined : hits ? `${hits} 处` : '没找到'}>
        <ResultCard props={props} open={open} />
      </ToolRow>
    )
  }

  function ReadRow(props: ToolViewProps) {
    const { catalog } = useCatalog()
    const ref = toolArgs<{ ref: string }>(props)?.ref?.trim().replace(/^@/, '')
    const view = ref ? describeRef(catalog, ref.split('§')[0]!) : undefined
    const target = view?.target
    return (
      <ToolRow icon="read" title="读教材" state={rowState(props)} useDisclosure={props.useDisclosure}
        summary={ref && (ref.includes('§') || !view ? ref : view.label)} onSummary={target && (() => open(target))}>
        <ResultCard props={props} open={open} />
      </ToolRow>
    )
  }

  return { textbook_outline: OutlineRow, textbook_search: SearchRow, textbook_read: ReadRow }
}

/** 代码里第一行有内容的语句（跳过 import 和注释），当作这次计算的摘要。 */
function codeSummary(code: string): string {
  const line = code.split('\n').map((l) => l.trim()).find((l) => l && !l.startsWith('#') && !/^(import|from)\s/.test(l))
  return firstLine(line ?? code, 60)
}

export function PythonRow(props: ToolViewProps) {
  const code = toolArgs<{ code: string }>(props)?.code
  const state = rowState(props)
  const out = resultText(props)
  return (
    <ToolRow icon="code" title="计算" state={state} useDisclosure={props.useDisclosure}
      summary={state === 'error' && out ? firstLine(out, 60) : code ? codeSummary(code) : undefined}
      suffix={state === 'ok' && out ? `→ ${firstLine(out, 40)}` : undefined}>
      {code !== undefined && (
        <IoCard sections={[
          { label: '代码', body: code },
          ...(out === undefined ? [] : [{ label: state === 'error' ? '出错' : '输出', body: out, error: state === 'error' }]),
        ]} />
      )}
    </ToolRow>
  )
}

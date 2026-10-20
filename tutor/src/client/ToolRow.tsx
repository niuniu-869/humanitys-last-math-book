/** 答疑工具在对话里的一行：图标 · 标题 · 摘要，可展开看输入输出。外观与 dsh 自带的工具行一致。 */
import { type KeyboardEvent, type ReactNode, useMemo } from 'react'
import type { ToolViewProps, UseDisclosure } from './host.ts'
import { Icon, type IconName } from './icons.tsx'
import css from './ToolRow.module.css'

export type RowState = 'running' | 'ok' | 'error'

/** 这次调用的参数原文；还在生成参数（preparing）时为 undefined。 */
export const argsRaw = (props: ToolViewProps): string | undefined =>
  props.phase === 'start' ? props.block.argsRaw : props.phase === 'result' ? props.block.call?.argsRaw : undefined

export function parseArgs<T>(raw: string | undefined): Partial<T> | undefined {
  if (!raw) return undefined
  try {
    const v: unknown = JSON.parse(raw)
    return typeof v === 'object' && v !== null ? (v as Partial<T>) : undefined
  } catch {
    return undefined
  }
}

/** 这次调用的参数；解析失败时为 undefined。 */
export const toolArgs = <T,>(props: ToolViewProps): Partial<T> | undefined => parseArgs<T>(argsRaw(props))

/** 同上，但同一份参数原文返回同一个对象，供作为 effect 依赖（流式输出时父组件会频繁重渲染）。 */
export function useToolArgs<T>(props: ToolViewProps): Partial<T> | undefined {
  const raw = argsRaw(props)
  return useMemo(() => parseArgs<T>(raw), [raw])
}

/** 工具结果的文字；失败时是报错原因。 */
export function resultText(props: ToolViewProps): string | undefined {
  if (props.phase !== 'result') return undefined
  const text = props.block.content.flatMap((c) => (c.type === 'text' && c.text ? [c.text] : [])).join('\n')
  return text || props.block.error?.reason || (props.block.isError ? props.block.error?.code : undefined)
}

export const rowState = (props: ToolViewProps): RowState => (props.phase !== 'result' ? 'running' : props.block.isError ? 'error' : 'ok')

export const firstLine = (s: string, max = 60): string => {
  const line = s.split('\n').find((l) => l.trim())?.trim() ?? ''
  return line.length > max ? `${line.slice(0, max)}…` : line
}

interface RowProps {
  icon: IconName
  title: string
  state: RowState
  useDisclosure: UseDisclosure
  summary?: string | undefined
  /** 有它时摘要显示成链接（例如翻到教材某页）。 */
  onSummary?: (() => void) | undefined
  suffix?: string | undefined
  /** 展开后的内容；没有时这一行不能展开。 */
  children?: ReactNode
}

export function ToolRow({ icon, title, state, useDisclosure, summary, onSummary, suffix, children }: RowProps) {
  const { expanded, toggle } = useDisclosure()
  const expandable = children !== undefined && children !== null && children !== false
  const onKey = (e: KeyboardEvent) => {
    if (e.target !== e.currentTarget || (e.key !== 'Enter' && e.key !== ' ')) return
    e.preventDefault()
    toggle()
  }
  return (
    <div className={css.root} data-state={state}>
      <div className={css.row} data-state={state} data-expandable={expandable || undefined}
        {...(expandable ? { role: 'button', tabIndex: 0, 'aria-expanded': expanded, onClick: toggle, onKeyDown: onKey } : {})}>
        <span className={css.leading}>
          <span className={css.idle}><Icon name={state === 'error' ? 'alert' : icon} /></span>
          {expandable && <span className={css.chevron}><Icon name={expanded ? 'up' : 'down'} /></span>}
        </span>
        <span className={css.title}>{title}</span>
        {summary && <span className={css.sep} aria-hidden="true" />}
        {summary && (onSummary
          ? <button type="button" className={css.link} title={summary} onClick={(e) => { e.stopPropagation(); onSummary() }}>{summary}</button>
          : <span className={css.summary} title={summary}>{summary}</span>)}
        {suffix && <span className={css.suffix}>{suffix}</span>}
      </div>
      {expandable && expanded && children}
    </div>
  )
}

/** 展开后的输入/输出卡。 */
export function IoCard({ sections }: { sections: readonly { label: string; body: ReactNode; error?: boolean }[] }) {
  return (
    <div className={css.card}>
      {sections.map((s, i) => (
        <div key={s.label} style={{ display: 'contents' }}>
          {i > 0 && <span className={css.divider} aria-hidden="true" />}
          <div className={css.section}>
            <span className={css.label}>{s.label}</span>
            <pre className={css.text} data-error={s.error || undefined}>{s.body}</pre>
          </div>
        </div>
      ))}
    </div>
  )
}

export const refClass = css.ref

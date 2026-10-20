/**
 * manim 图卡：服务器渲染好的图片或动画，浏览器只下载成品。
 * - 生成代码、渲染中：16:9 的占位，标题先出来，显示已经等了几秒。
 * - 报错（模型会按报错重画）：只留一行灰色的「没画成」，可展开看原因。
 * - 成功：图片，或视频（滚到眼前时静音播放一遍，可重播、拖动）；下面列出分步说明，
 *   视频播到哪一步就高亮哪一步，点一步跳到那里播放。
 * - 之后又用同一标题重画成功了：这张折叠成一行「已重画」，展开还能看。
 */
import { useEffect, useRef, useState, useSyncExternalStore } from 'react'
import { MEDIA_MARK, STEP_MARK } from '../media.ts'
import { api } from './catalog.ts'
import css from './Figure.module.css'
import type { ToolViewProps } from './host.ts'
import { IoCard, resultText, rowState, ToolRow, useToolArgs } from './ToolRow.tsx'

function Failed({ props, title, reason }: { props: ToolViewProps; title: string | undefined; reason: string | undefined }) {
  return (
    <ToolRow icon="plot" title="画图" state="error" useDisclosure={props.useDisclosure} summary={title} suffix="没画成">
      {reason && <IoCard sections={[{ label: '原因', body: reason, error: true }]} />}
    </ToolRow>
  )
}

interface Step { readonly t: number; readonly text: string }
interface Media { readonly id: string; readonly kind: 'png' | 'mp4'; readonly width: number; readonly height: number; readonly steps: readonly Step[] }

export function parseMedia(text: string | undefined): Media | undefined {
  const m = text ? MEDIA_MARK.exec(text) : null
  if (!m) return undefined
  const steps = [...text!.matchAll(STEP_MARK)].map((s) => ({ t: Number(s[1]), text: s[2]! }))
  return { id: m[1]!, kind: m[2] as Media['kind'], width: Number(m[3]), height: Number(m[4]), steps }
}

/** 页面上已经画好的 manim 图，按出现顺序；用来判断某张图之后有没有同标题的重画。 */
const drawn: { key: string; title: string }[] = []
const listeners = new Set<() => void>()
let version = 0
const subscribe = (fn: () => void) => (listeners.add(fn), () => listeners.delete(fn))
const changed = () => { version++; for (const fn of listeners) fn() }

function useSuperseded(key: string, title: string | undefined, ok: boolean): boolean {
  useEffect(() => {
    if (!ok || !title) return
    drawn.push({ key, title })
    changed()
    return () => {
      const i = drawn.findIndex((d) => d.key === key)
      if (i >= 0) drawn.splice(i, 1)
      changed()
    }
  }, [key, title, ok])
  useSyncExternalStore(subscribe, () => version)
  const i = drawn.findIndex((d) => d.key === key)
  return i >= 0 && drawn.slice(i + 1).some((d) => d.title === title)
}

function useElapsed(running: boolean): number {
  const [seconds, setSeconds] = useState(0)
  useEffect(() => {
    if (!running) return
    const start = Date.now()
    const timer = setInterval(() => setSeconds(Math.floor((Date.now() - start) / 1000)), 1000)
    return () => clearInterval(timer)
  }, [running])
  return seconds
}

/** 视频第一次滚进视野时自动播放一遍（静音，浏览器允许）；之后由学生自己点。 */
function Movie({ src, poster, videoRef: ref, onTime }: {
  src: string; poster: string; videoRef: React.RefObject<HTMLVideoElement | null>; onTime: (t: number) => void
}) {
  useEffect(() => {
    const video = ref.current
    if (!video) return
    const io = new IntersectionObserver(([entry]) => {
      if (!entry?.isIntersecting) return
      void video.play().catch(() => {})
      io.disconnect()
    }, { threshold: 0.6 })
    io.observe(video)
    return () => io.disconnect()
  }, [src, ref])
  return (
    <video ref={ref} className={css.media} src={src} poster={poster} controls muted playsInline preload="metadata"
      onTimeUpdate={(e) => onTime(e.currentTarget.currentTime)} onSeeked={(e) => onTime(e.currentTarget.currentTime)} />
  )
}

export function ManimCard(props: ToolViewProps) {
  const args = useToolArgs<{ title: string; animate: boolean }>(props)
  const state = rowState(props)
  const text = resultText(props)
  const media = state === 'ok' ? parseMedia(text) : undefined
  const superseded = useSuperseded(props.callId, args?.title, media !== undefined)
  const seconds = useElapsed(state === 'running')
  const title = args?.title

  if (state === 'error') return <Failed props={props} title={title} reason={text} />
  if (state === 'ok' && !media) return <Failed props={props} title={title} reason="渲染结果里没有找到图片" />
  if (superseded) {
    return (
      <ToolRow icon="plot" title="画图" state="ok" useDisclosure={props.useDisclosure} summary={title} suffix="已重画">
        {media && <Picture media={media} title={title} />}
      </ToolRow>
    )
  }
  if (!media) {
    const status = props.phase === 'preparing' || (props.phase === 'start' && !args?.title) ? '正在写画图代码…' : `正在渲染${args?.animate ? '动画' : ''}… ${seconds} 秒`
    return (
      <figure className={css.figure} aria-label={title ?? '图'} aria-busy="true">
        <div className={`${css.frame} ${css.screen} ${css.pending}`} style={{ aspectRatio: '16 / 9' }} />
        <figcaption className={css.caption}>
          {title && <span>{title}</span>}
          <span className={css.status}>{status}</span>
        </figcaption>
      </figure>
    )
  }
  return <Picture media={media} title={title} />
}

function Picture({ media, title }: { media: Media; title: string | undefined }) {
  const still = api(`media?id=${media.id}.png`)
  const video = useRef<HTMLVideoElement>(null)
  const [time, setTime] = useState(0)
  const movie = media.kind === 'mp4'
  // 当前步：开始时刻不晚于播放位置的最后一步（静态图不高亮）
  const current = movie ? media.steps.findLastIndex((s) => s.t <= time + 0.05) : -1
  const seek = (t: number) => {
    const v = video.current
    if (!v) return
    v.currentTime = t
    void v.play().catch(() => {})
  }
  return (
    <figure className={css.figure} aria-label={title ?? '图'}>
      <div className={`${css.frame} ${css.screen}`} style={{ aspectRatio: `${media.width} / ${media.height}` }}>
        {movie
          ? <Movie src={api(`media?id=${media.id}.mp4`)} poster={still} videoRef={video} onTime={setTime} />
          : <img className={css.media} src={still} alt={title ?? '图'} decoding="async" />}
      </div>
      {title && <figcaption className={css.caption}><span>{title}</span></figcaption>}
      {media.steps.length > 0 && (
        <ol className={css.steps}>
          {media.steps.map((s, i) => (
            <li key={i} data-current={i === current || undefined}>
              {movie
                ? <button type="button" className={css.step} onClick={() => seek(s.t)} title={`从第 ${s.t} 秒播放`}>{s.text}</button>
                : <span className={css.step}>{s.text}</span>}
            </li>
          ))}
        </ol>
      )}
    </figure>
  )
}

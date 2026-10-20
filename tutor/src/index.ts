/**
 * 宿主端：提供教材取材服务 `hlmbMaterial`、记录每个会话已附上哪些材料的会话投影，以及浏览器端用的鉴权路由。
 * 答疑 agent 本身（提示词、工具、@ 引用注入）在 `./agent`，挂在 `hlmb-tutor` 这个 agent preset 里。
 */
import type { Context } from '@deepseek-ai/cordis'
import z from '@deepseek-ai/schemastery'
import { createHash } from 'node:crypto'
import { createReadStream } from 'node:fs'
import { readFile, stat } from 'node:fs/promises'
import { homedir } from 'node:os'
import { dirname, isAbsolute, join, resolve } from 'node:path'
import { Readable } from 'node:stream'
import { createManim } from './manim.ts'
import { MEDIA_FILE } from './media.ts'
import { type Material, materialLoader, titleFor } from './material.ts'
import { probeSandbox } from './sandbox.ts'
import { MATERIAL_SOURCE, PROJECTION_KEY, type MaterialService, type SeenState, seenStateSchema } from './shared.ts'

export const name = 'hlmb-tutor'
export const inject = ['sessionProjections']

export interface Config {
  indexPath: string
  books: string[]
  manimPython: string
  mediaDir: string
  manimTimeoutMs: number
  manimMemoryMB: number
  maxMediaMB: number
}

export const Config: z<Config> = z.object({
  indexPath: z.string().default('').description('indexer 生成的 index.json 的路径。'),
  books: z.array(z.string()).default([]).description('答疑用到的分册，按显示顺序；留空时用索引里的全部分册。'),
  manimPython: z.string().default('').description('装好 manim 的 Python 解释器路径；留空时不提供 manim 画图工具。'),
  mediaDir: z.string().default('').description('画好的图和动画存放的目录；留空时用 ~/.cache/dsh-plugin-humanitys-last-math-book/media。'),
  manimTimeoutMs: z.natural().default(180_000).description('渲染一张图或一段动画的时间上限（毫秒）。'),
  manimMemoryMB: z.natural().default(4096).description('渲染进程的地址空间上限（MB）。'),
  maxMediaMB: z.natural().default(500).description('媒体目录的容量上限（MB），超过时删掉最旧的。'),
})

/** dsh-session-title `SessionTitleService` 中用到的部分（0.2.1-rc.2）。 */
interface SessionTitle {
  register(provider: {
    readonly id: string
    readonly automatic: 'first-prompt'
    generate(request: {
      readonly messages: readonly { readonly seq: number; readonly text: string }[]
      readonly currentTitle?: { readonly title: string }
      readonly signal: AbortSignal
    }): Promise<{ readonly title: string; readonly messageSeqs: readonly number[] }>
  }): () => Promise<void>
}

interface FetchRoute { path: string; methods: readonly string[]; requestBody: 'buffered'; fetch: (r: Request) => Promise<Response> }
interface Connection { fetch: { register(route: FetchRoute): () => Promise<void> } }

const WORKER = new URL('./pdf.worker.min.mjs', import.meta.url)
/** 欢迎页用的大肥鱼头像（美术许可见 NOTICE）。 */
const AVATAR = new URL('../art/fish-avatar.webp', import.meta.url)

/** 会话投影的折叠函数：记下每个单元、条目最近一次附上时的事件序号。 */
export function foldSeen(state: SeenState, event: { type: string; seq: number; data?: unknown }): SeenState {
  if (event.type !== 'user/message') return state
  const source = (event.data as { source?: { kind?: unknown; units?: unknown; items?: unknown } } | undefined)?.source
  if (source?.kind !== MATERIAL_SOURCE) return state
  const mark = (prev: Record<string, number>, keys: unknown): Record<string, number> =>
    Array.isArray(keys) ? { ...prev, ...Object.fromEntries(keys.filter((k) => typeof k === 'string').map((k) => [k, event.seq])) } : prev
  return { units: mark(state.units, source.units), items: mark(state.items, source.items) }
}

const MEDIA_TYPES: Record<string, string> = { png: 'image/png', mp4: 'video/mp4' }

/**
 * 画好的图和动画。文件名是内容哈希，可以长期缓存；视频支持单段 Range（Safari 播放视频必须）。
 */
export async function serveMedia(req: Request, mediaDir: string): Promise<Response> {
  const id = new URL(req.url).searchParams.get('id') ?? ''
  if (!MEDIA_FILE.test(id)) return new Response('没有这个文件', { status: 404 })
  const file = join(mediaDir, id)
  const info = await stat(file).catch(() => undefined)
  if (!info) return new Response('图已经清理掉了，请重新画', { status: 404 })
  const type = MEDIA_TYPES[id.slice(id.lastIndexOf('.') + 1)]!
  const base = { 'Content-Type': type, 'Accept-Ranges': 'bytes', 'Cache-Control': 'private, max-age=31536000, immutable' }
  const range = /^bytes=(\d*)-(\d*)$/.exec(req.headers.get('range') ?? '')
  if (range && (range[1] || range[2])) {
    const start = range[1] ? Number(range[1]) : Math.max(0, info.size - Number(range[2]))
    const end = range[1] && range[2] ? Math.min(Number(range[2]), info.size - 1) : info.size - 1
    if (start > end || start >= info.size) return new Response(null, { status: 416, headers: { 'Content-Range': `bytes */${info.size}` } })
    const headers = { ...base, 'Content-Length': String(end - start + 1), 'Content-Range': `bytes ${start}-${end}/${info.size}` }
    if (req.method === 'HEAD') return new Response(null, { status: 206, headers })
    return new Response(Readable.toWeb(createReadStream(file, { start, end })) as ReadableStream, { status: 206, headers })
  }
  const headers = { ...base, 'Content-Length': String(info.size) }
  if (req.method === 'HEAD') return new Response(null, { headers })
  return new Response(Readable.toWeb(createReadStream(file)) as ReadableStream, { headers })
}

async function servePdf(req: Request, material: Material): Promise<Response> {
  const book = material.book(new URL(req.url).searchParams.get('book') ?? '')
  if (!book) return new Response('没有这本书', { status: 404 })
  const file = isAbsolute(book.pdf) ? book.pdf : resolve(dirname(material.indexPath), book.pdf)
  const { size, mtimeMs } = await stat(file)
  const etag = `"${createHash('sha1').update(`${file}:${size}:${mtimeMs}`).digest('hex').slice(0, 16)}"`
  const headers = { 'Content-Type': 'application/pdf', 'Content-Length': String(size), 'Cache-Control': 'private, no-cache', ETag: etag }
  if (req.headers.get('if-none-match') === etag) return new Response(null, { status: 304, headers: { ETag: etag } })
  if (req.method === 'HEAD') return new Response(null, { headers })
  return new Response(Readable.toWeb(createReadStream(file)) as ReadableStream, { headers })
}

export function apply(ctx: Context, config: Config): void {
  const load = config.indexPath
    ? materialLoader(config.indexPath, config.books)
    : () => Promise.reject(new Error('还没有配置教材索引：在 profile 的 cordis.patch.yml 里给 hlmb-tutor 设置 indexPath'))
  const sandbox = probeSandbox()
  void sandbox.then((problem) => { if (problem) ctx.logger.warn('python 沙箱不可用，答疑里不提供 python 工具：%s', problem) })
  const manim = config.manimPython
    ? createManim({
      python: config.manimPython,
      mediaDir: config.mediaDir || join(homedir(), '.cache', 'dsh-plugin-humanitys-last-math-book', 'media'),
      timeoutMs: config.manimTimeoutMs, memoryMB: config.manimMemoryMB, maxMediaMB: config.maxMediaMB,
    })
    : undefined
  void manim?.ready.then((problem) => { if (problem) ctx.logger.warn('manim 不可用，答疑里不提供画图工具：%s', problem) })
  const service: MaterialService = { load, sandbox, manim }
  ctx.effect(() => ctx.provide('hlmbMaterial', service), 'hlmb: material service')

  ctx.effect(() => ctx.sessionProjections.register({
    key: PROJECTION_KEY,
    stateSchema: seenStateSchema,
    stateVersion: 1,
    init: () => ({ units: {}, items: {} }),
    apply: (state, event) => foldSeen(state, event as unknown as Parameters<typeof foldSeen>[1]),
  }), 'hlmb: material projection')

  const guarded = (handler: (req: Request, m: Material) => Promise<Response>) => async (req: Request): Promise<Response> => {
    try {
      return await handler(req, await load())
    } catch (err) {
      return new Response(err instanceof Error ? err.message : String(err), { status: 503 })
    }
  }

  // 会话标题：学生常常只发一个 @L8-01，按原文起标题只会得到题号或空话；有引用时用题目的考查点、单元名起标题，没有时取第一个分句。
  ctx.inject(['sessionTitle'], (c) => {
    const titles = (c as unknown as { sessionTitle: SessionTitle }).sessionTitle
    c.effect(() => titles.register({
      id: 'hlmb-tutor-refs',
      automatic: 'first-prompt',
      async generate({ messages, currentTitle }) {
        const first = messages[0]
        if (!first) throw new Error('还没有可用来起标题的消息')
        const title = titleFor(await load(), first.text) ?? currentTitle?.title ?? first.text
        return { title, messageSeqs: [first.seq] }
      },
    }), 'hlmb: session titles')
  })

  ctx.inject(['connection'], (c) => {
    const conn = (c as unknown as { connection: Connection }).connection
    c.effect(() => conn.fetch.register({
      path: '/api/hlmb/catalog', methods: ['GET'], requestBody: 'buffered',
      fetch: guarded(async (_req, m) => Response.json(m.catalog(), { headers: { 'Cache-Control': 'private, no-cache' } })),
    }), 'hlmb: catalog route')
    c.effect(() => conn.fetch.register({
      path: '/api/hlmb/pdf', methods: ['GET', 'HEAD'], requestBody: 'buffered', fetch: guarded(servePdf),
    }), 'hlmb: pdf route')
    c.effect(() => conn.fetch.register({
      path: '/api/hlmb/pdf-worker.mjs', methods: ['GET'], requestBody: 'buffered',
      fetch: async () => new Response(await readFile(WORKER), {
        headers: { 'Content-Type': 'text/javascript', 'Cache-Control': 'private, max-age=86400' },
      }),
    }), 'hlmb: pdf worker route')
    if (manim) {
      c.effect(() => conn.fetch.register({
        path: '/api/hlmb/media', methods: ['GET', 'HEAD'], requestBody: 'buffered',
        fetch: (req) => serveMedia(req, manim.mediaDir),
      }), 'hlmb: media route')
    }
    c.effect(() => conn.fetch.register({
      path: '/api/hlmb/art/fish-avatar.webp', methods: ['GET'], requestBody: 'buffered',
      fetch: async () => new Response(await readFile(AVATAR), {
        headers: { 'Content-Type': 'image/webp', 'Cache-Control': 'private, max-age=86400' },
      }),
    }), 'hlmb: avatar route')
  })
}

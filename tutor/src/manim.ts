/**
 * Manim 画图：在 bwrap 里运行 manim/run.py，把模型写的场景渲染成图片或视频，并做自查（见 run.py）。
 *
 * - 产物存在媒体目录：`<id>.png`（最终画面，也是视频的封面）、`<id>.mp4`、`<id>-sheet.png`（动画关键帧拼图）、`<id>.json`（报告）。
 * - id 是代码、输出规格和工具库内容的哈希：同一段代码只渲染一次，会话回放时直接读文件。
 * - 同一时间只渲染一张，免得几个会话同时画图把机器拖慢；媒体目录超过上限时删掉最旧的。
 */
import { createHash } from 'node:crypto'
import { readFileSync } from 'node:fs'
import { copyFile, mkdir, mkdtemp, readdir, readFile, rm, stat, unlink, writeFile } from 'node:fs/promises'
import { tmpdir } from 'node:os'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { clip, runSandboxed, sandboxCommand } from './sandbox.ts'

const KIT_DIR = fileURLToPath(new URL('../manim/', import.meta.url))

export interface ManimOptions {
  /** 装好 manim 的 Python 解释器（例如 conda 环境里的 bin/python）。 */
  python: string
  mediaDir: string
  timeoutMs: number
  memoryMB: number
  maxMediaMB: number
}

export interface ManimIssue { t: number; msg: string }
/** 一步说明：从第 t 秒开始（静态图里没有意义）。 */
export interface ManimStep { t: number; text: string }

export type ManimReport =
  | {
    ok: true
    id: string
    animate: boolean
    width: number
    height: number
    /** 动画总时长（秒）；静态图是场景里 play / wait 的总时长，没有意义。 */
    duration: number
    issues: ManimIssue[]
    manifest: string[]
    steps: ManimStep[]
    /** 动画关键帧拼图里各帧对应的时刻。 */
    sheetTimes?: number[]
  }
  | { ok: false; error: string; internal?: boolean }

/** 静态图和动画的输出规格。 */
const STILL = { width: 1280, height: 720, fps: 15 }
const MOVIE = { width: 960, height: 540, fps: 30 }
/** 渲染脚本和工具库的内容哈希：改了它们，旧缓存自然失效。 */
const KIT_HASH = createHash('sha256')
  .update(readFileSync(join(KIT_DIR, 'run.py')))
  .update(readFileSync(join(KIT_DIR, 'tutor_kit.py')))
  .digest('hex')
const MAX_SECONDS = 30

export function manimId(code: string, animate: boolean): string {
  const spec = animate ? MOVIE : STILL
  return createHash('sha256').update(JSON.stringify({ kit: KIT_HASH, animate, spec, code })).digest('hex').slice(0, 24)
}

interface RunReport {
  ok: boolean
  error?: string
  internal?: boolean
  animate?: boolean
  width?: number
  height?: number
  duration?: number
  issues?: ManimIssue[]
  manifest?: string[]
  steps?: ManimStep[]
  files?: { final: string; video?: string; sheet?: string; sheetTimes?: number[] }
}

export interface ManimRenderer {
  /** 启动时实测一次；可用时为 undefined，不可用时是原因。 */
  readonly ready: Promise<string | undefined>
  readonly mediaDir: string
  render(job: { code: string; animate: boolean }, signal: AbortSignal): Promise<ManimReport>
}

export function createManim(options: ManimOptions): ManimRenderer {
  const envDir = dirname(dirname(options.python))
  let queue: Promise<unknown> = Promise.resolve()

  /** 沙箱：只读挂上 Python 环境、工具库、字体和 TeX，读写挂上本次的工作目录，断网。 */
  const command = (work: string, argv: string[]) => sandboxCommand(options.memoryMB * 1024 * 1024, [
    '--setenv', 'TEXMFVAR', '/tmp/texmf-var',
    '--ro-bind', '/etc/fonts', '/etc/fonts',
    '--ro-bind-try', '/etc/texmf', '/etc/texmf',
    '--ro-bind-try', '/var/lib/texmf', '/var/lib/texmf',
    '--ro-bind', envDir, envDir,
    '--ro-bind', KIT_DIR, '/kit',
    '--bind', work, '/work',
    '--chdir', '/work',
  ], [options.python, '-E', '-s', ...argv])

  const runOnce = async (id: string, job: { code: string; animate: boolean }, signal: AbortSignal): Promise<ManimReport> => {
    const work = await mkdtemp(join(tmpdir(), 'hlmb-manim-'))
    try {
      const spec = job.animate ? MOVIE : STILL
      await writeFile(join(work, 'scene.py'), job.code)
      await writeFile(join(work, 'job.json'), JSON.stringify({ animate: job.animate, ...spec, maxSeconds: MAX_SECONDS }))
      const r = await runSandboxed(command(work, ['/kit/run.py', '/work']), '', {
        timeoutMs: options.timeoutMs, memoryBytes: options.memoryMB * 1024 * 1024, outputChars: 4000, signal,
      })
      signal.throwIfAborted()
      if (r.timedOut) return { ok: false, error: `渲染超过 ${options.timeoutMs / 1000} 秒，被终止。请减少对象数量、缩短动画，或改画静态图。` }
      const report = await readFile(join(work, 'report.json'), 'utf8').then((t) => JSON.parse(t) as RunReport, () => undefined)
      if (!report) return { ok: false, internal: true, error: `渲染进程异常退出（退出码 ${r.exitCode}）：${clip(r.stderr || r.stdout, 1500)}` }
      if (!report.ok || !report.files) return { ok: false, error: report.error ?? '渲染失败', internal: report.internal }
      await mkdir(options.mediaDir, { recursive: true })
      const put = (from: string, name: string) => copyFile(join(work, from), join(options.mediaDir, name))
      await put(report.files.final, `${id}.png`)
      if (report.files.video) await put(report.files.video, `${id}.mp4`)
      if (report.files.sheet) await put(report.files.sheet, `${id}-sheet.png`)
      const result: ManimReport = {
        ok: true, id, animate: job.animate, width: report.width!, height: report.height!, duration: report.duration ?? 0,
        issues: report.issues ?? [], manifest: report.manifest ?? [], steps: report.steps ?? [],
        ...(report.files.sheetTimes ? { sheetTimes: report.files.sheetTimes } : {}),
      }
      await writeFile(join(options.mediaDir, `${id}.json`), JSON.stringify(result))
      await prune(options.mediaDir, options.maxMediaMB * 1024 * 1024, id)
      return result
    } finally {
      await rm(work, { recursive: true, force: true })
    }
  }

  const render = async (job: { code: string; animate: boolean }, signal: AbortSignal): Promise<ManimReport> => {
    const id = manimId(job.code, job.animate)
    const cached = await readFile(join(options.mediaDir, `${id}.json`), 'utf8').then((t) => JSON.parse(t) as ManimReport, () => undefined)
    if (cached) return cached
    const run = queue.then(() => {
      signal.throwIfAborted()
      return runOnce(id, job, signal)
    })
    queue = run.catch(() => {})
    return run
  }

  const ready = (async (): Promise<string | undefined> => {
    try {
      const work = await mkdtemp(join(tmpdir(), 'hlmb-manim-probe-'))
      try {
        const r = await runSandboxed(command(work, ['-c', 'import manim, cairo, manimpango; print("ok")']), '', {
          timeoutMs: 60_000, memoryBytes: options.memoryMB * 1024 * 1024, outputChars: 2000,
        })
        return r.exitCode === 0 && r.stdout.trim() === 'ok' ? undefined : (r.stderr.trim() || `exit ${r.exitCode}`)
      } finally {
        await rm(work, { recursive: true, force: true })
      }
    } catch (err) {
      return err instanceof Error ? err.message : String(err)
    }
  })()

  return { ready, mediaDir: options.mediaDir, render }
}

/** 媒体目录超过上限时，按修改时间从旧到新删，刚生成的那组不删。 */
async function prune(dir: string, maxBytes: number, keep: string): Promise<void> {
  const files = await Promise.all((await readdir(dir)).map(async (name) => ({ name, ...(await stat(join(dir, name)).then((s) => ({ size: s.size, mtime: s.mtimeMs }))) })))
  let total = files.reduce((n, f) => n + f.size, 0)
  for (const f of files.sort((a, b) => a.mtime - b.mtime)) {
    if (total <= maxBytes) break
    if (f.name.startsWith(keep)) continue
    await unlink(join(dir, f.name)).catch(() => {})
    total -= f.size
  }
}

/**
 * 给模型的渲染回执：结果、自动检查、图元清单，以及怎样对照附图自查。
 * @param seesImage - 本轮模型能不能看到附上的成品图。
 */
export function describeRender(r: Extract<ManimReport, { ok: true }>, title: string, seesImage: boolean): string {
  const what = r.animate ? `动画 ${r.duration} 秒（${r.width}×${r.height}）` : `静态图（${r.width}×${r.height}）`
  const issues = r.issues.length
    ? `自动检查发现 ${r.issues.length} 处问题：\n${r.issues.map((i) => `- ${r.animate ? `${i.t} 秒时：` : ''}${i.msg}`).join('\n')}`
    : '自动检查：没有发现文字出界、重叠或过小。'
  const picture = !seesImage
    ? '（当前模型看不到图片，只能靠上面的检查和清单自查。）'
    : r.animate
      ? `附图是动画各段结束时的画面，按时间从左到右、从上到下排列：${(r.sheetTimes ?? []).map((t) => `${t} 秒`).join('、')}。`
      : '附图是渲染出的成品。'
  const steps = r.steps.length
    ? `分步说明（列在图下方，播放到哪一步就高亮哪一步）：\n${r.steps.map((s) => `[step ${s.t}] ${s.text.replace(/\s+/g, ' ')}`).join('\n')}`
    : '没有分步说明。'
  return [
    `已渲染「${title}」：${what}，学生已经能看到。`,
    `[manim ${r.id} ${r.animate ? 'mp4' : 'png'} ${r.width}x${r.height}]`,
    steps,
    issues,
    `图元清单（最终画面）：\n${r.manifest.map((l, i) => (i === 0 ? l : `- ${l}`)).join('\n')}`,
    picture,
    '请自查：① 数学对不对：清单里的坐标、交点、斜率、函数值是否和题目、和你的讲解一致；② 看得清不清楚：标签是否压在线上或离对象太远，颜色是否区分得开，画面是否拥挤；'
    + '③ 分步说明和画面对得上：每一步说的就是那一段画面在变的东西。'
    + '有问题就改代码重画，title 保持不变（学生只会看到同一标题的最新一张）；没有问题就结束，不用再写正文。',
  ].join('\n\n')
}

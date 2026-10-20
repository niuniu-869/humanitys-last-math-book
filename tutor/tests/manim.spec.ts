import { existsSync } from 'node:fs'
import { mkdtemp, readFile, rm, writeFile } from 'node:fs/promises'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterAll, beforeAll, describe, expect, it } from 'vitest'
import { serveMedia } from '../src/index.ts'
import { createManim, describeRender, manimId } from '../src/manim.ts'
import { MEDIA_FILE, MEDIA_MARK, STEP_MARK } from '../src/media.ts'

describe('manimId', () => {
  it('同一段代码同一规格得到同一个 id，静态图和动画不同', () => {
    const id = manimId('class Main(Scene): pass', false)
    expect(id).toMatch(/^[0-9a-f]{24}$/)
    expect(manimId('class Main(Scene): pass', false)).toBe(id)
    expect(manimId('class Main(Scene): pass', true)).not.toBe(id)
    expect(MEDIA_FILE.test(`${id}.png`) && MEDIA_FILE.test(`${id}-sheet.png`) && MEDIA_FILE.test(`${id}.mp4`)).toBe(true)
    expect(MEDIA_FILE.test(`../${id}.png`) || MEDIA_FILE.test(`${id}.json`)).toBe(false)
  })
})

describe('describeRender', () => {
  const report = {
    ok: true as const, id: 'a'.repeat(24), animate: true, width: 960, height: 540, duration: 6.5,
    issues: [{ t: 2, msg: '文字「切线」超出画面右边' }], manifest: ['坐标轴 x∈[-3,3]', '点 A (1, 1)'], sheetTimes: [1, 3.5, 6.5],
    steps: [{ t: 0, text: '蓝色曲线是 y=x²' }, { t: 2.5, text: 'Q 沿曲线滑向 P，\n割线斜率变小' }],
  }
  it('回执里的标记行能被图卡认出来', () => {
    const text = describeRender(report, '切线', true)
    const m = MEDIA_MARK.exec(text)
    expect(m?.slice(1)).toEqual(['a'.repeat(24), 'mp4', '960', '540'])
  })
  it('分步说明逐行写出，图卡能按行取回（多行文字压成一行）', () => {
    const text = describeRender(report, '切线', true)
    expect([...text.matchAll(STEP_MARK)].map((m) => [Number(m[1]), m[2]])).toEqual([[0, '蓝色曲线是 y=x²'], [2.5, 'Q 沿曲线滑向 P， 割线斜率变小']])
  })
  it('写明自动检查、清单、拼图时刻和自查要求；看不到图时说明', () => {
    const text = describeRender(report, '切线', true)
    expect(text).toContain('2 秒时：文字「切线」超出画面右边')
    expect(text).toContain('- 点 A (1, 1)')
    expect(text).toContain('1 秒、3.5 秒、6.5 秒')
    expect(text).toContain('title 保持不变')
    expect(describeRender({ ...report, issues: [] }, '切线', false)).toContain('当前模型看不到图片')
  })
})

describe('serveMedia', () => {
  let dir: string
  const id = `${'b'.repeat(24)}.mp4`
  const get = (name: string, headers: Record<string, string> = {}, method = 'GET') =>
    serveMedia(new Request(`http://x/api/hlmb/media?id=${encodeURIComponent(name)}`, { headers, method }), dir)
  beforeAll(async () => {
    dir = await mkdtemp(join(tmpdir(), 'hlmb-media-test-'))
    await writeFile(join(dir, id), '0123456789')
    await writeFile(join(dir, 'secret.txt'), 'x')
  })
  afterAll(() => rm(dir, { recursive: true, force: true }))

  it('整文件：类型、长度、长期缓存', async () => {
    const r = await get(id)
    expect(r.status).toBe(200)
    expect(r.headers.get('content-type')).toBe('video/mp4')
    expect(r.headers.get('content-length')).toBe('10')
    expect(r.headers.get('cache-control')).toContain('immutable')
    expect(await r.text()).toBe('0123456789')
  })
  it('单段 Range：起止、只给起点、只给末尾长度、越界', async () => {
    const a = await get(id, { range: 'bytes=2-4' })
    expect([a.status, a.headers.get('content-range'), await a.text()]).toEqual([206, 'bytes 2-4/10', '234'])
    const b = await get(id, { range: 'bytes=7-' })
    expect(await b.text()).toBe('789')
    const c = await get(id, { range: 'bytes=-3' })
    expect(await c.text()).toBe('789')
    const d = await get(id, { range: 'bytes=0-99' })
    expect([d.headers.get('content-range'), await d.text()]).toEqual(['bytes 0-9/10', '0123456789'])
    const e = await get(id, { range: 'bytes=10-' })
    expect([e.status, e.headers.get('content-range')]).toEqual([416, 'bytes */10'])
  })
  it('HEAD 不带正文；不合规的文件名和不存在的文件一律 404', async () => {
    const h = await get(id, {}, 'HEAD')
    expect([h.status, h.headers.get('content-length'), await h.text()]).toEqual([200, '10', ''])
    for (const name of ['secret.txt', `../${id}`, `${'c'.repeat(24)}.png`]) expect((await get(name)).status).toBe(404)
  })
})

/** 装好 manim 的 Python 解释器，例如 `MANIM_PYTHON=/path/to/manim-env/bin/python pnpm test`；不设就跳过真实渲染。 */
const python = process.env.MANIM_PYTHON ?? ''

describe.skipIf(!python || !existsSync(python))('createManim（真实渲染，需要 manim 环境和 bwrap）', () => {
  let mediaDir: string
  const manim = () => createManim({ python, mediaDir, timeoutMs: 120_000, memoryMB: 4096, maxMediaMB: 50 })
  beforeAll(async () => { mediaDir = await mkdtemp(join(tmpdir(), 'hlmb-manim-test-')) })
  afterAll(() => rm(mediaDir, { recursive: true, force: true }))

  it('静态图：出 png，清单里有函数采样，中文能排；同样的代码第二次直接读缓存', async () => {
    const m = manim()
    expect(await m.ready).toBeUndefined()
    const code = [
      'class Main(Scene):',
      '    def construct(self):',
      '        ax = Axes(x_range=[-2, 2, 1], y_range=[-1, 4, 1], x_length=7, y_length=5)',
      '        g = ax.plot(lambda x: x**2, color=YELLOW)',
      '        self.say("抛物线开口向上")',
      '        self.add(ax, g, zh("抛物线 $y=x^2$").to_corner(UL))',
    ].join('\n')
    const r = await m.render({ code, animate: false }, AbortSignal.timeout(120_000))
    expect(r.ok).toBe(true)
    if (!r.ok) return
    expect(r.manifest.join('\n')).toContain('f(1)=1, f(2)=4')
    expect(r.steps).toEqual([{ t: 0, text: '抛物线开口向上' }])
    expect((await readFile(join(mediaDir, `${r.id}.png`))).subarray(1, 4).toString()).toBe('PNG')
    const again = await m.render({ code, animate: false }, AbortSignal.timeout(1000))
    expect(again).toEqual(r)
  }, 150_000)

  it('代码出错时返回出错的行，而不是整段 traceback', async () => {
    const r = await manim().render({ code: 'class Main(Scene):\n    def construct(self):\n        self.add(Circl())', animate: false }, AbortSignal.timeout(120_000))
    expect(r.ok).toBe(false)
    if (r.ok) return
    expect(r.error).toContain('Circl')
    expect(r.internal).toBeFalsy()
  }, 150_000)
})

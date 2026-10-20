import { describe, expect, it } from 'vitest'
import { clip, probeSandbox, runPython } from '../src/sandbox.ts'

const problem = await probeSandbox()
const opts = { timeoutMs: 20_000, memoryBytes: 1 << 30, outputChars: 4000 }

describe('clip', () => {
  it('超长输出保留头尾', () => {
    const s = clip('a'.repeat(70) + 'b'.repeat(130), 100)
    expect(s.startsWith('a'.repeat(70))).toBe(true)
    expect(s.endsWith('b'.repeat(30))).toBe(true)
    expect(s).toContain('省略 100 个字符')
    expect(clip('短', 100)).toBe('短')
  })
})

describe.skipIf(problem !== undefined)('runPython（需要 bwrap 和非特权 user namespace）', () => {
  it('能用 sympy 和 numpy', async () => {
    const r = await runPython('import sympy as s, numpy as np\nx=s.symbols("x")\nprint(s.integrate(x**2,(x,0,1)), np.linalg.det(np.eye(2)))', opts)
    expect(r).toMatchObject({ exitCode: 0, timedOut: false })
    expect(r.stdout.trim()).toBe('1/3 1.0')
  })

  it('以 nobody 运行，没有 capability，看不到项目和家目录，断网', async () => {
    const code = [
      'import os, socket',
      'print(os.getuid())',
      'print(open("/proc/self/status").read().split("CapEff:")[1].split()[0])',
      `print(os.path.exists("/root"), os.path.exists(${JSON.stringify(process.cwd())}), os.path.exists("/etc/passwd"))`,
      'try:',
      '    socket.create_connection(("1.1.1.1", 80), timeout=3); print("net")',
      'except OSError as e:',
      '    print("offline")',
    ].join('\n')
    const r = await runPython(code, opts)
    expect(r.stdout.trim().split('\n')).toEqual(['65534', '0000000000000000', 'False False False', 'offline'])
  })

  it('超时被杀掉，已输出的内容保留', async () => {
    const r = await runPython('print("start", flush=True)\nwhile True: pass', { ...opts, timeoutMs: 1500 })
    expect(r.timedOut).toBe(true)
    expect(r.stdout.trim()).toBe('start')
  })

  it('超出内存上限时是 MemoryError，而不是拖垮宿主', async () => {
    const r = await runPython('x = bytearray(2 * 1024**3)', { ...opts, memoryBytes: 512 * 1024 * 1024 })
    expect(r.exitCode).not.toBe(0)
    expect(r.stderr).toContain('MemoryError')
  })

  it('疯狂 print 时只收上限内的输出', async () => {
    const r = await runPython('for i in range(10**6): print(i)', { ...opts, outputChars: 1000 })
    expect(r.exitCode).toBe(0)
    expect(r.stdout.length).toBeLessThan(1100)
  })
})

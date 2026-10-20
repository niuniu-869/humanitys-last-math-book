/**
 * 在 bubblewrap 里运行模型写的 Python。
 *
 * 防的是「模型写错的代码」而不是蓄意攻击：死循环、吃光内存、误读误写文件、联网。
 * 沙箱里只读挂载 /usr，看不到家目录、项目和密钥；断网；以 nobody 身份运行，丢弃全部 capability；
 * 外层用 prlimit 限制地址空间，超时直接杀进程。dsh 自带的 sandbox 只管写文件，管不了读和网络，所以这里自己调 bwrap。
 */
import { spawn } from 'node:child_process'

export interface RunOptions {
  timeoutMs: number
  memoryBytes: number
  /** 返回给模型的输出上限（字符），防止一次 print 撑爆上下文。 */
  outputChars: number
  signal?: AbortSignal
}

export interface RunResult {
  stdout: string
  stderr: string
  exitCode: number | null
  timedOut: boolean
}

const BWRAP_ARGS = [
  '--unshare-all', '--unshare-user', '--uid', '65534', '--gid', '65534',
  '--cap-drop', 'ALL', '--die-with-parent', '--new-session',
  '--clearenv', '--setenv', 'PATH', '/usr/bin:/bin', '--setenv', 'HOME', '/tmp',
  '--setenv', 'OPENBLAS_NUM_THREADS', '1', '--setenv', 'OMP_NUM_THREADS', '1',
  '--ro-bind', '/usr', '/usr',
  '--symlink', 'usr/lib', '/lib', '--symlink', 'usr/lib64', '/lib64', '--symlink', 'usr/bin', '/bin',
  '--ro-bind-try', '/etc/alternatives', '/etc/alternatives',
  '--ro-bind-try', '/etc/ld.so.cache', '/etc/ld.so.cache',
  '--proc', '/proc', '--dev', '/dev', '--tmpfs', '/tmp',
]

/**
 * 沙箱里的一条命令。
 * @param extra - 追加的 bwrap 参数（额外的只读 / 读写挂载、环境变量、--chdir），放在基础参数之后。
 * @param argv - 沙箱里要执行的程序和参数。
 */
export function sandboxCommand(memoryBytes: number, extra: readonly string[], argv: readonly string[]): [string, string[]] {
  return ['prlimit', [`--as=${memoryBytes}`, '--', 'bwrap', ...BWRAP_ARGS, ...extra, ...argv]]
}

/** 把超长输出截成头尾两段。 */
export function clip(text: string, max: number): string {
  if (text.length <= max) return text
  const head = Math.floor(max * 0.7)
  const tail = max - head
  return `${text.slice(0, head)}\n…（中间省略 ${text.length - max} 个字符）…\n${text.slice(-tail)}`
}

export function runPython(code: string, options: RunOptions): Promise<RunResult> {
  return runSandboxed(sandboxCommand(options.memoryBytes, ['--chdir', '/tmp'], ['/usr/bin/python3', '-I', '-']), code, options)
}

/** 运行一条沙箱命令，stdin 写入 input，超时或取消时直接杀掉。 */
export function runSandboxed([file, args]: [string, string[]], input: string, options: RunOptions): Promise<RunResult> {
  return new Promise((resolve, reject) => {
    const child = spawn(file, args, { stdio: ['pipe', 'pipe', 'pipe'] })
    let stdout = ''
    let stderr = ''
    let timedOut = false
    // 输出先按上限的两倍收，避免死循环 print 把宿主内存吃满
    const cap = options.outputChars * 2
    child.stdout.setEncoding('utf8').on('data', (d: string) => { if (stdout.length < cap) stdout += d })
    child.stderr.setEncoding('utf8').on('data', (d: string) => { if (stderr.length < cap) stderr += d })
    const kill = (): void => { child.kill('SIGKILL') }
    const timer = setTimeout(() => { timedOut = true; kill() }, options.timeoutMs)
    options.signal?.addEventListener('abort', kill, { once: true })
    child.on('error', (err) => { clearTimeout(timer); reject(err) })
    child.on('close', (exitCode) => {
      clearTimeout(timer)
      options.signal?.removeEventListener('abort', kill)
      resolve({ stdout: clip(stdout, options.outputChars), stderr: clip(stderr, options.outputChars), exitCode, timedOut })
    })
    child.stdin.on('error', () => {}) // 进程提前退出时写 stdin 会 EPIPE，结果以 close 为准
    child.stdin.end(input)
  })
}

/** 启动时实测一次：bwrap、prlimit、python3 都在，且本机允许非特权 user namespace。 */
export async function probeSandbox(): Promise<string | undefined> {
  try {
    const r = await runPython('print(1+1)', { timeoutMs: 10_000, memoryBytes: 1 << 30, outputChars: 1000 })
    return r.exitCode === 0 && r.stdout.trim() === '2' ? undefined : (r.stderr.trim() || `exit ${r.exitCode}`)
  } catch (err) {
    return err instanceof Error ? err.message : String(err)
  }
}

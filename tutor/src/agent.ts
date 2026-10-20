/**
 * 答疑 agent：挂在 `hlmb-tutor` agent preset 里，每个会话一份。
 *
 * - 提示词：prompts/ 下的规则作为完整系统提示（complete），不带编码助手的人设和运行时上下文。
 * - 工具：查教材（textbook_outline / textbook_search / textbook_read）、manim（3Blue1Brown 的画图库，服务器上渲染成图片或动画）、
 *   python（bwrap 沙箱）、联网（宿主的 web_search / web_fetch）。manim 和 python 实测可用时才注册；宿主的其他全局工具一律不给。
 * - 取材：学生消息里的 `@题号` / `@分册/页码` 在进入模型前换成教材原文，作为一条「教材材料」消息放在学生消息前面
 *   （讲义在前、问题在后，同一单元的不同会话共享前缀，能命中上下文缓存）。对话里仍可见的单元和条目不重复附上。
 */
import type { Context } from '@deepseek-ai/cordis'
import type { Agent, PreStepDecision } from '@deepseek-ai/dsh-agent'
import { createUserMessage } from '@deepseek-ai/dsh-llm'
import type { UserMessage } from '@deepseek-ai/dsh-session'
import { defineTool, type ToolDefinition } from '@deepseek-ai/dsh-tools'
import z from '@deepseek-ai/schemastery'
import { readFile } from 'node:fs/promises'
import { join } from 'node:path'
import { DOC_KINDS, outline, read, REF_HELP, search } from './lookup.ts'
import { describeRender } from './manim.ts'
import { type Bundle, refTokens } from './material.ts'
import { runPython } from './sandbox.ts'
import { MATERIAL_SOURCE, type MaterialSource, PROJECTION_KEY } from './shared.ts'

export const name = 'hlmb-tutor-agent'
export const inject = ['hlmbMaterial', 'tools', 'systemPrompt', 'sessionProjections']

export interface Config {
  pythonTimeoutMs: number
  pythonMemoryMB: number
}

export const Config: z<Config> = z.object({
  pythonTimeoutMs: z.natural().default(30_000).description('python 工具单次运行的时间上限（毫秒）。'),
  pythonMemoryMB: z.natural().default(1024).description('python 工具的地址空间上限（MB）。'),
})

/** 与 dsh-system-prompt 的 PERSONA_PREFIX_SECTION 同名：在本会话的作用域里顶替部署级人设。 */
const PERSONA_SECTION = 'deployment:persona-prefix'
const PYTHON_OUTPUT_CHARS = 8000
/** 宿主的联网工具（dsh-tool-web），答疑放行它们。 */
const WEB_TOOLS = ['web_search', 'web_fetch']

/** 结构化的图片引用，形状与 dsh-tool-fs 的 read_image 输出一致。 */
interface ImageValue { attachmentId: string; mediaType: 'image/png'; bytes: number; width: number; height: number; name?: string }
interface Attachments { saveImage(input: { data: Uint8Array; mediaType: 'image/png'; name: string }): Promise<ImageValue> }
interface ModelInfo { inputModalities?: readonly string[] }
interface Llm { resolveModelInfo(provider: string, model: string, signal?: AbortSignal): Promise<ModelInfo> }

/** 同一张图（同一标题）一轮里最多渲染几次，报错的也算：一次初画，加上按自查或报错重画。 */
const MAX_RENDERS = 4

const prompt = (file: string): Promise<string> => readFile(new URL(`../prompts/${file}`, import.meta.url), 'utf8')

/**
 * @param bundle - 新附上的材料；全都已在对话里时为 undefined。
 * @param missing - 教材里找不到的引用，告诉模型，免得它照着题号编内容。
 */
function materialMessage(bundle: Bundle | undefined, missing: readonly string[]): UserMessage {
  const lost = missing.length ? `找不到 ${missing.map((t) => `@${t}`).join('、')}` : ''
  const summary = [bundle?.summary, lost].filter(Boolean).join('；')
  const body = [
    bundle?.text,
    lost && `（学生引用的 ${missing.map((t) => `@${t}`).join('、')} 在教材里找不到，请学生核对题号或页码，不要凭题号猜内容。）`,
  ].filter(Boolean).join('\n\n')
  const source: MaterialSource = { kind: MATERIAL_SOURCE, form: 'notice', summary, units: bundle?.units ?? [], items: bundle?.items ?? [] }
  return createUserMessage({
    content: [{ type: 'text', text: `<教材材料>\n（系统按学生的 @ 引用附上的教材原文，不是学生写的话。）\n\n${body}\n</教材材料>` }],
    source,
  })
}

function failureMessage(reason: string): UserMessage {
  const source: MaterialSource = { kind: MATERIAL_SOURCE, form: 'notice', summary: '教材材料读取失败', units: [], items: [] }
  return createUserMessage({
    content: [{ type: 'text', text: `<教材材料>\n（读取失败：${reason}。本轮没有附上教材原文，回答时要告诉学生。）\n</教材材料>` }],
    source,
  })
}

/** 学生本轮亲手写的消息里的 `@` 引用（工具结果、系统注入的文字里出现 @ 不算）。 */
function userRefTokens(messages: readonly UserMessage[]): string[] {
  const tokens: string[] = []
  for (const message of messages) {
    if (message.source.kind !== 'user') continue
    for (const block of message.content) {
      if (block.type === 'text') for (const t of refTokens(block.text)) if (!tokens.includes(t)) tokens.push(t)
    }
  }
  return tokens
}

export async function apply(ctx: Context, config: Config): Promise<void> {
  const sandboxProblem = await ctx.hlmbMaterial.sandbox
  const manim = ctx.hlmbMaterial.manim
  const manimProblem = manim ? await manim.ready : '没有配置 manimPython'
  const rules = await prompt('rules.md')
    + (sandboxProblem ? '' : `\n${await prompt('python.md')}`)
    + (manimProblem ? '' : `\n${await prompt('manim.md')}`)

  ctx.effect(() => ctx.systemPrompt.section({
    name: PERSONA_SECTION,
    order: ctx.systemPrompt.getSectionOrder('DEPLOYMENT_PERSONA_PREFIX'),
    text: rules,
    interpolate: false,
    complete: true,
  }), 'hlmb: tutor rules')
  ctx.effect(() => ctx.systemPrompt.suppressRuntimeContext(), 'hlmb: no runtime context')

  /** 对话里仍然可见的材料（被压缩掉的不算，下次引用时重新附上）。 */
  const seen = (agent: Agent): { units: Set<string>; items: Set<string> } => {
    const state = ctx.sessionProjections.stateOf(agent.session, PROJECTION_KEY)
    const visible = new Set<number>(agent.session.surface.nodes)
    const keep = (rec: Record<string, number> = {}): Set<string> =>
      new Set(Object.entries(rec).filter(([, seq]) => visible.has(seq)).map(([k]) => k))
    return { units: keep(state?.units), items: keep(state?.items) }
  }

  const own: string[] = []
  const register = (def: ToolDefinition, label: string): void => {
    own.push(def.name)
    ctx.effect(() => ctx.tools.register(def), label)
  }

  const textOutput = { schema: { type: 'string' }, render: (_args: unknown, value: string) => [{ type: 'text' as const, text: value }] } as const

  register(defineTool({
    name: 'textbook_outline',
    description: `看教材的结构：不填 scope 时列出全部分册和单元；scope 是分册号（如 L）时列出各单元的小节；scope 是单元号（如 L8）时列出小节、例题、题目和页码。用来弄清「有什么、在哪」，再用 textbook_read 读原文。`,
    parameters: {
      scope: { type: 'string', description: '分册号或单元号；不填看全书。分册号和单元号同名（如 C1）时指分册，单元写成 C1/C1' },
    },
    output: textOutput,
    isConcurrencySafe: () => true,
    async execute(args) {
      return outline(await ctx.hlmbMaterial.load(), args.scope || undefined)
    },
    presentCall: (args) => ({ card: 'generic', title: `查目录${(args as { scope?: string }).scope ? `：${(args as { scope: string }).scope}` : ''}`, kind: 'search' }),
  }), 'hlmb: outline tool')

  register(defineTool({
    name: 'textbook_search',
    description: `在教材里按关键词定位，返回相关片段和引用（不返回全文）。语料分五类：讲义（按小节）、速记、题目、例题、答案。多个关键词用空格隔开，优先返回同时包含全部关键词的。找到后用 textbook_read 读方括号里的引用。`,
    parameters: {
      query: { type: 'string', required: true, description: '关键词，如「过渡矩阵 坐标」' },
      scope: { type: 'string', description: '只在某分册（如 L）或某单元（如 L8）里找；分册号和单元号同名（如 C1）时指分册，单元写成 C1/C1' },
      kinds: { type: 'array', items: { type: 'string', enum: [...DOC_KINDS] }, description: '只找这几类' },
      limit: { type: 'integer', description: '最多返回几处，默认 8，最多 20' },
    },
    output: textOutput,
    isConcurrencySafe: () => true,
    async execute(args) {
      return search(await ctx.hlmbMaterial.load(), args.query, { scope: args.scope || undefined, kinds: args.kinds, limit: args.limit })
    },
    presentCall: (args) => ({ card: 'generic', title: `查教材：${(args as { query?: string }).query ?? ''}`, kind: 'search' }),
  }), 'hlmb: search tool')

  register(defineTool({
    name: 'textbook_read',
    description: `按引用读教材原文。${REF_HELP}。题号会连同官方答案、验算记录和前置题一起给出；整个单元的讲义很长，只需要一部分时读小节。`,
    parameters: {
      ref: { type: 'string', required: true, description: '一个引用，如 L8-05、L/140、L8§3' },
    },
    output: textOutput,
    isConcurrencySafe: () => true,
    async execute(args, exec) {
      return read(await ctx.hlmbMaterial.load(), args.ref, exec.agent ? seen(exec.agent).units : undefined)
    },
    presentCall: (args) => ({ card: 'generic', title: `读教材：${(args as { ref?: string }).ref ?? ''}`, kind: 'read' }),
  }), 'hlmb: read tool')

  /** 本轮模型能不能看图：路由的模型声明了图片输入才附图，否则图片块会让纯文本模型的请求失败。 */
  const seesImages = async (exec: { agent?: Agent; signal: AbortSignal }): Promise<boolean> => {
    const routed = exec.agent?.session.requestHeader()?.config
    const provider = routed?.provider ?? exec.agent?.options.provider
    const model = routed?.model ?? exec.agent?.options.model
    const llm = ctx.get('llm') as Llm | undefined
    if (!provider || !model || !llm) return false
    const info = await llm.resolveModelInfo(provider, model, exec.signal).catch(() => undefined)
    return info?.inputModalities?.includes('image') ?? false
  }

  /** 每个会话本轮里各标题已经渲染了几次；学生发来新消息时清零（见下面的 agent/pre-step）。 */
  const renders = new WeakMap<object, Map<string, number>>()

  if (manim && !manimProblem) {
    const imageSchema = {
      type: 'object', additionalProperties: false,
      properties: {
        attachmentId: { type: 'string', required: true },
        mediaType: { type: 'string', enum: ['image/png'], required: true },
        bytes: { type: 'integer', required: true },
        width: { type: 'integer', required: true },
        height: { type: 'integer', required: true },
        name: { type: 'string' },
      },
    } as const
    register(defineTool({
      name: 'manim',
      description: '用 Manim（3Blue1Brown 做视频用的数学动画库）画图或做动画，在服务器上渲染，学生会在回答里直接看到。code 写法、风格和自查方法见系统提示里的「画图」一节。',
      parameters: {
        title: { type: 'string', required: true, description: '图的标题，显示在图下方；重画同一张图时保持不变' },
        code: { type: 'string', required: true, description: '完整的场景代码：定义 class Main(Scene)，在 construct 里画；不用写 import' },
        animate: { type: 'boolean', description: 'true 输出动画（MP4）；省略或 false 只输出最后一帧的静态图（PNG），中间的 self.play 过程都看不到' },
      },
      output: {
        schema: { type: 'object', additionalProperties: false, properties: { text: { type: 'string', required: true }, image: imageSchema } },
        render: (_args, value) => [
          { type: 'text' as const, text: value.text },
          ...(value.image ? [{ type: 'image' as const, attachment: value.image as never }] : []),
        ],
      },
      isConcurrencySafe: () => true,
      async execute(args, exec) {
        // 光看动画看不出在干什么：没有分步说明的动画不渲染（检查在渲染之前，不占重画次数）
        const says = args.code.match(/\bself\.say\(/g)?.length ?? 0
        const plays = args.code.match(/\bself\.play\(/g)?.length ?? 0
        if (args.animate === true && says === 0) {
          throw new Error('动画要配分步说明：在每段要讲的 self.play(...) 之前写一句 self.say("这一步在看什么")，3～6 步，学生在视频下方逐步看到。改好再画。')
        }
        // 写了好几段动画和分步说明却没开 animate：静态图只留最后一帧，说明里讲的变化学生看不到
        if (args.animate !== true && says >= 2 && plays >= 2) {
          throw new Error(`代码里有 ${plays} 段 self.play 和 ${says} 步说明，但 animate 没有设为 true，渲染出来只是最后一帧的静态图，说明里讲的变化学生看不到。要展示过程就加上 animate: true 重画；只要一张图就把 self.play 换成 self.add，说明改成描述最终画面。`)
        }
        const session = exec.agent?.session
        const counts = session ? renders.get(session) ?? new Map<string, number>() : undefined
        if (session && counts) renders.set(session, counts)
        const n = counts?.get(args.title) ?? 0
        if (n >= MAX_RENDERS) {
          throw new Error(`「${args.title}」这一轮已经渲染了 ${n} 次，不能再重画。用学生已经看到的最新一张接着讲；图上还有不影响理解的小瑕疵，可以在正文里提醒一句。`)
        }
        counts?.set(args.title, n + 1)
        const r = await manim.render({ code: args.code, animate: args.animate === true }, exec.signal)
        exec.signal.throwIfAborted()
        if (!r.ok) throw new Error(r.internal ? `画图环境出了问题，这次画不了：${r.error}` : `图没有画出来，请改正代码后重画：\n${r.error}`)
        const attachments = ctx.get('attachments') as Attachments | undefined
        const see = attachments !== undefined && await seesImages(exec)
        let image: ImageValue | undefined
        if (see) {
          const file = join(manim.mediaDir, r.animate ? `${r.id}-sheet.png` : `${r.id}.png`)
          const ref = await attachments.saveImage({ data: await readFile(file), mediaType: 'image/png', name: `${r.id}.png` }).catch(() => undefined)
          if (ref) image = { attachmentId: ref.attachmentId, mediaType: 'image/png', bytes: ref.bytes, width: ref.width, height: ref.height, name: `${r.id}.png` }
        }
        return { text: describeRender(r, args.title, image !== undefined), ...(image ? { image } : {}) }
      },
      presentCall: (args) => ({ card: 'generic', title: `画图：${(args as { title?: string }).title ?? ''}`, kind: 'other' }),
    }), 'hlmb: manim tool')
  }

  if (!sandboxProblem) {
    register(defineTool({
      name: 'python',
      description: '在隔离环境里运行一段 Python 3 代码（无网络、看不到任何文件、有时间和内存上限），返回它 print 的内容。可用 sympy、numpy、fractions。',
      parameters: {
        code: { type: 'string', required: true, description: '完整的 Python 代码，用 print 输出结果' },
      },
      output: {
        schema: { type: 'string' },
        render: (_args, value) => [{ type: 'text', text: value }],
      },
      isConcurrencySafe: () => true,
      async execute(args, exec) {
        const r = await runPython(args.code, {
          timeoutMs: config.pythonTimeoutMs,
          memoryBytes: config.pythonMemoryMB * 1024 * 1024,
          outputChars: PYTHON_OUTPUT_CHARS,
          signal: exec.signal,
        })
        exec.signal.throwIfAborted()
        if (r.timedOut) throw new Error(`运行超过 ${config.pythonTimeoutMs / 1000} 秒，被终止。${r.stdout ? `\n已输出：\n${r.stdout}` : ''}`)
        if (r.exitCode !== 0) throw new Error(`运行出错（退出码 ${r.exitCode}）：\n${r.stderr || r.stdout}`)
        return r.stdout || '（没有输出：记得用 print 打印结果）'
      },
      presentCall: () => ({ card: 'generic', title: '计算', kind: 'execute' }),
    }), 'hlmb: python tool')
  }

  // 只留答疑自己的工具和联网工具：宿主全局注册的其他工具（如 working_directory、读写文件）对学生没有意义。
  // restrict 在 preset 作用域校验名字、在 agent 作用域生效，preset 自己的工具两边身份不同，
  // allow 白名单两头都不对，所以按名字 deny 掉启动时已有的全局工具。
  const globals = ctx.tools.schemas().map((t) => t.name).filter((n) => !own.includes(n) && !WEB_TOOLS.includes(n) && n !== 'run_code')
  if (globals.length) ctx.effect(() => ctx.tools.restrict({ deny: globals }), 'hlmb: no host tools')

  ctx.on('agent/pre-step', async ({ agent, messages, signal }, next): Promise<PreStepDecision> => {
    if (messages.some((m) => m.source.kind === 'user')) renders.delete(agent.session)
    const decision = await next()
    if (decision.kind === 'reject') return decision
    const tokens = userRefTokens(messages)
    if (tokens.length === 0) return decision
    let injected: UserMessage
    try {
      const material = await ctx.hlmbMaterial.load()
      signal.throwIfAborted()
      const refs = tokens.flatMap((t) => material.resolve(t) ?? [])
      const missing = tokens.filter((t) => !material.resolve(t))
      const bundle = material.bundle(refs, seen(agent))
      if (!bundle && missing.length === 0) return decision
      injected = materialMessage(bundle, missing)
    } catch (err) {
      if (signal.aborted) throw err
      ctx.logger.warn('教材材料读取失败：%s', err)
      injected = failureMessage(err instanceof Error ? err.message : String(err))
    }
    return { ...decision, messages: [injected, ...decision.messages] }
  })
}

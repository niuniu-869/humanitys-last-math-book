/** 宿主插件和 agent 插件共用的名字、类型与服务声明。 */
import { z } from 'zod'
import type {} from '@deepseek-ai/dsh-session-projection'
import type { ManimRenderer } from './manim.ts'
import type { Material } from './material.ts'

/** 教材材料消息的 `source.kind`。 */
export const MATERIAL_SOURCE = 'hlmb-material'
/** 记录已附上材料的会话投影。 */
export const PROJECTION_KEY = 'hlmb-tutor/material'

export interface MaterialService {
  load(): Promise<Material>
  /** 进程启动时实测一次 Python 沙箱；可用时为 undefined，不可用时是原因。 */
  sandbox: Promise<string | undefined>
  /** Manim 画图；没有配置 manimPython 时为 undefined。可不可用看 `manim.ready`。 */
  manim: ManimRenderer | undefined
}

/** 单元键（`分册/单元`）和题号 → 最近一次附上它的材料消息的事件序号。 */
export interface SeenState {
  units: Record<string, number>
  items: Record<string, number>
}

export const seenStateSchema = z.object({
  units: z.record(z.string(), z.number()),
  items: z.record(z.string(), z.number()),
})

export interface MaterialSource {
  kind: typeof MATERIAL_SOURCE
  form: 'notice'
  summary: string
  units: string[]
  items: string[]
}

declare module '@deepseek-ai/cordis' {
  interface Context {
    hlmbMaterial: MaterialService
  }
}

declare module '@deepseek-ai/dsh-llm' {
  interface MessageSourceMap {
    'hlmb-material': MaterialSource
  }
}

declare module '@deepseek-ai/dsh-session-projection/types' {
  interface SessionProjectionStateMap {
    'hlmb-tutor/material': SeenState
  }
}

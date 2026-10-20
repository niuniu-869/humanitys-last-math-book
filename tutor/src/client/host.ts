/**
 * 浏览器端用到的 dsh 宿主接口（0.2.1-rc.2）。
 *
 * dsh 的插件文档要求插件不要把 dsh 客户端包当模块引用（接口会变、组件抛错会让整个插槽空白），
 * 所以这里按结构只声明本插件用到的字段，每段注明出处，升级 dsh 时对照这些出处核对。
 */
import type { ComponentType } from 'react'

/** dsh-client-ui-chat `UseDisclosure`：每个工具行自己的展开状态，随所在回合一起重置。 */
export type UseDisclosure = () => { readonly expanded: boolean; readonly setExpanded: (open: boolean) => void; readonly toggle: () => void }

/** dsh-client-ui-conversation `ToolResultNode` 中用到的字段。 */
export interface ToolResult {
  readonly callId: string
  readonly call: { readonly name: string; readonly argsRaw: string } | null
  readonly content: readonly { readonly type: string; readonly text?: string }[]
  readonly isError: boolean
  readonly error?: { readonly name: string; readonly code: string; readonly reason?: string }
}

/** dsh-client-ui-tool `tool.call.toolview` 插槽的属性：同一次调用依次经历 preparing → start → result。 */
export type ToolViewProps = { readonly callId: string; readonly toolName: string; readonly useDisclosure: UseDisclosure } & (
  | { readonly phase: 'preparing'; readonly block: { readonly callId: string } }
  | { readonly phase: 'start'; readonly block: { readonly callId: string; readonly argsRaw: string } }
  | { readonly phase: 'result'; readonly block: ToolResult })

/** dsh-client-ui-conversation `InputActions`：会话作用域插槽都会收到它，用来往输入框里插字。 */
export interface InputActions {
  /** 记下当前光标位置和草稿版本。 */
  captureInsertion(): unknown
  /** 在记下的位置插入文字；草稿在此期间变了或正在发送时返回 false。 */
  insertText(text: string, span: unknown): boolean
}

/** dsh-client-ui-sidebar-right `SidebarRightTabInfo` 中用到的字段。 */
export interface TabInfo {
  readonly sidebar: { readonly expanded: boolean; readonly fullscreen: boolean }
  readonly tab: { readonly visible: boolean; readonly navigation: { readonly params: unknown; readonly revision: number } }
}

/** dsh-client-ui-sidebar-right `ISidebarRight`（`ctx.sidebarRight`）。 */
export interface SidebarRight {
  openTab(kind: string, options?: { readonly params?: unknown }): void
  isExpanded(): boolean
  toggleExpanded(): void
}

/** dsh-client-ui-input-trigger `InputTriggerCandidate`。 */
export interface TriggerCandidate {
  readonly name: string
  readonly label?: string
  readonly description?: string
  readonly icon?: 'file' | 'folder' | 'session'
  readonly hint?: string
  readonly section?: string
  readonly value?: string
}

/** dsh-client-ui-conversation `ReferenceInsert`：补全选中后插进输入框的引用芯片。 */
export interface ReferenceInsert {
  readonly source: string
  /** 发出去的原文，含 @。 */
  readonly ref: string
  readonly label: string
  readonly appearance: 'file' | 'folder' | 'session'
  readonly clipboardText: string
}

interface SessionRef { readonly sessionId: string }

/** dsh-client-ui-input-trigger `InputTriggerSource` 中用到的部分。 */
export interface TriggerSource {
  readonly trigger: '@'
  readonly name: string
  readonly order?: number
  readonly showGroupTitle?: boolean
  candidates(session: SessionRef, req: { readonly query: string; readonly signal: AbortSignal }): Promise<readonly TriggerCandidate[]>
  onPick(pick: { readonly candidate: TriggerCandidate }): { readonly insert: ReferenceInsert } | undefined
  warm?(session: SessionRef): void
  lexicon?(session: SessionRef): readonly string[] | undefined
  subscribeLexicon?(session: SessionRef, listener: () => void): () => void
  openReference?(session: SessionRef, reference: { readonly ref: string; readonly appearance?: string }): boolean
  readonly codec: { clipboardText(ref: string): string; serialize(ref: string, signal: AbortSignal): Promise<string> }
}

/** dsh-client-ui-conversation `UserTextRule`：用户气泡里的文字按规则切出业务节点。 */
export interface UserTextRule<Id extends string, Data> {
  readonly id: Id
  readonly order: number
  match(text: string, from: number): { readonly id: Id; readonly start: number; readonly end: number; readonly data: Data } | undefined
}

/** `conversation.user.text.node` 插槽的属性。 */
export interface UserTextNodeProps<Data> {
  readonly node: { readonly data: Data }
  /** 原文。 */
  readonly raw: string
  /** 气泡里可点；草稿预览等场景为 false。 */
  readonly interactive: boolean
}

interface SlotSpec { readonly name: string; readonly key?: string; readonly priority?: number }

/** 本插件用到的客户端上下文。 */
export interface ClientContext {
  readonly slots: {
    inject(name: string, fn: () => unknown): void
    register(spec: SlotSpec, component: ComponentType<never>): unknown
  }
  readonly sidebarRightTabs: { register(def: unknown): () => void }
  readonly sidebarRight: SidebarRight
  readonly inputTriggers: { registerSource(src: TriggerSource): () => void }
  readonly uiConversation: { readonly userText: { register(rule: UserTextRule<string, unknown>): unknown } }
  readonly locale: import('./welcome.tsx').LocaleRuntime
  effect(fn: () => unknown, label?: string): void
}

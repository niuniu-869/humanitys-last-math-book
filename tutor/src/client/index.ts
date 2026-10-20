/**
 * 浏览器端：
 * - 工具在对话里的样子：查教材三件套和计算是一行（可展开），画图（manim）是始终展开的图卡；
 * - 右侧「教材」面板；
 * - `@` 补全「教材」和用户气泡里的引用芯片；
 * - 欢迎页的文案和大肥鱼图标。
 * 工具名（manim、textbook_read 等）是与 ../agent.ts 之间的协议，两边要一致。
 */
import { createBookTab } from './BookTab.tsx'
import type { BookTarget } from './catalog.ts'
import type { ClientContext } from './host.ts'
import { createLookupViews, PythonRow } from './LookupRows.tsx'
import { ManimCard } from './ManimCard.tsx'
import { createRefChip, createRefSource, refRule, RULE_ID } from './references.tsx'
import { HeroMark, installCopy } from './welcome.tsx'

export const inject = ['slots', 'sidebarRightTabs', 'sidebarRight', 'inputTriggers', 'uiConversation', 'locale']

const BOOK_TAB = 'dsh-plugin-humanitys-last-math-book/book'
const BOOK_KIND = 'hlmb-book'

export function apply(ctx: ClientContext): void {
  const openBook = (target: BookTarget): void => {
    try {
      ctx.sidebarRight.openTab(BOOK_KIND, { params: target })
    } catch (err) {
      console.warn('[hlmb-tutor] 打开教材面板失败', err)
    }
  }

  const toolViews = { manim: ManimCard, python: PythonRow, ...createLookupViews(openBook) }
  ctx.slots.inject('tool.call.toolview', function* () {
    for (const [key, view] of Object.entries(toolViews)) yield ctx.slots.register({ name: 'tool.call.toolview', key }, view as never)
  })

  ctx.effect(() => ctx.sidebarRightTabs.register({
    id: BOOK_TAB, kind: BOOK_KIND, priority: 'extension', title: () => '教材',
    guide: [{ id: BOOK_KIND, order: 5, title: () => '教材', description: () => '对照原书翻页，点题号直接提问' }],
  }), 'hlmb: book tab type')
  const BookTab = createBookTab(ctx.sidebarRight)
  ctx.slots.inject('sidebar.right.pane.tab', () => ctx.slots.register({ name: 'sidebar.right.pane.tab', key: BOOK_TAB }, BookTab as never))

  ctx.effect(() => ctx.inputTriggers.registerSource(createRefSource(openBook)), 'hlmb: @ source')
  ctx.uiConversation.userText.register(refRule)
  const RefChip = createRefChip(openBook)
  ctx.slots.inject('conversation.user.text.node', () => ctx.slots.register({ name: 'conversation.user.text.node', key: RULE_ID, priority: 100 }, RefChip as never))

  // 文案只是锦上添花：语言包注册失败（如 dsh 改了语言包接口）时保留 dsh 原文，不能连累整个插件
  try {
    installCopy(ctx.locale, (fn, label) => ctx.effect(fn, label))
  } catch (err) {
    console.warn('[hlmb-tutor] 答疑版文案没有装上，沿用 dsh 原文', err)
  }
  ctx.slots.inject('conversation.hero.brand.mark', () => ctx.slots.register({ name: 'conversation.hero.brand.mark', priority: 100 }, HeroMark as never))
}

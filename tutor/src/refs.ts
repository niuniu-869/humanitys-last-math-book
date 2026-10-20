/** `@` 引用的写法，服务端（取材）和浏览器端（补全、芯片）共用；不依赖 Node。 */

/**
 * 题号（L8-05）、例题和随堂练习（Z1·例01、L8·练03）、单元（L8）或「分册/页码」（L/140）。
 * 前面不能紧跟字母数字，避免把邮箱当引用；后面紧跟中文或标点也能切开。
 */
export const REF_TOKEN = /(?<![A-Za-z0-9_.])@([A-Za-z0-9-]+(?:·[例练]\d+|\/\d+)?)/g

export function refTokens(text: string): string[] {
  return [...text.matchAll(REF_TOKEN)].map((m) => m[1]!)
}

/** 页码引用拆成分册和页码；不是页码引用时返回 undefined。 */
export function pageRef(token: string): { book: string; page: number } | undefined {
  const m = /^([A-Za-z0-9-]+)\/(\d+)$/.exec(token)
  return m ? { book: m[1]!, page: Number(m[2]) } : undefined
}

/** 线框图标：16 格画布、1px 描边、currentColor，与 dsh 工具行的图标同一套画法。 */
import type { ReactNode } from 'react'

const PATHS = {
  book: <><path d="M8 3.5C6.5 2.6 4.6 2.3 2 2.5v9.5c2.6-.2 4.5.1 6 1 1.5-.9 3.4-1.2 6-1V2.5c-2.6-.2-4.5.1-6 1Z" /><path d="M8 3.5V13" /></>,
  search: <><circle cx="7" cy="7" r="4.25" /><path d="m10.25 10.25 3.5 3.5" /></>,
  read: <><path d="M3.5 1.5h6l3 3v10h-9z" /><path d="M9.5 1.5v3h3M5.5 8h5M5.5 10.5h5" /></>,
  outline: <><path d="M5.5 3.5h8M5.5 8h8M5.5 12.5h8" /><circle cx="2.75" cy="3.5" r=".75" /><circle cx="2.75" cy="8" r=".75" /><circle cx="2.75" cy="12.5" r=".75" /></>,
  code: <><rect x="1.5" y="2.5" width="13" height="11" rx="1.5" /><path d="m4.5 6.5 2 1.75-2 1.75M8 10.5h3.5" /></>,
  plot: <><path d="M2.5 1.5v12h12" /><path d="M4 11c2-6 4.5-7.5 9-8" /></>,
  alert: <><circle cx="8" cy="8" r="6.5" /><path d="M8 4.5v4.25M8 11v.5" /></>,
  down: <path d="M4 6l3.3 3.3a1 1 0 0 0 1.4 0L12 6" />,
  up: <path d="M12 10 8.7 6.7a1 1 0 0 0-1.4 0L4 10" />,
  left: <path d="M10 4 6.7 7.3a1 1 0 0 0 0 1.4L10 12" />,
  right: <path d="m6 4 3.3 3.3a1 1 0 0 1 0 1.4L6 12" />,
  ask: <><path d="M2.5 3.5a1 1 0 0 1 1-1h9a1 1 0 0 1 1 1v6.5a1 1 0 0 1-1 1H7l-3 2.5v-2.5h-.5a1 1 0 0 1-1-1z" /><path d="M6.5 6h3M6.5 8h2" /></>,
} satisfies Record<string, ReactNode>

export type IconName = keyof typeof PATHS

export function Icon({ name, size = 14, className }: { name: IconName; size?: number; className?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth={1}
      strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" className={className}>
      {PATHS[name]}
    </svg>
  )
}

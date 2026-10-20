import { describe, expect, it } from 'vitest'
import { foldSeen } from '../src/index.ts'
import { seenStateSchema } from '../src/shared.ts'

const empty = { units: {}, items: {} }
const material = (seq: number, units: string[], items: string[]) =>
  ({ type: 'user/message', seq, data: { source: { kind: 'hlmb-material', form: 'notice', summary: '', units, items } } })

describe('foldSeen', () => {
  it('无关事件原样返回同一个引用', () => {
    expect(foldSeen(empty, { type: 'assistant/message', seq: 1, data: {} })).toBe(empty)
    expect(foldSeen(empty, { type: 'user/message', seq: 2, data: { source: { kind: 'user' } } })).toBe(empty)
  })

  it('记下最近一次附上的事件序号', () => {
    const a = foldSeen(empty, material(3, ['L42/L8'], ['L8-05']))
    const b = foldSeen(a, material(9, [], ['L8-05', 'L8-06']))
    expect(b).toEqual({ units: { 'L42/L8': 3 }, items: { 'L8-05': 9, 'L8-06': 9 } })
    expect(seenStateSchema.parse(b)).toEqual(b)
  })

  it('来源字段损坏时跳过，不抛错', () => {
    const bad = { type: 'user/message', seq: 4, data: { source: { kind: 'hlmb-material', units: 'L8', items: [1, 'L8-01'] } } }
    expect(foldSeen(empty, bad)).toEqual({ units: {}, items: { 'L8-01': 4 } })
  })
})

import { describe, expect, it } from 'vitest'
import { describeRef } from '../src/client/catalog.ts'
import { candidates, refRule } from '../src/client/references.tsx'
import { Material } from '../src/material.ts'
import { fixtureIndex } from './fixture.ts'

const catalog = () => new Material(fixtureIndex(), ['L42']).catalog()

describe('describeRef（浏览器端解析，与服务端同序：单元 → 页码 → 条目）', () => {
  it('题号翻到题目页，例题标签带题干，页码和单元也能翻', () => {
    expect(describeRef(catalog(), 'L8-05')).toMatchObject({ kind: 'item', label: 'L8-05', target: { book: 'L42', page: 4 } })
    expect(describeRef(catalog(), 'L8·例01')?.detail).toContain('子空间的例子')
    expect(describeRef(catalog(), 'L42/3')).toMatchObject({ kind: 'page', label: 'L42 第 3 页', target: { book: 'L42', page: 3 } })
    expect(describeRef(catalog(), 'L8')).toMatchObject({ kind: 'unit', target: { book: 'L42', page: 2 } })
  })
  it('越界页码、白名单外的题、目录没到时都认不出', () => {
    expect(describeRef(catalog(), 'L42/7')).toBeUndefined()
    expect(describeRef(catalog(), 'L8-07')).toBeUndefined()
    expect(describeRef(undefined, 'L8-05')).toBeUndefined()
  })
})

describe('@ 补全候选', () => {
  it('空输入列出全部单元', () => {
    expect(candidates(catalog(), '').map((c) => c.name)).toEqual(['L8', 'L9'])
  })
  it('题号前缀优先，单元号前缀排最前', () => {
    const names = candidates(catalog(), 'l8').map((c) => c.name)
    expect(names[0]).toBe('L8')
    expect(names).toEqual(expect.arrayContaining(['L8-04', 'L8-05', 'L8·例01']))
    expect(names).not.toContain('L9-01')
  })
  it('按例题题干和单元名里的中文搜', () => {
    expect(candidates(catalog(), '子空间').map((c) => c.name)).toEqual(['L8', 'L8·例01'])
  })
  it('分册/页码列出页', () => {
    expect(candidates(catalog(), 'L42/').map((c) => c.name)).toEqual(['L42/1', 'L42/2', 'L42/3', 'L42/4', 'L42/5', 'L42/6'])
    expect(candidates(catalog(), 'L42/4')[0]).toMatchObject({ name: 'L42/4', description: 'L8-05' })
  })
})

describe('用户气泡里的引用切分', () => {
  it('从 from 起找下一个引用，邮箱不算', () => {
    const text = '发到 a@b.com，看 @L8-05 和@L42/140页'
    const first = refRule.match(text, 0)!
    expect(text.slice(first.start, first.end)).toBe('@L8-05')
    const second = refRule.match(text, first.end)!
    expect(second.data.ref).toBe('L42/140')
    expect(refRule.match(text, second.end)).toBeUndefined()
  })
})

import { describe, expect, it } from 'vitest'
import { outline, read, search } from '../src/lookup.ts'
import { type Index, Material, splitSections } from '../src/material.ts'
import { fixtureIndex } from './fixture.ts'

const m = (): Material => new Material(fixtureIndex(), ['L42'])

describe('splitSections', () => {
  it('开篇、编号小节、本章小结；四级标题留在所属小节里', () => {
    const s = splitSections(fixtureIndex().units['L42/L8']!.lesson)
    expect(s.map((x) => [x.key, x.title])).toEqual([['0', '开篇'], ['1', '1. 什么是子空间？'], ['2', '2. 交与并'], ['小结', '本章小结']])
    expect(s[1]!.text).toContain('#### 三类子空间')
  })
})

describe('引用解析', () => {
  it('单元、小节、速记表；不存在的小节和白名单外的分册不算', () => {
    const x = m()
    expect(x.resolve('L8')).toEqual({ kind: 'unit', book: 'L42', unit: 'L8' })
    expect(x.resolve('L8§2')).toEqual({ kind: 'section', book: 'L42', unit: 'L8', section: '2' })
    expect(x.resolve('L8§速记')).toEqual({ kind: 'section', book: 'L42', unit: 'L8', section: '速记' })
    expect(x.resolve('L8§9')).toBeUndefined()
    expect(x.resolve('L7§1')).toBeUndefined()
  })

  it('@ 单元会附上整个单元的讲义', () => {
    const x = m()
    const b = x.bundle([x.resolve('L8')!], { units: new Set(), items: new Set() })!
    expect(b.units).toEqual(['L42/L8'])
    expect(b.items).toEqual([])
    expect(b.text).toContain('两个子空间的交集仍是子空间')
  })
})

describe('outline', () => {
  it('全书：分册和单元', () => {
    expect(outline(m())).toBe('L42《线性代数》，6 页\n  - L8：L.8 · 子空间\n  - L9：基与维数')
  })

  it('分册：各单元的小节引用', () => {
    const text = outline(m(), 'L42')
    expect(text).toContain('    - L8§1：1. 什么是子空间？')
    expect(text).toContain('    - L8§小结：本章小结')
  })

  it('单元：小节、例题、题目和页码，不含别的册错挂的条目', () => {
    const text = outline(m(), 'L8')
    expect(text).toContain('L8§2：2. 交与并（')
    expect(text).toContain('L8§速记：速记表')
    expect(text).toContain('例题：\n  - L8·例01：例 1：子空间的例子（L42 第 2 页）')
    expect(text).toContain('  - L8-05：L8-05〔B〕（L42 第 4 页）')
    expect(text).not.toContain('L8-07')
  })

  it('范围写错时说明有哪些分册', () => {
    expect(() => outline(m(), 'W3')).toThrow(/分册有：L42/)
  })
})

describe('search', () => {
  it('多个关键词同时命中的排在前面，结果带引用、类别、标题和片段', () => {
    const text = search(m(), '子空间 零向量')
    const lines = text.split('\n')
    expect(lines[0]).toMatch(/^共 \d+ 处/)
    expect(lines[1]).toBe('1. [L8§1] 讲义 · L.8 · 子空间 › 1. 什么是子空间？')
    expect(lines[2]).toContain('必含零向量')
  })

  it('题目命中时带页码；答案单独成一类', () => {
    expect(search(m(), '交与并')).toContain('[L8-05] 题目 · L8-05〔B〕（L42 第 4 页）')
    expect(search(m(), '答案五', { kinds: ['答案'] })).toContain('[L8-05] 答案 · L8-05 的答案（L42 第 6 页）')
  })

  it('全部关键词同时命中的一处都没有时，退回部分命中并说明', () => {
    expect(search(m(), '交集 不存在的词')).toMatch(/^没有同时包含全部关键词的结果/)
    expect(search(m(), '完全不存在')).toMatch(/^没有找到「完全不存在」/)
  })

  it('按范围和类别过滤；参数写错时报错', () => {
    expect(search(m(), '子空间', { scope: 'L9' })).toMatch(/^没有找到/)
    expect(search(m(), '子空间', { kinds: ['速记'] })).toContain('[L8§速记] 速记')
    expect(() => search(m(), '子空间', { kinds: ['笔记'] })).toThrow(/kinds 只能取/)
    expect(() => search(m(), '子空间', { scope: 'X1' })).toThrow(/不是分册号也不是单元号/)
    expect(() => search(m(), '  ')).toThrow(/不能为空/)
  })

  it('limit 截断结果数', () => {
    const text = search(m(), '子空间', { limit: 1 })
    expect(text.split('\n').filter((l) => /^\d+\. /.test(l))).toHaveLength(1)
  })
})

describe('read', () => {
  it('题号：题目、答案、验算、前置题和页码', () => {
    const text = read(m(), 'L8-05')
    expect(text).toContain('答案五')
    expect(text).toContain('## 前置题 L8-04')
    expect(text).toContain('（题目在 L42 第 4 页，答案在第 6 页）')
  })

  it('页码：页面文字和本页条目；可以带 @', () => {
    const text = read(m(), '@L42/4')
    expect(text).toContain('题 L8-05 所在页')
    expect(text).toContain('本页条目：L8-05（L8-05〔B〕）')
  })

  it('单元给全文；已在对话里时只给一句说明', () => {
    expect(read(m(), 'L8')).toContain('## 本单元速记表')
    expect(read(m(), 'L8', new Set(['L42/L8']))).toMatch(/已经在对话里/)
  })

  it('小节和速记表', () => {
    expect(read(m(), 'L8§2')).toBe('# L.8 · 子空间 › 2. 交与并\n\n### 2. 交与并\n\n两个子空间的交集仍是子空间，并集一般不是。')
    expect(read(m(), 'L8§速记')).toBe('# L.8 · 子空间 › 速记表\n\nL8 速记：子空间先看零向量')
  })

  it('找不到时给出引用写法', () => {
    expect(() => read(m(), 'L8-99')).toThrow(/找不到「L8-99」。引用写法/)
  })
})

describe('分册号和单元号同名（新仓库的 C1 册含 C1 单元）', () => {
  const index: Index = {
    books: { C1: { title: '微积分（一）', pdf: 'C1.pdf', pages: 2, units: ['C1', 'C2'], page_items: { '1': ['C1-01'], '2': ['C2-01'] }, page_text: ['极限', '导数'] } },
    items: {
      'C1-01': { kind: 'problem', book: 'C1', unit: 'C1', label: 'C1-01', md: '**C1-01** 求极限', answer: '1', pages: { problem: [1] } },
      'C2-01': { kind: 'problem', book: 'C1', unit: 'C2', label: 'C2-01', md: '**C2-01** 求极限的导数', answer: '0', pages: { problem: [2] } },
    },
    units: {
      'C1/C1': { title: 'C1 · 极限', lesson: '### 1. 极限\n\n极限的定义', problems_head: '', cheatsheet: '' },
      'C1/C2': { title: 'C2 · 导数', lesson: '### 1. 导数\n\n导数的定义', problems_head: '', cheatsheet: '' },
    },
  }
  const x = (): Material => new Material(index, [])

  it('引用里的 C1 指单元，C1/C1 也指单元，C1/2 是页码', () => {
    expect(x().resolve('C1')).toEqual({ kind: 'unit', book: 'C1', unit: 'C1' })
    expect(x().resolve('C1/C1')).toEqual({ kind: 'unit', book: 'C1', unit: 'C1' })
    expect(x().resolve('L42/C1')).toBeUndefined()
    expect(x().resolve('C1/2')).toMatchObject({ kind: 'page', book: 'C1', page: 2 })
  })

  it('查找范围里的 C1 指分册，单元写成 C1/C1', () => {
    expect(search(x(), '极限', { scope: 'C1' })).toContain('[C2-01]')
    expect(search(x(), '极限', { scope: 'C1/C1' })).not.toContain('[C2-01]')
    expect(outline(x(), 'C1')).toContain('C2：C2 · 导数')
    expect(outline(x(), 'C1/C1')).toMatch(/^C1：C1 · 极限（分册 C1）/)
  })
})

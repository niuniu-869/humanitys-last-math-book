import { mkdtemp, rm, utimes, writeFile } from 'node:fs/promises'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterEach, describe, expect, it } from 'vitest'
import { Material, materialLoader, prereqIds, refTokens, titleFor } from '../src/material.ts'
import { fixtureIndex } from './fixture.ts'

const none = { units: new Set<string>(), items: new Set<string>() }
const material = (): Material => new Material(fixtureIndex(), ['L42'])

describe('refTokens', () => {
  it('题号、例题号、页码，后面紧跟中文或标点也能切开', () => {
    expect(refTokens('看 @L8-05 和 @Z1·例01，还有@L42/140页')).toEqual(['L8-05', 'Z1·例01', 'L42/140'])
    expect(refTokens('@L8-05这题怎么做')).toEqual(['L8-05'])
  })
  it('邮箱和单独的 @ 不算引用', () => {
    expect(refTokens('发到 a@b.com 或者 @ 一下')).toEqual([])
  })
})

describe('prereqIds', () => {
  it('从「先做」里取出前置题号', () => {
    expect(prereqIds('〔B｜先做 L8-04、L8-03）〕')).toEqual(['L8-04', 'L8-03'])
    expect(prereqIds('没有前置')).toEqual([])
  })
})

describe('Material', () => {
  it('只认白名单分册，以及归属白名单分册的条目', () => {
    const m = material()
    expect(m.books()).toEqual([{ id: 'L42', title: '线性代数', pages: 6 }])
    expect(m.resolve('L8-07')).toBeUndefined()
    expect(m.resolve('W3/1')).toBeUndefined()
    expect(m.pageItems('L42', 4)).toEqual([{ id: 'L8-05', kind: 'problem', label: 'L8-05〔B〕' }])
  })

  it('白名单为空时用索引里的全部分册', () => {
    expect(new Material(fixtureIndex(), []).bookIds).toEqual(['L42', 'W3'])
  })

  it('解析题号和页码；页码越界或不是整数都不算', () => {
    const m = material()
    expect(m.resolve('L8-05')).toEqual({ kind: 'item', id: 'L8-05', book: 'L42', unit: 'L8' })
    expect(m.resolve('L42/6')).toEqual({ kind: 'page', book: 'L42', page: 6, unit: 'L9' })
    expect(m.resolve('L42/3')).toEqual({ kind: 'page', book: 'L42', page: 3, unit: 'L8' })
    expect(m.resolve('L42/1')).toEqual({ kind: 'page', book: 'L42', page: 1, unit: undefined })
    expect(m.resolve('L42/0')).toBeUndefined()
    expect(m.resolve('L42/7')).toBeUndefined()
    expect(m.resolve('L8-99')).toBeUndefined()
  })

  it('例题去掉 label 尾巴上的分隔符', () => {
    expect(material().pageItems('L42', 2)).toEqual([{ id: 'L8·例01', kind: 'example', label: '例 1' }])
  })

  it('题目材料：讲义在前，题目、官方答案、验算、前置题在后', () => {
    const b = material().bundle([{ kind: 'item', id: 'L8-05', book: 'L42', unit: 'L8' }], none)!
    expect(b.units).toEqual(['L42/L8'])
    expect(b.items).toEqual(['L8-05'])
    const order = ['L8 讲义全文', 'L8 题目说明', 'L8 速记', '## 题目 L8-05', '答案五', '[l8] ok L8-05', '## 前置题 L8-04', '答案四']
      .map((s) => b.text.indexOf(s))
    expect(order.every((i) => i >= 0)).toBe(true)
    expect([...order].sort((a, c) => a - c)).toEqual(order)
    expect(b.summary).toBe('附上教材：L8 讲义、L8-05')
  })

  it('例题不带答案', () => {
    const text = material().itemBlock('L8·例01')
    expect(text).toContain('讲义例题 L8·例01（讲义小节：1. 子空间）')
    expect(text).not.toContain('官方答案')
  })

  it('页码材料带上整页文字和该页的条目，不带别的册错挂的条目', () => {
    const m = material()
    const b = m.bundle([m.resolve('L42/4')!], none)!
    expect(b.items).toEqual(['L8-05'])
    expect(b.text).toContain('分册 L42 第 4 页')
    expect(b.text).toContain('题 L8-05 所在页')
    expect(b.text).not.toContain('旧版的题')
  })

  it('已在对话里的单元和条目不重复附上；全都附过时返回 undefined', () => {
    const m = material()
    const refs = [m.resolve('L8-05')!, m.resolve('L8-05')!, m.resolve('L42/4')!]
    const first = m.bundle(refs, none)!
    expect(first.units).toEqual(['L42/L8'])
    expect(first.items).toEqual(['L8-05'])
    expect(first.text.match(/## 题目 L8-05/g)).toHaveLength(1)

    const seen = { units: new Set(first.units), items: new Set(first.items) }
    expect(m.bundle([m.resolve('L8-05')!], seen)).toBeUndefined()
    const next = m.bundle([m.resolve('L8-04')!], seen)!
    expect(next.units).toEqual([])
    expect(next.text).not.toContain('L8 讲义全文')
    expect(next.summary).toBe('附上教材：L8-04')
  })

  it('目录只含白名单分册的条目，页码取题目页或讲义页', () => {
    const c = material().catalog()
    expect(c.books[0]!.pageItems).toEqual({ '2': ['L8·例01'], '4': ['L8-05'], '5': ['L8-04'], '6': ['L9-01'] })
    expect(Object.keys(c.items).sort()).toEqual(['L8-04', 'L8-05', 'L8·例01', 'L9-01'])
    expect(c.items['L8·例01']).toEqual({ book: 'L42', unit: 'L8', kind: 'example', label: '例 1', page: 2, hint: '子空间的例子' })
    expect(c.books[0]!.units).toEqual([{ id: 'L8', title: 'L.8 · 子空间', page: 2 }, { id: 'L9', title: '基与维数', page: 6 }])
  })
})

describe('materialLoader', () => {
  let dir: string | undefined
  afterEach(async () => { if (dir) await rm(dir, { recursive: true }) })

  it('按修改时间缓存，文件更新后重新读取', async () => {
    dir = await mkdtemp(join(tmpdir(), 'hlmb-'))
    const file = join(dir, 'index.json')
    await writeFile(file, JSON.stringify(fixtureIndex()))
    const load = materialLoader(file, ['L42'])
    const a = await load()
    expect(await load()).toBe(a)
    expect(a.indexPath).toBe(file)

    const changed = fixtureIndex()
    changed.books.L42!.title = '线性代数（新）'
    await writeFile(file, JSON.stringify(changed))
    const later = new Date(Date.now() + 5000)
    await utimes(file, later, later)
    const b = await load()
    expect(b).not.toBe(a)
    expect(b.books()[0]!.title).toBe('线性代数（新）')
  })

  it('读取失败不缓存失败结果', async () => {
    dir = await mkdtemp(join(tmpdir(), 'hlmb-'))
    const file = join(dir, 'index.json')
    await writeFile(file, '{坏的 json')
    const load = materialLoader(file, ['L42'])
    await expect(load()).rejects.toThrow()
    await writeFile(file, JSON.stringify(fixtureIndex()))
    const later = new Date(Date.now() + 5000)
    await utimes(file, later, later)
    await expect(load()).resolves.toBeInstanceOf(Material)
  })
})

describe('会话标题', () => {
  it('题目用考查点，例题和没写考查点的题目用单元名', () => {
    const index = fixtureIndex()
    index.items['L8-05']!.label = 'L8-05〔B｜方法 1 · 考查：交与并的封闭性〕'
    const m = new Material(index, ['L42'])
    expect(m.titleOf('L8-05')).toBe('L8-05 交与并的封闭性')
    expect(m.titleOf('L8-04')).toBe('L8-04 子空间')
    expect(m.titleOf('L8·例01')).toBe('L8·例01 子空间')
  })

  it('页码、单元、小节', () => {
    const m = material()
    expect(m.titleOf('L42/4')).toBe('L42 第 4 页 子空间')
    expect(m.titleOf('L8')).toBe('L.8 · 子空间')
    expect(m.titleOf('L9')).toBe('基与维数')
    expect(m.titleOf('L8§2')).toBe('L8§2 交与并')
  })

  it('取消息里第一处有效引用', () => {
    expect(titleFor(material(), '@L8-99 不存在，@L8-04 这题怎么做')).toBe('L8-04 子空间')
  })

  it('没有引用时取第一个像样的分句', () => {
    expect(titleFor(material(), '向量组的秩和极大无关组，教材哪里讲了？用 python 算一下')).toBe('向量组的秩和极大无关组')
    expect(titleFor(material(), '嗯，子空间为什么一定含零向量')).toBe('子空间为什么一定含零向量')
    expect(titleFor(material(), '为什么矩阵的行秩等于列秩而且还等于非零子式的最高阶数呢')).toBe('为什么矩阵的行秩等于列秩而且还等于非零子…')
    expect(titleFor(material(), '矩阵 [[2,1],[1,2]] 作用在平面上是什么样子？特征向量在哪？')).toBe('矩阵 [[2,1],[1,2]] 作用在…')
    expect(titleFor(material(), 'What is a subspace? Draw it')).toBe('What is a subspace')
    expect(titleFor(material(), '@L8-99')).toBeUndefined()
  })
})

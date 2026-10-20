import type { Index } from '../src/material.ts'

/** 一本 L42、一本不在白名单里的旧版 W3；W3 的条目 L8-07 被 L42 的页面错误引用（模拟旧索引的题号冲突）。 */
export function fixtureIndex(): Index {
  return {
    books: {
      L42: {
        title: '线性代数', pdf: 'L.pdf', pages: 6, units: ['L8', 'L9'],
        page_items: { '2': ['L8·例01'], '4': ['L8-05', 'L8-07'], '5': ['L8-04'], '6': ['L9-01'] },
        page_text: ['封面', '例 1 的讲解', '没有条目的一页', '题 L8-05 所在页', '题 L8-04 所在页', '第 9 单元'],
      },
      W3: {
        title: '旧版线代', pdf: '/abs/W3.pdf', pages: 2, units: ['L8'],
        page_items: { '1': ['L8-07'] }, page_text: ['旧版', '旧版'],
      },
    },
    items: {
      'L8·例01': { kind: 'example', book: 'L42', unit: 'L8', label: '例 1 · ', md: '**例 1** 子空间的例子', section: '1. 子空间', pages: { lesson: [2] } },
      'L8-04': { kind: 'problem', book: 'L42', unit: 'L8', label: 'L8-04〔A〕', md: '**L8-04** 证明零向量在子空间里', answer: '答案四', verify: [], pages: { problem: [5] } },
      'L8-05': {
        kind: 'problem', book: 'L42', unit: 'L8', label: 'L8-05〔B〕', md: '**L8-05**〔B｜先做 L8-04）〕交与并', answer: '答案五',
        verify: ['[l8] ok L8-05'], pages: { problem: [4], answer: [6] },
      },
      'L8-07': { kind: 'problem', book: 'W3', unit: 'L8', label: 'L8-07', md: '旧版的题', answer: '旧答案', pages: { problem: [1] } },
      'L9-01': { kind: 'problem', book: 'L42', unit: 'L9', label: 'L9-01', md: '**L9-01** 第 9 单元的题', answer: '答案', pages: { problem: [6] } },
    },
    units: {
      'L42/L8': {
        title: 'L.8 · 子空间',
        lesson: '## L.8 · 子空间\n\nL8 讲义全文的开篇。\n\n### 1. 什么是子空间？\n\n子空间对加法和数乘封闭，必含零向量。\n\n#### 三类子空间\n\n张成、列空间、零空间。\n\n### 2. 交与并\n\n两个子空间的交集仍是子空间，并集一般不是。\n\n### 本章小结\n\n记住封闭性。',
        problems_head: 'L8 题目说明',
        cheatsheet: 'L8 速记：子空间先看零向量',
      },
      'L42/L9': { title: '基与维数', lesson: 'L9 讲义全文', problems_head: 'L9 题目说明', cheatsheet: 'L9 速记' },
    },
  }
}

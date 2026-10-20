/** 教材 PDF：pdf.js 按需加载，每本书只下载、解析一次，整个页面共用。 */
import type { PDFDocumentProxy } from 'pdfjs-dist'
import { api } from './catalog.ts'
import { pdfjs } from './chunks.ts'

const docs = new Map<string, Promise<PDFDocumentProxy>>()

export function loadBook(book: string): Promise<PDFDocumentProxy> {
  let doc = docs.get(book)
  if (!doc) {
    doc = pdfjs().then((lib) => {
      lib.GlobalWorkerOptions.workerSrc = api('pdf-worker.mjs')
      return lib.getDocument({ url: api(`pdf?book=${encodeURIComponent(book)}`) }).promise
    })
    // 失败不缓存，下次打开重试
    doc.catch(() => docs.delete(book))
    docs.set(book, doc)
  }
  return doc
}

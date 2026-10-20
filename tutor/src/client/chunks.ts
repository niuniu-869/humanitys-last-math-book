/**
 * 按需加载的一块：PDF（pdf.js）。
 * 构建时打成自包含的 lib/client.<名字>.js（tsdown.config.ts 的 lazyChunks），这里用 dsh 模块加载器的 require.async 取。
 * 不用 import() 让打包器自己拆：拆出的共享分块会被同步 require，dsh 的加载器不认，运行时会抛错并卸载整个插件。
 */
type ChunkLoader = { async(spec: string): Promise<unknown> }

const load = <T>(file: string): Promise<T> => (require as unknown as ChunkLoader).async(`./${file}`) as Promise<T>

export const pdfjs = (): Promise<typeof import('./pdfjs.ts')> => load('client.pdfjs.js')

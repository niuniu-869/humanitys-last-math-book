import { clientBundle } from './build/tsdown.client.ts'

// 宿主端两个入口（宿主插件、答疑 agent）共享 material 等模块；@deepseek-ai/* 由 dsh 提供，其余依赖打进 lib。
export default clientBundle('dsh-plugin-humanitys-last-math-book', ['src/index.ts', 'src/agent.ts'], {
  libExternal: [/^@deepseek-ai\//],
  lib: {
    copy: [{ from: 'node_modules/pdfjs-dist/build/pdf.worker.min.mjs', to: 'lib' }],
  },
  // 浏览器端按需加载的 pdf.js（见 src/client/chunks.ts）
  lazyChunks: {
    pdfjs: 'src/client/pdfjs.ts',
  },
})

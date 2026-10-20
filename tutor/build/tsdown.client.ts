/**
 * Reproducible tsdown preset mirrored from dsh-web-ui for this standalone
 * distribution. Emits a
 * closure-factory artifact: the bundle calls window.__ModuleLoader__.load
 * ({id, factory}) and resolves externals through the injected require
 * (loader module table — cordis DI entities, no globals, no import map).
 * CSS Modules are compiled by lightningcss inside the bundle: importing
 * `x.module.css` yields the hashed class map, and the css text auto-injects
 * a <style data-plugin="<id>"> tag at factory execution (the loader removes
 * plugin-owned tags on unload). The virtual loader registers each real
 * stylesheet as a watch dependency. The platform module list mirrors the
 * shell's seed table in `./web-platform.ts`.
 */
import { readFile, stat, utimes } from 'node:fs/promises'
import { existsSync } from 'node:fs'
import { basename, dirname, relative, resolve as resolvePath, sep } from 'node:path'
import { fileURLToPath } from 'node:url'
import { Rolldown, type TsdownPlugin, type UserConfig } from 'tsdown'
import { transform } from 'lightningcss'
import { PLATFORM_MODULES } from './web-platform.ts'

/**
 * Virtual-id wrapper keeping module CSS away from tsdown's own css pipeline
 * (which requires @tsdown/css). The suffix matters: tsdown's guard matches ids
 * ending in `.css`, so the virtual id must not.
 */
const CSS_VIRTUAL_PREFIX = '\0dsh-css:'
const CSS_VIRTUAL_SUFFIX = '.mjs'

/**
 * Wire/type layers a client bundle may inline: browser-safe contract surfaces
 * with no runtime identity to share (no Symbol/instanceof/singleton state).
 * Everything else under @deepseek-ai/* is either a module-table entry
 * (external) or a leak the purity gate rejects.
 */
export const INLINE_SAFE = /^(?:@deepseek-ai\/dsh-(?:file-reference|session|llm|tools|brand|util-crypto|util-workspace-path)(?:\/|$)|@deepseek-ai\/dsh-token-meter\/client$)/

/** Generated descriptor/codec contribution with no shared runtime identity. */
const GENERATED_REMOTE = /^@deepseek-ai\/dsh-[a-z0-9]+(?:-[a-z0-9]+)*\/remote$/

/**
 * Workspace mode replaces an empty config array with the root defaults. A
 * falsey entry instead removes this package before entry resolution.
 */
const SKIP_WORKSPACE_BUILD: UserConfig = { entry: '' }

/** Externals resolved from the loader module table. */
export const CLIENT_EXTERNALS: readonly string[] = [...PLATFORM_MODULES]

const REPOSITORY_ROOT = fileURLToPath(new URL('..', import.meta.url))

/** Rebase a physical lib-relative source onto a browser URL that mirrors the repository directories. */
function browserSourcePath(source: string, sourcemapPath: string): string {
  if (!source.startsWith('.')) return source
  const physicalSource = resolvePath(dirname(sourcemapPath), source)
  const repositoryPath = relative(REPOSITORY_ROOT, physicalSource).split(sep).join('/')
  return repositoryPath.startsWith('packages/') ? `../../../${repositoryPath}` : source
}

/**
 * Build the tsdown config for one UI plugin package: the node-half lib build
 * plus the browser client bundle. Client packages emit both halves during the
 * Client pass by default; packages needed for Host reflection may opt into the
 * earlier Host pass. A package-level tsdown.config.ts REPLACES the root
 * workspace layout, so the lib half must be restated here — dropping it leaves
 * the package without lib/index.js and the host Loader cannot import its node
 * half.
 * @param id - plugin id (package name), stamped into the __ModuleLoader__.load
 * handoff and onto the injected style tags.
 * @param libEntry - node-half entries, spelled at the call site so the
 * package-invariants gate can see `src/invariant.ts` (or the tsc emit path) in
 * each package's own tsdown.config.ts.
 * @param options - phase placement, lib overrides, companion Node configs.
 * @returns ENV-selected tsdown config for the current build face.
 */
export function clientBundle(
  id: string,
  libEntry: readonly string[],
  options: ClientBundleOptions = {},
): BuildFaceConfig {
  const lib = clientLibraryConfig(id, libEntry, options.lib, options.libExternal)
  return ({ env }) => {
    const face = buildFace(env?.DSH_BUILD_FACE)
    const client = clientConfig(
      id,
      face === undefined ? 'src/client/index.ts' : 'lib/types/client/index.js',
      options.portableCssModuleIds === true,
    )
    const lazy = Object.entries(options.lazyChunks ?? {}).map(([name, entry]) => lazyChunkConfig(id, name, entry))
    const node = [lib, ...(options.companions ?? [])]
    if (face === 'host') return options.hostPhase === true ? node : [SKIP_WORKSPACE_BUILD]
    if (face === 'client') return options.hostPhase === true ? [client, ...lazy] : [...node, client, ...lazy]
    return [...node, client, ...lazy]
  }
}

interface ClientBundleOptions {
  /** Emit the Node-side artifacts during the Host pass instead of the Client pass. */
  readonly hostPhase?: boolean
  /** Additional Node-side configs emitted alongside the package library. */
  readonly companions?: readonly UserConfig[]
  /** Overrides for the package's primary Node-side library config. */
  readonly lib?: UserConfig
  /** Extra Node-side externals (in addition to the default cordis entry). */
  readonly libExternal?: readonly (string | RegExp)[]
  /** Use repository-relative CSS virtual ids and hashes for cross-platform reproducible artifacts. */
  readonly portableCssModuleIds?: boolean
  /**
   * 按需加载的分块：名字 → 入口。每块单独打成自包含的 lib/client.<名字>.js（内部的动态 import 一并内联），
   * 主包用加载器的 require.async('./client.<名字>.js') 取。dsh 的模块加载器不支持分块之间的同步 require，
   * 所以主包本身不允许再拆分块（见 dsh-client-single-chunk）。
   */
  readonly lazyChunks?: Readonly<Record<string, string>>
}

type BuildFace = 'host' | 'client' | undefined

type BuildFaceConfig = (inlineConfig: Pick<UserConfig, 'env'>) => UserConfig[]

function buildFace(value: unknown): BuildFace {
  if (value === undefined || value === 'host' || value === 'client') return value
  throw new Error(`tsdown: --env.DSH_BUILD_FACE must be host or client, received ${String(value)}`)
}

function clientLibraryConfig(
  id: string,
  libEntry: readonly string[],
  overrides: UserConfig = {},
  extraExternal: readonly (string | RegExp)[] = [],
): UserConfig {
  return {
    name: id,
    entry: [...libEntry],
    outDir: 'lib',
    format: ['esm'],
    platform: 'node',
    target: 'es2024',
    fixedExtension: false,
    dts: false,
    clean: false,
    // The cordis framework resolves at runtime from the dsh profile tree, never
    // from this repo's install; its built declarations carry .ts-suffixed
    // relative imports rolldown cannot follow, so the import must stay
    // external (the same stance as the peer APIs above).
    external: ['@deepseek-ai/cordis', ...extraExternal],
    ...overrides,
  }
}

function clientConfig(id: string, entry: string, portableCssModuleIds: boolean): UserConfig {
  const cssFiles = new Map<string, string>()
  return {
    name: `${id}/client`,
    entry: { client: entry },
    // Browser bundle lands next to the node half (single lib/ artifact dir;
    // the entryFileNames pin keeps it exactly lib/client.js). clean must stay
    // off — a default clean would wipe the node-half output emitted above.
    outDir: 'lib',
    format: 'cjs',
    platform: 'browser',
    // Types ship from lib/types (tsc); dts here would wrap the banner/footer into .d.cts and break parsing.
    dts: false,
    // Plugin code is fetched outside Vite's module graph, so its own bundle
    // must carry the TS/TSX mapping consumed by browser profiling tools.
    sourcemap: true,
    // 本插件按需加载 pdf.js，不压缩时这个分块就有数 MB。
    minify: true,
    clean: false,
    external: [...CLIENT_EXTERNALS],
    // Browser bundles inline node-idiom deps (zustand/immer read
    // process.env.NODE_ENV; zustand's esm build also probes
    // import.meta.env.MODE, which a CJS output cannot carry — rolldown flags
    // EMPTY_IMPORT_META). vite defined both on the seed path; tsdown inlining
    // needs the substitutions here or the factory throws ReferenceError at
    // boot / the build gate reds. Both keys honor the build's NODE_ENV so a
    // dev build keeps the dev-branch semantics; artifacts default to production.
    // The bare `import.meta.env` key is required alongside the precise MODE
    // key: zustand probes `import.meta.env ? import.meta.env.MODE : ...`, and
    // the truthiness probe would otherwise survive as an empty import.meta.
    define: {
      'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV ?? 'production'),
      'import.meta.env.MODE': JSON.stringify(process.env.NODE_ENV ?? 'production'),
      'import.meta.env': JSON.stringify({ MODE: process.env.NODE_ENV ?? 'production' }),
    },
    // tsdown auto-externalizes package dependencies; anything NOT in the
    // loader module table must inline instead (wire/type layers, zod, clsx —
    // every non-shared dep). A require() the table cannot answer is a
    // guaranteed runtime throw, so the rule is the table list itself: no
    // opinion for table entries (external above wins), bundle everything else.
    noExternal: (id: string) => (CLIENT_EXTERNALS.includes(id) ? undefined : true),
    plugins: [asyncChunkRequirePlugin(), purityPlugin(), singleChunkPlugin(), {
      name: 'dsh-css-modules-inline',
      resolveId(source: string, importer: string | undefined) {
        if (!source.endsWith('.module.css')) return null
        const abs = importer !== undefined ? sourceAssetPath(source, importer) : source
        const sourceId = portableCssModuleIds
          ? relative(REPOSITORY_ROOT, abs).split(sep).join('/')
          : abs
        const virtualId = CSS_VIRTUAL_PREFIX + sourceId + CSS_VIRTUAL_SUFFIX
        cssFiles.set(virtualId, abs)
        return virtualId
      },
      async load(virtualId: string) {
        if (!virtualId.startsWith(CSS_VIRTUAL_PREFIX)) return null
        const sourceId = virtualId.slice(CSS_VIRTUAL_PREFIX.length, -CSS_VIRTUAL_SUFFIX.length)
        const fileId = cssFiles.get(virtualId) ?? sourceId
        // The virtual id otherwise hides the physical stylesheet from Rolldown's watch graph.
        this.addWatchFile(fileId)
        const source = await readFile(fileId)
        const { code, exports: cssExports } = transform({
          filename: portableCssModuleIds ? sourceId : fileId,
          code: source,
          cssModules: { pattern: '[hash]_[local]' },
          minify: true,
        })
        const classMap: Record<string, string> = {}
        // Sort deterministically: lightningcss's cssExports iteration order is
        // process-dependent (hash-map seeds), which would otherwise churn the
        // emitted lib/client.js on every rebuild.
        for (const [local, exp] of Object.entries(cssExports ?? {}).sort(([a], [b]) => a < b ? -1 : a > b ? 1 : 0)) {
          classMap[local] = exp.name
        }
        // One <style data-plugin> per module file; idempotent under re-evaluation.
        return [
          `const css = ${JSON.stringify(code.toString())};`,
          `const tagId = ${JSON.stringify(`${id}/${basename(sourceId)}`)};`,
          'if (typeof document !== \'undefined\' && document.querySelector(\'style[data-plugin-css=\' + JSON.stringify(tagId) + \']\') === null) {',
          '  const tag = document.createElement(\'style\');',
          `  tag.dataset.plugin = ${JSON.stringify(id)};`,
          '  tag.dataset.pluginCss = tagId;',
          '  tag.textContent = css;',
          '  document.head.appendChild(tag);',
          '}',
          `export default ${JSON.stringify(classMap)};`,
        ].join('\n')
      },
    }],
    outputOptions: {
      entryFileNames: 'client.js',
      chunkFileNames: 'client.[name].js',
      // The map is served from /plugins/<scoped-package>/client.js.map. The
      // browser resolves its local sources back into URLs that mirror the
      // /packages/<group>/<package>/src directories; sourcesContent keeps them usable
      // without exposing that tree as an HTTP route.
      sourcemapPathTransform: browserSourcePath,
      banner: (chunk: { isEntry: boolean; fileName: string }) =>
        `window.__ModuleLoader__.load({ id: ${JSON.stringify(id)}, ${chunk.isEntry ? '' : `chunk: ${JSON.stringify(chunk.fileName)}, `}factory: (require) => {`,
      footer: 'return module.exports; } });',
      intro: 'var module = { exports: {} }; var exports = module.exports;',
    },
  }
}

/** Resolve an emitted JS asset import against its source-tree counterpart. */
function sourceAssetPath(source: string, importer: string): string {
  const emitted = resolvePath(dirname(importer), source)
  if (existsSync(emitted)) return emitted
  const marker = `${sep}lib${sep}types${sep}`
  const boundary = emitted.indexOf(marker)
  if (boundary < 0) return emitted
  return resolvePath(emitted.slice(0, boundary), 'src', emitted.slice(boundary + marker.length))
}

/** Escape a package name for literal use inside a RegExp source. */
function escapeSpecifier(name: string): string {
  return name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}

/**
 * Render package-local dynamic imports through the Client module loader's
 * asynchronous operation (ported from deepseek-harness packages/client/tsdown.client.ts, MIT).
 */
/**
 * Bundle purity gate (build-time mirror of the module-edge rules):
 * platform seed entries stay external, inline-safe wire layers inline,
 * and every other @deepseek-ai value import is a build error — a
 * cross-plugin value import either inlines a duplicate runtime instance
 * or requires a specifier the frozen module table cannot answer.
 * Cross-plugin collaboration goes through cordis services instead.
 */
function purityPlugin(): TsdownPlugin {
  return {
    name: 'dsh-client-bundle-purity',
    resolveId(source: string) {
      if (!source.startsWith('@deepseek-ai/')) return null
      if (CLIENT_EXTERNALS.includes(source)) return null // platform module: external wins
      if (INLINE_SAFE.test(source) || GENERATED_REMOTE.test(source)) return null // wire contribution: inline is the point
      throw new Error(
        `client bundle purity: "${source}" is not a platform module (CLIENT_EXTERNALS), an inline-safe wire layer, or a generated /remote contribution — `
        + 'cross-plugin value imports are forbidden; collaborate through cordis services (type-only imports are erased and never reach this gate)',
      )
    },
  }
}

/** 主包只能有一个文件：拆出的分块会被同步 require，而 dsh 的加载器只认已登记的模块，运行时必然抛错。 */
function singleChunkPlugin(): TsdownPlugin {
  return {
    name: 'dsh-client-single-chunk',
    generateBundle(_options, bundle) {
      const extra = Object.values(bundle).filter((o) => o.type === 'chunk' && !o.isEntry).map((o) => o.fileName)
      if (extra.length) this.error(`client bundle: 主包拆出了分块 ${extra.join(', ')}；用 lazyChunks 声明按需加载的模块，主包里用 require.async 取，不要写 import()`)
    },
  }
}

const CLIENT_DEFINE = {
  'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV ?? 'production'),
  'import.meta.env.MODE': JSON.stringify(process.env.NODE_ENV ?? 'production'),
  'import.meta.env': JSON.stringify({ MODE: process.env.NODE_ENV ?? 'production' }),
}

/** 一个按需加载的分块：自包含的单文件，以 chunk 身份登记到插件名下，供 require.async 取。 */
function lazyChunkConfig(id: string, name: string, entry: string): UserConfig {
  const fileName = `client.${name}.js`
  return {
    name: `${id}/${fileName}`,
    entry: { [`client.${name}`]: entry },
    outDir: 'lib',
    format: 'cjs',
    platform: 'browser',
    dts: false,
    sourcemap: true,
    minify: true,
    clean: false,
    external: [...CLIENT_EXTERNALS],
    define: CLIENT_DEFINE,
    noExternal: (dep: string) => (CLIENT_EXTERNALS.includes(dep) ? undefined : true),
    plugins: [purityPlugin()],
    outputOptions: {
      entryFileNames: fileName,
      inlineDynamicImports: true,
      sourcemapPathTransform: browserSourcePath,
      banner: `window.__ModuleLoader__.load({ id: ${JSON.stringify(id)}, chunk: ${JSON.stringify(fileName)}, factory: (require) => {`,
      footer: 'return module.exports; } });',
      intro: 'var module = { exports: {} }; var exports = module.exports;',
    },
  }
}

function asyncChunkRequirePlugin(): TsdownPlugin {
  return {
    name: 'dsh-client-async-chunk-require',
    renderChunk(code, chunk, outputOptions) {
      if (outputOptions.format !== 'cjs') return null
      const transformed = new Rolldown.RolldownMagicString(code)
      for (const dynamicImport of chunk.dynamicImports) {
        const fileName = dynamicImport.startsWith('./') ? dynamicImport.slice(2) : dynamicImport
        if (!/^client\.[A-Za-z0-9][A-Za-z0-9._-]*\.js$/.test(fileName)) continue
        const specifier = `./${fileName}`
        const call = new RegExp(
          `Promise\\.resolve\\(\\)\\.then\\(\\(\\)\\s*=>\\s*require\\((['"])${escapeSpecifier(specifier)}\\1\\)\\)`,
          'gu',
        )
        const matches = [...code.matchAll(call)]
        if (matches.length === 0) {
          throw new Error(`client bundle compiler: dynamic chunk ${JSON.stringify(specifier)} has no generated import expression`)
        }
        for (const match of matches) {
          transformed.overwrite(match.index!, match.index! + match[0].length, `require.async(${JSON.stringify(specifier)})`)
        }
      }
      return transformed.hasChanged() ? transformed : null
    },
    async writeBundle(outputOptions, bundle) {
      const entry = Object.values(bundle).find(output => output.type === 'chunk' && output.isEntry)
      if (entry === undefined || outputOptions.dir === undefined) return
      const entryPath = resolvePath(outputOptions.dir, entry.fileName)
      const current = await stat(entryPath)
      const completedAt = new Date(Math.max(Date.now(), current.mtimeMs + 1))
      await utimes(entryPath, current.atime, completedAt)
    },
  }
}

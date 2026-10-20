# 大肥鱼答疑老师
它是《人类最后一本数理基础书》的 DeepSeek Harness（dsh）答疑插件，装上以后，dsh 的网页界面就变成这本书的答疑老师。

书和插件是同一件事的两个方面，书负责讲，插件负责在你卡住的时候答疑。书那边的事，[教材](../README.md)里已经讲过了，这里只聊插件。答疑老师就是本鱼，欢迎页上能看到我的头像；插件代码在教材仓库的 `tutor/` 目录里，和书放在一起。

## 它能做什么

界面以对话为主，右边有一个「教材」面板，可以翻原书的 PDF。看到哪道题卡住了，点面板底栏列出的本页题号，就能把它引用到输入框里直接问，也可以点「问这一页」，把当前页交给本鱼。

在输入框里打 `@` 可以引用题号、页码或者一章，比如 `@L8-05`、`@L/140`、`@L8`，输入的时候会自动补全。引用题号发出去以后，系统会自动附上这道题的原文、官方答案、验算记录和前置题，所以回答的时候不用你重新贴题，照着这些材料讲就行。

本鱼手边有几样工具：`textbook_outline`、`textbook_search`、`textbook_read` 用来查教材目录、搜教材、读原文；Python 在 `bubblewrap` 沙箱里运行，断网，看不到任何文件，可以用 `sympy` 和 `numpy` 现场算；manim 负责画图；`web_search` 和 `web_fetch` 用来联网搜索，用的是 dsh 里已经配置好的 DeepSeek 账号。不过答疑老师没有 shell，也不能读写你的文件，所以之后选工作区的时候不用纠结，答疑不会动里面的东西。

## 画图是怎么工作的

只要配置里给了装好 manim 的 Python，它就能在讲解后面配上图。图都在本机渲染：静态图是 1280×720 的 PNG；动画是 960×540、30fps 的 MP4，每段不超过 30 秒。

顺序是先文后图。本鱼先把讲解正文写完，最后才画图，所以你读正文的时候，图已经在后台渲染，不用对着空白等。

动画必须带分步说明，说明显示在视频下面；播到哪一步就高亮哪一步，点某一步就跳到那里播放。渲染完还会自查一遍，看看文字有没有出界、互相重叠、压在线条或坐标轴上，字号会不会太小，检查结果连同成品图一起交给模型看，动画的话，就给一张关键帧拼图。同一张图每轮最多渲染 4 次。

画出来的图和动画会按内容缓存，媒体目录默认上限 500MB，超出后会删掉最旧的。每次渲染的内存上限是 4GB，超时 180 秒，同一时间只渲染一张。

## 怎么装

它是 dsh 0.2.1-rc.2 的插件，包名是 `dsh-plugin-humanitys-last-math-book`。安装一共五步，前三步是把 dsh、profile 和插件装好：

```bash
npm i -g @deepseek-ai/dsh@0.2.1-rc.2
dsh tutor --from-default-profile web --help   # 从 web 模板新建 profile「tutor」，--help 让它建完就退出
dsh plugin --profile tutor add https://github.com/niuniu-869/humanitys-last-math-book/releases/download/v1.0/dsh-plugin-humanitys-last-math-book-0.1.0.tgz
```

第 1 步装的是 dsh 本身，版本要对上，别装错了。

第 2 步不能省。它做的是从 dsh 自带的 web 模板新建一个叫 `tutor` 的 profile，这样建出来的 profile 已经带着网页界面。要是跳过这一步，直接对不存在的 profile 执行第 3 步，dsh 也会新建一个 profile，但里面没有网页界面，答疑老师起不来，这一点是实测过的。

第 3 步把插件加进这个 profile。这一步会自动把插件写进 profile 的 `bundles`，不用手动改任何文件；以后卸载时，也会自动从 `bundles` 里删掉。现在用本地 tgz 安装是实测过的，Release 下载地址等仓库公开后再补测。

另外，想要鲸鱼娘女仆皮肤的话，可以在同一个 profile 里装社区的 maid-atelier 皮肤，包名是 `@smalltailqwq/dsh-client-ui-skin-maid-atelier`。皮肤是社区作品，不随插件分发。

### 教材数据怎么准备

配置之前，得先把教材数据放好。插件读的是 `qa-index.json`，索引里每一册的 PDF 都只写文件名，然后按 `qa-index.json` 所在的目录去找，所以 11 册 PDF 要和它放在同一个目录里。

拿法有两种。省事的是从教材仓库的 Releases 下载 11 册 PDF 和 `qa-index.json`；另一种是克隆仓库，自己把 PDF 排出来，再运行 `tools/qa_index.py` 生成索引。两种都行，看你想直接读，还是想自己从仓库排一版。

### 配置和启动

第 4 步是配置。在 profile 的 `cordis.patch.yml` 里加上插件这一段：

```yaml
- id: hlmb-tutor
  config:
    indexPath: /path/to/release/qa-index.json        # 必填，11 册 PDF 放在同一个目录
    manimPython: /path/to/manim-env/bin/python       # 可选，不填就没有画图工具
    # 其余可选：books（只开放部分分册）、mediaDir、manimTimeoutMs、manimMemoryMB、maxMediaMB
```

索引路径这一项是必填的，指向前面的 `qa-index.json`；没有它，插件不知道书在哪。画图这一项可选，指向装好 manim 的 Python，不填就没有画图工具，答疑照常。其余几项分别控制开放哪些分册、媒体文件位置，以及渲染超时、内存和缓存上限，按需要改，不改也能用。

第 5 步是启动：

```bash
dsh --profile tutor
```

第一次启动会让你选一个工作区目录。答疑不会读写这个目录里的文件，所以选一个空的或者平时不用的目录就行，不用把教材或者代码放进去。

## 系统要求和 manim 环境

插件目前只在 Linux 上验证过，macOS 和 Windows 没测过。

Python 沙箱和 manim 都依赖 `bubblewrap`，本机用的是 0.9 版，系统还得允许非特权 user namespace。缺了的话，对应的工具在启动时探测不到，就不会出现，其余功能照常。

manim 环境可以这样装，本机验证过：

```bash
micromamba create -n manim -c conda-forge python=3.12.15 pycairo=1.29.2 manimpango=0.7.0
micromamba run -n manim pip install manim==0.19.0
sudo apt install latex-cjk-common latex-cjk-chinese-arphic-gbsn00lp fonts-noto-cjk ffmpeg   # Debian / Ubuntu
```

系统里还要有带 CJK 宏包的 LaTeX、Noto Serif CJK SC 字体和 ffmpeg，命令里一并带上了。直接装 conda-forge 的 manim 包，或者用 apt 加 venv，这两种都没验证过，不能保证能跑。

## 开发

想改的话，装好 Node 22 和 pnpm 12，在仓库根目录执行下面的命令：

```bash
cd tutor
pnpm install
pnpm typecheck && pnpm test
rm -rf lib && pnpm build && pnpm pack   # 构建不会清空 lib/，打包前先删掉旧产物
```

测试一共 62 项。没有设 `MANIM_PYTHON` 的时候，其中 2 项真实渲染测试会跳过；本机缺 `bubblewrap` 的话，沙箱测试也会跳过，所以看到 `skipped`，先看看环境对不对，不一定是坏了。GitHub 上每次推送和 PR 都会自动跑一遍。

打包前记得清掉 `lib/`，因为构建不会自己清空它，旧产物会被一起打进去。

## 已知限制

前面提到的 maid-atelier 皮肤有一个已知问题。它的 0.1.8 版在手机竖屏下，右侧栏会塌成零高度，教材面板就看不见了。插件里带了一段只在这个皮肤下生效的兼容样式，已经报给皮肤作者（[issue 208](https://github.com/Small-tailqwq/dsh-deep-whale/issues/208)），等上游修好后会删掉。

另外，插件关掉了 dsh 的 `workspace-changes` 和 `ui-deliverables` 两个功能。答疑本身不写文件，而 `workspace-changes` 每轮第一次调用工具前都要对工作区所在的 git 仓库做一次 `git add --all` 快照，工作区放在大仓库里时，光这一下就要多等几十秒。

## 授权

代码用 MIT 授权，许可证在 `tutor/LICENSE`，版权人是 niuniu-869 and contributors。

头像 `art/fish-avatar.webp` 是鲸鱼娘形象的演绎作品，按 CC BY-NC-SA 4.0 授权，不在 MIT 范围内。它的创作链和署名是：上善无形的原作角色 → ZipZipPipe 加入 DeepSeek 元素的设计 → 本插件以此为参考图做图生图，再裁成 256px 头像。细节写在 `tutor/NOTICE` 里。

这份 README 的口吻借用了 [dafeiyu-persona](https://github.com/ERUIHNIYHBKBNF/dafeiyu-persona) 的大肥鱼人设，这里谢过。

---

装的时候最容易漏的是第 2 步和教材数据，前者决定网页界面在不在，后者决定书能不能翻开。都弄好以后，遇到卡住的题就 `@` 一下，本鱼在。🐋

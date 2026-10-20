# 许可说明

本仓库的内容分两类，用两种许可。

| 内容 | 位置 | 许可 |
|---|---|---|
| 正文和插图 | `books/**/*.md`、`books/**/fig/`、`docs/`、`README.md` | [CC BY-SA 4.0](LICENSE) |
| 代码 | `tools/`、`tutor/`（答疑插件）、`books/**/verify.py`、`books/**/checks/`、`books/**/figs/` | [MIT](LICENSE-CODE) |
| README 开头的三张梗图 | `docs/images/meme-*.jpg` | 不适用本仓库的许可，见下 |
| 答疑插件的大肥鱼头像 | `tutor/art/fish-avatar.webp` | [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)，见 `tutor/NOTICE` |

**正文和插图（CC BY-SA 4.0）**：可以复制、分发、改编，也可以用于商业用途，包括印成纸书、用作课程讲义。条件是：署名（注明出自 niuniu-869 等著《人类最后一本数理基础书》，并给出仓库链接），注明是否做了修改，改编后的作品使用同样的许可发布。

**代码（MIT）**：可以随意使用、修改和再分发，保留版权声明和许可声明即可。由画图脚本生成的图属于正文插图，按 CC BY-SA 4.0 使用。

## 其他说明

- **README 开头的三张梗图**：网络梗图，2026 年 9 月流行，作者不详，转自微博「蚁工厂」2026-09-21 的合订本。图中女仆鲸鱼娘的原设计来自画师上善无形（角色「溟月」，以 CC BY-NC-SA 4.0 开放二创）和 B 站 UP 主 ZipZipPipe（女仆版，禁止商用）。本仓库只做非商业引用，这三张图的权利归原作者，不随本仓库的 CC BY-SA 4.0 授权给你。转载请遵守原作者的条件，不要商用。作者如不同意引用，请联系我们删除。
- **答疑插件的大肥鱼头像**（`tutor/art/fish-avatar.webp`）：DeepSeek 鲸鱼娘形象的演绎作品，以 CC BY-NC-SA 4.0 授权，不在 MIT 范围内。创作链是：上善无形的原作角色 → ZipZipPipe 加入 DeepSeek 元素的鲸鱼娘设计 → 本插件以此为参考图做图生图（2026-10），再裁切成 256px 头像。使用时须保留这条完整署名，只能非商业使用，再演绎须以相同方式共享；美术版权归以上各作者。详见 `tutor/NOTICE`。
- **答疑插件的构建配置**（`tutor/build/tsdown.client.ts`、`tutor/build/web-platform.ts`）：改编自 Small-tailqwq 的 [dsh-deep-whale](https://github.com/Small-tailqwq/dsh-deep-whale)（MIT，Copyright (c) 2026 Small-tailqwq），其中 asyncChunkRequirePlugin 来自 DeepSeek 的 [deepseek-harness](https://github.com/deepseek-ai/deepseek-harness)（MIT，Copyright (c) 2026 DeepSeek）。再分发时须保留这两条版权声明，原文见 `tutor/NOTICE`。插件推荐的 maid-atelier 皮肤不在本仓库，它的美术按 CC BY-NC-SA 4.0 授权、不能商用。
- **字体**：本仓库不包含字体文件。排版用到的 Noto CJK、STIX Two、TeX Gyre Heros、DejaVu Sans 各自使用开源字体许可，需要另外安装。
- **商标**：书中提到的 GPT、ChatGPT、Llama、Qwen、DeepSeek 等名称属于各自的权利人，只用于说明事实，不表示与这些机构有任何关联。书名借用了 AI 评测 Humanity's Last Exam（Center for AI Safety 与 Scale AI）的句式，本书与它及其出品方同样没有关联。
- **AI 写成的内容**：本书的文字、题目、代码和配图全部由 AI 模型写成，人类作者只做题、提意见（见 README）。在一些法域，完全由模型生成的内容是否受著作权保护尚无定论；上述许可适用于本书中依法享有权利的全部内容。
- **贡献**：向本仓库提交的内容，默认按上面同样的许可授权（正文按 CC BY-SA 4.0，代码按 MIT）。

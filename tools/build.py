#!/usr/bin/env python3
"""把一册排成可双面打印的 A4 PDF。

    python tools/build.py P                  # 产物：release/P_humanitys-last-math-book.pdf
    python tools/build.py all                # 全部分册，按书序逐册排
    python tools/build.py P --units P1,P2    # 只排其中几章（试排用）
    python tools/build.py P --tex-only       # 只生成 LaTeX 源 books/P/_build/P.tex，不编译

依赖：
- pandoc ≥ 3.0；
- LuaLaTeX（TeX Live 2023 及以后或 MiKTeX），需要 ctex、unicode-math、tcolorbox、fancyvrb、enumitem 等宏包；
- 字体：Noto Serif/Sans/Sans Mono CJK SC、STIX Two Text/Math、TeX Gyre Heros、DejaVu Sans，都是开源字体。
  中文字体名可用环境变量 BOOK_SERIF、BOOK_SANS、BOOK_MONO 覆盖，例如只装了思源字体时设为 Source Han Serif SC。
每册编译约占 2–3.5 GB 内存。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

NAME = "人类最后一本数理基础书"  # 书名，印在封面上（页眉印的是册名）
SLUG = "humanitys-last-math-book"  # PDF 文件名用的英文名：GitHub Releases 会删掉附件文件名里的中文
ROOT = Path(__file__).resolve().parents[1]
BOOKS = ROOT / "books"
RELEASE = ROOT / "release"
ORDER = ["Z", "C1", "C2", "C3", "L", "P", "M", "K1", "K2", "K3", "K4"]  # 书序

# 正文里用到的几个符号在 PDF 字体里缺字形，换成数学符号；其余 emoji 一律删掉
SYMBOLS = {"✓": r"$\checkmark$", "✗": r"$\times$", "➜": r"$\rightarrow$"}
EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF☀-➿️]")


def clean(md: str) -> str:
    # 有的公式写成 \(..\)、\[..\]，pandoc 只认 $，统一换掉；表格换行 \\[2mm] 前面还有一个反斜杠，不动
    md = re.sub(r"(?<!\\)\\\[(.+?)(?<!\\)\\\]", lambda m: "$$" + m[1].strip() + "$$", md, flags=re.S)
    md = re.sub(r"(?<!\\)\\\((.+?)(?<!\\)\\\)", lambda m: "$" + m[1].strip() + "$", md, flags=re.S)
    out, fence = [], False
    for line in md.splitlines():
        if line.lstrip().startswith("```"):
            fence = not fence
        elif fence:
            line = line.replace("⟹", "⇒")  # 等宽字体 DejaVu Sans Mono 没有长箭头 ⟹，排出来是空白
        if line.startswith("#"):
            line = re.sub(r"\s+", " ", EMOJI_RE.sub("", line)).rstrip()
        else:
            segs = line.split("`")  # 反引号里是代码，不换符号
            for i, seg in enumerate(segs):
                if not i % 2:
                    for k, v in SYMBOLS.items():
                        seg = seg.replace(k, v)
                segs[i] = EMOJI_RE.sub("", seg)
            line = "`".join(segs)
        out.append(line)
    # 列表紧跟在普通文字行后面时 pandoc 不认，会排成字面的「1.」「- 」：补一个空行
    list_item = re.compile(r"^\s*(\d+[.)]|[-*+]) ")
    fixed = []
    for prev, line in zip([""] + out, out):
        if (list_item.match(line) and prev.strip() and not list_item.match(prev)
                and not prev.startswith(("|", ">", "    ", "\t"))):
            fixed.append("")
        fixed.append(line)
    return fit_tables("\n".join(fixed) + "\n")


def _width(cell: str) -> int:
    # 粗略显示宽度：去掉公式和格式符号，中文按 2 计
    cell = re.sub(r"\\[a-zA-Z]+|[{}$*`]", "", cell)
    return sum(2 if ord(ch) > 0x2E80 else 1 for ch in cell.strip())


def fit_tables(md: str) -> str:
    """按每列最长内容重写 pipe 表格的分隔行，让 pandoc 按比例分配列宽。"""
    lines = md.split("\n")
    for i, line in enumerate(lines):
        if not re.fullmatch(r"\|(\s*:?-{3,}:?\s*\|)+", line.strip()):
            continue
        j = i + 1
        while j < len(lines) and lines[j].startswith("|"):
            j += 1
        cells = [r.strip().strip("|").split("|") for r in [lines[i - 1]] + lines[i + 1:j]]
        widths = [max(3, max(_width(c[k]) if k < len(c) else 0 for c in cells)) for k in range(len(cells[0]))]
        total = sum(widths)
        # 分隔行要比 pandoc 的 --columns 长，列宽才按比例生效
        lines[i] = "|" + "|".join("-" * max(3, round(w * 100 / total)) for w in widths) + "|"
    return "\n".join(lines)


def to_latex(md: str) -> str:
    return subprocess.run(
        ["pandoc", "-f", "markdown+tex_math_dollars+pipe_tables+hard_line_breaks-raw_html-subscript-superscript",
         "-t", "latex", "--wrap=preserve", "--columns=60", "--no-highlight"],
        input=md, capture_output=True, text=True, check=True,
    ).stdout


PREAMBLE = r"""
\documentclass[UTF8,zihao=5,twoside,fontset=none]{ctexart}
\setCJKmainfont{@SERIF@}[BoldFont=@SERIF@ Bold]
\setCJKsansfont{@SANS@}[BoldFont=@SANS@ Bold]
\setCJKmonofont{@MONO@}
\directlua{luaotfload.add_fallback("fb",{"DejaVu Sans:mode=harf;","file:STIXTwoMath-Regular.otf:mode=harf;"})}
\ltjdefcharrange{100}{"2460-"24FF}\ltjsetparameter{jacharrange={+100}}
\setmainfont{STIXTwoText}[Extension=.otf,UprightFont=*-Regular,BoldFont=*-SemiBold,ItalicFont=*-Italic,BoldItalicFont=*-SemiBoldItalic,RawFeature={fallback=fb}]
\setsansfont{TeX Gyre Heros}[RawFeature={fallback=fb}]
\setmonofont{DejaVu Sans Mono}[Scale=0.85]
\usepackage[a4paper,inner=25.5mm,outer=19mm,top=22mm,bottom=20mm,headsep=6mm]{geometry}
\usepackage{amsmath}
\usepackage[warnings-off={mathtools-colon,mathtools-overbracket}]{unicode-math}
\setmathfont{STIXTwoMath-Regular.otf}
% STIX Two Math 没有粗体版本，\boldsymbol 会排成细体，改用粗斜体字符；\square 等由同形字符补上
\AtBeginDocument{\renewcommand{\boldsymbol}[1]{\symbfit{#1}}}
\AtBeginDocument{\providecommand{\square}{\mdlgwhtsquare}\providecommand{\Box}{\mdlgwhtsquare}\providecommand{\blacksquare}{\mdlgblksquare}}
\usepackage{longtable,booktabs,array,calc,multirow}
\usepackage{xcolor,tcolorbox,enumitem,fancyhdr,graphicx}
\tcbuselibrary{breakable,skins}
\usepackage{float,caption}
\usepackage{fancyvrb}\RecustomVerbatimEnvironment{verbatim}{Verbatim}{fontsize=\small,frame=leftline,framerule=1.2pt,framesep=3mm,xleftmargin=2mm,samepage=true}
\floatplacement{figure}{H}
\captionsetup[figure]{labelformat=empty,font=small,skip=2pt}
\setkeys{Gin}{keepaspectratio}
\usepackage[hidelinks]{hyperref}
\setlength{\emergencystretch}{3em}
\linespread{1.31}
\raggedbottom  % 双面默认 flushbottom 会把页内空白拉开，改为页底不强求对齐
\setlength{\parindent}{0pt}
\setlength{\parskip}{0.6em}
\setlist{itemsep=0.25em,topsep=0.45em}
\setcounter{secnumdepth}{-1}
\providecommand{\tightlist}{\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
\providecommand{\pandocbounded}[1]{#1}
\makeatletter\@ifundefined{c@none}{\newcounter{none}}{}\makeatother
\def\LTcaptype{none}
% 全书按黑白打印设计：标题条、引用块底色都是灰度
\definecolor{ink}{gray}{0.12}
\definecolor{soft}{gray}{0.92}
\ctexset{
  section={format=\color{ink}\sffamily\bfseries\Large\raggedright,beforeskip=1.6em,afterskip=0.8em},
  subsection={format=\color{ink}\sffamily\bfseries\large\raggedright,beforeskip=1.6em,afterskip=0.65em},
  subsubsection={format=\sffamily\bfseries\normalsize\raggedright,beforeskip=1.1em,afterskip=0.35em},
  paragraph={format=\sffamily\bfseries\normalsize\raggedright,runin=false,beforeskip=0.6em,afterskip=0.2em},
}
\renewenvironment{quote}{\begin{tcolorbox}[breakable,enhanced,colback=soft,colframe=soft,
  borderline west={2pt}{0pt}{ink},sharp corners,left=6pt,right=6pt,top=4.5pt,bottom=4.5pt,before skip=0.85em,after skip=0.85em]}{\end{tcolorbox}}
\renewcommand{\partmark}[1]{\markboth{#1}{#1}}
\renewcommand{\sectionmark}[1]{}\renewcommand{\subsectionmark}[1]{}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[LE]{\sffamily\small{} \BOOKTITLE}
\fancyhead[RO]{\sffamily\small\leftmark}
\fancyfoot[LE,RO]{\sffamily\small\thepage}
\renewcommand{\headrulewidth}{0.4pt}
\newcommand{\newpart}[2]{\cleardoublepage\partmark{#1}%
  \begin{tcolorbox}[colback=ink,colframe=ink,coltext=white,sharp corners,left=8pt,top=6pt,bottom=6pt]
  {\sffamily\bfseries\LARGE #1}\hfill{\sffamily\small #2}\end{tcolorbox}\vspace{0.4em}}
\renewcommand{\arraystretch}{1.35}
% 独立公式上下的空白；\normalsize 会重设这两个值，所以挂在它后面
\makeatletter\g@addto@macro\normalsize{\setlength\abovedisplayskip{9pt plus 3pt minus 3pt}\setlength\belowdisplayskip{9pt plus 3pt minus 3pt}}\makeatother
"""


def fonts(tex: str) -> str:
    return (tex.replace("@SERIF@", os.environ.get("BOOK_SERIF", "Noto Serif CJK SC"))
               .replace("@SANS@", os.environ.get("BOOK_SANS", "Noto Sans CJK SC"))
               .replace("@MONO@", os.environ.get("BOOK_MONO", "Noto Sans Mono CJK SC")))


def unit_md(book: str, unit: str, name: str) -> str:
    p = BOOKS / book / unit / name
    if not p.exists():
        return ""
    md = p.read_text(encoding="utf-8")
    # 图片路径：章内的 fig/ → 相对 books/<册>/_build/ 的 ../<章>/fig/
    md = re.sub(r"\]\((?:\./)?fig/", f"](../{unit}/fig/", md)

    # 公式内三处修补：①② 等带圈数字数学字体没有，改由正文字体排；LuaTeX 把汉字当字母，
    # \cdot狗 会被读成命令「cdot狗」，命令名后紧跟汉字时补一个空格；长元组 (a,\ b,\ c) 允许在逗号后断行
    def fix_math(m: re.Match) -> str:
        t = re.sub(r"(?<!\\text\{)([\u2460-\u2473])", r"\\text{\1}", m.group(0))
        t = re.sub(r"(\\[A-Za-z]+)(?=[\u3400-\u9fff])", r"\1 ", t)
        return t if t.startswith("$$") else t.replace(r",\ ", r",\allowbreak\ ")
    md = re.sub(r"\$\$.*?\$\$|\$[^$\n]+?\$", fix_math, md, flags=re.S)
    # pandoc 要求标题前有空行，否则标题会被并进上一段或引用块
    md = re.sub(r"(?m)^(?!```)(.*\S.*)\n(#{2,4} )", r"\1\n\n\2", md)
    return md.strip() + "\n\n"


def cover(book: str, title: str, units: list[str]) -> str:
    rows = "\n".join(rf"\textbf{{{u}}} & & & & & \\[0.5em] \hline" for u in units)
    return rf"""
\thispagestyle{{empty}}
\vspace*{{30mm}}
{{\sffamily\bfseries\fontsize{{34}}{{40}}\selectfont {book}}}\par\vspace{{4mm}}
{{\sffamily\bfseries\LARGE {title}}}\par\vspace{{2mm}}
{{\sffamily\large {NAME}}}\par
\vspace{{14mm}}
\begin{{tcolorbox}}[colback=soft,colframe=ink,boxrule=0.5pt,sharp corners,title={{\sffamily\bfseries 本册结构与用法}},coltitle=white,colbacktitle=ink]
\begin{{enumerate}}[leftmargin=1.5em]
\item 本册依次为：\textbf{{速记表}} → \textbf{{讲义}} → \textbf{{练习题}} → \textbf{{答案}}，各部分从新的一页开始，可以拆开使用。
\item 讲义按学习顺序排列，每个单元开头说明它接着上一单元解决什么问题。每个概念先从具体例子讲起，再给定义；每个方法配有由浅入深的例题。
\item 练习题分 \textbf{{A 基础 → B 进阶 → C 提高}} 三档，每题标注所用方法；B 档含变式题，C 档题注明先做哪几道。
\item 答案先给最终结果，再写关键推导；数值答案都经过代码验算。
\end{{enumerate}}
\end{{tcolorbox}}
\vfill
\newpage
\thispagestyle{{empty}}
{{\sffamily\bfseries\Large 间隔复习表}}\hfill{{\small 学完后第 1、3、7、14 天各复习一次：遮住速记表右栏自测，再重做错题}}\par\vspace{{3mm}}
\begin{{tabular}}{{|p{{14mm}}|>{{\centering}}p{{18mm}}|>{{\centering}}p{{18mm}}|>{{\centering}}p{{18mm}}|>{{\centering}}p{{18mm}}|>{{\centering\arraybackslash}}p{{52mm}}|}}
\hline \textbf{{单元}} & 学完 & +1/+3 天 & +7 天 & +14 天 & 错题号 \\ \hline
{rows}
\end{{tabular}}
"""


PARTS = (  # 文件名、部分名、副标题；答案部分用小一号字
    ("cheatsheet.md", "速记表", "遮住右栏自测", ""),
    ("lesson.md", "讲义", "问题 · 直觉 · 方法 · 例题", ""),
    ("problems.md", "练习题", "A 基础 · B 进阶 · C 提高", ""),
    ("answers.md", "答案", "做完再对照", r"\small"),
)


def book_tex(book: str, only: list[str] | None = None) -> str:
    o = json.loads((BOOKS / book / "outline.json").read_text(encoding="utf-8"))
    units = [u["code"] for u in o["units"] if not only or u["code"] in only]
    body = []
    for name, label, sub, size in PARTS:
        md = "".join(unit_md(book, u, name) for u in units)
        if md.strip():
            body.append(rf"\newpart{{{label}}}{{{sub}}}{size}" + "\n" + to_latex(clean(md)))
    head = fonts(PREAMBLE.replace(r"\BOOKTITLE", f"{book} · {o['title']}"))
    return head + "\n\\begin{document}\n" + cover(book, o["title"], units) + "\n".join(body) + "\n\\end{document}\n"


def compile_tex(tex: str, bdir: Path, name: str) -> Path | None:
    bdir.mkdir(parents=True, exist_ok=True)
    src = bdir / f"{name}.tex"
    src.write_text(tex, encoding="utf-8")
    for ext in ("aux", "out", "toc"):
        (bdir / f"{name}.{ext}").unlink(missing_ok=True)
    for _ in range(2):  # 两遍：第二遍才有正确的书签和页眉
        r = subprocess.run(["lualatex", "-interaction=nonstopmode", "-halt-on-error", src.name],
                           cwd=bdir, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if r.returncode != 0:
            print(f"[{name}] LaTeX 失败，日志末尾：\n{r.stdout[-3000:]}")
            return None
    return bdir / f"{name}.pdf"


def build(book: str, only: list[str] | None = None, tex_only: bool = False) -> bool:
    tex = book_tex(book, only)
    bdir = BOOKS / book / "_build"
    if tex_only:
        bdir.mkdir(parents=True, exist_ok=True)
        (bdir / f"{book}.tex").write_text(tex, encoding="utf-8")
        print(f"[{book}] {bdir / f'{book}.tex'}")
        return True
    pdf = compile_tex(tex, bdir, book)
    if not pdf:
        return False
    RELEASE.mkdir(exist_ok=True)
    out = RELEASE / f"{book}_{SLUG}.pdf"
    pdf.replace(out)
    print(f"[{book}] {out}")
    return True


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("book", help="册号（" + "、".join(ORDER) + "）或 all")
    ap.add_argument("--units", help="只排这些章，逗号分隔，例如 P1,P2")
    ap.add_argument("--tex-only", action="store_true", help="只生成 LaTeX 源，不编译")
    a = ap.parse_args()
    books = ORDER if a.book == "all" else [a.book]
    ok = [build(b, a.units and a.units.split(","), a.tex_only) for b in books]
    sys.exit(0 if all(ok) else 1)


if __name__ == "__main__":
    main()

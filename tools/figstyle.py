"""配图的统一风格。

用法（画图脚本放在 books/<册>/<章>/figs/<图名>.py，在 figs/ 的上一级目录运行）：
    import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / "tools"))
    from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
    fig, ax = new_fig(12, 7.5)
    ...
    save(fig, "P7-n1")          # → 当前目录 fig/P7-n1.pdf 和 fig/P7-n1.png

全书按黑白打印设计：只用灰度，不同对象靠线型、点形和文字标签区分。
中文用 Noto Sans CJK SC，公式用 STIX；图注写在 markdown 里，图内只放必要标注。
"""
import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.patheffects as pe  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib import font_manager  # noqa: E402

_FONT_DIRS = [  # 系统字体目录之外的补充位置；字体已装进系统时不需要
    Path("/usr/share/fonts/opentype/noto"),
    *(Path(p) for p in os.environ.get("FIGSTYLE_FONT_DIRS", "").split(os.pathsep) if p),
]
for d in _FONT_DIRS:
    if d.exists():
        for f in list(d.glob("*.otf")) + list(d.glob("*.ttc")):
            font_manager.fontManager.addfont(str(f))
_names = {f.name for f in font_manager.fontManager.ttflist}
_CJK = next((n for n in ("Noto Sans CJK SC", "Noto Sans CJK JP") if n in _names), "DejaVu Sans")


class C:
    """调色板：全部是灰度。名字沿用早期脚本里的 BLUE/RED/…，实际是由深到浅的四级灰；
    不同对象还要靠线型（实线/虚线/点线）、点形（实心/空心/方块）和文字标签区分，不能只靠深浅。"""
    BLUE, RED, TEAL, AMBER = "#000000", "#404040", "#6E6E6E", "#9A9A9A"
    INK, GRAY, LIGHT, PAPER = "#000000", "#808080", "#E3E3E3", "#FFFFFF"
    CMAP = "Greys"  # 曲面和等高线填色


plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": [_CJK, "STIX Two Text", "DejaVu Sans"],
    "mathtext.fontset": "stix",
    "axes.unicode_minus": False,
    "font.size": 10,
    "axes.labelsize": 10,
    "axes.titlesize": 10.5,
    "axes.edgecolor": C.GRAY,
    "axes.linewidth": 0.8,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.prop_cycle": matplotlib.cycler(color=[C.BLUE, C.RED, C.TEAL, C.AMBER, C.GRAY]),  # 线型不进循环：旧脚本默认实线，要虚线的地方脚本自己写
    "xtick.color": C.GRAY, "ytick.color": C.GRAY,
    "xtick.labelcolor": C.INK, "ytick.labelcolor": C.INK,
    "lines.linewidth": 1.6,
    "legend.frameon": False,
    "figure.facecolor": C.PAPER,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.04,
    "pdf.fonttype": 42,
})


def new_fig(w_cm: float = 12, h_cm: float = 7.5, **kw):
    return plt.subplots(figsize=(w_cm / 2.54, h_cm / 2.54), **kw)


def new_fig3d(w_cm: float = 12, h_cm: float = 9, elev: float = 28, azim: float = -58):
    fig = plt.figure(figsize=(w_cm / 2.54, h_cm / 2.54))
    ax = fig.add_subplot(projection="3d")
    ax.view_init(elev=elev, azim=azim)
    for a in (ax.xaxis, ax.yaxis, ax.zaxis):
        a.pane.set_facecolor((1, 1, 1, 0))
        a.pane.set_edgecolor(C.LIGHT)
        a._axinfo["grid"]["color"] = (0.85, 0.85, 0.85, 0.6)
    return fig, ax


HALO = [pe.withStroke(linewidth=3, foreground=C.PAPER)]  # 图内文字描白边，压在曲线上也看得清


def label(ax, text, xy, offset=(0, 0), color=C.INK, **kw):
    """图内标注统一走这里：带白边，offset 以磅为单位。"""
    return ax.annotate(text, xy, xytext=offset, textcoords="offset points", color=color,
                       path_effects=HALO, zorder=6, **kw)


def arrow(ax, start, vec, color=C.RED, text=None, lw=1.8, offset=(4, 4), **kw):
    """从 start 出发画向量 vec（2D）；text 写在箭头尖旁边。"""
    (x, y), (dx, dy) = start, vec
    ax.annotate("", xy=(x + dx, y + dy), xytext=(x, y),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, shrinkA=0, shrinkB=0, mutation_scale=11), **kw)
    if text:
        label(ax, text, (x + dx, y + dy), offset, color)


def dot(ax, xy, text=None, color=C.INK, offset=(5, -10), size=22):
    ax.scatter(*xy, s=size, color=color, zorder=5)
    if text:
        label(ax, text, xy, offset, color)


def save(fig, name: str, outdir: str = "fig") -> None:
    out = Path(outdir)
    out.mkdir(exist_ok=True)
    fig.savefig(out / f"{name}.pdf")
    fig.savefig(out / f"{name}.png", dpi=200)
    plt.close(fig)

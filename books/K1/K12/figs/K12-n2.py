import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, PathPatch
from matplotlib.path import Path

fig, ax = new_fig(17, 9)
ax.set(xlim=(0, 12), ylim=(0, 6))
ax.axis("off")

def box(x, y, text, w=3.0):
    ax.add_patch(FancyBboxPatch((x-w/2, y-.48), w, .96,
                 boxstyle="round,pad=0.04,rounding_size=0.12",
                 facecolor=C.PAPER, edgecolor=C.INK, lw=1.2))
    label(ax, text, (x, y), ha="center", va="center", fontsize=10)

box(2, 4.8, "1  冠军是甲或丁")
box(10, 4.8, "5  冠军是乙或丙")
ax.add_patch(FancyArrowPatch((3.6, 4.8), (8.4, 4.8),
             arrowstyle="<->", mutation_scale=14, lw=2, color=C.INK))
label(ax, "必然一真一假（矛盾对）", (6, 5.2), ha="center", fontsize=10)
box(2, 2.4, "2  冠军既不是甲\n也不是乙")
box(6, 2.4, "3  冠军是乙或丁")
box(10, 2.4, "4  冠军是乙")
ax.add_patch(FancyArrowPatch((8.45, 2.4), (7.55, 2.4),
             arrowstyle="-|>", mutation_scale=14, lw=1.5, ls="--", color=C.INK))
label(ax, "4 真 ⇒ 3 真", (8, 3.17), ha="center", fontsize=10)
# A downward brace groups exactly statements 2, 3, and 4.
verts = [(0.5, 1.55), (0.5, 1.3), (0.8, 1.2), (3.2, 1.2),
         (5.6, 1.2), (6, 1.15), (6, .86),
         (6, 1.15), (6.4, 1.2), (8.8, 1.2),
         (11.2, 1.2), (11.5, 1.3), (11.5, 1.55)]
ax.add_patch(PathPatch(Path(verts, [Path.MOVETO] + [Path.CURVE4]*12),
             fill=False, edgecolor=C.INK, lw=1.3))
label(ax, "这三句里恰有一句真", (6, .36), ha="center")
save(fig, "K12-n2")

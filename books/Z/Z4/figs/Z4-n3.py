import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle, FancyArrowPatch
from matplotlib.transforms import Affine2D

fig, ax = new_fig(16, 8)
ax.set_xlim(-2.0, 8.7); ax.set_ylim(-1.0, 4.9); ax.axis("off")
for i in range(6):
    x = i*1.25
    if i < 3:
        rect = Rectangle((x-.18, 0), .36, 2.05, facecolor=C.LIGHT, edgecolor=C.INK, lw=1.4)
        rect.set_transform(Affine2D().rotate_deg_around(x, 0, [-27, -20, -14][i]) + ax.transData)
        ax.add_patch(rect)
    else:
        ax.add_patch(Rectangle((x-.18, 0), .36, 2.05, facecolor=C.PAPER, edgecolor=C.INK, lw=1.4))
    label(ax, str(i+1), (x, -.35), ha="center", va="top")
label(ax, "……", (7.7, .8), fontsize=18, ha="center")
arrow(ax, (-1.9, .9), (-.3, .9), color=C.INK, lw=2.8)
label(ax, "奠基：推倒第 1 块\n对应 $P(1)$", (-1.9, 1.15), ha="left", va="bottom")
for i, txt, yy in [(0, "$P(1)\\Rightarrow P(2)$", 3.0), (1, "$P(2)\\Rightarrow P(3)$", 3.5)]:
    ax.add_patch(FancyArrowPatch((i*1.25+.1, 2.45), ((i+1)*1.25+.1, 2.45), connectionstyle="arc3,rad=-.45", arrowstyle="-|>", mutation_scale=13, lw=1.5, color=C.INK))
    label(ax, txt, ((i+.5)*1.25+.1, yy), ha="center", fontsize=9)
ax.plot([-.3, 2.8], [4.05, 4.05], color=C.INK, lw=1.1)
label(ax, "归纳步：任取 $m$，$P(m)\\Rightarrow P(m+1)$，一次证完所有箭头", (1.25, 4.15), ha="center", va="bottom")
for i in range(3, 6):
    x = i*1.25
    ax.plot([x+.3, x+.8], [1.9, 2.4], color=C.GRAY, lw=1.2, ls="--")
save(fig, "Z4-n3")

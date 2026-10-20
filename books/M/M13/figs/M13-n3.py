import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle, Circle

d, k, r = 8, 8, 2
unit = 0.28
fig, ax = new_fig(19, 11)
ax.set_aspect("equal")
ax.set(xlim=(-0.55, 11.3), ylim=(-0.9, 6.6))
ax.axis("off")

def block(x, y, cols, rows, text, fill=C.PAPER):
    width, height = cols*unit, rows*unit
    ax.add_patch(Rectangle((x, y), width, height, facecolor=fill, edgecolor=C.INK, lw=1.2))
    if text:
        label(ax, text, (x+width/2, y+height/2), ha="center", va="center")
    return width, height

block(0, 2.0, 1, k, "")
label(ax, r"$x$", (0.14, 4.55), ha="center")
label(ax, r"$k$", (-0.16, 3.12), ha="right", va="center")
block(3.0, 3.85, k, d, "$W_0$\n"+r"$d\times k$，冻结", C.LIGHT)
label(ax, r"$k$", (4.12, 6.28), ha="center")
label(ax, r"$d$", (2.85, 5.55), ha="right", va="center")
block(3.0, 0.94, k, r, r"$A$  $r\times k$")
label(ax, r"$k$", (4.12, 0.65), ha="center", va="top")
label(ax, r"$r$", (2.85, 1.62), ha="right", va="center")
block(7.0, 0.1, r, d, r"$B$")
label(ax, r"$r$", (7.28, 2.53), ha="center")
label(ax, r"$d$", (7.72, 1.88), va="center")
label(ax, r"$d\times r$", (7.28, -0.15), ha="center", va="top")
ax.add_patch(Rectangle((2.5, -0.52), 5.65, 3.45, fill=False, edgecolor=C.INK, ls="--", lw=1.0))
label(ax, "只训练这里", (5.25, 3.13), ha="center", va="center")

arrow(ax, (0.28, 3.12), (0.97, 0), color=C.INK)
dot(ax, (1.25, 3.12), size=12)
ax.plot([1.25, 1.25, 2.6], [3.12, 4.97, 4.97], color=C.INK, lw=1.2)
arrow(ax, (2.6, 4.97), (0.4, 0), color=C.INK, lw=1.2)
ax.plot([1.25, 1.25, 2.6], [3.12, 1.22, 1.22], color=C.INK, lw=1.2)
arrow(ax, (2.6, 1.22), (0.4, 0), color=C.INK, lw=1.2)
arrow(ax, (5.24, 1.22), (1.76, 0), color=C.INK, lw=1.2)
label(ax, r"$Ax$（$r$ 个分量）", (6.12, 1.58), ha="center", fontsize=9)
ax.plot([5.24, 9.05, 9.05], [4.97, 4.97, 3.85], color=C.INK, lw=1.2)
arrow(ax, (9.05, 3.85), (0, -0.46), color=C.INK, lw=1.2)
ax.plot([7.56, 9.05, 9.05], [1.22, 1.22, 2.4], color=C.INK, lw=1.2)
arrow(ax, (9.05, 2.4), (0, 0.45), color=C.INK, lw=1.2)
ax.add_patch(Circle((9.05, 3.12), 0.27, facecolor=C.PAPER, edgecolor=C.INK))
label(ax, "+", (9.05, 3.12), ha="center", va="center", fontsize=14)
arrow(ax, (9.32, 3.12), (1.0, 0), color=C.INK, lw=1.2)
block(10.32, 2.0, 1, d, "")
label(ax, r"$y$", (10.46, 4.55), ha="center")
label(ax, r"$d$", (10.77, 3.12), va="center")
label(ax, r"$B$ 初始为 0，所以开始时 $y=W_0x$", (5.32, -0.84), ha="center", fontsize=9)
save(fig, "M13-n3")

import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle

n = 3
assert n*n + (2*n+1) == (n+1)**2 == 16
fig, ax = new_fig(11, 9)
ax.set_xlim(-1.2, 4.9); ax.set_ylim(-1.25, 5.0); ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(Rectangle((-.38, .62), 2.76, 2.76, facecolor=C.LIGHT, edgecolor=C.INK, lw=1.4))
for i in range(4):
    for j in range(4):
        x, y = j, 3-i
        if i < 3 and j < 3:
            ax.scatter([x], [y], s=34, color=C.INK, zorder=4)
        else:
            ax.scatter([x], [y], s=42, facecolors=C.PAPER, edgecolors=C.INK, zorder=4)
ax.add_patch(Rectangle((-.5, -.5), 4, 4, fill=False, edgecolor=C.INK, lw=1.5))
label(ax, "$n^2=9$", (1, 1.55), ha="center", va="center")
label(ax, "$2n+1=7$", (4.0, 2.0), rotation=90, ha="center", va="center")
label(ax, "$(n+1)^2=16$", (1.5, 4.42), ha="center")
label(ax, "$1+3+5=3^2$，补上 7 个点得 $4^2$", (1.9, -.93), ha="center", va="top")
save(fig, "Z4-n2")

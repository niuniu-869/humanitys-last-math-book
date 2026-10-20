import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Circle, FancyArrowPatch

fig, ax = new_fig(13, 8)
ax.set_xlim(-2.2, 2.2); ax.set_ylim(-1.9, 2.1); ax.axis("off")
pos = {"活跃": (-1.0, 0.25), "沉默": (1.0, 0.25)}
for name, (x, y) in pos.items():
    ax.add_patch(Circle((x, y), 0.42, facecolor=C.PAPER, edgecolor=C.INK, lw=1.5, zorder=3))
    label(ax, name, (x, y), ha="center", va="center")

def curved(a, b, rad, text, text_xy):
    ax.add_patch(FancyArrowPatch(a, b, connectionstyle=f"arc3,rad={rad}", arrowstyle="-|>",
                                 mutation_scale=12, lw=1.5, color=C.INK, zorder=4))
    label(ax, text, text_xy, ha="center", va="center")

curved((-1.22, 0.58), (-0.78, 0.58), -1.6, "0.8", (-1.0, 1.2))
curved((-0.60, 0.48), (0.60, 0.48), -0.32, "0.2", (0, 1.05))
curved((0.60, 0.02), (-0.60, 0.02), -0.32, "0.3", (0, -0.52))
curved((0.78, -0.17), (1.22, -0.17), 1.6, "0.7", (1.0, -0.98))
label(ax, "活跃出发：0.8 + 0.2 = 1；沉默出发：0.3 + 0.7 = 1", (0, -1.55), ha="center", va="center", fontsize=9)
save(fig, "P9-n1")

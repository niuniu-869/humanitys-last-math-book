import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Circle, FancyArrowPatch

fig, ax = new_fig(10, 8)
ax.set_xlim(-2.0, 2.0); ax.set_ylim(-1.8, 2.1); ax.axis("off")
pos = {"A": (0, 0.95), "B": (1.15, -0.85), "C": (-1.15, -0.85)}
for name, (x, y) in pos.items():
    ax.add_patch(Circle((x, y), 0.36, facecolor=C.PAPER, edgecolor=C.INK, lw=1.5, zorder=3))
    label(ax, name, (x, y), ha="center", va="center")

def edge(a, b, rad, text, text_xy):
    ax.add_patch(FancyArrowPatch(a, b, connectionstyle=f"arc3,rad={rad}", arrowstyle="-|>",
                                 mutation_scale=12, lw=1.5, color=C.INK, zorder=2))
    label(ax, text, text_xy, ha="center", va="center")

edge((0.26, 0.72), (0.95, -0.55), 0.05, "1/2", (0.72, 0.18))
edge((-0.26, 0.72), (-0.95, -0.55), 0.22, "1/2", (-0.80, 0.30))
edge((0.82, -0.92), (-0.82, -0.92), 0.28, "1", (0, -1.35))
edge((-0.95, -0.58), (-0.18, 0.72), 0.22, "1", (-0.20, 0.0))
label(ax, "A：0.4", (0, 1.72), ha="center", va="center")
label(ax, "B：0.2", (1.55, -1.25), ha="center", va="center")
label(ax, "C：0.4", (-1.55, -1.25), ha="center", va="center")
save(fig, "P9-n3")

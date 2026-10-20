import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label


fig, ax = new_fig(14, 6.6)
ax.set_xlim(-1.3, 5.5)
ax.set_ylim(-2.5, 3.2)
ax.axis("off")

# Number line and ticks.
ax.annotate("", xy=(5.1, 0), xytext=(-1.1, 0),
            arrowprops=dict(arrowstyle="-|>", color=C.INK, lw=1.3, mutation_scale=10))
for x in range(0, 5):
    ax.plot([x, x], [-0.10, 0.10], color=C.INK, linewidth=1.2)
    label(ax, str(x), (x, 0), offset=(0, -18), fontsize=10, ha="center")

# Original disjunction: two closed rays.
arrow(ax, (1, 1.85), (-2.1, 0), color=C.INK, lw=3)
arrow(ax, (3, 1.85), (2.1, 0), color=C.INK, lw=3)
ax.scatter([1, 3], [1.85, 1.85], s=48, color=C.INK, zorder=5)
label(ax, r"$x\leq1$ 或 $x\geq3$", (2.0, 2.55), fontsize=11, ha="center")

# Contradictory sentence: open interval, with open endpoints.
ax.plot([1, 3], [-1.15, -1.15], color=C.LIGHT, linewidth=9.0,
        solid_capstyle="round")
ax.plot([1, 3], [-1.15, -1.15], color=C.INK, linewidth=1, linestyle=":")
ax.scatter([1, 3], [-1.15, -1.15], s=62, facecolors=C.PAPER, edgecolors=C.INK,
           linewidths=1.5, zorder=5)
label(ax, r"$1<x<3$（矛盾句）", (3.2, -1.15), fontsize=10.5, ha="left", va="center")

# Compact legend written directly in the figure.
ax.plot([-1.05, -0.60], [-2.12, -2.12], color=C.INK, linewidth=3)
label(ax, "实线射线：原句成立", (-0.48, -2.12), fontsize=9, va="center")
ax.plot([2.25, 2.70], [-2.12, -2.12], color=C.LIGHT, linewidth=9)
ax.plot([2.25, 2.70], [-2.12, -2.12], color=C.INK, linewidth=1, linestyle=":")
label(ax, "阴影线段：矛盾句成立", (2.82, -2.12), fontsize=9, va="center")

save(fig, "Z1-n3")

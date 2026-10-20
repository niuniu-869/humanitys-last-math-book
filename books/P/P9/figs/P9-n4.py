import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Circle, FancyArrowPatch

fig, axes = new_fig(18, 8, ncols=3)

def node(ax, x, y, name, absorbing=False):
    ax.add_patch(Circle((x, y), 0.22, facecolor=C.PAPER, edgecolor=C.INK, lw=1.2, zorder=3))
    if absorbing:
        ax.add_patch(Circle((x, y), 0.29, facecolor="none", edgecolor=C.INK, lw=0.9, zorder=3))
    label(ax, name, (x, y), ha="center", va="center", fontsize=9)

def edge(ax, a, b, rad, text, xy):
    ax.add_patch(FancyArrowPatch(a, b, connectionstyle=f"arc3,rad={rad}", arrowstyle="-|>", mutation_scale=9,
                                 lw=1.2, color=C.INK, zorder=2))
    label(ax, text, xy, ha="center", va="center", fontsize=8)

ax = axes[0]; ax.set_xlim(-1.1, 1.1); ax.set_ylim(-1.8, 1.9); ax.axis("off")
label(ax, "来回摆（周期 2）", (0, 1.62), ha="center", va="center")
label(ax, "从 (1, 0) 出发；柱形依次为状态 1、2", (0, -1.72), ha="center", va="center", fontsize=8)
node(ax, -0.52, 0.72, "1"); node(ax, 0.52, 0.72, "2")
edge(ax, (-0.28, 0.72), (0.28, 0.72), 0, "1", (0, 0.93)); edge(ax, (0.28, 0.58), (-0.28, 0.58), 0, "1", (0, 0.37))
for i, vals in enumerate([(1, 0), (0, 1), (1, 0)]):
    x = -0.75 + i * 0.75; ax.bar([x - 0.11, x + 0.11], vals, bottom=-1.22, width=0.18, color=[C.INK, C.PAPER], edgecolor=C.INK, linewidth=0.8)
    label(ax, f"n={i}", (x, -1.34), ha="center", va="top", fontsize=8)

ax = axes[1]; ax.set_xlim(-1.1, 1.1); ax.set_ylim(-1.45, 1.9); ax.axis("off")
label(ax, "出不来（两个吸收态）", (0, 1.62), ha="center", va="center")
node(ax, -0.52, 0.72, "1", True); node(ax, 0.52, 0.72, "2", True)
edge(ax, (-0.70, 0.93), (-0.34, 0.93), -1.5, "1", (-0.52, 1.25)); edge(ax, (0.34, 0.93), (0.70, 0.93), -1.5, "1", (0.52, 1.25))
label(ax, "没有与起点无关的共同极限", (0, -1.05), ha="center", va="center", fontsize=9)

ax = axes[2]; ax.set_xlim(-1.25, 1.25); ax.set_ylim(-1.75, 1.9); ax.axis("off")
label(ax, "正常（不可约、非周期）", (0, 1.62), ha="center", va="center")
node(ax, -0.72, 0.72, "1"); node(ax, 0.72, 0.72, "2"); node(ax, 0, -0.05, "3")
edge(ax, (-0.49, 0.72), (0.49, 0.72), 0, "1/2", (0, 0.94)); edge(ax, (-0.80, 0.50), (-0.60, 0.50), 1.4, "1/2", (-0.72, 0.17))
edge(ax, (0.58, 0.52), (0.16, 0.18), 0, "1", (0.48, 0.28)); edge(ax, (-0.17, 0.16), (-0.58, 0.52), 0, "1", (-0.42, 0.25))
dist = [(1, 0, 0), (0.5, 0.5, 0), (0.25, 0.25, 0.5), (0.625, 0.125, 0.25)]
for i, vals in enumerate(dist):
    x = -0.98 + i * 0.65
    ax.bar([x - 0.13, x, x + 0.13], vals, bottom=-1.30, width=0.11, color=[C.INK, C.GRAY, C.PAPER], edgecolor=C.INK, linewidth=0.7)
    label(ax, f"n={i}", (x, -1.43), ha="center", va="top", fontsize=7.5)
label(ax, "趋于 (0.5, 0.25, 0.25)；柱形依次为状态 1、2、3", (0.0, -1.72), ha="center", va="center", fontsize=8.5)
save(fig, "P9-n4")

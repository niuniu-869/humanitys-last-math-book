import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle

fig, ax = new_fig(10.5, 7.6)
ax.axhline(0, color=C.INK, lw=1.5)
label(ax, "水面", (5.3, 0), offset=(0, 8))
x0 = 2.2
ax.add_patch(Rectangle((x0, -4), 4.0, 3.0, facecolor=C.LIGHT, edgecolor=C.INK, lw=1.5))
ax.plot([x0, x0], [-4, -1], color=C.INK, lw=2.0)
# 深度轴向下
ax.annotate("", xy=(0.0, -4.35), xytext=(0.0, -0.05), arrowprops=dict(arrowstyle="-|>", color=C.INK, lw=1.2))
label(ax, "深度 $x$（向下）", (0.0, -2.2), offset=(-6, 0), rotation=90, va="center", ha="right")
# 窄条：深度 2.8 到 3.0
ax.fill_between([x0, x0+4], [-3.0, -3.0], [-2.8, -2.8], color=C.GRAY, alpha=0.85)
label(ax, "窄条，宽 $w$", (x0+2, -2.8), offset=(0, 7), ha="center")
label(ax, r"$\mathrm{d}x$", (x0+4, -2.9), offset=(6, 0), va="center")
# 压强箭头：深度 1,2,3,4，长度与深度成正比
for d in (1, 2, 3, 4):
    arrow(ax, (x0-d, -d), (d-0.12, 0), color=C.INK, lw=1.4)
ax.plot([x0, x0-4], [0, -4], color=C.INK, ls="--", lw=1.1)
label(ax, r"压强 $\rho gx$", (-2.8, -0.7), ha="left", va="center")
ax.set(xlim=(-3.0, 7.0), ylim=(-4.7, 0.7), aspect="equal")
ax.set_xticks([]); ax.set_yticks([])
save(fig, "C13-n7")

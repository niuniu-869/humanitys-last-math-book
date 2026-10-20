import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Ellipse, Polygon

fig, ax = new_fig(11.5, 7.6)
x = np.linspace(0, 2.3, 500); f = 0.6 + 0.35*x**2
ax.plot(x, f, color=C.INK, lw=1.5, zorder=3)
ax.plot(x, -f, color=C.INK, ls=":", lw=1.2, zorder=3)
arrow(ax, (0, 0), (2.55, 0), color=C.INK, lw=1.4)
label(ax, "旋转轴", (2.0, 0.03), offset=(0, 9), ha="left", va="bottom")

x1, x2 = 1.2, 1.75
y1, y2 = 0.6 + 0.35*x1**2, 0.6 + 0.35*x2**2

# 圆台侧面：两端椭圆之间的整条带子，浅灰填充
ax.add_patch(Polygon([[x1, y1], [x2, y2], [x2, -y2], [x1, -y1]], closed=True,
                     facecolor=C.LIGHT, edgecolor="none", zorder=1))
# 宽 dx 的圆柱侧面轮廓：上下两条水平虚线（比圆台窄）
ax.plot([x1, x2], [y1, y1], color=C.INK, ls="--", lw=1.1, zorder=2)
ax.plot([x1, x2], [-y1, -y1], color=C.INK, ls="--", lw=1.1, zorder=2)
# 圆台两端椭圆（实线）及半径辅助线
for xc, yc in ((x1, y1), (x2, y2)):
    ax.add_patch(Ellipse((xc, 0), 0.16, 2*yc, fill=False, edgecolor=C.INK,
                         lw=1.2, zorder=4))
    ax.plot([xc, xc], [0, yc], color=C.INK, lw=0.8, zorder=2)
# 斜高 ds 对应的一小段加粗；竖直直角边 dy
ax.plot([x1, x2], [y1, y2], color=C.INK, lw=2.8, zorder=5)
ax.plot([x2, x2], [y1, y2], color=C.INK, lw=0.8, zorder=4)

label(ax, "$y$", (x1, y1/2), offset=(-9, 0), ha="right", va="center")
label(ax, r"$y+\mathrm{d}y$", (x2, y2), offset=(8, -2), ha="left", va="center")
label(ax, r"圆台：斜高 $\mathrm{d}s$", (0.85, 1.95), ha="center")
label(ax, r"圆柱：宽 $\mathrm{d}x$", (-0.95, 1.0), ha="left")

ax.set(xlim=(-1.15, 2.85), ylim=(-2.6, 2.75), aspect="equal")
ax.set_xticks([]); ax.set_yticks([])
save(fig, "C13-n6")

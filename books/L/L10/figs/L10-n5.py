import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Polygon

# 在 a1,a2 张成的平面里取正交坐标：横轴沿 b1，纵轴沿 b2
r2, r6 = np.sqrt(2), np.sqrt(6)
b1 = np.array([r2, 0.0])            # = a1
a2 = np.array([r2 / 2, r6 / 2])     # (0.707, 1.225)
pr = np.array([r2 / 2, 0.0])        # 投影 (1/2) b1
b2 = a2 - pr                        # (0, 1.225)

fig, ax = new_fig(10.5, 8.6)
ax.set_aspect("equal", adjustable="box")
ax.set_xlim(-1.0, 2.0); ax.set_ylim(-0.42, 1.65)
ax.axis("off")
ax.add_patch(Polygon([(-0.95, -0.36), (1.85, -0.36), (1.85, 1.55), (-0.95, 1.55)], closed=True,
                     facecolor=C.LIGHT, edgecolor=C.GRAY, lw=0.8, alpha=0.55, zorder=0))
label(ax, "$\\boldsymbol{a}_1,\\boldsymbol{a}_2$ 张成的平面", (1.8, 1.5), color=C.INK, ha="right", va="top", fontsize=8.5)

arrow(ax, (0, 0), b1, color=C.INK, lw=1.8)
label(ax, "$\\boldsymbol{b}_1=\\boldsymbol{a}_1$", b1, offset=(4, -12), color=C.INK, ha="left")
arrow(ax, (0, 0), a2, color=C.INK, lw=1.8)
label(ax, "$\\boldsymbol{a}_2$", a2, offset=(6, 2), color=C.INK, ha="left")
# 投影：粗点线
ax.plot([0, pr[0]], [0, 0], color=C.INK, lw=3.2, ls=":", zorder=4)
ax.scatter(*pr, s=26, color=C.INK, zorder=5)
label(ax, "投影 $\\frac{1}{2}\\boldsymbol{b}_1$", pr, offset=(0, -10), color=C.INK, ha="center", va="top", fontsize=8.5)
# 减去投影后剩下的部分：虚线
ax.plot([pr[0], a2[0]], [pr[1], a2[1]], color=C.INK, lw=1.6, ls="--", zorder=3)
label(ax, "减去投影后\n剩下的部分", (pr[0], 0.62), offset=(8, 0), color=C.INK, ha="left", va="center", fontsize=8.5)
s = 0.09
ax.plot([pr[0] + s, pr[0] + s, pr[0]], [0, s, s], color=C.INK, lw=1.0, zorder=5)
# b2：粗实线箭头
arrow(ax, (0, 0), b2, color=C.INK, lw=2.6)
label(ax, "$\\boldsymbol{b}_2=\\boldsymbol{a}_2-\\frac{1}{2}\\boldsymbol{b}_1$", b2, offset=(-6, 4), color=C.INK, ha="right", va="bottom")
ax.plot([s, s, 0], [0, s, s], color=C.INK, lw=1.0, zorder=5)
# 平行四边形示意：浅灰细线
ax.plot([b2[0], a2[0]], [b2[1], a2[1]], color=C.GRAY, lw=0.8, zorder=2)
label(ax, "$O$", (0, 0), offset=(-6, -6), color=C.INK, ha="right", va="top")
save(fig, "L10-n5")

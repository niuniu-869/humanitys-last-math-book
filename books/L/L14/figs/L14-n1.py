import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(11.5, 9.2)

q1 = np.array([2.0, -1.0]) / np.sqrt(5.0)
q2 = np.array([1.0, 2.0]) / np.sqrt(5.0)
origin = np.zeros(2)

# 原坐标轴：细实线
ax.plot([-3, 3], [0, 0], color=C.GRAY, lw=0.9, zorder=1)
ax.plot([0, 0], [-3, 3], color=C.GRAY, lw=0.9, zorder=1)
label(ax, r"$x$", (2.95, 0), offset=(-2, 5), color=C.INK, ha="right")
label(ax, r"$y$", (0, 2.95), offset=(5, -2), color=C.INK, va="top")

# 主轴方向与椭圆
for q in (q1, q2):
    p = 3.0 * q
    ax.plot([-p[0], p[0]], [-p[1], p[1]], color=C.GRAY, lw=1.0, ls="--", zorder=1)

t = np.linspace(0, 2 * np.pi, 500)
ellipse = np.sqrt(6.0) * np.cos(t)[:, None] * q1 + np.sin(t)[:, None] * q2
ax.plot(ellipse[:, 0], ellipse[:, 1], color=C.BLUE, lw=2.2, zorder=3)

# 单位方向箭头
arrow(ax, origin, q1, color=C.RED, lw=1.7)
arrow(ax, origin, q2, color=C.RED, lw=1.7)

# 主轴标签和半轴长度
label(ax, r"$\boldsymbol{q}_1$", q1, offset=(6, -12), color=C.INK)
label(ax, r"$y_1$ 轴", (2.72 * q1[0], 2.72 * q1[1]), offset=(-26, -20), color=C.INK)
label(ax, r"$y_2$ 轴", (2.72 * q2[0], 2.72 * q2[1]), offset=(5, -4), color=C.INK)
label(ax, r"$\sqrt{6}$", (1.25 * q1[0], 1.25 * q1[1]), offset=(5, 6), color=C.INK)
label(ax, r"$1$", (0.58 * q2[0], 0.58 * q2[1]), offset=(6, -2), color=C.INK)

# 半轴端点：q1 方向实心，q2 方向空心
p1 = np.sqrt(6.0) * q1
p2 = q2
ax.scatter([p1[0], -p1[0]], [p1[1], -p1[1]], s=30, color=C.INK, zorder=5)
ax.scatter([p2[0], -p2[0]], [p2[1], -p2[1]], s=34, facecolors=C.PAPER, edgecolors=C.INK, linewidths=1.3, zorder=5)
label(ax, r"$\sqrt{6}\,\boldsymbol{q}_1$", p1, offset=(6, 6), color=C.INK)
label(ax, r"$-\sqrt{6}\,\boldsymbol{q}_1$", -p1, offset=(-8, -13), color=C.INK, ha="right")
label(ax, r"$\boldsymbol{q}_2$", p2, offset=(7, 5), color=C.INK)
label(ax, r"$-\boldsymbol{q}_2$", -p2, offset=(-7, -13), color=C.INK, ha="right")

ax.set_aspect("equal")
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_xticks([-2, 0, 2])
ax.set_yticks([-2, 0, 2])
ax.set_xlabel("")
ax.set_ylabel("")
save(fig, "L14-n1")

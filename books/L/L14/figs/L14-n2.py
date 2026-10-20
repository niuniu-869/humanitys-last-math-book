import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(11.2, 8.5)

q1 = np.array([2.0, -1.0]) / np.sqrt(5.0)
q2 = np.array([1.0, 2.0]) / np.sqrt(5.0)

a = np.linspace(-2.7, 2.7, 2)
for q in (q1, q2):
    p = 2.7 * q
    ax.plot([-p[0], p[0]], [-p[1], p[1]], color=C.LIGHT, lw=1.0, zorder=1)

# 三条闭曲线：实线、点线、虚线
th = np.linspace(0, 2 * np.pi, 600)
circle = np.column_stack((np.cos(th), np.sin(th)))
ax.plot(circle[:, 0], circle[:, 1], color=C.BLUE, lw=2.0, ls="-", zorder=3)

f1 = np.cos(th)[:, None] * q1 + (1 / np.sqrt(6.0)) * np.sin(th)[:, None] * q2
f6 = np.sqrt(6.0) * np.cos(th)[:, None] * q1 + np.sin(th)[:, None] * q2
ax.plot(f1[:, 0], f1[:, 1], color=C.RED, lw=1.7, ls=":", zorder=2)
ax.plot(f6[:, 0], f6[:, 1], color=C.TEAL, lw=1.7, ls="--", zorder=2)

# 曲线标签
label(ax, "单位圆", (0.72, 0.70), offset=(4, 4), color=C.BLUE)
label(ax, r"$f=1$", (0.83 * q1[0], 0.83 * q1[1]), offset=(-8, 8), color=C.RED)
label(ax, r"$f=6$", (2.10 * q1[0], 2.10 * q1[1]), offset=(5, 4), color=C.TEAL)
label(ax, r"$\boldsymbol{q}_1$", (2.35 * q1[0], 2.35 * q1[1]), offset=(4, -3), color=C.INK)
label(ax, r"$\boldsymbol{q}_2$", (2.35 * q2[0], 2.35 * q2[1]), offset=(4, 3), color=C.INK)

# 切点：最小值处实心，最大值处空心
p1 = q1
p2 = q2
ax.scatter([p1[0], -p1[0]], [p1[1], -p1[1]], s=30, color=C.INK, zorder=5)
ax.scatter([p2[0], -p2[0]], [p2[1], -p2[1]], s=34, facecolors=C.PAPER, edgecolors=C.INK, linewidths=1.3, zorder=5)
label(ax, "最小 1", p1, offset=(7, -13), color=C.INK)
label(ax, "最小 1", -p1, offset=(-7, 7), color=C.INK, ha="right")
label(ax, "最大 6", p2, offset=(7, 6), color=C.INK)
label(ax, "最大 6", -p2, offset=(-7, -14), color=C.INK, ha="right")

ax.set_aspect("equal")
ax.set_xlim(-2.7, 2.7)
ax.set_ylim(-2.7, 2.7)
ax.set_xticks([-2, -1, 0, 1, 2])
ax.set_yticks([-2, -1, 0, 1, 2])
ax.set_xlabel("$x$")
ax.set_ylabel("$y$")
save(fig, "L14-n2")

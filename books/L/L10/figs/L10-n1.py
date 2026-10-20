import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, save, arrow, dot, label
from matplotlib.patches import Polygon

# 用斜投影在平面上画：平行四边形代表过原点的子空间 S，竖直方向代表垂直于 S 的方向
fig, ax = new_fig(12, 7.2)
ax.set_aspect("equal")
ax.set_axis_off()
ax.set_xlim(-0.3, 8.0)
ax.set_ylim(-0.3, 4.9)

plane = np.array([[0.0, 0.0], [6.0, 0.0], [7.6, 2.3], [1.6, 2.3]])
ax.add_patch(Polygon(plane, closed=True, facecolor=C.LIGHT, edgecolor=C.GRAY, lw=1.0, zorder=1))
label(ax, r"$S=C(A)$", (1.75, 1.85), color=C.INK)

O = np.array([1.2, 0.55])
p = np.array([4.1, 1.0])
q = np.array([5.9, 1.75])
b = np.array([4.1, 4.4])

arrow(ax, O, p - O, color=C.GRAY, lw=1.3)          # O 到垂足 p
arrow(ax, p, b - p, color=C.INK, lw=2.6)           # 残差 e，粗实线
ax.plot([p[0], q[0]], [p[1], q[1]], color=C.INK, lw=1.6, ls=":", zorder=3)   # 平面内 p-q，点线
ax.plot([q[0], b[0]], [q[1], b[1]], color=C.INK, lw=1.6, ls="--", zorder=3)  # 斜边 b-q，虚线

# p 处两个直角标记：e 垂直于平面内的 p-q 方向，也垂直于 O-p 方向
v = np.array([0.0, 1.0])
for w in (q - p, O - p):
    u = w / np.linalg.norm(w)
    s = 0.32
    pts = np.array([p + s * u, p + s * u + s * v, p + s * v])
    ax.plot(pts[:, 0], pts[:, 1], color=C.INK, lw=1.0, zorder=4)

dot(ax, O, color=C.INK, size=22)
dot(ax, p, color=C.INK, size=30)
dot(ax, b, color=C.INK, size=30)
ax.scatter(*q, s=40, facecolors=C.PAPER, edgecolors=C.INK, linewidths=1.5, zorder=5)

label(ax, "$O$", O, offset=(-12, -10))
label(ax, r"$\boldsymbol{p}=A\hat{\boldsymbol{x}}$", p, offset=(-14, -17))
label(ax, r"$\boldsymbol{b}$", b, offset=(7, 0))
label(ax, r"$\boldsymbol{q}$", q, offset=(7, -8))
label(ax, r"$\boldsymbol{e}=\boldsymbol{b}-\boldsymbol{p}$", (p + b) / 2, offset=(-62, 4))
label(ax, r"$\boldsymbol{p}-\boldsymbol{q}$", (p + q) / 2, offset=(-4, -16))
label(ax, r"$\Vert\boldsymbol{b}-\boldsymbol{q}\Vert$（斜边）", (q + b) / 2, offset=(9, 6))

save(fig, "L10-n1")

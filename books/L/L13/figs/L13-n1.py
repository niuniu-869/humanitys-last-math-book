import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Polygon

A = np.array([[2.0, 1.0], [1.0, 2.0]])
q1 = np.array([1.0, 1.0]) / np.sqrt(2.0)
q2 = np.array([1.0, -1.0]) / np.sqrt(2.0)
origin = np.zeros(2)

fig, ax = new_fig(12.5, 10.0)
ax.set_aspect("equal", adjustable="box")
ax.set_xlim(-3.3, 3.3)
ax.set_ylim(-3.3, 3.3)
ax.set_xticks(np.arange(-3, 4, 1))
ax.set_yticks(np.arange(-3, 4, 1))
ax.axhline(0, color=C.GRAY, lw=0.9, zorder=1)
ax.axvline(0, color=C.GRAY, lw=0.9, zorder=1)
label(ax, "$x$", (3.25, 0), offset=(-2, 5), color=C.INK, ha="right")
label(ax, "$y$", (0, 3.25), offset=(5, -2), color=C.INK, va="top")

# 主轴方向：两条互相垂直的虚线
for q in (q1, q2):
    p = 3.25 * q
    ax.plot([-p[0], p[0]], [-p[1], p[1]], color=C.GRAY, lw=1.0, ls="--", zorder=1)

# 单位圆与其像椭圆
t = np.linspace(0, 2 * np.pi, 600)
circle = np.column_stack((np.cos(t), np.sin(t)))
ellipse = (A @ circle.T).T
ax.add_patch(Polygon(ellipse, closed=True, facecolor=C.LIGHT, edgecolor="none", alpha=0.72, zorder=2))
ax.plot(circle[:, 0], circle[:, 1], color=C.GRAY, lw=1.2, zorder=3)
ax.plot(ellipse[:, 0], ellipse[:, 1], color=C.INK, lw=2.6, zorder=4)

# 原点附近的直角标记（沿 q1、q2 两方向）
s = 0.18
right_angle = np.array([s * q1, s * q1 + s * q2, s * q2])
ax.plot(right_angle[:, 0], right_angle[:, 1], color=C.GRAY, lw=1.0, zorder=5)

# 特征向量及其像：细箭头与粗箭头分层绘制
arrow(ax, origin, q1, color=C.GRAY, lw=1.25)
label(ax, r"$\boldsymbol{q}_1$", q1, offset=(-24, 2), color=C.INK)
arrow(ax, origin, q2, color=C.GRAY, lw=1.25)
aq1 = 3.0 * q1
aq2 = q2.copy()
arrow(ax, origin, aq1, color=C.INK, lw=2.4)
label(ax, r"$A\boldsymbol{q}_1=3\boldsymbol{q}_1$", aq1, offset=(6, 7), color=C.INK)
arrow(ax, origin, aq2, color=C.INK, lw=2.4)
label(ax, r"$A\boldsymbol{q}_2=\boldsymbol{q}_2$", aq2, offset=(6, -27), color=C.INK)

# 对照点 e1 与其像：空心圆、实心方块，点线箭头表示方向改变
e1 = np.array([1.0, 0.0])
Ae1 = A @ e1
ax.scatter(*e1, s=52, facecolors=C.PAPER, edgecolors=C.INK, linewidths=1.5, zorder=6)
label(ax, r"$\boldsymbol{e}_1$", e1, offset=(-4, 9), color=C.INK, ha="right")
ax.scatter(*Ae1, s=52, marker="s", color=C.INK, zorder=6)
label(ax, r"$A\boldsymbol{e}_1=(2,1)$", Ae1, offset=(7, 6), color=C.INK)
ax.annotate("", xy=Ae1, xytext=e1,
            arrowprops=dict(arrowstyle="-|>", color=C.GRAY, lw=1.25, linestyle=":",
                            shrinkA=5, shrinkB=7, mutation_scale=10), zorder=5)
label(ax, "方向改变了", (1.62, -0.42), offset=(0, 0), color=C.INK, ha="left")

save(fig, "L13-n1")

import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Polygon, Arc

fig, ax = new_fig(13, 8)
ax.set_aspect("equal", adjustable="box")

p0 = np.array([0.0, 0.0]); p1 = np.array([0.6, 1.6])
v = np.array([1.4, 0.0]); q0, q1 = p0 + v, p1 + v
ax.add_patch(Polygon([p0, p1, q1, q0], closed=True, facecolor=C.LIGHT,
                     edgecolor=C.INK, linewidth=1.5, alpha=0.75))
ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=C.INK, lw=3.0, solid_capstyle="round")
ax.plot([q0[0], q1[0]], [q0[1], q1[1]], color=C.INK, lw=1.5)
arrow(ax, p0, v, color=C.INK, lw=1.5)
arrow(ax, p1, v, color=C.INK, lw=1.5)
label(ax, r"$\boldsymbol{v}$", p0 + 0.5 * v, offset=(0, -14), ha="center")
label(ax, "网（面积 $A$）", p0 + 0.3 * (p1 - p0), offset=(-10, 0), ha="right")
# 标签移到平行四边形内部偏左的空白处，不再切断右边的边
label(ax, "一秒内穿过的水", np.array([1.06, 1.15]), ha="center")

# n：垂直于网的单位向量（虚线箭头），从网的中点出发
perp = np.array([1.6, -0.6]); n = perp / np.linalg.norm(perp)
mid = 0.5 * (p0 + p1)
tip = mid + n
ax.plot([mid[0], tip[0]], [mid[1], tip[1]], color=C.INK, lw=1.4, ls="--")
arrow(ax, mid + 0.82 * n, 0.18 * n, color=C.INK, lw=1.4)
label(ax, r"$\boldsymbol{n}$", tip, offset=(12, 12), ha="left")

# 高：从网中点沿 n 一直作到平行四边形远端边的垂线段（点线，与 n 共线）
height = np.dot(q0 - mid, n)          # = ||v|| cosθ
foot = mid + height * n
ax.plot([mid[0], foot[0]], [mid[1], foot[1]], color=C.INK, ls=":", lw=1.4)
label(ax, r"高 $\Vert\boldsymbol{v}\Vert\cos\theta$", np.array([0.75, 0.29]),
      ha="center", va="center")

# θ：n 与从网中点水平向右的 v 方向之间的夹角
ang_n = np.degrees(np.arctan2(n[1], n[0]))
ax.plot([mid[0], mid[0] + 0.42], [mid[1], mid[1]], color=C.INK, lw=0.9, ls=":")
ax.add_patch(Arc(mid, 0.9, 0.9, angle=0, theta1=ang_n, theta2=0, color=C.INK, lw=1.1))
label(ax, r"$\theta$", mid + 0.50 * np.array([np.cos(np.radians(ang_n / 2)),
                                             np.sin(np.radians(ang_n / 2))]),
      offset=(2, 2), ha="left")

ax.set_xlim(-0.45, 2.05); ax.set_ylim(-0.45, 2.05)
ax.set_xticks([]); ax.set_yticks([])
for spine in ax.spines.values(): spine.set_visible(False)
save(fig, "C28-n2")

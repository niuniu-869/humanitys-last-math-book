import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Polygon

# A 的特征向量与特征值
p1 = np.array([1.0, 1.0])
p2 = np.array([1.0, -2.0])
A = np.array([[4.0, 1.0], [2.0, 3.0]])

fig, (ax1, ax2) = new_fig(17.5, 7.3, ncols=2)

# 左：标准基中的单位方格及其像
ax1.set_aspect("equal", adjustable="box")
ax1.set_xlim(-0.5, 5.5)
# 请求中的上限 4 会裁掉像的顶点 (5,5)，故扩展到 5.6 以完整显示图形。
ax1.set_ylim(-0.5, 5.6)
ax1.set_xticks(np.arange(0, 6, 1))
ax1.set_yticks(np.arange(0, 6, 1))
ax1.grid(True, color=C.LIGHT, lw=0.7, alpha=0.65, zorder=0)
ax1.axhline(0, color=C.GRAY, lw=0.9, zorder=1)
ax1.axvline(0, color=C.GRAY, lw=0.9, zorder=1)
ax1.set_xlabel("$x$")
ax1.set_ylabel("$y$")
ax1.set_title("标准基：格子被拧斜")

unit = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])
image = (A @ unit.T).T
ax1.add_patch(Polygon(unit, closed=True, facecolor=C.LIGHT, edgecolor=C.GRAY,
                      linewidth=1.1, zorder=2))
ax1.plot(*np.vstack([image, image[0]]).T, color=C.INK, lw=2.6, zorder=3)
arrow(ax1, np.array([0.0, 0.0]), A[:, 0], color=C.GRAY, lw=1.5, offset=(5, 5))
label(ax1, r"$\boldsymbol{e}_1\mapsto(4,2)$", A[:, 0], offset=(4, 6), color=C.GRAY)
arrow(ax1, np.array([0.0, 0.0]), A[:, 1], color=C.GRAY, lw=1.5, offset=(5, 5))
label(ax1, r"$\boldsymbol{e}_2\mapsto(1,3)$", A[:, 1], offset=(4, 6), color=C.GRAY)
label(ax1, "单位方格", (0.5, 0.5), offset=(0, 0), ha="center", va="center", color=C.INK)
label(ax1, "像", (4.25, 4.35), offset=(0, 0), ha="center", va="center", color=C.INK)

# 右：以 p1,p2 为基的斜网格
ax2.set_aspect("equal", adjustable="box")
ax2.set_xlim(-1.0, 8.0)
ax2.set_ylim(-5.0, 6.0)
ax2.set_xticks(np.arange(-1, 9, 1))
ax2.set_yticks(np.arange(-5, 7, 1))
ax2.grid(True, color=C.LIGHT, lw=0.55, alpha=0.45, zorder=0)
ax2.axhline(0, color=C.GRAY, lw=0.8, zorder=1)
ax2.axvline(0, color=C.GRAY, lw=0.8, zorder=1)
ax2.set_xlabel("$x$")
ax2.set_ylabel("$y$")
ax2.set_title("特征向量作基：只沿格线伸缩")

# 斜网格：v=常数时平行 p1，u=常数时平行 p2
s = np.linspace(-8, 8, 2)
for v in range(-4, 6):
    pts = np.outer(s, p1) + v * p2
    ax2.plot(pts[:, 0], pts[:, 1], color=C.LIGHT, lw=0.8, ls="--", zorder=1)
for u in range(-6, 9):
    pts = u * p1 + np.outer(s, p2)
    ax2.plot(pts[:, 0], pts[:, 1], color=C.LIGHT, lw=0.8, ls="--", zorder=1)

orig = np.array([[0.0, 0.0], p1, p1 + p2, p2])
image2 = np.array([[0.0, 0.0], 5 * p1, 5 * p1 + 2 * p2, 2 * p2])
ax2.add_patch(Polygon(orig, closed=True, facecolor=C.LIGHT, edgecolor=C.GRAY,
                      linewidth=1.1, zorder=2))
ax2.plot(*np.vstack([image2, image2[0]]).T, color=C.INK, lw=2.8, zorder=3)

arrow(ax2, np.array([0.0, 0.0]), p1, color=C.GRAY, lw=1.4, offset=(4, 5))
label(ax2, r"$\boldsymbol{p}_1$", p1, offset=(4, 5), color=C.GRAY)
arrow(ax2, np.array([0.0, 0.0]), p2, color=C.GRAY, lw=1.4, offset=(4, -12))
label(ax2, r"$\boldsymbol{p}_2$", p2, offset=(4, -12), color=C.GRAY)
arrow(ax2, np.array([0.0, 0.0]), 5 * p1, color=C.INK, lw=2.1, offset=(4, 5))
label(ax2, r"$5\boldsymbol{p}_1$", 5 * p1, offset=(4, 5), color=C.INK)
arrow(ax2, np.array([0.0, 0.0]), 2 * p2, color=C.INK, lw=2.1, offset=(4, -12))
label(ax2, r"$2\boldsymbol{p}_2$", 2 * p2, offset=(4, -12), color=C.INK)

# 同一格点在变换前后的对应关系：实心圆到实心方块，点线箭头连接
x = p1 + p2
Ax = A @ x
ax2.scatter(*x, s=42, color=C.INK, zorder=5)
label(ax2, "坐标 (1,1)", x, offset=(7, 6), color=C.INK)
ax2.scatter(*Ax, s=52, marker="s", color=C.INK, zorder=5)
label(ax2, "坐标 (5,2)", Ax, offset=(7, 6), color=C.INK)
ax2.annotate("", xy=Ax, xytext=x,
             arrowprops=dict(arrowstyle="-|>", color=C.GRAY, lw=1.4, linestyle=":",
                             shrinkA=5, shrinkB=7, mutation_scale=10), zorder=4)

save(fig, "L12-n1")

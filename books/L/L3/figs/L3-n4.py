import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Polygon, FancyArrowPatch
from matplotlib.path import Path


def matrix_title(ax, title, entries, factor=""):
    ax.text(0.5, 1.27, title, transform=ax.transAxes, ha="center", color=C.INK)
    for i in range(2):
        for j in range(2):
            ax.text(0.45+0.12*j, 1.16-0.075*i, f"${entries[i][j]}$",
                    transform=ax.transAxes, ha="center", va="center", color=C.INK)
    for x, sign in ((0.36, 1), (0.66, -1)):
        ax.plot([x+0.025*sign, x, x, x+0.025*sign], [1.20, 1.20, 1.045, 1.045],
                transform=ax.transAxes, clip_on=False, color=C.INK, lw=0.8)
    if factor:
        ax.text(0.30, 1.12, factor, transform=ax.transAxes, ha="center", va="center", color=C.INK)


def setup(ax, matrix, projection=False):
    ax.set(xlim=(-2, 3), ylim=(-2, 3), aspect="equal")
    ax.set_xticks(range(-2, 4))
    ax.set_yticks(range(-2, 4))
    ax.tick_params(labelsize=8, length=2)
    for k in range(-2, 4):
        ax.axvline(k, color=C.LIGHT, lw=0.6, ls="--", zorder=0)
        ax.axhline(k, color=C.LIGHT, lw=0.6, ls="--", zorder=0)
    # Rank-one projection sends all grid lines onto y=x.
    if not projection:
        for k in range(-3, 4):
            for fixed, direction in ((matrix[:, 0], matrix[:, 1]), (matrix[:, 1], matrix[:, 0])):
                p = k*fixed + np.array([-20, 20])[:, None]*direction
                ax.plot(*p.T, color=C.LIGHT, lw=0.6, ls="-", zorder=0.5)
    ax.axhline(0, color=C.GRAY, lw=0.8, zorder=1)
    ax.axvline(0, color=C.GRAY, lw=0.8, zorder=1)
    label(ax, "$x$", (2.85, 0), offset=(0, -15), ha="right")
    label(ax, "$y$", (0, 2.85), offset=(6, 0), va="top")
    if not projection:
        ax.add_patch(Polygon(square @ matrix.T, facecolor=C.LIGHT, edgecolor=C.INK, lw=1.2, zorder=2))
    ax.plot(*np.vstack((square, square[0])).T, color=C.GRAY, ls="--", lw=1, zorder=3)
    for j in range(2):
        ax.annotate("", xy=matrix[:, j], xytext=(0, 0), arrowprops=dict(
            arrowstyle="-|>", color=C.INK, lw=2.3 if j == 0 else 1.7,
            linestyle="-" if j == 0 else "--", shrinkA=0, shrinkB=0,
            mutation_scale=12), zorder=5)


S = np.array([[1, 1], [0, 1]])
R = np.array([[0, -1], [1, 0]])
P = np.ones((2, 2))/2
square = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])
assert np.array_equal(R @ [2, 1], [-1, 2])
assert np.array_equal(P @ [1, 0], [.5, .5])
assert np.array_equal(P @ [-1, 1], [0, 0])
assert np.array_equal(P @ [1, 1], [1, 1])
assert np.linalg.det(S) == 1

fig, axes = new_fig(30, 12, ncols=3)
fig.subplots_adjust(left=0.04, right=0.99, bottom=0.12, top=0.72, wspace=0.27)
for ax, m in zip(axes, (S, R, P)):
    setup(ax, m, projection=(m is P))
matrix_title(axes[0], "② 剪切", S)
matrix_title(axes[1], "③ 转 $90^\circ$", R)
matrix_title(axes[2], "④ 投影", [[1, 1], [1, 1]], r"$\frac{1}{2}$")
ax = axes[0]
label(ax, "第 1 列", (1, 0), offset=(9, -18), fontsize=9)
label(ax, "第 2 列", (1, 1), offset=(-5, 15), fontsize=9, ha="right")
label(ax, "高为 $y$ 的水平线横移 $y$\n同底同高，面积不变", (-1.8, -1.15), fontsize=8.5)
ax = axes[1]
label(ax, "第 1 列", (0, 1), offset=(0, 9), fontsize=9, ha="center", va="bottom")
label(ax, "第 2 列", (-1, 0), offset=(-8, -18), fontsize=9, ha="right")
t = np.linspace(0, np.pi/2, 100)
arc = np.column_stack((np.cos(t), np.sin(t)))
ax.add_patch(FancyArrowPatch(path=Path(arc), arrowstyle="-|>", color=C.INK, lw=1.1, mutation_scale=10, zorder=4))
label(ax, "转 $90^\circ$", (0.75, 0.75), offset=(15, -2), fontsize=9)
point = np.array([2, 1])
image = R @ point
for q in (point, image):
    ax.plot([0, q[0]], [0, q[1]], color=C.INK, ls=":", lw=1, zorder=3)
ax.scatter(*point, s=35, facecolors=C.PAPER, edgecolors=C.INK, zorder=5)
dot(ax, image, size=28)
label(ax, "$(2,1)$", point, offset=(5, 8), fontsize=9)
label(ax, "$(-1,2)$", image, offset=(-5, 9), ha="right", fontsize=9)
ax = axes[2]
ax.plot([-2, 3], [-2, 3], color=C.INK, lw=1.8, zorder=2)
ax.plot([0, 1], [0, 1], color=C.INK, lw=4, zorder=3)
label(ax, "整个平面压到这条线上", (1.6, 2.65), ha="center", fontsize=8.5)
label(ax, "两列相同，\n都是 $(1/2,\ 1/2)$", (.5, .5), offset=(12, -30), ha="left", va="top", fontsize=8.5)
q, foot = np.array([1., 0.]), P @ [1, 0]
ax.plot([q[0], foot[0]], [q[1], foot[1]], color=C.INK, ls=":", lw=1.2, zorder=4)
ax.scatter(*q, s=35, facecolors=C.PAPER, edgecolors=C.INK, zorder=5)
dot(ax, foot, size=32)
label(ax, "垂直地压", (.85, .2), offset=(16, 8), fontsize=9)
arrow(ax, (0, 0), (-1, 1), color=C.INK, lw=1, zorder=4)
dot(ax, (0, 0), size=30)
label(ax, "$(-1,1)$ 被压到原点", (-1, 1), offset=(-4, 6), ha="center", va="bottom", fontsize=8.5)
save(fig, "L3-n4")

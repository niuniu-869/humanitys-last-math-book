import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Polygon, FancyArrowPatch


def setup(ax):
    ax.set(xlim=(-2, 6), ylim=(-2, 6), aspect="equal")
    ax.set_xticks(range(-2, 7, 2))
    ax.set_yticks(range(-2, 7, 2))
    ax.tick_params(labelsize=8, length=2)
    ax.axhline(0, color=C.GRAY, lw=0.8, zorder=2)
    ax.axvline(0, color=C.GRAY, lw=0.8, zorder=2)
    label(ax, "$x$", (5.8, 0), offset=(0, -14), ha="right")
    label(ax, "$y$", (0, 5.8), offset=(6, 0), va="top")


def vector(ax, v, dashed=False):
    ax.annotate("", xy=v, xytext=(0, 0), arrowprops=dict(
        arrowstyle="-|>", color=C.INK, lw=2.1,
        linestyle="--" if dashed else "-", shrinkA=0, shrinkB=0,
        mutation_scale=12), zorder=5)


A = np.array([[2, 1], [1, 2]])
square = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])
walk = np.array([[0, 0], [1, 0], [2, 0], [2, 1]])
theta = np.linspace(0, 2*np.pi, 721)
circle = np.column_stack((np.cos(theta), np.sin(theta)))
assert np.array_equal(A @ [2, 1], [5, 4])
assert np.array_equal(A @ [1, 1], [3, 3])
assert np.array_equal(A @ [-1, 1], [-1, 1])
assert np.allclose(np.linalg.svd(A, compute_uv=False), [3, 1])

fig, axes = new_fig(26, 12, ncols=2)
fig.subplots_adjust(left=0.05, right=0.98, bottom=0.10, top=0.91, wspace=0.38)
for ax in axes:
    setup(ax)
for k in range(-2, 7):
    axes[0].axvline(k, color=C.LIGHT, lw=0.55, zorder=0)
    axes[0].axhline(k, color=C.LIGHT, lw=0.55, zorder=0)
for k in range(-3, 6):
    for fixed, direction in ((A[:, 0], A[:, 1]), (A[:, 1], A[:, 0])):
        # Endpoints lie beyond the window; axes clipping retains the full line.
        p = k*fixed + np.array([-30, 30])[:, None]*direction
        axes[1].plot(*p.T, color=C.LIGHT, lw=0.55, ls="-", zorder=0)

for ax, matrix in zip(axes, (np.eye(2), A)):
    polygon = square @ matrix.T
    ax.add_patch(Polygon(polygon, facecolor=C.LIGHT, edgecolor=C.INK, lw=1.1, zorder=1))
    path = walk @ matrix.T
    ax.plot(*path.T, color=C.INK, ls=":", lw=1.8, zorder=4)
    curve = circle @ matrix.T
    ax.plot(*curve.T, color=C.GRAY, ls="--", lw=1.0, zorder=3)
    vector(ax, matrix[:, 0])
    vector(ax, matrix[:, 1], dashed=True)

axes[0].set_title("变换前", pad=10)
axes[1].set_title("变换后", pad=10)
label(axes[0], r"$\boldsymbol{e}_1$", (1, 0), offset=(1, -20))
label(axes[0], r"$\boldsymbol{e}_2$", (0, 1), offset=(-20, 7))
axes[0].scatter(2, 1, s=40, facecolors=C.PAPER, edgecolors=C.INK, zorder=5)
label(axes[0], r"$\boldsymbol{x}=2\boldsymbol{e}_1+\boldsymbol{e}_2$", (2, 1), offset=(8, 12))
label(axes[1], "第 1 列", (2, 1), offset=(6, -22), fontsize=9)
label(axes[1], "第 2 列", (1, 2), offset=(-6, 4), ha="right", fontsize=9)
dot(axes[1], (5, 4), size=35)
label(axes[1], r"$A\boldsymbol{x}=2\boldsymbol{a}_1+\boldsymbol{a}_2=(5,4)$",
      (5, 4), offset=(-2, 15), ha="right", fontsize=9)
t = np.array([-2, 6])
axes[1].plot(t, t, color=C.GRAY, ls="-.", lw=0.8, zorder=2)
axes[1].plot(t, -t, color=C.GRAY, ls="-.", lw=0.8, zorder=2)
label(axes[1], "$(1,1)$ 方向\n拉长 3 倍", (3.4, 3.4), offset=(-8, 4), ha="right", fontsize=9)
label(axes[1], "$(-1,1)$ 方向不变", (-1.95, 2.75), offset=(0, 0), ha="left", fontsize=9)
label(axes[0], "单位圆", (-0.75, -0.75), offset=(-4, -4), ha="right", va="top", fontsize=9)
label(axes[1], "椭圆", (-1.25, -1.6), offset=(-4, 0), ha="right", fontsize=9)
fig.canvas.draw()
left, right = [ax.get_position() for ax in axes]
y = (left.y0 + left.y1)/2
fig.add_artist(FancyArrowPatch((left.x1+0.025, y), (right.x0-0.025, y),
    transform=fig.transFigure, arrowstyle="-|>", color=C.INK, lw=2, mutation_scale=19))
fig.text((left.x1+right.x0)/2, y+0.045, "乘 $A$", ha="center", color=C.INK)
save(fig, "L3-n3")

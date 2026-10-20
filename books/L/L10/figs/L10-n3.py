import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import FancyArrowPatch

fig, ax = new_fig(10.5, 10.0)
ax.set_aspect("equal", adjustable="box")
ax.set_xlim(-0.5, 3.6); ax.set_ylim(-0.5, 3.6)
ax.set_xticks(range(0, 4)); ax.set_yticks(range(0, 4))
ax.grid(True, color=C.LIGHT, lw=0.55, zorder=0)
ax.axhline(0, color=C.GRAY, lw=0.8, zorder=1); ax.axvline(0, color=C.GRAY, lw=0.8, zorder=1)
ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
# 直线 y=x
ax.plot([-0.5, 3.6], [-0.5, 3.6], color=C.INK, lw=2.4, zorder=2)
label(ax, "$y=x$", (3.0, 3.0), offset=(10, -4), color=C.INK, ha="left", va="top")

def drop(p, q, show=True):
    ax.scatter(*p, s=36, color=C.INK, zorder=5)
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=11, color=C.INK,
                                 lw=1.4, linestyle="--", shrinkA=3, shrinkB=4, zorder=4))
    ax.scatter(*q, s=40, facecolors=C.PAPER, edgecolors=C.INK, linewidths=1.3, zorder=6)

drop((3, 1), (2, 2)); drop((0, 2), (1, 1)); drop((3, 0), (1.5, 1.5))
# 直角标记 at (2,2)
u = np.array([1, 1]) / np.sqrt(2); v = np.array([1, -1]) / np.sqrt(2); s = 0.17
c = np.array([2, 2])
ax.plot(*np.array([c + s * u, c + s * u + s * v, c + s * v]).T, color=C.INK, lw=1.0, zorder=5)
label(ax, "$\\boldsymbol{b}=(3,1)^T$", (3, 1), offset=(4, -14), color=C.INK, ha="left")
label(ax, "$P\\boldsymbol{b}=(2,2)^T$", (2, 2), offset=(-8, 6), color=C.INK, ha="right", va="bottom")
label(ax, "$\\boldsymbol{e}=(1,-1)^T$", (2.5, 1.5), offset=(8, 2), color=C.INK, ha="left")
# 直线上不动的点
ax.scatter([0.5], [0.5], s=46, marker="s", color=C.INK, zorder=6)
label(ax, "直线上的点不动", (0.5, 0.5), offset=(7, -3), color=C.INK, ha="left", va="top")
label(ax, "实心点：原来的点；空心点：压到的位置", (-0.4, 3.5), color=C.INK, ha="left", va="top", fontsize=8)
save(fig, "L10-n3")

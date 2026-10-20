import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle

fig, ax = new_fig(9.5, 9.5)
pi = np.pi
xs = np.linspace(-pi / 2, pi / 2, 300)
asin_x = np.linspace(-1, 1, 300)
ax.plot(xs, np.sin(xs), color=C.INK, lw=1.7)
ax.plot(asin_x, np.arcsin(asin_x), color=C.INK, lw=2.4)
ax.plot([-2, 2], [-2, 2], color=C.GRAY, ls="--", lw=1.1)
for x, y in [(-pi/2, -1), (pi/2, 1), (-1, -pi/2), (1, pi/2)]:
    dot(ax, (x, y), size=24)
ax.add_patch(Rectangle((-pi/2, -1), pi, 2, facecolor=C.LIGHT, alpha=.18,
                       edgecolor=C.GRAY, ls=":", lw=1.1))
ax.add_patch(Rectangle((-1, -pi/2), 2, pi, facecolor=C.LIGHT, alpha=.18,
                       edgecolor=C.GRAY, ls="--", lw=1.1))
u = (pi/6, .5); v = (.5, pi/6)
ax.plot([u[0], v[0]], [u[1], v[1]], color=C.GRAY, ls=":", lw=1.0)
ax.scatter(*u, s=42, facecolors=C.PAPER, edgecolors=C.INK, zorder=5)
ax.scatter(*v, s=42, facecolors=C.PAPER, edgecolors=C.INK, zorder=5)
label(ax, "$y=x$", (1.08, 1.73), ha="left", va="center", fontsize=9)
# 两个框的标注放进各自的框内角上，并写明线型对应关系
label(ax, "$\\sin$ 的定义域与值域\n（点线框）", (-1.50, .93),
      ha="left", va="top", fontsize=8)
label(ax, "$\\arcsin$ 的定义域与值域\n（短划线框）", (.94, -1.10),
      ha="right", va="top", fontsize=8)
label(ax, r"$(\frac{\pi}{6},\frac{1}{2})$", u, offset=(-8, 8),
      ha="right", va="bottom", fontsize=8.5)
label(ax, r"$(\frac{1}{2},\frac{\pi}{6})$", v, offset=(3, -8),
      ha="left", va="top", fontsize=8.5)
ax.set_xlim(-2, 2); ax.set_ylim(-2, 2); ax.set_aspect("equal")
ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
ax.set_xticks([-2, -pi/2, -1, 0, 1, pi/2, 2])
ax.set_xticklabels(["-2", r"$-\frac{\pi}{2}$", "-1", "0", "1", r"$\frac{\pi}{2}$", "2"])
ax.set_yticks([-2, -pi/2, -1, 0, 1, pi/2, 2])
ax.set_yticklabels(["-2", r"$-\frac{\pi}{2}$", "-1", "0", "1", r"$\frac{\pi}{2}$", "2"])
fig.tight_layout()
save(fig, "C1-n2")

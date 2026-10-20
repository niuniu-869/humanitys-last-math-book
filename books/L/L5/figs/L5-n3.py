import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(10.5, 8.5)
ax.set_aspect("equal", adjustable="box")
ax.set_xlim(-1.3, 1.5)
ax.set_ylim(-1.3, 1.5)
ax.set_xticks(np.arange(-1.0, 1.51, 0.5))
ax.set_yticks(np.arange(-1.0, 1.51, 0.5))
ax.grid(True, color=C.LIGHT, lw=0.65, alpha=0.8)
ax.axhline(0, color=C.GRAY, lw=0.8, ls="-")
ax.axvline(0, color=C.GRAY, lw=0.8, ls="-")

xx = np.linspace(-1.3, 1.5, 400)
ax.plot(xx, xx, color=C.INK, lw=1.6, ls="-", zorder=1)
label(ax, "$y=x$：④的像", (1.45, 1.45), offset=(-8, -2), ha="right")
ax.plot(xx, -xx, color=C.GRAY, lw=1.35, ls=":", zorder=1)
label(ax, "方向 $(-1,1)$：整条压到原点", (0.2, -1.15), offset=(0, 0), ha="left")

# 两点到同一像点的垂直投影（沿 y=-x 方向）
p = (0.5, 0.5)
for start in [(1, 0), (0, 1)]:
    ax.annotate("", xy=p, xytext=start,
                arrowprops=dict(arrowstyle="-|>", color=C.GRAY, lw=1.2, ls="--", mutation_scale=10), zorder=3)

dot(ax, (1, 0), "$(1,0)$", color=C.INK, offset=(6, -14), size=30)
ax.scatter(0, 1, s=34, facecolors=C.PAPER, edgecolors=C.INK, linewidths=1.5, zorder=5)
label(ax, "$(0,1)$", (0, 1), offset=(-36, 5), color=C.INK)
ax.scatter(*p, s=46, marker="s", color=C.INK, zorder=6)
label(ax, r"$(\frac{1}{2},\frac{1}{2})$：两点撞在一起", p, offset=(7, 8), color=C.INK)
dot(ax, (0, 0), "$O$", color=C.INK, offset=(6, -15), size=20)

ax.set_xlabel("$x$")
ax.set_ylabel("$y$")
save(fig, "L5-n3")

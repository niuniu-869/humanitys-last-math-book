import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label


fig, ax = new_fig(15.0, 10.0)
ax.set_aspect("equal", adjustable="box")
ax.set_xlim(-2.5, 3.5)
ax.set_ylim(-2.0, 3.0)
ax.set_xticks(np.arange(-2, 4, 1))
ax.set_yticks(np.arange(-2, 4, 1))
ax.grid(True, color=C.LIGHT, lw=0.7, alpha=0.65, zorder=0)
ax.axhline(0, color=C.GRAY, lw=0.8, zorder=1)
ax.axvline(0, color=C.GRAY, lw=0.8, zorder=1)
ax.set_xlabel(r"$x_1$")
ax.set_ylabel(r"$x_2$")

# 直线 x2=x1（像），以及一族 x1+x2=c 的代表线。
x = np.linspace(-2.5, 3.5, 400)
ax.plot(x, x, color=C.BLUE, lw=3.0, ls="-", zorder=2)
ax.plot(x, -x, color=C.RED, lw=1.8, ls="--", zorder=2)
ax.plot(x, 2 - x, color=C.TEAL, lw=2.2, ls="-", zorder=3)
ax.plot(x, -1 - x, color=C.GRAY, lw=1.2, ls=":", zorder=2)
ax.plot(x, 4 - x, color=C.GRAY, lw=1.2, ls=":", zorder=2)

label(ax, "像：$x_2=x_1$", (2.35, 2.35), offset=(5, -16), color=C.BLUE)
label(ax, "被压到原点\n$x_1+x_2=0$", (1.75, -1.42), offset=(0, 0), color=C.RED,
      ha="left", va="top")
label(ax, "解集：$x_1+x_2=2$", (-0.3, 2.42), offset=(0, 0), color=C.TEAL,
      ha="left", va="bottom")
label(ax, "每条点线\n整条压到一个点", (-1.0, -1.42), offset=(0, 0), color=C.GRAY,
      ha="left", va="top")

# 三个解点，以及沿解集指向交点 (1,1) 的箭头。
for p, vec, text, off in [
    ((2, 0), (-0.78, 0.78), "$(2,0)$", (7, 5)),
    ((0, 2), (0.78, -0.78), "$(0,2)$", (7, 5)),
    ((3, -1), (-1.28, 1.28), "$(3,-1)$", (-42, 4)),
]:
    ax.scatter([p[0]], [p[1]], s=34, color=C.INK, zorder=5)
    label(ax, text, p, offset=off, color=C.INK)
    arrow(ax, p, vec, color=C.GRAY, lw=1.15)

# b=(1,1) 用实心方块；b'=(1,0) 用空心圆。
ax.scatter([1], [1], s=54, marker="s", color=C.INK, zorder=6)
label(ax, r"$\mathbf{b}=(1,1)$", (1, 1), offset=(10, 0), color=C.INK, ha="left", va="center")
ax.scatter([1], [0], s=58, marker="o", facecolors=C.PAPER, edgecolors=C.INK,
           linewidths=1.6, zorder=6)
label(ax, "$\\mathbf{b}'=(1,0)$\n不在像上\n所以无解", (0.97, -0.22), offset=(0, 0), color=C.INK, ha="left", va="top", fontsize=9.5)

label(ax, "$O$", (0, 0), offset=(0, -8), color=C.INK, ha="center", va="top")
save(fig, "L9-n2")

import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label


def setup(ax):
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-0.8, 7.2)
    ax.set_ylim(-0.6, 6.6)
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.axhline(0, color=C.LIGHT, lw=0.7, zorder=0)
    ax.axvline(0, color=C.LIGHT, lw=0.7, zorder=0)
    label(ax, r"$O$", (-0.1, -0.1), offset=(0, 0), color=C.INK, ha="right", va="top")


def poly(ax, pts, ls="-", lw=1.5, color=C.INK, fill=False):
    p = np.array(pts + [pts[0]], float)
    if fill:
        ax.fill(p[:, 0], p[:, 1], color=C.LIGHT, alpha=0.85, zorder=1)
    ax.plot(p[:, 0], p[:, 1], color=color, lw=lw, ls=ls, zorder=3)


def darrow(ax, start, end, color=C.GRAY, lw=1.6, ls="--"):
    ax.annotate("", xy=tuple(end), xytext=tuple(start),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, linestyle=ls,
                                mutation_scale=11, shrinkA=0, shrinkB=0), zorder=4)


O = np.array([0.0, 0.0])
a1 = np.array([2.0, 1.0])
a2 = np.array([1.0, 2.0])
a1x2 = 2 * a1
b = 2 * a1 + a2
A1, A2, B = r"$\mathbf{a}_1$", r"$\mathbf{a}_2$", r"$\mathbf{b}$"

fig, axs = new_fig(18.0, 10.5, nrows=1, ncols=2)
for ax in axs:
    setup(ax)

# Left: a1 -> 2a1 doubles the area.
ax = axs[0]
poly(ax, [O, a1, a1 + a2, a2], fill=True, lw=1.2)
poly(ax, [O, a1x2, a1x2 + a2, a2], ls="--", color=C.GRAY, lw=1.5)
arrow(ax, O, a1, color=C.INK, lw=1.8, offset=(0, 0))
arrow(ax, O, a2, color=C.INK, lw=1.8, offset=(0, 0))
darrow(ax, a1, a1x2)
label(ax, A1, (2.05, 0.55), offset=(0, 0), color=C.INK, ha="left", va="center")
label(ax, A2, (0.35, 2.3), offset=(0, 0), color=C.INK, ha="right", va="center")
label(ax, r"$2\mathbf{a}_1$", (4.15, 1.75), offset=(0, 0), color=C.GRAY, ha="left", va="center")
label(ax, "3", (1.5, 1.5), offset=(0, 0), color=C.INK, ha="center", va="center")
label(ax, "3", (3.5, 2.5), offset=(0, 0), color=C.INK, ha="center", va="center")
ax.set_title("阴影：以 $\\mathbf{a}_1,\\mathbf{a}_2$ 为边，面积 3\n虚线：以 $2\\mathbf{a}_1,\\mathbf{a}_2$ 为边，面积 3+3=6",
             color=C.INK, loc="left", fontsize=10)

# Right: slide 2a1 along a2 to b; same base a2, same height.
ax = axs[1]
poly(ax, [O, a1x2, a1x2 + a2, a2], ls="--", color=C.GRAY, lw=1.5)
poly(ax, [O, b, b + a2, a2], ls="-", color=C.INK, lw=1.9)
arrow(ax, O, a2, color=C.INK, lw=2.4, offset=(0, 0))
darrow(ax, O, a1x2)
arrow(ax, O, b, color=C.INK, lw=2.0, offset=(0, 0))
darrow(ax, a1x2, b, color=C.INK, lw=1.2, ls=":")
ax.plot([3.5, 6.6], [1.0, 7.2], color=C.GRAY, lw=0.8, ls=":", zorder=2)
label(ax, A2 + "（公共的底）", (0.75, 2.3), offset=(0, 0), color=C.INK, ha="right", va="bottom")
label(ax, r"$2\mathbf{a}_1$", (3.0, 1.15), offset=(0, 0), color=C.GRAY, ha="left", va="top")
label(ax, B + r"$=2\mathbf{a}_1+\mathbf{a}_2$", (5.15, 3.75), offset=(0, 0), color=C.INK, ha="left", va="center")
label(ax, "滑动 " + A2, (4.6, 2.75), offset=(0, 0), color=C.INK, ha="left", va="center")
ax.set_title("虚线：以 $2\\mathbf{a}_1,\\mathbf{a}_2$ 为边，面积 6\n实线：以 $\\mathbf{b},\\mathbf{a}_2$ 为边，同底等高，面积 6",
             color=C.INK, loc="left", fontsize=10)

save(fig, "L6-n5")

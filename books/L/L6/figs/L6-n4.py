import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label


def setup(ax):
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-1.3, 3.8)
    ax.set_ylim(-1.9, 5.8)
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.axhline(0, color=C.LIGHT, lw=0.7, zorder=0)
    ax.axvline(0, color=C.LIGHT, lw=0.7, zorder=0)


def dimline(ax, x0, x1, y, text):
    ax.annotate("", xy=(x1, y), xytext=(x0, y),
                arrowprops=dict(arrowstyle="<->", color=C.GRAY, lw=0.9,
                                shrinkA=0, shrinkB=0, mutation_scale=9), zorder=5)
    label(ax, text, ((x0 + x1) / 2, y - 0.08), offset=(0, 0), color=C.INK, ha="center", va="top")


fig, axs = new_fig(17.0, 11.0, nrows=1, ncols=2)
for ax in axs:
    setup(ax)

O = np.array([0.0, 0.0])
r2 = np.array([0.0, 3.0])
r1 = np.array([1.0, 0.5])
r1p = np.array([1.5, 2.0])
sumv = np.array([2.5, 2.5])
R1, R1P, R2 = r"$\mathbf{r}_1$", r"$\mathbf{r}_1'$", r"$\mathbf{r}_2$"

# Left panel: two parallelograms on the same base r2.
ax = axs[0]
left_a = np.array([[0, 0], [1, 0.5], [1, 3.5], [0, 3], [0, 0]], float)
left_b = np.array([[0, 0], [1.5, 2], [1.5, 5], [0, 3], [0, 0]], float)
ax.fill(left_a[:, 0], left_a[:, 1], color=C.LIGHT, alpha=0.78, zorder=1)
ax.plot(left_a[:, 0], left_a[:, 1], color=C.INK, lw=1.6, zorder=3)
ax.plot(left_b[:, 0], left_b[:, 1], color=C.GRAY, lw=1.35, ls="--", zorder=3)
arrow(ax, O, r2, color=C.INK, lw=2.2, offset=(7, 0))
label(ax, R2 + "（底）", (-0.12, 1.5), offset=(0, 0), color=C.INK, ha="right", va="center")
arrow(ax, O, r1, color=C.INK, lw=1.7, offset=(6, 7))
label(ax, R1, (1.12, 0.3), offset=(0, 0), color=C.INK, ha="left", va="center")
ax.annotate("", xy=tuple(r1p), xytext=tuple(O),
            arrowprops=dict(arrowstyle="-|>", color=C.GRAY, lw=1.7, linestyle="--",
                            mutation_scale=11, shrinkA=0, shrinkB=0), zorder=4)
label(ax, R1P, (1.62, 1.85), offset=(0, 0), color=C.GRAY, ha="left", va="center")
label(ax, "面积 3", (0.5, 2.1), offset=(0, 0), color=C.INK, ha="center", va="center")
label(ax, "虚线围成：\n面积 4.5", (1.62, 4.3), offset=(0, 0), color=C.INK, ha="left", va="center")
for x, y in [(1.0, 0.5), (1.5, 2.0)]:
    ax.plot([x, x], [-1.25, y], color=C.GRAY, lw=0.8, ls=":", zorder=2)
dimline(ax, 0, 1, -0.6, r"$h=1$")
dimline(ax, 0, 1.5, -1.25, r"$h'=1.5$")
ax.set_title("同底的两个平行四边形", color=C.INK)

# Right panel: the parallelogram of the sum.
ax = axs[1]
right = np.array([[0, 0], [2.5, 2.5], [2.5, 5.5], [0, 3], [0, 0]], float)
ax.fill(right[:, 0], right[:, 1], color=C.LIGHT, alpha=0.78, zorder=1)
ax.plot(right[:, 0], right[:, 1], color=C.INK, lw=1.7, zorder=3)
arrow(ax, O, r2, color=C.INK, lw=2.2, offset=(7, 0))
label(ax, R2 + "（底）", (-0.12, 1.5), offset=(0, 0), color=C.INK, ha="right", va="center")
arrow(ax, O, r1, color=C.INK, lw=1.7, offset=(6, 7))
label(ax, R1, (1.05, 0.22), offset=(0, 0), color=C.INK, ha="left", va="center")
ax.annotate("", xy=tuple(sumv), xytext=tuple(r1),
            arrowprops=dict(arrowstyle="-|>", color=C.GRAY, lw=1.7, linestyle="--",
                            mutation_scale=11, shrinkA=0, shrinkB=0), zorder=4)
label(ax, R1P, (1.95, 1.3), offset=(0, 0), color=C.GRAY, ha="left", va="center")
arrow(ax, O, sumv, color=C.INK, lw=2.1, offset=(7, 7))
label(ax, R1 + "+" + R1P, (2.62, 2.35), offset=(0, 0), color=C.INK, ha="left", va="center")
label(ax, "面积 7.5 = 3 + 4.5", (1.55, 3.75), offset=(0, 0), color=C.INK, ha="center", va="center")
for x, y in [(1.0, 0.5), (2.5, 2.5)]:
    ax.plot([x, x], [-1.25, y], color=C.GRAY, lw=0.8, ls=":", zorder=2)
dimline(ax, 0, 1, -0.6, r"$h$")
dimline(ax, 1, 2.5, -0.6, r"$h'$")
dimline(ax, 0, 2.5, -1.25, r"$h+h'$")
ax.set_title("和的平行四边形", color=C.INK)

save(fig, "L6-n4")

import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(13, 8)
levels = [0, 1 / 8, 1 / 2, 7 / 8, 1]
segments = [(-1, 0, 0), (0, 1, 1 / 8), (1, 2, 1 / 2),
            (2, 3, 7 / 8), (3, 4, 1)]
for left, right, y in segments:
    ax.plot([left, right], [y, y], color=C.INK, lw=1.8, ls="-")
    if left >= 0:
        dot(ax, (left, y), color=C.INK, size=24)
    if right <= 3:
        ax.scatter([right], [y], s=28, facecolors=C.PAPER, edgecolors=C.INK,
                   linewidths=1.0, zorder=5)
ax.plot([1, 1], [1 / 8, 1 / 2], color=C.INK, lw=1.0, ls=":")
label(ax, r"跳高 $\frac{3}{8}=P(X=1)$", (1, 5 / 16), offset=(8, 0), va="center", fontsize=9)
ax.set(xlim=(-1.2, 4.2), ylim=(-0.04, 1.08),
       xticks=[0, 1, 2, 3], yticks=levels,
       yticklabels=["0", r"$\frac{1}{8}$", r"$\frac{1}{2}$", r"$\frac{7}{8}$", "1"],
       xlabel="$x$", ylabel="$F(x)$")
ax.grid(False)
save(fig, "P3-n3")

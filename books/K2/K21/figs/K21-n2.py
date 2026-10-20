import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import FancyArrowPatch

fig, ax = new_fig(16, 16)
fig.subplots_adjust(left=0.08, right=0.97, bottom=0.08, top=0.97)
ax.set(xlim=(-2, 9), ylim=(-2, 9), aspect="equal")
ax.spines["bottom"].set_position("zero")
ax.spines["left"].set_position("zero")
ax.set_xticks([3, 5, 7, 9])
ax.set_yticks([3, 5, 7, 9])
label(ax, "$x$", (8.85, 0), (0, -17), ha="right")
label(ax, "$y$", (0, 8.8), (-12, 0), ha="right")
x = np.linspace(-2, 9, 300)
ax.plot(x, 2*x + 1, color=C.INK, lw=2.0, ls="-")
ax.plot(x, x, color=C.RED, lw=1.3, ls="--")
label(ax, r"$y=2x+1$", (2.2, 6.1), (-18, 3), ha="right")
label(ax, r"$y=x$", (7.6, 7.6), (15, -14))
h = [0]
for _ in range(3):
    h.append(2*h[-1] + 1)
assert h == [0, 1, 3, 7]
for a, b in zip(h[:-1], h[1:]):
    for start, end in [((a, a), (a, b)), ((a, b), (b, b))]:
        ax.plot([start[0], end[0]], [start[1], end[1]], color=C.INK, lw=0.9, ls="-")
        start, end = np.array(start), np.array(end)
        arrow(ax, start + 0.43*(end-start), 0.17*(end-start), color=C.INK, lw=0.9)
ax.scatter(h, h, s=36, facecolors=C.PAPER, edgecolors=C.INK, marker="o", zorder=5)
for i, value in enumerate(h):
    offset, align = ((14, 2) if i == 0 else (8, 10)), "left"
    label(ax, rf"$h_{i}={value}$", (value, 0), offset, ha=align, fontsize=9)
dot(ax, (-1, -1), size=32)
ax.annotate("", xy=(-1, -1), xytext=(-1.65, 1.9),
            arrowprops=dict(arrowstyle="-", lw=0.7, color=C.GRAY))
label(ax, r"不动点 $x^*=-1$", (-1.75, 2.15), fontsize=9, ha="left")
for i, value in enumerate(h):
    distance = value + 1
    assert distance == 2**i
    y = -0.45 - i*0.44
    ax.add_patch(FancyArrowPatch((-1, y), (value, y),
                                arrowstyle="<->", mutation_scale=8,
                                lw=0.9, linestyle=":", color=C.INK,
                                shrinkA=0, shrinkB=0))
    text_x = (value-1)/2 + (0.3 if i == 1 else 0)
    label(ax, str(distance), (text_x, y), (0, 3), ha="center", va="bottom", fontsize=8)
save(fig, "K21-n2")

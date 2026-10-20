import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import FancyArrowPatch, Arc

fig, ax = new_fig(16, 8)
ax.set_xlim(-1.35, 5.55); ax.set_ylim(-2.2, 2.15); ax.axis("off")
ax.plot([-1, 5], [0, 0], color=C.INK, lw=1.5)
for x in range(-1, 6):
    ax.plot([x, x], [-.10, .10], color=C.INK, lw=1.2)
    label(ax, str(x), (x, -.28), ha="center", va="top")
ax.plot([1, 1], [-.18, .18], color=C.INK, lw=2)
ax.plot([3, 3], [-.18, .18], color=C.INK, lw=2)
dot(ax, (1, 0), size=36)
dot(ax, (3, 0), size=36)
label(ax, "1", (1, .18), ha="center", va="bottom")
label(ax, "3", (3, .18), ha="center", va="bottom")

def bracket(x0, x1, text, solid_left=False, solid_right=False):
    y = -1.05
    ax.plot([x0, x1], [y, y], color=C.INK, lw=1.2)
    ax.plot([x0, x0], [y, y+.13], color=C.INK, lw=1.2)
    ax.plot([x1, x1], [y, y+.13], color=C.INK, lw=1.2)
    label(ax, text, ((x0+x1)/2, y-.14), ha="center", va="top")
    if solid_left: ax.scatter([x0], [y], s=45, facecolors=C.INK, edgecolors=C.INK, zorder=5)
    if solid_right: ax.scatter([x1], [y], s=45, facecolors=C.INK, edgecolors=C.INK, zorder=5)

bracket(-.85, 1, "$x<1$", solid_right=True)
bracket(1, 3, "$1\u2264x\u22643$")
bracket(3, 4.85, "$x>3$", solid_left=True)

dot(ax, (2, 0), size=62, color=C.INK)
label(ax, "$x=2$", (2, .18), ha="center", va="bottom")
ax.plot([1, 2], [.42, .42], color=C.INK, lw=1.5)
ax.plot([2, 3], [.70, .70], color=C.INK, lw=1.5)
label(ax, "$|x-1|=1$", (1.5, .42), offset=(0, 5), ha="center")
label(ax, "$|x-3|=1$", (2.5, .70), offset=(0, 5), ha="center")
label(ax, "$x=2$ 时\n和 = 2", (-0.9, .55), ha="left")

dot(ax, (4.5, 0), size=70, color=C.PAPER)
ax.scatter([4.5], [0], s=70, facecolors=C.PAPER, edgecolors=C.INK, marker="s", zorder=5)
label(ax, "$x=4.5$", (4.5, 0), offset=(0, 20), ha="center")
ax.add_patch(FancyArrowPatch((4.5, .35), (3.05, .35), connectionstyle="arc3,rad=.25", arrowstyle="-", lw=1.4, ls="--", color=C.GRAY))
ax.add_patch(FancyArrowPatch((4.5, .35), (1.05, .35), connectionstyle="arc3,rad=.48", arrowstyle="-", lw=1.4, ls="--", color=C.GRAY))
label(ax, "$|x-3|=1.5$", (3.85, .90), ha="center")
label(ax, "$|x-1|=3.5$", (2.75, 1.48), ha="center")
label(ax, "和 = 5 > 2", (4.15, 1.72), ha="center")
save(fig, "Z4-n1")

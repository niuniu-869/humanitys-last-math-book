import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(11, 8)
xlim = (-2.5, 4.0); ylim = (-5.0, 10.0)
x = np.linspace(xlim[0], xlim[1], 1000)
ax.plot(x, x**2, color=C.GRAY, lw=1.5, ls="--")
ax.plot(x, 6 * x - 9, color=C.INK, lw=1.1, ls="-")
ax.plot(x, -2 * x - 1, color=C.INK, lw=1.1, ls="-")
P = (1.0, -3.0)
dot(ax, P, color=C.INK, size=30)
label(ax, "P(1,-3)", P, offset=(6, 6))
for q, txt, off in [((3.0, 9.0), "(3,9)", (6, -12)), ((-1.0, 1.0), "(-1,1)", (-8, 12))]:
    ax.scatter(*q, s=36, facecolors=C.PAPER, edgecolors=C.INK, linewidths=1.2, zorder=5)
    label(ax, txt, q, offset=off)
assert 6 * P[0] - 9 == -2 * P[0] - 1 == P[1]
label(ax, "$y=x^2$", (-1.8, 5.5), offset=(0, 0))
label(ax, "$y=6x-9$", (1.25, 7.6), offset=(0, 0))
label(ax, "$y=-2x-1$", (-1.6, -1.0), offset=(0, 0))
ax.set_xlim(*xlim); ax.set_ylim(*ylim)
ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
ax.set_xticks([-2, -1, 0, 1, 2, 3, 4]); ax.set_yticks([-5, 0, 5, 10])
save(fig, "C4-n3")

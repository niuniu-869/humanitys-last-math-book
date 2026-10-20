import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(12, 8.5)
a, b, xc = 0.5, 4., 2.6
def lower(x):
    return 0.2 + 0.15*(x-2)**2
def upper(x):
    return 2.6 + 0.5*np.sin(1.3*x)
x = np.linspace(a, b, 501)
assert np.all(upper(x) > lower(x))
ax.fill_between(x, lower(x), upper(x), color=C.LIGHT, lw=0)
for fn in (lower, upper):
    ax.plot(x, fn(x), color=C.INK, ls="-", lw=1.6)
for side in (a, b):
    ax.plot([side, side], [lower(side), upper(side)], color=C.INK, ls="-", lw=1.6)
arrow(ax, (1.85, lower(1.85)), (0.35, lower(2.2)-lower(1.85)), color=C.INK)
arrow(ax, (2.2, upper(2.2)), (-0.35, upper(1.85)-upper(2.2)), color=C.INK)
arrow(ax, (a, 1.8), (0, -0.45), color=C.INK)
arrow(ax, (b, 1.35), (0, 0.45), color=C.INK)
label(ax, r"$y=\varphi_1(x)$", (3.05, lower(3.05)), offset=(0, 20))
label(ax, r"$y=\varphi_2(x)$", (1.15, upper(1.15)), offset=(-12, 11))
label(ax, "$D$", (1.55, 1.5), fontsize=13)
ax.plot([xc, xc], [lower(xc), upper(xc)], color=C.INK, ls="--", lw=1.2)
ax.scatter([xc, xc], [lower(xc), upper(xc)], s=35,
           facecolors=C.PAPER, edgecolors=C.INK, zorder=5)
ax.plot([xc, xc], [0, lower(xc)], color=C.GRAY, ls=":", lw=0.8)
ax.axhline(0, color=C.GRAY, lw=0.8)
ax.axvline(0, color=C.GRAY, lw=0.8)
for xv, text in ((a, "$a$"), (b, "$b$"), (xc, "$x$")):
    ax.plot([xv, xv], [0, 0.07], color=C.INK, lw=0.8)
    label(ax, text, (xv, 0), offset=(0, -14), ha="center")
label(ax, "$x$", (4.5, 0), offset=(0, 5))
label(ax, "$y$", (0, 3.45), offset=(5, 0))
ax.set_xlim(-0.3, 4.7)
ax.set_ylim(-0.4, 3.75)
ax.axis("off")
save(fig, "C27-n2")

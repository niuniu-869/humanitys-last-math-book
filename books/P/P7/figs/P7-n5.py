import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(12, 7.5)
pts = [(0,1,.20),(0,2,.15),(0,3,.05),(1,1,.10),(1,2,.25),(1,3,.25)]
for x, y, p in pts:
    ax.scatter([x], [y], s=1100*p, facecolors=C.PAPER if x == 0 else C.LIGHT,
               edgecolors=C.INK, linewidths=1.2, zorder=4)
xx = np.linspace(-.4, 1.4, 200); yy = 13/8 + 5/8*xx
ax.plot(xx, yy, color=C.INK, lw=1.6)
for x, y, txt in [(0,13/8,r"$E(Y\mid X=0)=\frac{13}{8}$"),(1,9/4,r"$E(Y\mid X=1)=\frac{9}{4}$")]:
    ax.scatter([x],[y], s=75, marker="s", facecolors=C.PAPER, edgecolors=C.INK, zorder=6)
label(ax, r"$E(Y\mid X=0)=\frac{13}{8}$", (-.38, 2.30), offset=(0, 0), ha="left", va="bottom")
label(ax, r"$E(Y\mid X=1)=\frac{9}{4}$", (.56, 2.40), offset=(0, 0), ha="left", va="bottom")
ax.set_xlim(-.4,1.4); ax.set_ylim(.4,3.6); ax.set_xlabel("$X$"); ax.set_ylabel("$Y$")
save(fig, "P7-n5")

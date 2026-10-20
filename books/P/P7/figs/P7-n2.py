import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(12, 7.5)
pts = [(0,1,.20),(0,2,.15),(0,3,.05),(1,1,.10),(1,2,.25),(1,3,.25)]
for x, y, p in pts:
    ax.scatter([x], [y], s=1100*p, facecolors=C.PAPER if x == 0 else C.LIGHT,
               edgecolors=C.INK, linewidths=1.2, zorder=4)
    label(ax, f"{p:.2f}", (x, y), offset=(8, 5), va="center")
ax.axvline(.6, color=C.GRAY, ls="--", lw=1.1); ax.axhline(2, color=C.GRAY, ls="--", lw=1.1)
ax.plot(.6, 2, marker="+", markersize=12, mew=1.6, color=C.INK, zorder=6)
label(ax, "均值点 (0.6, 2)", (.52, 2.42), offset=(0, 0), ha="right", va="bottom")
label(ax, "+", (1.35, 3.4), ha="center", va="center", fontsize=15)
label(ax, "−", (-.35, 3.4), ha="center", va="center", fontsize=15)
label(ax, "−", (1.35, .62), ha="center", va="center", fontsize=15)
label(ax, "+", (-.35, .62), ha="center", va="center", fontsize=15)
ax.set_xlim(-.5, 1.5); ax.set_ylim(.4, 3.6)
ax.set_xlabel("$X$"); ax.set_ylabel("$Y$")
save(fig, "P7-n2")

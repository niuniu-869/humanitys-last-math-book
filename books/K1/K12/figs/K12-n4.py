import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.lines import Line2D

fig, ax = new_fig(15, 10)
ax.set(xlim=(-.5, 10.5), ylim=(-1.7, 6.3))
ax.axis("off")
a, b, c = (1.6, 4.6), (8.4, 4.6), (5, .5)
for p, q, style in [(a, b, "-"), (b, c, "--"), (a, c, "--")]:
    ax.plot([p[0], q[0]], [p[1], q[1]], color=C.INK, ls=style, lw=1.6)
dot(ax, a, size=65)
dot(ax, b, size=65)
ax.scatter(*c, s=65, facecolors=C.PAPER, edgecolors=C.INK, linewidths=1.5, zorder=5)
label(ax, "甲（骑士）", a, (-7, 12), ha="right")
label(ax, "乙（骑士）", b, (7, 12), ha="left")
label(ax, "丙（无赖）", c, (0, -20), ha="center")
label(ax, "同类\n甲说乙是骑士", (5, 5.05), ha="center", va="bottom")
label(ax, "异类（推出）\n由前两条推出", (.1, 2.3), ha="left")
label(ax, "异类\n乙说丙是无赖", (9.9, 2.3), ha="right")
handles = [Line2D([], [], color=C.INK, ls="-", label="同类"),
           Line2D([], [], color=C.INK, ls="--", label="异类"),
           Line2D([], [], color=C.INK, ls="", marker="o", label="骑士"),
           Line2D([], [], color=C.INK, ls="", marker="o", markerfacecolor=C.PAPER, label="无赖")]
ax.legend(handles=handles, loc="lower center", ncol=4, columnspacing=1.2, handlelength=1.8)
save(fig, "K12-n4")

import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, save, arrow, dot, label

fig, (a1, a2) = new_fig(16, 7.6, ncols=2)
for ax in (a1, a2):
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.5, 1.5)
    ax.set_xticks([-1, 0, 1]); ax.set_yticks([-1, 0, 1])
    for v in (-1, 0, 1):
        ax.plot([v, v], [-1.5, 1.5], color=C.LIGHT, lw=0.7, ls=":", zorder=0)
        ax.plot([-1.5, 1.5], [v, v], color=C.LIGHT, lw=0.7, ls=":", zorder=0)
    ax.axhline(0, color=C.GRAY, lw=0.8, zorder=1); ax.axvline(0, color=C.GRAY, lw=0.8, zorder=1)
    ax.plot([-1.5, 1.5], [-1.5, 1.5], color=C.GRAY, lw=1.0, zorder=1)

a1.set_title("变换前")
arrow(a1, (0, 0), (1, 0), color=C.INK, lw=2.4)
label(a1, r"$\boldsymbol{e}_1$", (1, 0), offset=(-4, 6))
arrow(a1, (0, 0), (0, 1), color=C.INK, lw=2.4)
label(a1, r"$\boldsymbol{e}_2$", (0, 1), offset=(5, -4))
a1.annotate("", xy=(1, -1), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=C.INK, lw=2.0,
            linestyle=(0, (4, 2)), shrinkA=0, shrinkB=0, mutation_scale=11), zorder=5)
label(a1, r"虚线：$\boldsymbol{e}_1-\boldsymbol{e}_2=(1,-1)$", (-0.55, -1.38), offset=(0, 0), fontsize=9)
label(a1, "$y=x$", (1.15, 1.15), offset=(-28, 2), color=C.GRAY, fontsize=9)

a2.set_title("投影④之后")
arrow(a2, (0, 0), (0.5, 0.5), color=C.INK, lw=2.6)
dot(a2, (0.5, 0.5), size=26)
label(a2, r"$\boldsymbol{e}_1$、$\boldsymbol{e}_2$ 都到了这里" + "\n" + r"$(\frac{1}{2},\frac{1}{2})$", (0.5, 0.5), offset=(9, -14), fontsize=9)
a2.scatter([0], [0], s=46, facecolors=C.PAPER, edgecolors=C.INK, linewidths=1.4, zorder=6)
label(a2, "$(1,-1)$ 被送到原点", (0, 0), offset=(6, -16), fontsize=9)
label(a2, "整个平面被压到直线 $y=x$ 上", (-1.45, 1.2), offset=(0, 0), fontsize=9)

fig.text(0.505, 0.5, "→", ha="center", va="center", fontsize=22)
fig.subplots_adjust(wspace=0.35)
save(fig, "L7-n1")

import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(13, 7.5)
n = np.arange(1, 16)
a = 1 + (-1.0) ** n / n
assert np.allclose(a[:6], [0, 1.5, 2/3, 1.25, .8, 7/6])
ax.axhspan(.8, 1.2, facecolor=C.LIGHT, alpha=.45, zorder=0)
ax.axhline(1, color=C.INK, lw=1.7)
ax.axhline(.8, color=C.GRAY, ls="--", lw=1.1)
ax.axhline(1.2, color=C.GRAY, ls="--", lw=1.1)
ax.plot(n[:5], a[:5], ls="none", marker="o", markersize=5.5, markerfacecolor=C.PAPER,
        markeredgecolor=C.INK, zorder=4)
ax.plot(n[5:], a[5:], ls="none", marker="o", markersize=5.5, markerfacecolor=C.INK,
        markeredgecolor=C.INK, zorder=4)
ax.plot([5, 5], [0, 1.6], color=C.GRAY, ls=":", lw=1.1)
# 三个标注都移到带外的空白处：极限线标在带上方，两条边界标在带上下方
label(ax, "极限 $a=1$", (7.2, 1.33), ha="center", va="center", fontsize=9)
label(ax, "$1-\\varepsilon$", (15.15, .715), ha="right", va="center", fontsize=9)
label(ax, "$1+\\varepsilon$", (15.15, 1.285), ha="right", va="center", fontsize=9)
label(ax, "$\\varepsilon=0.2$", (13.6, 1.43), ha="center", va="center", fontsize=9)
# 从 ε 标注向下指到带的上边界，说明带宽
ax.annotate("", xy=(13.6, 1.205), xytext=(13.6, 1.37),
            arrowprops=dict(arrowstyle="-|>", color=C.GRAY, lw=1.0,
                            shrinkA=0, shrinkB=0, mutation_scale=8))
label(ax, "$N=5$", (5, .06), offset=(5, 3), ha="left", va="bottom", fontsize=9)
label(ax, "$n>N$ 以后全在带内", (8.3, 1.50), ha="center", va="center", fontsize=9)
ax.set_xlim(0, 16); ax.set_ylim(0, 1.6)
ax.set_xlabel("$n$"); ax.set_ylabel("$a_n$")
ax.set_xticks(np.arange(0, 17, 2)); ax.set_yticks([0, .4, .8, 1.0, 1.2, 1.6])
fig.tight_layout()
save(fig, "C1-n4")

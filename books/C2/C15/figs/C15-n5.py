import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(12, 7.5)
eps = 0.1
x = np.linspace(0, 1, 600)
ax.fill_between(x, 0, eps, color=C.LIGHT, zorder=0)
ax.axhline(eps, color=C.GRAY, lw=0.8)
label(ax, r"$y=\varepsilon$", (0.02, eps), offset=(0, 4))
# 带子里有三条曲线穿过，说明文字放到左侧空白处
label(ax, "灰带：0 附近宽为 $\\varepsilon$ 的带子", (0.05, 0.775), offset=(0, 0), ha="left", va="center")
for n, ls, xl in [(2, "-", 0.55), (8, "--", 0.83), (40, ":", 0.975)]:
    ax.plot(x, x**n, color=C.INK, lw=1.6, ls=ls)
AP = dict(arrowstyle="-", color=C.GRAY, lw=0.7)
label(ax, "$n=2$", (0.7, 0.7**2), offset=(-70, 18), arrowprops=AP)
label(ax, "$n=8$", (0.92, 0.92**8), offset=(-70, 30), arrowprops=AP)
label(ax, "$n=40$", (0.985, 0.985**40), offset=(-70, 60), arrowprops=AP)
ax.scatter([1], [1], s=30, color=C.INK, zorder=5)
label(ax, "$x=1$ 处 $x^n=1$", (1, 1), offset=(-82, 2))
x40 = eps ** (1 / 40)
ax.plot([x40, x40], [0, eps], color=C.INK, lw=1.0, ls=":")
ax.scatter([x40], [eps], s=18, color=C.INK, zorder=5)
ax.set_xlim(0, 1.04); ax.set_ylim(0, 1.08)
# 注记放到左上空白处；用细灰折线引线指向带子边缘上的那一点。
label(ax, "此点右侧都在带子外", (0.05, 0.87), offset=(0, 0), ha="left", va="center")
ax.plot([0.43, 0.50], [0.87, 0.87], color=C.GRAY, lw=0.7, zorder=4, solid_capstyle="butt")
ax.annotate("", xy=(x40, eps), xytext=(0.50, 0.87),
            arrowprops=dict(arrowstyle="-|>", color=C.GRAY, lw=0.7, shrinkA=0, shrinkB=3, mutation_scale=9), zorder=4)
ax.set_xlabel("$x$")
save(fig, "C15-n5")

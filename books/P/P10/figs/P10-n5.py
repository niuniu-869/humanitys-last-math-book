import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from scipy.stats import f


fig, ax = new_fig(13, 7.5)
x = np.linspace(1e-4, 6, 1800)
y510 = f.pdf(x, 5, 10)
y105 = f.pdf(x, 10, 5)
ax.plot(x, y510, color=C.INK, ls="-", lw=1.8)
ax.plot(x, y105, color=C.INK, ls="--", lw=1.6)

cut = 3.326
tail_x = x[x >= cut]
ax.fill_between(tail_x, 0, f.pdf(tail_x, 5, 10), color=C.LIGHT, zorder=0)
ax.axvline(cut, color=C.GRAY, ls=":", lw=1.0)
label(ax, "右尾完整面积\n0.05\n（延伸到画外）", (5.94, 0.09), offset=(0, 0), ha="right", va="bottom")
label(ax, "3.326", (cut, 0.115), offset=(-6, 0), ha="right", va="center")
ax.annotate("F(5,10)（实线）", xy=(0.5, f.pdf(0.5, 5, 10)), xytext=(2.3, 0.65), fontsize=13, ha="center", arrowprops=dict(arrowstyle="-|>", color="black", lw=1.0))
ax.annotate("F(10,5)（虚线）", xy=(3.55, f.pdf(3.55, 10, 5)), xytext=(3.50, 0.40), fontsize=13, ha="left", va="center", arrowprops=dict(arrowstyle="-|>", color="black", lw=1.0))
ax.set_xlim(0, 6)
ax.set_ylim(0, 0.75)
ax.set_xlabel("x")
ax.set_ylabel("密度")
save(fig, "P10-n5")

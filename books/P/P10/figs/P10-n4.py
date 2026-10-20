import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from scipy.stats import norm, t


fig, ax = new_fig(13, 7.5)
x = np.linspace(-5, 5, 1800)
ax.plot(x, norm.pdf(x), color=C.INK, ls="-", lw=2.2)
ax.plot(x, t.pdf(x, 4), color=C.INK, ls="--", lw=1.6)
ax.plot(x, t.pdf(x, 1), color=C.INK, ls=":", lw=1.6)

cut = 2.776
tail_x = x[x >= cut]
ax.fill_between(tail_x, 0, t.pdf(tail_x, 4), color=C.LIGHT, zorder=0)
ax.plot([cut, cut], [0, 0.30], color=C.GRAY, ls=":", lw=1.0)
label(ax, "右尾完整面积\n0.025\n（延伸到画外）", (4.92, 0.315), offset=(0, 0), ha="right", va="bottom")
label(ax, "2.776", (cut, 0.07), offset=(2, 0), ha="left", va="center")
ax.annotate("N(0,1)", xy=(-0.9, norm.pdf(-0.9)), xytext=(-3.0, 0.32), fontsize=13, ha="center", arrowprops=dict(arrowstyle="-|>", color="black", lw=1.0))
ax.annotate("t(4)", xy=(1.2, t.pdf(1.2, 4)), xytext=(3.2, 0.265), fontsize=13, ha="center", arrowprops=dict(arrowstyle="-|>", color="black", lw=1.0))
ax.annotate("t(1)", xy=(1.8, t.pdf(1.8, 1)), xytext=(3.6, 0.17), fontsize=13, ha="center", arrowprops=dict(arrowstyle="-|>", color="black", lw=1.0))
ax.set_xlim(-5, 5)
ax.set_ylim(0, 0.45)
ax.set_xlabel("x")
ax.set_ylabel("密度")
save(fig, "P10-n4")

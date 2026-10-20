import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from scipy.stats import chi2


fig, ax = new_fig(13, 8)
x = np.linspace(1e-4, 25, 1600)
specs = [(1, ":", 1.4), (2, "--", 1.5), (5, "-", 2.4), (10, "-.", 1.5)]
for df, ls, lw in specs:
    ax.plot(x, chi2.pdf(x, df), color=C.INK, ls=ls, lw=lw)

tail_x = x[x >= 11.07]
ax.fill_between(tail_x, 0, chi2.pdf(tail_x, 5), color=C.LIGHT, zorder=0)
ax.axvline(11.07, color=C.GRAY, ls=":", lw=1.0)
label(ax, "完整右尾面积约 0.05\n（尾部延伸到画外）", (24.2, 0.155), offset=(0, 0), ha="right", va="bottom")
label(ax, r"χ²$_{0.05}$(5)=11.07", (11.07, 0.10), offset=(5, 0), ha="left", va="center")
ax.annotate("n=1", xy=(0.5, chi2.pdf(0.5, 1)), xytext=(2.4, 0.45), fontsize=13, ha="center", arrowprops=dict(arrowstyle="-|>", color="black", lw=1.0))
ax.annotate("n=2", xy=(1.0, chi2.pdf(1.0, 2)), xytext=(2.6, 0.33), fontsize=13, ha="center", arrowprops=dict(arrowstyle="-|>", color="black", lw=1.0))
ax.annotate("n=5", xy=(4.0, chi2.pdf(4.0, 5)), xytext=(5.6, 0.22), fontsize=13, ha="center", arrowprops=dict(arrowstyle="-|>", color="black", lw=1.0))
ax.annotate("n=10", xy=(10.0, chi2.pdf(10.0, 10)), xytext=(8.0, 0.17), fontsize=13, ha="center", arrowprops=dict(arrowstyle="-|>", color="black", lw=1.0))
arrow(ax, (0.28, 0.46), (0, 0.09), color=C.INK, lw=1.1, offset=(4, 0))
label(ax, "向上无限陡", (0.28, 0.49), offset=(7, 0), ha="left", va="center")
ax.set_xlim(0, 25)
ax.set_ylim(0, 0.5)
ax.set_xlabel("x")
ax.set_ylabel("密度")
ax.set_xticks([0, 5, 10, 15, 20, 25])
save(fig, "P10-n2")

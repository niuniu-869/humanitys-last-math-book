import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from scipy.stats import poisson, binom

k = np.arange(10)
pois = poisson.pmf(k, 3)
bi = binom.pmf(k, 60, 0.05)
assert np.allclose(pois[:3], [0.0498, 0.1494, 0.2240], atol=5e-5)
assert np.allclose(bi[:3], [0.0461, 0.1455, 0.2259], atol=5e-5)

fig, ax = new_fig(15, 8)
w = 0.34
ax.bar(k - w / 2, pois, width=w, facecolor=C.LIGHT, edgecolor=C.INK,
       linewidth=0.9, label=r"实心：泊松 $P(3)$")
ax.bar(k + w / 2, bi, width=w, facecolor=C.PAPER, edgecolor=C.INK,
       linewidth=0.9, label=r"空心：二项 $B(60,0.05)$")
ax.set(xlim=(-0.65, 9.65), ylim=(0, 0.27), xticks=k,
       xlabel="$k$", ylabel="概率")
ax.grid(axis="y", ls=":", color=C.LIGHT, lw=0.7)
ax.set_axisbelow(True)
for j in [2, 3]:
    label(ax, "一样高", (j - w / 2, pois[j]), offset=(0, 7),
          ha="center", va="bottom", fontsize=8)
ax.legend(loc="upper right", handlelength=1.2)
save(fig, "P3-n5")

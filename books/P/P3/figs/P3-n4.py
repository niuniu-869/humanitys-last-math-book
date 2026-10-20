import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from scipy.stats import binom

fig, axes = new_fig(18, 5.8, ncols=3, sharey=True)
k = np.arange(11)
for ax, p, mode in zip(axes, [0.3, 0.5, 0.7], [3, 5, 7]):
    vals = binom.pmf(k, 10, p)
    assert np.argmax(vals) == mode
    assert np.isclose(vals.sum(), 1)
    ax.bar(k, vals, width=0.72, facecolor=C.LIGHT, edgecolor=C.INK, linewidth=0.8)
    ax.bar([mode], [vals[mode]], width=0.72, facecolor=C.PAPER, edgecolor=C.INK,
           linewidth=1.0, hatch="///")
    label(ax, f"最可能值 $k={mode}$", (mode, vals[mode]), offset=(0, 24 if p == 0.7 else 7),
          ha="center", va="bottom", fontsize=9)
    if p == 0.7:
        assert round(float(vals[mode]), 4) == 0.2668
        label(ax, f"{vals[mode]:.4f}", (mode, vals[mode]), offset=(0, 6),
              ha="center", va="bottom", fontsize=8)
    ax.set(xlim=(-0.6, 10.6), ylim=(0, 0.4), xticks=k,
           title=f"$p={p:.1f}$", xlabel="$k$")
    ax.grid(axis="y", ls=":", color=C.LIGHT, lw=0.7)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", labelsize=8)
axes[0].set_ylabel("概率")
fig.subplots_adjust(wspace=0.16)
save(fig, "P3-n4")

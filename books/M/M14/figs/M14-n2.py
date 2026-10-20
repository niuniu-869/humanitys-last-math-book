import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, axes = new_fig(21, 8, ncols=3, sharey=True)
fig.subplots_adjust(left=0.07, right=0.985, bottom=0.24, top=0.85, wspace=0.22)
z = np.array([2.0, 1.0, 0.0])
expected = [[0.8668, 0.1173, 0.0159], [0.6652, 0.2447, 0.0900],
            [0.5065, 0.3072, 0.1863]]
for ax, temperature, rounded, entropy in zip(axes, [0.5, 1, 2], expected, [0.441, 0.832, 1.020]):
    weights = np.exp((z-z.max()) / temperature)
    p = weights / weights.sum()
    h = -np.sum(p*np.log(p))
    assert np.isclose(p.sum(), 1)
    assert np.allclose(p, rounded, atol=0.00005)
    assert abs(h-entropy) < 0.0005
    ax.bar([1, 2, 3], p, width=0.58, facecolor=C.LIGHT, edgecolor=C.INK, lw=1)
    for x, value in enumerate(p, 1):
        label(ax, f"{value:.4f}", (x, value), offset=(0, 5), ha="center", fontsize=8)
    ax.set(ylim=(0, 1), xlim=(0.45, 3.55), xticks=[1, 2, 3],
           xticklabels=["词 1", "词 2", "词 3"], title=f"$T={temperature:g}$")
    ax.text(0.97, 0.96, f"熵 {h:.3f}", transform=ax.transAxes, ha="right", va="top", fontsize=9)
axes[0].set_ylabel("概率")
fig.text(0.5, 0.055, r"均匀分布的熵上限 $\ln 3\approx1.099$", ha="center", fontsize=9)
save(fig, "M14-n2")

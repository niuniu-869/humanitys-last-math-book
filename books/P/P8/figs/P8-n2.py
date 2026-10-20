import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

rng = np.random.default_rng(20261017)
ns = [10, 100, 1000, 10000]
fig, axes = new_fig(16, 7.2, ncols=4, sharex=True)
for ax, n in zip(axes, ns):
    means = rng.integers(1, 7, size=(2000, n)).mean(1)
    w = (35 / 12 / n) ** 0.5 / 3  # 每个小图的柱宽取标准差的 1/3，窄的分布也能看出形状
    bins = np.arange(1.5 + (3.5 - 1.5) % w - w, 5.5 + w, w)
    ax.hist(means, bins=bins, density=True, color=C.LIGHT, edgecolor=C.INK, linewidth=(0.8 if n <= 10 else 0.25))
    ax.axvline(3.5, color=C.GRAY, ls='--', lw=1.2)
    ax.set_xlim(1.5, 5.5)
    ax.set_title(f'$n={n}$')
    ax.set_xlabel('平均')
    ax.set_ylabel('频率密度')
    ax.grid(False)
fig.subplots_adjust(wspace=0.35)
save(fig, 'P8-n2')

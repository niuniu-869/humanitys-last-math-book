import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

rng = np.random.default_rng(1)
x = rng.uniform(0, 10, size=(20000, 10))
ests = [x.max(axis=1), 2*x.mean(axis=1), 1.1*x.max(axis=1)]
titles = ['最大值 $M$', '矩估计 $2\\bar X$', '修正后 $\\frac{n+1}{n}M$']
fig, axes = new_fig(15, 5.2, ncols=3, sharex=True)
for ax, e, title in zip(axes, ests, titles):
    ax.hist(e, bins=36, range=(4, 16), density=True, color=C.LIGHT, edgecolor=C.INK, ls='-')
    ax.axvline(10, color=C.INK, ls='--', lw=1.1)
    ax.axvline(e.mean(), color=C.GRAY, ls=':', lw=1.1)
    label(ax, f'均值={e.mean():.2f}\n标准差={e.std():.2f}', (0.03, 0.96), xycoords='axes fraction', offset=(0, 0), va='top', size=8)
    ax.set_title(title)
    ax.set_xlim(4, 16)
    ax.set_ylim(bottom=0)
axes[0].set_ylabel('密度')
for ax in axes:
    ax.set_xlabel('估计值')
save(fig, "P11-n4")

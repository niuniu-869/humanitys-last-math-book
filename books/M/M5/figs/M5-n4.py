import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

eigenvalues = np.array([7., 2., 1.])
indices = np.arange(1, 4)
cumulative = np.cumsum(eigenvalues) / eigenvalues.sum() * 100
assert np.allclose(cumulative, [70, 90, 100])
fig, axes = new_fig(17, 7.8, ncols=2)
axes[0].plot(indices, eigenvalues, 'o-', color=C.INK, markersize=5)
axes[0].set(ylabel='特征值', ylim=(0, 8))
axes[1].step(indices, cumulative, where='post', color=C.INK, ls='-')
axes[1].scatter(indices, cumulative, color=C.INK, s=25, zorder=4)
axes[1].axhline(90, color=C.GRAY, ls='--', lw=1.1)
axes[1].set(ylabel='累计贡献率', ylim=(0, 110))
axes[1].set_yticks([0, 20, 40, 60, 80, 100], ['0%', '20%', '40%', '60%', '80%', '100%'])
for i, value in zip(indices, cumulative):
    label(axes[1], f'{value:.0f}%', (i, value), offset=(0, 8), ha='center', fontsize=9)
for ax in axes:
    ax.set(xlim=(.7, 3.3), xlabel='主成分序号')
    ax.set_xticks(indices)
fig.tight_layout(w_pad=2)
save(fig, "M5-n4")

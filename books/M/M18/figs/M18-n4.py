import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

d, warmup = 512, 4000
step = np.arange(1, 20001)
rate = d**-0.5 * np.minimum(step**-0.5, step*warmup**-1.5)
peak = d**-0.5 * warmup**-0.5
later = d**-0.5 * 10000**-0.5
assert np.argmax(rate)+1 == warmup
assert f'{peak:.2e}' == '6.99e-04'
assert f'{later:.2e}' == '4.42e-04'
fig, ax = new_fig(16, 10)
rise = np.linspace(0, 8000, 401)
fall = np.linspace(1000, 20000, 700)
ax.plot(rise, d**-0.5*rise*warmup**-1.5*1e4,
        color=C.GRAY, ls='--', lw=1.4, label='预热线的延长')
ax.plot(fall, d**-0.5*fall**-0.5*1e4,
        color=C.GRAY, ls=':', lw=1.6, label='衰减线的延长')
ax.plot(np.r_[0, step], np.r_[0, rate]*1e4,
        color=C.INK, ls='-', lw=1.8, label='学习率')
dot(ax, (warmup, peak*1e4))
label(ax, r'峰值 $6.99\times10^{-4}$', (warmup, peak*1e4), offset=(14, 13))
ax.scatter(10000, later*1e4, s=40, facecolor=C.PAPER, edgecolor=C.INK, zorder=5)
label(ax, r'$4.42\times10^{-4}$', (10000, later*1e4), offset=(10, 15))
ax.set(xlim=(0, 20000), ylim=(0, 15), xlabel='step', ylabel=r'学习率（$10^{-4}$）')
ax.set_xticks([0, 4000, 8000, 10000, 15000, 20000])
ax.tick_params(axis='x', labelsize=9)
handles, labels = ax.get_legend_handles_labels()
ax.legend([handles[i] for i in [2, 0, 1]], [labels[i] for i in [2, 0, 1]], loc='upper right')
fig.tight_layout()
save(fig, "M18-n4")

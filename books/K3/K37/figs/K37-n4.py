import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

t = np.arange(23)
bound = 2.0**(-t)
assert bound[19] > 1e-6 > bound[20]
assert np.flatnonzero(bound < 1e-6)[0] == 20
fig, ax = new_fig(17, 11)
ax.set_yscale('log')
ax.plot(t, bound, color=C.INK, ls='-', marker='o', markersize=3.8, lw=1.4)
ax.axhline(1e-6, color=C.RED, ls='--', lw=1.2)
ax.plot(19, bound[19], marker='o', ms=7.5, mfc=C.PAPER, mec=C.INK, mew=1.4, zorder=5)
ax.plot(20, bound[20], marker='o', ms=7, mfc=C.INK, mec=C.INK, zorder=5)
label(ax, r'$2^{-t}$', (8, bound[8]), (12, 5))
label(ax, '百万分之一', (2, 1e-6), (0, 8))
label(ax, '19 次尚不能\n统一保证', (19, bound[19]), (0, 32), ha='center', va='bottom')
label(ax, '20 次', (20, bound[20]), (-5, -25), ha='right')
ax.set(xlim=(0, 22), ylim=(1e-7, 1), xlabel=r'重复次数 $t$', ylabel='错误率上界')
ax.set_xticks([0, 5, 10, 15, 19, 20, 22])
ax.tick_params(axis='x', labelsize=9)
ax.set_yticks(10.0**np.arange(-7, 1))
ax.minorticks_off()
fig.tight_layout()
save(fig, "K37-n4")

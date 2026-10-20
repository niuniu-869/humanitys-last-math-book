import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

n = np.array([10, 100, 1000, 10000, 100000, 1000000], dtype=float)
f = np.array([.2000, .1400, .1660, .1627, .1652, .1667])
assert np.allclose(f, [.2, .14, .166, .1627, .1652, .1667])
fig, ax = new_fig(14, 8)
ax.plot(n, f, color=C.INK, ls='-', marker='o', ms=5.5, lw=1.6, markerfacecolor=C.INK)
ax.axhline(1/6, color=C.GRAY, ls='--', lw=1.2)
label(ax, r'$\frac{1}{6}\approx0.1667$', (250, 1/6), offset=(0, 26), ha='left', fontsize=10)
for x, y in zip(n, f):
    label(ax, f'{y:.4f}', (x, y), offset=(0, 12 if y >= .16 else -20), ha='center', fontsize=8.5)
ax.set_xscale('log'); ax.set(xlim=(4, 1.5e6), ylim=(0, .3), xlabel='$n$', ylabel='和为 7 的频率')
ax.set_xticks(n); ax.set_xticklabels([r'$10^1$', r'$10^2$', r'$10^3$', r'$10^4$', r'$10^5$', r'$10^6$'])
ax.set_yticks(np.arange(0, .31, .05))
save(fig, 'P1-n3')

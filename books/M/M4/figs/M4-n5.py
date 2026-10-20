import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

x = np.arange(1, 6)
y = np.array([2, 3, 5, 6, 9], dtype=float)
eta = 0.5
f0 = np.full(5, y.mean())
residual = y-f0
f1 = f0 + eta*np.where(x < 2.5, residual[:2].mean(), residual[2:].mean())
residual = y-f1
f2 = f1 + eta*np.where(x < 4.5, residual[:4].mean(), residual[4:].mean())
assert np.allclose(f1, [15/4, 15/4, 35/6, 35/6, 35/6])
assert np.allclose(f2, [161/48, 161/48, 87/16, 87/16, 89/12])
print('M4-n5 F1:', f1.tolist(), 'F2:', f2.tolist())
fig, ax = new_fig(12, 8)
ax.scatter(x, y, s=30, color=C.INK, marker='o', zorder=5, label='数据')
ax.plot([0.65, 5.35], [5, 5], color=C.GRAY, lw=0.8, ls='-', label='$F_0$')
ax.stairs([f1[0], f1[2]], [0.65, 2.5, 5.35], baseline=None,
          color=C.INK, ls='--', lw=1.5, label='$F_1$')
ax.stairs([f2[0], f2[2], f2[4]], [0.65, 2.5, 4.5, 5.35], baseline=None,
          color=C.INK, ls='-.', lw=1.5, label='$F_2$')
ax.set(xlim=(0.6, 5.4), ylim=(0, 10), xlabel='$x$', ylabel='$y$')
ax.set_xticks(x)
label(ax, r'$\eta=0.5$', (3.1, 8.6))
ax.legend(loc='upper left', ncol=2, fontsize=9, handlelength=2.7)
fig.tight_layout()
save(fig, "M4-n5")

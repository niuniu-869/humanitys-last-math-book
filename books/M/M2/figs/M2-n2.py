import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

x = np.arange(1, 6, dtype=float)
y = np.array([2, 3, 5, 6, 9], dtype=float)
line = 1.7 * x - 0.1

fig, ax = new_fig(12, 7.5)
xx = np.linspace(0.7, 5.35, 300)
ax.plot(xx, 1.7 * xx - 0.1, color=C.INK, ls='-', label=r'$\hat y=1.7x-0.1$')
for xi, yi, yi_hat in zip(x, y, line):
    ax.plot([xi, xi], [yi_hat, yi], color=C.GRAY, ls='--', lw=1.0)
ax.scatter(x, y, s=34, color=C.INK, zorder=5)

# A small vertical normal density centered at the fitted mean for x=3.
mu = 1.7 * 3 - 0.1
sigma = 0.72
yy = np.linspace(mu - 2.0, mu + 2.0, 180)
width = 0.32 * np.exp(-0.5 * ((yy - mu) / sigma) ** 2)
ax.fill_betweenx(yy, 3, 3 + width, color=C.LIGHT, alpha=0.8, zorder=1)
ax.plot(3 + width, yy, color=C.GRAY, lw=1.0, zorder=2)
label(ax, r'$N(wx+b,\,\sigma^2)$', (3.05, mu + 2.0), offset=(4, 0), color=C.GRAY, fontsize=8.5)
label(ax, '残差', (4.2, 7.0), offset=(5, 0), color=C.GRAY, fontsize=8.5)
ax.set(xlim=(0.7, 5.45), ylim=(0.6, 9.8), xlabel='$x$', ylabel='$y$')
save(fig, 'M2-n2')

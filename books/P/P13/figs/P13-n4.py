import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

x = np.arange(1, 6)
y = np.array([2, 3, 5, 4, 6])
slope, intercept = np.polyfit(x, y, 1)
yhat = intercept + slope * x
residuals = y - yhat
assert np.allclose([intercept, slope], [1.3, .9])
assert np.allclose(residuals[[2, 3]], [1, -.9])
fig, ax = new_fig(14, 10)
xx = np.linspace(0, 6, 200)
ax.plot(xx, intercept + slope * xx, color=C.INK, ls='-', label=r'$\hat y=1.3+0.9x$')
ax.vlines(x, yhat, y, color=C.GRAY, ls=':', lw=1.4)
ax.scatter(x, yhat, facecolor=C.PAPER, edgecolor=C.INK, s=30, zorder=4)
ax.scatter(x, y, facecolor=C.INK, edgecolor=C.INK, s=30, zorder=5)
ax.scatter([x.mean()], [y.mean()], marker='s', color=C.INK, s=38, zorder=6)
label(ax, r'$(\bar x,\bar y)$', (3, 4), offset=(0, -30), ha='center')
label(ax, '$1.0$', (3, 4.65), offset=(-8, 0), ha='right')
label(ax, '$-0.9$', (4, 4.4), offset=(9, 0))
ax.set(xlim=(0, 6), ylim=(0, 7), xlabel='$x$', ylabel='$y$')
ax.legend(loc='upper left')
fig.subplots_adjust(left=.12, right=.97, bottom=.13, top=.96)
save(fig, "P13-n4")

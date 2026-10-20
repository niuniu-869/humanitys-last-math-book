import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

from matplotlib.path import Path
from matplotlib.patches import PathPatch

fig, ax = new_fig(18, 11)
x = np.arange(1, 6)
y = np.array([2, 3, 5, 4, 6])
slope, intercept = np.polyfit(x, y, 1)
yhat = intercept + slope * 5
mean = y.mean()
assert np.allclose([yhat, mean, 6-yhat], [5.8, 4, .2])
xx = np.linspace(0, 5.35, 200)
ax.plot(xx, intercept+slope*xx, color=C.INK, ls='-', label=r'$\hat y=1.3+0.9x$')
ax.axhline(mean, color=C.GRAY, ls='--', lw=1.1)
ax.scatter(x[:-1], y[:-1], facecolor=C.PAPER, edgecolor=C.AMBER, s=27)
ax.plot([5, 5], [mean, yhat], color=C.INK, lw=3.2)
ax.plot([5, 5], [yhat, 6], color=C.INK, lw=1)
ax.scatter([5], [yhat], facecolor=C.PAPER, edgecolor=C.INK, s=30, zorder=5)
dot(ax, (5, 6), size=30)
label(ax, r'$\bar y=4$', (.15, 4), offset=(0, 7))
label(ax, r'$\hat y_i-\bar y$'+'\n回归解释的部分', (5, 4.8), offset=(-135, 55), ha='center', va='center',
      arrowprops=dict(arrowstyle='-', color=C.GRAY, lw=.7))
label(ax, r'$y_i-\hat y_i$（残差）', (5, 5.9), offset=(-25, 36), ha='right',
      arrowprops=dict(arrowstyle='-', color=C.GRAY, lw=.7))
# A data-coordinate brace preserves the exact total-deviation endpoints.
verts = [(5.6, 4), (5.88, 4), (5.6, 4.8), (5.95, 5),
         (5.6, 5.2), (5.88, 6), (5.6, 6)]
ax.add_patch(PathPatch(Path(verts, [Path.MOVETO]+[Path.CURVE4]*6),
                       fill=False, edgecolor=C.INK, lw=1.1))
label(ax, r'$y_i-\bar y$', (6, 5), offset=(7, 0), va='center')
ax.set(xlim=(0, 7.1), ylim=(0, 7.2), xlabel='$x$', ylabel='$y$')
ax.set_xticks(range(7))
ax.legend(loc='upper left')
fig.subplots_adjust(left=.09, right=.97, bottom=.12, top=.96)
save(fig, "P13-n5")

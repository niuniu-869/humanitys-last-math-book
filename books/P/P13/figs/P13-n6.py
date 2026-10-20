import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

x = np.arange(1, 6)
y = np.array([2, 3, 5, 4, 6])
slope, intercept = np.polyfit(x, y, 1)
sigma, t = .796, 3.182
sxx = np.sum((x-x.mean())**2)
xx = np.linspace(0, 7, 701)
fit = intercept+slope*xx
se = 1/len(x)+(xx-x.mean())**2/sxx
ci = t*sigma*np.sqrt(se)
pi = t*sigma*np.sqrt(1+se)
fig, ax = new_fig(17, 11)
ax.axvspan(1, 5, facecolor=C.LIGHT, zorder=0)
ax.plot(xx, fit, color=C.INK, ls='-', label='回归直线')
for width, ls, text in [(ci, '--', '均值的 95% 置信带'), (pi, ':', '新观测的 95% 预测带')]:
    ax.plot(xx, fit-width, color=C.INK, ls=ls, lw=1.3, label=text)
    ax.plot(xx, fit+width, color=C.INK, ls=ls, lw=1.3)
ax.scatter(x, y, color=C.INK, s=24, zorder=5)
for width, ls, dx, ha in [(t*sigma*np.sqrt(.2), '--', 9, 'left'),
                          (t*sigma*np.sqrt(1.2), ':', -9, 'right')]:
    low, high = y.mean()-width, y.mean()+width
    ax.plot([3, 3], [low, high], color=C.GRAY, ls=ls, lw=.9)
    ax.hlines([low, high], 2.88, 3.12, color=C.INK, lw=1.3)
    for end in [low, high]:
        label(ax, f'${end:.2f}$', (3, end), offset=(dx, -6 if dx > 0 else 8), ha=ha, va='center')
assert np.allclose(np.round([4-ci[300], 4+ci[300], 4-pi[300], 4+pi[300]], 2), [2.87, 5.13, 1.23, 6.77])
label(ax, '已有数据范围', (3, -1.55), ha='center')
ax.set(xlim=(0, 7), ylim=(-2, 12), xlabel='$x$', ylabel='$y$')
ax.legend(loc='upper left', fontsize=9)
fig.subplots_adjust(left=.1, right=.97, bottom=.12, top=.97)
save(fig, "P13-n6")

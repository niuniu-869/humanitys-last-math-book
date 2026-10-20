import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

from scipy.stats import norm

delta = np.linspace(0, 5, 600)
def power(n):
    return 1 - norm.cdf(1.645 - delta * np.sqrt(n) / 6)

fig, ax = new_fig(14, 8)
ax.plot(delta, power(36), color=C.INK, ls='-', lw=1.8)
ax.plot(delta, power(100), color=C.GRAY, ls='--', lw=1.8)
ax.plot(delta, power(78), color=C.GRAY, ls=':', lw=1.3)
ax.axhline(.9, color=C.GRAY, ls=':', lw=1.1)
p36 = float(1 - norm.cdf(1.645 - 2 * np.sqrt(36) / 6))
p78 = float(1 - norm.cdf(1.645 - 2 * np.sqrt(78) / 6))
ax.scatter([2], [p36], s=45, color=C.INK, zorder=5)
ax.scatter([2], [p78], s=45, facecolors=C.PAPER, edgecolors=C.INK, marker='s', zorder=5)
label(ax, '功效 0.639', (2, p36), offset=(7, -17), ha='left')
label(ax, '功效 0.903', (2, p78), offset=(7, 8), ha='left')
label(ax, 'n=100', (0.987, .5), offset=(-8, 0), ha='right')
label(ax, 'n=78', (1.69, .8), offset=(8, -6), ha='left')
label(ax, 'n=36', (1.645, .5), offset=(8, -8), ha='left')
label(ax, '功效 0.9', (4.9, .9), offset=(0, -20), ha='right')
label(ax, r'$\alpha=0.05$', (0, .05), offset=(7, 8), ha='left')
ax.set(xlim=(0, 5), ylim=(0, 1), xlabel=r'$\delta$', ylabel='功效')
ax.set_yticks([0, .05, .25, .5, .75, .9, 1])
fig.subplots_adjust(left=.12, right=.97, bottom=.16, top=.96)
save(fig, 'P12-n5')

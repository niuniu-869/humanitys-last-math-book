import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

from scipy.stats import t

data = np.array([12.1, 11.6, 12.4, 11.9, 12.3, 11.7])
xbar = data.mean()
s = data.std(ddof=1)
se = s / np.sqrt(len(data))
mu = np.linspace(11.2, 12.8, 700)
p = 2 * t.sf(np.abs(xbar - mu) / se, df=5)
fig, ax = new_fig(14, 8)
ax.plot(mu, p, color=C.INK, ls='-', lw=1.8)
ax.axhline(.05, color=C.GRAY, ls='--', lw=1.1)
for c in (11.66, 12.34):
    ax.axvline(c, color=C.GRAY, ls=':', lw=1.1)
ax.plot([11.66, 12.34], [0.015, 0.015], color=C.INK, ls='-', lw=4.0, solid_capstyle='butt')
label(ax, '95% 置信区间', (12.0, .015), offset=(0, 10), ha='center')
label(ax, '$p=0.05$', (12.69, .05), offset=(4, 3), ha='left')
p118 = 2 * t.sf(abs(xbar - 11.8) / se, 5)
p116 = 2 * t.sf(abs(xbar - 11.6) / se, 5)
ax.scatter([11.8], [p118], s=45, facecolors=C.PAPER, edgecolors=C.INK, zorder=5)
ax.scatter([11.6], [p116], s=45, facecolors=C.INK, edgecolors=C.INK, zorder=5)
label(ax, r'$\mu_0=11.8$, $p=0.189$', (11.8, p118), offset=(7, 8), ha='left')
label(ax, r'$\mu_0=11.6$, $p=0.029$', (11.6, p116), offset=(-7, 15), ha='right')
ax.set(xlim=(11.2, 12.8), ylim=(0, 1.05), xlabel=r'$\mu_0$', ylabel='$p$ 值')
ax.set_yticks([0, .05, .25, .5, .75, 1.0])
fig.subplots_adjust(left=.12, right=.97, bottom=.16, top=.96)
save(fig, 'P12-n4')

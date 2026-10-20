import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

from scipy.stats import norm

fig, ax = new_fig(14, 8)
x = np.linspace(166, 176, 900)
f0 = norm.pdf(x, 170, 1)
f1 = norm.pdf(x, 172, 1)
crit = 171.645
ax.plot(x, f0, color=C.INK, ls='-', lw=1.8)
ax.plot(x, f1, color=C.GRAY, ls='--', lw=1.8)
ax.fill_between(x[x >= crit], 0, f0[x >= crit], color=C.LIGHT, edgecolor=C.INK, linewidth=0.5)
ax.fill_between(x[x <= crit], 0, f1[x <= crit], facecolor=C.PAPER, edgecolor=C.GRAY,
                hatch='///', linewidth=0.0)
ax.axvline(crit, color=C.INK, ls='--', lw=1.2)
label(ax, '临界值 171.645', (crit, 0.425), ha='center')
ax.annotate(r'$\alpha=0.05$', xy=(172.0, 0.03), xytext=(173.3, 0.17), ha='center', arrowprops=dict(arrowstyle='->', color='k'))
ax.annotate(r'$\beta=0.361$', xy=(171.0, 0.12), xytext=(168.3, 0.2), ha='center', arrowprops=dict(arrowstyle='->', color='k'))
label(ax, '不拒绝', (169.1, 0.012), ha='center')
label(ax, '拒绝', (174.3, 0.012), ha='center')
label(ax, r'浅灰 = $\alpha$，斜线 = $\beta$', (166.2, 0.38), ha='left')
ax.set(xlim=(166, 176), ylim=(0, .43), xlabel=r'$\bar x$', ylabel='密度')
ax.set_xticks([166, 168, 170, 172, 174, 176])
fig.subplots_adjust(left=.12, right=.97, bottom=.16, top=.96)
save(fig, 'P12-n2')

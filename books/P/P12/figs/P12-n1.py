import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

from scipy.stats import norm

fig, ax = new_fig(14, 8)
x = np.linspace(-4, 4, 800)
y = norm.pdf(x)
ax.plot(x, y, color=C.INK, ls='-', lw=1.8)

left = x <= -1.96
right = x >= 1.96
ax.fill_between(x[left], 0, y[left], color=C.LIGHT, edgecolor=C.INK, linewidth=0.5)
ax.fill_between(x[right], 0, y[right], color=C.LIGHT, edgecolor=C.INK, linewidth=0.5)
for c in (-1.96, 1.96):
    ax.axvline(c, color=C.GRAY, ls='--', lw=1.2)
ax.axvline(2.1, color=C.INK, ls='-', lw=1.4)
label(ax, '观察值 $u=2.1$', (2.1, norm.pdf(2.1)), offset=(8, 18), ha='left')
label(ax, '0.025', (-2.55, 0.055), ha='center')
label(ax, '0.025', (2.55, 0.055), ha='center')
label(ax, '不拒绝', (0, 0.18), ha='center')
label(ax, '阴影 = 拒绝域', (-3.9, 0.30), ha='left')
ax.set(xlim=(-4, 4), ylim=(0, 0.46), xlabel='$u$', ylabel='密度')
ax.set_xticks([-4, -1.96, 0, 1.96, 4])
fig.subplots_adjust(left=.12, right=.97, bottom=.16, top=.96)
save(fig, 'P12-n1')

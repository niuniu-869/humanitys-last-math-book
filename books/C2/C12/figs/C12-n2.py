import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(14, 8.4)
eps = 0.05
x = np.linspace(0.012, 1, 1000)
xs = np.linspace(eps, 1, 700)
ys = 1 / np.sqrt(xs)
yi = 1 / xs

ax.fill_between(xs, 0, ys, color=C.LIGHT, zorder=1)
ax.fill_between(xs, ys, yi, facecolor=C.PAPER, edgecolor=C.GRAY,
                hatch='///', linewidth=0, zorder=1)
ax.plot(x, 1 / np.sqrt(x), color=C.INK, ls='-', zorder=3)
ax.plot(x, 1 / x, color=C.GRAY, ls='--', zorder=3)
ax.axvline(eps, color=C.GRAY, ls=':', lw=1.2, zorder=2)

label(ax, r'$y=\frac{1}{\sqrt{x}}$', (0.86, 2.2), offset=(0, 0), ha='center')
label(ax, r'$y=\frac{1}{x}$', (0.23, 4.35), offset=(6, 2), ha='left')
label(ax, r'$\varepsilon$', (eps, 0), offset=(5, 8), ha='left', va='bottom')
label(ax, r'面积 $2-2\sqrt{\varepsilon}\approx1.55$', (0.58, 0.83),
      ha='center', va='center', fontsize=9)
label(ax, r'浅灰与斜线合计面积 $\ln\frac{1}{\varepsilon}\approx3.00$',
      (0.63, 3.4), ha='center', va='center', fontsize=9)
label(ax, r'浅灰 = $1/\sqrt{x}$ 下方；斜线阴影 = $1/x$ 下方比 $1/\sqrt{x}$ 多出的部分',
      (0.53, -0.5), ha='center', va='top', fontsize=8.5)
arrow(ax, (0.016, 7.35), (0, 0.55), color=C.INK, lw=1.3)
arrow(ax, (0.012, 7.35), (0, 0.55), color=C.GRAY, lw=1.3)

ax.set(xlim=(-0.02, 1.03), ylim=(-1.2, 8), xlabel='$x$', ylabel='$y$')
ax.set_xticks([eps, .25, .5, .75, 1])
ax.set_yticks([0, 2, 4, 6, 8])
fig.tight_layout()
save(fig, 'C12-n2')

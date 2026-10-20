import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(14, 8.2)
x = np.linspace(0, 4, 900)
g = np.exp(-x**2)
e = np.exp(-x)
xs = np.linspace(1, 4, 650)
ax.fill_between(xs, 0, np.exp(-xs**2), color=C.LIGHT, zorder=1)
ax.fill_between(xs, np.exp(-xs**2), np.exp(-xs), facecolor=C.PAPER,
                edgecolor=C.GRAY, hatch='///', linewidth=0, zorder=1)
ax.plot(x, g, color=C.INK, ls='-', zorder=3)
ax.plot(x, e, color=C.GRAY, ls='--', zorder=3)
ax.axvline(1, color=C.GRAY, ls=':', lw=1.2, zorder=2)

ax.scatter([0, 1], [1, np.exp(-1)], s=34, facecolors=C.PAPER,
           edgecolors=C.INK, linewidths=1.1, zorder=5)
label(ax, r'实线 $y=e^{-x^2}$', (0.05, 0.30), offset=(0, 0), ha='left')
label(ax, r'虚线 $y=e^{-x}$', (2.2, 0.22), offset=(0, 0), ha='left')
label(ax, '$x=1$', (1, 0.95), offset=(5, 0), ha='left', va='center')
label(ax, '普通定积分', (0.5, 0), offset=(0, 10), ha='center', va='bottom', fontsize=9)
label(ax, '反常部分', (3.0, 0.55), offset=(0, 10), ha='center', va='bottom', fontsize=9)
label(ax, r'$e^{-1}\approx0.368$', (1, np.exp(-1)), offset=(10, 0), ha='left', va='center')
label(ax, r'$\int_1^{+\infty}e^{-x^2}\,\mathrm{d}x$', (3.0, 0.42),
      ha='center', va='center', fontsize=9)
label(ax, r'浅灰 = $e^{-x^2}$ 下方；斜线阴影 = $e^{-x}$ 下方比 $e^{-x^2}$ 多出的部分',
      (2, -0.07), ha='center', va='top', fontsize=8.5)

ax.set(xlim=(-0.12, 4.1), ylim=(-0.15, 1.05), xlabel='$x$', ylabel='$y$')
ax.set_xticks([0, 1, 2, 3, 4])
ax.set_yticks([0, .2, .4, .6, .8, 1.0])
fig.tight_layout()
save(fig, 'C12-n3')

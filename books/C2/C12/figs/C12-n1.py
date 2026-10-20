import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(14, 8.2)
x = np.linspace(1, 12, 900)
y2 = 1 / x**2
y1 = 1 / x
x_fill = np.linspace(1, 10, 700)

ax.fill_between(x_fill, 0, 1 / x_fill**2, color=C.LIGHT, zorder=1)
ax.fill_between(x_fill, 1 / x_fill**2, 1 / x_fill, facecolor=C.PAPER,
                edgecolor=C.GRAY, hatch='///', linewidth=0, zorder=1)
ax.plot(x, y2, color=C.INK, ls='-', label=r'$y=1/x^2$', zorder=3)
ax.plot(x, y1, color=C.GRAY, ls='--', label=r'$y=1/x$', zorder=3)
ax.axvline(10, color=C.GRAY, ls=':', lw=1.2, zorder=2)

label(ax, r'$y=\frac{1}{x^2}$', (11.6, 0.03), offset=(0, 4), ha='right')
label(ax, r'$y=\frac{1}{x}$', (11.6, 0.12), offset=(0, 6), ha='right')
label(ax, '$b=10$', (10, 0.9), offset=(5, 0), ha='left', va='center')
label(ax, r'面积 $1-\frac{1}{b}$，$b=10$ 时为 0.9，永远小于 1',
      (7.2, 0.62), ha='center', va='center', fontsize=9)
label(ax, r'$\ln b$，$b=10$ 时为 2.30，无上界',
      (7.2, 0.50), ha='center', va='center', fontsize=9)
label(ax, '浅灰 = $1/x^2$ 下方；斜线阴影 = $1/x$ 下方比 $1/x^2$ 多出的部分',
      (6.5, -0.08), ha='center', va='top', fontsize=8.5)

ax.set(xlim=(0.8, 12.2), ylim=(-0.16, 1.1), xlabel='$x$', ylabel='$y$')
ax.set_xticks([1, 5, 10, 12])
ax.set_yticks([0, .2, .4, .6, .8, 1.0])
fig.tight_layout()
save(fig, 'C12-n1')

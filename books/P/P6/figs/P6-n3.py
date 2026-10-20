import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(12, 11)
x = np.linspace(-1, 3, 601)
ax.fill_between(x, -1, 2-x, color=C.LIGHT)
ax.fill_between(x, 2-x, 2.6-x, color=C.AMBER, alpha=0.45, hatch='///', edgecolor=C.GRAY, linewidth=0)
ax.plot(x, 2-x, color=C.INK, ls='-')
ax.plot(x, 2.6-x, color=C.INK, ls='--')
for px, xlab in [(0.65, '$x_1$'), (1.5, '$x_2$')]:
    py = 2-px
    ax.plot([px, px], [0, py], color=C.INK, ls=':')
    ax.plot(px, py, 'o', mfc=C.PAPER, mec=C.INK, ms=6, zorder=5)
    label(ax, xlab, (px, 0), (0, -15), ha='center')
label(ax, '$y=z-x$', (-0.8, 1.6))
label(ax, r'$x+y\leq z$', (-0.7, 0.65))
label(ax, r'$z$ 到 $z+\Delta z$', (1.7, 1.75), ha='center')
arrow(ax, (1.7, 1.65), (-0.48, -0.54), color=C.INK, lw=0.8)
label(ax, '$x+y=2$', (2.55, -0.55), (-3, -20), ha='right')
for side in ['left', 'bottom']:
    ax.spines[side].set_position('zero')
ax.set(xlim=(-1, 3), ylim=(-1, 3), aspect='equal')
ax.set_xticks([-1, 0, 2, 3])
ax.set_yticks([-1, 1, 2, 3])
label(ax, '$x$', (2.9, 0), (0, 7))
label(ax, '$y$', (0, 2.9), (7, 0))
save(fig, 'P6-n3')

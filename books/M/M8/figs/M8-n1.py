import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(13, 8)
k = np.arange(0, 11)
curves = [
    ((1 / 4) ** k, '-', 'o', True, C.BLUE, r'sigmoid, $w=1$'),
    ((1 / 2) ** k, '--', 'o', False, C.RED, r'sigmoid, $w=2$'),
    ((1.5) ** k, '-.', 's', True, C.TEAL, r'放大方向'),
    ((0.5) ** k, ':', 's', False, C.AMBER, r'缩小方向'),
]
for y, ls, marker, filled, color, lab in curves:
    ax.plot(k, y, ls=ls, marker=marker, color=color, label=lab,
            markerfacecolor=color if filled else C.PAPER,
            markeredgecolor=color, markersize=5.5, linewidth=1.7)
ax.axhline(1, color=C.GRAY, ls=':', lw=1.0)
ax.set_yscale('log')
ax.set_ylim(1e-7, 1e2)
ax.set_xlim(-0.2, 15.5)
ax.set_xticks(k)
ax.set_xlabel('回传的层数')
ax.set_ylabel('误差信号的倍数')
ax.grid(True, axis='y', which='major', color=C.LIGHT, lw=0.6)
ax.legend(loc='lower left', fontsize=8)
label(ax, r'$9.5\times10^{-7}$', (10, (1/4)**10), offset=(8, -3), fontsize=8)
label(ax, r'$9.8\times10^{-4}$（$w=2$ 与缩小方向重合）', (10, (1/2)**10), offset=(8, -3), fontsize=8)
label(ax, r'$57.7$', (10, 1.5**10), offset=(8, -3), fontsize=8)
save(fig, "M8-n1")

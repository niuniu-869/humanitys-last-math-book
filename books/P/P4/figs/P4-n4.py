import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(14, 8.5)
fig.subplots_adjust(left=0.12, right=0.97, bottom=0.16, top=0.95)
x = np.linspace(-6, 6, 1201)
for mu, sigma, style, name in [(0, 1, '-', '$N(0,1)$'),
                              (0, 2, '--', '$N(0,4)$'),
                              (2, 1, ':', '$N(2,1)$')]:
    density = np.exp(-0.5 * ((x - mu) / sigma) ** 2) / (sigma * np.sqrt(2 * np.pi))
    ax.plot(x, density, color=C.INK, ls=style, label=name)
peak = 1 / np.sqrt(2 * np.pi)
label(ax, f'{peak:.4f}', (0, peak), (0, 9), ha='center')
label(ax, f'{peak / 2:.4f}', (0, peak / 2), (0, -5), ha='center', va='top')
ax.plot([-1, 1], [peak * np.exp(-0.5)] * 2, ls='None', marker='o',
        mfc=C.PAPER, mec=C.INK, ms=5, zorder=5)
label(ax, '拐点', (-1, peak * np.exp(-0.5)), (-35, 10), ha='right')
ax.set(xlim=(-6, 6), ylim=(0, 0.46), xlabel='$x$', ylabel='密度',
       xticks=[-6, -4, -2, -1, 0, 1, 2, 4, 6], yticks=[0, 0.1, 0.2, 0.3, 0.4])
ax.legend(loc='upper left', handlelength=2.8)
save(fig, "P4-n4")

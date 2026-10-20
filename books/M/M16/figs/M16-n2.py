import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import FancyArrowPatch

fig, ax = new_fig(14, 8)
x = np.linspace(0.5, 5, 700)
y = np.log(x)
ax.plot(x, y, color=C.INK, lw=2)
ax.plot([1, 4], [0, np.log(4)], ls='--', color=C.RED, lw=1.6)
dot(ax, (1, 0), color=C.INK, size=30)
dot(ax, (4, np.log(4)), color=C.INK, size=30)
xm = 2.5
yc = np.log(xm)
ych = (np.log(4) / 3) * 1.5
yt = yc + 0.4 * (x - xm)
ax.plot([xm, xm], [0, yc], ls=':', color=C.GRAY, lw=1.1)
ax.plot(x, yt, ls=':', color=C.TEAL, lw=1.2)
ax.scatter([xm], [yc], s=42, facecolors=C.PAPER, edgecolors=C.INK, zorder=5)
ax.scatter([xm], [ych], s=44, marker='s', color=C.INK, zorder=5)
gap = yc - ych
assert np.isclose(gap, 0.2231, atol=5e-5)
ax.add_patch(FancyArrowPatch((xm, ych), (xm, yc), arrowstyle='<->', mutation_scale=12,
                             color=C.RED, lw=1.3))
label(ax, '$\\log E[X]$', (xm, yc), offset=(8, 4), ha='left')
label(ax, '$E[\\log X]$', (xm, ych), offset=(8, -13), ha='left')
label(ax, '差距 0.2231', (xm, (yc + ych) / 2), offset=(10, 0), ha='left', color=C.RED)
label(ax, '对数曲线', (4.05, np.log(4.05)), offset=(5, -12))
label(ax, '切线', (4.35, yc + 0.4 * (4.35 - xm)), offset=(5, 5), color=C.TEAL)
ax.set(xlim=(0.5, 5), ylim=(-0.35, 1.85), xlabel='$x$', ylabel='$y=\\ln x$')
save(fig, 'M16-n2')

import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

f = lambda x: x**2/(x-1)
assert np.isclose(f(-2), -4/3) and np.isclose(f(3), 4.5) and np.isclose(f(.5), -.5)

fig, ax = new_fig(12, 7.5)
for lo, hi in [(-4, .995), (1.005, 5)]:
    x = np.linspace(lo, hi, 850)
    ax.plot(x, f(x), color=C.INK, ls='-', lw=1.7)
ax.axvline(1, color=C.GRAY, ls='--', lw=1.1)
xas = np.linspace(-4, 5, 400)
ax.plot(xas, xas+1, color=C.GRAY, ls='--', lw=1.1)
ax.scatter([0], [0], s=38, facecolors=C.PAPER, edgecolors=C.INK, zorder=5)
ax.scatter([2], [4], s=30, color=C.INK, zorder=5)
label(ax, '极大', (0, 0), offset=(-8, -16), ha='right', va='top')
label(ax, '极小', (2, 4), offset=(7, 5), ha='left', va='bottom')
label(ax, '凹（帽形）', (-2.6, -5.2), ha='center', va='center')
label(ax, '凸（碗形）', (3.5, 8.0), ha='center', va='center')
label(ax, '$x=1$', (1, 9.0), offset=(-6, 0), ha='right', va='bottom')
label(ax, '$y=x+1$', (3.3, 3.3), offset=(3, 0), ha='left', va='top')
ax.set(xlim=(-4, 5), ylim=(-8, 10), xlabel='$x$', ylabel='$y$')
save(fig, 'C8-n3')

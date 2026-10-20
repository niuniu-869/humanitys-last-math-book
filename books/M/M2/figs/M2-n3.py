import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))

fig, ax = new_fig(12, 7.5)
x = np.arange(1, 6, dtype=float)
y = np.array([0, 0, 1, 0, 1], dtype=float)
xx = np.linspace(0.7, 5.3, 500)
pp = sigmoid(1.0904 * xx - 3.894)
ax.plot(xx, pp, color=C.INK, ls='-', label=r'$p=\sigma(1.0904x-3.894)$')
ax.axhline(0.5, color=C.GRAY, ls='--', lw=1.0)
xb = 3.894 / 1.0904
ax.axvline(xb, color=C.GRAY, ls=':', lw=1.0)
ax.scatter(x, y, s=34, color=C.INK, zorder=5)
p3 = sigmoid(1.0904 * 3 - 3.894)
ax.scatter([3], [p3], s=42, facecolors=C.PAPER, edgecolors=C.INK, linewidths=1.2, zorder=6)
label(ax, '分界点 3.571', (xb, 0.5), offset=(5, 8), fontsize=8.5)
label(ax, '$p\\approx0.349$', (3, p3), offset=(7, -14), fontsize=8.5)
label(ax, '判错', (3, 1), offset=(7, 5), color=C.GRAY, fontsize=8.5)
label(ax, '判错', (4, 0), offset=(7, 5), color=C.GRAY, fontsize=8.5)
ax.set(xlim=(0.7, 5.3), ylim=(-0.1, 1.1), xlabel='$x$', ylabel='$p$')
save(fig, 'M2-n3')

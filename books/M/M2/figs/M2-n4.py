import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))

fig, ax = new_fig(12, 7.5)
z = np.linspace(-8, 4, 600)
s = sigmoid(z)
g_ce = s - 1
g_sq = 2 * (s - 1) * s * (1 - s)
ax.plot(z, g_ce, color=C.INK, ls='-', label='交叉熵')
ax.plot(z, g_sq, color=C.GRAY, ls='--', label='sigmoid + 平方误差')
z0 = -5
v_ce = sigmoid(z0) - 1
v_sq = 2 * (sigmoid(z0) - 1) * sigmoid(z0) * (1 - sigmoid(z0))
ax.scatter([z0], [v_ce], s=30, color=C.INK, zorder=5)
ax.scatter([z0], [v_sq], s=36, facecolors=C.PAPER, edgecolors=C.GRAY, linewidths=1.1, zorder=5)
label(ax, '$-0.9933$', (z0, v_ce), offset=(6, 7), fontsize=8.5)
label(ax, '$-0.0132$', (z0, v_sq), offset=(6, -14), color=C.GRAY, fontsize=8.5)
label(ax, '交叉熵', (2.2, -0.89), offset=(0, 0), fontsize=8.5)
label(ax, '平方误差', (1.2, -0.04), offset=(0, 0), color=C.GRAY, fontsize=8.5)
ax.axhline(0, color=C.LIGHT, lw=0.8)
ax.set(xlim=(-8, 4), ylim=(-1.08, 0.12), xlabel='$z$', ylabel=r'$\partial\ell/\partial z$')
save(fig, 'M2-n4')

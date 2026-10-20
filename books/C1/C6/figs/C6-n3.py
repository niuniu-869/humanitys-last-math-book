import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, axes = new_fig(17, 6.2, ncols=2)

x = np.linspace(1, 4, 400)
f = np.sqrt(x)
chord = 1 + (x - 1) / 3
xi = 9 / 4
yi = np.sqrt(xi)
yc = 1 + (xi - 1) / 3

# 曲线与弦。
ax = axes[0]
ax.plot(x, f, color=C.INK, ls='-')
ax.plot(x, chord, color=C.GRAY, ls='--')
ax.scatter([1, 4], [1, 2], s=28, color=C.INK, zorder=5)
ax.scatter([xi], [yi], s=34, facecolors=C.INK, edgecolors=C.INK, zorder=5)
ax.plot([xi, xi], [yc, yi], color=C.LIGHT, ls='-', lw=5, solid_capstyle='butt', zorder=2)
ax.plot([1.45, 3.05], [yi - (xi - 1.45) / 3, yi + (3.05 - xi) / 3], color=C.GRAY, ls=':', lw=1.2)
label(ax, '$A$', (1, 1), offset=(6, -2), ha='left')
label(ax, '$B$', (4, 2), offset=(7, 1), ha='left')
ax.set(xlim=(0.8, 4.25), ylim=(0.8, 2.25), xlabel='$x$', ylabel='$f(x)$', aspect='equal')

# 减去弦后的函数。
ax = axes[1]
phi = f - chord
ax.plot(x, phi, color=C.INK, ls='-')
ax.plot([1, 4], [0, 0], color=C.GRAY, ls='--', lw=1.1)
ax.scatter([1, 4], [0, 0], s=28, color=C.INK, zorder=5)
ax.scatter([xi], [yi - yc], s=34, facecolors=C.INK, edgecolors=C.INK, zorder=5)
ax.plot([1.6, 3.0], [yi - yc, yi - yc], color=C.GRAY, ls='--', lw=1.1)
label(ax, '$\\varphi(x)=\\sqrt{x}-1-\\frac{1}{3}(x-1)$', (2.5, 0.022), offset=(0, 0), ha='center', fontsize=8.5)
label(ax, '$\\varphi\\\'(\\xi)=0$', (xi, yi - yc), offset=(12, 16), ha='left')
ax.set(xlim=(0.8, 4.25), ylim=(-0.025, 0.13), xlabel='$x$', ylabel='$\\varphi(x)$', aspect='auto')

axes[0].set_xlabel('$x$\n虚线：弦，斜率 $\\frac{1}{3}$；点线：$\\xi=\\frac{9}{4}$ 处的切线，与弦平行；\n$\\xi$ 处是曲线高出弦最多的点',fontsize=9)
fig.tight_layout(w_pad=2.0)
save(fig, 'C6-n3')

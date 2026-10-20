import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(12, 7.5)
x = np.linspace(-2.2, 2.2, 500)
ax.plot(x, x**2, color=C.INK, ls='-', label=r'$L(\theta)=\theta^2$')
ax.set(xlim=(-2.25, 2.25), ylim=(-0.15, 4.8), xlabel=r'$\theta$', ylabel='$L$')
ax.axhline(0, color=C.LIGHT, lw=0.8)
configs = [(0.25, 'o', C.INK, '-', '0.5', 7), (0.75, 'o', C.GRAY, '--', '-0.5', 7), (1.1, 's', C.INK, ':', '-1.2', 4)]
for eta, marker, color, ls, fac, n in configs:
    pts = [1.0]
    for _ in range(n): pts.append((1 - 2*eta) * pts[-1])
    ys = np.array(pts)**2
    ax.plot(pts, ys, color=color, ls=ls, lw=1.2, zorder=3)
    ax.scatter(pts, ys, marker=marker, s=30, facecolors=(C.PAPER if color == C.GRAY else color), edgecolors=color, linewidths=1.2, zorder=5)
    if eta == 0.25:
        label(ax, fr'$\eta={eta}$', (1.45, 0.62), offset=(0, 0), color=color)
        label(ax, fr'$1-\eta\lambda={fac}$', (1.45, 0.4), offset=(0, 0), color=color)
    elif eta == 0.75:
        label(ax, fr'$\eta={eta}$', (-1.95, 0.95), offset=(0, 0), color=color)
        label(ax, fr'$1-\eta\lambda={fac}$', (-2.05, 0.7), offset=(0, 0), color=color)
    else:
        label(ax, fr'$\eta={eta}$', (pts[-1], ys[-1]), offset=(-55, 4), color=color)
        label(ax, fr'$1-\eta\lambda={fac}$', (pts[2], ys[2]), offset=(8, 4), color=color)
label(ax, r'$\theta_0=1$', (1, 1), offset=(10, 6))
save(fig, 'M1-n1')

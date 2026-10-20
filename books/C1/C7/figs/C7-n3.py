import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

x = np.linspace(-2 * np.pi, 2 * np.pi, 1200)
p1 = x
p3 = x - x**3 / 6
p5 = x - x**3 / 6 + x**5 / 120
assert abs((np.pi - np.pi**3 / 6) + 2.026) < 0.002
assert abs((np.pi - np.pi**3 / 6 + np.pi**5 / 120) - 0.524) < 0.002

fig, ax = new_fig(14, 8)
ax.plot(x, np.sin(x), color=C.INK, ls='-', lw=2.2)
ax.plot(x, p1, color=C.GRAY, ls=':', lw=1.6)
ax.plot(x, p3, color=C.TEAL, ls='--', lw=1.6)
ax.plot(x, p5, color=C.RED, ls='-.', lw=1.6)
label(ax, '一次', (-2.1, -2.1), offset=(4, 5))
label(ax, '三次', (3.1, -2.0), offset=(5, 5))
label(ax, '五次', (3.0, 0.66), offset=(5, 4))
label(ax, '$\\sin x$', (4.55, -0.98), offset=(5, 0))
ax.set(xlabel='$x$', ylabel='$y$', xlim=(-2 * np.pi, 2 * np.pi), ylim=(-2.5, 2.5))
ax.set_xticks([-2*np.pi, -np.pi, 0, np.pi, 2*np.pi], [r'$-2\pi$', r'$-\pi$', '0', r'$\pi$', r'$2\pi$'])
save(fig, 'C7-n3')

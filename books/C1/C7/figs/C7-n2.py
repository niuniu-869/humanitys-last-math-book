import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

x = np.linspace(-2, 2, 600)
curves = {
    'P_1': 1 + x,
    'P_2': 1 + x + x**2 / 2,
    'P_3': 1 + x + x**2 / 2 + x**3 / 6,
    'e^x': np.exp(x),
}
assert abs((1 + 0.1 + 0.1**2 / 2 + 0.1**3 / 6) - 1.105167) < 1e-6
assert abs(curves['P_1'][-1] - 3) < 1e-12
assert abs(curves['P_2'][-1] - 5) < 1e-12
assert abs(curves['P_3'][-1] - 6.3333333333) < 1e-6
assert abs(curves['e^x'][-1] - 7.389056) < 1e-5

fig, ax = new_fig(14, 8)
ax.plot(x, curves['e^x'], color=C.INK, ls='-', lw=2.2)
ax.plot(x, curves['P_1'], color=C.GRAY, ls=':', lw=1.6)
ax.plot(x, curves['P_2'], color=C.TEAL, ls='--', lw=1.6)
ax.plot(x, curves['P_3'], color=C.RED, ls='-.', lw=1.6)
dot(ax, (0, 1), color=C.INK)
label(ax, '$e^x$', (1.56, np.exp(1.56)), offset=(-30, 12))
label(ax, '$P_1$', (1.56, 2.4), offset=(5, -4))
label(ax, '$P_2$', (1.56, 3.55), offset=(5, 0))
label(ax, '$P_3$', (1.56, 5.5), offset=(5, 0))
ax.set(xlabel='$x$', ylabel='$y$', xlim=(-2, 2), ylim=(-1, 7))
save(fig, 'C7-n2')

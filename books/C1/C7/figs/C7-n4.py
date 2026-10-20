import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

x = np.linspace(-0.8, 0.8, 800)
diff = np.tan(x) - np.sin(x)
approx = x**3 / 2
assert abs((np.tan(0.1) - np.sin(0.1)) - 5.0126e-4) < 2e-7
assert abs(0.1**3 / 2 - 5e-4) < 1e-12

fig, ax = new_fig(14, 7)
ax.plot(x, diff, color=C.INK, ls='-', lw=2.0)
ax.plot(x, approx, color=C.GRAY, ls='--', lw=1.6)
ax.axhline(0, color=C.TEAL, ls=':', lw=1.6)
label(ax, '$\\tan x-\\sin x$', (0.52, np.tan(0.52)-np.sin(0.52)), offset=(5, 3))
label(ax, '$x^3/2$', (0.38, 0.38**3 / 2), offset=(5, 3))
label(ax, '替换后：0', (-0.02, 0), offset=(5, 8))
ax.set(xlabel='$x$', ylabel='$y$', xlim=(-0.8, 0.8), ylim=(-0.27, 0.27))
save(fig, 'C7-n4')

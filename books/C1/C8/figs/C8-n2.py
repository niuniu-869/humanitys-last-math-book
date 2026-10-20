import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

ell = lambda z: np.logaddexp(0, -z)
assert np.isclose(ell(0), np.log(2))
assert np.isclose(ell(-3), 3.048587, atol=1e-5)
assert np.isclose(ell(3), 0.048587, atol=1e-5)

fig, ax = new_fig(12, 7.5)
z = np.linspace(-5, 5, 900)
ax.plot(z, ell(z), color=C.INK, ls='-', lw=1.8)
ax.axhline(0, color=C.GRAY, ls=':', lw=1.1)
ax.plot(z, -z, color=C.GRAY, ls='--', lw=1.1)
z0, y0, m = 0, np.log(2), -.5
ax.scatter([z0], [y0], s=28, color=C.INK, zorder=5)
half = 1.0
ax.plot([-half, half], [y0-m*half, y0+m*half], color=C.GRAY, ls='-.', lw=1.1)
label(ax, r'$\ell=0$', (4.0, .0), offset=(0, 7), ha='center', va='bottom')
label(ax, r'$\ell=-z$', (-2.9, 4.0), offset=(2, 2), ha='left', va='bottom')
label(ax, r'$\ell(z)=\ln(1+e^{-z})$', (1.35, 1.05), offset=(4, 4), ha='left', va='bottom')
label(ax, r'切线斜率 $-\frac{1}{2}$', (.75, .28), offset=(3, 2), ha='left', va='bottom')
ax.set(xlim=(-5, 5), ylim=(-.5, 5.5), xlabel='$z$', ylabel=r'$\ell$')
save(fig, 'C8-n2')

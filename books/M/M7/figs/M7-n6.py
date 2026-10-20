import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(12.5, 7.5)
eps = np.logspace(-12, 0, 241)
x = 1.0; truth = np.e
forward = np.abs((np.exp(x+eps)-np.exp(x))/eps-truth)/truth
center = np.abs((np.exp(x+eps)-np.exp(x-eps))/(2*eps)-truth)/truth
ax.loglog(eps, forward, ls='--', color=C.INK, lw=1.6, label='前向差分')
ax.loglog(eps, center, ls='-', color=C.INK, lw=1.6, label='中心差分')
r1 = np.logspace(-6,-2,50); r2 = np.logspace(-4,-1,50)
ax.loglog(r1, 3*r1, ls=':', color=C.GRAY, lw=1.1)
ax.loglog(r2, .015*r2**2, ls=':', color=C.GRAY, lw=1.1)
ax.axvline(1e-5, ls=':', color=C.GRAY, lw=1.0)
label(ax, r'$\propto\varepsilon$', (1e-3, 3e-3), offset=(-8,12), fontsize=9)
label(ax, r'$\propto\varepsilon^2$', (1e-2, 1.5e-6), offset=(8,-15), fontsize=9)
label(ax, '常取 $10^{-5}$', (1e-5, 0.2), offset=(5,0), fontsize=8)
ax.set_xlim(1e-12, 1); ax.set_ylim(1e-13, 2)
ax.set_xlabel(r'$\varepsilon$'); ax.set_ylabel('相对误差')
ax.legend(loc='upper left', fontsize=9)
ax.grid(True, which='major', color=C.LIGHT, lw=0.6)
save(fig, "M7-n6")

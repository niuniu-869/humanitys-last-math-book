import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, axes = new_fig(14, 6, ncols=2)
lam = 0.4
for ax in axes:
    ax.set_xlabel('$x$'); ax.set_ylabel('$f(x)$')
x = np.linspace(-2.2, 2.2, 500)
f = x**2; axes[0].plot(x, f, color=C.INK)
a, b = -1.4, 1.3; fa, fb = a*a, b*b
axes[0].plot([a,b], [fa,fb], color=C.GRAY, ls='--')
u = lam*a + (1-lam)*b; chord = lam*fa + (1-lam)*fb
axes[0].plot([u,u], [u*u,chord], color=C.GRAY, ls=':')
label(axes[0], r'$f(\alpha x+(1-\alpha)y)$', (u,u*u), offset=(8,-2))
label(axes[0], '弦', ((a+b)/2, (fa+fb)/2), offset=(3,8), color=C.GRAY)
axes[0].set(xlim=(-2.2,2.2), ylim=(-.2,4.8))
g = x**4 - 2*x**2 + 0.5*x; axes[1].plot(x,g,color=C.INK)
a, b = -1.25, 1.15; ga = a**4-2*a*a+0.5*a; gb = b**4-2*b*b+0.5*b
axes[1].plot([a,b],[ga,gb],color=C.GRAY,ls='--')
axes[1].scatter([-0.98, 0.93], [(-0.98)**4-2*(-0.98)**2+0.5*(-0.98), 0.93**4-2*0.93**2+0.5*0.93], s=35, color=C.INK)
label(axes[1], '全局最小', (-0.98, -1.25), offset=(-4,8))
label(axes[1], '局部最小', (0.93, -0.8), offset=(6,6))
label(axes[1], '弦低于曲线', (-0.1, -0.2), offset=(0,8), color=C.GRAY)
axes[1].set(xlim=(-2.2,2.2), ylim=(-1.6,5.0))
fig.subplots_adjust(wspace=0.3)
save(fig, 'M1-n3')

import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

lo, hi = 0.3, 0.8
assert np.isclose((2*lo+2*hi)*(hi-lo)/2, 0.55)
assert np.isclose(hi**2-lo**2, 0.55)
fig, (a, b) = new_fig(18, 8, ncols=2)
x = np.linspace(0, 1, 301)
a.plot(x, 2*x, color=C.INK, lw=2, ls='-')
u = np.linspace(lo, hi, 151)
a.fill_between(u, 0, 2*u, color=C.LIGHT)
a.vlines([lo, hi], 0, [2*lo, 2*hi], color=C.GRAY, lw=0.9, ls='-')
label(a, r'面积 $0.55$', (0.56, 0.40), ha='center')
a.set(title=r'概率密度 $f(x)=2x$', xlim=(0, 1.1), ylim=(0, 2.2), xlabel=r'$x$', ylabel=r'$y$')
a.set_xticks([0, lo, hi, 1])
b.plot(x, x*x, color=C.INK, lw=2, ls='-')
b.plot([1, 1.1], [1, 1], color=C.INK, lw=2, ls='-')
for p in [lo, hi]:
    b.vlines(p, 0, p*p, color=C.GRAY, ls=':', lw=1.2)
    b.hlines(p*p, 0, p, color=C.GRAY, ls='--', lw=1.2)
    dot(b, (p, p*p), size=20)
b.annotate('', xy=(0.19, hi**2), xytext=(0.19, lo**2),
           arrowprops=dict(arrowstyle='<->', color=C.INK, lw=1, shrinkA=0, shrinkB=0))
label(b, '$0.55$', (0.19, (hi**2+lo**2)/2), offset=(6, 0), va='center')
b.set(title=r'分布函数 $F$', xlim=(0, 1.1), ylim=(0, 1.1), xlabel=r'$x$', ylabel=r'$y$')
b.set_xticks([0, lo, hi, 1])
b.set_yticks([0, lo**2, hi**2, 1], ['0', '0.09', '0.64', '1'])
fig.subplots_adjust(left=0.07, right=0.98, bottom=0.18, top=0.87, wspace=0.35)
save(fig, "C10-n3")

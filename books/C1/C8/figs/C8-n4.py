import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

g = lambda x: np.exp(x)/x
assert np.isclose(g(1), np.e)

def bisect(fun, a, b, n=70):
    fa, fb = fun(a), fun(b)
    assert fa * fb <= 0
    for _ in range(n):
        c = (a+b)/2
        if fa * fun(c) <= 0:
            b, fb = c, fun(c)
        else:
            a, fa = c, fun(c)
    return (a+b)/2

x5a = bisect(lambda x: g(x)-5, .01, 1)
x5b = bisect(lambda x: g(x)-5, 1, 3)
xm2 = bisect(lambda x: g(x)+2, -1, -.01)
assert np.isclose(x5a, .259171, atol=1e-5) and np.isclose(x5b, 2.542641, atol=1e-5)
assert np.isclose(xm2, -.351734, atol=1e-5)

fig, ax = new_fig(12, 7.5)
for lo, hi in [(-4, -.025), (.025, 3)]:
    x = np.linspace(lo, hi, 900)
    ax.plot(x, g(x), color=C.INK, ls='-', lw=1.7)
ax.axhline(np.e, color=C.GRAY, ls='--', lw=1.1)
ax.axhline(5, color=C.GRAY, ls=':', lw=1.1)
ax.axhline(-2, color=C.GRAY, ls=':', lw=1.1)
pts = [(1, np.e), (x5a, 5), (x5b, 5), (xm2, -2)]
ax.scatter([p[0] for p in pts[1:]], [p[1] for p in pts[1:]], s=25, color=C.INK, zorder=5)
ax.scatter([1], [np.e], s=38, facecolors=C.PAPER, edgecolors=C.INK, zorder=5)
label(ax, '$k=e$：1 个根', (-3.9, 2.9), offset=(0, 2), ha='left', va='bottom')
label(ax, '$k>e$：2 个根', (-3.9, 5.3), offset=(0, 2), ha='left', va='bottom')
label(ax, '$k<0$：1 个根', (-3.9, -1.7), offset=(0, 2), ha='left', va='bottom')
ax.set(xlim=(-4, 3), ylim=(-6, 12), xlabel='$x$', ylabel='$y$')
save(fig, 'C8-n4')

import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import ConnectionPatch

f = lambda x: (x-1)*(x-2)
phi = lambda x: x**3/3 - 3*x*x/2 + 2*x
assert np.allclose([phi(1), phi(2), phi(2)-phi(1)], [5/6, 2/3, -1/6])
fig, (a, b) = new_fig(14, 13, nrows=2, sharex=True)
x = np.linspace(-0.3, 2.8, 501)
a.plot(x, f(x), color=C.INK, lw=2, ls='-')
u = np.linspace(0, 1, 151)
v = np.linspace(1, 2, 151)
a.fill_between(u, 0, f(u), color=C.LIGHT)
a.fill_between(v, f(v), 0, facecolor=C.PAPER, edgecolor=C.GRAY, hatch='////', lw=0.5)
label(a, r'$+\frac{5}{6}$', (0.32, 0.48), ha='center')
label(a, r'$-\frac{1}{6}$', (1.5, -0.58), ha='center', va='center')
for p in [1, 2]:
    dot(a, (p, 0), size=17)
    label(a, str(p), (p, 0), offset=(7, 7))
a.set(ylim=(-0.85, 3.2), ylabel=r'$y$')
a.set_title(r'$f(t)=(t-1)(t-2)$', loc='left', pad=10)
b.plot(x, phi(x), color=C.INK, lw=2, ls='-')
for p in [1, 2]:
    dot(b, (p, phi(p)), size=27)
label(b, r'极大 $\frac{5}{6}$', (1, phi(1)), offset=(-12, 17), ha='right')
label(b, r'极小 $\frac{2}{3}$', (2, phi(2)), offset=(12, -24))
b.scatter([0], [0], s=30, facecolors=C.INK, edgecolors=C.INK, zorder=5)
b.set(xlim=(-0.3, 2.8), ylim=(-0.85, 1.35), xlabel=r'$x$', ylabel=r'$y$')
b.set_title(r'$\Phi(x)=\int_0^x f$', loc='left', pad=10)
b.set_xticks([0, 1, 2, 2.8])
for ax in [a, b]:
    ax.axhline(0, color=C.GRAY, lw=0.8, ls='-')
    ax.axvline(0, color=C.GRAY, lw=0.8, ls='-')
    for p in [1, 2]:
        ax.axvline(p, color=C.GRAY, lw=1, ls=':', zorder=0)
for p in [1, 2]:
    fig.add_artist(ConnectionPatch((p, 0), (p, 1), coordsA=a.get_xaxis_transform(),
                                  coordsB=b.get_xaxis_transform(), color=C.GRAY,
                                  lw=1, ls=':', zorder=0, clip_on=False))
fig.subplots_adjust(left=0.12, right=0.97, bottom=0.10, top=0.93, hspace=0.40)
save(fig, "C10-n4")

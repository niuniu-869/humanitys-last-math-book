import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(16, 10)
x = np.linspace(-1.5, 2, 401)
F = lambda x: x**3 / 3
p, slope = 1.5, 1.5**2
assert np.isclose(slope, 2.25)
for c, ls, name in [(0, '-', '$F$'), (1, '--', '$F+1$'), (-1, ':', '$F-1$')]:
    ax.plot(x, F(x)+c, color=C.INK, lw=2, ls=ls)
    s = np.linspace(1.25, 1.75, 31)
    ax.plot(s, F(p)+c+slope*(s-p), color=C.RED, lw=0.9, ls='-')
    dot(ax, (p, F(p)+c), size=16)
    label(ax, name, (1.98, F(1.98)+c), offset=(0, 2), ha='right', va='bottom', fontsize=9)
ax.annotate('', xy=(-1, F(-1)+1), xytext=(-1, F(-1)),
            arrowprops=dict(arrowstyle='<->', color=C.INK, lw=1, shrinkA=0, shrinkB=0))
label(ax, r'差 $1$', (-1, F(-1)+0.5), offset=(10, 6), va='center')
label(ax, r'斜率都是 $x^2=2.25$', (0.15, 4.65))
ax.axhline(0, color=C.GRAY, lw=0.7, ls='-')
ax.axvline(0, color=C.GRAY, lw=0.7, ls='-')
ax.set(xlim=(-1.5, 2), ylim=(-2.5, 5.5), xlabel=r'$x$', ylabel=r'$y$')
ax.set_xticks([-1.5, -1, 0, 1, 1.5, 2])
fig.subplots_adjust(left=0.13, right=0.97, bottom=0.14, top=0.97)
save(fig, "C10-n2")

import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

n = np.arange(1, 11)
s = np.cumsum((-1.0)**(n-1)/n)
assert np.all(np.diff(s[::2]) < 0) and np.all(np.diff(s[1::2]) > 0)
assert np.isclose(s[2]-s[3], 1/4)
fig, ax = new_fig(15, 8.5)
ax.set(xlim=(.6, 11.5), ylim=(.46, 1.08), xticks=n,
       xlabel='$n$', ylabel='$S_n$')
ax.plot(n, s, color=C.INK, lw=.9, ls='-')
ax.scatter(n[::2], s[::2], color=C.INK, s=28, zorder=5, label='奇数项部分和')
ax.scatter(n[1::2], s[1::2], facecolors=C.PAPER, edgecolors=C.INK,
           s=30, zorder=5, label='偶数项部分和')
ax.axhline(np.log(2), color=C.GRAY, ls='--', lw=1.2)
label(ax, '和 $S$', (10.6, np.log(2)), (0, 7), ha='center')
ax.plot([3, 3.48], [s[2], s[2]], color=C.GRAY, ls=':', lw=.8)
ax.plot([3.48, 4], [s[3], s[3]], color=C.GRAY, ls=':', lw=.8)
ax.annotate('', xy=(3.48, s[2]), xytext=(3.48, s[3]),
            arrowprops=dict(arrowstyle='|-|', color=C.INK, lw=1, shrinkA=0, shrinkB=0))
label(ax, r'$u_4=\frac{1}{4}$', (3.48, .89), ha='center', fontsize=10)
ax.legend(loc='upper right', fontsize=9)
save(fig, 'C14-n4')

import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(13, 13)
fig.subplots_adjust(left=0.10, right=0.96, bottom=0.09, top=0.96)
theta = np.linspace(0, 2*np.pi, 600)
ax.plot(5*np.cos(theta), 5*np.sin(theta), color=C.INK, ls='-')
ax.plot([0, 3], [0, 4], color=C.RED, ls='--')
x = np.linspace(-1, 7, 200)
ax.plot(x, (25-3*x)/4, color=C.INK, ls='-')
ax.axhline(0, color=C.GRAY, lw=0.7)
ax.axvline(0, color=C.GRAY, lw=0.7)
dot(ax, (0, 0), '$O$', offset=(-14, -15))
dot(ax, (3, 4), '$(3,4)$', offset=(9, 12))
label(ax, r'斜率 $\frac{4}{3}$', (1.35, 3.3), ha='center')
label(ax, r'斜率 $-\frac{3}{4}$', (4.4, 2.95), (0, 17))
label(ax, r'$x^2+y^2=25$', (-4.8, 4.9), fontsize=10)
p = np.array([3., 4.]); u = np.array([-3., -4.])/5; v = np.array([4., -3.])/5
corner = np.array([p+0.38*u, p+0.38*(u+v), p+0.38*v])
ax.plot(corner[:, 0], corner[:, 1], color=C.INK, lw=0.9)
assert np.dot(u, v) == 0 and 3*p[0]+4*p[1] == 25
ax.set(xlim=(-6, 6), ylim=(-6, 6), xlabel='$x$', ylabel='$y$')
ax.set_xticks([-5, 0, 5]); ax.set_yticks([-5, 0, 5]); ax.set_aspect('equal')
save(fig, "C5-n3")

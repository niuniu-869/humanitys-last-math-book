import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

from matplotlib.patches import Rectangle

fig, ax = new_fig(17, 9)
edges = np.array([0, 0.9, 2.0, 2.8, 4.1, 5.0])
xi = np.array([0.5, 1.3, 2.5, 3.1, 4.6])
f = lambda x: 1 + 0.5*np.sin(1.6*x)
assert np.all((edges[:-1] < xi) & (xi < edges[1:]))
assert np.all(~np.isclose(xi, (edges[:-1]+edges[1:])/2))
for left, width, t in zip(edges[:-1], np.diff(edges), xi):
    ax.add_patch(Rectangle((left, 0), width, f(t), facecolor=C.LIGHT,
                           edgecolor=C.INK, lw=0.9, ls='-'))
    ax.plot([t, t], [0, f(t)], color=C.INK, lw=0.9, ls=':')
ax.scatter(xi, f(xi), s=32, facecolors=C.PAPER, edgecolors=C.INK, zorder=5)
x = np.linspace(0, 5, 501)
ax.plot(x, f(x), color=C.INK, lw=2, ls='-')
ax.set(xlim=(0, 5.3), ylim=(0, 1.85), xlabel='$x$', ylabel='$y$')
ax.xaxis.set_label_coords(1.01, -0.055)
ax.set_xticks(edges, ['$a=x_0$', '$x_1$', '$x_2$', '$x_3$', '$x_4$', '$b=x_5$'])
ax.set_yticks([0, 0.5, 1, 1.5])
label(ax, r'$\xi_3$', (xi[2], 0), offset=(0, -17), ha='center')
ax.annotate('', xy=(2.8, -0.30), xytext=(2, -0.30), annotation_clip=False,
            arrowprops=dict(arrowstyle='<->', color=C.INK, lw=0.9))
label(ax, r'$\Delta x_3$', (2.4, -0.30), offset=(0, -8), ha='center', va='top', annotation_clip=False)
ax.annotate('', xy=(2.12, f(xi[2])), xytext=(2.12, 0),
            arrowprops=dict(arrowstyle='<->', color=C.INK, lw=0.9))
label(ax, r'$f(\xi_3)$', (2.12, f(xi[2])/2), offset=(5, 0), va='center')
label(ax, '$y=f(x)$', (3.55, 1.58))
fig.subplots_adjust(left=0.09, right=0.96, bottom=0.28, top=0.94)
save(fig, "C9-n3")

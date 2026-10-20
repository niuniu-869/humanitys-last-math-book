import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

from matplotlib.patches import Rectangle

fig, axes = new_fig(18, 8.5, ncols=2)
edges = np.linspace(0, 1, 5)
x = np.linspace(0, 1, 401)
for ax, heights, title, expected in zip(
    axes, [edges[1:]**2, edges[:-1]**2],
    ["右端点：和 0.46875，偏大", "左端点：和 0.21875，偏小"],
    [0.46875, 0.21875],
):
    assert np.isclose(np.sum(heights) / 4, expected)
    for left, h in zip(edges[:-1], heights):
        ax.add_patch(Rectangle((left, 0), 0.25, h, facecolor=C.LIGHT,
                               edgecolor=C.INK, lw=0.9, ls='-'))
    for e in edges[1:-1]:
        ax.plot([e, e], [0, e**2], color=C.INK, lw=0.8, ls=':')
    ax.plot([1, 1], [0, 1.08], color=C.INK, lw=0.8, ls='--')
    ax.plot(x, x**2, color=C.INK, lw=2.2, ls='-')
    ax.set(xlim=(0, 1.1), ylim=(0, 1.1), xlabel='$x$', ylabel='$y$')
    ax.set_aspect('equal')
    ax.set_xticks(edges, ['$0$', r'$\frac{1}{4}$', r'$\frac{1}{2}$', r'$\frac{3}{4}$', '$1$'])
    ax.set_yticks([0, 0.5, 1])
    ax.set_title(title, pad=12)
    label(ax, '$y=x^2$', (0.18, 0.8))
fig.subplots_adjust(left=0.07, right=0.99, bottom=0.18, top=0.86, wspace=0.26)
save(fig, "C9-n1")

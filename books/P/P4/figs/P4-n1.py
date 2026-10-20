import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, axes = new_fig(18, 6.7, ncols=3, sharex=True, sharey=True)
fig.subplots_adjust(left=0.08, right=0.98, bottom=0.19, top=0.84, wspace=0.18)
x = np.linspace(0, 3, 601)
for ax, width in zip(axes, [1, 0.5, 0.125]):
    edges = np.linspace(0, 3, round(3 / width) + 1)
    heights = np.diff(edges ** 3) / (27 * width)
    assert np.isclose(np.sum(heights * width), 1)
    ax.bar(edges[:-1], heights, width=width, align='edge',
           color=C.LIGHT, edgecolor=C.INK, linewidth=0.65)
    ax.plot(x, x ** 2 / 9, color=C.INK, ls='-', lw=1.8)
    ax.set(xlim=(0, 3), ylim=(0, 1.1), xticks=[0, 1, 2, 3],
           yticks=[0, 0.5, 1], xlabel='$x$', title=f'宽度 {width:g}')
axes[0].set_ylabel('$f(x)$')
label(axes[0], r'面积 $=\frac{7}{27}$', (1.5, 0.12), ha='center', va='center')
save(fig, "P4-n1")

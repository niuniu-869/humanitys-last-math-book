import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle

fig, ax = new_fig(16, 9)
ax.set(xlim=(-0.10, 1.15), ylim=(-1.2, 5.4))
ax.axis('off')
ends = 1 - 2.0 ** (-np.arange(1, 5))
assert np.allclose(ends, [1/2, 3/4, 7/8, 15/16])
for n, end in enumerate(ends, 1):
    y = 5.1 - n
    left = 0
    for j in range(1, n + 1):
        width = 2.0 ** -j
        ax.add_patch(Rectangle((left, y), width, .65,
                              facecolor=C.LIGHT, edgecolor=C.INK, lw=1, ls='-'))
        label(ax, rf'$\frac{{1}}{{{2**j}}}$', (left + width/2, y+.325),
              ha='center', va='center', fontsize=10)
        left += width
    ax.add_patch(Rectangle((end, y), 1-end, .65, fill=False,
                          edgecolor=C.INK, lw=1, ls='--'))
    label(ax, rf'$S_{n}$', (-.04, y+.325), ha='right', va='center')
arrow(ax, (0, 0), (1.1, 0), color=C.INK, lw=1)
for x, text in [(0, '$0$'), (.5, r'$\frac{1}{2}$'), (.75, r'$\frac{3}{4}$'),
                (.875, r'$\frac{7}{8}$'), (1, '$1$')]:
    ax.plot([x, x], [-.055, .055], color=C.INK, lw=.8)
    label(ax, text, (x, 0), (0, -13), ha='center', va='top')
for i, x in enumerate(ends, 1):
    dot(ax, (x, 0), size=22)
    label(ax, rf'$S_{i}$', (x, 0), (0, 10),
          ha='center', va='bottom', fontsize=9)
ax.scatter([1], [0], s=36, facecolors=C.PAPER, edgecolors=C.INK, zorder=7)
label(ax, '极限 1', (1, -1.0), ha='center', fontsize=10)
save(fig, 'C14-n1')

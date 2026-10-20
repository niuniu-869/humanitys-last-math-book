import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

from matplotlib.patches import Circle

levels = [[(0, 3.5)], [(-1, 2.5), (1, 2.5)], [(-1.5, 1.5), (-.5, 1.5), (.5, 1.5), (1.5, 1.5)],
          [(-1.75, .5), (-1.25, .5), (-.75, .5), (-.25, .5), (.25, .5), (.75, .5), (1.25, .5), (1.75, .5)]]
assert list(map(len, levels)) == [1, 2, 4, 8]
fig, ax = new_fig(15, 8.5)
for d in range(3):
    for i, (x, y) in enumerate(levels[d]):
        for child in levels[d + 1][2*i:2*i+2]:
            ax.plot([x, child[0]], [y, child[1]], color=C.INK, lw=1.2, zorder=1)
leaf_filled = {1, 4, 6}
for d, nodes in enumerate(levels):
    for i, (x, y) in enumerate(nodes):
        if d < 3:
            face = C.INK
        else:
            face = C.INK if i in leaf_filled else C.PAPER
        ax.add_patch(Circle((x, y), .13, facecolor=face, edgecolor=C.INK, lw=1.2, zorder=3))
for d, text in enumerate(['第 0 层 $\\leq 1$', '第 1 层 $\\leq 2$', '第 2 层 $\\leq 4$', '第 3 层 $\\leq 8$']):
    label(ax, text, (2.55, levels[d][0][1]), ha='left', va='center', fontsize=9)
label(ax, '已放叶子', (-1.25, .5), offset=(0, -18), ha='center', fontsize=9)
label(ax, '空位', (-.25, .5), offset=(0, -18), ha='center', fontsize=9)
ax.set(xlim=(-2.2, 4.8), ylim=(-.45, 4.0), aspect='equal')
ax.axis('off')
save(fig, 'K22-n5')

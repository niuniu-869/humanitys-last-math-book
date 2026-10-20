import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

from matplotlib.patches import Circle, FancyArrowPatch

pos = {'N': (2.4, 3.4), 'S': (2.4, .7), 'K': (0.8, 2.0), 'E': (4.4, 2.0)}
edges = [('N', 'K', -.20), ('N', 'K', .20), ('S', 'K', .20), ('S', 'K', -.20),
         ('N', 'E', 0), ('S', 'E', 0), ('K', 'E', 0)]
assert len(edges) == 7
degree = {'K': 5, 'N': 3, 'S': 3, 'E': 3}
fig, ax = new_fig(12, 8)
for a, b, rad in edges:
    ax.add_patch(FancyArrowPatch(pos[a], pos[b], connectionstyle=f'arc3,rad={rad}', arrowstyle='-',
                                 color=C.INK, lw=1.8, shrinkA=14, shrinkB=14, zorder=1))
for v, (x, y) in pos.items():
    ax.add_patch(Circle((x, y), .2, facecolor=C.PAPER, edgecolor=C.INK, lw=1.4, zorder=3))
    label(ax, v, (x, y), ha='center', va='center', fontsize=10)
    off = {'N': (8, 8), 'S': (8, -15), 'K': (-28, 0), 'E': (8, 0)}[v]
    label(ax, f'度 {degree[v]}', (x, y), offset=off, fontsize=9)
label(ax, '四个奇度点', (2.6, -.18), ha='center', va='top', fontsize=11)
ax.set(xlim=(-.65, 5.25), ylim=(-.65, 4.25), aspect='equal')
ax.axis('off')
save(fig, 'K22-n3')

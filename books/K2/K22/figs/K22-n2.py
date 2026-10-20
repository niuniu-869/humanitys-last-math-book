import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

from matplotlib.patches import Circle, Rectangle, FancyArrowPatch

pos = {'E': (2.7, 3.2), 'C': (0.8, 2.0), 'D': (2.7, 2.0), 'F': (4.6, 2.0),
       'A': (1.7, .7), 'B': (3.7, .7)}
edges = ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', 'DF', 'EF']
assert len(edges) == 9
fig, ax = new_fig(14, 8.5)
same = {'CD': -.25, 'DF': .25, 'AB': 0}
tree = {'EC', 'ED', 'EF', 'CA', 'CB', 'DB'}
for edge in edges:
    a, b = edge
    key = ''.join(sorted((a, b)))
    is_tree = key in {''.join(sorted(e)) for e in tree}
    rad = same.get(key, 0)
    ax.add_patch(FancyArrowPatch(pos[a], pos[b], connectionstyle=f'arc3,rad={rad}', arrowstyle='-',
                                 color=C.INK, lw=1.8 if is_tree else 1.2,
                                 ls='-' if is_tree else '--', shrinkA=12, shrinkB=12, zorder=1))
levels = {0: ['E'], 1: ['C', 'D', 'F'], 2: ['A', 'B']}
for level, nodes in levels.items():
    y = {0: 3.2, 1: 2.0, 2: .7}[level]
    label(ax, f'第 {level} 层', (-.55, y), ha='right', va='center', fontsize=9)
    for v in nodes:
        x, _ = pos[v]
        if level == 0:
            ax.add_patch(Circle((x, y), .18, facecolor=C.INK, edgecolor=C.INK, zorder=3))
        elif level == 1:
            ax.add_patch(Circle((x, y), .18, facecolor=C.PAPER, edgecolor=C.INK, lw=1.4, zorder=3))
        else:
            ax.add_patch(Rectangle((x-.17, y-.17), .34, .34, facecolor=C.PAPER, edgecolor=C.INK, lw=1.4, zorder=3))
        label(ax, v, (x, y), offset=(0, 17) if level == 0 else (0, 0), ha='center', va='center', fontsize=10)
ax.set(xlim=(-1.35, 5.5), ylim=(-.65, 3.75), aspect='equal')
ax.axis('off')
save(fig, 'K22-n2')

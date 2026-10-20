import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

from matplotlib.patches import Circle

pos = {'1': (2.5, 0), '2': (1.4, 1.2), '3': (3.6, 1.2), '4': (1.4, 2.4), '6': (3.6, 2.4), '12': (2.5, 3.6)}
edges = [('1','2'), ('1','3'), ('2','4'), ('2','6'), ('3','6'), ('4','12'), ('6','12')]
assert len(edges) == 7
fig, ax = new_fig(10, 8)
for a, b in edges:
    ax.plot(*zip(pos[a], pos[b]), color=C.INK, lw=1.8, zorder=1)
for v, (x, y) in pos.items():
    ax.add_patch(Circle((x, y), .22, facecolor=C.PAPER, edgecolor=C.INK, lw=1.4, zorder=3))
    label(ax, v, (x, y), ha='center', va='center', fontsize=10)
ax.set(xlim=(-.2, 5.2), ylim=(-1.0, 4.15), aspect='equal')
ax.axis('off')
save(fig, 'K22-n7')

import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

from matplotlib.patches import Circle

pos = {'A': (0, 1), 'B': (1, 2), 'C': (1, 0), 'D': (3, 2), 'E': (3, 0), 'F': (4, 1)}
edges = [('A', 'B', 4), ('A', 'C', 2), ('B', 'C', 1), ('B', 'D', 5),
         ('C', 'D', 8), ('C', 'E', 10), ('D', 'E', 2), ('D', 'F', 6), ('E', 'F', 3)]
degrees = {v: 0 for v in pos}
for a, b, _ in edges:
    degrees[a] += 1; degrees[b] += 1
assert len(edges) == 9 and [degrees[v] for v in 'ABCDEF'] == [2, 3, 4, 4, 3, 2]

fig, ax = new_fig(13.5, 7.2)
for a, b, weight in edges:
    ax.plot(*zip(pos[a], pos[b]), color=C.INK, lw=1.8, zorder=1)
    mx, my = (np.array(pos[a]) + np.array(pos[b])) / 2
    off = (10, 0) if a+b in ('BC', 'DE') else (-10, 7) if a+b == 'CD' else (0, 8)
    label(ax, str(weight), (mx, my), offset=off, ha='center', va='center', fontsize=9, fontstyle='italic')
offsets = {'A': (-33, -4), 'B': (-10, 16), 'C': (-17, -22), 'D': (0, 16), 'E': (4, -22), 'F': (14, -4)}
for v, (x, y) in pos.items():
    ax.add_patch(Circle((x, y), .16, facecolor=C.PAPER, edgecolor=C.INK, lw=1.4, zorder=3))
    label(ax, v, (x, y), ha='center', va='center', fontsize=9)
    label(ax, f'度 {degrees[v]}', (x, y), offset=offsets[v], fontsize=9)
label(ax, '度之和 $=18=2\\times9$', (2, -0.78), ha='center', va='center', fontsize=11)
ax.set(xlim=(-.8, 4.9), ylim=(-1.15, 2.55), aspect='equal')
ax.axis('off')
save(fig, 'K22-n1')

import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import FancyBboxPatch

nodes, events = {}, []
positions = {'': (7, 6), 'L': (4, 4), 'R': (11, 4),
             'LL': (2.5, 2), 'LR': (6, 2), 'RL': (10, 2),
             'RR': (12.5, 2), 'LLL': (1.2, 0), 'LLR': (3.8, 0)}

def visit(k, path=''):
    nodes[path] = k
    if k <= 0:
        return
    events.append((path, '先', k))
    visit(k - 1, path + 'L')
    events.append((path, '后', k))
    visit(k - 2, path + 'R')

visit(3)
assert len(nodes) == 9 and sum(k <= 0 for k in nodes.values()) == 5
assert [e[2] for e in events] == [3, 2, 1, 1, 2, 3, 1, 1]
fig, ax = new_fig(19, 11)
for path in nodes:
    if path:
        x0, y0 = positions[path[:-1]]
        x1, y1 = positions[path]
        ax.plot([x0, x1], [y0 - .29, y1 + .29], color=C.INK, ls='-', lw=1)
for path, k in nodes.items():
    x, y = positions[path]
    ax.add_patch(FancyBboxPatch((x - .76, y - .27), 1.52, .54,
                 boxstyle='round,pad=0.04,rounding_size=0.10',
                 facecolor=C.LIGHT if k <= 0 else C.PAPER,
                 edgecolor=C.INK, lw=1, zorder=3))
    label(ax, f'Show({k})', (x, y), ha='center', va='center', fontsize=10)
for order, (path, side, k) in enumerate(events, 1):
    x, y = positions[path]
    direction = -1 if side == '先' else 1
    label(ax, f'{side} {k}', (x + direction * 1.28, y),
          ha='center', va='center', fontsize=9)
    label(ax, str(order), (x + direction * 2.03, y), ha='center', va='center',
          fontsize=8, bbox=dict(boxstyle='circle,pad=0.18', fc=C.PAPER, ec=C.INK, lw=.8))
label(ax, '出口：n ≤ 0', (7, -.85), ha='center', va='center', fontsize=9)
ax.set(xlim=(-.2, 13.8), ylim=(-1.25, 6.65))
ax.axis('off')
fig.tight_layout()
save(fig, "K36-n1")

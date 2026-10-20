import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import FancyBboxPatch
from collections import Counter

nodes = {}
leaf = 0

def build(k, path='', depth=0):
    global leaf
    if k <= 1:
        x = leaf * 1.55
        leaf += 1
    else:
        left = build(k - 1, path + 'L', depth + 1)
        right = build(k - 2, path + 'R', depth + 1)
        x = (left + right) / 2
    nodes[path] = (k, x, -depth * 1.6)
    return x

build(5)
counts = Counter(v[0] for v in nodes.values())
assert len(nodes) == 15 and counts == {5: 1, 4: 1, 3: 2, 2: 3, 1: 5, 0: 3}
fig, ax = new_fig(19, 12)
for prefix in ('LL', 'R'):
    members = [v for p, v in nodes.items() if p.startswith(prefix)]
    xmin = min(v[1] for v in members) - .70
    xmax = max(v[1] for v in members) + .70
    ymin = min(v[2] for v in members) - .47
    ymax = max(v[2] for v in members) + .76
    ax.add_patch(FancyBboxPatch((xmin, ymin), xmax-xmin, ymax-ymin,
                 boxstyle='round,pad=0.03,rounding_size=0.12',
                 facecolor='none', edgecolor=C.INK, ls='--', lw=1))
    tx = xmin + .18 if prefix == 'LL' else xmax - .18
    label(ax, '重复 2 次', (tx, ymax-.23),
          fontsize=9, ha='left' if prefix == 'LL' else 'right', va='center')
for path, (k, x, y) in nodes.items():
    if path:
        _, px, py = nodes[path[:-1]]
        ax.plot([px, x], [py-.23, y+.23], color=C.INK, ls='-', lw=1)
for path, (k, x, y) in nodes.items():
    ax.add_patch(FancyBboxPatch((x-.52, y-.23), 1.04, .46,
                 boxstyle='round,pad=0.03,rounding_size=0.08',
                 facecolor=C.LIGHT if k <= 1 else C.PAPER,
                 edgecolor=C.INK, lw=1, zorder=3))
    label(ax, f'Fib({k})', (x, y), fontsize=9, ha='center', va='center')
    if k == 2:
        label(ax, '×3', (x+.61, y), fontsize=9, va='center')
label(ax, '出口：Fib(1)、Fib(0)', (5.4, -7.25), fontsize=9, ha='center')
ax.set(xlim=(-.95, 12), ylim=(-7.55, .65))
ax.axis('off')
fig.tight_layout()
save(fig, "K36-n2")

import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Circle, Rectangle
from collections import Counter

nodes = []
leaf_count = 0

def build(k, depth=0):
    global leaf_count
    node = dict(k=k, y=-2.8*depth, children=[])
    nodes.append(node)
    if k < 2:
        node.update(x=2.25*leaf_count, value=k)
        leaf_count += 1
    else:
        node['children'] = [build(k-1, depth+1), build(k-2, depth+1)]
        node['x'] = sum(c['x'] for c in node['children']) / 2
        node['value'] = sum(c['value'] for c in node['children'])
    return node

root = build(5)
counts = Counter(v['k'] for v in nodes)
assert len(nodes) == 15 and leaf_count == 8
assert counts == {5: 1, 4: 1, 3: 2, 2: 3, 1: 5, 0: 3}
assert sum(v['k'] >= 2 for v in nodes) == 7
assert all(v['value'] == [0, 1, 1, 2, 3, 5][v['k']] for v in nodes)

def descendants(node):
    return [node] + [v for c in node['children'] for v in descendants(c)]

fig, ax = new_fig(23, 16)
for node in nodes:
    for child in node['children']:
        ax.plot([node['x'], child['x']], [node['y'], child['y']],
                color=C.INK, lw=.9, ls='-', zorder=1)

# Nested boxes enclose complete subtrees, including every descendant.
for node in nodes:
    if node['k'] not in (2, 3):
        continue
    sub = descendants(node)
    pad = 1.02 if node['k'] == 3 else .75
    left = min(v['x'] for v in sub) - pad
    right = max(v['x'] for v in sub) + pad
    bottom = min(v['y'] for v in sub) - pad
    top = node['y'] + pad
    ax.add_patch(Rectangle((left, bottom), right-left, top-bottom,
                          fill=False, edgecolor=C.INK, ls='--', lw=.8))
    label(ax, '重复', (left+.12, top+.15), fontsize=8, va='bottom')

for node in nodes:
    x, y = node['x'], node['y']
    if node['k'] < 2:
        patch = Rectangle((x-.60, y-.46), 1.20, .92,
                          facecolor=C.PAPER, edgecolor=C.INK, lw=1)
    else:
        patch = Circle((x, y), .63, facecolor=C.PAPER, edgecolor=C.INK, lw=1)
    patch.set_zorder(3)
    ax.add_patch(patch)
    label(ax, f"FIB({node['k']})", (x, y), ha='center', va='center', fontsize=8)
    value_xy = (x+.40, y-.62) if node['k'] < 2 else (x+.80, y-.25)
    label(ax, str(node['value']), value_xy, fontsize=7, va='center')
label(ax, '总结点数 15', (14.8, 0), ha='center', fontsize=10)
ax.set(xlim=(-1.5, 17.4), ylim=(-12.7, 1.2), aspect='equal')
ax.axis('off')
fig.subplots_adjust(left=.02, right=.98, bottom=.02, top=.98)
save(fig, "K31-n2")

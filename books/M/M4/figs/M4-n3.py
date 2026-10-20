import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(19, 11)
ax.set(xlim=(-0.8, 10.8), ylim=(-0.65, 7.3))
ax.axis('off')
nodes = {
    'root': (5, 6.4, '$X_1$ 是 1 吗？', 10, 4),
    'left': (2.1, 4.5, '$X_2$ 是 1 吗？', 4, 3),
    'right': (7.9, 4.5, '$X_2$ 是 1 吗？', 6, 1),
    'lh': (3.0, 2.4, '$X_3$ 是 1 吗？', 2, 1),
    'rh': (7.0, 2.4, '$X_3$ 是 1 吗？', 3, 1),
    'll': (0.5, 2.4, '$Y=1$\n2 个', 2, 2),
    'rr': (9.5, 2.4, '$Y=0$\n3 个', 3, 0),
    'lhy': (1.8, 0.2, '$Y=1$\n1 个', 1, 1),
    'lhn': (4.2, 0.2, '$Y=0$\n1 个', 1, 0),
    'rhn': (5.8, 0.2, '$Y=1$\n1 个', 1, 1),
    'rhy': (8.2, 0.2, '$Y=0$\n2 个', 2, 0),
}
edges = [('root', 'left', '1'), ('root', 'right', '0'),
         ('left', 'll', '1'), ('left', 'lh', '0'),
         ('right', 'rh', '1'), ('right', 'rr', '0'),
         ('lh', 'lhy', '1'), ('lh', 'lhn', '0'),
         ('rh', 'rhn', '0'), ('rh', 'rhy', '1')]
questions = {'root', 'left', 'right', 'lh', 'rh'}
for parent in questions:
    children = [nodes[target] for source, target, _ in edges if source == parent]
    assert sum(child[3] for child in children) == nodes[parent][3]
    assert sum(child[4] for child in children) == nodes[parent][4]
entropy = lambda p: -p*np.log2(p) - (1-p)*np.log2(1-p)
gain = entropy(0.4) - 0.4*entropy(0.75) - 0.6*entropy(1/6)
assert round(gain, 3) == 0.256
for source, target, answer in edges:
    x1, y1 = nodes[source][:2]
    x2, y2 = nodes[target][:2]
    end_y = y2 + (0.29 if target in questions else 0.44)
    ax.annotate('', xy=(x2, end_y), xytext=(x1, y1-0.30),
                arrowprops=dict(arrowstyle='->', color=C.INK, lw=1.0))
    mx, my = (x1+x2)/2, (y1+y2)/2
    label(ax, answer, (mx, my), (-9 if x2 < x1 else 9, 0),
          ha='right' if x2 < x1 else 'left', va='center', fontsize=9)
for key, (x, y, text, count, defaults) in nodes.items():
    boxstyle = 'square,pad=0.35' if key in questions else 'round,pad=0.4'
    ax.text(x, y, text, ha='center', va='center', color=C.INK, fontsize=10,
            bbox=dict(boxstyle=boxstyle, facecolor=C.PAPER, edgecolor=C.INK, lw=1))
    if key in questions:
        offset = (32, 24) if key == 'lh' else (-32, 24) if key == 'rh' else (0, 24)
        label(ax, f'{count} 个\n$Y=1$：{defaults} 个', (x, y), offset,
              ha='center', fontsize=8)
label(ax, f'信息增益 {gain:.3f}', (6.25, 6.4), fontsize=9, va='center')
fig.tight_layout(pad=0.5)
save(fig, "M4-n3")

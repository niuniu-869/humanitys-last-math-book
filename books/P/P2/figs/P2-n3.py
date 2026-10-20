import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle, Ellipse

fig, (left, right) = new_fig(24, 11, ncols=2, gridspec_kw={'width_ratios': [1, 2.3]})
fig.subplots_adjust(left=0.02, right=0.99, top=0.94, bottom=0.08, wspace=0.08)
left.set(xlim=(-0.15, 3.2), ylim=(-0.65, 3.7), aspect='equal')
left.axis('off')
left.add_patch(Rectangle((0, 0), 3, 3, fill=False, edgecolor=C.INK, lw=1.2))
left.add_patch(Ellipse((1.5, 1.5), 2.7, 1.5, facecolor=C.LIGHT,
                       edgecolor=C.INK, lw=1.3, ls='-'))
for x in [1, 2]:
    left.plot([x, x], [0, 3], color=C.INK, lw=1.2, ls='--')
for i in range(1, 4):
    label(left, rf'$B_{i}$', (i - .5, 2.65), ha='center')
    label(left, rf'$AB_{i}$', (i - .5, 1.5), ha='center', va='center')
label(left, r'$\Omega$', (0.05, 3.25), ha='left')
label(left, r'阴影 = $A$', (1.5, -0.45), ha='center')

right.set(xlim=(-0.3, 9.5), ylim=(-0.65, 7.2))
right.axis('off')
root = (0, 3.45)
dot(right, root, size=18)
for i, y in enumerate([5.9, 3.45, 1.0], 1):
    node, a, other = (2.5, y), (5.1, y + .65), (5.1, y - .65)
    right.plot([root[0], node[0]], [root[1], node[1]], color=C.INK, lw=2.0, ls='-')
    right.plot([node[0], a[0]], [node[1], a[1]], color=C.INK, lw=2.0, ls='-')
    right.plot([node[0], other[0]], [node[1], other[1]], color=C.INK, lw=0.9, ls='--')
    dot(right, node, size=18)
    dot(right, a, size=22)
    right.scatter(*other, s=24, facecolors=C.PAPER, edgecolors=C.INK, zorder=5)
    branch_y = root[1] + (y - root[1]) * 1.15 / 2.5
    label(right, rf'$P(B_{i})$', (1.15, branch_y),
          offset=(0, -19 if i == 3 else 15), ha='center')
    label(right, rf'$B_{i}$', node, offset=(0, -18), ha='center')
    label(right, rf'$P(A\mid B_{i})$', (3.8, y+.45), offset=(0, 10), ha='center')
    label(right, '$A$', a, offset=(7, 0), va='center')
    label(right, r'$\overline{A}$', other, offset=(7, 0), va='center')
    label(right, rf'$P(B_{i})P(A\mid B_{i})$', (6.15, a[1]), va='center')
for y in [5.325, 2.875]:
    label(right, '$+$', (7.65, y), ha='center', va='center', fontsize=14)
right.plot([6.15, 9.2], [0.9, 0.9], color=C.INK, lw=0.7, ls='-')
label(right, r'$=P(A)$', (7.65, 0.25), ha='center', va='center', fontsize=12)
save(fig, 'P2-n3')

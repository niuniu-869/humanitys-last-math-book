import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle, FancyArrowPatch

a = [5, 2, 8, 1, 9, 3]
pairs = [(0, 1), (0, 3), (0, 5), (1, 3), (2, 3), (2, 5), (4, 5)]
counts = [sum(a[j] < a[i] for j in range(i + 1, len(a))) for i in range(len(a))]
assert counts == [3, 1, 2, 0, 1, 0] and len(pairs) == 7

fig, ax = new_fig(17, 7.2)
xs = np.arange(6) * 1.45
for i, value in enumerate(a):
    ax.add_patch(Rectangle((xs[i] - .43, 0), .86, .8, facecolor=C.PAPER,
                           edgecolor=C.INK, lw=1.2))
    label(ax, str(value), (xs[i], .4), ha='center', va='center', fontsize=14)
    label(ax, str(i + 1), (xs[i], -.22), ha='center', va='center', fontsize=9)
    label(ax, str(counts[i]), (xs[i], -0.72), ha='center', va='center', fontsize=11)
label(ax, '右边比它小的个数', (xs[0] - 1.15, -0.72), ha='right', va='center', fontsize=9)
label(ax, '合计 7', (xs[-1] + 1.05, -0.72), ha='left', va='center', fontsize=11)

for i, j in pairs:
    span = j - i
    height = 1.10 + 0.34 * span + 0.12 * i
    ax.add_patch(FancyArrowPatch((xs[i], .82), (xs[j], .82),
        connectionstyle=f'arc3,rad={-height / max(xs[j] - xs[i], .1)}',
        arrowstyle='-', lw=1.0, color=C.INK))
ax.set(xlim=(-1.8, 9.7), ylim=(-1.15, 4.1), aspect='equal')
ax.axis('off')
save(fig, 'K32-n1')

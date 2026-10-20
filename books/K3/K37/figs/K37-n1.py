import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle, FancyArrowPatch

values = [1, 2, 3, 5, 8, 9]
assert values[1:5] == [2, 3, 5, 8] and 2 / len(values[1:5]) == 0.5
fig, axes = new_fig(18, 12, nrows=2)
for ax, pivot, title in zip(axes, [1, 2], [
    '端点先选中（2 或 8；图示选 2）',
    '中间的数先选中（3 或 5；图示选 3）',
]):
    ax.set(xlim=(-0.7, 5.7), ylim=(-1.15, 1.85))
    ax.axis('off')
    ax.set_title(title, pad=10)
    for i, value in enumerate(values):
        ax.add_patch(Rectangle((i-.34, -.3), .68, .6,
            facecolor=C.LIGHT if 1 <= i <= 4 else C.PAPER,
            edgecolor=C.INK, lw=2.6 if i == pivot else 1, zorder=3))
        label(ax, str(value), (i, 0), ha='center', va='center', fontsize=12)
        label(ax, rf'$z_{i+1}$', (i, .43), (10, 0) if pivot == 2 and i == 2 else (0, 0),
              ha='center', va='bottom')
    ax.plot([.66, .66, 4.34, 4.34], [-.49, -.65, -.65, -.49],
            color=C.INK, ls='-', lw=1.1)
    label(ax, r'$S=\{2,3,5,8\}$', (2.5, -.94), ha='center')
    if pivot == 1:
        ax.add_patch(FancyArrowPatch((1, .81), (4, .81),
            connectionstyle='arc3,rad=-0.35', arrowstyle='<->',
            mutation_scale=11, color=C.INK, lw=1.4, ls='-'))
        label(ax, '比较', (2.5, 1.78), ha='center')
    else:
        ax.plot([2, 2], [-.48, 1.22], color=C.INK, ls='--', lw=1.2, zorder=2)
        label(ax, '分到两边，永不比较', (2.5, 1.47), ha='center')
fig.subplots_adjust(hspace=.48, bottom=.13, top=.92)
fig.text(.5, .035, '4 个数等可能先被选：2 个端点 → 概率 2/4 = 1/2', ha='center')
save(fig, "K37-n1")

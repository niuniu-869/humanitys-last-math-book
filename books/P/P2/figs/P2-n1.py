import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle

points = [(x, y) for x in range(1, 7) for y in range(1, 7)]
event = [(x, y) for x, y in points if x == 6 or y == 6]
condition = [(x, y) for x, y in points if x + y >= 10]
joint = [p for p in condition if p in event]
assert len(event) == 11 and len(condition) == 6 and len(joint) == 5
assert set(condition) - set(joint) == {(5, 5)}

fig, axes = new_fig(21, 10, ncols=2)
fig.subplots_adjust(left=0.07, right=0.97, bottom=0.21, top=0.84, wspace=0.65)
for ax, shown, shaded in zip(axes, [points, condition], [event, joint]):
    for x, y in shaded:
        ax.add_patch(Rectangle((x - 0.5, y - 0.5), 1, 1,
                               facecolor=C.LIGHT, edgecolor='none'))
    for t in np.arange(0.5, 7, 1):
        ax.plot([0.5, 6.5], [t, t], color=C.GRAY, lw=0.5, ls=':')
        ax.plot([t, t], [0.5, 6.5], color=C.GRAY, lw=0.5, ls=':')
    for p in shown:
        dot(ax, p, size=12)
    ax.set(xlim=(0.5, 6.5), ylim=(0.5, 6.5), xticks=range(1, 7),
           yticks=range(1, 7), xlabel='第一颗', ylabel='第二颗', aspect='equal')
axes[1].scatter(*np.array(condition).T, s=160, facecolors='none',
                edgecolors=C.INK, linewidths=1.1, zorder=4)
axes[0].set_title('原来的样本空间：36 个点', pad=14)
axes[1].set_title('已知和不小于 10：只剩 6 个点', pad=14)
label(axes[0], r'阴影 = 至少一颗是 6，$\frac{11}{36}$', (3.5, -1.15),
      ha='center', va='center', annotation_clip=False)
label(axes[1], r'阴影 = 其中有 6 的 5 个，占 $\frac{5}{6}$', (3.5, -1.15),
      ha='center', va='center', annotation_clip=False)
middle = fig.add_axes([0.415, 0.46, 0.17, 0.15])
middle.set(xlim=(0, 1), ylim=(0, 1))
middle.axis('off')
arrow(middle, (0.1, 0.3), (0.8, 0), color=C.INK)
label(middle, '只看这一块\n放大回 1', (0.5, 0.6), ha='center', va='bottom', fontsize=9)
save(fig, 'P2-n1')

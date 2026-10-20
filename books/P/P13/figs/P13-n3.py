import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, axes = new_fig(18, 9, ncols=2, sharey=True)
for ax, pair, title in zip(axes, [([10, 12], [13, 15]), ([11, 15], [18, 12])],
                           ['无交互：两线平行', '有交互：两线交叉']):
    ax.plot([0, 1], pair[0], '-o', color=C.INK, label='设计 1', markersize=5)
    ax.plot([0, 1], pair[1], '--s', color=C.INK, markerfacecolor=C.PAPER,
            label='设计 2', markersize=5)
    ax.set(xlim=(-.2, 1.2), ylim=(8, 20), xlabel='设备', title=title)
    ax.set_xticks([0, 1], ['手机', '电脑'])
    ax.set_yticks([8, 10, 12, 14, 16, 18, 20])
axes[0].set_ylabel('停留时长')
axes[0].legend(loc='upper left')
fig.subplots_adjust(left=.09, right=.98, bottom=.15, top=.88, wspace=.18)
save(fig, "P13-n3")

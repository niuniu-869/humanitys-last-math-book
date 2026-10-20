import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle

points = np.array([(0, 0), (4, 0), (0, 2), (4, 2)])
fig, axes = new_fig(17, 7.5, ncols=2)
for ax, groups, title, expected in [
        (axes[0], [[0, 2], [1, 3]], '左右分堆', 4),
        (axes[1], [[0, 1], [2, 3]], '上下分堆', 16)]:
    centers = np.array([points[group].mean(axis=0) for group in groups])
    objective = sum(np.sum((points[group]-center)**2) for group, center in zip(groups, centers))
    assert np.isclose(objective, expected)
    distances = np.sum((points[:, None, :]-centers[None, :, :])**2, axis=2)
    for i, group in enumerate(groups):
        assert np.all(distances[group, i] == distances[group].min(axis=1))
        low, high = points[group].min(axis=0)-0.42, points[group].max(axis=0)+0.42
        ax.add_patch(Rectangle(low, *(high-low), fill=False, edgecolor=C.INK, ls='--', lw=1))
    ax.scatter(*points.T, s=32, marker='o', color=C.INK, label='数据点', zorder=4)
    ax.scatter(*centers.T, s=48, marker='s', color=C.INK, label='中心', zorder=4)
    ax.set(xlim=(-1, 5), ylim=(-1, 3), xlabel='$x$', ylabel='$y$')
    ax.set_aspect('equal')
    ax.set_xticks([0, 2, 4]); ax.set_yticks([0, 1, 2])
    ax.set_title(f'{title}：$J={objective:g}$', pad=12)
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=2, bbox_to_anchor=(0.5, 0.01))
fig.tight_layout(rect=(0, 0.13, 1, 1), w_pad=2)
save(fig, "M4-n6")

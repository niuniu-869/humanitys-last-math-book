import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

prob = np.array([0.057, 0.153, 0.349, 0.615, 0.826])
y = np.array([0, 0, 1, 0, 1])
thresholds = np.array([0.9, 0.7, 0.5, 0.3, 0.1])
precision = []
recall = []
for t in thresholds:
    pred = prob >= t
    tp = np.sum(pred & (y == 1))
    fp = np.sum(pred & (y == 0))
    fn = np.sum((~pred) & (y == 1))
    precision.append(tp / (tp + fp) if tp + fp else 0.0)
    recall.append(tp / (tp + fn) if tp + fn else 0.0)
precision = np.array(precision)
recall = np.array(recall)
assert np.allclose(precision, [0, 1, 0.5, 2 / 3, 0.5])
assert np.allclose(recall, [0, 0.5, 0.5, 1, 1])

fig, ax = new_fig(12, 7.5)
ax.plot(thresholds, recall, color=C.INK, ls='-', marker='o', markersize=5.5, label='召回率')
ax.plot(thresholds, precision, color=C.GRAY, ls='--', marker='o', markerfacecolor=C.PAPER,
        markeredgecolor=C.GRAY, markersize=5.5, label='精确率')
ax.scatter([0.5], [0.5], s=40, color=C.INK, zorder=6)
ax.scatter([0.5], [0.5], s=52, facecolors=C.PAPER, edgecolors=C.GRAY, linewidths=1.0, zorder=7)
ax.scatter([0.3], [2 / 3], s=40, color=C.GRAY, zorder=6)
note = ('阈值 0.5：精确率 0.5，召回率 0.5\n'
        '（空心加实心点）\n'
        '阈值 0.3：精确率 2/3，召回率 1\n'
        '（灰色实心点）\n'
        '阈值 0.9 时没有样本判为 1，\n'
        '精确率无定义，按 0 画')
label(ax, note, (0.48, 0.06), offset=(0, 0), fontsize=7.0, va='bottom', linespacing=1.10)
ax.set_xticks(thresholds, [f'{t:.1f}' for t in thresholds])
ax.set_xlim(0.95, 0.05)
ax.set_ylim(-0.08, 1.08)
ax.set(xlabel='阈值', ylabel='比例')
ax.legend(loc='upper left', fontsize=8.5, bbox_to_anchor=(0.0, 0.93),
          borderaxespad=0.5, handlelength=1.4, handletextpad=0.5,
          labelspacing=0.4, borderpad=0.25)
save(fig, 'M2-n6')

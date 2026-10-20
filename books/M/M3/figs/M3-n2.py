import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

d = np.arange(5)
bias = np.array([26.01, 0, 0, 0, 0])
variance = np.array([0.05, 0.275, 1.15, 6.05, 62.75])
total = bias + variance + 0.25
training = np.array([6.0, 0.22, 0.0914, 0.0714, 0])
assert np.argmin(total) == 1 and np.isclose(total[1], 0.525)
fig, ax = new_fig(15, 10)
ax.plot(d, bias, ls='--', color=C.RED, label='偏差²', lw=1.6, zorder=4)
ax.plot(d, variance, ls=':', color=C.INK, label='方差', lw=2.2, zorder=5)
ax.plot(d, total, ls='-', color=C.TEAL, label='偏差²+方差+噪声', lw=3)
ax.plot(d, training, ls='-', marker='s', markersize=4, color=C.INK,
        label='训练误差', lw=0.9, zorder=6)
ax.axvline(1, color=C.GRAY, ls='--', lw=0.8)
label(ax, '最佳', (1, total[1]), offset=(18, 33), fontsize=9,
      arrowprops=dict(arrowstyle='->', color=C.INK))
label(ax, '欠拟合：偏差大', (0.25, 24.5), fontsize=9)
label(ax, '过拟合：方差大', (2.4, 16.5), fontsize=9)
label(ax, '方差 62.75\n总误差 63', (2.45, 28),
      ha='left', va='top', fontsize=9)
arrow(ax, (4, 25.5), (0, 4), color=C.INK, lw=1.0)
ax.set(xlim=(-0.08, 4.15), ylim=(-0.8, 30),
       xlabel='模型复杂度（多项式次数 0–4）', ylabel='误差')
ax.set_xticks(d); ax.set_yticks(range(0, 31, 5))
ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.02), ncol=2, fontsize=9)
fig.tight_layout()
save(fig, "M3-n2")

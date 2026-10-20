import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Polygon

fig, ax = new_fig(11, 9)
ax.add_patch(Polygon([(0, 0), (15, 0), (60, 45), (60, 60), (45, 60), (0, 15)],
                     closed=True, facecolor=C.LIGHT, edgecolor='none', zorder=0))
ax.plot([0, 45], [15, 60], color=C.INK, ls='--', lw=1.2)
ax.plot([15, 60], [0, 45], color=C.INK, ls='--', lw=1.2)
label(ax, '阴影 = 碰得上', (30, 32), ha='center', va='center', fontsize=9)
label(ax, r'$|x-y|\leq15$', (30, 27), ha='center', va='center', fontsize=10)
label(ax, '空白 = 碰不上', (10, 52), ha='center', va='center', fontsize=9)
label(ax, '$45\\times45\\div2$', (12, 48), ha='center', va='center', fontsize=9)
label(ax, '$45\\times45\\div2$', (48, 12), ha='center', va='center', fontsize=9)
ax.set(xlim=(0, 60), ylim=(0, 60), aspect='equal', xlabel='甲到达时刻 $x$（分钟）', ylabel='乙到达时刻 $y$')
ax.set_xticks([0, 15, 45, 60]); ax.set_yticks([0, 15, 45, 60])
for side in ('top', 'right'): ax.spines[side].set_visible(True)
assert 2*45*45/2 == 2025 and 1-2025/3600 == 7/16
save(fig, 'P1-n5')

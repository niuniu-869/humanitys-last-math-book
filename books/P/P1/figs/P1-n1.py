import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle, Circle

points = [(i, j) for i in range(1, 7) for j in range(1, 7)]
shadow = [(i, j) for i, j in points if i == 6 or j == 6]
sum10 = [(i, j) for i, j in points if i + j >= 10]
sum7 = [(i, j) for i, j in points if i + j == 7]
assert len(shadow) == 11 and len(sum10) == 6 and len(sum7) == 6
assert set(sum10) - set(shadow) == {(5, 5)}

fig, ax = new_fig(14, 9)
for i, j in points:
    ax.add_patch(Rectangle((i - .5, j - .5), 1, 1,
                           facecolor=C.LIGHT if (i, j) in shadow else C.PAPER,
                           edgecolor=C.GRAY, lw=.65, zorder=0))
    dot(ax, (i, j), size=18)
for i, j in sum10:
    ax.add_patch(Circle((i, j), .27, fill=False, edgecolor=C.INK, lw=1.35, zorder=4))
xs = np.linspace(1, 6, 200)
ax.plot(xs, 7 - xs, color=C.INK, ls='-.', lw=1.2, zorder=2)
label(ax, '点划线 = 和为 7（6 个点）', (.58, 7.96), ha='left', fontsize=9)
label(ax, '阴影 = 至少有一颗是 6（11 个点）', (0.58, 7.0), ha='left', fontsize=9)
label(ax, '圆圈 = 点数和不小于 10（6 个点）', (.58, 7.48), ha='left', fontsize=9)
ax.set(xlim=(.35, 7.3), ylim=(.25, 8.35), aspect='equal',
       xlabel='第一颗的点数 $i$', ylabel='第二颗的点数 $j$')
ax.set_xticks(range(1, 7)); ax.set_yticks(range(1, 7))
save(fig, 'P1-n1')

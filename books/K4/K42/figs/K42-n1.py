import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle

durations = np.array([8, 40, 84, 18])
edges = np.r_[0, durations.cumsum()]
rate = 60 / 84
assert edges[-1] == 150 and 84 / 7 == 12
assert np.isclose(4 / rate, 5.6)
fig, ax = new_fig(19, 6.5)
for left, width, fill, hatch in zip(edges[:-1], durations,
                                    [C.PAPER, C.LIGHT, C.PAPER, C.PAPER],
                                    ['///', None, None, '...']):
    ax.add_patch(Rectangle((left, 0), width, .6, facecolor=fill,
                           edgecolor=C.INK, lw=1.1, hatch=hatch))
for x in np.arange(60, 132, 12):
    ax.plot([x, x], [0, .6], color=C.GRAY, lw=.65, ls='-')
for x, text in [(4, '扫卷\n8 分钟'), (28, '选择题 10 题，40 分钟'),
                (90, '解答题 7 题，84 分钟'), (141, '检查\n18 分钟')]:
    label(ax, text, (x, .76), ha='center', va='bottom', fontsize=9)
ax.plot([8, 8, 48, 48], [1.16, 1.29, 1.29, 1.16], color=C.INK, lw=1, ls='-')
label(ax, '放弃线 ≈ 5.6 分钟/题', (28, 1.38), ha='center', fontsize=10)
for x in edges:
    ax.plot([x, x], [0, -.06], color=C.INK, lw=.8)
    label(ax, str(x), (x, -.12), ha='center', va='top', fontsize=9)
label(ax, '分钟', (154, -.12), va='top', fontsize=9)
label(ax, '40 分 ÷ 40 分钟 = 1 分/分钟', (28, -.46), ha='center', va='top', fontsize=9)
label(ax, '60 分 ÷ 84 分钟 ≈ 0.71 分/分钟', (90, -.46), ha='center', va='top', fontsize=9)
ax.set(xlim=(-6, 164), ylim=(-1, 1.75))
ax.set_axis_off()
fig.subplots_adjust(left=.03, right=.99, bottom=.04, top=.98)
print(f'K42-n1: boundaries={edges.tolist()}, rate={rate}, cutoff={4/rate}')
save(fig, "K42-n1")

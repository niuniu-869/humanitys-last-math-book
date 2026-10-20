import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle

names = ['过程', '计算', '概念', '方法', '时间']
scores = [11, 8, 7, 4, 4]
assert sum(scores) == 34 and scores[0] == 2+6+3 and scores[1] == 4+4
fig, ax = new_fig(18, 8.5)
fig.subplots_adjust(left=.10, right=.64, bottom=.18, top=.96)
for i, (name, score) in enumerate(zip(names, scores)):
    relearn = name in ['概念', '方法']
    ax.barh(i, score, height=.6, facecolor=C.PAPER if relearn else C.LIGHT,
            edgecolor=C.INK, lw=1, hatch='///' if relearn else None)
    label(ax, str(score), (score, i), (5, 0), va='center', fontsize=11)
ax.set(xlim=(0, 12), ylim=(4.6, -.6), xticks=np.arange(0, 13, 2),
       yticks=np.arange(5), yticklabels=names, xlabel='丢分')
for y, fill, hatch, text in [(.68, C.LIGHT, None, '浅灰：不用学新东西'),
                              (.43, C.PAPER, '///', '斜线：要回去重学')]:
    ax.add_patch(Rectangle((1.06, y), .055, .08, transform=ax.transAxes,
                           clip_on=False, facecolor=fill, edgecolor=C.INK, hatch=hatch, lw=1))
    label(ax, text, (1.14, y+.04), xycoords=ax.transAxes, va='center', fontsize=9)
print('K42-n5: total=', sum(scores))
save(fig, "K42-n5")

import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(17, 10)
ax.set(xlim=(-.8, 6.5), ylim=(-1.65, 6.2)); ax.axis('off')
arrow(ax, (-.3, 0), (0, 5.7), color=C.INK, lw=1.2)
label(ax, '论证的支撑度', (-.3, 5.85), ha='left', fontsize=9)
threshold = 2.6
for x, h in zip([1, 3, 5], [3.2, 4.8, 1.3]):
    ax.bar(x, h, width=.95, color=C.LIGHT, edgecolor=C.INK, lw=1.2)
    ax.bar(x, min(h, threshold), width=.95, color=C.LIGHT, edgecolor=C.INK,
           hatch='///', lw=1.2)
ax.plot([-.3, 6.3], [threshold, threshold], color=C.INK, ls='--', lw=1)
label(ax, '勉强成立', (6.3, threshold), offset=(0, 7), ha='right', fontsize=9)
arrow(ax, (3.7, 3.2), (0, 1.6), color=C.INK)
label(ax, '升高', (3.7, 4.8), offset=(5, 0), va='center')
arrow(ax, (5.7, 2.5), (0, -1.2), color=C.INK)
label(ax, '塌', (5.7, 1.3), offset=(5, 0), va='center')
for x, text in zip([1, 3, 5], ['原论证', '加上一个\n加强项', '去掉一个\n必须假设']):
    label(ax, text, (x, -.15), ha='center', va='top', fontsize=9)
label(ax, '去掉加强项：回到左边那根', (3, -1.45), ha='center', fontsize=9)
save(fig, "K15-n4")

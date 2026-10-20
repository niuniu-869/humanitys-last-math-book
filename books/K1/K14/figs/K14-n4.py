import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

groups = ['轻症','重症','合计']; a = [90,60,66]; b = [85,50,78]
x = np.arange(3); w = .34
fig, ax = new_fig(14, 8)
ba = ax.bar(x-w/2, a, w, color=C.PAPER, edgecolor=C.INK, label='药 A')
bb = ax.bar(x+w/2, b, w, color=C.LIGHT, edgecolor=C.INK, label='药 B')
for bars in (ba,bb):
    for bar in bars: label(ax, f'{bar.get_height():.0f}', (bar.get_x()+bar.get_width()/2, bar.get_height()), offset=(0,4), ha='center', va='bottom', fontsize=9)
for i,t in enumerate(['A 20 人，B 80 人','A 80 人，B 20 人','各 100 人']): label(ax, t, (i, -12), ha='center', va='top', fontsize=8.5)
ax.set(xlim=(-.65,2.65), ylim=(0,108), xticks=x, xticklabels=groups, ylabel='好转率（%）')
ax.legend(loc='upper right'); ax.grid(axis='y', color=C.LIGHT, lw=.7)
save(fig, 'K14-n4')

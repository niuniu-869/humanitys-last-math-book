import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

months = [0, 1]
fig, ax = new_fig(15, 9)
ax.plot(months, [30, 36], color=C.INK, ls='-', marker='o', ms=7, mfc=C.INK, label='A 城（推出会员制）')
ax.plot(months, [30, 34], color=C.INK, ls='--', marker='s', ms=7, mfc=C.PAPER, mec=C.INK, label='B 城（未推出）')
for x, y, t in [(1,36,'36'), (1,34,'34')]: label(ax, t, (x,y), offset=(7,0), va='center')
ax.annotate('', xy=(1.03,36), xytext=(1.03,34), arrowprops=dict(arrowstyle='<->', color=C.INK, lw=1.2))
label(ax, '2 个点：会员制可争取的部分', (1.08,35), offset=(4,0), va='center', fontsize=9)
ax.annotate('', xy=(0.93,34), xytext=(0.93,30), arrowprops=dict(arrowstyle='<->', color=C.INK, lw=1.0))
label(ax, '4 个点：共同因素（季节等）', (0.90,30.9), ha='right', va='center', fontsize=8.5)
ax.set(xlim=(-0.35,1.55), ylim=(28,38), xticks=months, xticklabels=['3 月前','3 月后'], yticks=np.arange(28,39,2), ylabel='复购率（%）')
ax.legend(loc='upper left', fontsize=8.5)
ax.grid(axis='y', color=C.LIGHT, lw=.7)
save(fig, 'K14-n2')

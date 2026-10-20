import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

k = np.arange(1,6); p = 0.8 ** k
fig, ax = new_fig(13, 8)
bars = ax.bar(k,p,color=C.LIGHT,edgecolor=C.INK,width=.62)
for x,y in zip(k,p): label(ax,f'{y:.2f}',(x,y),offset=(0,4),ha='center',va='bottom',fontsize=9)
ax.axhline(.5,color=C.INK,ls='--',lw=1.1); label(ax,'一半',(5.45,.5),offset=(3,0),va='center',fontsize=9)
ax.set(xlim=(.35,5.7), ylim=(0,1.02), xticks=k, xlabel='连续成立的步数', ylabel='概率')
ax.grid(axis='y',color=C.LIGHT,lw=.7)
save(fig, 'K14-n6')

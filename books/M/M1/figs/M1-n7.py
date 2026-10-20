import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

t=np.arange(0,1101); lr=np.where(t<=100,3e-4*t/100,3e-5+(3e-4-3e-5)*.5*(1+np.cos(np.pi*(t-100)/1000)))
fig,ax=new_fig(12,7.0); ax.plot(t,lr*1e4,color=C.INK); ax.set(xlim=(0,1150),ylim=(0,3.3),xlabel='步数 $t$',ylabel=r'学习率（$10^{-4}$）'); ax.set_xticks(np.arange(0,1001,200))
for ti,val,off in [(50,1.5,(5,8)),(600,1.65,(5,8)),(1100,.3,(-45,18))]:
    ax.scatter([ti],[val],s=34,facecolors=C.PAPER,edgecolors=C.INK,zorder=5); label(ax, f'{val:g}', (ti,val), offset=off)
label(ax,'预热', (50,1.5), offset=(5,-17), color=C.GRAY); label(ax,'余弦衰减',(760,1.0),offset=(5,8),color=C.GRAY)
save(fig,'M1-n7')

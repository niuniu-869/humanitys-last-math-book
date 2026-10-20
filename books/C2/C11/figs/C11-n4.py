import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(10, 6.5); x=np.linspace(0,np.pi/2,500); f=np.sin(x)/(np.sin(x)+np.cos(x)); g=1-f
ax.plot(x,f,color=C.INK,lw=1.8); ax.plot(x,g,color=C.INK,ls='--',lw=1.5); ax.axhline(1,color=C.INK,ls=':',lw=1.1); ax.fill_between(x,0,f,color=C.LIGHT)
ax.axvline(np.pi/4,color=C.INK,ls='-.',lw=1); ax.scatter([np.pi/4],[.5],s=36,facecolors=C.PAPER,edgecolors=C.INK,zorder=5)
label(ax,'$I$ 的被积函数（实线）',(0.35,.27)); label(ax,'伙伴 $J$ 的被积函数（虚线）',(0.12,.93)); label(ax,'两者相加 = 1',(1.12,1.03)); label(ax,'对称轴',(np.pi/4,1.08),ha='center'); label(ax,'$I$',(.64,.08),ha='center')
ax.set(xlim=(-.04,np.pi/2+.04),ylim=(-.05,1.14),xticks=[0,np.pi/4,np.pi/2],xticklabels=['0',r'$\frac{\pi}{4}$',r'$\frac{\pi}{2}$'],yticks=[0,.5,1]); ax.set_aspect('auto'); ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False); save(fig,'C11-n4')

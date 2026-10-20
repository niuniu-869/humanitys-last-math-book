import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Arc

x=np.deg2rad(100); t=np.tan(x/2); P=(np.cos(x),np.sin(x)); fig, ax=new_fig(8,7); th=np.linspace(0,2*np.pi,500); ax.plot(np.cos(th),np.sin(th),color=C.INK); ax.axhline(0,color=C.INK,lw=.9); ax.axvline(0,color=C.INK,lw=.9)
ax.plot([-1,P[0]],[0,P[1]],color=C.INK,lw=2.2); ax.plot([0,P[0]],[0,P[1]],color=C.INK); ax.plot([-1,0],[0,0],color=C.INK); ax.scatter([-1,1,0],[0,0,0],s=34,facecolors=C.PAPER,edgecolors=C.INK,zorder=4); ax.scatter([P[0]],[P[1]],s=34,color=C.INK,zorder=5)
ax.add_patch(Arc((0,0),.42,.42,angle=0,theta1=0,theta2=100,color=C.INK)); ax.add_patch(Arc((-1,0),.45,.45,angle=0,theta1=0,theta2=50,color=C.INK)); label(ax,'$x$',(.23,.18)); label(ax,r'$\frac{x}{2}$',(-.79,.18)); label(ax,r'斜率 $t=\tan\frac{x}{2}$',(-.93,.40),ha='center'); label(ax,r'$(\cos x,\sin x)$',(.03,1.05)); label(ax,'A',(-1,0),offset=(-10,7)); label(ax,'B',(1,0),offset=(5,7)); label(ax,'O',(0,0),offset=(5,-12)); label(ax,'P',P,offset=(5,2)); label(ax,'1',(-.52,.02),fontsize=8); label(ax,'1',(-.02,.52),fontsize=8)
ax.set(xlim=(-1.35,1.35),ylim=(-.25,1.25),aspect='equal'); ax.axis('off'); save(fig,'C11-n6')

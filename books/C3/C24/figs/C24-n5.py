import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.transforms import ScaledTranslation

fig, ax = new_fig(15, 13)
t = np.linspace(0,2*np.pi,721)
for r,ls,lw in [(1,'--',1),(np.sqrt(2),'-',1.5),(2,'--',1)]:
    ax.plot(r*np.cos(t),r*np.sin(t),color=C.INK,ls=ls,lw=lw)
u = np.array([-.8,2.8])
ax.plot(u,2-u,color=C.INK,lw=2.1,ls='-')
dot(ax,(1,1))
label(ax,r'$(1,1)$',(1,1),(-12,5),ha='right')
for length,ls,lw in [(2,'-',1.7),(1,'--',1.6)]:
    shift = 0 if length == 2 else 4/72
    coords = ax.transData + ScaledTranslation(shift,-shift,fig.dpi_scale_trans)
    ax.annotate('',xy=(1+length,1+length),xytext=(1,1),
                xycoords=coords, textcoords=coords,
                arrowprops=dict(arrowstyle='-|>',color=C.INK,lw=lw,ls=ls,
                                shrinkA=0,shrinkB=0,mutation_scale=12),zorder=4)
label(ax,r'$\nabla f=(2,2)$',(3,3),(-6,9),ha='right')
label(ax,r'$\nabla g=(1,1)$',(2,2),(15,-7))
label(ax,r'$x+y=2$',(2.5,-.5),(8,-3))
label(ax,'$r=1$',(0,-.7),ha='center')
for p,txt in [((0,-np.sqrt(2)),r'$r=\sqrt{2}$'),((-2,0),'$r=2$')]:
    label(ax,txt,p,(-6,-10),ha='right',fontsize=9)
ax.scatter([0,2],[2,0],marker='s',s=28,facecolor=C.PAPER,edgecolor=C.INK,zorder=5)
ax.axhline(0,color=C.GRAY,ls=':',lw=.7); ax.axvline(0,color=C.GRAY,ls=':',lw=.7)
ax.text(.5,-.2,r'$r=1$：不相交；$r=2$：相交于两点（方块）',transform=ax.transAxes,ha='center',fontsize=9)
ax.set(xlim=(-2.65,3.75),ylim=(-2.3,3.65),xlabel='$x$',ylabel='$y$')
ax.set_aspect('equal')
fig.subplots_adjust(left=.1,right=.96,bottom=.23,top=.96)
save(fig, "C24-n5")

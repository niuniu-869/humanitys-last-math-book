import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(15, 10)
x = np.linspace(-1.8,1.8,501)
# g=y-x^2/2=0; f=1.8*(y+x^2/4). Gradient display scale is .75.
for c in [-.5,0,.65]:
    ax.plot(x,c-x*x/4,color=C.AMBER,ls=':',lw=1.4)
ax.plot(x,x*x/2,color=C.INK,lw=1.8,ls='-')
ax.plot([-1.8,1.8],[0,0],color=C.INK,ls='--',lw=1)
dot(ax,(0,0),r'$P_0$',offset=(7,-17))
arrow(ax,(0,0),(0,1.35),color=C.INK,lw=1.7)
arrow(ax,(0,0),(0,.75),color=C.INK,lw=1.5)
label(ax,r'$\nabla g$',(0,.75),(9,0),va='center')
label(ax,r'$\nabla f$',(0,1.35),(-9,0),ha='right',va='center')
for start,end in [(-1.2,-.8),(.8,1.2)]:
    dot(ax,(start,start*start/2),size=16)
    xx = np.linspace(start,end,41)
    ax.plot(xx,xx*xx/2+.065,color=C.INK,ls=':',lw=1.4)
    ax.annotate('',xy=(end,end*end/2+.065),xytext=(xx[-5],xx[-5]**2/2+.065),
                arrowprops=dict(arrowstyle='->',color=C.INK,lw=1.2,ls=':'))
label(ax,'沿曲线走',(-1.08,.64),(-12,19),ha='center',fontsize=9)
label(ax,'沿曲线走',(1.08,.64),(12,19),ha='center',fontsize=9)
label(ax,r'$g=c$',(1.65,1.65**2/2),(6,0))
label(ax,'切线',(1.65,0),(5,8))
label(ax,r'$f$ 的等高线',(-1.55,-.5-1.55**2/4),(0,-17),fontsize=9)
ax.set(xlim=(-2,2.1),ylim=(-1.65,1.95))
ax.set_aspect('equal'); ax.set_axis_off()
fig.subplots_adjust(left=.04,right=.96,bottom=.04,top=.97)
save(fig, "C24-n7")

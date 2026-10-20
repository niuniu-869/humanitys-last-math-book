import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.transforms import ScaledTranslation

fig, ax = new_fig(15, 13)
t = np.linspace(0,2*np.pi,721)
q = np.sqrt(.5)
ax.plot(np.cos(t),np.sin(t),color=C.INK,lw=2,ls='-',label='单位圆')
# In rotated coordinates u=(x+y)/sqrt(2), v=(x-y)/sqrt(2), f=3u^2+v^2.
for level,ls in [(1,'--'),(3,':')]:
    u = np.sqrt(level/3)*np.cos(t)
    v = np.sqrt(level)*np.sin(t)
    x,y = (u+v)*q,(u-v)*q
    assert np.allclose(2*x*x+2*x*y+2*y*y,level)
    ax.plot(x,y,color=C.INK,lw=1.4,ls=ls,label=f'$f={level}$')
for p,val,off in [((q,q),3,(15,-14)),((-q,-q),3,(-35,-15)),
                  ((q,-q),1,(13,-13)),((-q,q),1,(-36,9))]:
    dot(ax,p)
    label(ax,f'$f={val}$',p,off)
    assert np.isclose(2*p[0]**2+2*p[0]*p[1]+2*p[1]**2,val)
# Display both collinear vectors at the same common scale, with labels on opposite sides.
p = np.array([q,q])
scale = .2
for v,ls in [(6*p,'-'),(2*p,'--')]:
    shift = 0 if ls == '-' else 4/72
    coords = ax.transData + ScaledTranslation(shift,-shift,fig.dpi_scale_trans)
    ax.annotate('',xy=p+scale*v,xytext=p,
                xycoords=coords,textcoords=coords,
                arrowprops=dict(arrowstyle='-|>',color=C.INK,lw=1.6,ls=ls,
                                shrinkA=0,shrinkB=0,mutation_scale=12),zorder=4)
label(ax,r'$\nabla f$',p+scale*6*p,(-5,10),ha='right')
label(ax,r'$\boldsymbol{n}$',p+scale*2*p,(14,-8))
ax.text(.5,-.2,'梯度与外法向量按同一比例缩短',transform=ax.transAxes,ha='center',fontsize=9)
ax.set(xlim=(-1.7,1.95),ylim=(-1.6,1.95),xlabel='$x$',ylabel='$y$')
ax.set_aspect('equal')
ax.legend(loc='upper left',fontsize=9)
ax.set_xticks([-1,0,1]); ax.set_yticks([-1,0,1])
fig.subplots_adjust(left=.1,right=.97,bottom=.23,top=.97)
save(fig, "C24-n6")

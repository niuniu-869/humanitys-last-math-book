import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(15, 10)
ax.fill([0,3,3,0],[0,0,2,2],facecolor=C.LIGHT,edgecolor=C.INK,lw=1.5)
points = [(0,0),(0,2),(3,0),(3,2),(2,2)]
values = [0,4,9,1,0]
offsets = [(-10,-24),(-10,12),(10,-24),(10,12),(0,12)]
for p,v,offset in zip(points,values,offsets):
    assert p[0]**2-2*p[0]*p[1]+2*p[1] == v
    dot(ax,p)
    label(ax, f'$({p[0]},{p[1]})$\n$f={v}$',p,offset,ha='center',fontsize=9)
ax.scatter([1],[1],s=36,facecolors=C.PAPER,edgecolors=C.INK,zorder=5)
label(ax,r'$(1,1),\ f=1$',(1,1),(10,0),va='center')
ax.text(.98,.98,'最大值 9，最小值 0',transform=ax.transAxes,ha='right',va='top')
ax.set(xlim=(-.65,3.7),ylim=(-.65,2.85),xlabel='$x$',ylabel='$y$')
ax.set_xticks([0,1,2,3]); ax.set_yticks([0,1,2])
ax.set_aspect('equal')
fig.subplots_adjust(left=.1,right=.97,bottom=.14,top=.97)
save(fig, "C24-n3")

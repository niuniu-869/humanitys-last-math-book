import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

points = {w:np.array(p) for w,p in {'国王':(.9,2.1),'女王':(-1.1,1.9),'男人':(1,.1),
          '女人':(-1,0),'王子':(.8,1.2),'公主':(-.9,1.1),'苹果':(.1,-1.5)}.items()}
q = points['国王']-points['男人']+points['女人']
assert np.allclose(q,[-1.1,2])
fig, ax = new_fig(15, 15)
for a,b in [('男人','国王'),('女人','女王')]:
    arrow(ax,points[a],points[b]-points[a],color=C.INK,lw=1.3)
for a,b in [('男人','女人'),('国王','女王')]:
    ax.plot(*np.stack([points[a],points[b]]).T,ls='--',color=C.INK,lw=1)
for w,point in points.items():
    offsets = {'女王':(-32,-12), '王子':(-35,7), '女人':(-32,-17)}
    dot(ax,point,w,offset=offsets.get(w,(8,-3)))
ax.scatter(*q,marker='s',s=55,facecolors=C.PAPER,edgecolors=C.INK,zorder=6)
label(ax,r'$\boldsymbol{q}=$ 国王 − 男人 + 女人',q,(-22,28),fontsize=9)
cos = lambda a,b: np.dot(a,b)/np.linalg.norm(a)/np.linalg.norm(b)
ax.text(.5,-.09,rf'cos($\boldsymbol{{q}}$, 女王)$={cos(q,points["女王"]):.4f}$',transform=ax.transAxes,ha='center')
ax.text(.5,-.15,rf'cos($\boldsymbol{{q}}$, 公主)$={cos(q,points["公主"]):.4f}$',transform=ax.transAxes,ha='center')
ax.axhline(0,color=C.GRAY,lw=.6,ls=':'); ax.axvline(0,color=C.GRAY,lw=.6,ls=':')
ax.set(xlim=(-1.8,1.65),ylim=(-1.85,2.85),aspect='equal')
ax.set_xticks([-1,0,1]); ax.set_yticks([-1,0,1,2])
save(fig, "M9-n6")

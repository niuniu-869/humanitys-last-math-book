import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle, FancyArrowPatch

fig, ax = new_fig(16, 8)
ax.set(xlim=(0,16), ylim=(0,8)); ax.axis('off')
def box(x,y,w,h,text,fill=C.PAPER, lw=1.1):
    ax.add_patch(Rectangle((x,y),w,h,facecolor=fill,edgecolor=C.INK,lw=lw)); label(ax,text,(x+w/2,y+h/2),ha='center',va='center',fontsize=9)
def conn(a,b): ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=11,color=C.INK,lw=1.1))
box(6.25,6.6,3.5,.7,'1000 人',lw=1.5)
box(2.0,4.7,3.5,.75,'有病 10 人'); box(10.5,4.7,3.5,.75,'没病 990 人'); conn((7.1,6.6),(3.75,5.45)); conn((8.9,6.6),(12.25,5.45))
box(.6,2.35,3.2,.75,'阳性 9',fill=C.LIGHT); box(4.3,2.35,3.2,.75,'阴性 1'); conn((3.75,4.7),(2.2,3.1)); conn((3.75,4.7),(5.9,3.1))
box(8.7,2.35,3.5,.75,'阳性约 89',fill=C.LIGHT); box(12.7,2.35,3.0,.75,'阴性约 901'); conn((12.25,4.7),(10.45,3.1)); conn((12.25,4.7),(14.2,3.1))
label(ax,'阳性共约 98 人，其中有病 9 人，约占 9.2%',(8,0.82),ha='center',fontsize=9)
ax.plot([.8,15.2],[1.35,1.35],color=C.INK,lw=1.0); ax.plot([.8,.8],[1.35,1.55],color=C.INK,lw=1.0); ax.plot([15.2,15.2],[1.35,1.55],color=C.INK,lw=1.0)
save(fig, 'K14-n5')

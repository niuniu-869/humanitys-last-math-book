import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle

levels = [[()]]
for row in range(4):
    levels.append([p+(c,) for p in levels[-1] for c in range(1,5)
                   if all(c != old and abs(c-old) != row-i for i,old in enumerate(p))])
assert list(map(len,levels)) == [1,4,6,4,2]
assert levels[-1] == [(2,4,1,3),(3,1,4,2)]
xs = {():5.5, (1,):1, (2,):4, (3,):7, (4,):10,
      (1,3):0, (1,4):2, (2,4):4, (3,1):7, (4,1):9, (4,2):11,
      (1,4,2):2, (2,4,1):4, (3,1,4):7, (4,1,3):9,
      (2,4,1,3):4, (3,1,4,2):7}
fig, ax = new_fig(19, 11)
for depth, nodes in enumerate(levels):
    for p in nodes:
        x,y = xs[p], 7-depth*1.6
        if p:
            ax.plot([xs[p[:-1]],x], [7-(depth-1)*1.6-.22,y+(.36 if depth == 4 else .24)], color=C.INK, lw=1, zorder=1)
        text = "根" if not p else "("+",".join(map(str,p))+")"
        if depth == 4:
            for w,h in [(1.9,.58),(2.04,.72)]:
                ax.add_patch(Rectangle((x-w/2,y-h/2),w,h,facecolor=C.PAPER,edgecolor=C.INK,fill=False,lw=1))
            label(ax,"解",(x,y-.8),ha="center",fontsize=10)
        label(ax,text,(x,y),ha="center",va="center",fontsize=10)
        if depth in (2,3) and not any(q[:-1] == p for q in levels[depth+1]):
            ax.plot([x-.09,x+.09],[y-.43,y-.61],color=C.INK,lw=1.5)
            ax.plot([x-.09,x+.09],[y-.61,y-.43],color=C.INK,lw=1.5)
            label(ax,f"第 {depth+1} 行\n无处可放",(x,y-.79),ha="center",va="top",fontsize=8)
ax.set(xlim=(-.9,11.9), ylim=(-.5,7.6))
ax.axis("off")
save(fig, "K33-n5")

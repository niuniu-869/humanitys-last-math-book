import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch, FancyArrowPatch

fig, ax = new_fig(10, 8)
for i in range(5): ax.plot([i, i], [0, 3], color=C.GRAY, lw=0.8)
for j in range(4): ax.plot([0, 4], [j, j], color=C.GRAY, lw=0.8)
path = [(0,0),(1,0),(2,0),(2,1),(3,1),(3,2),(4,2),(4,3)]
for a,b in zip(path[:-1], path[1:]): ax.plot([a[0],b[0]], [a[1],b[1]], color=C.INK, lw=2.8)
letters = ["R","R","U","R","U","R","U"]
for (a,b), t in zip(zip(path[:-1],path[1:]), letters):
    mx,my=(a[0]+b[0])/2,(a[1]+b[1])/2
    if a[1]==b[1]: label(ax,t,(mx,my),offset=(0,-13),ha="center")
    else: label(ax,t,(mx,my),offset=(-10,0),ha="center",va="center")
dot(ax,(0,0),"O(0,0)",offset=(-40,-14),size=30); dot(ax,(4,3),"B(4,3)",offset=(5,4),size=30)
ax.scatter([2],[1],s=70,facecolors=C.PAPER,edgecolors=C.INK,linewidths=1.6,zorder=5); label(ax,"P(2,1)",(2,1),offset=(-8,6),ha="right")
ax.text(2,-0.95,"实线路线 = RRURURU",ha="center")
ax.text(2,-1.45,r"$O\to P$：2 个 R、1 个 U，$\mathrm{C}_3^1=3$ 条",ha="center")
ax.text(2,-1.95,r"$P\to B$：2 个 R、2 个 U，$\mathrm{C}_4^2=6$ 条",ha="center")
ax.set_aspect("equal"); ax.set_xlim(-0.9,4.9); ax.set_ylim(-2.3,3.5); ax.axis("off")
save(fig, "Z5-n4")

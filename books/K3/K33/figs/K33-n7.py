import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Circle, FancyArrowPatch

pos = {"A":(0,3), "B":(3,3), "C":(6,3), "D":(0,0), "E":(3,0), "F":(6,0)}
weights = {"AB":4,"AC":2,"BC":1,"BD":5,"CD":8,"CE":10,"DE":2,"DF":6,"EF":3}
distance, parent, order = {v:float("inf") for v in pos}, {}, []
distance["A"] = 0
while len(order) < len(pos):
    u = min((v for v in pos if v not in order), key=lambda v:distance[v])
    order.append(u)
    for edge,w in weights.items():
        if u in edge:
            v = edge.replace(u,"")
            if distance[u]+w < distance[v]:
                distance[v],parent[v] = distance[u]+w,u
tree = {"".join(sorted(v+p)) for v,p in parent.items()}
assert order == list("ACBDEF")
assert [distance[v] for v in order] == [0,2,3,8,10,13]
assert tree == {"AC","BC","BD","DE","EF"}
assert sum(weights[e] for e in tree) == 13
fig, ax = new_fig(16, 10)
weight_pos = {"AB":(1.5,3.18), "AC":(3,4.4), "BC":(4.5,3.18), "BD":(1.32,1.62),
              "CD":(3.13,1.9), "CE":(4.75,1.4), "DE":(1.5,.17), "DF":(3,-1.43), "EF":(4.5,.17)}
for edge,w in weights.items():
    a,b = edge
    rad = -.38 if edge == "AC" else .38 if edge == "DF" else 0
    ax.add_patch(FancyArrowPatch(pos[a],pos[b],connectionstyle=f"arc3,rad={rad}",arrowstyle="-",
        shrinkA=12,shrinkB=12,color=C.INK,lw=2.3 if edge in tree else 1.1,
        ls="-" if edge in tree else "--",zorder=1))
    label(ax,str(w),weight_pos[edge],ha="center",va="center",fontsize=10)
for v,(x,y) in pos.items():
    ax.add_patch(Circle((x,y),.24,facecolor=C.PAPER,edgecolor=C.INK,zorder=3))
    label(ax,v,(x,y),ha="center",va="center",fontsize=12)
    label(ax,f"{order.index(v)+1}: ({distance[v]})",(x,y+(.48 if y else -.58)),ha="center",fontsize=9)
ax.set(xlim=(-.8,6.8),ylim=(-1.75,4.75),aspect="equal")
ax.axis("off")
save(fig, "K33-n7")

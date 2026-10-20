import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Circle
from collections import deque

edges = ["AB", "AC", "BC", "BD", "CD", "CE", "DE", "DF", "EF"]
adj = {v:sorted(b if a == v else a for a,b in edges if v in (a,b)) for v in "ABCDEF"}
queue, distance, order, tree = deque("E"), {"E":0}, [], set()
while queue:
    u = queue.popleft()
    order.append(u)
    for v in adj[u]:
        if v not in distance:
            distance[v] = distance[u]+1
            tree.add("".join(sorted(u+v)))
            queue.append(v)
assert order == list("ECDFAB")
assert tree == {"CE", "DE", "EF", "AC", "BC"}
pos = {"E":(3,4), "C":(0,2), "D":(3,2), "F":(6,2), "A":(0,0), "B":(3,0)}
fig, ax = new_fig(16, 10)
for edge in edges:
    ax.plot(*zip(*(pos[v] for v in edge)), color=C.INK,
            lw=2.3 if edge in tree else 1, ls="-" if edge in tree else "--", zorder=1)
for v,(x,y) in pos.items():
    ax.add_patch(Circle((x,y), .25, facecolor=C.PAPER, edgecolor=C.INK, zorder=3))
    label(ax, v, (x,y), ha="center", va="center", fontsize=12)
    label(ax, f"({distance[v]})", (x+.36,y+(.65 if v == "C" else .32)), fontsize=10)
    tx,ty,align = {"E":(x-.45,y+.36,"right"), "C":(x-.35,y-.5,"right"),
                   "D":(x+.4,y-.5,"left"), "F":(x+.4,y-.5,"left")}.get(v,(x,y-.52,"center"))
    label(ax, f"取出 {order.index(v)+1}", (tx,ty), ha=align, fontsize=9)
for level,y in enumerate([4,2,0]):
    label(ax, f"第 {level} 层", (-1.3,y), ha="center", va="center", fontsize=9)
ax.set(xlim=(-1.9,7.4), ylim=(-.9,4.8), aspect="equal")
ax.axis("off")
save(fig, "K33-n3")

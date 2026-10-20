import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Circle, FancyArrowPatch

pos = {"A":(0,3), "B":(3,3), "C":(6,3), "D":(0,0), "E":(3,0), "F":(6,0)}
edges = ["AB", "AC", "BC", "BD", "CD", "CE", "DE", "DF", "EF"]
adj = {v:sorted(b if a == v else a for a,b in edges if v in (a,b)) for v in pos}
order, tree = [], []
def visit(u):
    order.append(u)
    for v in adj[u]:
        if v not in order:
            tree.append((u,v))
            visit(v)
visit("E")
assert order == list("ECABDF")
fig, ax = new_fig(16, 10)
for edge in edges:
    directed = next(((a,b) for a,b in tree if set((a,b)) == set(edge)), None)
    a,b = directed or edge
    # The outer arcs avoid the middle vertices on each row.
    rad = -.38 if a+b == "AC" else .38 if a+b == "CA" else .38 if a+b == "DF" else 0
    ax.add_patch(FancyArrowPatch(pos[a],pos[b], connectionstyle=f"arc3,rad={rad}",
        arrowstyle="-|>" if directed else "-", mutation_scale=13, shrinkA=12, shrinkB=12,
        color=C.INK, lw=2.2 if directed else 1.2, ls="-" if directed else ":" if edge == "BC" else "--", zorder=1))
for v,(x,y) in pos.items():
    ax.add_patch(Circle((x,y), .24, facecolor=C.PAPER, edgecolor=C.INK, zorder=3))
    label(ax, v, (x,y), ha="center", va="center", fontsize=12)
    label(ax, f"进入 {order.index(v)+1}", (x,y+(.48 if y else -.58)), ha="center", fontsize=9)
label(ax, "已访问：环", (4.25,3.35), ha="center", fontsize=8)
ax.set(xlim=(-.8,6.8), ylim=(-1.5,4.5), aspect="equal")
ax.axis("off")
save(fig, "K33-n4")

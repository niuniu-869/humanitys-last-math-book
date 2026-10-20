import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Circle

fig, axes = new_fig(17, 10, ncols=2)
orders = [[5, 2, 8, 1, 9, 3], [1, 2, 3, 5, 8, 9]]
positions = [{5:(2.1,5), 2:(.9,3.1), 8:(3.4,3.1), 1:(.1,1.2), 3:(1.7,1.2), 9:(4.2,1.2)},
             {v:(.35+i*.7, 5-i*.95) for i,v in enumerate(orders[1])}]
for panel, (ax, order, pos) in enumerate(zip(axes, orders, positions)):
    children, depth, edges = {}, {}, []
    for v in order:
        children[v] = {}
        if not depth:
            depth[v] = 1
            continue
        p = order[0]
        while True:
            side = "left" if v < p else "right"
            if side not in children[p]:
                children[p][side] = v
                depth[v] = depth[p]+1
                edges.append((p,v))
                break
            p = children[p][side]
    assert sum(depth.values()) == [14,21][panel]
    for a,b in edges:
        ax.plot(*zip(pos[a],pos[b]), color=C.INK, lw=2.6 if panel == 0 and (a,b) in [(5,2),(2,3)] else 1, zorder=1)
    for v, (x,y) in pos.items():
        ax.add_patch(Circle((x,y), .24, facecolor=C.PAPER, edgecolor=C.INK, lw=1.2, zorder=3))
        label(ax, str(v), (x,y), ha="center", va="center", fontsize=11)
        label(ax, str(depth[v]), (x+.42,y+.18), fontsize=8, ha="left")
    if panel == 0:
        ax.add_patch(Circle(pos[3], .36, fill=False, edgecolor=C.INK, ls="--", lw=1.2))
    label(ax, "按 " + ",".join(map(str,order)) + " 插入", (2.1,5.95), ha="center", fontsize=10)
    label(ax, f"深度总和：{sum(depth.values())}", (2.1,-.6), ha="center", fontsize=9)
    ax.set(xlim=(-.5,4.9), ylim=(-1,6.3), aspect="equal")
    ax.axis("off")
fig.subplots_adjust(wspace=.15)
save(fig, "K33-n2")

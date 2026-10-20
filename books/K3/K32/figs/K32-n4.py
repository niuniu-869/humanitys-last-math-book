import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch

fig, ax = new_fig(13, 8)
nodes = {1:(3.5,4.8), 2:(2.0,3.25), 3:(5.0,3.25), 4:(1.25,1.7), 5:(2.75,1.7), 6:(5.0,1.7)}
vals = {1:9, 2:5, 3:8, 4:1, 5:2, 6:3}
for p, ch in [(1,2),(1,3),(2,4),(2,5),(3,6)]:
    ax.plot([nodes[p][0], nodes[ch][0]], [nodes[p][1]-.28, nodes[ch][1]+.28], color=C.INK, lw=1.2)
for i, (x,y) in nodes.items():
    ax.add_patch(Circle((x,y), .32, facecolor=C.PAPER, edgecolor=C.INK, lw=1.2))
    label(ax, str(vals[i]), (x,y), ha='center', va='center', fontsize=13)
    label(ax, str(i), (x+.38,y+.28), ha='left', va='bottom', fontsize=8)
label(ax, '最大堆', (3.5,5.55), ha='center', fontsize=11)

arr_y = .35
for i, v in enumerate([9,5,8,1,2,3], start=1):
    x = .75 + (i-1)*1.08
    ax.add_patch(Rectangle((x-.38, arr_y-.3), .76, .6, facecolor=C.PAPER, edgecolor=C.INK, lw=1.0))
    label(ax, str(v), (x, arr_y), ha='center', va='center', fontsize=11)
    label(ax, str(i), (x, arr_y-.53), ha='center', va='top', fontsize=8)
ax.set(xlim=(-.2, 6.8), ylim=(-.9, 6.0), aspect='equal')
ax.axis('off')
save(fig, 'K32-n4')

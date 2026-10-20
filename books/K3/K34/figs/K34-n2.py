import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle
from math import comb

values = np.array([[1, 1, 1, 1], [1, 2, 3, 4], [1, 3, 6, 10], [1, 4, 10, 20]])
assert values[1, 2] == 3 and values[2, 1] == 3 and values[2, 2] == 6 and values[3, 3] == 20
assert values[3, 3] == comb(6, 3)
for i in range(1, 4):
    for j in range(1, 4):
        assert values[i, j] == values[i-1, j] + values[i, j-1]
fig, ax = new_fig(13, 10)
x0, y0, cell = 1.0, 0.0, 1.15
for j in range(4):
    label(ax, str(j+1), (x0 + j*cell + cell/2, y0 + 4.9), ha="center", va="center", fontsize=10)
for i in range(4):
    label(ax, str(i+1), (x0 - .38, y0 + (3-i)*cell + cell/2), ha="center", va="center", fontsize=10)
for i in range(4):
    for j in range(4):
        lw = 2.4 if (i, j) == (3, 3) else 1.0
        ax.add_patch(Rectangle((x0+j*cell, y0+(3-i)*cell), cell, cell,
                               facecolor=C.PAPER, edgecolor=C.INK, lw=lw))
        label(ax, str(values[i, j]), (x0+j*cell+cell/2, y0+(3-i)*cell+cell/2),
              ha="center", va="center", fontsize=12)
label(ax, "起点", (x0 + cell/2, y0 + 3.65), ha="center", va="center", fontsize=8)
label(ax, "终点", (x0 + 4*cell + .08, y0 + cell/2), offset=(4, 0), va="center", fontsize=9)
target = (x0 + 2*cell + cell/2, y0 + cell + cell/2)
arrow(ax, (target[0], target[1]+cell-.25), (0, -cell+.5), color=C.INK, lw=1.2)
arrow(ax, (target[0]-cell+.25, target[1]), (cell-.5, 0), color=C.INK, lw=1.2)
label(ax, "3+3=6", (target[0], target[1]-.36), ha="center", va="center", fontsize=8)
ax.set(xlim=(.15, 6.4), ylim=(-.3, 5.2), aspect="equal")
ax.axis("off")
save(fig, "K34-n2")

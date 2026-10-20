import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle, FancyArrowPatch
from matplotlib.path import Path

table = np.array([
    [0,0,0,0,0,0,0,0,0],
    [0,0,3,3,3,3,3,3,3],
    [0,0,3,4,4,7,7,7,7],
    [0,0,3,4,5,7,8,9,9],
    [0,0,3,4,5,8,8,11,12],
])
assert table.shape == (5, 9) and table[4, 8] == 12
assert table[3, 3] == table[2, 3] == 4 and table[2, 3] != table[1, 3]
weights, values = [2,3,4,5], [3,4,5,8]
computed = np.zeros((5,9), dtype=int)
for i, (w,v) in enumerate(zip(weights,values), 1):
    for c in range(9):
        computed[i,c] = max(computed[i-1,c], computed[i-1,c-w]+v if c >= w else 0)
assert np.array_equal(computed, table)
chosen, c = [], 8
for i in range(4,0,-1):
    if table[i,c] != table[i-1,c]:
        chosen.append(i)
        c -= weights[i-1]
assert chosen == [4,2] and c == 0
assert sum(weights[i-1] for i in chosen) == 8
assert sum(values[i-1] for i in chosen) == 12
fig, ax = new_fig(18, 11)
x0, y0, cell = 1.1, .2, 1.0

def cx(c):
    return x0 + (c + .5) * cell

def cy(i):
    return y0 + (4 - i + .5) * cell

for c in range(9):
    label(ax, str(c), (cx(c), y0 + 5*cell + .35), ha="center", va="center", fontsize=9)
label(ax, "$c$", (x0-.3, y0+5*cell+.35), ha="center", va="center")
label(ax, "$i$", (x0-.7, y0+4.8), ha="center", va="center")
for i in range(5):
    label(ax, str(i), (x0-.3, cy(i)), ha="center", va="center", fontsize=9)
for i in range(5):
    for c in range(9):
        ax.add_patch(Rectangle((x0+c*cell, y0+(4-i)*cell), cell, cell,
                               facecolor=C.PAPER, edgecolor=C.INK, lw=1.0))
        label(ax, str(table[i, c]), (cx(c), cy(i)),
              ha="center", va="center", fontsize=10)
for i, text in [(1, "1 (2,3)"), (2, "2 (3,4)"), (3, "3 (4,5)"), (4, "4 (5,8)")]:
    label(ax, text, (x0+9*cell+.2, cy(i)), va="center", fontsize=9)
label(ax, "物品 (w,v)", (x0+9*cell+.2, y0+4.7), va="center", fontsize=9)

# 回头读的路径：五个粗框格子，包含容量已为 0 时的 (1,0) 与 (0,0)。
path = [(4,8), (3,3), (2,3), (1,0), (0,0)]
for i, c in path:
    ax.add_patch(Rectangle((x0+c*cell, y0+(4-i)*cell), cell, cell,
                           fill=False, edgecolor=C.INK, lw=2.4, zorder=4))

def path_arrow(start, end, lw):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=10,
                                 color=C.INK, lw=lw, shrinkA=0, shrinkB=0, zorder=5))

def jump_arrow(start, bend, tip, lw=2.0):
    """斜跳箭头：先从起点格的边水平穿过数字上方的空白，再弯入目标格。"""
    p = Path([start, bend, tip], [Path.MOVETO, Path.CURVE3, Path.CURVE3])
    ax.add_patch(FancyArrowPatch(path=p, arrowstyle="-|>", mutation_scale=10,
                                 color=C.INK, lw=lw, shrinkA=0, shrinkB=0, zorder=5,
                                 capstyle="round", joinstyle="round"))

# (4,8) -> (3,3)：从 12 格的左边出发，沿第 4 行数字上方的空白向左，
# 再经曲线从下方进入 4 格，避开 (3,4) 里的 5 和 (3,5) 里的 7。
jump_arrow((x0+8*cell+.02, y0+.84), (x0+4.50*cell, y0+.84),
           (x0+3.80*cell, y0+1.40), 2.0)
# (3,3) -> (2,3)：竖直向上，只跳过物品 3。
path_arrow((x0+3*cell+.15, y0+1.30), (x0+3*cell+.15, y0+2.65), 1.0)
# (2,3) -> (1,0)：从 4 格的左边沿第 2 行数字上方的空白向左，
# 再弯入 0 格，避开 (2,2) 里的 3 和 (2,1) 里的 0。
jump_arrow((x0+3*cell+.02, y0+2.84), (x0+1.50*cell, y0+2.84),
           (x0+.80*cell, y0+3.40), 2.0)
# (1,0) -> (0,0)：容量已为 0，继续竖直到第 0 行。
path_arrow((x0+.20, y0+3.25), (x0+.20, y0+4.35), 1.0)

# 标签放在各自格子内数字下方的空白处，避开数字与箭头。
label(ax, "选 4，−5", (x0+6.50*cell, y0+.176), ha="center", va="center", fontsize=7.5)
label(ax, "没选 3", (x0+3.58*cell, y0+2.176), ha="center", va="center", fontsize=7.5)
label(ax, "选 2，−3", (x0+1.50*cell, y0+2.176), ha="center", va="center", fontsize=7.5)
ax.set(xlim=(0, 11.6), ylim=(-.1, 5.9), aspect="equal")
ax.axis("off")
save(fig, "K34-n3")

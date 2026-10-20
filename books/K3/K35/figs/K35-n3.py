import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle, FancyArrowPatch

x, y = 'kitten', 'sitting'
table = np.zeros((len(x)+1, len(y)+1), dtype=int)
table[:, 0] = np.arange(len(x)+1)
table[0, :] = np.arange(len(y)+1)
for i in range(1, len(x)+1):
    for j in range(1, len(y)+1):
        table[i, j] = min(table[i-1, j]+1, table[i, j-1]+1,
                          table[i-1, j-1]+int(x[i-1] != y[j-1]))
expected = [[0,1,2,3,4,5,6,7], [1,1,2,3,4,5,6,7], [2,2,1,2,3,4,5,6],
            [3,3,2,1,2,3,4,5], [4,4,3,2,1,2,3,4], [5,5,4,3,2,2,3,4], [6,6,5,4,3,3,2,3]]
assert table.tolist() == expected
path = [(6,7),(6,6),(5,5),(4,4),(3,3),(2,2),(1,1),(0,0)]
fig, ax = new_fig(18, 11)
for i in range(7):
    for j in range(8):
        active = (i,j) in path
        ax.add_patch(Rectangle((j-.5, -i-.5), 1, 1, facecolor=C.LIGHT if active else C.PAPER,
                               edgecolor=C.INK if active else C.GRAY, lw=2 if active else .65))
        label(ax, str(table[i,j]), (j, -i), ha='center', va='center', fontsize=12)
for j, char in enumerate(['空']+list(y)):
    label(ax, char, (j, .92), ha='center', va='center', fontsize=12)
for i, char in enumerate(['空']+list(x)):
    label(ax, char, (-.95, -i), ha='center', va='center', fontsize=12)
for (i,j), (a,b) in zip(path, path[1:]):
    shrink = 10 if i != a and j != b else 7
    ax.add_patch(FancyArrowPatch((j,-i), (b,-a), shrinkA=shrink, shrinkB=shrink,
        arrowstyle='-|>', mutation_scale=12, lw=1.8, color=C.INK, ls='-'))
notes = [(1, '(1,1)  k→s 替换'), (2, '(2,2)  保留 i'), (3, '(3,3)  保留 t'),
         (4, '(4,4)  保留 t'), (5, '(5,5)  e→i 替换'), (6, '(6,6)  保留 n')]
for row, text in notes:
    label(ax, text, (8.0, -row), ha='left', va='center', fontsize=10)
label(ax, '插入 g', (6.55, -6.95), ha='center', va='center', fontsize=10)
label(ax, '2 次替换 + 1 次插入 = 3', (3.5, -7.65), ha='center', va='center')
ax.set(xlim=(-1.45, 11.8), ylim=(-8.05, 1.4), aspect='equal')
ax.axis('off')
save(fig, 'K35-n3')

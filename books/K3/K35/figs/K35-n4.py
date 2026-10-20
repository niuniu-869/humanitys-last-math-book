import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle, FancyArrowPatch

x, y = 'ACGTTA', 'AGTCA'
table = np.zeros((7, 6), dtype=int)
for i in range(1, 7):
    for j in range(1, 6):
        table[i,j] = table[i-1,j-1]+1 if x[i-1] == y[j-1] else max(table[i-1,j], table[i,j-1])
assert table.tolist() == [[0,0,0,0,0,0],[0,1,1,1,1,1],[0,1,1,1,2,2],
                          [0,1,2,2,2,2],[0,1,2,3,3,3],[0,1,2,3,3,3],[0,1,2,3,3,4]]
path = [(6,5),(5,4),(4,4),(4,3),(3,2),(2,1),(1,1),(0,0)]
collected = [x[i-1] for (i,j),(a,b) in zip(path,path[1:]) if (i-a,j-b)==(1,1)]
assert ''.join(reversed(collected)) == 'AGTA'
assert table[4,4] == table[5,3] == 3
fig, ax = new_fig(17, 12)
for i in range(7):
    for j in range(6):
        active = (i,j) in path
        ax.add_patch(Rectangle((j-.5,-i-.5),1,1,facecolor=C.LIGHT if active else C.PAPER,
                               edgecolor=C.INK if active else C.GRAY,lw=2 if active else .65))
        label(ax,str(table[i,j]),(j,-i),ha='center',va='center',fontsize=12)
for j,char in enumerate(['空']+list(y)):
    label(ax,char,(j,.92),ha='center',va='center',fontsize=12)
for i,char in enumerate(['空']+list(x)):
    label(ax,char,(-.95,-i),ha='center',va='center',fontsize=12)
for (i,j),(a,b) in zip(path,path[1:]):
    diagonal = (i-a,j-b)==(1,1)
    shrink = 10 if diagonal else 7
    ax.add_patch(FancyArrowPatch((j,-i),(b,-a),shrinkA=shrink,shrinkB=shrink,
        arrowstyle='-|>',mutation_scale=12,lw=1.8 if diagonal else 1.3,
        color=C.INK,ls='-' if diagonal else '--'))
for i,j,char in [(6,5,'A'),(4,3,'T'),(3,2,'G'),(1,1,'A')]:
    label(ax,f'({i},{j})  收下 {char}',(6.0,-i),ha='left',va='center',fontsize=10)
label(ax,'(5,4) 上方 3 = 左方 3\n并列，选上方',(6.0,-5),ha='left',va='center',fontsize=9)
label(ax,'倒读：AGTA',(2.5,-7.05),ha='center',va='center',fontsize=12)
ax.set(xlim=(-1.45,10.45),ylim=(-7.55,1.4),aspect='equal')
ax.axis('off')
save(fig, 'K35-n4')

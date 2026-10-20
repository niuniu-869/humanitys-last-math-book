import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle, FancyArrowPatch

p = [5,10,3,12,5]
M = np.zeros((5,5), dtype=int)
K = np.zeros_like(M)
for length in range(2,5):
    for i in range(1,6-length):
        j = i+length-1
        M[i,j], K[i,j] = min((M[i,k]+M[k+1,j]+p[i-1]*p[k]*p[j], k) for k in range(i,j))
assert [M[1,2],M[2,3],M[3,4],M[1,3],M[2,4],M[1,4]] == [150,360,180,330,330,405]
assert [K[1,2],K[2,3],K[3,4],K[1,3],K[2,4],K[1,4]] == [1,2,3,2,2,2]
fig, ax = new_fig(15, 10)
for i in range(1,5):
    for j in range(i,5):
        cx, cy = 1.7*(j-1), -1.25*(i-1)
        ax.add_patch(Rectangle((cx-.85,cy-.625),1.7,1.25,
            facecolor=C.LIGHT if (i,j)==(1,4) else C.PAPER,edgecolor=C.INK,lw=1))
        label(ax,str(M[i,j]),(cx,cy+.16 if i!=j else cy),ha='center',va='center',fontsize=13)
        if i!=j:
            label(ax,f'$(k={K[i,j]})$',(cx,cy-.29),ha='center',va='center',fontsize=10)
for j in range(1,5):
    label(ax,str(j),(1.7*(j-1),1.65),ha='center',va='center')
for i in range(1,5):
    label(ax,str(i),(-1.22,-1.25*(i-1)),ha='center',va='center')
label(ax,'$j$',(6.2,1.65),ha='center',va='center')
label(ax,'$i$',(-1.22,.9),ha='center',va='center')
# Dependency arrows travel outside the table so they never cross another entry.
for start,end,rad in [((1.7,.65),(5.1,.65),-.32),((5.98,-2.5),(5.98,0),.55)]:
    ax.add_patch(FancyArrowPatch(start,end,connectionstyle=f'arc3,rad={rad}',
        arrowstyle='-|>',mutation_scale=13,lw=1.6,ls='--',color=C.INK))
label(ax,r'$150+180+5\cdot3\cdot5=405$',(2.55,-4.85),ha='center',va='center',fontsize=12)
ax.set(xlim=(-1.7,7.15),ylim=(-5.25,2.15),aspect='equal')
ax.axis('off')
save(fig, 'K35-n5')

import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle

fig, axes = new_fig(15, 13, ncols=2)
for ax,full in zip(axes,[True,False]):
    for row in range(1,13):
        selected = full or row in [3,7,10]
        ax.add_patch(Rectangle((0,12-row),1,1,facecolor=C.LIGHT if selected else C.PAPER,edgecolor=C.INK,lw=1.8 if selected else .6,zorder=3 if selected else 1))
        ax.text(-.18,12.5-row,str(row),ha='right',va='center',fontsize=9)
        if not full and selected:
            ax.text(1.2,12.5-row,'真词' if row==3 else '负词',va='center',fontsize=9)
    ax.text(.5,12.5,r'$U_{\mathrm{out}}$',ha='center')
    ax.text(.5,-.6,r'$\vdots$',ha='center')
    ax.text(.5,-1.6,r'$O(Vd)$' if full else r'$O((K+1)d)$',ha='center')
    ax.set_title('完整 softmax' if full else '负采样（$K=2$）',pad=12)
    ax.set(xlim=(-1.4,2.6),ylim=(-2.1,13),aspect='equal'); ax.axis('off')
save(fig, "M9-n5")

import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Circle

n = 8
levels = [[(j+.5)*16/(2**i)-1 for j in range(2**i)] for i in range(4)]
work = [n // (2**i) for i in range(4)]
assert [len(xs)*w for xs, w in zip(levels, work)] == [8]*4
assert sum(len(xs)*w for xs, w in zip(levels, work)) == 32
fig, ax = new_fig(22, 10.5)
for i, xs in enumerate(levels[:-1]):
    for j, x in enumerate(xs):
        for child_x in levels[i+1][2*j:2*j+2]:
            ax.plot([x, child_x], [-2*i, -2*(i+1)], color=C.INK, lw=.9, ls='-')
for i, xs in enumerate(levels):
    for x in xs:
        ax.add_patch(Circle((x, -2*i), .4, facecolor=C.PAPER,
                            edgecolor=C.INK, lw=1, zorder=3))
        label(ax, str(work[i]), (x, -2*i), ha='center', va='center', fontsize=10)
    scale = ['$n=8$', '$n/2=4$', '$n/4=2$', '$n/8=1$'][i]
    label(ax, scale, (-1.4, -2*i), ha='right', va='center', fontsize=9)
    total = ['$8$', '$4+4=8$', r'$2\times4=8$', r'$1\times8=8$'][i]
    label(ax, f'第 {i} 层  '+total, (16, -2*i), va='center', fontsize=10)
label(ax, '规模', (-1.4, 1), ha='right', fontsize=9)
label(ax, '每层之和', (16, 1), fontsize=9)
ax.plot([15.9, 20.8], [-6.9, -6.9], color=C.INK, lw=.9)
label(ax, r'共 $8\times4=32$', (16, -7.65), va='center', fontsize=11)
ax.set(xlim=(-4.5, 21.4), ylim=(-8.2, 1.6), aspect='equal')
ax.axis('off')
fig.subplots_adjust(left=.02, right=.98, bottom=.02, top=.98)
save(fig, "K31-n3")

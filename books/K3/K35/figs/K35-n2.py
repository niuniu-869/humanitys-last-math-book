import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch

x, y = 'ACGTTA', 'AGTCA'
c = np.zeros((7, 6), dtype=int)
for i in range(1, 7):
    for j in range(1, 6):
        c[i,j] = c[i-1,j-1]+1 if x[i-1] == y[j-1] else max(c[i-1,j], c[i,j-1])
assert c[3:5,2:4].tolist() == [[2, 2], [2, 3]]

fig, axes = new_fig(18, 8, ncols=2)
for ax in axes:
    for r in range(2):
        for c in range(2):
            ax.add_patch(Rectangle((2*c, 2*r), 2, 2, facecolor=C.PAPER, edgecolor=C.GRAY, lw=1))
    ax.set(xlim=(-.8, 4.35), ylim=(-1.4, 4.8), aspect='equal')
    ax.axis('off')
ax = axes[0]
for text, xy in [('$c[i-1][j-1]$', (1, 3.5)), ('$c[i-1][j]$', (3, 3.5)),
                 ('$c[i][j-1]$', (1, 1.65)), ('$c[i][j]$', (3, 1))]:
    label(ax, text, xy, ha='center', va='center', fontsize=10)
ax.add_patch(Circle((3, 1), .78, facecolor='none', edgecolor=C.INK, lw=1.4))
for start, end, style, width in [((1, 3), (2.43, 1.60), '-', 2),
                                ((3, 3), (3, 1.82), '--', 1.3),
                                ((1, 1), (2.18, 1), '--', 1.3)]:
    ax.add_patch(FancyArrowPatch(start, end, shrinkA=0, shrinkB=0,
        arrowstyle='-|>', mutation_scale=12, color=C.INK, lw=width, ls=style))
label(ax, '$x_i=y_j$：加 1', (2, -.45), ha='center', va='center')
label(ax, r'$x_i\ne y_j$：取较大者', (2, -1.02), ha='center', va='center')
ax = axes[1]
for text, xy in [('$c[3][2]=2$', (1, 3.5)), ('$c[3][3]=2$', (3, 3.5)),
                 ('$c[4][2]=2$', (1, 1.65)), ('$c[4][3]=3$', (3, 1))]:
    label(ax, text, xy, ha='center', va='center', fontsize=10)
ax.add_patch(Circle((3, 1), .9, facecolor='none', edgecolor=C.INK, lw=1.4))
ax.add_patch(FancyArrowPatch((1, 3), (2.34, 1.66), shrinkA=0, shrinkB=0,
    arrowstyle='-|>', mutation_scale=12, color=C.INK, lw=2, ls='-'))
for text, xy in [('G', (1, 4.35)), ('T', (3, 4.35)), ('G', (-.4, 3)), ('T', (-.4, 1))]:
    label(ax, text, xy, ha='center', va='center', fontsize=11)
label(ax, '$T=T$', (2, -.45), ha='center', va='center')
label(ax, '$2+1=3$', (2, -1.02), ha='center', va='center', fontsize=12)
fig.subplots_adjust(wspace=.25)
save(fig, 'K35-n2')

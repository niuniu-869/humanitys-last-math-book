import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle, Circle

fig, axes = new_fig(18, 11, nrows=2, ncols=3)
titles = [r'$A\cup B$', r'$AB$', r'$\overline{A}$', r'$A-B$', r'$AB=\varnothing$', r'$A\subset B$']
notes = ['阴影 = $A$ 或 $B$ 至少有一个发生', '阴影 = $A$ 与 $B$ 同时发生',
         '阴影 = $A$ 不发生', '阴影 = $A$ 发生而 $B$ 不发生', '', '阴影 = $A$ 发生']
for k, ax in enumerate(axes.flat):
    ax.add_patch(Rectangle((0, 0), 4, 3, facecolor=C.PAPER, edgecolor=C.INK, lw=1.0))
    label(ax, r'$\Omega$', (3.72, 2.8), ha='right', va='top', fontsize=9)
    if k == 0:
        ax.add_patch(Circle((1.65, 1.55), .92, facecolor=C.LIGHT, edgecolor=C.INK, lw=1.2))
        ax.add_patch(Circle((2.35, 1.55), .92, facecolor=C.LIGHT, edgecolor=C.INK, lw=1.2))
        label(ax, '$A$', (1.25, 2.25), ha='center'); label(ax, '$B$', (2.75, 2.25), ha='center')
    elif k == 1:
        a = Circle((1.65, 1.55), .92, facecolor=C.PAPER, edgecolor=C.INK, lw=1.2)
        b = Circle((2.35, 1.55), .92, facecolor=C.PAPER, edgecolor=C.INK, lw=1.2)
        ax.add_patch(a); ax.add_patch(b)
        lens = Circle((1.65, 1.55), .92, facecolor=C.LIGHT, edgecolor='none')
        lens.set_clip_path(b); ax.add_patch(lens)
        label(ax, '$A$', (1.15, 2.25), ha='center'); label(ax, '$B$', (2.85, 2.25), ha='center')
    elif k == 2:
        ax.add_patch(Rectangle((0, 0), 4, 3, facecolor=C.LIGHT, edgecolor='none'))
        ax.add_patch(Circle((2, 1.5), .92, facecolor=C.PAPER, edgecolor=C.INK, lw=1.2))
        label(ax, '$A$', (2, 1.5), ha='center', va='center')
    elif k == 3:
        ax.add_patch(Circle((1.65, 1.55), .92, facecolor=C.LIGHT, edgecolor=C.INK, lw=1.2))
        ax.add_patch(Circle((2.35, 1.55), .92, facecolor=C.PAPER, edgecolor=C.INK, lw=1.2))
        label(ax, '$A$', (1.2, 2.25), ha='center'); label(ax, '$B$', (2.8, 2.25), ha='center')
    elif k == 4:
        ax.add_patch(Circle((1.3, 1.5), .68, facecolor=C.PAPER, edgecolor=C.INK, lw=1.2))
        ax.add_patch(Circle((2.7, 1.5), .68, facecolor=C.PAPER, edgecolor=C.INK, lw=1.2))
        label(ax, '$A$', (1.3, 1.5), ha='center', va='center'); label(ax, '$B$', (2.7, 1.5), ha='center', va='center')
    else:
        ax.add_patch(Circle((2, 1.5), 1.05, facecolor=C.PAPER, edgecolor=C.INK, lw=1.2))
        ax.add_patch(Circle((2, 1.5), .55, facecolor=C.LIGHT, edgecolor=C.INK, lw=1.2))
        label(ax, '$B$', (2, 2.55), ha='center'); label(ax, '$A$', (2, 1.5), ha='center', va='center')
    if k in (0, 1, 3):
        for cx in (1.65, 2.35):
            ax.add_patch(Circle((cx, 1.55), .92, fill=False, edgecolor=C.INK, lw=1.2))
    ax.add_patch(Rectangle((0, 0), 4, 3, fill=False, edgecolor=C.INK, lw=1))
    label(ax, titles[k] + ('（包含）' if k == 5 else ''), (2, -.15), ha='center', va='top', fontsize=11)
    if notes[k]: label(ax, notes[k], (2, -.85), ha='center', va='top', fontsize=7.2)
    elif k == 4: label(ax, '互斥', (2, -.85), ha='center', va='top', fontsize=8)
    ax.set(xlim=(-.15, 4.15), ylim=(-1.25, 3.15), aspect='equal'); ax.axis('off')
fig.subplots_adjust(wspace=.28, hspace=.35)
save(fig, 'P1-n2')

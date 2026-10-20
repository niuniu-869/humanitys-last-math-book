import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle

fig, ax = new_fig(17, 8.5)
fig.subplots_adjust(bottom=.24)
ax.set(xlim=(.3, 17), ylim=(0, 1.12), xticks=range(1, 17),
       yticks=[0, .25, .5, 1])
ax.set_yticklabels(['0', r'$\frac{1}{4}$', r'$\frac{1}{2}$', '1'])
ax.tick_params(axis='x', labelsize=8)
ax.bar([1], [1], width=1, facecolor=C.PAPER, edgecolor=C.INK, linewidth=1)
label(ax, '首项', (1, 1), (0, 8), ha='center', fontsize=9)
for k in range(1, 5):
    first, last = 2**(k-1)+1, 2**k
    ns = np.arange(first, last+1)
    ax.bar(ns, 1/ns, width=1, color=C.LIGHT if k % 2 else C.PAPER,
           edgecolor=C.INK, linewidth=1)
    # Hatching identifies the common lower rectangle without relying on gray.
    ax.add_patch(Rectangle((first-.5, 0), len(ns), 1/last,
                          facecolor='none', edgecolor=C.GRAY, hatch='///', lw=0))
    ax.plot([first-.5, last+.5], [1/last, 1/last], ls='--', color=C.INK, lw=1.7)
    ax.plot([first-.5, first-.5], [0, 1.04], ls='--', color=C.GRAY, lw=.8)
    label(ax, f'第 {k} 组', ((first+last)/2, 0), (0, -24),
          ha='center', va='top', fontsize=9)
    assert np.isclose(len(ns)/last, .5)
    assert np.sum(1/ns) >= .5
label(ax, r'每组面积 $\geq\frac{1}{2}$', (9.5, .83), ha='center')
label(ax, r'斜线矩形面积 $=\frac{1}{2}$', (9.5, .64), ha='center', fontsize=9)
label(ax, '$n$', (16.7, 0), (0, -17), ha='center')
save(fig, 'C14-n3')

import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle

fig, (ax, ex) = new_fig(17, 7.8, nrows=2)
for a in (ax, ex): a.axis('off')

def band(a, y, values, groups, labels, title=None):
    xs = np.arange(len(values))
    for k, val in enumerate(values):
        grp = groups[k]
        fc = C.LIGHT if grp == 0 else C.PAPER
        hatch = '///' if grp == 1 else None
        lw = 2.0 if grp == 3 else 1.0
        a.add_patch(Rectangle((k, y), 1, .72, facecolor=fc, edgecolor=C.INK,
                              lw=lw, hatch=hatch))
        label(a, str(val), (k + .5, y + .36), ha='center', va='center', fontsize=11)
    for start, end, text in labels:
        label(a, text, ((start + end) / 2, y + .93), ha='center', va='bottom', fontsize=9)
    if title: label(a, title, (-.3, y + .36), ha='right', va='center', fontsize=10)

def ptr(a, x, t, y0=.38):
    arrow(a, (x, y0), (0, .3), color=C.INK, lw=1.0)
    label(a, t, (x, y0 - .02), ha='center', va='top', fontsize=10)

band(ax, .8, ['≤ x', '> x', '未检查', '基准 x'], [0, 1, 2, 3], [], 'A[p..r]')
for x, t in [(.2, 'p'), (.8, 'i'), (2.15, 'j'), (3.5, 'r')]:
    ptr(ax, x, t, .74 - .0 if False else .45)
ax.set(xlim=(-1.2, 4.2), ylim=(-.2, 1.9))

band(ex, .8, [2, 5, 8, 1, 9, 3], [0, 1, 1, 2, 2, 3],
     [(0, 1, '≤ x'), (1, 3, '> x'), (3, 5, '未检查'), (5, 6, '基准 x=3')], '[2,5,8,1,9,3]')
for x, t in [(.2, 'p=1'), (.8, 'i=1'), (3.5, 'j=4'), (5.5, 'r=6')]:
    ptr(ex, x, t, .45)
ex.set(xlim=(-1.6, 6.4), ylim=(-.2, 2.1))
fig.subplots_adjust(hspace=.45)
save(fig, 'K32-n3')

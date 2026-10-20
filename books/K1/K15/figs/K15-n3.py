import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import FancyArrowPatch

fig, ax = new_fig(19, 10)
ax.set(xlim=(-.04, 1.05), ylim=(-4.6, 1.2)); ax.axis('off')
arrow(ax, (0, 0), (1.02, 0), color=C.INK, lw=1.1)
for x in [0, .25, .5, .75, 1]:
    ax.plot([x, x], [0, .09], color=C.INK, lw=1)
    label(ax, f'{x:g}', (x, .15), ha='center', va='bottom', fontsize=9)
dot(ax, (.5, 0), size=30)
ax.scatter([.7], [0], marker='s', s=32, color=C.INK, zorder=5)
arrow(ax, (.51, .02), (.18, 0), color=C.INK, lw=1.6)
label(ax, '读论据前 0.50', (.5, .65), ha='right', fontsize=9)
label(ax, '读论据后 0.70', (.7, .65), ha='left', fontsize=9)
for top, bottom in [(-.12, -.65), (-1.18, -1.55), (-2.08, -2.45), (-2.98, -3.35)]:
    ax.plot([.7, .7], [top, bottom], color=C.GRAY, ls=':', lw=1)
values = [.677, .62, .538, .318]
assert np.allclose(values, [2.1/3.1, .6*.7+.4*.5, (7/6)/(1+7/6), (7/15)/(1+7/15)], atol=.0005)
for y, x, text in zip([-.65, -1.55, -2.45, -3.35], values,
                      ['(a) 可能还有别的原因', '(d) 质疑论据',
                       '(b) 确有他因，只解释一部分', '(c) 直接对照']):
    ax.add_patch(FancyArrowPatch((.7, y), (x, y), arrowstyle='-|>', mutation_scale=10,
                               color=C.INK, ls='--', lw=2.2 if x == .318 else 1.3,
                               shrinkA=0, shrinkB=0))
    ax.scatter([x], [y], s=32, facecolors=C.PAPER, edgecolors=C.INK, zorder=5)
    label(ax, f'{text}  {x:.3f}', (x, y-.2), ha='center', va='top', fontsize=9)
label(ax, '相信会员制有效的程度', (.5, -4.4), ha='center')
save(fig, "K15-n3")

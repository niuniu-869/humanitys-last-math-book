import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

from matplotlib.patches import Circle, FancyArrowPatch, PathPatch
from matplotlib.path import Path

fig, (left, right) = new_fig(16, 6.8, ncols=2)
for ax in (left, right):
    ax.axis('off'); ax.set_aspect('equal')
def path(ax, xs, y=.9):
    for x1, x2 in zip(xs[:-1], xs[1:]):
        ax.plot([x1, x2], [y, y], color=C.INK, lw=1.8, zorder=1)
    for i, x in enumerate(xs):
        ax.add_patch(Circle((x, y), .14, facecolor=C.INK, edgecolor=C.INK, zorder=3))
        label(ax, f'$v_{i}$', (x, y), offset=(0, 11), ha='center', fontsize=9)
path(left, [0, 1, 2, 3, 4]); path(right, [0, 1, 2, 3, 4])
curve = Path([(0, .9), (1.5, -1.0), (3, .9)], [Path.MOVETO, Path.CURVE3, Path.CURVE3])
region = Path([(0, .9), (1.5, -1.0), (3, .9), (0, .9), (0, .9)],
              [Path.MOVETO, Path.CURVE3, Path.CURVE3, Path.LINETO, Path.CLOSEPOLY])
left.add_patch(PathPatch(region, facecolor=C.LIGHT, edgecolor='none', zorder=0))
left.add_patch(PathPatch(curve, fill=False, edgecolor=C.INK, ls='--', lw=1.4, zorder=2))
label(left, '$w=v_3$', (3, .9), offset=(8, -18), ha='center', fontsize=9)
label(left, '出现圈', (1.5, .5), ha='center', va='center', fontsize=10)
label(left, 'w 在路径上', (2, 1.75), ha='center', fontsize=10)
right.plot([-1.4, 0], [.9, .9], color=C.INK, ls='--', lw=1.4, zorder=2)
right.add_patch(Circle((-1.4, .9), .14, facecolor=C.PAPER, edgecolor=C.INK, lw=1.4, zorder=3))
label(right, '$w$', (-1.4, .9), offset=(0, 11), ha='center', fontsize=9)
label(right, '路径变长', (-.55, .9), offset=(0, -28), ha='center', fontsize=10)
label(right, 'w 不在路径上', (1.65, 1.75), ha='center', fontsize=10)
for ax in (left, right): ax.set(xlim=(-1.8, 4.8), ylim=(-.25, 2.1))
save(fig, 'K22-n4')

import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

from matplotlib.patches import Circle, FancyArrowPatch

fig, (odd, even) = new_fig(15, 7, ncols=2)
for ax in (odd, even): ax.axis('off'); ax.set_aspect('equal')
def cycle(ax, n, title, conflict=False):
    ang = np.pi/2 - np.arange(n) * 2*np.pi/n
    pts = np.c_[np.cos(ang), np.sin(ang)]
    for i in range(n):
        j = (i + 1) % n
        ax.add_patch(FancyArrowPatch(pts[i], pts[j], arrowstyle='-', color=C.INK,
                                     lw=2.0 if conflict and i == n-1 else 1.4,
                                     ls='--' if conflict and i == n-1 else '-',
                                     shrinkA=12, shrinkB=12, zorder=1))
    for i, (x, y) in enumerate(pts):
        filled = i % 2 == 0
        ax.add_patch(Circle((x, y), .13, facecolor=C.INK if filled else C.PAPER,
                            edgecolor=C.INK, lw=1.3, zorder=3))
        label(ax, str(i+1), (1.25*x, 1.25*y), ha='center', va='center', fontsize=9)
    label(ax, title, (0, -1.45), ha='center', va='top', fontsize=10)
    ax.set(xlim=(-1.55, 1.55), ylim=(-1.7, 1.45))
cycle(odd, 5, '奇圈（5 个点）', True)
label(odd, '冲突', (-.82, .95), ha='center', fontsize=9)
cycle(even, 6, '偶圈（6 个点）')
save(fig, 'K22-n6')

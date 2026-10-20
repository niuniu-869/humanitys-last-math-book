import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from math import gamma, sqrt, pi

fig, ax = new_fig(14, 8.4)
s = np.linspace(0.2, 5.3, 1000)
y = np.array([gamma(v) for v in s])
ax.plot(s, y, color=C.INK, ls='-', zorder=3)

points = [(1, 1, r'$0!=1$'), (2, 1, r'$1!=1$'), (3, 2, r'$2!=2$'),
          (4, 6, r'$3!=6$'), (5, 24, r'$\Gamma(5)=4!=24$')]
for i, (sx, sy, txt) in enumerate(points):
    ax.scatter([sx], [sy], s=34, marker='o', color=C.INK, zorder=5)
    off = [(0, 14), (0, 14), (-10, 14), (-12, 8), (-16, 0)][i]
    label(ax, txt, (sx, sy), offset=off, ha='center' if i < 2 else 'right', va='center')

half_y = sqrt(pi)
ax.scatter([0.5], [half_y], s=42, marker='o', facecolors=C.PAPER,
           edgecolors=C.INK, linewidths=1.1, zorder=5)
ax.plot([0.5, 0.5], [0, half_y], color=C.GRAY, ls='--', lw=1)
ax.plot([0.2, 0.5], [half_y, half_y], color=C.GRAY, ls='--', lw=1)
label(ax, r'$\Gamma(\frac{1}{2})=\sqrt{\pi}\approx1.7725$', (0.5, half_y),
      offset=(14, 34), ha='left')
label(ax, '$s$', (5.3, 0), offset=(5, -2), ha='left', va='top')
label(ax, r'$\Gamma(s)$', (0.2, 25.2), offset=(7, 0), ha='left', va='bottom')

ax.set(xlim=(0.2, 5.3), ylim=(0, 26), xlabel='', ylabel='')
ax.set_xticks([.5, 1, 2, 3, 4, 5]); ax.set_xticklabels(['0.5','1','2','3','4','5'])
ax.set_yticks([0, 5, 10, 15, 20, 25])
fig.tight_layout()
save(fig, 'C12-n4')

import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle, PathPatch
from matplotlib.path import Path

assert 950 + 50 == 1000 and 4950 + 94050 == 99000
assert 950 + 4950 == 5900 and 950 / 5900 == 19 / 118

def brace(ax, start, end, depth):
    start, end = np.array(start), np.array(end)
    v = end - start
    n = depth * np.array([-v[1], v[0]]) / np.linalg.norm(v)
    controls = [(0, 0), (0, .65), (.03, 1), (.25, 1),
                (.45, 1), (.48, 1), (.5, 1.6),
                (.52, 1), (.55, 1), (.75, 1),
                (.97, 1), (1, .65), (1, 0)]
    vertices = [start + t*v + h*n for t, h in controls]
    ax.add_patch(PathPatch(Path(vertices, [Path.MOVETO] + [Path.CURVE4]*12),
                           fill=False, edgecolor=C.INK, lw=1.2))

fig, ax = new_fig(20, 12)
ax.set(xlim=(-2, 10.4), ylim=(-2.3, 6.8))
ax.axis('off')
# Heights and widths are deliberately schematic; every cell carries its count.
ax.add_patch(Rectangle((0, 2), 3, 2, facecolor=C.AMBER, edgecolor='none', alpha=0.55))
ax.add_patch(Rectangle((3, 2), 7, 2, facecolor=C.LIGHT, edgecolor='none'))
ax.add_patch(Rectangle((0, 0), 10, 4, fill=False, edgecolor=C.INK, lw=1.3))
ax.plot([3, 3], [0, 4], color=C.INK, lw=1.2, ls='-')
ax.plot([0, 10], [2, 2], color=C.INK, lw=1.2, ls='-')
for x, text in [(1.5, '患病 1000'), (6.5, '健康 99 000')]:
    label(ax, text, (x, 4.2), ha='center', va='bottom')
for x, y, text in [(1.5, 3, '阳性\n950'), (1.5, 1, '阴性\n50'),
                    (6.5, 3, '阳性\n4950'), (6.5, 1, '阴性\n94 050')]:
    label(ax, text, (x, y), ha='center', va='center', linespacing=1.6)
brace(ax, (0, 4.8), (10, 4.8), 0.25)
label(ax, r'$P($患病$\mid$阳性$)=\frac{950}{950+4950}=\frac{19}{118}\approx16.1\%$',
      (5, 6.1), ha='center', va='center')
label(ax, '分母 = 阳性的 5900 人', (5, 5.45), ha='center', va='center')
brace(ax, (-0.25, 0), (-0.25, 4), 0.4)
label(ax, '患病\n1000 人', (-1.05, 2), ha='right', va='center', fontsize=9)
label(ax, r'$P($阳性$\mid$患病$)=\frac{950}{1000}=0.95$',
      (0, -0.6), ha='left', va='center')
label(ax, '分母 = 患病的 1000 人', (0, -1.2), ha='left', va='center')
label(ax, '阴影 = 阳性', (8, -0.6), ha='center', va='center')
label(ax, '共 10 万人；示意，未按比例', (5, -2), ha='center', va='center', fontsize=9)
fig.subplots_adjust(left=0.02, right=0.98, bottom=0.02, top=0.98)
save(fig, 'P2-n2')

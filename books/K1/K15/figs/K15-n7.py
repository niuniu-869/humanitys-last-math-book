import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Circle, Rectangle

fig, axes = new_fig(24, 6.6, ncols=5)
fig.subplots_adjust(left=.015, right=.985, top=.97, bottom=.05, wspace=.15)
def circle(ax, xy, r, style='-'):
    p = Circle(xy, r, facecolor='none', edgecolor=C.INK, ls=style, lw=1.3)
    ax.add_patch(p)
    return p
for ax, title, example in zip(axes, ['全同', '种属', '交叉', '矛盾', '反对'],
                            ['偶数 / 2 的倍数', '正方形 / 矩形', '质数 / 偶数\n重叠处是 2', '奇数 / 偶数', '正数 / 负数']):
    ax.set(xlim=(-.08, 3.08), ylim=(-1.35, 3.05), aspect='equal'); ax.axis('off')
    ax.add_patch(Rectangle((0, 0), 3, 2.8, facecolor=C.PAPER, edgecolor=C.INK, lw=1))
    label(ax, title, (1.5, -.28), ha='center', va='top')
    label(ax, example, (1.5, -.78), ha='center', va='top', fontsize=8)
circle(axes[0], (1.5, 1.4), 1)
circle(axes[0], (1.5, 1.4), 1, '--').set_linewidth(2.4)
label(axes[0], 'A = B', (1.5, 1.4), ha='center', va='center')
circle(axes[1], (1.5, 1.4), 1.15, '--')
circle(axes[1], (1.22, 1.2), .56)
label(axes[1], 'A', (1.22, 1.2), ha='center', va='center')
label(axes[1], 'B', (2.05, 1.95), ha='center', va='center')
a = circle(axes[2], (1.05, 1.4), .86)
b = circle(axes[2], (1.95, 1.4), .86, '--')
lens = Circle((1.05, 1.4), .86, facecolor=C.LIGHT, edgecolor='none')
axes[2].add_patch(lens); lens.set_clip_path(b)
a.set_zorder(3); b.set_zorder(3)
for x, text in [(.7, 'A'), (2.3, 'B'), (1.5, '2')]:
    label(axes[2], text, (x, 1.4), ha='center', va='center')
axes[3].plot([1.5, 1.5], [0, 2.8], color=C.INK, lw=1.3)
for x, text in [(.75, 'A'), (2.25, 'B')]:
    label(axes[3], text, (x, 1.4), ha='center', va='center')
for x, text, style in [(.75, 'A', '-'), (2.25, 'B', '--')]:
    circle(axes[4], (x, 1.75), .57, style)
    label(axes[4], text, (x, 1.75), ha='center', va='center')
label(axes[4], '还有第三种', (1.5, .55), ha='center', va='center', fontsize=8)
save(fig, "K15-n7")

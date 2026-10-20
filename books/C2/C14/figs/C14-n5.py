import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle, Polygon

fig, ax = new_fig(19, 24)
ax.set(xlim=(-.8, 18), ylim=(0, 23.4))
ax.axis('off')

def box(x, y, w, h, text, diamond=False):
    if diamond:
        patch = Polygon([(x-w/2, y), (x, y+h/2),
                         (x+w/2, y), (x, y-h/2)], closed=True,
                        facecolor=C.PAPER, edgecolor=C.INK, lw=1)
    else:
        patch = Rectangle((x-w/2, y-h/2), w, h,
                          facecolor=C.PAPER, edgecolor=C.INK, lw=1)
    ax.add_patch(patch)
    label(ax, text, (x, y), ha='center', va='center', fontsize=9)

def link(points, text=None, at=None):
    for start, end in zip(points[:-2], points[1:-1]):
        ax.plot([start[0], end[0]], [start[1], end[1]], color=C.INK, lw=.9)
    a, b = points[-2:]
    arrow(ax, a, (b[0]-a[0], b[1]-a[1]), color=C.INK, lw=.9)
    if text:
        label(ax, text, at, ha='center', va='center', fontsize=8)

box(8, 22.4, 3.2, .85, '拿到级数')
box(8, 20.1, 5.7, 2.1, '通项趋于 0 吗？', True)
box(14.7, 20.1, 2.6, .85, '发散')
box(8, 17.2, 5.4, 2.0, '各项非负吗？', True)
box(3.1, 14.1, 5.5, 1.7, '正项级数\n比较（含等价替换）\n比值或根值、积分')
box(11.3, 14.1, 5.2, 1.35, r'看 $\sum |u_n|$' + '\n（用左侧办法）')
box(3.1, 10.9, 3.4, .9, '收敛 / 发散')
box(11.3, 10.9, 5.3, 2.1, r'$\sum |u_n|$ 收敛吗？', True)
box(16.1, 10.9, 2.7, .9, '绝对收敛')
box(11.3, 7.8, 5.3, 2.1, '是交错级数吗？', True)
box(11.3, 4.7, 5.6, 2.1, '满足莱布尼茨条件？', True)
box(11.3, 1.9, 3.3, .9, '条件收敛')
box(3.1, 3.1, 5.3, 1.7, '继续判断\n换判别法、拆项\n或回到部分和')
link([(8, 21.975), (8, 21.15)])
link([(10.85, 20.1), (13.4, 20.1)], '否', (12.1, 20.45))
link([(8, 19.05), (8, 18.2)], '是', (8.45, 18.65))
link([(5.3, 17.2), (3.1, 17.2), (3.1, 14.95)], '是', (4.2, 17.55))
link([(10.7, 17.2), (11.3, 17.2), (11.3, 14.775)], '否', (11.75, 16.3))
link([(3.1, 13.25), (3.1, 11.35)], '可判定', (3.8, 12.3))
link([(.35, 14.1), (-.3, 14.1), (-.3, 3.1), (.45, 3.1)])
label(ax, r'$\rho=1$ 等：换方法', (-.3, 8.2), (8, 0), rotation=90,
      ha='center', va='center', fontsize=8)
link([(11.3, 13.425), (11.3, 11.95)])
link([(13.95, 10.9), (14.75, 10.9)], '是', (14.35, 11.3))
link([(11.3, 9.85), (11.3, 8.85)], '否', (11.75, 9.35))
link([(11.3, 6.75), (11.3, 5.75)], '是', (11.75, 6.25))
link([(8.65, 7.8), (7, 7.8), (7, 3.1), (5.75, 3.1)], '否', (7.7, 8.15))
link([(8.5, 4.7), (7, 4.7)], '否', (7.75, 5.05))
link([(11.3, 3.65), (11.3, 2.35)], '是', (11.75, 3))
label(ax, r'比值或根值得 $\rho>1$ 时，原级数也发散',
      (8.5, .3), ha='center', va='center', fontsize=9)
save(fig, 'C14-n5')

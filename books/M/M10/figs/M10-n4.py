import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, save, arrow, label
from matplotlib.patches import Rectangle, Circle

fig, ax = new_fig(17, 9)
def circ(x, y, s):
    ax.add_patch(Circle((x, y), .3, facecolor=C.PAPER, edgecolor=C.INK, lw=1.4))
    label(ax, s, (x, y), ha='center', va='center', fontsize=12)
def box(x, y, s):
    ax.add_patch(Rectangle((x - .55, y - .35), 1.1, .7, facecolor=C.LIGHT, edgecolor=C.INK, lw=1.3))
    label(ax, s, (x, y), ha='center', va='center', fontsize=11)
def dash(p, q, ls='--'):
    ax.annotate("", xy=q, xytext=p, arrowprops=dict(arrowstyle="-|>", color=C.GRAY, lw=1.2, ls=ls, shrinkA=0, shrinkB=0, mutation_scale=10))
# 细胞状态主干
yc = 4.3
ax.plot([.4, 9.4], [yc, yc], color=C.INK, lw=3.2)
arrow(ax, (9.0, yc), (.9, 0), color=C.INK, lw=3.2)
label(ax, '$c_{t-1}$', (.4, yc), offset=(0, 8), ha='left', va='bottom', fontsize=12)
label(ax, '$c_t$', (9.9, yc), offset=(0, 8), ha='center', va='bottom', fontsize=12)
circ(2.2, yc, '×'); circ(5.4, yc, '+'); circ(5.4, 3.0, '×'); circ(8.2, 5.7, '×')
arrow(ax, (5.4, 3.3), (0, .7), color=C.INK, lw=2.0)
# tanh(c_t) -> 输出
ax.plot([7.0, 7.0], [yc, 5.7], color=C.INK, lw=1.6)
box(7.0, 5.7, 'tanh'); ax.plot([7.55, 7.9], [5.7, 5.7], color=C.INK, lw=1.6)
arrow(ax, (8.5, 5.7), (1.2, 0), color=C.INK, lw=2.0)
label(ax, '$h_t$', (9.7, 5.7), offset=(6, 0), ha='left', va='center', fontsize=12)
# 四个方框
yb = 1.4
for x, s in [(2.2, 'σ'), (4.4, 'σ'), (6.6, 'tanh'), (8.2, 'σ')]:
    box(x, yb, s)
label(ax, '$f_t$', (2.2, 2.2), offset=(8, 0), ha='left', va='center')
label(ax, '$i_t$', (4.4, 2.2), offset=(-8, 0), ha='right', va='center')
label(ax, '$\\tilde c_t$', (6.6, 2.2), offset=(8, 0), ha='left', va='center')
label(ax, '$g_t$', (8.2, 2.2), offset=(8, 0), ha='left', va='center')
dash((2.2, yb + .35), (2.2, yc - .3))
dash((4.4, yb + .35), (5.2, 2.75))
dash((6.6, yb + .35), (5.6, 2.75))
dash((8.2, yb + .35), (8.2, 5.4))
# 输入总线
ax.plot([1.2, 8.7], [.35, .35], color=C.INK, lw=1.5)
for x in [2.2, 4.4, 6.6, 8.2]:
    ax.plot([x, x], [.35, yb - .35], color=C.INK, lw=1.2)
label(ax, '$h_{t-1}$ 与 $x_t$ 合并', (-.45, .60), ha='left', va='center', fontsize=9.5)
ax.set(xlim=(-.6, 10.6), ylim=(-.1, 6.5))
ax.axis('off')
save(fig, 'M10-n4')

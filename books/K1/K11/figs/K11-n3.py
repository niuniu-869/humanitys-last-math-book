import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import FancyBboxPatch

fig, ax = new_fig(14, 7.5)

def box(x, y, text, w=1.7, h=0.62, lw=1.2):
    ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h,
                                boxstyle='round,pad=0.02,rounding_size=0.05',
                                facecolor=C.PAPER, edgecolor=C.INK, lw=lw,
                                zorder=2))
    label(ax, text, (x, y), ha='center', va='center', fontsize=10)

# 四个叶子子句，顺序按请求：（1）（3）（2）（4）
leaves = [(1.3, 3.8, r'$\neg p\vee q$（1）'), (3.7, 3.8, r'$p$（3）'),
          (6.3, 3.8, r'$\neg q\vee r$（2）'), (8.9, 3.8, r'$\neg r$（4）')]
for x, y, text in leaves:
    box(x, y, text, w=2.0)

box(2.5, 2.55, '$q$')
box(4.4, 1.65, '$r$')
box(6.7, 0.72, '□', w=1.45, h=0.68, lw=2.2)

# 每条线只从上一层框底边中点出发，到下一层框顶边中点结束。
def seg(points, ls='-', lw=1.3):
    xs, ys = zip(*points)
    ax.plot(xs, ys, color=C.INK, ls=ls, lw=lw, zorder=1,
            solid_capstyle='round', solid_joinstyle='round')

# 框的 boxstyle 带 pad=0.02，连线端点取到实际外框边（x ± w/2, y ± h/2 ± 0.02）
PAD = 0.02
# 叶子（1）（3）汇到 q
seg([(1.3, 3.49 - PAD), (1.3, 3.20), (2.5, 2.86 + PAD)])
seg([(3.7, 3.49 - PAD), (3.7, 3.20), (2.5, 2.86 + PAD)])
# q 与叶子（2）汇到 r
seg([(2.5, 2.24 - PAD), (4.4, 1.96 + PAD)])
seg([(6.3, 3.49 - PAD), (4.4, 1.96 + PAD)])
# r 与叶子（4）汇到空子句
seg([(4.4, 1.34 - PAD), (4.4, 1.20), (6.7, 1.06 + PAD)])
seg([(8.9, 3.49 - PAD), (8.9, 1.80), (6.7, 1.06 + PAD)])

# 标签放在两条汇合线之间的空白处
label(ax, '消去 $p$', (2.5, 3.24), ha='center', va='center', fontsize=9)
label(ax, '消去 $q$', (3.95, 2.32), ha='center', va='center', fontsize=9)
label(ax, '消去 $r$', (6.0, 1.35), ha='center', va='center', fontsize=9)

ax.set(xlim=(0.15, 10.05), ylim=(0.2, 4.35)); ax.axis('off')
save(fig, 'K11-n3')

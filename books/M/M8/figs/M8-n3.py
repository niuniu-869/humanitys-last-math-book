import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle, Circle

fig, (ax1, ax2) = new_fig(17, 8, ncols=2)
for ax, title in ((ax1, '普通网络'), (ax2, '残差网络')):
    ax.set_xlim(0, 10); ax.set_ylim(-1.8, 5.2); ax.axis('off'); ax.set_title(title)
Y = 3.0
def block(ax, x, text):
    ax.add_patch(Rectangle((x-0.6, Y-0.45), 1.2, 0.9, facecolor=C.PAPER, edgecolor=C.INK, lw=1.2, zorder=3))
    label(ax, text, (x, Y), offset=(-7, -4), fontsize=10)
def ar(ax, a, b, ls='-', lw=1.6, rad=0.0):
    ax.annotate('', xy=b, xytext=a, arrowprops=dict(arrowstyle='-|>', lw=lw, ls=ls, color=C.INK, mutation_scale=10, connectionstyle=f'arc3,rad={rad}', shrinkA=0, shrinkB=0))
def pt(ax, x, text):
    ax.scatter([x], [Y], s=26, color=C.INK, zorder=4)
    label(ax, text, (x, Y), offset=(-8, -22), fontsize=9)
# 左：普通网络
pt(ax1, 0.8, r'$\boldsymbol{x}_0$'); block(ax1, 2.8, r'$F_1$'); pt(ax1, 5.0, r'$\boldsymbol{x}_1$'); block(ax1, 7.0, r'$F_2$'); pt(ax1, 9.2, r'$\boldsymbol{x}_2$')
for a, b in ((0.9, 2.2), (3.4, 4.9), (5.1, 6.4), (7.6, 9.1)):
    ar(ax1, (a, Y), (b, Y))
label(ax1, '只有一条路：$J_2J_1$', (5, 4.3), offset=(-52, 0), fontsize=9)
# 右：残差网络
pt(ax2, 0.8, r'$\boldsymbol{x}_0$'); block(ax2, 2.8, r'$F_1$'); block(ax2, 7.0, r'$F_2$')
for x, t in ((5.0, r'$\boldsymbol{x}_1$'), (9.2, r'$\boldsymbol{x}_2$')):
    ax2.add_patch(Circle((x, Y), 0.22, facecolor=C.PAPER, edgecolor=C.INK, lw=1.2, zorder=3)); label(ax2, '+', (x, Y), offset=(-4, -4), fontsize=10)
    label(ax2, t, (x, Y), offset=(-8, -26), fontsize=9)
for a, b in ((0.9, 2.2), (3.4, 4.75), (5.25, 6.4), (7.6, 8.95)):
    ar(ax2, (a, Y), (b, Y))
ar(ax2, (0.8, Y+0.1), (4.9, Y+0.22), ls=':', lw=1.4, rad=-0.55)
ar(ax2, (5.0, Y+0.22), (9.1, Y+0.22), ls=':', lw=1.4, rad=-0.55)
label(ax2, '跳线（虚线弧）', (2.9, 4.75), fontsize=8)
rows = ['① 两条跳线都走：$I$', '② 走 $F_1$、跳过 $F_2$：$J_1$', '③ 跳过 $F_1$、走 $F_2$：$J_2$', '④ 两个 $F$ 都走：$J_2J_1$']
for i, s in enumerate(rows):
    label(ax2, s, (0.2, 1.2 - 0.6*i), fontsize=8.5)
fig.text(0.5, 0.02, r'$(I+J_2)(I+J_1)=I+J_1+J_2+J_2J_1$', ha='center', fontsize=11)
save(fig, "M8-n3")

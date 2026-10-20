import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Circle, FancyArrowPatch, Arc

fig, axes = new_fig(18, 6, ncols=3)
def node(ax, xy, text):
    ax.add_patch(Circle(xy, .42, facecolor=C.PAPER, edgecolor=C.INK, lw=1.3))
    label(ax, text, xy, ha='center', va='center')
def directed(ax, a, b):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle='-|>', mutation_scale=13, color=C.INK, lw=1.5))
for ax in axes: ax.set(xlim=(0,4), ylim=(0,4)); ax.axis('off')
node(axes[0], (1,2), 'A'); node(axes[0], (3,2), 'B'); directed(axes[0], (1.45,2), (2.55,2))
label(axes[0], 'A 导致 B', (2, .55), ha='center')
node(axes[1], (1,2), 'A'); node(axes[1], (3,2), 'B'); directed(axes[1], (2.55,2), (1.45,2))
label(axes[1], 'B 导致 A（因果倒置）', (2, .55), ha='center', fontsize=9)
node(axes[2], (2,3.1), 'C'); node(axes[2], (1,1.1), 'A'); node(axes[2], (3,1.1), 'B')
directed(axes[2], (1.72,2.78), (1.25,1.5)); directed(axes[2], (2.28,2.78), (2.75,1.5))
axes[2].add_patch(Arc((2,1.35), 1.55, .8, theta1=200, theta2=340, color=C.INK, lw=1.1, ls='--'))
label(axes[2], '一起变化', (2,.65), ha='center', fontsize=8.5)
label(axes[2], '共同原因 C', (2,3.82), ha='center')
label(axes[2], 'C＝气温，A＝冰淇淋销量，B＝溺水事故', (2,.1), ha='center', fontsize=7.5)
fig.subplots_adjust(wspace=.12)
save(fig, 'K14-n3')

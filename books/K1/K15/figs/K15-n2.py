import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Circle, FancyArrowPatch

fig, axes = new_fig(21, 8.2, ncols=3)
fig.subplots_adjust(left=.025, right=.975, bottom=.06, top=.86, wspace=.22)
fig.text(.5, .95, 'A：会员制    B：复购率上升', ha='center', color=C.INK)
def node(ax, x, y, name):
    ax.add_patch(Circle((x, y), .26, facecolor=C.PAPER, edgecolor=C.INK, lw=1.3))
    label(ax, name, (x, y), ha='center', va='center')
def link(ax, a, b, style='--', rad=0):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle='-|>', mutation_scale=12,
                               connectionstyle=f'arc3,rad={rad}', ls=style, color=C.INK, lw=1.3))
for ax, title, example in zip(axes, ['他因', '倒置', '共同原因'],
                            ['新品上市', '爱复购的人才办会员', '顾客的消费习惯']):
    ax.set(xlim=(0, 4), ylim=(0, 4.8), aspect='equal'); ax.axis('off')
    node(ax, .7, 2.4, 'A'); node(ax, 3.3, 2.4, 'B')
    label(ax, title, (2, 4.35), ha='center')
    label(ax, example, (2, .25), ha='center', fontsize=9)
link(axes[0], (.98, 2.4), (3.02, 2.4), '-')
node(axes[0], .7, 1.2, 'C')
link(axes[0], (.95, 1.3), (3.08, 2.23))
label(axes[0], 'C 也能造成 B', (2.25, .85), ha='center', fontsize=9)
link(axes[1], (.98, 2.4), (3.02, 2.4), '-')
axes[1].plot([1.85, 2.15], [2.6, 2.2], color=C.INK, lw=1.6)
axes[1].plot([1.85, 2.15], [2.2, 2.6], color=C.INK, lw=1.6)
link(axes[1], (3.2, 2.12), (.8, 2.12), rad=-.45)
label(axes[1], 'B 反过来造成 A', (2, .85), ha='center', fontsize=9)
node(axes[2], 2, 3.6, 'Z')
link(axes[2], (1.8, 3.4), (.9, 2.6))
link(axes[2], (2.2, 3.4), (3.1, 2.6))
axes[2].plot([.98, 3.02], [2.4, 2.4], ls=':', color=C.INK)
label(axes[2], 'A 与 B 一起变化，\n却互不造成', (2, 1.05), ha='center', fontsize=9)
save(fig, "K15-n2")

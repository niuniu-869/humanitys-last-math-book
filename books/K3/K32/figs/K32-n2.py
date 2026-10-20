import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle, FancyArrowPatch

fig, (ax1, ax2) = new_fig(18, 9, ncols=2)
for ax in (ax1, ax2):
    ax.axis('off')

def node(ax, xy, text, box=False, width=1.24):
    x, y = xy
    if box:
        ax.add_patch(Rectangle((x - width/2, y - .22), width, .44, facecolor=C.PAPER,
                               edgecolor=C.GRAY, lw=.9, ls='--'))
    label(ax, text, xy, ha='center', va='center', fontsize=9)

split_nodes = {
    'root': (4.0, 5.9), 'l': (2.1, 4.7), 'r': (5.9, 4.7),
    'll': (1.2, 3.5), 'lr': (3.0, 3.5), 'rl': (5.0, 3.5), 'rr': (6.8, 3.5),
    'lll': (.75, 2.3), 'llr': (1.65, 2.3), 'rll': (4.55, 2.3), 'rlr': (5.45, 2.3),
}
split_text = {'root':'[5,2,8,1,9,3]', 'l':'[5,2,8]', 'r':'[1,9,3]',
              'll':'[5,2]', 'lr':'[8]', 'rl':'[1,9]', 'rr':'[3]',
              'lll':'[5]', 'llr':'[2]', 'rll':'[1]', 'rlr':'[9]'}
for child, parent in [('l','root'),('r','root'),('ll','l'),('lr','l'),('rl','r'),('rr','r'),
                       ('lll','ll'),('llr','ll'),('rll','rl'),('rlr','rl')]:
    ax1.add_patch(FancyArrowPatch(split_nodes[parent], split_nodes[child], arrowstyle='-|>',
                                  mutation_scale=10, color=C.INK, lw=1.0))
for k, xy in split_nodes.items(): node(ax1, xy, split_text[k])
label(ax1, '分：自上而下', (4.0, 6.55), ha='center', fontsize=11)
ax1.set(xlim=(-.1, 8.1), ylim=(1.6, 6.9))

mnodes = {'root': (4.0, 2.2), 'l': (2.1, 3.4), 'r': (5.9, 3.4),
          'll': (1.2, 4.6), 'lr': (3.0, 4.6), 'rl': (5.0, 4.6), 'rr': (6.8, 4.6),
          'lll': (.75, 5.8), 'llr': (1.65, 5.8), 'rll': (4.55, 5.8), 'rlr': (5.45, 5.8)}
mtext = {'root': '[1,2,3,5,8,9]', 'l': '[2,5,8]', 'r': '[1,3,9]', 'll': '[2,5]', 'lr': '[8]',
         'rl': '[1,9]', 'rr': '[3]', 'lll': '[5]', 'llr': '[2]', 'rll': '[1]', 'rlr': '[9]'}
mcomp = {'root': 5, 'l': 2, 'r': 2, 'll': 1, 'rl': 1}
for child, parent in [('l','root'),('r','root'),('ll','l'),('lr','l'),('rl','r'),('rr','r'),
                       ('lll','ll'),('llr','ll'),('rll','rl'),('rlr','rl')]:
    ax2.add_patch(FancyArrowPatch(mnodes[child], mnodes[parent], arrowstyle='-|>',
                                  mutation_scale=10, color=C.INK, lw=1.0, shrinkA=9, shrinkB=9))
for k, xy in mnodes.items():
    node(ax2, xy, mtext[k], box=k in mcomp, width={'root': 2.0, 'l': 1.3, 'r': 1.3}.get(k, 1.0))
# 比较次数标签：与对应虚线框至少留半个字宽，且避开所有箭头。
# [2,5]、[1,9] 放在框下方偏左，让开框右下方出去的那条箭头。
mcomp_pos = {
    'root': (4.00, 1.80, 'center', 'top'),
    'l':    (1.10, 3.40, 'right', 'center'),
    'r':    (6.88, 3.40, 'left', 'center'),
    'll':   (0.50, 4.00, 'center', 'center'),
    'rl':   (4.30, 4.00, 'center', 'center'),
}
for k in mcomp:
    x, y, ha, va = mcomp_pos[k]
    label(ax2, f'比较 {mcomp[k]} 次', (x, y), ha=ha, va=va, fontsize=8.5)
label(ax2, '合：自下而上', (3.9, 6.55), ha='center', fontsize=11)
label(ax2, '共 1+2+1+2+5=11 次比较', (4.0, .95), ha='center', fontsize=10)
ax2.set(xlim=(-.5, 8.4), ylim=(.6, 6.9))
fig.subplots_adjust(wspace=.25)
save(fig, 'K32-n2')

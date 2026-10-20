import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle

assert 8 * 64 == 512
fig, ax = new_fig(26, 11)
ax.set(xlim=(-0.85, 23.5), ylim=(-0.7, 8.0))
ax.axis('off')

def box(x, y, w, h, text, fill=C.PAPER, ls='-'):
    ax.add_patch(Rectangle((x, y-h/2), w, h, facecolor=fill,
                          edgecolor=C.INK, lw=1, ls=ls))
    label(ax, text, (x+w/2, y), ha='center', va='center', fontsize=9)

box(-0.55, 3.5, 2.1, 1.2, '输入\n'+r'$n\times512$')
arrow(ax, (1.55, 3.5), (1.2, 0), color=C.INK, lw=1.1)
ax.plot([2.75, 2.75], [1, 6.5], color=C.INK, lw=1.1)
label(ax, r'$n\times512$', (2.22, 3.82), ha='center', va='bottom', fontsize=8)
for y, i in [(6.5, '1'), (4.1, '2'), (1, '8')]:
    arrow(ax, (2.75, y), (1.3, 0), color=C.INK, lw=1.1)
    label(ax, r'$n\times512$', (3.4, y+0.28), ha='center', fontsize=8)
    ax.add_patch(Rectangle((4.05, y-0.85), 8.8, 1.7, fill=False,
                          edgecolor=C.INK, ls='--', lw=1))
    label(ax, '头 '+i, (4.2, y+0.57), fontsize=8)
    label(ax, rf'$QW_{i}^Q,\ KW_{i}^K,\ VW_{i}^V$'+'\n各 '+r'$n\times64$',
          (6.15, y-0.06), ha='center', va='center', fontsize=9)
    arrow(ax, (8.1, y), (1.1, 0), color=C.INK, lw=1.1)
    label(ax, r'$n\times64$', (8.65, y+0.28), ha='center', fontsize=8)
    label(ax, '注意力\n'+r'$n\times n$ 得分 $\to n\times64$',
          (10.95, y), ha='center', va='center', fontsize=9)
    arrow(ax, (12.85, y), (1.2, 0), color=C.INK, lw=1.1)
    label(ax, r'$n\times64$', (13.45, y+0.28), ha='center', fontsize=8)
label(ax, r'$\vdots$', (8.45, 2.55), ha='center', va='center', fontsize=19)
ax.plot([14.05, 14.05], [1, 6.5], color=C.INK, lw=1.1)
arrow(ax, (14.05, 3.5), (0.65, 0), color=C.INK, lw=1.1)
label(ax, r'$8\times(n\times64)$', (15.55, 4.45), ha='center', fontsize=8)
box(14.7, 3.5, 2.0, 1.2, '拼接\n'+r'$n\times512$', fill=C.LIGHT)
arrow(ax, (16.7, 3.5), (1.3, 0), color=C.INK, lw=1.1)
label(ax, r'$n\times512$', (17.35, 4.3), ha='center', fontsize=8)
box(18, 3.5, 2.2, 1.2, r'乘 $W^O$'+'\n'+r'$512\times512$')
arrow(ax, (20.2, 3.5), (1.3, 0), color=C.INK, lw=1.1)
label(ax, r'$n\times512$', (20.85, 4.3), ha='center', fontsize=8)
box(21.5, 3.5, 1.9, 1.2, '输出\n'+r'$n\times512$')
label(ax, r'$8\times64=512$', (15.7, 1.8), ha='center', fontsize=11)
fig.tight_layout(pad=0.5)
save(fig, "M18-n2")

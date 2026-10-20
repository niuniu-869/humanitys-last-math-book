import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle, FancyArrowPatch

fig, ax = new_fig(19, 8)
ax.set(xlim=(0, 19), ylim=(0, 8)); ax.axis('off')
for x, y, w, h, text, style in [
    (0.3, 4.8, 6.1, 2, '论据：推出会员制后，\n复购率从 31% 升到 38%', '-'),
    (13.1, 4.8, 5.6, 2, '论点：会员制\n提高了复购率', '-'),
    (4.2, 1.8, 10.6, 1.6, '桥（没说出口）：\n复购率的上升没有别的原因', '--'),
]:
    ax.add_patch(Rectangle((x, y), w, h, facecolor=C.LIGHT if style == '--' else C.PAPER,
                           edgecolor=C.INK, ls=style, lw=1.4))
    label(ax, text, (x+w/2, y+h/2), ha='center', va='center')
arrow(ax, (6.4, 5.8), (6.7, 0), color=C.INK)
label(ax, '作者以为的直通', (9.75, 6.25), ha='center', fontsize=9)
for start, end in [((3.35, 4.8), (4.2, 2.6)), ((14.8, 2.6), (15.9, 4.8))]:
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle='-|>', mutation_scale=12,
                               ls='--', lw=1.4, color=C.INK))
label(ax, '实线框 = 写出来的    虚线框 = 没写出来的', (18.7, 0.55), ha='right', fontsize=8)
save(fig, "K15-n1")

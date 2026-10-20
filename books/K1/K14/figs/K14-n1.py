import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = new_fig(18, 7)
ax.set(xlim=(0, 18), ylim=(0, 7)); ax.axis('off')
ax.add_patch(FancyBboxPatch((0.4, 4.0), 5.2, 2.0, boxstyle='round,pad=0.1', facecolor=C.PAPER, edgecolor=C.INK, lw=1.4))
label(ax, '前提：推出会员制后，\n复购率由 30% 升到 36%', (3.0, 5.0), ha='center', va='center', fontsize=10)
ax.add_patch(FancyBboxPatch((12.4, 4.0), 5.2, 2.0, boxstyle='round,pad=0.1', facecolor=C.PAPER, edgecolor=C.INK, lw=2.4))
label(ax, '结论：\n会员制提高了复购', (15.0, 5.0), ha='center', va='center', fontsize=10)
# 断开的箭头
ax.add_patch(FancyArrowPatch((5.7, 5.0), (7.9, 5.0), arrowstyle='-', color=C.INK, lw=1.7))
ax.add_patch(FancyArrowPatch((10.1, 5.0), (12.3, 5.0), arrowstyle='-|>', mutation_scale=14, color=C.INK, lw=1.7))
label(ax, '缺口', (9.0, 5.0), ha='center', va='center', fontsize=10)
# 假设框
ax.add_patch(FancyBboxPatch((4.0, 0.9), 10.0, 1.9, boxstyle='round,pad=0.1', facecolor=C.PAPER, edgecolor=C.INK, lw=1.2, ls='--'))
label(ax, '隐含假设：除会员制外，同期没有别的因素\n改变复购率（季节、促销、竞争）', (9.0, 1.85), ha='center', va='center', fontsize=10)
ax.add_patch(FancyArrowPatch((9.0, 2.95), (9.0, 4.6), arrowstyle='-', color=C.INK, lw=1.2, ls='--'))
label(ax, '后面各节检验的就是它', (9.3, 3.45), ha='left', va='center', fontsize=9)
save(fig, 'K14-n1')

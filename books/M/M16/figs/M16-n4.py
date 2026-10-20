import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch

fig, ax = new_fig(17, 8)
def box(cx, cy, w, h, txt, fill=C.PAPER, fs=10):
    ax.add_patch(Rectangle((cx-w/2, cy-h/2), w, h, facecolor=fill, edgecolor=C.INK, lw=1.2))
    label(ax, txt, (cx, cy), ha='center', va='center', fontsize=fs)
def conn(a, b, ls='-', lw=1.3, color=C.INK, style='-|>'):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle=style, mutation_scale=12, shrinkA=0, shrinkB=0,
                                 lw=lw, ls=ls, color=color))
# 前向主线
box(0.9, 3.4, 1.2, 0.8, '$\\boldsymbol{x}$')
box(2.9, 3.4, 1.6, 1.2, '编码器')
box(5.2, 4.1, 1.2, 0.7, '$\\boldsymbol{\\mu}$')
box(5.2, 2.7, 1.2, 0.7, '$\\boldsymbol{\\sigma}$')
ax.add_patch(Circle((8.0, 3.4), 0.95, facecolor=C.PAPER, edgecolor=C.INK, lw=1.2))
label(ax, '$\\boldsymbol{z}=\\boldsymbol{\\mu}+$\n$\\boldsymbol{\\sigma}\\odot\\boldsymbol{\\varepsilon}$', (8.0, 3.4), ha='center', va='center', fontsize=9)
box(10.3, 3.4, 1.6, 1.2, '解码器')
box(12.5, 3.4, 1.3, 0.8, '$g(\\boldsymbol{z})$')
box(8.0, 5.6, 2.5, 0.8, '$\\boldsymbol{\\varepsilon}\\sim N(\\boldsymbol{0},I)$', fill=C.LIGHT)
conn((1.5, 3.4), (2.1, 3.4)); conn((3.7, 3.6), (4.6, 4.0)); conn((3.7, 3.2), (4.6, 2.8))
conn((5.8, 4.1), (7.2, 3.75)); conn((5.8, 2.7), (7.2, 3.05)); conn((8.95, 3.4), (9.5, 3.4)); conn((11.1, 3.4), (11.85, 3.4))
conn((8.0, 5.2), (8.0, 4.35))
label(ax, '噪声从旁边进入，不依赖任何参数', (8.0, 6.15), ha='center')
# KL 与重建（虚线）
box(5.2, 5.6, 2.2, 0.8, '先验 $N(\\boldsymbol{0},I)$', fill=C.LIGHT)
ax.add_patch(Rectangle((4.45, 2.2), 1.5, 2.6, facecolor='none', edgecolor=C.GRAY, lw=1.0, ls='-.'))
label(ax, '$q$ 的参数', (6.05, 2.35), ha='left', color=C.GRAY)
conn((5.2, 4.8), (5.2, 5.2), ls='--', color=C.GRAY, style='<->')
label(ax, 'KL 项', (5.55, 5.0), ha='left', color=C.GRAY)
box(12.5, 5.6, 1.3, 0.8, '$\\boldsymbol{x}$（目标）', fill=C.LIGHT)
conn((12.5, 3.8), (12.5, 5.2), ls='--', color=C.GRAY, style='<->')
label(ax, '重建误差', (12.65, 4.5), ha='left', color=C.GRAY)
# 梯度回传：下面一行粗实线箭头
yb = 1.0
box(12.5, yb, 1.5, 0.7, '$\\partial L/\\partial g$', fs=9)
box(8.0, yb, 1.5, 0.7, '$\\partial L/\\partial \\boldsymbol{z}$', fs=9)
box(5.2, yb, 2.2, 0.7, '$\\partial L/\\partial\\boldsymbol{\\mu}$、$\\partial L/\\partial\\boldsymbol{\\sigma}$', fs=9)
box(2.2, yb, 2.2, 0.7, '编码器参数 $\\phi$', fs=9)
conn((11.75, yb), (8.75, yb), lw=2.6); conn((7.25, yb), (6.3, yb), lw=2.6); conn((4.1, yb), (3.3, yb), lw=2.6)
conn((12.5, 3.0), (12.5, 1.35), lw=2.0, ls=':'); conn((8.0, 2.45), (8.0, 1.35), lw=2.0, ls=':')
conn((5.2, 2.2), (5.2, 1.35), lw=2.0, ls=':')
label(ax, 'KL 项直接作用于均值和标准差', (5.35, 1.75), ha='left')
label(ax, '重建项经 $\\boldsymbol{z}$ 回传（粗实线），KL 项走直接支路（点线）；噪声保持固定', (7.0, -0.15), ha='center')
ax.set(xlim=(0, 13.6), ylim=(-0.5, 6.5), aspect='equal'); ax.axis('off')
save(fig, 'M16-n4')

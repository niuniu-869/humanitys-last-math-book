import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, save, arrow, label
from matplotlib.patches import Rectangle

fig, ax = new_fig(18, 9.6)
xs = [2.4, 5.7, 9.0]
hw = .72
yb, hb = 1.9, 1.15
for i, x in enumerate(xs, 1):
    # 循环单元
    ax.add_patch(Rectangle((x - hw, yb), 2*hw, hb, facecolor=C.LIGHT, edgecolor=C.INK, lw=1.5))
    label(ax, 'tanh', (x, 2.76), ha='center', va='center', fontsize=12)
    label(ax, '$W,U,b$', (x, 2.18), ha='center', va='center', fontsize=10)
    # 沿链向右传的状态
    x0 = .35 if i == 1 else xs[i-2] + hw
    arrow(ax, (x0, 2.45), (x - hw - x0, 0), color=C.INK, lw=2.0)
    hl = '$h_0=0$' if i == 1 else f'$h_{i-1}$'
    label(ax, hl, ((x0 + x - hw)/2, 2.45), offset=(0, 7), ha='center', va='bottom', fontsize=10)
    # 输入
    arrow(ax, (x, .85), (0, yb - .85), color=C.INK, lw=1.5)
    label(ax, f'$x_{i}$', (x, .85), offset=(7, -3), ha='left', va='top')
    label(ax, ['我', '爱', '你'][i-1], (x, .45), ha='center', va='center', fontsize=10)
    # 输出线性层：三个时刻写法相同，共用同一组 W_out, b_out
    ax.annotate("", xy=(x, 4.0), xytext=(x, yb + hb),
                arrowprops=dict(arrowstyle="-|>", color=C.GRAY, lw=1.2, ls='--',
                                shrinkA=0, shrinkB=0, mutation_scale=10))
    ax.add_patch(Rectangle((x - 1.10, 4.0), 2.20, .95,
                           facecolor=C.PAPER, edgecolor=C.GRAY, lw=1.0))
    label(ax, '$W_{out}, b_{out}$', (x, 4.62), ha='center', va='center', fontsize=8.5)
    label(ax, '线性输出', (x, 4.22), ha='center', va='center', fontsize=9)
    # 线性层到 softmax
    ax.annotate("", xy=(x, 5.55), xytext=(x, 4.95),
                arrowprops=dict(arrowstyle="-|>", color=C.GRAY, lw=1.2, ls='--',
                                shrinkA=0, shrinkB=0, mutation_scale=10))
    ax.add_patch(Rectangle((x - .70, 5.55), 1.40, .60,
                           facecolor=C.PAPER, edgecolor=C.GRAY, lw=1.0))
    label(ax, 'softmax', (x, 5.85), ha='center', va='center', fontsize=9)
    label(ax, f'$p_{i}$', (x, 6.22), offset=(0, 3), ha='center', va='bottom')

# 最右侧输出状态 h_3
arrow(ax, (xs[2] + hw, 2.45), (.85, 0), color=C.INK, lw=2.0)
label(ax, '$h_3$', (xs[2] + hw + .42, 2.45), offset=(0, 7), ha='center', va='bottom', fontsize=10)

ax.set(xlim=(0, 10.7), ylim=(0, 6.8))
ax.axis('off')
save(fig, 'M10-n1')

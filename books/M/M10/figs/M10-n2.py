import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, save, arrow, label
from matplotlib.patches import Rectangle, Circle

fig, ax = new_fig(17, 10.5)
xs = [2.4, 5.9, 9.4]
yplus, r = 7.15, .32
yb, hb = 5.15, 1.00          # “逐分量乘 1-h_t^2” 方框
yd = 4.20                    # δ_t 所在高度
for t, x in zip([1, 2, 3], xs):
    # 来自本步输出的梯度
    ax.annotate("", xy=(x, yplus + r), xytext=(x, 8.05),
                arrowprops=dict(arrowstyle="-|>", color=C.GRAY, lw=1.2, ls='--',
                                shrinkA=0, shrinkB=0, mutation_scale=10))
    label(ax, '$W_{out}^{T}(p_t-y_t)/T$', (x, 8.13), offset=(0, 3),
          ha='center', va='bottom', fontsize=8.5)
    # 加法节点
    ax.add_patch(Circle((x, yplus), r, facecolor=C.PAPER, edgecolor=C.INK, lw=1.4))
    label(ax, '+', (x, yplus), ha='center', va='center', fontsize=12)
    # 加法节点下方：∂L/∂h_t
    arrow(ax, (x, yplus - r), (0, yb + hb - (yplus - r)), color=C.INK, lw=1.4)
    label(ax, f'$\\partial L/\\partial h_{t}$', (x, (yplus - r + yb + hb)/2),
          offset=(7, 0), ha='left', va='center', fontsize=10)
    # 逐分量乘 1-h_t^2
    ax.add_patch(Rectangle((x - 1.18, yb), 2.36, hb,
                           facecolor=C.LIGHT, edgecolor=C.INK, lw=1.5))
    label(ax, '逐分量乘', (x, yb + .68), ha='center', va='center', fontsize=9.5)
    label(ax, '$1-h_t^2$', (x, yb + .24), ha='center', va='center', fontsize=10)
    # 方框下方箭头标 δ_t
    arrow(ax, (x, yb), (0, yd - yb), color=C.INK, lw=1.4)
    label(ax, f'$\\delta_{t}$', (x, yd), offset=(7, 0), ha='left', va='center', fontsize=12)
    # δ_t 向下连到阴影小方框
    ax.annotate("", xy=(x, 1.90), xytext=(x, yd - .28),
                arrowprops=dict(arrowstyle="-|>", color=C.GRAY, lw=1.0, ls=':',
                                shrinkA=0, shrinkB=0, mutation_scale=8))
    # 每个时刻的 δ_t h_{t-1}^T
    ax.add_patch(Rectangle((x - 1.18, 1.15), 2.36, .75,
                           facecolor=C.LIGHT, edgecolor=C.INK, lw=1.0))
    label(ax, f'$\\delta_{t}h_{t-1}^{{T}}$', (x, 1.525),
          ha='center', va='center', fontsize=10.5)

# 误差信号从右向左：从 δ_t 处引出，向上折入左侧加法节点
for x, xl, t in [(xs[1], xs[0], 2), (xs[2], xs[1], 3)]:
    xr = x - 1.75
    ax.plot([x, xr], [yd, yd], color=C.INK, lw=2.0, solid_capstyle='butt')
    ax.plot([xr, xr], [yd, yplus], color=C.INK, lw=2.0, solid_capstyle='butt')
    arrow(ax, (xr, yplus), (xl + r - xr, 0), color=C.INK, lw=2.0)
    label(ax, f'$W^{{T}}\\delta_{t}$', ((x + xr)/2, yd), offset=(0, 5),
          ha='center', va='bottom', fontsize=10)
# 最右侧没有从右边来的箭头
label(ax, '$\\delta_{T+1}=0$', (xs[2] + r, yplus), offset=(6, 0),
      ha='left', va='center', fontsize=10)

# 三项相加得到 W 的梯度
for x0, x1 in [(xs[0], xs[1]), (xs[1], xs[2])]:
    label(ax, '+', ((x0 + x1)/2, 1.525), ha='center', va='center', fontsize=14)
label(ax, '$=\\ \\partial L/\\partial W$', (xs[2] + 1.42, 1.525),
      ha='left', va='center', fontsize=12)
label(ax, '每个时刻的小方框加起来才是 $W$ 的梯度', (5.9, .48),
      ha='center', va='center', fontsize=10.5)

ax.set(xlim=(.35, 12.75), ylim=(.15, 8.8))
ax.axis('off')
save(fig, 'M10-n2')

import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, save, arrow, label
from matplotlib.patches import Rectangle, Circle

fig, ax = new_fig(17, 9.5)
w = [0.2045, 0.3576, 0.4379]
xs = [2.0, 4.0, 6.0]
hs = ['$h_1=(1,0)$', '$h_2=(0,1)$', '$h_3=(1,1)$']
sum_c, sum_r = (4.0, 6.5), .38

def on_circle(target, r=sum_r, c=sum_c):
    """从圆心指向 target 的方向与圆的交点。"""
    vx, vy = target[0] - c[0], target[1] - c[1]
    d = np.hypot(vx, vy)
    return (c[0] + r*vx/d, c[1] + r*vy/d)

# 灰色虚线框（保持原高度，柱顶数字在框内）
ax.add_patch(Rectangle((.9, .9), 6.2, 4.55, facecolor='none',
                       edgecolor=C.GRAY, lw=1.0, ls='--'))

# 权重柱（浅灰填充）与柱顶数值、底部标签
for x, wi, hl in zip(xs, w, hs):
    top = 1.0 + wi*7
    ax.add_patch(Rectangle((x - .45, 1.0), .9, wi*7, facecolor=C.LIGHT,
                           edgecolor=C.INK, lw=1.4))
    nx = x - .23 if x == 4.0 else x   # 中间柱的数字略向左，让开右侧的点线
    label(ax, f'{wi:.4f}', (nx, top), offset=(0, 3),
          ha='center', va='bottom', fontsize=9.5)
    label(ax, hl, (x, .36), ha='center', va='center', fontsize=9.5)

# 加权求和：柱顶汇合到 Σ（实线）
ax.add_patch(Circle(sum_c, sum_r, facecolor=C.PAPER, edgecolor=C.INK, lw=1.5))
for x, wi in zip(xs, w):
    top = 1.0 + wi*7
    start = (x, top + .75)
    ax.annotate("", xy=on_circle(start), xytext=start,
                arrowprops=dict(arrowstyle="-|>", color=C.INK, lw=1.3,
                                shrinkA=0, shrinkB=0, mutation_scale=10))
label(ax, 'Σ', sum_c, ha='center', va='center', fontsize=14)
label(ax, '$\\bar h_t=(0.6424,\\ 0.7955)$', (4.0, 6.9), offset=(0, 4),
      ha='center', va='bottom', fontsize=11)

# 梯度：从 Σ 出发的三条直线点线箭头，指向各 h_j 标签上方一点。
# 起点取在圆的右下方并与柱子顶上来的实线错开，线从柱子上层穿过。
g_targets = [(2.20, .68), (4.43, .68), (6.45, .68)]
g_starts = [on_circle(g_targets[0]), (4.20, 6.15), (4.30, 6.13)]
for (x0, y0), (x1, y1) in zip(g_starts, g_targets):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), zorder=4,
                arrowprops=dict(arrowstyle="-|>", color=C.INK, lw=1.0,
                                ls=(0, (1.2, 2.2)), shrinkA=0, shrinkB=0,
                                mutation_scale=8))

# 解码器（位置不变）
ax.add_patch(Rectangle((8.4, 2.3), 2.4, 1.2, facecolor=C.PAPER,
                       edgecolor=C.INK, lw=1.5))
label(ax, '解码器', (9.6, 3.12), ha='center', va='center', fontsize=12)
label(ax, '$s_{t-1}=(1,0)$', (9.6, 2.55), ha='center', va='center', fontsize=10)
arrow(ax, (8.4, 2.9), (-1.3, 0), color=C.INK, lw=1.8)
label(ax, '打分、softmax', (9.6, 3.80), ha='center', va='center', fontsize=9.5)

# 图下说明：实线与点线的含义只在这里交代一次
label(ax, '柱高 = 权重 $\\alpha$；实线：加权求和，', (5.2, -.30),
      ha='center', va='center', fontsize=9.2)
label(ax, '点线：梯度经本步上下文向量直接连到每个 $h_j$（权重很小时贡献也小）',
      (5.2, -.78), ha='center', va='center', fontsize=9.2)

ax.set(xlim=(.2, 11.2), ylim=(-1.15, 7.65))
ax.axis('off')
save(fig, 'M10-n5')

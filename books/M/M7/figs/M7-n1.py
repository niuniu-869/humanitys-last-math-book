import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, (ax1, ax2) = new_fig(14, 6.2, ncols=2)
inputs = np.array([[0,0],[1,0],[0,1],[1,1]])
hidden = np.maximum(0, inputs.sum(axis=1)[:, None] + np.array([0,-1]))
assert np.array_equal(hidden, [[0,0],[1,0],[1,0],[2,1]])
assert np.array_equal(hidden @ np.array([1,-2]) > 0.5, [False,True,True,False])

# 输入平面：异或四点与一条会分错的直线
ax1.set_xlim(-0.5, 1.5); ax1.set_ylim(-0.5, 1.5)
ax1.set_aspect('equal', adjustable='box')
ax1.set_xlabel(r'$x_1$'); ax1.set_ylabel(r'$x_2$')
ax1.set_title('输入平面')
for xy in [(0, 0), (1, 1)]:
    ax1.scatter(*xy, s=52, marker='o', facecolor=C.INK, edgecolor=C.INK, zorder=5)
for xy in [(1, 0), (0, 1)]:
    ax1.scatter(*xy, s=58, marker='o', facecolor=C.PAPER, edgecolor=C.INK, linewidth=1.4, zorder=5)
xx = np.linspace(-0.5, 1.5, 200)
ax1.plot(xx, 0.5-xx, ls='--', color=C.GRAY, lw=1.3)
label(ax1, '分错', (0.52, -0.02), offset=(4, 6), fontsize=9)
label(ax1, '标签 0', (0, 0), offset=(-6, -17), fontsize=8)
label(ax1, '标签 1', (1.42, -0.28), ha='right', fontsize=8)

# 隐藏层输出平面
ax2.set_xlim(-0.5, 2.5); ax2.set_ylim(-0.5, 1.5)
ax2.set_aspect('equal', adjustable='box')
ax2.set_xlabel(r'$h_1$'); ax2.set_ylabel(r'$h_2$')
ax2.set_title('隐藏层输出平面')
for xy in [(0, 0), (2, 1)]:
    ax2.scatter(*xy, s=52, marker='o', facecolor=C.INK, edgecolor=C.INK, zorder=5)
ax2.scatter(1, 0, s=58, marker='o', facecolor=C.PAPER, edgecolor=C.INK, linewidth=1.4, zorder=5)
hx = np.linspace(-0.5, 2.5, 200)
ax2.plot(hx, 0.5*hx-0.25, ls='-', color=C.INK, lw=1.3)
label(ax2, r'$h_1-2h_2=\frac{1}{2}$', (0.0, 1.2), fontsize=9)
label(ax2, '$(1,0)$ 与 $(0,1)$ 重合', (0.45, -0.40), fontsize=8)
label(ax2, '判为 1', (1.42, -0.1), offset=(4, -2), fontsize=8)
label(ax2, '标签 0', (2, 1), offset=(-7, 7), ha='right', fontsize=8)
fig.tight_layout(w_pad=2.0)
save(fig, "M7-n1")

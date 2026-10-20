import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

assert np.isclose(2.0, 2) and np.isclose(1/2, .5)
# 曲率半径 R=(1+y'^2)^(3/2)/|y''|，在 (1,1) 处约为 5.59
R = (1 + 2**2)**1.5 / 2
assert np.isclose(R, 5.59017, atol=1e-4)
fig, ax = new_fig(12, 7.5)
x = np.linspace(-1.2, 1.2, 700)
ax.plot(x, x**2, color=C.INK, ls='-', lw=1.8)
theta = np.linspace(0, 2*np.pi, 700)
ax.plot(.5*np.cos(theta), .5 + .5*np.sin(theta), color=C.GRAY, ls='--', lw=1.2)
ax.plot([-.07, .07], [.5, .5], color=C.INK, lw=1.0)
ax.plot([0, 0], [.43, .57], color=C.INK, lw=1.0)
ax.scatter([0], [0], s=28, color=C.INK, zorder=5)
# (1,1) 处的切线是 y=2x-1；端点按作者指定，直线需过 (1,1) 且斜率为 2
p0 = np.array([0.85, 0.70])
p1 = np.array([1.15, 1.30])
m_tan = (p1[1] - p0[1]) / (p1[0] - p0[0])
assert np.isclose(m_tan, 2)
assert np.isclose(p0[1] + m_tan * (1 - p0[0]), 1)      # 过 (1,1)
assert np.isclose(p0[1], 2 * p0[0] - 1) and np.isclose(p1[1], 2 * p1[0] - 1)
ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=C.GRAY, ls=':', lw=1.1)
label(ax, r'曲率圆：半径 $\frac{1}{2}$', (0, -.18), offset=(0, 0), ha='center', va='center')
# 放在曲率圆上方的空白处，避开抛物线和图边
label(ax, '(1,1) 处曲率半径\n约 5.59，弯得缓得多', (-.45, 1.43), offset=(0, 0), ha='left', va='top')
ax.set(xlim=(-1.2, 1.2), ylim=(-.3, 1.5), xlabel='$x$', ylabel='$y$')
ax.set_aspect('equal', adjustable='box')
save(fig, 'C8-n5')

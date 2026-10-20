import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

# 参数曲线 x=g(t)=t^2, y=f(t)=t^3, t in [0,1]；弦斜率 1；切线斜率 f'/g' = 3t/2 = 1 => t = 2/3
xi = 2 / 3
assert abs(1.5 * xi - 1) < 1e-12
t = np.linspace(0, 1, 400)
x, y = t**2, t**3
xc, yc = xi**2, xi**3
tx = np.array([xc - 0.35, xc + 0.35])
ty = yc + 1.0 * (tx - xc)

fig, ax = new_fig(12, 8)
ax.plot(x, y, color=C.INK, ls='-', lw=1.8)
ax.plot([0, 1], [0, 1], color=C.GRAY, ls='--', lw=1.5)
ax.plot(tx, ty, color=C.INK, ls=':', lw=1.7)
dot(ax, (0, 0), '原点', offset=(-38, 6), color=C.INK)
dot(ax, (1, 1), '终点 $t=1$', offset=(-70, 4), color=C.INK)
ax.scatter([xc], [yc], s=40, facecolors=C.PAPER, edgecolors=C.INK, zorder=6)
label(ax, r'切点 $t=\xi=\frac{2}{3}$', (xc, yc), offset=(-12, 10), ha='right')
label(ax, '弦（虚线）：斜率 $f(b)/g(b)=1$', (0.0, 0.72), offset=(0, 0), ha='left')
label(ax, "切线（点线）：斜率 $f'(\\xi)/g'(\\xi)=1$", (0.62, 0.2), offset=(0, 0), ha='left')
ax.set(xlabel='$x=g(t)=t^2$', ylabel='$y=f(t)=t^3$', xlim=(-0.1, 1.7), ylim=(-0.1, 1.15))
ax.set_aspect('equal', adjustable='box')
save(fig, 'C7-n1')

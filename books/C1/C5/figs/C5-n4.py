import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(18, 9.5)
fig.subplots_adjust(left=0.07, right=0.98, bottom=0.15, top=0.95)
p = np.array([[0, 0], [1, 2], [3, 2], [4, 0]])
ax.plot(p[:, 0], p[:, 1], color=C.GRAY, ls='--')
ax.scatter(p[:, 0], p[:, 1], s=30, marker='s', color=C.INK, zorder=5)
for i, point in enumerate(p):
    label(ax, f'$P_{i}$', point, (0, 12 if i in (1, 2) else -18), ha='center')
t = np.linspace(0, 1, 600)
ax.plot(3*t+3*t*t-2*t**3, 6*t-6*t*t, color=C.INK, ls='-')
for t0, offset in ((0.25, (25, -42)), (0.5, (28, -33))):
    x, y = 3*t0+3*t0**2-2*t0**3, 6*t0-6*t0**2
    slope = (6-12*t0)/(3+6*t0-6*t0**2)
    xs = np.array([x-0.42, x+0.42])
    ax.plot(xs, y+slope*(xs-x), color=C.RED, ls=':', lw=1.4)
    dot(ax, (x, y), size=25)
    text = r'$t=\frac{1}{4}$，斜率 $\frac{8}{11}$' if t0 == 0.25 else r'$t=\frac{1}{2}$，斜率 $0$'
    label(ax, text, (x, y), offset, ha='center', fontsize=10)
# 两句话放到控制线段的外侧（左、右），并用细引线指到线段上。
label(ax, '起点处切线\n沿虚线 $P_0P_1$', (0.275, 0.55), (-28, 0),
      ha='right', va='center', fontsize=8.5,
      arrowprops=dict(arrowstyle='-', color=C.GRAY, lw=0.6, shrinkA=2, shrinkB=1))
label(ax, '终点处切线\n沿虚线 $P_2P_3$', (3.725, 0.55), (20, 0),
      ha='left', va='center', fontsize=8.5,
      arrowprops=dict(arrowstyle='-', color=C.GRAY, lw=0.6, shrinkA=2, shrinkB=1))
ax.axhline(0, color=C.GRAY, lw=0.7)
ax.axvline(0, color=C.GRAY, lw=0.7)
ax.set(xlim=(-1.15, 5.05), ylim=(-0.45, 2.55), xlabel='$x$', ylabel='$y$')
ax.set_xticks([0, 1, 2, 3, 4]); ax.set_yticks([0, 1, 1.5, 2])
ax.set_aspect('equal')
assert np.isclose(3/4+3/16-2/64, 29/32)
assert np.isclose((6-12/4)/(3+6/4-6/16), 8/11)
save(fig, "C5-n4")

import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(16, 10)
x0, A, eps = 2.0, 4.0, 0.5
delta = min(1, eps / 5)
assert (x0-delta)**2 > A-eps and (x0+delta)**2 < A+eps
ax.axhspan(A-eps, A+eps, color=C.LIGHT, zorder=0)
for y, text in [(4.5, r'$A+\varepsilon=4.5$'), (3.5, r'$A-\varepsilon=3.5$'), (4, '$A=4$')]:
    ax.axhline(y, color=C.GRAY, ls=':' if y == 4 else '--', lw=0.9)
    label(ax, text, (2.49, y), offset=(-2, 5), ha='right', fontsize=9)
for v in [x0-delta, x0+delta]:
    ax.axvline(v, color=C.GRAY, ls='--', lw=0.9)
# 竖虚线 x=x0 保留；函数在 x0 处有定义。
ax.axvline(x0, color=C.GRAY, ls='--', lw=0.9)
x = np.linspace(1.5, 2.5, 1001)
ax.plot(x, x*x, color=C.INK, ls='-', lw=1.3)
xw = np.linspace(x0-delta, x0+delta, 301)
ax.plot(xw, xw*xw, color=C.INK, ls='-', lw=3)
# (x0, A) 在曲线上：实心点表示函数有定义。
ax.scatter([x0], [A], s=50, color=C.INK, zorder=5)
# 横轴上的空心点只表示去心邻域不含 x0。
ax.scatter([x0], [2.5], s=50, facecolors=C.PAPER, edgecolors=C.INK,
           linewidths=1.0, zorder=6, clip_on=False)
label(ax, r'去心邻域不含 $x_0$', (2.15, 2.62), ha='left', va='bottom', fontsize=8.5)
arrow(ax, (2.15, 2.64), (-0.115, -0.10), color=C.INK, lw=0.6)
label(ax, '$y=x^2$', (2.28, 5.55))
ax.set(xlim=(1.5, 2.5), ylim=(2.5, 6), xlabel='$x$', ylabel='$y$')
ax.set_xticks([1.5, 1.9, 2, 2.1, 2.5], ['1.5', '1.9\n'+r'$x_0-\delta$', '2\n$x_0$', '2.1\n'+r'$x_0+\delta$', '2.5'])
ax.set_yticks([2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6])
fig.subplots_adjust(left=0.12, right=0.97, bottom=0.22, top=0.96)
save(fig, "C2-n1")

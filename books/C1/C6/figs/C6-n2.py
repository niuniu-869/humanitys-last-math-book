import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, axes = new_fig(18, 5.8, ncols=3)

# 缺连续：右端点断开。
ax = axes[0]
x = np.linspace(0, 0.999, 300)
ax.plot(x, x, color=C.INK, ls='-')
ax.scatter([1], [1], s=34, facecolors=C.PAPER, edgecolors=C.INK, zorder=5)
ax.scatter([1], [0], s=28, color=C.INK, zorder=5)
label(ax, '右端点断开', (0.5, 1.22), ha='center')
ax.set(xlim=(-0.12, 1.12), ylim=(-0.12, 1.35), xlabel='$x$', ylabel='$f(x)$', aspect='equal')

# 缺可导：谷底尖角。
ax = axes[1]
x = np.linspace(-1, 1, 300)
ax.plot(x, np.abs(x), color=C.INK, ls='-')
ax.scatter([-1, 1], [1, 1], s=28, color=C.INK, zorder=5)
label(ax, '谷底是尖角', (0, 1.22), ha='center')
ax.set(xlim=(-1.15, 1.15), ylim=(-0.12, 1.35), xlabel='$x$', ylabel='$f(x)$', aspect='equal')

# 缺等高：两端不等高。
ax = axes[2]
x = np.linspace(0, 1, 300)
ax.plot(x, x, color=C.INK, ls='-')
ax.scatter([0, 1], [0, 1], s=28, color=C.INK, zorder=5)
label(ax, '两端不等高', (0.5, 1.22), ha='center')
ax.set(xlim=(-0.12, 1.12), ylim=(-0.12, 1.35), xlabel='$x$', ylabel='$f(x)$', aspect='equal')

axes[0].set_xlabel('$x$\n两端等高，内部斜率处处为 1', fontsize=9)
axes[1].set_xlabel('$x$\n原点处没有切线', fontsize=9)
axes[2].set_xlabel('$x$\n斜率恒为 1', fontsize=9)
fig.tight_layout(w_pad=1.6)
save(fig, 'C6-n2')

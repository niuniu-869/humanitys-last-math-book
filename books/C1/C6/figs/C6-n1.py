import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, axes = new_fig(18, 5.8, ncols=3)

# 山顶：两条割线的斜率分别为 0.6 和 -0.6。
ax = axes[0]
x = np.linspace(-0.2, 2.2, 400)
y = 2 - (x - 1) ** 2
ax.plot(x, y, color=C.INK, ls='-')
ax.plot([-0.05, 2.05], [2, 2], color=C.GRAY, ls='--', lw=1.1)
ax.plot([0.4, 1], [1.64, 2], color=C.GRAY, ls=':')
ax.plot([1, 1.6], [2, 1.64], color=C.GRAY, ls=':')
ax.scatter([1], [2], s=34, facecolors=C.INK, edgecolors=C.INK, zorder=5)
ax.set(xlim=(-0.2, 2.2), ylim=(-0.15, 2.35), xlabel='$x$', ylabel='$f(x)$', aspect='equal')

# x^3：原点切线水平但不是极值。
ax = axes[1]
x = np.linspace(-1.2, 1.2, 400)
ax.plot(x, x**3, color=C.INK, ls='-')
ax.plot([-0.75, 0.75], [0, 0], color=C.GRAY, ls='--', lw=1.1)
ax.scatter([0], [0], s=30, facecolors=C.INK, edgecolors=C.INK, zorder=5)
ax.set(xlim=(-1.2, 1.2), ylim=(-1.75, 1.75), xlabel='$x$', ylabel='$f(x)$', aspect='equal')

# |x|：谷底存在，但尖角处没有切线。
ax = axes[2]
x = np.linspace(-1.2, 1.2, 300)
ax.plot(x, np.abs(x), color=C.INK, ls='-')
ax.scatter([0], [0], s=34, facecolors=C.INK, edgecolors=C.INK, zorder=5)
ax.set(xlim=(-1.2, 1.2), ylim=(-0.15, 1.45), xlabel='$x$', ylabel='$f(x)$', aspect='equal')

axes[0].set_xlabel('$x$\n虚线：切线，$f\'(x_0)=0$\n点线：割线，左边斜率 $\\geq0$\n右边斜率 $\\leq0$', fontsize=9)
axes[1].set_xlabel("$x$\n$f'(0)=0$，但 0 不是极值", fontsize=9)
axes[2].set_xlabel("$x$\n尖角：$f'(0)$ 不存在", fontsize=9)
fig.tight_layout(w_pad=1.6)
save(fig, 'C6-n1')

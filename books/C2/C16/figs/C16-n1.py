import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(12, 8.5)

# 方波：在跳跃点 x=0 处断开
left = np.linspace(-np.pi, 0, 400, endpoint=False)
right = np.linspace(0, np.pi, 400, endpoint=False)[1:]
ax.plot(left, -np.ones_like(left), color=C.LIGHT, lw=4.0, ls='-', solid_capstyle='butt', zorder=1)
ax.plot(right, np.ones_like(right), color=C.LIGHT, lw=4.0, ls='-', solid_capstyle='butt', zorder=1)

x = np.linspace(-np.pi, np.pi, 1601)
def partial_sum(n, xx=x):
    odd = np.arange(1, n + 1, 2)
    return (4 / np.pi) * sum(np.sin(k * xx) / k for k in odd)

s1 = partial_sum(1)
s3 = partial_sum(3)
s7 = partial_sum(7)
ax.plot(x, s1, color=C.GRAY, lw=1.5, ls='--', zorder=2)
ax.plot(x, s3, color=C.TEAL, lw=1.5, ls=':', zorder=3)
ax.plot(x, s7, color=C.INK, lw=1.6, ls='-', zorder=4)

# 坐标与刻度
ax.set_xlim(-np.pi, np.pi)
ax.set_ylim(-1.4, 1.4)
ax.set_xticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi])
ax.set_xticklabels([r'$-\pi$', r'$-\frac{\pi}{2}$', r'$0$', r'$\frac{\pi}{2}$', r'$\pi$'])
ax.set_yticks([-1, 0, 1])
ax.set_xlabel(r'$x$')
ax.set_ylabel(r'$y$')
ax.axhline(0, color=C.LIGHT, lw=0.8, ls='-', zorder=0)

# 错开放置曲线标签
label(ax, r'$S_1$', (1.05, 1.32), color=C.GRAY, ha='center', va='center')
label(ax, r'$S_3$', (np.pi/2, (4/np.pi)*(1-1/3)), offset=(8, -14), color=C.TEAL)
label(ax, r'$S_7$', (np.pi/2, partial_sum(7, np.pi/2)),
      offset=(0, 18), ha='center', va='center', color=C.INK)

assert np.allclose([partial_sum(n, 0) for n in (1, 3, 7)], 0)
assert np.allclose([partial_sum(n, np.pi/2) for n in (1, 3, 7)],
                   [4/np.pi, 8/(3*np.pi), 304/(105*np.pi)])

dot(ax, (0, 0), size=26)
label(ax, r'$\frac{-1+1}{2}=0$', (0, 0), offset=(9, 11))

fig.subplots_adjust(left=0.10, right=0.98, bottom=0.14, top=0.96)
save(fig, "C16-n1")

import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

# 上下两幅：上为奇延拓（锯齿波），下为偶延拓（屋顶形），避免两条线在上升段重合看不清
fig, (ax1, ax2) = new_fig(12, 10.5, nrows=2, sharex=True)

xmin, xmax = -3*np.pi, 3*np.pi
x = np.arange(-3, 4) * np.pi
xx0 = np.linspace(0, np.pi, 300)

# 上：奇延拓
for k in range(-2, 3):
    a, b = -np.pi + 2*k*np.pi, np.pi + 2*k*np.pi
    lo, hi = max(a, xmin), min(b, xmax)
    if hi > lo:
        xx = np.linspace(lo, hi, 500)
        ax1.plot(xx, xx - 2*k*np.pi, color=C.INK, lw=1.25, ls='-', zorder=3)
ax1.plot(xx0, xx0, color=C.INK, lw=3.2, ls='-', zorder=5)
for xp in (-3*np.pi, -np.pi, np.pi, 3*np.pi):
    ax1.scatter([xp, xp], [np.pi, -np.pi], s=30, facecolors=C.PAPER,
                edgecolors=C.INK, linewidths=1.0, zorder=6, clip_on=False)
    ax1.scatter([xp], [0], s=30, color=C.INK, zorder=6, clip_on=False)
ax1.axvline(np.pi, color=C.GRAY, lw=1.0, ls=':', zorder=1)
ax1.set_title('奇延拓（锯齿波）', loc='left')
label(ax1, r'$f(x)=x$', (0.4*np.pi, 0.4*np.pi), offset=(-15, 20))
label(ax1, '空心：单侧极限', (-2.85*np.pi, 2.35))
label(ax1, '实心：级数和 0', (0, -2.7), ha='center')

# 下：偶延拓
roof = np.abs((x + np.pi) % (2*np.pi) - np.pi)
ax2.plot(x, roof, color=C.INK, lw=1.4, ls='--', zorder=3)
ax2.plot(xx0, xx0, color=C.INK, lw=3.2, ls='-', zorder=5)
ax2.axvline(np.pi, color=C.GRAY, lw=1.0, ls=':', zorder=1)
ax2.set_title('偶延拓（屋顶形）', loc='left')
label(ax2, r'$f(x)=x$', (0.4*np.pi, 0.4*np.pi), offset=(-15, 20))
assert np.allclose(roof, [np.pi, 0, np.pi, 0, np.pi, 0, np.pi])

for ax in (ax1, ax2):
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(-3.6, 3.6)
    ax.set_yticks([-np.pi, 0, np.pi])
    ax.set_yticklabels([r'$-\pi$', r'$0$', r'$\pi$'])
    ax.axhline(0, color=C.LIGHT, lw=0.8, zorder=0)
    ax.set_ylabel(r'$y$')
ax2.set_xticks([-3*np.pi, -2*np.pi, -np.pi, 0, np.pi, 2*np.pi, 3*np.pi])
ax2.set_xticklabels([r'$-3\pi$', r'$-2\pi$', r'$-\pi$', r'$0$', r'$\pi$', r'$2\pi$', r'$3\pi$'])
ax2.set_xlabel(r'$x$')

fig.subplots_adjust(left=0.09, right=0.98, bottom=0.09, top=0.95, hspace=0.25)
save(fig, "C16-n2")

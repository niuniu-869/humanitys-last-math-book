import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, axs = new_fig(18, 18, nrows=2, ncols=2)
fig.subplots_adjust(left=0.05, right=0.97, bottom=0.04, top=0.94, wspace=0.30, hspace=0.30)

def polar_frame(ax, radius, limits):
    ts = np.linspace(0, 2*np.pi, 600)
    for r in np.arange(0.5, radius+0.01, 0.5):
        ax.plot(r*np.cos(ts), r*np.sin(ts), color=C.LIGHT, ls=':', lw=0.55, zorder=0)
    arrow(ax, (0, 0), (radius*1.12, 0), color=C.GRAY, lw=0.7)
    dot(ax, (0, 0), '$O$', offset=(8, -22), size=12)
    label(ax, '极轴', (radius*1.12, 0), (0, -17), ha='center', fontsize=8)
    ax.set_xlim(*limits[0]); ax.set_ylim(*limits[1]); ax.set_aspect('equal')
    ax.set_xticks([]); ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

ax = axs[0, 0]
polar_frame(ax, 2, ((-2.4, 2.7), (-2.3, 2.3)))
t = np.linspace(0, 2*np.pi, 1001); r = 1+np.cos(t)
ax.plot(r*np.cos(t), r*np.sin(t), color=C.INK, ls='-')
dot(ax, (2, 0), '$r=2$', offset=(10, 18), size=18)
label(ax, '心尖', (0, 0), (-45, 24), fontsize=9,
      arrowprops=dict(arrowstyle='-', color=C.GRAY, lw=0.7))
ax.set_title(r'心形线 $r=1+\cos\theta$')

ax = axs[0, 1]
polar_frame(ax, 1, ((-1.45, 1.55), (-1.35, 1.35)))
for center in (0, np.pi):
    t = np.linspace(center-np.pi/4, center+np.pi/4, 601)
    r = np.sqrt(np.maximum(0, np.cos(2*t))); r[[0, -1]] = 0
    ax.plot(r*np.cos(t), r*np.sin(t), color=C.INK, ls='-')
# 两个 r=0 的方向是与极轴成 ±45° 的两条斜线，不是竖直方向。
L = 1.20
for sgn in (1, -1):
    ax.plot([-L/np.sqrt(2), L/np.sqrt(2)], [-sgn*L/np.sqrt(2), sgn*L/np.sqrt(2)],
            color=C.GRAY, ls=':', lw=0.7, zorder=1)
label(ax, r'$\theta=\frac{\pi}{4}$', (L/np.sqrt(2), L/np.sqrt(2)), (7, 4),
      ha='left', va='center', fontsize=8)
label(ax, r'$\theta=-\frac{\pi}{4}$', (L/np.sqrt(2), -L/np.sqrt(2)), (7, -4),
      ha='left', va='center', fontsize=8)
label(ax, r'两瓣在这两个方向上相接，$r=0$', (0, 1.10), (0, 0),
      ha='center', va='bottom', fontsize=8.5)
ax.set_title(r'双纽线 $r^2=\cos2\theta$')

ax = axs[1, 0]
polar_frame(ax, 4*np.pi, ((-15, 17), (-15, 15)))
t = np.linspace(0, 4*np.pi, 3000)
ax.plot(t*np.cos(t), t*np.sin(t), color=C.INK, ls='-')
dot(ax, (2*np.pi, 0), r'$2\pi$', offset=(0, -17), size=18)
ax.scatter([4*np.pi], [0], marker='s', s=20, color=C.INK, zorder=5)
label(ax, r'$4\pi$', (4*np.pi, 0), (15, -32), ha='center')
for r in (2*np.pi, 4*np.pi):
    ax.plot([r, r], [0.4, 3.2], color=C.GRAY, ls=':', lw=0.7)
ax.annotate('', xy=(4*np.pi, 2.8), xytext=(2*np.pi, 2.8),
            arrowprops=dict(arrowstyle='<->', color=C.INK, lw=0.8))
label(ax, r'间距 $2\pi$', (3*np.pi, 2.8), (0, 8), ha='center', fontsize=9)
ax.set_title(r'阿基米德螺线 $r=\theta$')

ax = axs[1, 1]
polar_frame(ax, 1, ((-1.5, 1.65), (-1.4, 1.4)))
# Only nonnegative radii: split the petal crossing theta=0 at the domain boundary.
intervals = [(0, np.pi/6), (np.pi/2, 5*np.pi/6),
             (7*np.pi/6, 3*np.pi/2), (11*np.pi/6, 2*np.pi)]
for lo, hi in intervals:
    t = np.linspace(lo, hi, 501); r = np.maximum(0, np.cos(3*t))
    ax.plot(r*np.cos(t), r*np.sin(t), color=C.INK, ls='-')
for t, text, offset in [(0, r'$\theta=0$', (0, 16)),
                         (2*np.pi/3, r'$\theta=\frac{2\pi}{3}$', (-9, 13)),
                         (4*np.pi/3, r'$\theta=\frac{4\pi}{3}$', (-9, -25))]:
    dot(ax, (np.cos(t), np.sin(t)), text, offset=offset, size=18)
ax.set_title(r'三叶玫瑰线 $r=\cos3\theta$')
save(fig, "C5-n5")

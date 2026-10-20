import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Polygon, Arc

t0 = np.deg2rad(35); x0, y0 = np.sin(t0), np.cos(t0)
fig, ax = new_fig(8.5, 7.5)
th = np.linspace(0, np.pi/2, 300); ax.plot(np.cos(th), np.sin(th), color=C.INK, lw=1.8)
ax.fill_between(np.cos(th), 0, np.sin(th), color=C.LIGHT, zorder=0)
ax.plot([0,1.08],[0,0], color=C.INK, lw=1.1); ax.plot([0,0],[0,1.08], color=C.INK, lw=1.1)
dx=.06; ax.add_patch(Polygon([(x0-dx/2,0),(x0+dx/2,0),(x0+dx/2,y0),(x0-dx/2,y0)], facecolor=C.GRAY, alpha=.7, edgecolor=C.INK, lw=1.1))
ax.plot([0,x0],[0,y0], color=C.INK, ls='--', lw=1.1)
ax.add_patch(Arc((0,0), .28,.28, angle=0, theta1=55, theta2=90, color=C.INK, lw=1.1))
label(ax, r'$t$', (.10,.22)); label(ax, r'$\mathrm{d}x=\cos t\,\mathrm{d}t$', (x0+.07,.16), fontsize=9)
label(ax, r'高 $\sqrt{1-x^2}=\cos t$', (x0+.07,.32), fontsize=9)
label(ax, r'$x=\sin t_0$', (x0,-.10), ha='center', va='top'); label(ax, r'面积 $\frac{\pi}{4}$', (.80,.50), ha='center')
label(ax, r'$t$ 从 $0$ 到 $\frac{\pi}{2}$', (.30,.64), ha='center', fontsize=9)
ax.set(xlim=(-.12,1.15), ylim=(-.16,1.16), aspect='equal'); ax.axis('off'); save(fig,'C11-n2')

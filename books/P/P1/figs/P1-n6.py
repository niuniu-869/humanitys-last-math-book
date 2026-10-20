import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle, Arc

l, d = 1.0, 2.0
fig, (ax1, ax2) = new_fig(17, 7, ncols=2, gridspec_kw={'width_ratios': [1, 1.25]})
ax1.set(xlim=(0, 6), ylim=(0, 5), aspect='equal'); ax1.axis('off')
ax1.plot([.6, 5.4], [1, 1], color=C.INK, lw=1.2); ax1.plot([.6, 5.4], [4, 4], color=C.INK, lw=1.2)
cx, ang = 3.0, np.deg2rad(48)
scale = 3/d
half = scale*l/2*np.array([np.cos(ang), np.sin(ang)])
cy = 1 + half[1]
p1, p2 = np.array([cx, cy])-half, np.array([cx, cy])+half
ax1.plot([p1[0], p2[0]], [p1[1], p2[1]], color=C.INK, lw=3)
ax1.plot([cx, cx], [cy, 1], color=C.GRAY, lw=1, ls='--')
ax1.plot([p1[0], p1[0]], [p1[1], cy], color=C.GRAY, lw=1, ls=':')
ax1.plot([p1[0], 4.1], [cy, cy], color=C.GRAY, lw=.8, ls=':')
ax1.add_patch(Arc((cx, cy), .7, .7, theta1=0, theta2=np.degrees(ang), color=C.INK))
dot(ax1, (cx, cy), size=12)
label(ax1, '$\\varphi$', (3.48, cy+.13), ha='left')
label(ax1, '$x$', (3.12, (cy+1)/2), ha='left')
label(ax1, '$\\frac{l}{2}\\sin\\varphi$', (2.34, (cy+1)/2), ha='right')
label(ax1, '$l$', (2.85, 2.2), ha='center')
ax1.annotate('', xy=(5, 4), xytext=(5, 1), arrowprops=dict(arrowstyle='<->', color=C.INK, lw=1))
label(ax1, '$d$', (5.15, 2.5), va='center')
assert np.isclose(p1[1], 1) and np.isclose(np.linalg.norm(p2-p1)/scale, l)
assert np.isclose((cy-1)/scale, l/2*np.sin(ang))
assert np.isclose((l/2)/(np.pi*d/4), 2*l/(np.pi*d))
label(ax1, '$x=\\frac{l}{2}\\sin\\varphi$ 时恰好碰到', (3, .45), ha='center', fontsize=9)
ax2.add_patch(Rectangle((0, 0), np.pi/2, d/2, facecolor=C.PAPER, edgecolor=C.INK, lw=1.2))
phi = np.linspace(0, np.pi/2, 400); curve = l/2*np.sin(phi)
ax2.fill_between(phi, 0, curve, color=C.LIGHT); ax2.plot(phi, curve, color=C.INK, lw=1.5)
label(ax2, '阴影 = 相交', (1.02, .16), ha='center', fontsize=9)
label(ax2, '面积 $\\frac{l}{2}$', (1.02, .06), ha='center', fontsize=9)
label(ax2, '$x=\\frac{l}{2}\\sin\\varphi$', (.9, .58), ha='center', fontsize=9)
label(ax2, '长方形总面积 $\\frac{\\pi d}{4}$', (np.pi/4, d/2), offset=(0, 7), ha='center', va='bottom', fontsize=9)
ax2.set(xlim=(0, np.pi/2), ylim=(0, d/2), xlabel='$\\varphi$', ylabel='$x$')
ax2.set_xticks([0, np.pi/2]); ax2.set_xticklabels(['0', '$\\frac{\\pi}{2}$']); ax2.set_yticks([0, d/2]); ax2.set_yticklabels(['0', '$\\frac{d}{2}$'])
save(fig, 'P1-n6')

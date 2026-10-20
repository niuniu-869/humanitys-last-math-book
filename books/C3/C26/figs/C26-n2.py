import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from mpl_toolkits.mplot3d import proj3d

def sph(r, ph, th):
    return np.array([r*np.sin(ph)*np.cos(th), r*np.sin(ph)*np.sin(th), r*np.cos(ph)])

fig, ax = new_fig3d(14, 11, elev=26, azim=-35)
ax.computed_zorder = False
ph, th = np.deg2rad([50, 35])
dr, dph, dth = 0.3, 0.3, 0.3
P = sph(1, ph, th)
Q = P * [1, 1, 0]
assert np.isclose(np.linalg.norm(P), 1)
assert np.isclose(np.linalg.norm(Q), np.sin(ph))

# 坐标轴（细实线，轴端标 x、y、z）
axes = [(np.array([1.22, 0, 0]), r'$x$', (5, -1), 'left', 'center'),
        (np.array([0, 1.22, 0]), r'$y$', (4, 3), 'left', 'center'),
        (np.array([0, 0, 1.28]), r'$z$', (0, 5), 'center', 'bottom')]
for end, text, off, ha, va in axes:
    ax.plot(*np.array([np.zeros(3), end]).T, color=C.GRAY, lw=0.9, ls='-', zorder=2)

# OP 实线，OP' 虚线，PP' 点线
for points, ls in [(np.array([np.zeros(3), P]), '-'),
                   (np.array([np.zeros(3), Q]), '--'),
                   (np.array([P, Q]), ':')]:
    ax.plot(*points.T, color=C.INK, lw=1.1, ls=ls, zorder=3)

# 过 P 的经线和纬线各画一段点线
t_mer = np.linspace(np.deg2rad(10), np.deg2rad(80), 110)
t_par = np.linspace(0, np.deg2rad(50), 110)
ax.plot(*np.array([sph(1, s, th) for s in t_mer]).T, color=C.GRAY, lw=1, ls=':', zorder=1)
ax.plot(*np.array([sph(1, ph, s) for s in t_par]).T, color=C.GRAY, lw=1, ls=':', zorder=1)

# 角 φ（z 轴到 OP）与角 θ（x 轴到 OP'）的小弧
ax.plot(*np.array([sph(0.28, s, th) for s in np.linspace(0, ph, 40)]).T,
        color=C.INK, lw=0.9, ls='-', zorder=3)
ax.plot(*np.array([[0.3*np.cos(s), 0.3*np.sin(s), 0] for s in np.linspace(0, th, 40)]).T,
        color=C.INK, lw=0.9, ls='-', zorder=3)

# 小块的三条边（放大到 0.3 / 0.3 / 0.3 sinφ，粗实线）
edges = [np.array([P, sph(1+dr, ph, th)]),
         np.array([sph(1, s, th) for s in np.linspace(ph, ph+dph, 100)]),
         np.array([sph(1, ph, s) for s in np.linspace(th, th+dth, 100)])]
for edge, exact in zip(edges, [dr, dph, np.sin(ph)*dth]):
    assert np.isclose(np.linalg.norm(np.diff(edge, axis=0), axis=1).sum(), exact, rtol=1e-5)
    ax.plot(*edge.T, color=C.INK, lw=3.2, ls='-', zorder=4)

ax.scatter(*P, s=30, color=C.INK, depthshade=False, zorder=10)
ax.scatter(*Q, s=48, facecolors=C.PAPER, edgecolors=C.INK, linewidths=1.1,
           depthshade=False, zorder=10)
ax.scatter(*np.zeros(3), s=14, color=C.INK, depthshade=False, zorder=11)

ax.set(xlim=(-0.54, 1.35), ylim=(-0.54, 1.35), zlim=(-0.32, 1.40))
ax.set_box_aspect((1, 1, 1), zoom=1.28); ax.set_axis_off()
fig.canvas.draw()

# 三维点先投影，再写标注
texts = [
    (r'$O$',      np.zeros(3),                (-11, -13), 'right', 'top'),
    (r'$P$',      P,                          (-18, -5),  'right', 'bottom'),
    (r"$P'$",     Q,                          (8,  -12),  'left',  'top'),
    (r'$\varphi$', sph(0.42, ph/2, th),       (-3,  1),   'center','center'),
    (r'$\theta$', (0.60*np.cos(np.deg2rad(12)), 0.60*np.sin(np.deg2rad(12)), 0), (0, 1.2), 'center','center'),
    (r'$\Delta\rho$', edges[0][-1],           (14, 10),   'left',  'bottom'),
    (r'$\rho\Delta\varphi$', edges[1][-1],    (10, -6),   'left',  'top'),
    (r'$\rho\sin\varphi\Delta\theta$', edges[2][-1], (0, 18), 'center', 'bottom'),
]
for text, point, offset, ha, va in texts:
    u, v, _ = proj3d.proj_transform(*point, ax.get_proj())
    label(ax, text, (u, v), offset=offset, ha=ha, va=va)

for end, text, off, ha, va in axes:
    p = end * (1.06 if end[2] == 0 else 1.02)
    u, v, _ = proj3d.proj_transform(*p, ax.get_proj())
    label(ax, text, (u, v), offset=off, ha=ha, va=va)

save(fig, "C26-n2")

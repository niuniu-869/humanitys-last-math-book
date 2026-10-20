import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(13, 10)
a, r, h = 2.1, 1.35, 2.5
O, A = np.array([0., 0.]), np.array([0., h])
B, Bp = np.array([-r, 0.]), np.array([r, 0.])
d = np.hypot(r, h)
beta = np.arctan2(r, h)
assert np.isclose(np.cos(beta), h/d)
ax.plot([-a, a], [0, 0], color=C.INK, lw=2, ls='-')
ax.plot([0, 0], [0, h], color=C.GRAY, lw=0.9, ls=':')
for point in (B, Bp):
    ax.plot(*np.array([A, point]).T, color=C.GRAY, lw=1.1, ls='--')
    ax.scatter(*point, s=46, facecolors=C.PAPER, edgecolors=C.INK, zorder=6)
dot(ax, O, '$O$', offset=(-15, -15), size=15)
dot(ax, A, '$A$', offset=(7, 9), size=28)
label(ax, '$B$', B, (-6, -18))
label(ax, "$B'$", Bp, (-7, -18))
label(ax, '$h$', (0, 0.7), (8, 0))
label(ax, '$d$', (-0.75*r, 0.25*h), (-17, 1))
label(ax, '$r$', (r/2, 0), (0, -17), ha='center')
# Dimension line for the disk radius stays below the force construction.
ax.annotate('', xy=(a, -0.47), xytext=(0, -0.47),
            arrowprops=dict(arrowstyle='<->', color=C.GRAY, lw=0.9))
for x in (0, a):
    ax.plot([x, x], [-0.37, -0.56], color=C.GRAY, lw=0.8, ls='-')
label(ax, '$a$', (a/2, -0.47), (0, -13), ha='center')
scale = 0.44
forces = [scale*(point-A) for point in (B, Bp)]
assert np.allclose(forces[0]+forces[1], [0, -2*scale*h])
vert_len, horiz_len = 0.88, 0.45
for s, force in zip((-1, 1), forces):
    arrow(ax, A, force, color=C.INK, lw=1.7)
    # 竖直分量：粗实线，起点在 A 的左右两侧，箭头停在力箭头尖端上方，
    # 避免两个箭头头叠在一起。
    V = A + np.array([s*abs(force[0]), 0.])
    arrow(ax, V, (0., -vert_len), color=C.INK, lw=2.6)
    # 水平分量：点线，从竖直分量上端向外指（左/右），箭头头单独画成实心小三角。
    end = V + np.array([s*horiz_len, 0.])
    ax.plot([V[0], end[0]], [V[1], end[1]], color=C.INK, lw=1.1, ls=':', zorder=4)
    back = end - np.array([s*0.04, 0.])
    ax.annotate('', xy=end, xytext=back,
                arrowprops=dict(arrowstyle='-|>', color=C.INK, lw=1.1,
                                shrinkA=0, shrinkB=0, mutation_scale=9),
                zorder=5)
t = np.linspace(0, beta, 50)
ax.plot(0.62*np.sin(t), h-0.62*np.cos(t), color=C.INK, lw=0.9, ls='-')
label(ax, r'$\beta$', (0.62*np.sin(beta/2), h-0.62*np.cos(beta/2)), (-1, -17))
ax.set(xlim=(-2.35, 2.35), ylim=(-0.85, 2.9))
ax.set_aspect('equal'); ax.set_axis_off()
fig.tight_layout(pad=0.5)
save(fig, "C26-n4")

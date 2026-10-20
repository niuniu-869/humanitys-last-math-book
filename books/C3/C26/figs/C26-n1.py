import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from mpl_toolkits.mplot3d import proj3d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

fig, ax = new_fig3d(13, 10, elev=24, azim=-108)
ax.computed_zorder = False
O, X, Y, Z = np.vstack((np.zeros(3), np.eye(3)))
ax.add_collection3d(Poly3DCollection([[O, X, Y]], facecolors=C.LIGHT, alpha=0.55, zorder=0))
ax.add_collection3d(Poly3DCollection([[X, Y, Z]], facecolors=C.LIGHT, alpha=0.30, zorder=0))
for p, q in ((O, X), (O, Y), (O, Z), (X, Y), (X, Z), (Y, Z)):
    ax.plot(*np.array([p, q]).T, color=C.INK, lw=1.3, ls='-')
x, y = 0.25, 0.30
z = 1 - x - y
assert np.isclose(z, 0.45)
ax.plot([x, x], [y, y], [0, z], color=C.INK, lw=2.8, ls='-')
ax.plot([x, x], [y, y], [z, 0.75], color=C.INK, lw=1.4, ls='--')
ax.scatter([x, x], [y, y], [0, z], s=52, facecolors=C.PAPER,
           edgecolors=C.INK, depthshade=False, zorder=10)
# A central dot keeps the base point solid while retaining its endpoint ring.
ax.scatter([x], [y], [0], s=10, color=C.INK, depthshade=False, zorder=11)
ax.set(xlim=(-0.08, 1.08), ylim=(-0.08, 1.08), zlim=(-0.05, 1.08))
ax.set_box_aspect((1, 1, 1)); ax.set_axis_off()
fig.canvas.draw()
for text, p, offset in [
    (r'$D_{xy}$', (0.45, 0.10, 0), (0, 7)),
    (r'$z_1=0$', (x, y, 0), (5, -27)),
    (r'$z_2=1-x-y$', (x, y, z), (55, 8)),
]:
    u, v, _ = proj3d.proj_transform(*p, ax.get_proj())
    label(ax, text, (u, v), offset=offset)
save(fig, "C26-n1")

import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from mpl_toolkits.mplot3d import proj3d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

fig, ax = new_fig3d(13, 10, elev=25, azim=-58)
base = np.array([[0.4, 0.4, 0], [1, 0.4, 0], [1, 0.9, 0], [0.4, 0.9, 0]])
dx, dy = 0.6, 0.5
top = base.copy()
top[:, 2] = 0.5 + 0.3*top[:, 0] + 0.5*top[:, 1]
a, b = top[1]-top[0], top[3]-top[0]
assert np.allclose(top[0], [0.4, 0.4, 0.82])
assert np.allclose(a, [0.6, 0, 0.18]) and np.allclose(b, [0, 0.5, 0.25])
assert np.isclose(np.linalg.norm(np.cross(a, b)), 0.3*np.sqrt(1.34))
for points, alpha in [(base, 0.55), (top, 0.38)]:
    ax.add_collection3d(Poly3DCollection([points], facecolors=C.LIGHT, alpha=alpha))
ax.plot(*base[[0, 1, 2, 3, 0]].T, color=C.INK, lw=1.1, ls='-')
ax.plot(*top[[1, 2, 3]].T, color=C.INK, lw=1.2, ls='--')
for p, q in zip(base, top):
    ax.plot(*np.array([p, q]).T, color=C.GRAY, lw=1, ls=':')
for vec in (a, b):
    ax.quiver(*top[0], *vec, color=C.INK, lw=1.8, arrow_length_ratio=0.13)
ax.set(xlim=(0.2, 1.2), ylim=(0.2, 1.05), zlim=(-0.08, 1.35))
ax.set_box_aspect((1.2, 1, 1.2)); ax.set_axis_off()
fig.canvas.draw()
for text, p, offset in [
    (r'$\boldsymbol{a}$', top[0]+0.5*a, (18, 7)),
    (r'$\boldsymbol{b}$', top[0]+0.5*b, (-18, 6)),
    (r'$\Delta x\,\Delta y$', base.mean(axis=0), (-14, -4)),
    (r'$\Delta x$', base[0] + [0.5*dx, -0.015, 0], (0, -6)),
    (r'$\Delta y$', base[0] + [0, 0.5*dy, 0], (0, 10)),
]:
    u, v, _ = proj3d.proj_transform(*p, ax.get_proj())
    kw = {}
    if text == r'$\Delta x$':
        kw = dict(ha='center', va='top')
    elif text == r'$\Delta y$':
        kw = dict(ha='center', va='bottom')
    label(ax, text, (u, v), offset=offset, **kw)
save(fig, "C26-n3")

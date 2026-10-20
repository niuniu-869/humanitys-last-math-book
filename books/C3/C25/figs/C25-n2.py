import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

fig, ax = new_fig3d(14, 11, elev=24, azim=-57)
a, b, c, d, x0, dx = 0., 1., 0., 1., .55, .07
t = np.linspace(0, 1, 100)
for x in (a, b):
    ax.plot(np.full_like(t, x), t, x*x+t*t, color=C.INK, alpha=.55)
    ax.plot([x, x], [c, d], [0, 0], color=C.INK, alpha=.55)
for y in (c, d):
    ax.plot(t, np.full_like(t, y), t*t+y*y, color=C.INK, alpha=.55)
    ax.plot([a, b], [y, y], [0, 0], color=C.INK, alpha=.55)
for x in (a, b):
    for y in (c, d):
        ax.plot([x, x], [y, y], [0, x*x+y*y], color=C.INK, alpha=.55)
faces = []
for x in (x0, x0+dx):
    faces.append([(x, c, 0), *zip(np.full_like(t, x), t, x*x+t*t), (x, d, 0)])
    ax.plot(np.full_like(t, x), t, x*x+t*t, color=C.INK, ls='--', alpha=.55)
faces.append([*zip(np.full_like(t, x0), t, x0*x0+t*t),
              *zip(np.full_like(t, x0+dx), t[::-1], (x0+dx)**2+t[::-1]**2)])
for y in (c, d):
    faces.append([(x0, y, 0), (x0+dx, y, 0),
                  (x0+dx, y, (x0+dx)**2+y*y), (x0, y, x0*x0+y*y)])
ax.add_collection3d(Poly3DCollection(faces, facecolor=C.LIGHT, edgecolor=C.GRAY,
                                   linewidth=.7, alpha=.5))
ax.text(x0, .54, .22, r'$A(x_0)$')
ax.plot([x0, x0+dx], [-.12, -.12], [0, 0], color=C.INK, alpha=.55)
for x in (x0, x0+dx):
    ax.plot([x, x], [-.15, -.09], [0, 0], color=C.INK, alpha=.55)
ax.text(x0+.15, -.18, -.10, r'$\mathrm{d}x$')
ax.set(xlim=(0, 1), ylim=(-.08, 1), zlim=(0, 2.05))
ax.set_xticks([a, x0, b], ['$a$', '$x_0$', '$b$'])
ax.set_yticks([c, d], ['$y=c$', '$y=d$'])
ax.set_zticks([]); ax.grid(False)
ax.set_box_aspect((1.15, 1, 1))
save(fig, "C25-n2")

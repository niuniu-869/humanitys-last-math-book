import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label


def project(p):
    p = np.asarray(p, dtype=float)
    return p @ np.array([[-0.55, -0.38], [1.25, -0.08], [0.0, 1.0]])


def setup(w=12, h=10):
    fig, ax = new_fig(w, h)
    ax.set_aspect('equal')
    ax.axis('off')
    return fig, ax


def line(ax, points, **kw):
    q = project(points)
    opts = dict(color=C.INK, lw=1.3, alpha=0.55, ls='-')
    opts.update(kw)
    ax.plot(q[:, 0], q[:, 1], **opts)


def vector(ax, start, end, lw=2):
    a, b = project([start, end])
    ax.annotate('', b, a, arrowprops=dict(arrowstyle='-|>', color=C.INK,
                lw=lw, alpha=0.55, shrinkA=0, shrinkB=0, mutation_scale=11))


def text(ax, p, s, off=(4, 4), **kw):
    return label(ax, s, project(p), offset=off, **kw)


def point(ax, p, hollow=False, square=False):
    ax.scatter(*project(p), s=28, marker='s' if square else 'o',
               facecolors=C.PAPER if hollow else C.INK,
               edgecolors=C.INK, alpha=0.55, zorder=8)


def axes(ax, limits, origin='$O$'):
    for i, (length, name) in enumerate(zip(limits, ['$x$', '$y$', '$z$'])):
        p = np.zeros(3)
        p[i] = length
        vector(ax, np.zeros(3), p, lw=0.8)
        text(ax, p, name, (2, 2), fontsize=9)
    text(ax, [0, 0, 0], origin, (-14, -4), fontsize=9)


def fill(ax, vertices):
    ax.add_patch(plt.Polygon(project(vertices), facecolor=C.LIGHT,
                            edgecolor='none', alpha=0.4))


def ring(radius, z, samples=181):
    t = np.linspace(0, 2*np.pi, samples)
    return np.column_stack((radius*np.cos(t), radius*np.sin(t), np.full_like(t, z)))


def bounds(ax, points, margin=0.6):
    q = project(points)
    ax.set_xlim(q[:, 0].min()-margin, q[:, 0].max()+margin)
    ax.set_ylim(q[:, 1].min()-margin, q[:, 1].max()+margin)

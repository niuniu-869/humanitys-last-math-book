"""手写的 3D→2D 正交投影，用来画三维示意图（matplotlib 的 3D 轴在这些图上不好控制）。"""
import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, save, label, HALO


class View:
    def __init__(self, az, el):
        a, e = np.radians(az), np.radians(el)
        self.v = np.array([np.cos(e)*np.cos(a), np.cos(e)*np.sin(a), np.sin(e)])
        self.r = np.array([-np.sin(a), np.cos(a), 0.0])
        self.u = np.array([-np.sin(e)*np.cos(a), -np.sin(e)*np.sin(a), np.cos(e)])

    def __call__(self, p):
        p = np.asarray(p, float)
        return np.stack([p @ self.r, p @ self.u], axis=-1)


def setup(w=12, h=9):
    fig, ax = new_fig(w, h)
    ax.set_aspect("equal"); ax.axis("off")
    return fig, ax


def line(ax, V, pts, **kw):
    q = V(np.array(pts)); kw.setdefault("color", C.INK); kw.setdefault("lw", 1.8)
    ax.plot(q[:, 0], q[:, 1], **kw)


def poly(ax, V, pts, fc="#D9D9D9", alpha=0.6, ec="#444444", ls="-", lw=1.0, hatch=None, z=1):
    q = V(np.array(pts))
    ax.add_patch(plt.Polygon(q, closed=True, facecolor=fc, alpha=alpha, edgecolor="none", hatch=hatch, zorder=z))
    ax.add_patch(plt.Polygon(q, closed=True, fill=False, edgecolor=ec, ls=ls, lw=lw, zorder=z))


def arrow3(ax, V, p, d, lw=2.4, ls="-", color=C.INK):
    a, b = V(p), V(np.asarray(p, float) + np.asarray(d, float))
    ax.annotate("", xy=b, xytext=a, zorder=6,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, ls=ls, shrinkA=0, shrinkB=0, mutation_scale=13), annotation_clip=False)


def dot3(ax, V, p, s=34):
    q = V(p); ax.scatter(*q, s=s, color=C.INK, zorder=8)


def text3(ax, V, p, s, off=(0, 0), **kw):
    q = V(p)
    ax.annotate(s, q, xytext=off, textcoords="offset points", path_effects=HALO, zorder=9, annotation_clip=False, **kw)

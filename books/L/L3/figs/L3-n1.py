import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Polygon


def setup(ax, lim=(-2, 3)):
    ax.set_xlim(*lim)
    ax.set_ylim(*lim)
    ax.set_aspect("equal", adjustable="box")
    ticks = range(-2, 4) if lim == (-2, 3) else [0, 1]
    ax.set_xticks(list(ticks))
    ax.set_yticks(list(ticks))
    ax.grid(True, color=C.LIGHT, lw=0.55)
    ax.axhline(0, color=C.GRAY, lw=0.8, zorder=0)
    ax.axvline(0, color=C.GRAY, lw=0.8, zorder=0)
    ax.tick_params(labelsize=7, length=2)


def draw_case(ax, title, col1, col2, projection=False):
    setup(ax, (-0.4, 1.6) if projection else (-2, 3))
    ax.set_title(title, pad=8)
    square = np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]], dtype=float)
    ax.plot(square[:, 0], square[:, 1], ls="--", color=C.GRAY, lw=1.1, zorder=2)
    if projection:
        t = np.linspace(-2, 3, 200)
        ax.plot(t, 2 * t, ls=":", color=C.GRAY, lw=1.1, zorder=1)
        label(ax, "y=2x", (0.75, 1.5), offset=(4, 0), fontsize=8)
        end = np.asarray(col1) + np.asarray(col2)
        ax.plot([0, end[0]], [0, end[1]], color=C.INK, lw=2.3, zorder=4)
        label(ax, "像：一条线段", end, offset=(8, -2), fontsize=8)
    else:
        p = np.array([[0, 0], col1, np.asarray(col1) + np.asarray(col2), col2], dtype=float)
        ax.add_patch(Polygon(p, closed=True, facecolor=C.LIGHT, edgecolor=C.INK, lw=1.4, zorder=3))
    off1 = (6, 6) if abs(col1[1]) >= abs(col1[0]) else (4, -14)
    off2 = (-34, 6) if col2[0] > 0 else (-12, -16)
    if projection:
        off1, off2 = (-44, 6), (10, -12)
    arrow(ax, (0, 0), col1, color=C.INK, text="第1列", lw=2.2, offset=off1)
    x2, y2 = col2
    ax.annotate("", xy=(x2, y2), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=C.INK, lw=2.0, linestyle="--",
                                shrinkA=0, shrinkB=0, mutation_scale=11), zorder=5)
    label(ax, "第2列", (x2, y2), offset=off2, color=C.INK)


fig, axes = new_fig(24, 7.0, nrows=1, ncols=4)
matrices = [
    ("开头的 A", (2, 0), (1, 1), False),
    ("旋转 90°", (0, 1), (-1, 0), False),
    ("错切（k=1）", (1, 0), (1, 1), False),
    ("投影到 y=2x（放大）", (0.2, 0.4), (0.4, 0.8), True),
]
for ax, (title, c1, c2, proj) in zip(axes, matrices):
    draw_case(ax, title, c1, c2, proj)
fig.subplots_adjust(wspace=0.35, top=0.82, bottom=0.15)
save(fig, "L3-n1")

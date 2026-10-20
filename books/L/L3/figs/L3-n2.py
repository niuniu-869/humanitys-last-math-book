import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Polygon, FancyArrowPatch


def flag_points():
    return np.array([[0, 0], [0, 2], [1, 1.5], [0, 1], [0, 0]], dtype=float)


def transform(points, kind):
    x, y = points[:, 0], points[:, 1]
    if kind == "R":
        return np.column_stack((-y, x))
    if kind == "F":
        return np.column_stack((x, -y))
    raise ValueError(kind)


def setup(ax):
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2.5, 2.5)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xticks([-2, -1, 0, 1, 2])
    ax.set_yticks([-2, -1, 0, 1, 2])
    ax.axhline(0, color=C.GRAY, lw=0.8, zorder=0)
    ax.axvline(0, color=C.GRAY, lw=0.8, zorder=0)
    ax.tick_params(labelsize=7, length=2)


def draw_flag(ax, pts, show_reference=True):
    setup(ax)
    if show_reference:
        base = flag_points()
        ax.plot(base[:, 0], base[:, 1], ls="--", color=C.GRAY, lw=1.0, zorder=1)
    ax.plot(pts[:, 0], pts[:, 1], color=C.INK, lw=1.5, zorder=3)
    ax.add_patch(Polygon(pts[1:4], closed=True, facecolor=C.LIGHT, edgecolor=C.INK, lw=1.3, zorder=2))
    ax.plot(pts[:2, 0], pts[:2, 1], color=C.INK, lw=2.0, zorder=4)


def add_connector(fig, left_ax, right_ax, text):
    a = left_ax.get_position()
    b = right_ax.get_position()
    y = (a.y0 + a.y1) / 2
    fig.add_artist(FancyArrowPatch((a.x1 + 0.012, y), (b.x0 - 0.045, y),
                                   transform=fig.transFigure, arrowstyle="-|>",
                                   color=C.INK, lw=1.2, mutation_scale=10))
    fig.text((a.x1 + b.x0 - 0.033) / 2, y + 0.025, text, ha="center", va="bottom", fontsize=8, color=C.INK)


base = flag_points()
R = transform(base, "R")
F = transform(base, "F")
FR = transform(R, "F")
RF = transform(F, "R")

fig, axes = new_fig(20, 12, nrows=2, ncols=3)
for ax in axes.flat:
    ax.set_box_aspect(1)

# 上排：先旋转再反射
for ax, pts in zip(axes[0], [base, R, FR]):
    draw_flag(ax, pts)
axes[0, 0].set_title("原旗", pad=8)
axes[0, 1].set_title("先 R：逆时针转 90°", pad=8)
axes[0, 2].set_title("再 F：关于 x 轴反射", pad=8)
t = np.linspace(-2.5, 2.5, 100)
axes[0, 2].plot(t, -t, ls=":", color=C.GRAY, lw=1.0, zorder=1)
label(axes[0, 2], "y=-x", (1.0, -1.0), offset=(4, 4), fontsize=8)

# 下排：先反射再旋转
for ax, pts in zip(axes[1], [base, F, RF]):
    draw_flag(ax, pts)
axes[1, 0].set_title("原旗", pad=8)
axes[1, 1].set_title("先 F：关于 x 轴反射", pad=8)
axes[1, 2].set_title("再 R：逆时针转 90°", pad=8)
axes[1, 2].plot(t, t, ls=":", color=C.GRAY, lw=1.0, zorder=1)
label(axes[1, 2], "y=x", (1.0, 1.0), offset=(4, 4), fontsize=8)

fig.subplots_adjust(wspace=0.45, hspace=0.55, left=0.05, right=0.97, top=0.91, bottom=0.08)
save(fig, "L3-n2")

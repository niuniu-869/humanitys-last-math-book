import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Polygon, FancyArrowPatch


def draw_flag(ax, matrix):
    ax.set(xlim=(-3, 3), ylim=(-1, 3), aspect="equal")
    ax.set_xticks(range(-3, 4))
    ax.set_yticks(range(-1, 4))
    ax.tick_params(labelsize=8, length=2)
    ax.axhline(0, color=C.GRAY, lw=0.8, zorder=0)
    ax.axvline(0, color=C.GRAY, lw=0.8, zorder=0)
    label(ax, "$x$", (2.85, 0), offset=(0, -15), ha="right")
    label(ax, "$y$", (0, 2.85), offset=(6, 0), va="top")
    ax.plot(*pole.T, color=C.GRAY, ls="--", lw=0.9, zorder=1)
    ax.add_patch(Polygon(face, fill=False, edgecolor=C.GRAY, ls="--", lw=0.9, zorder=1))
    p, f = pole @ matrix.T, face @ matrix.T
    ax.add_patch(Polygon(f, facecolor=C.LIGHT, edgecolor=C.INK, lw=1.3, zorder=2))
    ax.plot(*p.T, color=C.INK, ls="-", lw=2.4, zorder=3)


def connector(fig, left_ax, right_ax, text):
    a, b = left_ax.get_position(), right_ax.get_position()
    y = (a.y0+a.y1)/2
    fig.add_artist(FancyArrowPatch((a.x1+0.012, y), (b.x0-0.025, y),
        transform=fig.transFigure, arrowstyle="-|>", color=C.INK, lw=1.6, mutation_scale=14))
    fig.text((a.x1+b.x0)/2, y+0.035, text, color=C.INK, fontsize=9,
             ha="center", va="bottom")


def matrix_note(fig, ax, name, matrix):
    box = ax.get_position()
    x, y = box.x1+0.053, (box.y0+box.y1)/2
    fig.text(x-0.011, y, f"${name}=$", ha="right", va="center", color=C.INK)
    for i in range(2):
        for j in range(2):
            fig.text(x+0.018+0.030*j, y+0.018-0.036*i,
                     f"${matrix[i,j]}$", color=C.INK, ha="center", va="center")
    from matplotlib.lines import Line2D
    for bx, sign in ((x-0.002, 1), (x+0.067, -1)):
        fig.add_artist(Line2D([bx+sign*.006, bx, bx, bx+sign*.006],
            [y+.037, y+.037, y-.037, y-.037], transform=fig.transFigure, color=C.INK, lw=.8))


S = np.array([[1, 1], [0, 1]])
R = np.array([[0, -1], [1, 0]])
pole = np.array([[0, 0], [0, 2]])
face = np.array([[0, 2], [1, 1.5], [0, 1]])
SR, RS = S @ R, R @ S
assert np.array_equal(SR, [[1, -1], [1, 0]])
assert np.array_equal(RS, [[0, -1], [1, 1]])
assert np.array_equal(face @ SR.T, [[-2, 0], [-.5, 1], [-1, 0]])
assert np.array_equal(face @ RS.T, [[-2, 2], [-1.5, 2.5], [-1, 1]])

fig, axes = new_fig(32, 17, nrows=2, ncols=3)
fig.subplots_adjust(left=0.035, right=0.84, bottom=0.09, top=0.91, wspace=0.55, hspace=0.48)
for row, matrices in zip(axes, ((np.eye(2), R, SR), (np.eye(2), S, RS))):
    for ax, matrix in zip(row, matrices):
        draw_flag(ax, matrix)
for ax, title in zip(axes.flat, ("原旗", "转后", "再剪切后", "原旗", "剪切后", "再转后")):
    ax.set_title(title, pad=9)
fig.canvas.draw()
connector(fig, axes[0, 0], axes[0, 1], "③ 转 $90^\circ$")
connector(fig, axes[0, 1], axes[0, 2], "② 剪切")
connector(fig, axes[1, 0], axes[1, 1], "② 剪切")
connector(fig, axes[1, 1], axes[1, 2], "③ 转 $90^\circ$")
matrix_note(fig, axes[0, 2], "SR", SR)
matrix_note(fig, axes[1, 2], "RS", RS)
save(fig, "L3-n5")

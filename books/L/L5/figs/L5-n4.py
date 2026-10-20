import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import FancyArrowPatch

fig, axes = new_fig(18.5, 7.0, ncols=3)
fig.subplots_adjust(wspace=0.42, left=0.07, right=0.98, bottom=0.18, top=0.88)
for ax in axes:
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-0.5, 1.5)
    ax.set_xticks(np.arange(-1.5, 1.51, 0.5))
    ax.set_yticks(np.arange(-0.5, 1.51, 0.5))
    ax.grid(True, color=C.LIGHT, lw=0.65, alpha=0.8)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")

polys = [
    np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]),
    np.array([[0, 0], [0, 1], [-1, 1], [-1, 0], [0, 0]]),
    np.array([[0, 0], [1, 1], [0, 1], [-1, 0], [0, 0]]),
]
titles = ["开始", "做完③", "再做②"]
for ax, poly, title in zip(axes, polys, titles):
    ax.fill(poly[:, 0], poly[:, 1], facecolor=C.LIGHT, alpha=0.55, zorder=1)
    ax.plot(poly[:, 0], poly[:, 1], color=C.INK, lw=1.8, ls="-", zorder=3)
    label(ax, title, (0, 1.34), offset=(0, 0), ha="center", va="center")

# 用粗、细箭头标出 e1、e2 的像，兼顾方向辨识
arrow(axes[0], (0, 0), (1, 0), color=C.BLUE, text="$\\mathbf{e}_1$", offset=(2, -15), lw=2.4)
arrow(axes[0], (0, 0), (0, 1), color=C.RED, text="$\\mathbf{e}_2$", offset=(-18, -6), lw=1.2)
arrow(axes[1], (0, 0), (0, 1), color=C.BLUE, text="$\\mathbf{e}_1$", offset=(6, 3), lw=2.4)
arrow(axes[1], (0, 0), (-1, 0), color=C.RED, text="$\\mathbf{e}_2$", offset=(-6, 6), lw=1.2)
arrow(axes[2], (0, 0), (1, 1), color=C.BLUE, text="$\\mathbf{e}_1$", offset=(4, 5), lw=2.4)
arrow(axes[2], (0, 0), (-1, 0), color=C.RED, text="$\\mathbf{e}_2$", offset=(-6, -16), lw=1.2)

# 子图之间的双向操作箭头
fig.canvas.draw()
for i, (left, right) in enumerate(zip(axes[:-1], axes[1:])):
    lp, rp = left.get_position(), right.get_position()
    x1, x2 = lp.x1 + 0.008, rp.x0 - 0.008
    top = FancyArrowPatch((x1, 0.91), (x2, 0.91), transform=fig.transFigure,
                          arrowstyle="-|>", mutation_scale=11, color=C.INK, lw=1.2)
    bottom = FancyArrowPatch((x2, 0.10), (x1, 0.10), transform=fig.transFigure,
                             arrowstyle="-|>", mutation_scale=11, color=C.INK, lw=1.2)
    fig.add_artist(top); fig.add_artist(bottom)
    top_label = "③" if i == 0 else "②"
    bottom_label = "$③^{-1}$" if i == 0 else "$②^{-1}$"
    xm = (x1 + x2) / 2
    fig.text(xm, 0.95, top_label, ha="center", va="center", color=C.INK)
    fig.text(xm, 0.06, bottom_label, ha="center", va="center", color=C.INK)

save(fig, "L5-n4")

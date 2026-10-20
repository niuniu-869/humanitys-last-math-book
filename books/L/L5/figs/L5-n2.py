import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import FancyArrowPatch

fig, axes = new_fig(17.0, 8.0, ncols=2)
fig.subplots_adjust(wspace=0.36, left=0.08, right=0.97, bottom=0.14, top=0.92)
# new_fig already creates axes; normalize the two panels.
for ax in axes:
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-0.5, 3.5)
    ax.set_ylim(-0.5, 3.5)
    ax.set_xticks(np.arange(-0.5, 3.51, 0.5))
    ax.set_yticks(np.arange(-0.5, 3.51, 0.5))
    ax.grid(True, color=C.LIGHT, lw=0.65, alpha=0.8)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")

# 左图：单位正方形
ax = axes[0]
sq = np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]])
ax.fill(sq[:, 0], sq[:, 1], facecolor=C.LIGHT, alpha=0.55, zorder=1)
ax.plot(sq[:, 0], sq[:, 1], color=C.INK, lw=1.8, ls="-", zorder=3)
arrow(ax, (0, 0), (1, 0), color=C.BLUE, text="$\\mathbf{e}_1$", offset=(4, -15), lw=1.8)
arrow(ax, (0, 0), (0, 1), color=C.RED, text="$\\mathbf{e}_2$", offset=(5, 4), lw=1.8)
label(ax, "原来", (1.5, 3.22), offset=(0, 0), ha="center", va="center")

# 右图：像与留存的虚线原方形
ax = axes[1]
ax.plot(sq[:, 0], sq[:, 1], color=C.GRAY, lw=1.4, ls="--", zorder=2)
par = np.array([[0, 0], [2, 1], [3, 3], [1, 2], [0, 0]])
ax.fill(par[:, 0], par[:, 1], facecolor=C.LIGHT, alpha=0.55, zorder=1)
ax.plot(par[:, 0], par[:, 1], color=C.INK, lw=1.8, ls="-", zorder=3)
arrow(ax, (0, 0), (2, 1), color=C.BLUE, text="$①\\mathbf{e}_1=(2,1)$", offset=(4, 5), lw=1.8)
arrow(ax, (0, 0), (1, 2), color=C.RED, text="$①\\mathbf{e}_2=(1,2)$", offset=(5, 2), lw=1.8)
label(ax, "经过①", (1.5, 3.22), offset=(0, 0), ha="center", va="center")

# 两个方向的弯箭头，放在两图之间
fig = axes[0].figure
fig.canvas.draw()
left_pos, right_pos = axes[0].get_position(), axes[1].get_position()
xmid = (left_pos.x1 + right_pos.x0) / 2
p1 = FancyArrowPatch((left_pos.x1 + 0.008, 0.66), (right_pos.x0 - 0.008, 0.66),
                     transform=fig.transFigure, arrowstyle="-|>", mutation_scale=12,
                     connectionstyle="arc3,rad=-0.28", color=C.INK, lw=1.3)
p2 = FancyArrowPatch((right_pos.x0 - 0.008, 0.34), (left_pos.x1 + 0.008, 0.34),
                     transform=fig.transFigure, arrowstyle="-|>", mutation_scale=12,
                     connectionstyle="arc3,rad=-0.28", color=C.INK, lw=1.3)
fig.add_artist(p1); fig.add_artist(p2)
fig.text(xmid, 0.79, "①", ha="center", va="center", color=C.INK)
fig.text(xmid, 0.21, "$①^{-1}$", ha="center", va="center", color=C.INK)

save(fig, "L5-n2")

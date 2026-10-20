import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Arc, FancyArrowPatch

fig, axes = new_fig(18.0, 7.6, nrows=1, ncols=3)
fig.subplots_adjust(wspace=0.28, left=0.045, right=0.985, top=0.82, bottom=0.23)

xmin, xmax, ymin, ymax = -1.5, 2.2, -1.5, 2.2

def setup(ax, title):
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_xticks(np.arange(-1, 3, 1))
    ax.set_yticks(np.arange(-1, 3, 1))
    ax.grid(True, color=C.LIGHT, lw=0.55, alpha=0.8, zorder=0)
    ax.axhline(0, color=C.GRAY, lw=0.8, zorder=1)
    ax.axvline(0, color=C.GRAY, lw=0.8, zorder=1)
    ax.set_title(title, pad=7)
    ax.tick_params(labelsize=8, length=2)

def dashed_arrow(ax, start, vec, color=C.GRAY, lw=1.7):
    x, y = start
    dx, dy = vec
    ax.add_patch(FancyArrowPatch((x, y), (x + dx, y + dy), arrowstyle="-|>",
                                 mutation_scale=11, color=color, lw=lw,
                                 linestyle="--", shrinkA=0, shrinkB=0, zorder=4))

# 左：剪切
ax = axes[0]
setup(ax, "老朋友②：剪切")
# 特征方向 x 轴
ax.plot([xmin, xmax], [0, 0], color=C.INK, lw=1.9, ls=":", zorder=2)
label(ax, "特征方向", (1.75, 0.12), offset=(0, 0), color=C.INK, ha="center", va="bottom")
# 原 (1,0) 与像 (1,0)
arrow(ax, (0, 0), (1, 0), color=C.INK, lw=1.7)
ax.scatter([1], [0], s=37, facecolors=C.PAPER, edgecolors=C.INK, linewidths=1.2, zorder=5)
label(ax, "不转向", (1.0, -0.15), offset=(0, 0), color=C.INK, ha="center", va="top")
# 原 (0,1) -> 像 (1,1)
arrow(ax, (0, 0), (0, 1), color=C.INK, lw=1.7)
dashed_arrow(ax, (0, 0), (1, 1))
label(ax, "被斜推", (1, 1), offset=(5, 3), color=C.GRAY)
label(ax, "实线：原向量；虚线：像", (1.95, 1.95), offset=(0, 0), color=C.INK, ha="right", va="top", fontsize=8.5)

# 中：转 90°
ax = axes[1]
setup(ax, "老朋友③：转 90°")
# (1,0) -> (0,1)
arrow(ax, (0, 0), (1, 0), color=C.INK, lw=1.7)
dashed_arrow(ax, (0, 0), (0, 1))
ax.add_patch(Arc((0, 0), 0.72, 0.72, angle=0, theta1=0, theta2=90,
                 color=C.GRAY, lw=1.1, zorder=3))
# (1,1) -> (-1,1)
arrow(ax, (0, 0), (1, 1), color=C.INK, lw=1.7)
dashed_arrow(ax, (0, 0), (-1, 1))
ax.add_patch(Arc((0, 0), 1.18, 1.18, angle=0, theta1=45, theta2=135,
                 color=C.GRAY, lw=1.1, zorder=3))
label(ax, "每个方向都转了，\n没有实特征向量", (0.35, -0.8), offset=(0, 0), color=C.INK, ha="center", va="center", fontsize=8.5)

# 右：投影
ax = axes[2]
setup(ax, "老朋友④：投影")
# y=x 特征方向
ax.plot([xmin, xmax], [xmin, xmax], color=C.INK, lw=1.9, ls=":", zorder=2)
label(ax, "特征值 1", (1.45, 1.9), offset=(0, 0), color=C.INK, ha="right", va="center")
# (1,1) -> (1,1)
arrow(ax, (0, 0), (1, 1), color=C.INK, lw=1.7)
ax.scatter([1], [1], s=37, facecolors=C.PAPER, edgecolors=C.INK, linewidths=1.2, zorder=5)
label(ax, "不动", (1, 1), offset=(6, -2), color=C.INK)
# (-1,1) -> (0,0)
arrow(ax, (0, 0), (-1, 1), color=C.INK, lw=1.7)
ax.scatter([0], [0], s=42, marker="s", color=C.INK, zorder=5)
label(ax, "$(-1,1)^T$ 压成原点\n特征值 0", (0.15, -0.4), offset=(0, 0), color=C.INK, ha="left", va="top")
# (1,0) -> (0.5,0.5)
arrow(ax, (0, 0), (1, 0), color=C.INK, lw=1.7)
dashed_arrow(ax, (0, 0), (0.5, 0.5))
label(ax, "转了", (0.5, 0.5), offset=(6, -3), color=C.GRAY)

save(fig, "L11-n2")

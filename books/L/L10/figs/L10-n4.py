import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Polygon, Arc

fig, axes = new_fig(16.0, 7.6, nrows=1, ncols=2)
fig.subplots_adjust(wspace=0.22, left=0.06, right=0.98, top=0.86, bottom=0.12)

def setup(ax, title):
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-1.6, 2.5); ax.set_ylim(-0.6, 2.0)
    ax.set_xticks(range(-1, 3)); ax.set_yticks(range(0, 3))
    ax.grid(True, color=C.LIGHT, lw=0.55, zorder=0)
    ax.axhline(0, color=C.GRAY, lw=0.8, zorder=1); ax.axvline(0, color=C.GRAY, lw=0.8, zorder=1)
    ax.set_title(title, pad=6)

def square(ax):
    ax.add_patch(Polygon([(0, 0), (1, 0), (1, 1), (0, 1)], closed=True, facecolor=C.LIGHT,
                         edgecolor=C.INK, lw=1.6, alpha=0.9, zorder=2))

def image(ax, pts):
    ax.add_patch(Polygon(pts, closed=True, fill=False, edgecolor=C.INK, lw=1.8, ls="--", zorder=3))

# 左：老朋友③ 转 90°
ax = axes[0]
setup(ax, "老朋友③：转 $90^\\circ$")
square(ax)
image(ax, [(0, 0), (0, 1), (-1, 1), (-1, 0)])
label(ax, "原正方形", (0.5, 0.5), color=C.INK, ha="center", va="center", fontsize=8.5)
label(ax, "像", (-0.5, 0.5), color=C.INK, ha="center", va="center", fontsize=9)
s = 0.13
ax.plot([-s, -s, 0], [0, s, s], color=C.INK, lw=1.0, zorder=4)
label(ax, "边长仍是 1，角仍是直角", (0.45, 1.55), color=C.INK, ha="center", va="center", fontsize=8.5)

# 右：老朋友② 剪切
ax = axes[1]
setup(ax, "老朋友②：剪切")
square(ax)
image(ax, [(0, 0), (1, 0), (2, 1), (1, 1)])
ax.annotate("", xy=(1, 1), xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color=C.INK, lw=1.6, ls="--", shrinkA=0, shrinkB=0, mutation_scale=11), zorder=4)
label(ax, "长 $\\sqrt{2}$", (0.1, 0.68), offset=(0, 0), color=C.INK, ha="left", va="center", fontsize=9)
ax.add_patch(Arc((0, 0), 0.6, 0.6, angle=0, theta1=0, theta2=45, color=C.INK, lw=1.0, zorder=4))
label(ax, "$45^\\circ$", (0.32, 0.12), offset=(4, 0), color=C.INK, ha="left", va="center", fontsize=8.5)
label(ax, "像", (1.5, 0.5), offset=(6, 0), color=C.INK, ha="left", va="center", fontsize=9)
label(ax, "面积还是 1，但边长和直角都变了", (0.45, 1.55), color=C.INK, ha="center", va="center", fontsize=8.5)
label(ax, "实线：原正方形；虚线：像", (2.45, -0.45), color=C.INK, ha="right", va="center", fontsize=8)
save(fig, "L10-n4")

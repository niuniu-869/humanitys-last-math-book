import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch
from matplotlib.path import Path


def pol(cx, cy, r, deg):
    a = np.deg2rad(deg)
    return (cx + r * np.cos(a), cy + r * np.sin(a))


fig, ax = new_fig(14, 9)
ax.set_xlim(-2.5, 2.7); ax.set_ylim(-2.6, 2.5); ax.axis("off")
pos = {"活跃": (-1.0, 0.0), "沉默": (1.0, 0.0), "付费": (1.75, 1.55), "流失": (1.75, -1.55)}
R, R2 = 0.36, 0.46
ax.add_patch(Ellipse((0, -0.02), 2.9, 1.75, facecolor=C.LIGHT, edgecolor=C.GRAY, lw=1.0, zorder=0))
t = label(ax, "暂态", (0.0, -0.66), ha="center", va="center", fontsize=9.5)
t.set_path_effects([])
label(ax, "吸收态", (2.28, 0.0), ha="center", va="center")
for name, (x, y) in pos.items():
    ax.add_patch(Circle((x, y), R, facecolor=C.PAPER, edgecolor=C.INK, lw=1.5, zorder=3))
    if name in ("付费", "流失"):
        ax.add_patch(Circle((x, y), R2, facecolor="none", edgecolor=C.INK, lw=1.1, zorder=3))
    label(ax, name, (x, y), ha="center", va="center")


def curved(a, b, rad, text, text_xy, fs=9.5):
    ax.add_patch(FancyArrowPatch(a, b, connectionstyle=f"arc3,rad={rad}", arrowstyle="-|>",
                                 mutation_scale=11, lw=1.4, color=C.INK, zorder=4,
                                 shrinkA=0, shrinkB=0))
    label(ax, text, text_xy, ha="center", va="center", fontsize=fs)


# 0.6 活跃自环：在“活跃”圈左上方，独立成环
p0 = pol(-1, 0, R, 150)
p3 = pol(-1, 0, R, 100)
loop = Path([p0, (-1.62, 1.02), (-1.18, 1.02), p3],
            [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4])
ax.add_patch(FancyArrowPatch(path=loop, arrowstyle="-|>", mutation_scale=11, lw=1.4,
                             color=C.INK, zorder=4))
label(ax, "0.6", (-1.34, 1.03), ha="center", va="center", fontsize=9.5)

# 活跃→沉默 0.2（上弧）
curved(pol(-1, 0, R, 30), pol(1, 0, R, 150), -0.18, "0.2", (0.0, 0.58))
# 沉默→活跃 0.3（下弧），标签在弧下、箭头附近，不压椭圆边界
curved(pol(1, 0, R, 210), pol(-1, 0, R, -30), -0.18, "0.3", (-0.50, -0.50),
       fs=9.5)
# 沉默 0.4 自环：在“沉默”圈下方
curved(pol(1, 0, R, 230), pol(1, 0, R, 310), 1.25, "0.4", (1.0, -0.92))
# 活跃→付费 0.2：从“活跃”圈右上方出发，与 0.6 自环分开
curved(pol(-1, 0, R, 60), pol(1.75, 1.55, R2, 200), -0.18, "0.2", (0.0, 1.38))
# 沉默→流失 0.3：从“沉默”圈右侧出发，向右弯出，避开 0.4 自环
curved(pol(1, 0, R, -5), pol(1.75, -1.55, R2, 150), -0.35, "0.3", (1.75, -0.65))
# 两个吸收态的自环
curved(pol(1.75, 1.55, R2, 145), pol(1.75, 1.55, R2, 35), -0.95, "1", (2.30, 1.98))
curved(pol(1.75, -1.55, R2, 215), pol(1.75, -1.55, R2, 325), 0.95, "1", (2.30, -1.98))
label(ax, "活跃出发：0.6 + 0.2 + 0.2 = 1；沉默出发：0.3 + 0.4 + 0.3 = 1", (-0.6, -2.45), ha="center", va="center", fontsize=8.5)
save(fig, "P9-n2")

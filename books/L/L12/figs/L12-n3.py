import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, save, arrow, label
from matplotlib.patches import Polygon

S = np.array([[2.0, 1.0], [1.0, 2.0]])
p1, p2 = np.array([1.0, 1.0]), np.array([-1.0, 1.0])
O = np.array([0.0, 0.0])

fig, (ax1, ax2) = new_fig(18.5, 9.0, ncols=2, gridspec_kw={"width_ratios": [1, 1.5]})

# 左：标准尺子
ax1.set_aspect("equal", adjustable="box")
ax1.set_xlim(-0.6, 3.8); ax1.set_ylim(-0.6, 3.8)
ax1.set_xticks(range(0, 4)); ax1.set_yticks(range(0, 4))
ax1.grid(True, color=C.LIGHT, lw=0.7, zorder=0)
ax1.axhline(0, color=C.GRAY, lw=0.9, zorder=1); ax1.axvline(0, color=C.GRAY, lw=0.9, zorder=1)
ax1.set_title("标准尺子")
unit = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], float)
img = (S @ unit.T).T
ax1.add_patch(Polygon(unit, closed=True, facecolor=C.LIGHT, edgecolor=C.GRAY, lw=1.1, zorder=2))
ax1.plot(*np.vstack([img, img[0]]).T, color=C.INK, lw=2.6, zorder=3)
label(ax1, "浅灰方块：原格子", (0.5, -0.3), ha="center", va="center", fontsize=9)
label(ax1, "像", (2.15, 2.0), ha="center", va="center")
arrow(ax1, O, S[:, 0], color=C.INK, lw=1.4)
label(ax1, r"$S\boldsymbol{e}_1=(2,1)$", S[:, 0], offset=(4, -12), fontsize=9)
arrow(ax1, O, S[:, 1], color=C.INK, lw=1.4)
label(ax1, r"$S\boldsymbol{e}_2=(1,2)$", S[:, 1], offset=(-62, 6), fontsize=9)
ax1.text(0.5, -0.16, "非对角元是 1：两个坐标搅在一起", transform=ax1.transAxes, ha="center", va="top", fontsize=9.5)

# 右：特征向量当尺子
ax2.set_aspect("equal", adjustable="box")
ax2.set_xlim(-3.4, 6.4); ax2.set_ylim(-1.2, 5.0)
ax2.set_xticks(range(-3, 7)); ax2.set_yticks(range(-1, 6))
ax2.axhline(0, color=C.GRAY, lw=0.8, zorder=1); ax2.axvline(0, color=C.GRAY, lw=0.8, zorder=1)
ax2.set_title("特征向量当尺子")
s = np.array([-10.0, 10.0])
for k in range(-6, 7):
    pts = np.outer(s, p1) + k * p2
    ax2.plot(pts[:, 0], pts[:, 1], color=C.GRAY, lw=0.6, ls="--", zorder=1, alpha=0.6)
    pts = k * p1 + np.outer(s, p2)
    ax2.plot(pts[:, 0], pts[:, 1], color=C.GRAY, lw=0.6, ls="--", zorder=1, alpha=0.6)
cell = np.array([O, p1, p1 + p2, p2])
cimg = np.array([O, 3 * p1, 3 * p1 + p2, p2])
ax2.add_patch(Polygon(cell, closed=True, facecolor=C.LIGHT, edgecolor=C.GRAY, lw=1.1, zorder=2))
ax2.plot(*np.vstack([cimg, cimg[0]]).T, color=C.INK, lw=2.6, zorder=3)
label(ax2, "像", (1.55, 2.75), ha="center", va="center")
arrow(ax2, O, 3 * p1, color=C.INK, lw=2.0)
label(ax2, r"$S\boldsymbol{p}_1=3\boldsymbol{p}_1$", 3 * p1, offset=(4, 4), fontsize=9)
arrow(ax2, O, p1, color=C.GRAY, lw=1.6)
label(ax2, r"$\boldsymbol{p}_1$", p1, offset=(5, -10), color=C.INK)
arrow(ax2, O, p2, color=C.INK, lw=1.6)
label(ax2, r"$\boldsymbol{p}_2=S\boldsymbol{p}_2$", p2, offset=(-48, -16), fontsize=9)
x = np.array([2.0, 0.0]); Sx = S @ x
ax2.scatter(*x, s=40, color=C.INK, zorder=5)
label(ax2, r"$\boldsymbol{x}$，新坐标 $(1,-1)$", x, offset=(-10, -16), fontsize=9)
ax2.scatter(*Sx, s=46, marker="s", color=C.INK, zorder=5)
label(ax2, r"$S\boldsymbol{x}$", Sx, offset=(8, -2), fontsize=9)
label(ax2, r"新坐标 $(3,-1)$", Sx, offset=(8, -14), fontsize=9)
ax2.annotate("", xy=Sx, xytext=x, arrowprops=dict(arrowstyle="-|>", color=C.INK, lw=1.3, linestyle=":",
             shrinkA=5, shrinkB=6, mutation_scale=10), zorder=4)
ax2.text(0.5, -0.16, r"浅灰方块：原格子。矩阵 $\mathrm{diag}(3,1)$：各管各的", transform=ax2.transAxes,
         ha="center", va="top", fontsize=9.5)

save(fig, "L12-n3")

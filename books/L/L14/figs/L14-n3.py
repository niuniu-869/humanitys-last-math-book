import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(11.5, 8.8)

q1 = np.array([1.0, 1.0]) / np.sqrt(2.0)
q2 = np.array([1.0, -1.0]) / np.sqrt(2.0)

# 坐标轴
ax.plot([-0.6, 2.4], [0, 0], color=C.GRAY, lw=0.9, zorder=1)
ax.plot([0, 0], [-2.0, 0.6], color=C.GRAY, lw=0.9, zorder=1)
label(ax, r"$w_1$", (2.38, 0), offset=(-2, -16), color=C.INK, ha="right")
label(ax, r"$w_2$", (0, 0.55), offset=(5, -2), color=C.INK, va="top")

# 两条特征方向主轴
for q in (q1, q2):
    p0, p1 = -3.0 * q, 3.0 * q
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=C.GRAY, lw=1.0, ls="--", zorder=1)
label(ax, r"$\boldsymbol{q}_1$（陡）", (0.42, 0.42), offset=(8, -8), color=C.INK)
label(ax, r"$\boldsymbol{q}_2$（平）", (1.10 * q2[0], 1.10 * q2[1]), offset=(6, -11), color=C.INK)

# 等高线 L=c：沿 q1 半轴 sqrt(2c/10)，沿 q2 半轴 sqrt(2c)
th = np.linspace(0, 2 * np.pi, 500)
for c in (0.5, 2.0, 5.0, 11.0):
    curve = np.sqrt(2 * c / 10.0) * np.cos(th)[:, None] * q1 + np.sqrt(2 * c) * np.sin(th)[:, None] * q2
    ax.plot(curve[:, 0], curve[:, 1], color=C.GRAY, lw=1.15, ls="-", zorder=2)

# 等高线文字，放在右下/左上空白处
label(ax, r"$L=0.5$", (0.18, -0.54), offset=(4, -2), color=C.INK)
label(ax, r"$L=2$", (0.48, -1.01), offset=(4, -2), color=C.INK)
label(ax, r"$L=5$", (0.77, -1.58), offset=(4, -2), color=C.INK)
label(ax, r"$L=11$", (1.78, -1.44), offset=(4, -2), color=C.INK)

# 梯度下降轨迹与迭代点
ws = np.array([
    (2.0, 0.0),
    (0.02, -1.62),
    (1.3124, -0.0324),
    (0.0394, -1.0634),
    (0.8617, -0.0425),
    (0.0431, -0.6984),
    (0.5662, -0.0419),
    (0.0396, -0.4590),
    (0.3722, -0.0366),
])
ax.plot(ws[:, 0], ws[:, 1], color=C.BLUE, lw=2.2, ls="-", zorder=4)
ax.scatter(ws[:, 0], ws[:, 1], s=25, color=C.BLUE, zorder=5)
label(ax, r"$\boldsymbol{w}_0$", ws[0], offset=(-4, 9), color=C.INK)
label(ax, r"$\boldsymbol{w}_1$", ws[1], offset=(7, -13), color=C.INK)
label(ax, r"$\boldsymbol{w}_2$", ws[2], offset=(7, 7), color=C.INK)

# 原点最小值点：空心圆
ax.scatter([0], [0], s=60, facecolors=C.PAPER, edgecolors=C.INK, linewidths=1.4, zorder=6)
label(ax, "最小值点", (0, 0), offset=(7, 7), color=C.INK)

ax.set_aspect("equal")
ax.set_xlim(-0.6, 2.4)
ax.set_ylim(-2.0, 0.6)
ax.set_xticks([0, 1, 2])
ax.set_yticks([-2, -1, 0])
ax.set_xlabel("")
ax.set_ylabel("")
save(fig, "L14-n3")

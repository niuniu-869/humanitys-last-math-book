import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, save, arrow, dot, label
from matplotlib.patches import FancyArrowPatch

# a2 = 2 a1：两种走法停在同一点 3a1，直线外的 b 拼不出
a1 = np.array([2.0, 1.0])
a2 = 2 * a1
end = 3 * a1
b = np.array([2.0, 4.0])

fig, ax = new_fig(12.5, 8.6)
ax.set_aspect("equal", adjustable="box")
ax.axhline(0, color=C.LIGHT, lw=0.9, zorder=0)
ax.axvline(0, color=C.LIGHT, lw=0.9, zorder=0)

# 张成：过原点的直线
xs = np.array([-2.0, 8.0])
ax.plot(xs, xs / 2, color=C.GRAY, lw=1.0, zorder=1)
label(ax, r"$\mathrm{span}(\boldsymbol{a}_1,\boldsymbol{a}_2)$：仍是这条直线", (8.0, 4.0), offset=(-4, 8), color=C.INK, ha="right")

# a1 实线箭头；a2 虚线箭头（向直线下方平移一点，免得和 a1 重叠）
arrow(ax, (0, 0), a1, color=C.INK, lw=2.4)
label(ax, r"$\boldsymbol{a}_1$", a1, offset=(-16, 4), color=C.INK)
n = np.array([1.0, -2.0]) / np.sqrt(5) * 0.32
ax.annotate("", xy=n + a2, xytext=n, arrowprops=dict(arrowstyle="-|>", color=C.RED, lw=1.8, ls="--",
            shrinkA=0, shrinkB=0, mutation_scale=11), zorder=4)
ax.annotate(r"$\boldsymbol{a}_2=2\boldsymbol{a}_1$（虚线箭头）", xy=n + 0.8 * a2, xytext=(4.5, 0.45), color=C.RED,
            arrowprops=dict(arrowstyle="-", color=C.GRAY, lw=0.8), zorder=6)

def hop(p, q, rad, ls):
    ax.add_patch(FancyArrowPatch(p, q, connectionstyle=f"arc3,rad={rad}", arrowstyle="-|>",
                                 mutation_scale=10, lw=1.3, ls=ls, color=C.INK, shrinkA=2, shrinkB=2, zorder=3))

# 走法一（直线上方，实线弧）：沿 a1 走三次
for k in range(3):
    hop(k * a1, (k + 1) * a1, -0.55, "-")
label(ax, r"走法一（实线弧）：$3\boldsymbol{a}_1+0\cdot\boldsymbol{a}_2$", (-1.9, 2.9), offset=(0, 0), color=C.INK, ha="left")

# 走法二（直线下方，虚线弧）：先 a1，再 a2
hop((0, 0), a1, 0.55, ":")
hop(a1, end, 0.45, ":")
label(ax, r"走法二（点线弧）：$\boldsymbol{a}_1+\boldsymbol{a}_2$", (4.2, -0.2), offset=(0, -22), color=C.INK, ha="left")

# 终点与直线外的点
dot(ax, end, size=40)
label(ax, r"同一点 $3\boldsymbol{a}_1$", end, offset=(8, -4), color=C.INK)
ax.scatter(*b, s=50, facecolors=C.PAPER, edgecolors=C.INK, linewidths=1.6, zorder=5)
label(ax, r"$\boldsymbol{b}$：不在直线上，拼不出", b, offset=(8, -3), color=C.INK)
dot(ax, (0, 0), size=18)
label(ax, r"$O$", (0, 0), offset=(-12, 2), color=C.INK)

ax.set_xlim(-2, 8.5)
ax.set_ylim(-1.8, 5)
ax.set_xticks(range(-2, 9, 2))
ax.set_yticks(range(-1, 6, 1))
save(fig, "L1-n2")

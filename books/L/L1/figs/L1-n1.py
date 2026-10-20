import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

# 原料点与两步混合的精确坐标
p1 = np.array([40.0, 10.0])
p2 = np.array([10.0, 40.0])
p3 = np.array([10.0, 10.0])
d = 0.5 * p2 + 0.5 * p3
inside = np.array([20.0, 20.0])
outside = np.array([30.0, 30.0])

fig, ax = new_fig(12.5, 9.0)
ax.set_aspect("equal", adjustable="box")

# 三种原料的凸包
tri = np.vstack([p1, p2, p3, p1])
ax.fill(tri[:, 0], tri[:, 1], color=C.LIGHT, alpha=0.55, zorder=1)
ax.plot(tri[:, 0], tri[:, 1], color=C.GRAY, lw=1.1, zorder=2)

# 两种原料的线段及其延长线
ax.plot([50, 40], [0, 10], color=C.GRAY, lw=1.1, ls="--", zorder=2)
ax.plot([10, 0], [40, 50], color=C.GRAY, lw=1.1, ls="--", zorder=2)
ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=C.BLUE, lw=2.8, zorder=3)

# 两步混合：先得到边 p2p3 的中点 d，再与 p1 混合
ax.plot([p1[0], d[0]], [p1[1], d[1]], color=C.AMBER, lw=1.9, ls="--", zorder=3)

# 目标点与原料点
dot(ax, p1, color=C.BLUE, size=34)
dot(ax, p2, color=C.BLUE, size=34)
dot(ax, p3, color=C.BLUE, size=34)
dot(ax, d, color=C.AMBER, size=32)
dot(ax, inside, color=C.TEAL, size=34)
dot(ax, (30, 20), color=C.TEAL, size=30)
ax.scatter(*outside, s=48, facecolors=C.PAPER, edgecolors=C.RED, linewidths=2.0, zorder=5)

# 线段参数标注
label(ax, r"$t=0$", p1, offset=(-14, -24), color=C.BLUE)
label(ax, r"$t=\frac{1}{3}$", (30, 20), offset=(9, 4), color=C.TEAL)
label(ax, r"$t=1$", p2, offset=(-34, -14), color=C.BLUE)

# 点标注
label(ax, r"$\boldsymbol{p}_1$", p1, offset=(7, 8), color=C.BLUE)
label(ax, r"$\boldsymbol{p}_2$", p2, offset=(-28, 15), color=C.BLUE)
label(ax, r"$\boldsymbol{p}_3$", p3, offset=(-28, -13), color=C.BLUE)
label(ax, r"$\boldsymbol{d}$", d, offset=(8, 4), color=C.AMBER)
label(ax, r"$(20,20)$：权重各 $\frac{1}{3}$", inside, offset=(-12, -27), color=C.TEAL, ha="center")
label(ax, r"$(30,30)$：$c_3=-\frac{1}{3}$", outside, offset=(8, 4), color=C.RED)
label(ax, "$t<0$ 或 $t>1$：要用负数的原料", (25, 48), offset=(0, -16), color=C.GRAY, ha="center")

ax.set_xlim(0, 52)
ax.set_ylim(0, 52)
ax.set_xticks([0, 10, 20, 30, 40, 50])
ax.set_yticks([0, 10, 20, 30, 40, 50])
ax.set_xlabel("蛋白质 %")
ax.set_ylabel("脂肪 %")

save(fig, "L1-n1")

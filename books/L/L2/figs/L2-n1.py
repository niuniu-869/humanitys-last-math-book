import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

# 几何数据：主直线 x+2y=5，法向量 a=(1,2)^T
O = np.array([0.0, 0.0])
a = np.array([1.0, 2.0])
x0 = np.array([1.0, 2.0])
y = np.array([4.0, 3.0])
f = np.array([3.0, 1.0])
line_dir = np.array([2.0, -1.0]) / np.sqrt(5.0)
normal_dir = a / np.sqrt(5.0)

fig, ax = new_fig(13.5, 9.0)
ax.set_aspect("equal", adjustable="box")

# 淡网格与坐标轴
ax.set_xlim(-1.0, 6.0)
ax.set_ylim(-1.0, 5.5)
ax.set_xticks(np.arange(-1, 7, 1))
ax.set_yticks(np.arange(-1, 6, 1))
ax.grid(True, color=C.LIGHT, lw=0.7, alpha=0.65, zorder=0)
ax.axhline(0, color=C.GRAY, lw=0.9, zorder=1)
ax.axvline(0, color=C.GRAY, lw=0.9, zorder=1)
ax.set_xlabel("$x$")
ax.set_ylabel("$y$")

# 三条平行线：y=(c-x)/2
xs = np.array([-1.0, 6.0])
for c in (0.0, 10.0):
    ax.plot(xs, (c - xs) / 2.0, color=C.GRAY, lw=1.5, ls=(0, (5, 4)), zorder=2)
ax.plot(xs, (5.0 - xs) / 2.0, color=C.BLUE, lw=3.0, zorder=3)

# 直线标签和 c 变化标签
label(ax, "$x+2y=5$", (5.45, (5.0 - 5.45) / 2.0), offset=(4, 5), color=C.BLUE)
label(ax, "$c=0$", (1.45, (0.0 - 1.45) / 2.0), offset=(4, -10), color=C.GRAY)
label(ax, "$c=10$", (5.35, (10.0 - 5.35) / 2.0), offset=(-2, 9), color=C.GRAY)

# 法向量 a：从 O 到直线上的 x0
arrow(ax, O, a, color=C.TEAL, lw=2.3, offset=(8, 5))
label(ax, r"$\boldsymbol{a}$", (0.40, 0.80), offset=(-8, 8), color=C.TEAL)
dot(ax, O, "$O$", color=C.INK, offset=(-14, -14), size=22)
dot(ax, x0, r"$\boldsymbol{x}_0=(1,2)$", color=C.INK, offset=(8, 7), size=30)

# 点 y 到垂足 f 的 -a 方向退步；f 使用珊瑚色空心点
arrow(ax, y, f - y, color=C.RED, lw=2.3, offset=(-5, 10))
label(ax, r"退一步 $-\boldsymbol{a}$，距离 $\sqrt{5}$", (3.7, 1.55), offset=(2, 0), color=C.RED, ha="left")
dot(ax, y, r"$\boldsymbol{y}=(4,3)$", color=C.RED, offset=(8, 7), size=32)
ax.scatter([f[0]], [f[1]], s=46, facecolors=C.PAPER, edgecolors=C.RED, linewidths=2.0, zorder=5)
label(ax, r"$\boldsymbol{f}=(3,1)$", f, offset=(14, -1), color=C.RED)

# 沿直线的位移 f-x0=(2,-1)
arrow(ax, x0, f - x0, color=C.AMBER, lw=2.0, offset=(2, -18))
label(ax, r"$\boldsymbol{f}-\boldsymbol{x}_0=(2,-1)$", (2.05, 1.48), offset=(0, -28), color=C.AMBER, ha="center")

# 在 x0 与 f 处画直角标记：两条互相垂直的小边，分别沿直线方向和法向方向
for p in (x0, f):
    s = 0.24
    q1 = p + s * line_dir
    q2 = p + s * normal_dir
    q12 = q1 + s * normal_dir
    ax.plot([q1[0], q12[0], q2[0]], [q1[1], q12[1], q2[1]], color=C.INK, lw=1.2, zorder=4)

# 关键点的精确关系由坐标直接体现
ax.set_xticklabels([str(v) for v in range(-1, 7)])
ax.set_yticklabels([str(v) for v in range(-1, 6)])

save(fig, "L2-n1")

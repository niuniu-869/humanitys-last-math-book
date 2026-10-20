import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import C, arrow, dot, label, new_fig, new_fig3d, np, plt, save

# 两个不共线的向量，以及它们铺出来的斜方格纸
a1 = np.array([1.0, 2.0])
a2 = np.array([3.0, 1.0])
XL, XR, YB, YT = -3.0, 10.0, -3.0, 9.0     # 画出来的窗口
C1L, C1R = -4, 6                            # 第一族格线：系数 c1 的取值
C2L, C2R = -3, 5                            # 第二族格线：系数 c2 的取值
REACH = 9.0                                 # 每条格线沿另一个方向画出的长度

fig, ax = new_fig(12.0, 11.5)
ax.set_aspect("equal")

# 族 1：固定 c1，直线 c1*a1 + t*a2
for k in range(C1L, C1R + 1):
    p, q = k * a1 - REACH * a2, k * a1 + REACH * a2
    ax.plot([p[0], q[0]], [p[1], q[1]], color=C.LIGHT, lw=0.6, zorder=1)
# 族 2：固定 c2，直线 s*a1 + c2*a2
for k in range(C2L, C2R + 1):
    p, q = k * a2 - REACH * a1, k * a2 + REACH * a1
    ax.plot([p[0], q[0]], [p[1], q[1]], color=C.LIGHT, lw=0.6, zorder=1)

# 格点：两个系数都取整数的组合 c1*a1 + c2*a2
lat = np.array([i * a1 + j * a2
                for i in range(C1L - 1, C1R + 2)
                for j in range(C2L - 1, C2R + 2)])
keep = ((lat[:, 0] > XL) & (lat[:, 0] < XR) & (lat[:, 1] > YB) & (lat[:, 1] < YT))
ax.scatter(lat[keep, 0], lat[keep, 1], s=5, color=C.GRAY, alpha=0.6, zorder=2)

# 坐标轴
ax.axhline(0, color=C.GRAY, lw=0.7, zorder=1)
ax.axvline(0, color=C.GRAY, lw=0.7, zorder=1)

# 两个向量
arrow(ax, (0, 0), a1, color=C.BLUE, text=r"$\boldsymbol{a}_1$", offset=(6, -11))
arrow(ax, (0, 0), a2, color=C.RED, text=r"$\boldsymbol{a}_2$", offset=(7, -3))

# b = 2a1 + a2：沿 a1 走两步，再沿 a2 走一步
arrow(ax, (0, 0), 2 * a1, color=C.TEAL, lw=2.0)
arrow(ax, 2 * a1, a2, color=C.TEAL, lw=2.0)
dot(ax, 2 * a1, color=C.TEAL, offset=(-34, -9), text=r"$2\boldsymbol{a}_1$")
label(ax, r"$\boldsymbol{a}_2$", 2 * a1 + 0.45 * a2, offset=(7, -12), color=C.TEAL)
dot(ax, (5, 5), color=C.TEAL, text=r"$\boldsymbol{b}$", offset=(-8, 7))
dot(ax, (0, 0), color=C.INK, text=r"$O$", offset=(-14, -12))

ax.set_xlim(XL, XR)
ax.set_ylim(YB, YT)
ax.set_xticks([0, 5, 10])
ax.set_yticks([0, 5])
save(fig, "LA1-1")

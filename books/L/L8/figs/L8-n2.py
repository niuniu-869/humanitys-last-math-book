import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

# 为了看清「垂直」，取 A = [[1,0,0],[0,1,0]]：行空间是水平面 z=0，零空间是竖直的 z 轴。
# x = (2,1,1.5) 分成 x_r = (2,1,0)（在平面上）与 x_n = (0,0,1.5)（在 z 轴方向）。
fig, ax = new_fig3d(13.0, 10.0, elev=22, azim=-60)
ax.set_axis_off()

# 行空间：水平面，浅灰阴影
g = np.array([-1.5, 3.0])
X, Y = np.meshgrid(g, np.array([-1.5, 2.5]))
ax.plot_surface(X, Y, np.zeros_like(X), color=C.LIGHT, alpha=0.5, edgecolor=C.GRAY, linewidth=0.8, shade=False)

# 零空间：竖直虚线（z 轴）
z = np.linspace(-1.6, 2.6, 2)
ax.plot([0, 0], [0, 0], z, color=C.INK, lw=1.6, ls=(0, (6, 4)))

xr = np.array([2.0, 1.0, 0.0]); xn = np.array([0.0, 0.0, 1.5]); x = xr + xn
ax.quiver(0, 0, 0, *x, color=C.INK, linewidth=2.6, arrow_length_ratio=0.08)
ax.quiver(0, 0, 0, *xr, color=C.INK, linewidth=2.0, arrow_length_ratio=0.10)
ax.quiver(*xr, *xn, color=C.INK, linewidth=2.0, linestyle=":", arrow_length_ratio=0.12)
# 平行四边形的另外两条边（细点线），说明 x = x_r + x_n
ax.plot([xn[0], x[0]], [xn[1], x[1]], [xn[2], x[2]], color=C.GRAY, lw=1.0, ls=":")

# 原点处直角记号：z 轴与平面内方向 (1,0,0)
s = 0.25
ax.plot([s, s, 0], [0, 0, 0], [0, s, s], color=C.INK, lw=1.0)
ax.scatter([0], [0], [0], s=16, color=C.INK, depthshade=False)

ax.text(2.25, 1.05, -0.35, r"$\boldsymbol{x}_r$", color=C.INK, fontsize=10)
ax.text(2.15, 1.05, 0.7, r"$\boldsymbol{x}_n$", color=C.INK, fontsize=10)
ax.text(2.1, 1.05, 1.7, r"$\boldsymbol{x}$", color=C.INK, fontsize=10)
ax.text(0.2, -1.45, 0.02, r"行空间 $C(A^{\mathsf{T}})$（阴影）", color=C.INK, fontsize=9)
ax.text(0.12, 0.0, 2.45, r"零空间 $N(A)$（虚线）", color=C.INK, fontsize=9)
ax.text2D(0.03, 0.04, r"$A\boldsymbol{x}_n=\boldsymbol{0}$，所以 $A\boldsymbol{x}=A\boldsymbol{x}_r$",
          transform=ax.transAxes, color=C.INK, fontsize=9)

ax.set_xlim(-1.5, 3.0); ax.set_ylim(-1.5, 2.5); ax.set_zlim(-1.6, 2.6)
ax.set_box_aspect((4.5, 4.0, 4.2))
save(fig, "L8-n2")

import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import C, arrow, dot, label, new_fig, new_fig3d, np, plt, save

fig, ax = new_fig3d(13.0, 11.0, elev=22, azim=-56)
ax.set_box_aspect((4, 4, 4.4), zoom=0.84)
fig.subplots_adjust(left=0.02, right=0.98, top=0.99, bottom=0.10)

XL, XR = -1.0, 3.2          # 平面在 x1, x2 方向铺开的范围
YL, YR = -1.0, 3.2

# 平面 z = x1 + x2：a1, a2 的全部线性组合
g = np.linspace(XL, XR, 9)
X, Y = np.meshgrid(g, g)
Z = X + Y
ax.plot_surface(X, Y, Z, cmap=C.CMAP, alpha=0.35, rstride=1, cstride=1,
                edgecolor="none", antialiased=True)

# 平面上的两族格线：固定 c1 或固定 c2，与图 LA1-1 的斜方格纸对应
tt = np.array([XL, XR])
ss = np.array([YL, YR])
for k in range(0, 4):
    ax.plot([k, k], tt, [k + tt[0], k + tt[1]], color=C.GRAY, lw=0.8, alpha=0.45)
    ax.plot(ss, [k, k], [ss[0] + k, ss[1] + k], color=C.GRAY, lw=0.8, alpha=0.45)

# 张成这张平面的两个向量
a1 = np.array([1.0, 0.0, 1.0])
a2 = np.array([0.0, 1.0, 1.0])
ax.quiver(0, 0, 0, *a1, color=C.BLUE, linewidth=2.4, arrow_length_ratio=0.15)
ax.quiver(0, 0, 0, *a2, color=C.RED, linewidth=2.4, arrow_length_ratio=0.15)

bp = np.array([2.0, 3.0, 5.0])      # 在平面上，是 c1=2 与 c2=3 两条格线的交点
bb = np.array([2.0, 3.0, 4.0])      # 在平面下方
ax.plot([2, 2], [3, 3], [3.30, 5.80], color=C.GRAY, ls=(0, (4, 3)), lw=1.3)
ax.scatter(*bp, s=54, color=C.TEAL, depthshade=False)
ax.scatter(*bb, s=54, facecolors="none", edgecolors=C.AMBER, linewidths=1.8,
           depthshade=False)

ax.text(1.12, -0.08, 1.06, r"$\boldsymbol{a}_1$", color=C.BLUE)
ax.text(-0.08, 1.20, 1.10, r"$\boldsymbol{a}_2$", color=C.RED)
ax.text(2.16, 3.34, 5.98, r"$\boldsymbol{b}'$", color=C.TEAL)
ax.text(1.30, 2.62, 3.24, r"$\boldsymbol{b}$", color=C.AMBER)

ax.set_xlabel("$x$", labelpad=8)
ax.set_ylabel("$y$", labelpad=8)
ax.set_zlabel("$z$", labelpad=8)
ax.set_xticks([0, 2])
ax.set_yticks([0, 2])
ax.set_zticks([0, 3, 6])
ax.set_xlim(XL, XR + 0.2)
ax.set_ylim(YL, YR + 0.2)
ax.set_zlim(-2.0, 6.6)
save(fig, "LA1-2")

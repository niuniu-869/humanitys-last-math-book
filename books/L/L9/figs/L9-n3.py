import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig3d, save, HALO

# 老朋友⑤：零空间（虚线，过原点）与 A x=(1,3,4)^T 的解集（实线，过 eta*）平行。
fig, ax = new_fig3d(15.0, 11.0, elev=24, azim=-64)
ax.set_xlim(-3.0, 1.0)
ax.set_ylim(-0.5, 1.6)
ax.set_zlim(0.0, 1.4)
ax.set_xticks([-3, -2, -1, 0, 1]); ax.set_yticks([0, 1]); ax.set_zticks([0, 1])
ax.tick_params(labelsize=7, pad=1)
ax.set_xlabel(r"$x_1$", labelpad=2)
ax.set_ylabel(r"$x_2$", labelpad=2)
ax.set_zlabel(r"$x_3$", labelpad=0)
ax.set_box_aspect((4.0, 2.1, 1.4))

xi = np.array([-2.0, 1.0, 0.0])
eta = np.array([0.0, 0.0, 1.0])
other = eta + xi

t = np.linspace(-0.35, 1.4, 120)
zero = np.outer(t, xi)
sol = eta + zero
ax.plot(zero[:, 0], zero[:, 1], zero[:, 2], color=C.INK, lw=1.6, ls=(0, (6, 4)))
ax.plot(sol[:, 0], sol[:, 1], sol[:, 2], color=C.INK, lw=2.6, ls="-")

# 竖直细点线：两条线上下相距 eta*。
ax.plot([0, 0], [0, 0], [0, 1], color=C.GRAY, lw=1.0, ls=":")
ax.plot([-2, -2], [1, 1], [0, 1], color=C.GRAY, lw=1.0, ls=":")

# 点：原点空心方块；(-2,1,0) 空心圆；两个解实心圆。
ax.scatter([0], [0], [0], marker="s", facecolors="white", edgecolors=C.INK, s=30, linewidths=1.0, depthshade=False)
ax.scatter([-2], [1], [0], marker="o", facecolors="white", edgecolors=C.INK, s=26, linewidths=1.0, depthshade=False)
ax.scatter([eta[0], other[0]], [eta[1], other[1]], [eta[2], other[2]], color=C.INK, s=34, depthshade=False)

def txt(x, y, z, s, **kw):
    ax.text(x, y, z, s, color=C.INK, fontsize=8.5, zorder=10, path_effects=HALO, **kw)

txt(0.10, 0.0, 1.16, r"$\boldsymbol{\eta}^*=(0,0,1)$", ha="left")
txt(-1.88, 1.0, 1.22, r"$(-2,1,1)$，也是解", ha="left")
txt(-1.25, 0.62, 0.55, r"走一步 $\boldsymbol{\xi}=(-2,1,0)$", ha="center")
txt(0.12, 0.0, -0.10, r"$O$")
txt(-2.12, 1.0, -0.12, r"$(-2,1,0)$", ha="right")
txt(-2.9, 1.45, 1.05, "实线：全部解\n$\\boldsymbol{\\eta}^*+t\\boldsymbol{\\xi}$", ha="right", va="center")
txt(-2.9, 1.45, 0.0, "虚线：零空间\n$N(A)=\\{t\\boldsymbol{\\xi}\\}$", ha="right", va="center")

txt(1.0, 1.6, 1.25, r"$x_3$", ha="center")
save(fig, "L9-n3")

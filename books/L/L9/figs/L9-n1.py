import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label


# 精确数据：非齐次解集、零空间与两解的和/差
eta = np.array([4.0, 0.0])
other = np.array([0.0, 2.0])
diff = other - eta                 # (-4, 2) ∈ N(A)
total = eta + other                # (4, 2)，落在 x1+2x2=8

fig, ax = new_fig(14.0, 9.0)
ax.set_aspect("equal", adjustable="box")
ax.set_xlim(-5.0, 9.0)
ax.set_ylim(-3.0, 5.0)
ax.set_xticks(np.arange(-5, 10, 1))
ax.set_yticks(np.arange(-3, 6, 1))
ax.grid(True, color=C.LIGHT, lw=0.7, alpha=0.65, zorder=0)
ax.axhline(0.0, color=C.GRAY, lw=0.9, zorder=1)
ax.axvline(0.0, color=C.GRAY, lw=0.9, zorder=1)
ax.set_xlabel(r"$x_1$")
ax.set_ylabel(r"$x_2$")

# 三条平行线：x1 + 2 x2 = c
x = np.array([-5.0, 9.0])
ax.plot(x, -x / 2.0, color=C.GRAY, lw=2.0, ls="--", zorder=2)
ax.plot(x, (4.0 - x) / 2.0, color=C.BLUE, lw=3.0, ls="-", zorder=3)
ax.plot(x, (8.0 - x) / 2.0, color=C.AMBER, lw=1.5, ls=":", zorder=2)

# 线标签放在线段附近，避开点和向量
label(ax, r"$N(A)$：$x_1+2x_2=0$", (0.2, -2.8), offset=(0, 0), color=C.GRAY)
label(ax, r"解集：$x_1+2x_2=4$", (6.25, -1.12), offset=(2, 7), color=C.BLUE)
label(ax, r"$x_1+2x_2=8$", (6.4, 0.80), offset=(2, 7), color=C.AMBER)

# 原点、两个解和它们的和。和点用空心圆，避免只靠灰度区分。
dot(ax, (0.0, 0.0), r"$O$", color=C.INK, offset=(-14, -14), size=20)
dot(ax, eta, r"$\boldsymbol{\eta}^*=(4,0)$", color=C.INK, offset=(8, 8), size=32)
dot(ax, other, r"$(0,2)$", color=C.INK, offset=(8, 8), size=32)
ax.scatter([total[0]], [total[1]], s=58, facecolors=C.PAPER, edgecolors=C.INK,
           linewidths=1.8, zorder=5)
label(ax, r"$(4,0)+(0,2)$：不是解", total, offset=(9, 6), color=C.INK)

# 两解之差：从原点出发，沿零空间方向的实线箭头；端点用方块标出。
arrow(ax, (0.0, 0.0), diff, color=C.RED, lw=2.0, offset=(-50, -4))
ax.scatter([diff[0]], [diff[1]], s=42, marker="s", facecolors=C.PAPER,
           edgecolors=C.RED, linewidths=1.5, zorder=5)
label(ax, "两解之差\n" + r"$(0,2)-(4,0)$" + "\n" + r"$=(-4,2)$", (-4.9, 1.45), offset=(0, 0), color=C.RED, ha="left", va="top")

# 从特解沿同一零空间方向到另一个解：点线箭头。
ax.annotate("", xy=other, xytext=eta,
            arrowprops=dict(arrowstyle="-|>", color=C.TEAL, lw=1.8,
                            linestyle=":", shrinkA=0, shrinkB=0, mutation_scale=11),
            zorder=4)
label(ax, "沿零空间方向走", (3.0, 1.45), offset=(0, 0), color=C.TEAL, ha="center", va="center")

save(fig, "L9-n1")

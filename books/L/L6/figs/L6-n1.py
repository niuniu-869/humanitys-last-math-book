import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label


fig, ax = new_fig(13.5, 10.0)
ax.set_aspect("equal", adjustable="box")
ax.set_xlim(-0.55, 4.75)
ax.set_ylim(-0.72, 3.85)
ax.set_xticks(np.arange(0, 5, 1))
ax.set_yticks(np.arange(0, 4, 1))
ax.grid(True, color=C.LIGHT, lw=0.65, alpha=0.65, zorder=0)
ax.axhline(0, color=C.GRAY, lw=0.9, zorder=1)
ax.axvline(0, color=C.GRAY, lw=0.9, zorder=1)
ax.set_xlabel("$x$")
ax.set_ylabel("$y$")

O = np.array([0.0, 0.0])
P = np.array([3.0, 1.0])
R = np.array([4.0, 3.0])
Q = np.array([1.0, 2.0])

# 六块角料：先铺灰色，再用白色平行四边形盖住内部。
pieces = [
    (np.array([O, [3, 0], P]), r"$\frac{1}{2}ac$"),
    (np.array([[3, 0], [4, 0], [4, 1], P]), r"$bc$"),
    (np.array([P, [4, 1], R]), r"$\frac{1}{2}bd$"),
    (np.array([O, Q, [0, 2]]), r"$\frac{1}{2}bd$"),
    (np.array([[0, 2], Q, [1, 3], [0, 3]]), r"$bc$"),
    (np.array([Q, [1, 3], R]), r"$\frac{1}{2}ac$"),
]
for poly, txt in pieces:
    ax.fill(poly[:, 0], poly[:, 1], color=C.LIGHT, alpha=0.78, zorder=2)
    ax.plot(poly[:, 0], poly[:, 1], color=C.GRAY, lw=0.9, zorder=3)
    center = poly.mean(axis=0)
    label(ax, txt, tuple(center), offset=(0, 0), color=C.INK, ha="center", va="center")

# 外框与平行四边形。
rect = np.array([[0, 0], [4, 0], [4, 3], [0, 3], [0, 0]])
ax.plot(rect[:, 0], rect[:, 1], color=C.INK, lw=1.15, zorder=4)
para = np.array([O, P, R, Q, O])
ax.fill(para[:, 0], para[:, 1], color=C.PAPER, zorder=5)
ax.plot(para[:, 0], para[:, 1], color=C.INK, lw=2.4, zorder=6)

# 向量与关键点。
arrow(ax, O, P - O, color=C.BLUE, lw=2.0, offset=(7, 6))
label(ax, r"$(a,c)^{T}$", (1.75, 0.95), offset=(0, 0), color=C.BLUE, ha="center")
arrow(ax, O, Q - O, color=C.RED, lw=2.0, offset=(-36, 4))
label(ax, r"$(b,d)^{T}$", (0.95, 1.3), offset=(0, 0), color=C.RED, ha="left")
dot(ax, O, "$O$", color=C.INK, offset=(-14, -15), size=22)

# 外框底边的分段尺寸。
ax.annotate("", xy=(3, -0.28), xytext=(0, -0.28),
            arrowprops=dict(arrowstyle="<->", color=C.GRAY, lw=1.0, shrinkA=0, shrinkB=0))
ax.annotate("", xy=(4, -0.28), xytext=(3, -0.28),
            arrowprops=dict(arrowstyle="<->", color=C.GRAY, lw=1.0, shrinkA=0, shrinkB=0))
label(ax, "$a$", (1.5, -0.28), offset=(0, -1), color=C.INK, ha="center", va="top")
label(ax, "$b$", (3.5, -0.28), offset=(0, -1), color=C.INK, ha="center", va="top")

# 外框左边的分段尺寸。
ax.annotate("", xy=(-0.28, 2), xytext=(-0.28, 0),
            arrowprops=dict(arrowstyle="<->", color=C.GRAY, lw=1.0, shrinkA=0, shrinkB=0))
ax.annotate("", xy=(-0.28, 3), xytext=(-0.28, 2),
            arrowprops=dict(arrowstyle="<->", color=C.GRAY, lw=1.0, shrinkA=0, shrinkB=0))
label(ax, "$d$", (-0.28, 1.0), offset=(-2, 0), color=C.INK, ha="right", va="center")
label(ax, "$c$", (-0.28, 2.5), offset=(-2, 0), color=C.INK, ha="right", va="center")

save(fig, "L6-n1")

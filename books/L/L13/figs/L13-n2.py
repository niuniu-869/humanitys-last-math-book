import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

origin = np.zeros(2)
x = np.array([2.0, 0.0])
v1 = np.array([1.0, 1.0])
v2 = np.array([1.0, -1.0])
w1 = 3.0 * v1
w2 = v2.copy()
Ax = w1 + w2

fig, ax = new_fig(12.5, 9.5)
ax.set_aspect("equal", adjustable="box")
ax.set_xlim(-0.5, 4.8)
ax.set_ylim(-1.8, 3.5)
ax.set_xticks(np.arange(0, 5, 1))
ax.set_yticks(np.arange(-1, 4, 1))
ax.grid(True, color=C.LIGHT, lw=0.65, alpha=0.8, zorder=0)
ax.axhline(0, color=C.GRAY, lw=0.9, zorder=1)
ax.axvline(0, color=C.GRAY, lw=0.9, zorder=1)
label(ax, "$x$", (4.74, 0), offset=(-2, 5), color=C.INK, ha="right")
label(ax, "$y$", (0, 3.43), offset=(5, -2), color=C.INK, va="top")

# 两个特征方向
for q, text, pos, off in [
    (v1, r"$\boldsymbol{q}_1$ 方向", (2.4, 2.4), (-72, 12)),
    (v2, r"$\boldsymbol{q}_2$ 方向", (1.25, -1.35), (4, -12)),
]:
    p = 4.7 * q / np.linalg.norm(q)
    ax.plot([-p[0], p[0]], [-p[1], p[1]], color=C.GRAY, lw=1.0, ls="--", zorder=1)
    label(ax, text, pos, offset=off, color=C.GRAY)

# x 的正交分量矩形
rect_before = np.array([origin, v1, x, v2])
ax.plot(*np.vstack([rect_before, rect_before[0]]).T, color=C.GRAY, lw=1.15, ls=":", zorder=2)
arrow(ax, origin, v1, color=C.GRAY, lw=1.45)
label(ax, "$(1,1)$", v1, offset=(6, 5), color=C.GRAY)
arrow(ax, origin, v2, color=C.GRAY, lw=1.45)
label(ax, "$(1,-1)$", v2, offset=(6, -14), color=C.GRAY)
arrow(ax, origin, x, color=C.INK, lw=1.8)
label(ax, r"$\boldsymbol{x}=(2,0)$", x, offset=(6, 6), color=C.INK)

# 分量矩形在 v1 处的直角标记
s = 0.18
corner = v1 + s * (-v1 / np.linalg.norm(v1))
corner2 = v1 + s * (-v1 / np.linalg.norm(v1)) + s * (v2 / np.linalg.norm(v2))
corner3 = v1 + s * (v2 / np.linalg.norm(v2))
ax.plot([corner[0], corner2[0], corner3[0]], [corner[1], corner2[1], corner3[1]],
        color=C.GRAY, lw=1.0, zorder=3)

# 伸缩后的分量与平行四边形
para_after = np.array([origin, w1, Ax, w2])
ax.plot(*np.vstack([para_after, para_after[0]]).T, color=C.GRAY, lw=1.2, ls=":", zorder=2)
arrow(ax, origin, w1, color=C.INK, lw=2.2)
label(ax, r"$3(1,1)=(3,3)$", w1, offset=(6, 6), color=C.INK)
label(ax, r"$\times3$", (1.62, 1.62), offset=(0, 0), color=C.INK, ha="center")
arrow(ax, origin, w2, color=C.INK, lw=2.2)
label(ax, r"$\times1$", (0.90, -0.78), offset=(0, 0), color=C.INK, ha="center")
arrow(ax, origin, Ax, color=C.INK, lw=2.6)
ax.scatter(*Ax, s=58, marker="s", color=C.INK, zorder=6)
label(ax, r"$A\boldsymbol{x}=(4,2)$", Ax, offset=(7, 6), color=C.INK)

save(fig, "L13-n2")

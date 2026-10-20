import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label


def right_angle_at(ax, p, u, v, size=0.18):
    u = np.asarray(u, dtype=float); u = u / np.linalg.norm(u)
    v = np.asarray(v, dtype=float); v = v / np.linalg.norm(v)
    p = np.asarray(p, dtype=float)
    p1 = p + size * u
    p2 = p + size * (u + v)
    p3 = p + size * v
    ax.plot([p1[0], p2[0], p3[0]], [p1[1], p2[1], p3[1]],
            color=C.INK, lw=1.0, zorder=5)


fig, ax = new_fig(10.8, 8.0)
fig.subplots_adjust(left=0.12, right=0.97, bottom=0.12, top=0.93)
ax.set_aspect("equal", adjustable="box")
ax.set_xlim(-1.5, 3.0); ax.set_ylim(-1.5, 3.0)
ax.set_xticks([-1, 0, 1, 2, 3]); ax.set_yticks([-1, 0, 1, 2, 3])
ax.axhline(0, color=C.GRAY, lw=0.8, zorder=0)
ax.axvline(0, color=C.GRAY, lw=0.8, zorder=0)
label(ax, "$x_1$", (2.95, 0), offset=(-2, -16), ha="right")
label(ax, "$x_2$", (0, 2.95), offset=(7, -6))

# 全部最小二乘解：x1 + x2 = 2（粗实线）
x = np.linspace(-1.5, 3.0, 300)
ax.plot(x, 2.0 - x, color=C.INK, lw=2.1, zorder=2)
label(ax, "最小二乘解 $x_1+x_2=2$", (0.3, 1.7), offset=(12, 8), ha="left")

# 零空间：过原点、方向 (-1,1) 的直线（虚线），与粗实线平行
z = np.linspace(-1.5, 1.5, 200)
ax.plot(z, -z, color=C.INK, lw=1.2, ls="--", zorder=1)
ax.text(1.15, -1.42, "零空间方向 $(-1,1)$", ha="right", va="bottom", color=C.INK, zorder=6)

# 行空间方向：原点到垂足 (1,1) 的线段（点线）
foot = np.array([1.0, 1.0])
ax.plot([0, 1], [0, 1], color=C.INK, lw=1.4, ls=":", zorder=3)
ax.annotate("行空间方向\n$(1,1)$", xy=(0.55, 0.55), xytext=(1.05, -1.05),
            textcoords="data", ha="left", va="bottom", color=C.INK, zorder=6,
            arrowprops=dict(arrowstyle="-", color=C.GRAY, lw=0.8, shrinkA=2, shrinkB=2))
right_angle_at(ax, foot, (1, -1), (-1, -1), size=0.18)

# 最短解与其他解
dot(ax, foot, size=42)
label(ax, r"$\boldsymbol{x}^+=(1,1)$，长 $\sqrt{2}$", tuple(foot), offset=(8, 7))
for p, off in [(np.array([2.0, 0.0]), (7, 6)), (np.array([0.0, 2.0]), (-10, -4))]:
    ax.scatter([p[0]], [p[1]], s=48, facecolors=C.PAPER, edgecolors=C.INK,
               linewidths=1.4, zorder=5)
    label(ax, "长 2", tuple(p), offset=off, ha="left" if off[0] >= 0 else "right")

save(fig, "L15-n4")

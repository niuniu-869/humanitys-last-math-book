import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label


fig, ax = new_fig(10.5, 8.3)
ax.set_aspect("equal", adjustable="box")

# 主方向与四个中心化数据点
x = np.linspace(-3.0, 3.0, 300)
ax.plot(x, x, color=C.BLUE, lw=1.8, zorder=1)
ax.plot(x, -x, color=C.GRAY, lw=1.4, ls=":", zorder=1)
label(ax, r"$\boldsymbol{v}_1$ 方向", (2.55, 2.55), offset=(0, 6), color=C.BLUE, ha="right")
label(ax, r"$\boldsymbol{v}_2$ 方向", (-2.3, 2.3), offset=(8, 2), color=C.GRAY, ha="left")

points = [np.array([2.0, 1.0]), np.array([1.0, 2.0]),
          np.array([-1.0, -2.0]), np.array([-2.0, -1.0])]
feet = [np.array([1.5, 1.5]), np.array([1.5, 1.5]),
        np.array([-1.5, -1.5]), np.array([-1.5, -1.5])]
texts = [r"$(2,1)$", r"$(1,2)$", r"$(-1,-2)$", r"$(-2,-1)$"]
offsets = [(7, -6), (-36, -4), (7, -6), (-44, -4)]

for p, f, txt, off in zip(points, feet, texts, offsets):
    ax.plot([p[0], f[0]], [p[1], f[1]], color=C.GRAY, lw=1.2, ls="--", zorder=2)
    dot(ax, p, color=C.BLUE, size=30)
    label(ax, txt, tuple(p), offset=off, color=C.BLUE)

# 两个共享垂足用空心点表示
for f in (feet[0], feet[2]):
    ax.scatter([f[0]], [f[1]], s=42, facecolors=C.PAPER, edgecolors=C.INK,
               linewidths=1.4, zorder=5)
label(ax, r"长 $\frac{1}{\sqrt{2}}$", (1.75, 1.25), offset=(7, 3), color=C.GRAY)

ax.axhline(0, color=C.GRAY, lw=0.8, zorder=0)
ax.axvline(0, color=C.GRAY, lw=0.8, zorder=0)
ax.set_xlim(-3.0, 3.0); ax.set_ylim(-3.0, 3.0)
ax.set_xticks([-2, 0, 2]); ax.set_yticks([-2, 0, 2])
ax.set_xlabel("测验 1")
ax.set_ylabel("测验 2")

save(fig, "L15-n2")

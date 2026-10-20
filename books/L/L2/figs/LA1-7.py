import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import C, arrow, dot, label, new_fig, np, plt, save

fig, ax = new_fig(11.5, 8.0)

a = np.array([2.0, 1.0])
b = np.array([1.0, 3.0])
p = (a @ b) / (a @ a) * a          # 垂足 p=(2,1)
e = b - p                          # 残差 e=(-1,2)
q = 2.0 * a                        # 直线上另一点 q=(4,2)

# 直线 span(a)
xs = np.array([-1.05, 6.65])
ax.plot(xs, xs / 2.0, color=C.GRAY, lw=1.1, zorder=1)

# 斜边 b->q（珊瑚色虚线）与直角边 p->q（灰）
ax.plot([b[0], q[0]], [b[1], q[1]], color=C.RED, lw=1.7, ls=(0, (5, 3)), zorder=2)
ax.plot([p[0], q[0]], [p[1], q[1]], color=C.GRAY, lw=2.2, zorder=2)

# 三个箭头
arrow(ax, (0, 0), a, color=C.BLUE, lw=1.8)
arrow(ax, (0, 0), b, color=C.BLUE, lw=1.8)
arrow(ax, p, e, color=C.TEAL, lw=1.8)

# p 处的直角符号（夹在 e 与 p->q 之间）
u1 = e / np.linalg.norm(e)
u2 = (q - p) / np.linalg.norm(q - p)
s = 0.30
sq = [p + s * u1, p + s * u1 + s * u2, p + s * u2]
ax.plot([v[0] for v in sq], [v[1] for v in sq], color=C.INK, lw=1.0, zorder=4)

# 关键点
dot(ax, (0, 0), color=C.INK, size=18)
dot(ax, p, color=C.TEAL, size=28)
dot(ax, b, color=C.BLUE, size=28)
dot(ax, q, color=C.INK, size=22)

# 标注
label(ax, "$O$", (0, 0), offset=(-8, -7), ha="right", va="top")
label(ax, r"$\boldsymbol{a}$", (1.5, 0.75), offset=(0, -16), ha="center", va="top", color=C.BLUE)
label(ax, r"$\boldsymbol{p}$", (2, 1), offset=(7, -11), ha="left", va="top", color=C.TEAL)
label(ax, r"$\boldsymbol{b}=(1,3)$", (1, 3), offset=(-10, 8), ha="right", va="bottom", color=C.BLUE)
label(ax, r"$\boldsymbol{q}=(4,2)$", (4, 2), offset=(7, -12), ha="left", va="top")
label(ax, r"$\boldsymbol{e}$", (1.5, 2.0), offset=(8, 0), ha="left", va="center", color=C.TEAL)
label(ax, "斜边", (2.5, 2.5), offset=(10, 10), ha="left", va="bottom", color=C.RED)
label(ax, r"$\operatorname{span}(\boldsymbol{a})$", (6.5, 3.25), offset=(0, 9), ha="right", va="bottom", color=C.GRAY)

ax.set_xlim(-1.05, 6.85)
ax.set_ylim(-1.05, 4.5)
ax.spines["left"].set_position(("data", 0))
ax.spines["bottom"].set_position(("data", 0))
ax.spines["left"].set_color(C.LIGHT)
ax.spines["bottom"].set_color(C.LIGHT)
ax.set_xticks([2, 4, 6])
ax.set_yticks([2, 4])
ax.set_aspect("equal")

save(fig, "LA1-7")

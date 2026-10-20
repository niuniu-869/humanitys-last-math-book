import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label


def right_angle(ax, u, v, size=0.18):
    """在原点画由单位方向 u,v 张成的小直角记号。"""
    u = np.asarray(u, dtype=float); u = u / np.linalg.norm(u)
    v = np.asarray(v, dtype=float); v = v / np.linalg.norm(v)
    p1 = size * u
    p2 = size * (u + v)
    p3 = size * v
    ax.plot([p1[0], p2[0], p3[0]], [p1[1], p2[1], p3[1]],
            color=C.INK, lw=1.0, zorder=5)


def dashed_arrow(ax, start, vec, color=C.GRAY, lw=1.7):
    x, y = start
    dx, dy = vec
    ax.annotate("", xy=(x + dx, y + dy), xytext=(x, y),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                linestyle="--", shrinkA=0, shrinkB=0,
                                mutation_scale=11), zorder=4)


fig, (ax1, ax2) = new_fig(17.2, 7.3, ncols=2)
fig.subplots_adjust(wspace=0.42, left=0.07, right=0.96, bottom=0.12, top=0.92)

# 左图：单位圆与两组输入方向
t = np.linspace(0.0, 2.0 * np.pi, 500)
ax1.plot(np.cos(t), np.sin(t), color=C.INK, lw=1.2)
v1 = np.array([1.0, 1.0]) / np.sqrt(2.0)
v2 = np.array([-1.0, 1.0]) / np.sqrt(2.0)
e1 = np.array([1.0, 0.0])
e2 = np.array([0.0, 1.0])
arrow(ax1, (0.0, 0.0), v1, color=C.BLUE, lw=1.9)
arrow(ax1, (0.0, 0.0), v2, color=C.BLUE, lw=1.9)
dashed_arrow(ax1, (0.0, 0.0), e1)
dashed_arrow(ax1, (0.0, 0.0), e2)
label(ax1, r"$\boldsymbol{v}_1$", tuple(v1), offset=(7, 5), color=C.BLUE)
label(ax1, r"$\boldsymbol{v}_2$", tuple(v2), offset=(-6, 4), color=C.BLUE, ha="right")
label(ax1, r"$\boldsymbol{e}_1$", tuple(e1), offset=(5, -15), color=C.GRAY)
label(ax1, r"$\boldsymbol{e}_2$", tuple(e2), offset=(6, 2), color=C.GRAY)
right_angle(ax1, v1, v2, size=0.19)
dot(ax1, (0.0, 0.0), color=C.INK, size=18)
ax1.set_xlim(-1.5, 1.5); ax1.set_ylim(-1.5, 1.5)
ax1.set_aspect("equal", adjustable="box")
ax1.set_xticks([-1, 0, 1]); ax1.set_yticks([-1, 0, 1])
ax1.axhline(0, color=C.GRAY, lw=0.8, zorder=0)
ax1.axvline(0, color=C.GRAY, lw=0.8, zorder=0)
ax1.set_title("输入：单位圆", pad=8)

# 右图：椭圆与输出方向
A = np.array([[3.0, 0.0], [4.0, 5.0]])
ellipse = A @ np.vstack([np.cos(t), np.sin(t)])
ax2.plot(ellipse[0], ellipse[1], color=C.INK, lw=1.2)
Av1 = A @ v1
Av2 = A @ v2
Ae1 = A @ e1
Ae2 = A @ e2
arrow(ax2, (0.0, 0.0), Av1, color=C.BLUE, lw=1.9)
arrow(ax2, (0.0, 0.0), Av2, color=C.BLUE, lw=1.9)
dashed_arrow(ax2, (0.0, 0.0), Ae1)
dashed_arrow(ax2, (0.0, 0.0), Ae2)
label(ax2, r"$\sigma_1\boldsymbol{u}_1$（长 $3\sqrt{5}$）", tuple(Av1), offset=(8, 8), color=C.BLUE)
label(ax2, r"$\sigma_2\boldsymbol{u}_2$（长 $\sqrt{5}$）", tuple(Av2), offset=(-6, 6), color=C.BLUE, ha="right")
label(ax2, r"$A\boldsymbol{e}_1=(3,4)$", tuple(Ae1), offset=(6, 5), color=C.GRAY)
label(ax2, r"$A\boldsymbol{e}_2=(0,5)$", tuple(Ae2), offset=(-4, 6), color=C.GRAY, ha="right")
label(ax2, "不垂直", (4.0, 1.0), offset=(0, 0), color=C.INK, ha="center")
right_angle(ax2, Av1, Av2, size=0.72)
dot(ax2, (0.0, 0.0), color=C.INK, size=18)
ax2.set_xlim(-7.5, 7.5); ax2.set_ylim(-7.5, 7.5)
ax2.set_aspect("equal", adjustable="box")
ax2.set_xticks([-5, 0, 5]); ax2.set_yticks([-5, 0, 5])
ax2.axhline(0, color=C.GRAY, lw=0.8, zorder=0)
ax2.axvline(0, color=C.GRAY, lw=0.8, zorder=0)
ax2.set_title("输出：椭圆", pad=8)

# 两幅图之间的线性变换箭头
ax1.annotate("", xy=(0.535, 0.52), xycoords="figure fraction",
             xytext=(0.465, 0.52), textcoords="figure fraction",
             arrowprops=dict(arrowstyle="-|>", color=C.INK, lw=1.5))
fig.text(0.50, 0.57, "$A$", ha="center", va="center", color=C.INK)

save(fig, "L15-n1")

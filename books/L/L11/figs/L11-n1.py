import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Arc

fig, ax = new_fig(13.5, 10.0)
ax.set_aspect("equal", adjustable="box")
ax.set_xlim(-3.3, 3.3)
ax.set_ylim(-3.3, 3.3)
ax.set_xticks(np.arange(-3, 4, 1))
ax.set_yticks(np.arange(-3, 4, 1))
ax.grid(True, color=C.LIGHT, lw=0.7, alpha=0.65, zorder=0)
ax.axhline(0, color=C.GRAY, lw=0.9, zorder=1)
ax.axvline(0, color=C.GRAY, lw=0.9, zorder=1)
ax.set_xlabel("$x$")
ax.set_ylabel("$y$")

# 两条不转向的方向：点线贯穿画面
xs = np.array([-3.3, 3.3])
ax.plot(xs, xs, color=C.GRAY, lw=1.2, ls=":", zorder=1)
ax.plot(xs, -xs, color=C.GRAY, lw=1.2, ls=":", zorder=1)
label(ax, r"$(1,1)^T$ 方向", (3.05, 3.05), offset=(-2, 2), color=C.GRAY, ha="right")
label(ax, r"$(-1,1)^T$ 方向", (-2.30, 2.30), offset=(8, 2), color=C.GRAY, ha="left", va="bottom")

# 单位圆及其在 A 下的椭圆像
th = np.linspace(0.0, 2.0 * np.pi, 600)
ax.plot(np.cos(th), np.sin(th), color=C.INK, lw=1.5, ls="--", zorder=2)
ex = 2.0 * np.cos(th) + np.sin(th)
ey = np.cos(th) + 2.0 * np.sin(th)
ax.plot(ex, ey, color=C.BLUE, lw=2.2, ls="-", zorder=2)
label(ax, "单位圆", (0.72, -0.70), offset=(4, -4), color=C.INK, ha="left", va="top")
label(ax, "$A$ 下的椭圆", (1.20, 2.28), offset=(5, 3), color=C.BLUE)

O = np.array([0.0, 0.0])
e1 = np.array([1.0, 0.0])
Ae1 = np.array([2.0, 1.0])
u = np.array([1.0, 1.0]) / np.sqrt(2.0)
Au = 3.0 * u
w = np.array([-1.0, 1.0]) / np.sqrt(2.0)
Aw = w.copy()

# e1 -> Ae1：原向量细实线、像粗实线，并用小圆弧提示方向改变
arrow(ax, O, e1, color=C.GRAY, lw=1.25)
arrow(ax, O, Ae1, color=C.BLUE, lw=2.4)
label(ax, r"$\boldsymbol{e}_1$", e1, offset=(3, -15), color=C.GRAY)
label(ax, r"$A\boldsymbol{e}_1$", Ae1, offset=(9, -2), color=C.BLUE)
label(ax, "方向转了", Ae1, offset=(9, -17), color=C.RED)
ang = float(np.degrees(np.arctan2(Ae1[1], Ae1[0])))
ax.add_patch(Arc(O, 0.95, 0.95, angle=0, theta1=0, theta2=ang,
                 color=C.RED, lw=1.15, zorder=4))

# u -> Au：沿 y=x 方向伸长 3 倍
arrow(ax, O, u, color=C.GRAY, lw=1.25)
arrow(ax, O, Au, color=C.BLUE, lw=2.6)
label(ax, r"$\boldsymbol{u}$", u, offset=(-18, 8), color=C.GRAY)
label(ax, r"$A\boldsymbol{u}=3\boldsymbol{u}$", Au, offset=(7, -15), color=C.BLUE)
label(ax, "伸长 3 倍", (1.2, 1.2), offset=(-8, 6), color=C.BLUE, ha="right")

# w -> Aw：重合，像用更粗箭头强调不变
arrow(ax, O, w, color=C.GRAY, lw=1.25)
arrow(ax, O, Aw, color=C.BLUE, lw=3.0)
label(ax, r"$\boldsymbol{w}=A\boldsymbol{w}$（不变）", Aw, offset=(-8, 6), color=C.BLUE, ha="right", va="bottom")

# 原点用实心点，关键特征方向端点用空心点作辅助区分
DotSize = 23
dot(ax, O, color=C.INK, size=DotSize)
ax.scatter([Au[0], Aw[0]], [Au[1], Aw[1]], s=34, facecolors=C.PAPER,
           edgecolors=C.BLUE, linewidths=1.4, zorder=5)

save(fig, "L11-n1")

import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

# 2 行 × 3 列：上排曲面，下排等高线
fig, ax0 = new_fig(18.0, 11.2)
fig.delaxes(ax0)
gs = fig.add_gridspec(2, 3, left=0.055, right=0.985, bottom=0.07, top=0.91,
                      wspace=0.25, hspace=0.32)

x = np.linspace(-1.5, 1.5, 81)
y = np.linspace(-1.5, 1.5, 81)
X, Y = np.meshgrid(x, y)

surfaces = [
    (X**2 + Y**2, r"碗：$x^2+y^2$（正定）"),
    (X**2 - Y**2, r"马鞍：$x^2-y^2$（不定）"),
    (X**2, r"槽：$x^2$（半正定）"),
]

# 上排三维曲面。曲面透明度控制在 0.55 以下，叠加浅线框保证黑白打印可辨。
for j, (Z, title) in enumerate(surfaces):
    ax = fig.add_subplot(gs[0, j], projection="3d")
    ax.view_init(elev=27, azim=-58)
    for a in (ax.xaxis, ax.yaxis, ax.zaxis):
        a.pane.set_facecolor((1, 1, 1, 0))
        a.pane.set_edgecolor(C.LIGHT)
        a._axinfo["grid"]["color"] = (0.85, 0.85, 0.85, 0.55)
    ax.plot_surface(X, Y, Z, color=C.LIGHT, alpha=0.42, linewidth=0, antialiased=True,
                    shade=False, rcount=24, ccount=24)
    ax.plot_wireframe(X, Y, Z, rstride=8, cstride=8, color=C.GRAY, linewidth=0.45,
                      alpha=0.55)
    ax.set_title(title, pad=8)
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    if j == 0:
        ax.set_zlim(0, 4.5)
    elif j == 1:
        ax.set_zlim(-2.4, 2.4)
    else:
        ax.set_zlim(0, 2.4)
    ax.set_xticks([-1, 0, 1])
    ax.set_yticks([-1, 0, 1])
    ax.set_zticks([])
    ax.set_xlabel("$x$", labelpad=-4)
    ax.set_ylabel("$y$", labelpad=-4)
    ax.tick_params(pad=-2, labelsize=8)

# 下排等高线
# 碗：同心圆 z=0.5, 1, 2；原点实心点并标最低点。
ax = fig.add_subplot(gs[1, 0])
ax.set_aspect("equal")
th = np.linspace(0, 2 * np.pi, 600)
for z, t, off in [(0.5, -0.22, (5, -2)), (1.0, 0.30, (5, 3)), (2.0, 0.72, (5, 3))]:
    r = np.sqrt(z)
    ax.plot(r * np.cos(th), r * np.sin(th), color=C.INK, lw=1.25, ls="-")
    # 三个高度值错开摆放，避免文字相互遮挡。
    label(ax, f"$z={z:g}$", (r * np.cos(t), r * np.sin(t)), offset=off, color=C.INK)
ax.scatter([0], [0], s=34, color=C.INK, zorder=5)
label(ax, "最低点", (0, 0), offset=(6, 5), color=C.INK)
ax.set_title("碗的等高线", pad=12)
ax.set_xlim(-1.6, 1.6)
ax.set_ylim(-1.6, 1.6)
ax.set_xticks([-1, 0, 1])
ax.set_yticks([-1, 0, 1])
ax.set_xlabel("$x$")
ax.set_ylabel("$y$")

# 马鞍：正值实线、负值虚线，零值渐近线点线。
ax = fig.add_subplot(gs[1, 1])
ax.set_aspect("equal")
for z, ls in [(0.5, "-"), (1.0, "-")]:
    a = np.sqrt(z)
    yy = np.linspace(-1.5, 1.5, 600)
    xx = np.sqrt(a * a + yy * yy)
    ax.plot(xx, yy, color=C.INK, lw=1.15, ls=ls)
    ax.plot(-xx, yy, color=C.INK, lw=1.15, ls=ls)
    label(ax, f"$z={z:g}$", (xx[-1], yy[-1]), offset=(-18, 2), color=C.INK, ha="right")
for z in (-0.5, -1.0):
    a = np.sqrt(-z)
    xx = np.linspace(-1.5, 1.5, 600)
    yy = np.sqrt(a * a + xx * xx)
    ax.plot(xx, yy, color=C.INK, lw=1.15, ls="--")
    ax.plot(xx, -yy, color=C.INK, lw=1.15, ls="--")
    label(ax, f"$z={z:g}$", (xx[-1], -yy[-1]), offset=(-18, -2), color=C.INK, ha="right")
line = np.linspace(-1.5, 1.5, 200)
ax.plot(line, line, color=C.GRAY, lw=1.0, ls=":")
ax.plot(line, -line, color=C.GRAY, lw=1.0, ls=":")
label(ax, r"$y=\pm x$", (0.96, -0.96), offset=(4, 2), color=C.INK,
      bbox=dict(facecolor=C.PAPER, edgecolor="none", pad=1.0))
ax.set_title("马鞍的等高线（实线 $z>0$，虚线 $z<0$）", pad=12)
ax.set_xlim(-1.6, 1.6)
ax.set_ylim(-1.6, 1.6)
ax.set_xticks([-1, 0, 1])
ax.set_yticks([-1, 0, 1])
ax.set_xlabel("$x$")
ax.set_ylabel("$y$")

# 槽：x=±0.7, ±1 的实线；y 轴为 z=0 的点线。
ax = fig.add_subplot(gs[1, 2])
ax.set_aspect("equal")
r5 = np.sqrt(0.5)
for xv in (-1.0, -r5, r5, 1.0):
    ax.plot([xv, xv], [-1.5, 1.5], color=C.INK, lw=1.2, ls="-")
for xv, dx, ha in ((-1.0, -0.06, "right"), (1.0, 0.06, "left")):
    ax.text(xv + dx, 0.7, "$z=1$", ha=ha, va="center", rotation=90, fontsize=8.5, color=C.INK)
for xv, dx, ha in ((-r5, 0.06, "left"), (r5, -0.06, "right")):
    ax.text(xv + dx, -0.7, "$z=0.5$", ha=ha, va="center", rotation=90, fontsize=8.5, color=C.INK)
ax.plot([0, 0], [-1.5, 1.5], color=C.GRAY, lw=1.0, ls=":")
ax.text(0.06, 0.7, "$z=0$", ha="left", va="center", rotation=90, fontsize=8.5, color=C.INK)
ax.set_title("槽的等高线（沿 $y$ 方向是平的）", pad=12)
ax.set_xlim(-1.6, 1.6)
ax.set_ylim(-1.6, 1.6)
ax.set_xticks([-1, 0, 1])
ax.set_yticks([-1, 0, 1])
ax.set_xlabel("$x$")
ax.set_ylabel("$y$")

save(fig, "L14-n4")

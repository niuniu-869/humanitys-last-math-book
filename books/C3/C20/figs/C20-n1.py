import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label


def surface_panel(ax, saddle=False):
    x = np.linspace(-1.5, 1.5, 25)
    y = np.linspace(-1.5, 1.5, 25)
    X, Y = np.meshgrid(x, y)
    Z = X**2 - Y**2 if saddle else X**2 + Y**2
    ax.plot_wireframe(X, Y, Z, rstride=2, cstride=2, color=C.LIGHT,
                      linewidth=0.55, zorder=1)
    t = np.linspace(-1.5, 1.5, 400)
    if saddle:
        ax.plot(t, np.zeros_like(t), t**2, color=C.INK, lw=2.6, zorder=10)
        ax.plot(np.zeros_like(t), t, -t**2, color=C.INK, lw=2.6, zorder=10)
    else:
        ax.plot(t, np.zeros_like(t), t**2, color=C.INK, lw=2.6, zorder=10)
        ax.plot(np.zeros_like(t), t, t**2, color=C.INK, lw=2.6, zorder=10)
    ax.scatter([0], [0], [0], s=30, color=C.INK, depthshade=False, zorder=11)
    ax.set(xlim=(-1.5, 1.5), ylim=(-1.5, 1.5),
           xlabel="x", ylabel="y")
    ax.xaxis.labelpad = 3
    ax.yaxis.labelpad = 3
    # z 轴没有刻度，直接把 z 贴在本图 z 轴旁，避免飘到两图中间
    ax.text2D(0.965, 0.55, "z", transform=ax.transAxes, rotation=90,
              ha="center", va="center", fontsize=10)
    ax.tick_params(axis="both", labelsize=8.5, pad=1)
    ax.set_xticks([-1, 0, 1]); ax.set_yticks([-1, 0, 1]); ax.set_zticks([])
    ax.set_box_aspect((1, 1, 1))


fig = plt.figure(figsize=(16 / 2.54, 12.5 / 2.54))
ax1 = fig.add_subplot(221, projection="3d"); ax1.view_init(elev=25, azim=-60)
ax2 = fig.add_subplot(222, projection="3d"); ax2.view_init(elev=25, azim=-60)
for ax in (ax1, ax2):
    ax.computed_zorder = False
    for a in (ax.xaxis, ax.yaxis, ax.zaxis):
        a.pane.set_facecolor((1, 1, 1, 0)); a.pane.set_edgecolor(C.LIGHT)
        a._axinfo["grid"]["color"] = (0.85, 0.85, 0.85, 0.6)
surface_panel(ax1); surface_panel(ax2, True)
ax1.set_title("碗", pad=4); ax2.set_title("鞍", pad=4)

ax3 = fig.add_subplot(223, aspect="equal")
u = np.linspace(-2, 2, 500); U, V = np.meshgrid(u, u)
cs = ax3.contour(U, V, U**2 + V**2, levels=[0.5, 1, 2, 3],
                 colors=C.INK, linewidths=1.3, linestyles="solid")
# 每条等高线只标一次；位置取在该圆上、远离其它圆的地方
def curve_label(ax, text, xy, angle):
    ax.text(*xy, text, rotation=angle, ha="center", va="center",
            fontsize=8.5, color=C.INK, zorder=6,
            bbox=dict(boxstyle="square,pad=0.10", fc=C.PAPER, ec="none"))

bowl_lab = [("0.5", (-0.5, -0.5), -45), ("1", (0.7071, 0.7071), -45),
            ("2", (-1.329, 0.484), 70), ("3", (0.866, -1.5), 30)]
for text, xy, ang in bowl_lab:
    curve_label(ax3, text, xy, ang)
ax3.set(xlim=(-2, 2), ylim=(-2, 2), xlabel="x", ylabel="y")
ax3.set_title("等高线", pad=1)

ax4 = fig.add_subplot(224, aspect="equal")
cs = ax4.contour(U, V, U**2 - V**2, levels=[-2, -1, -0.5, 0.5, 1, 2],
                 colors=C.INK, linewidths=1.2, linestyles="solid")
saddle_lab = [
    ("0.5", (0.789, 0.35), 66), ("1", (1.060, 0.35), 71.7),
    ("2", (1.457, 0.35), 76.5), ("-0.5", (-0.2, 0.735), -15),
    ("-1", (-0.2, 1.020), -11), ("-2", (-0.2, 1.428), -8),
]
for text, xy, ang in saddle_lab:
    curve_label(ax4, text, xy, ang)
ax4.plot(u, u, ls="--", color=C.INK, lw=1.2)
ax4.plot(u, -u, ls="--", color=C.INK, lw=1.2)
# 左右两块 x 占优，z>0；上下两块 y 占优，z<0
label(ax4, "z>0", (1.76, 0.0), offset=(0, 0), ha="center", va="center", fontsize=9)
label(ax4, "z>0", (-1.76, 0.0), offset=(0, 0), ha="center", va="center", fontsize=9)
label(ax4, "z<0", (0.0, 1.73), offset=(0, 0), ha="center", va="center", fontsize=9)
label(ax4, "z<0", (0.0, -1.73), offset=(0, 0), ha="center", va="center", fontsize=9)
ax4.set(xlim=(-2, 2), ylim=(-2, 2), xlabel="x", ylabel="y")
ax4.set_title("等高线", pad=1)

fig.subplots_adjust(left=0.06, right=0.95, top=0.97, bottom=0.06,
                    wspace=0.10, hspace=0.52)
save(fig, "C20-n1")

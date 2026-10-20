import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from mpl_toolkits.mplot3d import proj3d
from matplotlib.patches import ConnectionPatch

fig = plt.figure(figsize=(17.5 / 2.54, 8.2 / 2.54))
ax = fig.add_subplot(121, projection="3d"); ax.view_init(elev=20, azim=-55)
ax.computed_zorder = False
for a in (ax.xaxis, ax.yaxis, ax.zaxis):
    a.pane.set_facecolor((1, 1, 1, 0)); a.pane.set_edgecolor(C.LIGHT)
    a._axinfo["grid"]["color"] = (0.85, 0.85, 0.85, 0.6)

x = np.linspace(-1, 1, 41); y = np.linspace(-1, 1, 41); X, Y = np.meshgrid(x, y)
R2 = X**2 + Y**2
Z = np.divide(X*Y, R2, out=np.full_like(R2, np.nan), where=R2 >= 0.05**2)
ax.plot_wireframe(X, Y, Z, rstride=2, cstride=2, color=C.LIGHT,
                  linewidth=0.5, zorder=1)

t = np.linspace(-1, 1, 300)
ax.plot(t, np.zeros_like(t), np.zeros_like(t), color=C.INK, lw=2.6, zorder=10)
ax.plot(t, t, np.full_like(t, 0.5), color=C.INK, lw=2.6, zorder=10)
# 实心点：已定义的 h(0,0)=0；去心极限不存在，不用点标记
ax.scatter([0], [0], [0], s=40, color=C.INK, depthshade=False, zorder=12)

ax.set(xlim=(-1, 1), ylim=(-1, 1), zlim=(-0.65, 0.7),
       xlabel="x", ylabel="y")
ax.xaxis.labelpad = 4; ax.yaxis.labelpad = 4
ax.tick_params(axis="both", labelsize=8, pad=1)
ax.set_xticks([-1, 0, 1]); ax.set_yticks([-1, 0, 1])
ax.set_zticks([])
# z 轴（函数值 h）没有刻度，把 h 贴在本图 z 轴旁，避免和右图 y 轴混在一起
ax.text2D(0.945, 0.55, "h", transform=ax.transAxes, rotation=90,
          ha="center", va="center", fontsize=10)
ax.set_box_aspect((1, 1, 1.25))
ax.set_position([0.175, 0.10, 0.335, 0.84])

ax2 = fig.add_subplot(122, aspect="equal")
theta = np.deg2rad(np.arange(0, 180, 15)); r = np.linspace(0, 1.55, 100)
for th in theta:
    ax2.plot(r*np.cos(th), r*np.sin(th), color=C.INK, lw=1.0)
    val = 0.5*np.sin(2*th)
    if abs(val) < 0.005:
        val = 0.0
    txt = f"{val:.2f}".replace("-", "−")
    rr = 1.72
    label(ax2, txt, (rr*np.cos(th), rr*np.sin(th)), offset=(0, 0),
          ha="center", va="center", fontsize=8)
ax2.scatter([0], [0], s=22, color=C.INK, zorder=5)
ax2.set(xlim=(-2.05, 2.05), ylim=(-1.86, 1.86), xlabel="x", ylabel="y")
ax2.set_xticks([-1, 0, 1]); ax2.set_yticks([-1, 0, 1])
ax2.set_position([0.575, 0.11, 0.405, 0.81])

fig.subplots_adjust(left=0.05, right=0.98, top=0.97, bottom=0.08)
fig.canvas.draw()

# 图外空白处的文字，用细引线指到对应位置
def outside_label(text, target, y_frac, ha="right", x_frac=-0.055):
    xp, yp, _ = proj3d.proj_transform(*target, ax.get_proj())
    disp = ax.transData.transform((xp, yp))
    fxy = fig.transFigure.inverted().transform(disp)
    ax.text2D(x_frac, y_frac, text, transform=ax.transAxes, ha=ha,
              va="center", fontsize=8.5, color=C.INK)
    fig.add_artist(ConnectionPatch(xyA=(x_frac, y_frac), coordsA=ax.transAxes,
                                   xyB=fxy, coordsB=fig.transFigure,
                                   arrowstyle="-", color=C.GRAY, lw=0.6,
                                   shrinkA=1.5, shrinkB=1.0))

outside_label("沿 y=x：1/2", (-0.88, -0.88, 0.5), 0.95)
outside_label("沿 x 轴：0", (-0.88, 0.0, 0.0), 0.40)
outside_label("h(0,0)=0", (0.0, 0.0, 0.0), 0.18)

save(fig, "C20-n2")

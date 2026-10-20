import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label, HALO
from mpl_toolkits.mplot3d import proj3d
from matplotlib.patches import ConnectionPatch

fig = plt.figure(figsize=(15.5 / 2.54, 11.5 / 2.54))
ax = fig.add_subplot(111, projection="3d")
ax.view_init(elev=25, azim=-57)
ax.computed_zorder = False
for a in (ax.xaxis, ax.yaxis, ax.zaxis):
    a.pane.set_facecolor((1, 1, 1, 0)); a.pane.set_edgecolor(C.LIGHT)
    a._axinfo["grid"]["color"] = (0.85, 0.85, 0.85, 0.6)

x = np.linspace(-2, 2, 26); y = np.linspace(-3, 3, 32)
X, Y = np.meshgrid(x, y)
ax.plot_wireframe(X, Y, X**2 + Y**2, rstride=2, cstride=2,
                  color=C.LIGHT, linewidth=0.55, zorder=1)

# 两块被切的平面：规则矩形，浅灰填充 + 细实线边界
xs = np.array([0.2, 1.8]); zs1 = np.array([4.2, 5.8])
Xp, Zp = np.meshgrid(xs, zs1)
ax.plot_surface(Xp, np.full_like(Xp, 2.0), Zp, color=C.LIGHT, alpha=0.32,
                edgecolor="none", shade=False, zorder=2)
ys2 = np.array([1.2, 2.8]); zs2 = np.array([4.0, 6.0])
Yp, Zp2 = np.meshgrid(ys2, zs2)
ax.plot_surface(np.full_like(Yp, 1.0), Yp, Zp2, color=C.LIGHT, alpha=0.32,
                edgecolor="none", shade=False, zorder=2)

def rect_border(pts):
    pts = list(pts) + [pts[0]]
    ax.plot([p[0] for p in pts], [p[1] for p in pts], [p[2] for p in pts],
            color=C.INK, lw=1.0, zorder=4)

rect_border([(0.2, 2.0, 4.2), (1.8, 2.0, 4.2),
             (1.8, 2.0, 5.8), (0.2, 2.0, 5.8)])
rect_border([(1.0, 1.2, 4.0), (1.0, 2.8, 4.0),
             (1.0, 2.8, 6.0), (1.0, 1.2, 6.0)])

# 两条截线（粗实线）
t = np.linspace(-2, 2, 300)
ax.plot(t, np.full_like(t, 2), t**2 + 4, color=C.INK, lw=2.3, zorder=10)
t2 = np.linspace(-3, 3, 300)
ax.plot(np.full_like(t2, 1), t2, 1 + t2**2, color=C.INK, lw=2.3, zorder=10)

# P 与两条切线（虚线，沿切线方向各 ±0.8）
ax.scatter([1], [2], [5], s=90, color=C.INK, depthshade=False, zorder=13)
tt = np.linspace(-0.8, 0.8, 120)
ax.plot(1 + tt, np.full_like(tt, 2), 5 + 2*tt, color=C.INK, lw=2.2,
        ls=(0, (3, 2)), zorder=12)
ax.plot(np.full_like(tt, 1), 2 + tt, 5 + 4*tt, color=C.INK, lw=2.2,
        ls=(0, (3, 2)), zorder=12)

ax.set(xlim=(-2, 2), ylim=(-3, 3), zlim=(0, 13.2),
       xlabel="x", ylabel="y")
ax.xaxis.labelpad = 4; ax.yaxis.labelpad = 4
ax.tick_params(axis="both", labelsize=8, pad=1)
ax.set_xticks([-2, 0, 2]); ax.set_yticks([-3, 0, 3])
ax.set_zticks([])
ax.set_position([0.12, 0.06, 0.64, 0.88])
# z 轴无刻度，直接贴在 z 轴旁
ax.text2D(0.99, 0.76, "z", transform=ax.transAxes, rotation=90,
          ha="center", va="center", fontsize=10)

fig.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.02)
fig.canvas.draw()

def target_fig(xy3):
    xp, yp, _ = proj3d.proj_transform(*xy3, ax.get_proj())
    disp = ax.transData.transform((xp, yp))
    return fig.transFigure.inverted().transform(disp)

def side_label(text, xy3, ax_xy):
    fxy = target_fig(xy3)
    ax.text2D(*ax_xy, text, transform=ax.transAxes, ha="left", va="center",
              fontsize=8.5, color=C.INK)
    fig.add_artist(ConnectionPatch(xyA=ax_xy, coordsA=ax.transAxes,
                                   xyB=fxy, coordsB=fig.transFigure,
                                   arrowstyle="-", color=C.GRAY, lw=0.6,
                                   shrinkA=1.5, shrinkB=1.0))

side_label("$f_x=2$", (1.70, 2.0, 6.4), (1.015, 0.52))
side_label("$f_y=4$", (1.0, 2.75, 7.9), (1.015, 0.66))
side_label("平面 $x=1$", (1.0, 2.72, 4.55), (1.015, 0.40))

# 二维文字（3D 的 annotate 会再次投影，位置会跑）
def fig_text(text, target, dx, dy, ha="center", va="center", leader=False, fs=8.5):
    fxy = target_fig(target)
    tx, ty = fxy[0] + dx, fxy[1] + dy
    fig.text(tx, ty, text, ha=ha, va=va, fontsize=fs, color=C.INK,
             path_effects=HALO, zorder=30)
    if leader:
        fig.add_artist(ConnectionPatch(xyA=(tx, ty), coordsA=fig.transFigure,
                                       xyB=fxy, coordsB=fig.transFigure,
                                       arrowstyle="-", color=C.GRAY, lw=0.6,
                                       shrinkA=2.0, shrinkB=1.0))

fig_text("平面 $y=2$", (0.55, 2.0, 4.20), -0.055, -0.055, leader=True)
fig_text("$P$", (1, 2, 5), 0.012, 0.010, ha="left", va="bottom", fs=11)

save(fig, "C20-n3")

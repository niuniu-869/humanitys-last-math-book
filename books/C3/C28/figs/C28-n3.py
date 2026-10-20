import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from mpl_toolkits.mplot3d import proj3d
import matplotlib.patheffects as pe


def p2d(ax, xyz):
    """3D 点 → 投影后的 2D 数据坐标。"""
    x2, y2, _ = proj3d.proj_transform(*xyz, ax.get_proj())
    return (x2, y2)


def label3d(ax, text, xyz, offset=(0, 0), **kw):
    return ax.annotate(text, xy=p2d(ax, xyz), xytext=offset,
                       textcoords="offset points", color=kw.pop("color", C.INK),
                       zorder=7, annotation_clip=False,
                       path_effects=[pe.withStroke(linewidth=2.8, foreground=C.PAPER)], **kw)


def arrow3d(ax, p0, p1, lw=1.8, ms=13, color=C.INK, zorder=5):
    """在 3D 点的投影之间画屏幕空间的实心箭头，箭头大小不随透视缩放。"""
    ax.annotate("", xy=p2d(ax, p1), xytext=p2d(ax, p0),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                shrinkA=0, shrinkB=0, mutation_scale=ms),
                zorder=zorder, annotation_clip=False)


fig, ax = new_fig3d(14.5, 9.5, elev=33, azim=-58)
ax.set_xlim(-1.25, 1.25); ax.set_ylim(-1.25, 1.25); ax.set_zlim(0, 1.45)
fig.canvas.draw()

# 碗形曲面 z = x^2 + y^2, x^2+y^2 <= 1（浅灰网格面）
r = np.linspace(0, 1, 26); t = np.linspace(0, 2 * np.pi, 40)
R, T = np.meshgrid(r, t)
X, Y, Z = R * np.cos(T), R * np.sin(T), R**2
ax.plot_surface(X, Y, Z, cmap=C.CMAP, color=C.GRAY, alpha=0.22,
                linewidth=0.35, edgecolor=C.GRAY, antialiased=True)

# 边界 Gamma：z=1 的圆（从上往下看逆时针）
th = np.linspace(0, 2 * np.pi, 240)
ax.plot(np.cos(th), np.sin(th), np.ones_like(th), color=C.INK, lw=2.5)

# 三个均匀分布的边界箭头：尾端落在 Gamma 上，沿 theta 增大的切线方向
# 伸向圆外。切向短箭头不会像圆内弦那样看起来指向碗内，方向没有歧义。
for a in (4 * np.pi / 9, 10 * np.pi / 9, 16 * np.pi / 9):
    p0 = np.array([np.cos(a), np.sin(a), 1.0])
    tang = np.array([-np.sin(a), np.cos(a), 0.0])
    arrow3d(ax, tuple(p0), tuple(p0 + 0.68 * tang), lw=2.0, ms=10.5, zorder=6)

label3d(ax, r"$\Gamma$", (np.cos(2.60) * 1.13, np.sin(2.60) * 1.13, 1.06),
        offset=(0, 4), ha="center", va="baseline")

# 唯一的一根法向箭头：在曲面中部取点，方向为精确的上侧法向 (-2x,-2y,1)
p = np.array([0.50, 0.30, 0.34])
nvec = np.array([-2 * p[0], -2 * p[1], 1.0])
nvec /= np.linalg.norm(nvec)
tip = p + 0.66 * nvec
arrow3d(ax, tuple(p), tuple(tip), lw=1.9, ms=14, zorder=8)
label3d(ax, r"$\boldsymbol{n}$", tuple(tip), offset=(6, 5), ha="left", va="baseline")

# 「曲面在左手边」：从边界 (1,0,1) 附近向碗内画短点线，文字放在右侧空白处
lead0 = np.array([1.00, 0.00, 1.00])
lead1 = np.array([0.68, 0.08, 0.80])
ax.plot([lead0[0], lead1[0]], [lead0[1], lead1[1]], [lead0[2], lead1[2]],
        color=C.INK, ls=":", lw=1.4, zorder=6)
label3d(ax, "曲面在左手边", (1.13, 0.00, 1.04), offset=(6, 0),
        ha="left", va="center", fontsize=9.0)

ax.set_axis_off()
save(fig, "C28-n3")

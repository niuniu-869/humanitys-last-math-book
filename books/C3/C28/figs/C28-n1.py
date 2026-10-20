import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from mpl_toolkits.mplot3d import proj3d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.patheffects as pe


def p2d(ax, xyz):
    """3D 点 → 投影后的 2D 数据坐标（供 annotate 定位用）。"""
    x2, y2, _ = proj3d.proj_transform(*xyz, ax.get_proj())
    return (x2, y2)


def label3d(ax, text, xyz, offset=(0, 0), **kw):
    """在 3D 点的投影位置旁边写标签，offset 以磅为单位（屏幕方向）。"""
    return ax.annotate(text, xy=p2d(ax, xyz), xytext=offset,
                       textcoords="offset points", color=kw.pop("color", C.INK),
                       zorder=6, annotation_clip=False,
                       path_effects=[pe.withStroke(linewidth=3, foreground=C.PAPER)], **kw)


fig, ax = new_fig3d(13, 9, elev=28, azim=-58)
ax.set_xlim(-1.55, 1.55); ax.set_ylim(-1.55, 1.55); ax.set_zlim(0, 2.35)
fig.canvas.draw()

x = np.linspace(-1.4, 1.4, 35)
y = np.linspace(-1.4, 1.4, 35)
X, Y = np.meshgrid(x, y)
Z = 1.6 - 0.25 * (X**2 + Y**2)
ax.plot_surface(X, Y, Z, cmap=C.CMAP, color=C.GRAY, alpha=0.20,
                linewidth=0.35, edgecolor=C.GRAY, antialiased=True)

# 曲面上的小块：由 0.3×0.3 放大到 0.5×0.5，描边加粗
xs = np.array([0.35, 0.85, 0.85, 0.35])
ys = np.array([0.25, 0.25, 0.75, 0.75])
zs = 1.6 - 0.25 * (xs**2 + ys**2)
patch3d = Poly3DCollection([list(zip(xs, ys, zs))], facecolor=C.LIGHT,
                           edgecolor=C.INK, linewidth=2.2, alpha=0.85)
ax.add_collection3d(patch3d)
proj = Poly3DCollection([list(zip(xs, ys, np.zeros(4)))], facecolor=C.LIGHT,
                        edgecolor=C.INK, linewidth=2.0, alpha=0.82)
ax.add_collection3d(proj)
for xi, yi, zi in zip(xs, ys, zs):
    ax.plot([xi, xi], [yi, yi], [0, zi], ls=":", color=C.GRAY, lw=1.2)

center = np.array([0.6, 0.5])
zc = 1.6 - 0.25 * (center[0]**2 + center[1]**2)
label3d(ax, r"$\Delta S$", (0.85, 0.75, 1.6 - 0.25 * (0.85**2 + 0.75**2)),
        offset=(6, 0), ha="left", va="center")
label3d(ax, r"$\Delta\sigma$", (0.85, 0.75, 0.0),
        offset=(6, 0), ha="left", va="center")

# 法向量 n（实线）与竖直向上的 z 轴方向（虚线）
nraw = np.array([0.5 * center[0], 0.5 * center[1], 1.0])
nvec = nraw / np.linalg.norm(nraw) * 0.8
ax.quiver(center[0], center[1], zc, *nvec, color=C.INK, lw=1.8, arrow_length_ratio=0.16)
label3d(ax, r"$\boldsymbol{n}$", tuple(np.r_[center, zc] + nvec), offset=(5, -2), ha="left")
ax.quiver(center[0], center[1], zc, 0, 0, 0.8, color=C.INK, lw=1.3,
          linestyle="--", arrow_length_ratio=0.15)
label3d(ax, r"$z$ 轴方向", (center[0], center[1], zc + 0.8),
        offset=(-8, 2), ha="right", va="baseline")

# n 与 z 方向的夹角 γ：圆弧放大，γ 写在弧的外侧
k = np.array([0.0, 0.0, 1.0])
u = nvec / np.linalg.norm(nvec)
gamma = np.arccos(np.clip(np.dot(u, k), -1, 1))
e1 = u - np.dot(u, k) * k
e1 /= np.linalg.norm(e1)
t = np.linspace(0, gamma, 60)
arc = np.array([np.r_[center, zc] + 0.72 * (np.cos(tt) * k + np.sin(tt) * e1) for tt in t])
ax.plot(arc[:, 0], arc[:, 1], arc[:, 2], color=C.INK, lw=1.3)
arc_mid = np.r_[center, zc] + 0.72 * (np.cos(gamma / 2) * k + np.sin(gamma / 2) * e1)
label3d(ax, r"$\gamma$", tuple(arc_mid), offset=(3, 8), ha="center", va="baseline")

ax.set_axis_off()
save(fig, "C28-n1")

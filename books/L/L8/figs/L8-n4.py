import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, save
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

fig = plt.figure(figsize=(17 / 2.54, 8.5 / 2.54))
def setup(k, title):
    ax = fig.add_subplot(1, 2, k, projection="3d")
    ax.view_init(elev=20, azim=-55)
    ax.computed_zorder = False
    for a in (ax.xaxis, ax.yaxis, ax.zaxis):
        a.pane.set_facecolor((1, 1, 1, 0)); a.pane.set_edgecolor(C.LIGHT)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    ax.set_xlabel("$x$", labelpad=-12); ax.set_ylabel("$y$", labelpad=-12); ax.set_zlabel("$z$", labelpad=-12)
    ax.set_title(title, fontsize=10)
    return ax

a = setup(1, "输入空间 $\\mathbb{R}^3$")
a.set_xlim(-2.5, 2.5); a.set_ylim(-2.5, 2.5); a.set_zlim(-2.5, 2.5)
n = np.array([-2, 1, 0.0])
a.plot(*zip(-1.2 * n, 1.2 * n), color=C.INK, lw=2.2, ls=(0, (4, 2)), zorder=5)
a.scatter(*n, s=40, facecolors=C.PAPER, edgecolors=C.INK, linewidths=1.3, zorder=7)
a.scatter([0], [0], [0], color=C.INK, s=14, zorder=7)
a.text(*(n + np.array([0, 0, 0.5])), "$(-2,1,0)$", fontsize=9, zorder=10)
a.text2D(0.0, -0.06, "虚线：零空间（1 维），整条被送到原点", transform=a.transAxes, fontsize=9)

b = setup(2, "像：列空间（2 维）")
c1 = np.array([1, 2, 3.0]); c3 = np.array([1, 3, 4.0]); d = c3 - c1
corners = [s * c1 + t * d for s, t in [(-0.4, -1.6), (1.6, -1.6), (1.6, 1.6), (-0.4, 1.6)]]
b.add_collection3d(Poly3DCollection([corners], facecolor=C.LIGHT, alpha=0.6, edgecolor=C.GRAY, lw=0.6, zorder=0))
pts = np.array(corners)
b.set_xlim(pts[:, 0].min(), pts[:, 0].max()); b.set_ylim(pts[:, 1].min(), pts[:, 1].max()); b.set_zlim(pts[:, 2].min(), pts[:, 2].max())
for v, lab in [(c1, "$(1,2,3)$"), (c3, "$(1,3,4)$")]:
    b.quiver(0, 0, 0, *v, color=C.INK, lw=2.2, arrow_length_ratio=0.1, zorder=6)
b.text(*(c1 + np.array([0.2, -0.6, -0.4])), "$(1,2,3)$", fontsize=9, zorder=10)
b.text(*(c3 + np.array([0, 0, 0.3])), "$(1,3,4)$", fontsize=9, zorder=10)
b.scatter([0], [0], [0], color=C.INK, s=18, zorder=7)
b.text(0.1, 0, -0.9, "原点：$(-2,1,0)$ 到了这里", fontsize=9, zorder=10)
b.text2D(0.0, -0.06, "阴影：平面 $z=x+y$", transform=b.transAxes, fontsize=9)

fig.text(0.5, 0.55, "⑤ →", ha="center", fontsize=14)
fig.text(0.5, 0.0, "$\\dim N+\\dim C=1+2=3$", ha="center", fontsize=10)
save(fig, "L8-n4")

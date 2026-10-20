import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig3d, save
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

fig, ax = new_fig3d(12, 11, elev=14, azim=-60)
ax.computed_zorder = False
def plane(c, fc, ls):
    pts = [(x, y, x + y + c) for x, y in [(-1, -1), (1, -1), (1, 1), (-1, 1)]]
    ax.add_collection3d(Poly3DCollection([pts], facecolor=fc, alpha=0.45, edgecolor=C.INK, lw=0.9, linestyle=ls, zorder=0))
plane(0, C.LIGHT, "-")
plane(1, "#F2F2F2", (0, (4, 2)))
ax.set_xlim(-1, 1); ax.set_ylim(-1, 1); ax.set_zlim(-2, 3)
ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
ax.set_xlabel("$x$"); ax.set_ylabel("$y$"); ax.set_zlabel("$z$")
ax.quiver(0, 0, 0, 0, 0, 2, color=C.INK, lw=1.4, linestyle=(0, (4, 2)), arrow_length_ratio=0.1, zorder=4)
ax.quiver(0, 0, 0, 0, 0, 1, color=C.INK, lw=3.2, arrow_length_ratio=0.18, zorder=6)
ax.scatter([0], [0], [0], color=C.INK, s=18, zorder=7)
ax.scatter([0], [0], [1], color=C.INK, s=26, zorder=7)
ax.scatter([0], [0], [2], s=40, facecolors=C.PAPER, edgecolors=C.INK, linewidths=1.3, zorder=7)
ax.text(0.05, 0, -0.35, "原点 $O$", fontsize=9, zorder=10)
ax.text(0.08, 0, 1.0, "$(0,0,1)$ 在上面的平面上", fontsize=9, zorder=10)
ax.text(-0.08, 0, 2.05, "空心点 $(0,0,2)=2\\times(0,0,1)$：出界", fontsize=9, zorder=10, ha="right")
fig.text(0.03, 0.95, "实线边框：平面 $z=x+y$，过原点，是子空间", fontsize=10)
fig.text(0.03, 0.89, "虚线边框：平面 $z=x+y+1$，不过原点，不是子空间", fontsize=10)
save(fig, "L8-n3")

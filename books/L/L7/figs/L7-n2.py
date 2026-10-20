import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig3d, save
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

fig, ax = new_fig3d(13, 9, elev=18, azim=-78)
ax.computed_zorder = False
ax.set_xlim(0, 2.9); ax.set_ylim(0, 1.2); ax.set_zlim(0, 1.3)
ax.set_xticks([0, 1, 2]); ax.set_yticks([]); ax.set_zticks([0, 1])
ax.set_xlabel("$x$"); ax.set_ylabel("$y$"); ax.set_zlabel("$z$")
ax.set_box_aspect((2.9, 1.2, 1.3))
floor = [[(0, 0, 0), (2.9, 0, 0), (2.9, 1.2, 0), (0, 1.2, 0)]]
ax.add_collection3d(Poly3DCollection(floor, facecolor=C.LIGHT, alpha=0.5, edgecolor=C.GRAY, lw=0.6, zorder=0))

def arr(p, q, ls="-", lw=2.4, color=C.INK, z=5):
    ax.quiver(p[0], p[1], p[2], q[0]-p[0], q[1]-p[1], q[2]-p[2], color=color, lw=lw,
              linestyle=ls, arrow_length_ratio=0.1, zorder=z)

arr((0, 0, 0), (2, 0, 1))
ax.text(2.02, 0, 1.06, "箭头 $(2,0,1)$", fontsize=10, zorder=10)
ax.plot([2, 2], [0, 0], [1, 0], color=C.GRAY, lw=1.2, ls=":", zorder=4)
ax.text(2.06, 0, 0.45, "点线：落到地面", fontsize=8.5, color=C.INK, zorder=10)
arr((0, 0, 0), (2, 0, 0), ls=(0, (4, 2)), lw=1.6, color=C.INK, z=4)
arr((0, 0, 0), (1, 0, 0), lw=3.0, z=6)
ax.text(0.55, 0, 0.12, "箭头 $(1,0,0)$", fontsize=10, zorder=10)
ax.text(2.08, 0, -0.16, "虚线：影子 $(2,0)$", fontsize=9, zorder=10)
fig.text(0.05, 0.93, "箭头 $(1,0,0)$、$(2,0,1)$：不共线，线性无关", fontsize=10)
fig.text(0.05, 0.87, "影子 $(1,0)$、$(2,0)$：在同一条直线上，线性相关", fontsize=10)
fig.text(0.05, 0.81, "浅灰阴影：地面（$xy$ 平面）", fontsize=10)
save(fig, "L7-n2")

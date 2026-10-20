import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig3d, save
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

fig, ax = new_fig3d(12, 10, elev=24, azim=-115)
ax.computed_zorder = False
a1 = np.array([1, 0, 1.0]); a2 = np.array([0, 1, 1.0]); a3 = a1 + a2
corners = [s * a1 + t * a2 for s, t in [(-0.3, -0.3), (1.5, -0.3), (1.5, 1.5), (-0.3, 1.5)]]
ax.add_collection3d(Poly3DCollection([corners], facecolor=C.LIGHT, alpha=0.6, edgecolor=C.GRAY, lw=0.6, zorder=0))
L = 1.6
for v, n in [((L, 0, 0), "$x$"), ((0, L, 0), "$y$"), ((0, 0, 2.4), "$z$")]:
    ax.plot([0, v[0]], [0, v[1]], [0, v[2]], color=C.GRAY, lw=0.9, zorder=1)
    ax.text(*v, n, fontsize=10, zorder=10)
ax.set_xlim(-0.4, 1.6); ax.set_ylim(-0.4, 1.6); ax.set_zlim(-0.4, 2.4)
ax.set_axis_off()

def arr(p, v, ls="-", lw=2.4, z=5):
    ax.quiver(*p, *v, color=C.INK, lw=lw, linestyle=ls, arrow_length_ratio=0.12, zorder=z)

arr((0, 0, 0), a1)                      # 沿 alpha1
arr(a1, a2)                             # 再沿 alpha2
arr(a3, -a3, ls=(0, (4, 2)), lw=1.8)    # 逆着 alpha3 回到原点
ax.scatter([0], [0], [0], color=C.INK, s=16, zorder=7)
ax.text(*(a1 / 2 + np.array([0.1, -0.1, -0.75])), r"$\boldsymbol{\alpha}_1=(1,0,1)$", fontsize=10, zorder=10)
ax.text(*(a1 + a2 / 2 + np.array([0.08, 0.0, -0.1])), r"$\boldsymbol{\alpha}_2=(0,1,1)$", fontsize=10, zorder=10)
ax.text(*(a3 / 2 + np.array([-0.25, 0.2, 0.25])), r"虚线：$-\boldsymbol{\alpha}_3$", fontsize=10, zorder=10)
ax.text(*(a3 + np.array([0.0, 0.0, 0.12])), r"$\boldsymbol{\alpha}_3=(1,1,2)$ 的终点", fontsize=9, zorder=10)
ax.text(0.05, -0.05, -0.28, "原点", fontsize=9, zorder=10)
fig.text(0.04, 0.95, "浅灰阴影：平面 $z=x+y$，三个向量都躺在里面", fontsize=10)
fig.text(0.04, 0.89, r"走 $\boldsymbol{\alpha}_1$，再走 $\boldsymbol{\alpha}_2$，再逆着 $\boldsymbol{\alpha}_3$ 走，回到原点", fontsize=10)
save(fig, "L7-n3")

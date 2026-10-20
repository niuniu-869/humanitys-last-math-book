import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, save
from matplotlib.patches import Polygon, Arc

# 正对平面 x1+x2+x3=0 看（视线沿法向量 (1,1,1)），平面内用规范正交基
# ea = (1,-1,0)/sqrt2 -> 水平向右，eb = (1,1,-2)/sqrt6 -> 竖直向上，角度和长度都是真实的。
ea = np.array([1, -1, 0]) / np.sqrt(2); eb = np.array([1, 1, -2]) / np.sqrt(6)
xy = lambda v: np.array([v @ ea, v @ eb])
a1 = np.array([1, -1, 0.0]); a2 = np.array([1, 0, -1.0]); b2 = a2 - (a2 @ a1) / (a1 @ a1) * a1
P1, P2, B2, PR = xy(a1), xy(a2), xy(b2), xy(0.5 * a1)
assert abs(b2 @ a1) < 1e-12 and abs(b2.sum()) < 1e-12

fig, ax = new_fig(12, 8.6)
ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(Polygon([(-1.0, -0.75), (2.55, -0.75), (2.55, 2.0), (-1.0, 2.0)], closed=True,
                     facecolor=C.LIGHT, edgecolor=C.GRAY, lw=0.9))
ax.text(-0.92, 1.92, "阴影：平面 $x_1+x_2+x_3=0$\n（特征值 $-1$ 的特征空间，正对着看）", fontsize=8.5, va="top")

def arr(p, lw, ls="-"):
    ax.annotate("", xy=p, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=C.INK, lw=lw, ls=ls, mutation_scale=12, shrinkA=0, shrinkB=0))

arr(P1, 1.6); ax.text(P1[0] - 0.35, P1[1] + 0.05, "$\\boldsymbol{\\alpha}_1=(1,-1,0)^{\\mathrm{T}}$", fontsize=9, va="bottom")
arr(P2, 1.6); ax.text(P2[0] + 0.07, P2[1] + 0.02, "$\\boldsymbol{\\alpha}_2=(1,0,-1)^{\\mathrm{T}}$", fontsize=9, va="bottom")
arr(B2, 1.6, "--"); ax.text(B2[0] - 0.08, B2[1] + 0.04, "$\\boldsymbol{\\beta}_2=\\frac{1}{2}(1,1,-2)^{\\mathrm{T}}$（虚线）", fontsize=9, va="bottom", ha="center")
# 投影点与点线
ax.plot([PR[0], P2[0]], [PR[1], P2[1]], ls=":", color=C.INK, lw=1.4)
ax.scatter(*PR, s=36, facecolor="white", edgecolor=C.INK, zorder=6, lw=1.1)
ax.text(PR[0] + 0.05, PR[1] - 0.09, "$\\frac{1}{2}\\boldsymbol{\\alpha}_1$：$\\boldsymbol{\\alpha}_2$ 在 $\\boldsymbol{\\alpha}_1$ 上的投影", fontsize=8.5, va="top")
ax.text(PR[0] + 0.05, 0.62, "点线：减去投影", fontsize=8.5, va="center")
# 60° 弧与直角标记
ax.add_patch(Arc((0, 0), 0.5, 0.5, theta1=0, theta2=60, color=C.INK, lw=0.9))
ax.text(0.3, 0.13, "$60^\\circ$", fontsize=9)
s = 0.1
ax.plot([0, s, s], [s, s, 0], color=C.INK, lw=0.8)
# 法向量垂直于纸面：⊙
ax.scatter(0, 0, s=110, facecolor="white", edgecolor=C.INK, lw=1.2, zorder=7)
ax.scatter(0, 0, s=10, color=C.INK, zorder=8)
ax.text(-0.95, -0.25, "⊙ 原点处：法向量 $(1,1,1)^{\\mathrm{T}}$\n（特征值 2）垂直于纸面，指向读者", fontsize=8.5, va="top")
ax.set_xlim(-1.05, 2.6); ax.set_ylim(-0.8, 2.05)
save(fig, "L13-n4")

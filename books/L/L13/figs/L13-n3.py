import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, save
from matplotlib.patches import Polygon

# 斜投影示意：平面 W（x1=x3）画成「地板」，q1 竖直向上。
# 地板坐标 (s,t) 表示 s*f1 + t*f2，f1=(1,0,1)/sqrt2，f2=(0,1,0)。
F1 = np.array([1.0, 0.0]); F2 = np.array([0.55, 0.42]); Q = np.array([0.0, 1.0])
P = lambda s, t, h=0.0: s * F1 + t * F2 + h * Q
r2 = np.sqrt(2.0)
A = np.array([[2, 1, 0], [1, 2, 1], [0, 1, 2]], float)
f1 = np.array([1, 0, 1]) / r2; f2 = np.array([0, 1, 0.0])
def coords(v):  # v 在 W 里，返回 (s,t)
    return v @ f1, v @ f2
u = np.array([0, 1, 0.0]); up = np.array([1, 0, 1.0])
pts = {"u": coords(u), "Au": coords(A @ u), "up": coords(up), "Aup": coords(A @ up)}
assert np.allclose((A @ u)[0], (A @ u)[2]) and np.allclose((A @ up)[0], (A @ up)[2])

fig, ax = new_fig(13, 8.2)
ax.set_aspect("equal"); ax.axis("off")
corners = [P(-0.9, -0.6), P(3.5, -0.6), P(3.5, 2.7), P(-0.9, 2.7)]
ax.add_patch(Polygon(corners, closed=True, facecolor=C.LIGHT, edgecolor=C.GRAY, lw=0.9))
ax.text(-1.3, -0.45, "阴影：平面 $W$（$x_1=x_3$），与 $\\boldsymbol{q}_1$ 垂直", fontsize=9, color=C.INK, va="center", ha="left")

# q1 竖直向上，原点处直角标记
O = P(0, 0)
ax.annotate("", xy=P(0, 0, 1.7), xytext=O, arrowprops=dict(arrowstyle="-|>", color=C.INK, lw=2.4, mutation_scale=13, shrinkA=0, shrinkB=0))
ax.text(*(P(0, 0, 1.72) + np.array([0.08, 0.0])), "$\\boldsymbol{q}_1=\\frac{1}{\\sqrt{2}}(-1,0,1)^{\\mathrm{T}}$（特征值 2）", fontsize=9, va="bottom")
s = 0.16
ax.plot(*np.array([P(0, 0, s), P(s, 0, s), P(s, 0, 0)]).T, color=C.INK, lw=0.8)

def vec(st, lw, text, off, marker):
    tip = P(*st)
    ax.annotate("", xy=tip, xytext=O, arrowprops=dict(arrowstyle="-|>", color=C.INK, lw=lw, mutation_scale=11, shrinkA=0, shrinkB=3))
    if marker == "o":
        ax.scatter(*tip, s=34, facecolor="white", edgecolor=C.INK, zorder=6, lw=1.1)
    else:
        ax.scatter(*tip, s=34, marker="s", color=C.INK, zorder=6)
    ax.text(*(tip + np.array(off)), text, fontsize=9, va="center")

vec(pts["u"], 1.0, "$\\boldsymbol{u}=(0,1,0)^{\\mathrm{T}}$", (-0.1, 0.24), "o")
vec(pts["Au"], 2.0, "$A\\boldsymbol{u}=(1,2,1)^{\\mathrm{T}}$", (-0.55, 0.2), "s")
vec(pts["up"], 1.0, "$\\boldsymbol{u}'=(1,0,1)^{\\mathrm{T}}$", (-0.25, -0.2), "o")
vec(pts["Aup"], 2.0, "$A\\boldsymbol{u}'=(2,2,2)^{\\mathrm{T}}$", (0.1, -0.05), "s")
ax.text(-1.3, -0.66, "空心圆：$W$ 里的向量；实心方块：它的像，仍在 $W$ 里", fontsize=8.5, color=C.INK, va="center")
ax.set_xlim(-1.4, 5.6); ax.set_ylim(-0.78, 2.05)
save(fig, "L13-n3")

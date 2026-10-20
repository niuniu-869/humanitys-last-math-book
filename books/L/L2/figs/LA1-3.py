import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import C, arrow, dot, label, new_fig, np, plt, save

from matplotlib.offsetbox import AnnotationBbox, HPacker, TextArea

fig, ax = new_fig(16, 7.2)
ax.axis("off")
ax.set_aspect("equal")
ax.set_xlim(-0.9, 14.1)
ax.set_ylim(-1.6, 4.9)

O = np.array([0.0, 0.0])
A = np.array([2.7, 3.2])      # 向量 a 的终点
B = np.array([5.2, 0.0])      # 向量 b 的终点

# 三条边：a、b、a-b
arrow(ax, O, A, C.BLUE, r"$\mathbf{a}$", offset=(3, 6))
arrow(ax, O, B, C.RED, r"$\mathbf{b}$", offset=(2, -15))
ax.annotate("", xy=tuple(A), xytext=tuple(B),
            arrowprops=dict(arrowstyle="-|>", color=C.TEAL, lw=1.8, linestyle="--",
                            shrinkA=0, shrinkB=0, mutation_scale=11), zorder=4)
label(ax, r"$\mathbf{a}-\mathbf{b}$", (0.55 * (A + B)), offset=(8, 6), color=C.TEAL)

# 原点处的夹角
th = np.arctan2(A[1], A[0])
t = np.linspace(0.0, th, 60)
ax.plot(1.05 * np.cos(t), 1.05 * np.sin(t), color=C.INK, lw=1.0, zorder=5)
label(ax, r"$\theta$", (1.32 * np.cos(th / 2), 1.32 * np.sin(th / 2)))
dot(ax, O, r"$O$", offset=(-13, -12))


def equation(parts, xy):
    """把一条带颜色的式子拼成一行，左端对齐到 xy。"""
    box = HPacker(children=[TextArea(s, textprops=dict(color=c, fontsize=10.5)) for s, c in parts],
                  align="center", pad=0, sep=0)
    ax.add_artist(AnnotationBbox(box, xy, frameon=False, pad=0,
                                 box_alignment=(0, 0.5), xycoords="data"))


INK = C.INK
equation([(r"$\Vert\mathbf{a}-\mathbf{b}\Vert^2$", C.TEAL), (r"$\,=\,$", INK),
          (r"$\Vert\mathbf{a}\Vert^2$", C.BLUE), (r"$+\,$", INK),
          (r"$\Vert\mathbf{b}\Vert^2$", C.RED), (r"$-\,2\,$", INK),
          (r"$\Vert\mathbf{a}\Vert\,\Vert\mathbf{b}\Vert\cos\theta$", C.AMBER)], (6.7, 3.45))
equation([(r"$(\mathbf{a}-\mathbf{b})\cdot(\mathbf{a}-\mathbf{b})$", C.TEAL), (r"$\,=\,$", INK),
          (r"$\mathbf{a}\cdot\mathbf{a}$", C.BLUE), (r"$-\,2\,$", INK),
          (r"$\mathbf{a}\cdot\mathbf{b}$", C.AMBER), (r"$+\,$", INK),
          (r"$\mathbf{b}\cdot\mathbf{b}$", C.RED)], (6.7, 2.05))
equation([("消去 ", INK), (r"$\Vert\mathbf{a}\Vert^2+\Vert\mathbf{b}\Vert^2$", INK), (" 后：", INK),
          (r"$\mathbf{a}\cdot\mathbf{b}=\Vert\mathbf{a}\Vert\,\Vert\mathbf{b}\Vert\cos\theta$", C.AMBER)], (6.7, 0.65))

save(fig, "LA1-3")

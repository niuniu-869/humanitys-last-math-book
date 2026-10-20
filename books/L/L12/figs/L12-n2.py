import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

# 作者重排版：放大到稳态附近，每个点只配一个标签，避免标注拥挤
pi = np.array([0.6, 0.4])
points = [np.array([1.0, 0.0]), np.array([0.8, 0.2]), np.array([0.7, 0.3]), np.array([0.65, 0.35])]
coeff = ["0.4", "0.2", "0.1", "0.05"]

fig, ax = new_fig(11.0, 9.0)
ax.set_aspect("equal", adjustable="box")
ax.set_xlim(0.42, 1.14)
ax.set_ylim(-0.06, 0.62)
ax.set_xticks(np.arange(0.5, 1.11, 0.1))
ax.set_yticks(np.arange(0.0, 0.61, 0.1))
ax.grid(True, color=C.LIGHT, lw=0.7, alpha=0.75, zorder=0)
ax.set_xlabel("$x_1$（活跃占比）")
ax.set_ylabel("$x_2$（沉默占比）")

# 总占比为 1 的直线（实线）
ax.plot([0.42, 1.06], [0.58, -0.06], color=C.INK, lw=1.6, zorder=2)
label(ax, r"$x_1+x_2=1$", (0.47, 0.53), offset=(8, 4), color=C.INK)

# 特征值 1 的方向：过原点与稳态的虚线，方向 (3,2)
xs = np.array([0.42, 0.9])
ax.plot(xs, 2 * xs / 3, color=C.GRAY, lw=1.2, ls="--", zorder=1)
label(ax, "特征值 1 的方向 $(3,2)$", (0.86, 0.573), offset=(-4, 6), color=C.INK, ha="right")

# 轨迹点：标签放在直线右上方，冒号后是沿 (1,-1) 的偏离系数
offsets = [(6, 6), (7, 7), (7, 7), (7, 9)]
for i, (p, c) in enumerate(zip(points, coeff)):
    dot(ax, p, color=C.INK, size=30)
    label(ax, rf"$\boldsymbol{{x}}_{i}$：{c}", p, offset=offsets[i], color=C.INK)
for p, q in zip(points[:-1], points[1:]):
    arrow(ax, p + 0.2 * (q - p), 0.6 * (q - p), color=C.INK, lw=1.1, offset=(0, 0))

# 稳态：空心大圆
ax.scatter(*pi, s=110, facecolors=C.PAPER, edgecolors=C.INK, linewidths=1.8, zorder=5)
label(ax, "稳态 $(0.6,0.4)$", pi, offset=(-12, 4), color=C.INK, ha="right")

# 说明：偏离沿直线方向 (1,-1)，即特征值 0.5 的方向
label(ax, "偏离都沿 $(1,-1)$，\n即特征值 0.5 的方向；\n冒号后为偏离系数 $0.4\\times0.5^n$", (0.44, 0.03),
      offset=(0, 0), color=C.INK, ha="left", va="bottom")

save(fig, "L12-n2")

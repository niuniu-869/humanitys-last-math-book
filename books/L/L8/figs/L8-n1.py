import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(13.5, 10.5)
ax.set_aspect("equal", adjustable="box")
ax.set_xlim(-1, 7)
ax.set_ylim(-2, 5)
ax.set_xticks(np.arange(-1, 8, 1))
ax.set_yticks(np.arange(-2, 6, 1))
ax.set_xlabel("$x$")
ax.set_ylabel("$y$")

# 标准方格纸：很淡的点线
for x in np.arange(-1, 8, 1):
    ax.plot([x, x], [-2, 5], color=C.LIGHT, lw=0.7, ls=":", zorder=0)
for y in np.arange(-2, 6, 1):
    ax.plot([-1, 7], [y, y], color=C.LIGHT, lw=0.7, ls=":", zorder=0)

# 坐标轴
ax.axhline(0, color=C.GRAY, lw=0.9, zorder=1)
ax.axvline(0, color=C.GRAY, lw=0.9, zorder=1)

# 斜方格纸：x-y=2k 与 x+y=2k
xs = np.array([-1.0, 7.0])
for k in range(-3, 6):
    c = 2.0 * k
    # x-y=c -> y=x-c
    ax.plot(xs, xs - c, color=C.GRAY, lw=1.0, ls=(0, (5, 4)), zorder=1)
    # x+y=c -> y=c-x
    ax.plot(xs, c - xs, color=C.GRAY, lw=1.0, ls=(0, (5, 4)), zorder=1)

# 基向量与折线：4 alpha_1 + alpha_2 = (5,3)
arrow(ax, (0, 0), (1, 1), color=C.INK, lw=2.6, offset=(7, 7))
label(ax, r"$\boldsymbol{\alpha}_1$", (0.72, 0.72), offset=(5, 5), color=C.INK)
ax.annotate("", xy=(1, -1), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=C.INK, lw=2.4, linestyle=(0, (3, 1.5)), shrinkA=0, shrinkB=0, mutation_scale=11), zorder=5)  # α2：短划线
label(ax, r"$\boldsymbol{\alpha}_2$", (0.72, -0.72), offset=(5, -2), color=C.INK)

arrow(ax, (0, 0), (4, 4), color=C.INK, lw=2.8, offset=(4, 5))
label(ax, r"$4\boldsymbol{\alpha}_1$", (4, 4), offset=(-34, 7), color=C.INK)
ax.annotate("", xy=(5, 3), xytext=(4, 4), arrowprops=dict(arrowstyle="-|>", color=C.INK, lw=2.6, linestyle=(0, (3, 1.5)), shrinkA=0, shrinkB=0, mutation_scale=11), zorder=5)  # +α2：短划线
label(ax, r"$+\boldsymbol{\alpha}_2$", (4.55, 3.45), offset=(7, 5), color=C.INK)

dot(ax, (4, 4), color=C.INK, size=24)
dot(ax, (5, 3), text="$(5,3)$", color=C.INK, offset=(7, 7), size=34)

# 旁注
label(ax, "标准坐标 $(5,3)$", (0.15, -1.55), offset=(0, 0), color=C.INK, fontsize=10)
label(ax, "新坐标 $(4,1)$", (0.15, -1.9), offset=(0, 0), color=C.INK, fontsize=10)

save(fig, "L8-n1")

import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label


fig, ax = new_fig(13.5, 7.8)
ax.set_aspect("equal", adjustable="box")
ax.set_xlim(-1.0, 7.75)
ax.set_ylim(-0.85, 3.05)
ax.set_xticks(np.arange(0, 8, 1))
ax.set_yticks([0, 2])
ax.grid(True, color=C.LIGHT, lw=0.65, alpha=0.6, zorder=0)
ax.axhline(0, color=C.GRAY, lw=0.9, zorder=1)
ax.axvline(0, color=C.GRAY, lw=0.9, zorder=1)
ax.set_xlabel("$x$")
ax.set_ylabel("$y$")

O = np.array([0.0, 0.0])
A = np.array([3.0, 0.0])
B = np.array([4.0, 2.0])
Cpt = np.array([1.0, 2.0])
D = np.array([7.0, 2.0])

# 原平行四边形：实线、浅灰填充。
orig = np.array([O, A, B, Cpt, O])
ax.fill(orig[:, 0], orig[:, 1], color=C.LIGHT, alpha=0.70, zorder=2)
ax.plot(orig[:, 0], orig[:, 1], color=C.INK, lw=2.0, zorder=4)

# 新平行四边形：虚线、空白填充。
new = np.array([O, A, D, B, O])
ax.plot(new[:, 0], new[:, 1], color=C.RED, lw=1.8, ls="--", zorder=4)

# 向量箭头。
arrow(ax, O, A - O, color=C.BLUE, lw=2.0, offset=(3, -17))
label(ax, r"$\mathbf{r}_1$", (2.2, 0.08), offset=(0, 0), color=C.BLUE, ha="center", va="bottom")
arrow(ax, O, Cpt - O, color=C.TEAL, lw=2.0, offset=(-28, 4))
label(ax, r"$\mathbf{r}_2$", (0.47, 1.02), offset=(-2, 0), color=C.TEAL, ha="right")
ax.annotate("", xy=tuple(B), xytext=tuple(O),
            arrowprops=dict(arrowstyle="-|>", color=C.RED, lw=1.8, linestyle="--",
                            shrinkA=0, shrinkB=0, mutation_scale=11), zorder=5)
label(ax, r"$\mathbf{r}_2+\mathbf{r}_1$", (2.35, 1.5), offset=(0, 0), color=C.RED, ha="right", va="bottom")
dot(ax, O, "$O$", color=C.INK, offset=(-13, -15), size=22)

# 同一条水平上边线与滑动说明。
ax.plot([0, 7.5], [2, 2], color=C.GRAY, lw=1.1, ls=":", zorder=1)
label(ax, "上边沿这条线滑动", (5.15, 2.0), offset=(0, 14), color=C.GRAY, ha="center")

# 高与底的尺寸线。
ax.annotate("", xy=(-0.34, 2), xytext=(-0.34, 0),
            arrowprops=dict(arrowstyle="<->", color=C.GRAY, lw=1.0, shrinkA=0, shrinkB=0))
label(ax, "高 2", (-0.34, 1.0), offset=(-8, 0), color=C.INK, ha="right", va="center")
ax.annotate("", xy=(3, -0.28), xytext=(0, -0.28),
            arrowprops=dict(arrowstyle="<->", color=C.GRAY, lw=1.0, shrinkA=0, shrinkB=0))
label(ax, "底 3", (1.5, -0.28), offset=(0, -6), color=C.INK, ha="center", va="top")

save(fig, "L6-n2")

import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Circle, Rectangle, Polygon


fig, ax = new_fig(16.5, 8.8)
ax.set_xlim(-0.3, 11.8)
ax.set_ylim(-0.4, 7.2)
ax.set_aspect("equal")
ax.axis("off")

# The universe, Q, and the smaller P contained in Q.
ax.add_patch(Rectangle((0, 0), 11.4, 6.9, fill=False, edgecolor=C.INK, linewidth=1.5))
label(ax, "全体对象", (0.25, 6.45), offset=(0, 0), fontsize=10)
ax.add_patch(Circle((4.05, 3.35), 2.42, fill=False, edgecolor=C.INK, linewidth=1.8))
label(ax, r"$Q$：$q$ 为真", (4.05, 6.0), ha="center", fontsize=10)
ax.add_patch(Circle((3.10, 3.35), 1.30, facecolor=C.LIGHT, edgecolor=C.INK, linewidth=1.8, alpha=0.55))
label(ax, r"$P$：$p$ 为真", (3.10, 3.95), ha="center", fontsize=10)

# The three realized truth-table rows.
dot(ax, (3.10, 3.30), size=28)
label(ax, r"$p=1,\ q=1$", (3.10, 2.80), ha="center", fontsize=10)
ax.scatter(4.95, 2.40, s=46, facecolors=C.PAPER, edgecolors=C.INK, linewidths=1.5, zorder=5)
label(ax, r"$p=0,\ q=1$", (4.95, 1.92), ha="center", fontsize=10)
ax.scatter(8.40, 1.80, s=42, marker="s", color=C.INK, zorder=5)
label(ax, r"$p=0,\ q=0$", (8.40, 1.28), ha="center", fontsize=10)

# Empty protruding part: dashed outline and a cross make the missing p=1,q=0 row explicit.
empty = np.array([[4.30, 3.85], [6.85, 4.48], [7.45, 4.08],
                  [7.45, 3.30], [6.85, 3.02], [4.38, 3.12]])
ax.add_patch(Polygon(empty, closed=True, fill=False, edgecolor=C.GRAY, linewidth=1.3, linestyle="--"))
label(ax, r"$\times$", (6.95, 3.70), ha="center", va="center", fontsize=24)
label(ax, "假想凸出部分", (8.0, 5.05), fontsize=9)
label(ax, r"$p=1,\ q=0$", (8.0, 4.45), fontsize=10)
label(ax, "这一块是空的", (8.0, 3.92), fontsize=9.5)
arrow(ax, (8.05, 3.62), (-0.50, 0), color=C.INK, lw=1)

# Short explanatory callouts.
label(ax, "小圈：充分条件", (1.85, 0.35), ha="center", fontsize=9)
arrow(ax, (1.85, 0.85), (0.45, 1.40), color=C.INK, lw=1)
label(ax, "大圈：必要条件", (5.40, 0.35), ha="center", fontsize=9)
arrow(ax, (5.40, 0.85), (-0.12, 0.38), color=C.INK, lw=1)

save(fig, "Z1-n1")

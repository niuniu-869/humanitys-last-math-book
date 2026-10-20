import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label


fig, ax = new_fig(9, 9)
ax.set_aspect("equal", adjustable="box")
ax.set_xlim(-3.25, 3.25)
ax.set_ylim(-3.25, 3.25)

arrow(ax, (-3, 0), (6, 0), color=C.INK, lw=1.4)
arrow(ax, (0, -3), (0, 6), color=C.INK, lw=1.4)

e1 = np.array([1.0, 1.0]) / np.sqrt(2)
e2 = np.array([1.0, -1.0]) / np.sqrt(2)
for vec in (e1, e2):
    arrow(ax, tuple(-2.85 * vec), tuple(5.7 * vec), color=C.INK, lw=1.0)
label(ax, "W1 方向\n沿 (1,1) 的坐标", (2.12, 2.12), ha="left", va="bottom")
label(ax, "W2 方向\n沿 (1,-1) 的坐标", (2.12, -1.9), ha="left", va="bottom")

theta = np.linspace(0, 2 * np.pi, 400)
ax.plot(np.cos(theta), np.sin(theta), color=C.GRAY, ls=":", lw=1.0)
label(ax, "虚线圆：半径 1", (-3.1, 0.5), ha="left", va="center")

P = np.array([2.0, 0.5])
p1 = np.dot(P, e1) * e1
p2 = np.dot(P, e2) * e2
dot(ax, P, "(Z1, Z2)", offset=(6, 5), size=28)
ax.plot([P[0], p1[0]], [P[1], p1[1]], color=C.INK, ls="--", lw=1.0)
ax.plot([P[0], p2[0]], [P[1], p2[1]], color=C.INK, ls="--", lw=1.0)
ax.scatter([p1[0], p2[0]], [p1[1], p2[1]], s=22, color=C.PAPER, edgecolors=C.INK, zorder=5)
label(ax, "W1", p1, offset=(-3, 6), ha="right", va="bottom")
label(ax, "W2", p2, offset=(-3, -12), ha="right", va="top")
label(ax, r"W1≈1.77", (-3.0, 2.75), ha="left", va="center")
label(ax, r"$\bar Z=W_1/\sqrt{2}\approx1.25$", (-3.0, 2.35), ha="left", va="center")
label(ax, r"W2≈1.06", (1.2, -2.45), ha="left", va="center")
label(ax, r"$(Z_1-\bar Z)^2$", (-3.0, -2.66), ha="left", va="center")
label(ax, r"$+(Z_2-\bar Z)^2=W_2^2$", (-3.0, -2.98), ha="left", va="center")

ax.set_xlabel("Z1")
ax.set_ylabel("Z2")
ax.set_xticks([-3, -2, -1, 0, 1, 2, 3])
ax.set_yticks([-3, -2, -1, 0, 1, 2, 3])
save(fig, "P10-n3")

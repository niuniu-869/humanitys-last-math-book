import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Circle, Rectangle

fig, axes = new_fig(15.5, 6.2, ncols=2)
ax = axes[0]
x = np.linspace(0, 3, 500); y = 2/3*x**1.5
ax.plot(x, y, color=C.INK, lw=1.7)
xc = 1.5; yc = 2/3*xc**1.5
ax.add_patch(Circle((xc, yc), 0.3, fill=False, edgecolor=C.INK, ls=":", lw=1.3))
dot(ax, (xc, yc), size=22)
label(ax, "放大", (xc+0.28, yc+0.23), offset=(4, 3))
ax.set(xlim=(-0.15, 3.2), ylim=(-0.15, 3.7), aspect="equal"); ax.set_xticks([]); ax.set_yticks([])

ax = axes[1]
P = np.array([0.55, 0.65]); Q = np.array([2.15, 2.60])
ax.plot([P[0], Q[0]], [P[1], Q[1]], color=C.INK, lw=1.8)
ax.plot([P[0], Q[0]], [P[1], P[1]], color=C.INK, ls="--", lw=1.1)
ax.plot([Q[0], Q[0]], [P[1], Q[1]], color=C.INK, ls="--", lw=1.1)
ax.add_patch(Rectangle((Q[0]-0.12, P[1]), 0.12, 0.12, facecolor=C.PAPER, edgecolor=C.INK, lw=0.9))
label(ax, r"$\mathrm{d}x$", ((P[0]+Q[0])/2, P[1]), offset=(0, -18), ha="center")
label(ax, r"$\mathrm{d}y$", (Q[0], (P[1]+Q[1])/2), offset=(7, 0), va="center")
label(ax, r"$\mathrm{d}s$", ((P[0]+Q[0])/2, (P[1]+Q[1])/2), offset=(5, 4))
ax.set(xlim=(0.2, 2.65), ylim=(0.25, 3.05), aspect="equal"); ax.set_xticks([]); ax.set_yticks([])
save(fig, "C13-n5")

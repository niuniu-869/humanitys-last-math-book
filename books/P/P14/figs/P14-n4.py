import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(10.8, 7.0)

x = np.linspace(0.08, 3.0, 800)
ax.plot(x, np.log(x), color=C.BLUE, lw=2.0, label="$y=\\ln x$")
ax.plot(x, x - 1, color=C.RED, lw=1.8, ls="--", label="$y=x-1$")

dot(ax, (1, 0), None, color=C.INK, size=34)
ax.scatter([1], [0], s=34, facecolors=C.PAPER, edgecolors=C.INK, linewidths=1.3, zorder=6)

x0 = 0.5
y_curve = np.log(x0)
y_tangent = x0 - 1
ax.plot([x0, x0], [y_curve, y_tangent], color=C.INK, lw=2.2, ls="-")
label(ax, "间隔 $(x-1)-\\ln x\\geq0$", (0.5, -0.6), offset=(8, -14), color=C.INK, ha="left")
label(ax, "相切", (1, 0), offset=(8, -22), color=C.INK)

ax.set_xlim(0.08, 3.02)
ax.set_ylim(-2.5, 2.0)
ax.set_xlabel("$x$")
ax.set_ylabel("$y$")
ax.set_xticks([0.5, 1, 2, 3])
ax.set_yticks([-2, -1, 0, 1, 2])
ax.legend(loc="upper left", fontsize=8.5, handlelength=2.0)
save(fig, "P14-n4")

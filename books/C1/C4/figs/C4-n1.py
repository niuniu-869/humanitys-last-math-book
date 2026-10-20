import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(12, 8)
xlim = (-0.5, 2.5)
ylim = (-0.5, 6.8)
x = np.linspace(xlim[0], xlim[1], 900)
ax.plot(x, x**2, color=C.INK, lw=2.0, ls="-")

P = (1.0, 1.0)
dot(ax, P, color=C.INK, size=30)
label(ax, "P(1,1)", P, offset=(6, -14))

for h, off in [
    (1.0, (-30, 4)),
    (0.5, (-30, 6)),
    (0.25, (-34, 8)),
]:
    q = (1 + h, (1 + h)**2)
    slope = (q[1] - P[1]) / (q[0] - P[0])
    assert np.isclose(slope, 2 + h)
    ax.scatter(*q, s=34, facecolors=C.PAPER, edgecolors=C.INK, linewidths=1.2, zorder=5)
    label(ax, rf"$h={h:g}$", q, offset=off, ha="right")
    xx = np.array(xlim)
    yy = P[1] + slope * (xx - P[0])
    ax.plot(xx, yy, color=C.GRAY, lw=1.0, ls=":", zorder=1)
    label(ax, f"斜率 {slope:g}", (2.5, 1 + 1.5 * slope),
          offset=(-3, {3.0: 8, 2.5: 0, 2.25: -9}[slope]), ha="right", fontsize=8)

xt = np.array(xlim)
ax.plot(xt, 2 * xt - 1, color=C.INK, lw=1.1, ls="-")
label(ax, "切线，斜率 2", (1.83, 2.2), offset=(0, 0), fontsize=9)
ax.set_xlim(*xlim); ax.set_ylim(*ylim)
ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
ax.set_xticks([-0.5, 0, 0.5, 1, 1.5, 2, 2.5])
ax.set_yticks([0, 1, 2, 3, 4, 5, 6])
save(fig, "C4-n1")

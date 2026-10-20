import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Polygon

fig, ax = new_fig(10.5, 7.2)
x = np.linspace(0, 1.2, 500)
y = x**2
ax.plot(x, y, color=C.INK, lw=1.8)
ax.axhline(0, color=C.INK, lw=0.9)
ax.axvline(0, color=C.INK, lw=0.9)

x0, x1 = 0.6, 0.9
y0, y1 = x0**2, x1**2
ax.fill_between([x0, x1], [0, 0], [y0, y0], color=C.LIGHT, zorder=1)
ax.plot([x0, x1, x1, x0, x0], [0, 0, y0, y0, 0], color=C.INK, lw=1.2)
xx = np.linspace(x0, x1, 120)
ax.fill_between(xx, y0, xx**2, color=C.GRAY, alpha=0.55, zorder=2)
ax.plot([x0, x1], [y1, y1], color=C.INK, ls="--", lw=1.1)
ax.plot([x1, x1], [0, y1], color=C.INK, ls="--", lw=1.0)
ax.plot([x0, x1], [y0, y0], color=C.INK, lw=1.1)
label(ax, r"$x$", (x0, 0), offset=(-3, -18), ha="right")
label(ax, r"$x+\mathrm{d}x$", (x1, 0), offset=(3, -18), ha="left")
label(ax, r"$x^2$", (0, y0), offset=(-38, 0), ha="right", va="center")
label(ax, r"$(x+\mathrm{d}x)^2$", (0, y1), offset=(-38, 0), ha="right", va="center")
label(ax, r"$x^2\,\mathrm{d}x$", ((x0+x1)/2, y0/2), ha="center", va="center")
label(ax, "漏掉的一小块", (0.76, 0.53), offset=(4, 4), ha="center")
label(ax, r"$y=x^2$", (1.02, 1.02), offset=(3, 2))
ax.set(xlim=(-0.18, 1.32), ylim=(-0.16, 1.13), aspect="equal")
ax.set_xticks([]); ax.set_yticks([])
save(fig, "C13-n1")

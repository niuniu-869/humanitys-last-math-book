import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Ellipse, Rectangle, FancyArrowPatch

fig, axes = new_fig(15.5, 6.5, ncols=2)
ax = axes[0]
x = np.linspace(0, 2, 400); f = 2 - x**2/2
ax.fill_between(x, 0, f, color=C.LIGHT)
ax.plot(x, f, color=C.INK, lw=1.7)
ax.axvline(0, color=C.INK, lw=2.0, ls="-." )
label(ax, "旋转轴", (0, 1.65), offset=(12, 0), va="center")
x0 = 1.2; f0 = 2 - x0**2/2; dx = 0.16
ax.fill_between([x0-dx/2, x0+dx/2], [0, 0], [f0, f0], color=C.GRAY, alpha=0.7)
ax.plot([x0-dx/2, x0-dx/2, x0+dx/2, x0+dx/2], [0, f0, f0, 0], color=C.INK, lw=1.2)
label(ax, "$x$", (x0, 0), offset=(-3, -18), ha="center")
label(ax, "$f(x)$", (x0+dx/2, f0), offset=(5, -2))
label(ax, r"$\mathrm{d}x$", (x0, f0/2), offset=(5, 0))
ax.set(xlim=(-0.35, 2.3), ylim=(-0.2, 2.25), aspect="equal"); ax.set_xticks([]); ax.set_yticks([])

ax = axes[1]
cx, cy, rad, h = 1.15, 1.2, 0.78, 1.55
ax.add_patch(Ellipse((cx, cy+h/2), 2*rad, 0.34, facecolor=C.LIGHT, edgecolor=C.INK, lw=1.2))
ax.add_patch(Ellipse((cx, cy-h/2), 2*rad, 0.34, facecolor=C.PAPER, edgecolor=C.INK, lw=1.2))
ax.plot([cx-rad, cx-rad], [cy-h/2, cy+h/2], color=C.INK, lw=1.2)
ax.plot([cx+rad, cx+rad], [cy-h/2, cy+h/2], color=C.INK, lw=1.2)
ax.plot([cx+rad+0.2, cx+rad+0.2], [cy-h/2, cy+h/2], color=C.INK, ls="--", lw=1.0)
label(ax, "剪开", (cx+rad+0.2, 1.55), offset=(8, 0), va="center")
rx, ry, rw, rh = 3.05, 0.45, 1.55, 1.55
ax.add_patch(Rectangle((rx, ry), rw, rh, facecolor=C.LIGHT, edgecolor=C.INK, lw=1.2))
ax.plot([rx+0.18, rx+0.18], [ry, ry+rh], color=C.INK, lw=1.0)
ax.annotate("", xy=(rx, ry+rh/2), xytext=(cx+rad+0.2, cy), arrowprops=dict(arrowstyle="-|>", color=C.INK, lw=1.1, ls="--"))
label(ax, r"长 $2\pi x$", (rx+rw/2, ry), offset=(0, -17), ha="center")
label(ax, r"宽 $f(x)$", (rx+rw, ry+rh/2), offset=(6, 0), va="center")
label(ax, r"厚 $\mathrm{d}x$", (rx+0.09, ry+rh), offset=(0, 10), ha="center", va="bottom")
ax.set(xlim=(0.0, 5.1), ylim=(-0.25, 3.1), aspect="equal"); ax.set_xticks([]); ax.set_yticks([])
save(fig, "C13-n4")
